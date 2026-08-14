#!/usr/bin/env python3
"""Re-run the released analysis and check that it reproduces the published results.

    python scripts/reproduce.py                 # offline steps only (default)
    python scripts/reproduce.py --with-network  # also re-measure the live-read steps

Two kinds of step:

  offline   Scripts 11 and 21 read only released files. Their outputs must match
            the committed results byte-for-value; if they do not, something in
            the archive has drifted and the run fails.

  network   Scripts 12, 13, 19 and 20 query live services (GitHub,
            raw.githubusercontent.com, Crossref, Europe PMC) at a logged access
            date. Re-running them today can legitimately return different values,
            because repositories and databases change between the access date and
            now. They are therefore re-run only on request, and a difference is
            reported as a difference, not as a failure.

This script is the answer to a question a reader of an audit like this one is
entitled to ask: does the pipeline that produced the reported numbers actually
run, from the archive as published, on a machine that is not the authors'?
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paths  # noqa: E402  (needs HERE on the path first)

OFFLINE = [
    ("11_screening_kappa.py", "screening-reliability.json"),
    ("21_reported_numbers.py", "reported-numbers.json"),
]
NETWORK = [
    ("12_truncation_check.py", "truncation-check.json"),
    ("13_backward_coverage.py", "backward-coverage.json"),
    ("19_env_pinning_audit.py", "env-pinning-audit.json"),
    ("20_run_instructions_audit.py", "run-instructions-audit.json"),
]

# Fields that record when a live read happened. A change in these is expected on
# a re-run and is not a difference in the finding.
VOLATILE = {"access_date", "generated", "run_at", "retrieved"}


def strip_volatile(obj):
    if isinstance(obj, dict):
        return {k: strip_volatile(v) for k, v in obj.items() if k not in VOLATILE}
    if isinstance(obj, list):
        return [strip_volatile(v) for v in obj]
    return obj


def load(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def run_step(script, result_name, must_match):
    target = paths.RESULTS / result_name
    before = load(target)

    proc = subprocess.run([sys.executable, str(HERE / script)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()
        return "ERROR", script, "\n".join(tail[-4:])

    after = load(target)
    if after is None:
        return "ERROR", script, f"{result_name} was not written"
    if before is None:
        return "NEW", script, f"{result_name} written (no previous copy to compare)"

    if strip_volatile(before) == strip_volatile(after):
        return "OK", script, f"{result_name} reproduced"
    if must_match:
        return "DIFF", script, (f"{result_name} changed, and this step reads only "
                                f"released files, so it should not have")
    return "CHANGED", script, (f"{result_name} differs from the published values; "
                               f"expected for a live re-read at a later date")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--with-network", action="store_true",
                    help="also re-run the steps that query live services")
    args = ap.parse_args()

    print("=" * 78)
    print("re-running the released analysis")
    print(f"  layout : {paths.LAYOUT}")
    print(f"  results: {paths.RESULTS}")
    print("=" * 78)

    steps = [(s, r, True) for s, r in OFFLINE]
    if args.with_network:
        steps += [(s, r, False) for s, r in NETWORK]
    else:
        print(f"\n  ({len(NETWORK)} live-read steps skipped; pass --with-network to include them)")

    results = []
    for script, result_name, must_match in steps:
        status, name, detail = run_step(script, result_name, must_match)
        results.append(status)
        print(f"\n[{status:7s}] {name}\n          {detail}")

    print("\n" + "=" * 78)
    bad = [s for s in results if s in ("ERROR", "DIFF")]
    if bad:
        print(f"FAILED: {len(bad)} of {len(results)} steps did not reproduce")
        return 1
    print(f"OK: {len(results)} of {len(results)} steps ran and reproduced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
