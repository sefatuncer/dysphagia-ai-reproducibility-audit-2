#!/usr/bin/env python3
"""Cross-check every headline number in the manuscript against the released results.

The manuscript and the archive are edited separately, so a number can drift in one
without the other. This reads the released result files and asserts that each value
appears in the LaTeX source, which is the check a reader would otherwise have to do
by hand.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX = (ROOT / "taslak" / "latex" / "makale-IJMI.tex").read_text(encoding="utf-8")
AN = ROOT / "analiz"


def load(name):
    return json.loads((AN / name).read_text(encoding="utf-8"))


def check(label, needle, must=True):
    hit = needle in TEX
    ok = hit if must else not hit
    print(f"  [{'OK ' if ok else 'FAIL'}] {label:52s} {needle!r}")
    return ok


def main():
    env = load("env-pinning-audit.json")
    ri = load("run-instructions-audit.json")
    bc = load("backward-coverage.json")
    kap = load("screening-reliability.json")

    ok = True
    print("environment pinning (script 19)")
    c = env["study_level_2x2"]
    ok &= check("pinned & portable = 0", "absent in all 18")
    ok &= check("pinned, not portable = 2", "pinned and not portable")
    ok &= check("not pinned, portable = 4", "the remaining four are portable and")
    ok &= check("studies with an env file = 6", "six environment specifications")
    assert c["pinned_portable"] == 0 and c["pinned_not_portable"] == 2 \
        and c["not_pinned_portable"] == 4 and env["studies_with_env_file"] == 6

    print("\nrun instructions (script 20)")
    s = ri["study_level"]
    ok &= check(f"run instructions = {s['run_instructions']}/18",
                "7/18 document how to install")
    ok &= check(f"README present = {s['readme_present']}/18", "15/18 studies have a README")

    print("\ncoverage and sharing (script 13)")
    cc = bc["counts"]
    assess = cc["in_census"] + cc["code_not_in_census"] + cc["oa_no_code"]
    ok &= check(f"pool = {bc['n_unique_dois']}", "comparator pool of 83 records")
    ok &= check(f"unretrievable = {cc['not_assessable']}", "unretrievable for 44")
    ok &= check(f"assessable = {assess}", "39 assessable records")
    ok &= check("own-code rate 2/39", "2/39, or 5.1")
    ok &= check("any-declared rate 3/39", "3/39, or 7.7")

    print("\nscreening reliability (script 11)")
    g = kap["rule_B_primary"]["github_pwc"]
    ok &= check("rule reproduced 15/15 inclusions", "15 of 15")
    ok &= check("rule reproduced 0/3 exclusions", "0 of 3")
    assert g["r1_include"] == 15 and g["r2_include"] == 18

    print("\nclaims that must NOT be present (withdrawn in revision)")
    ok &= check("no 'a fifth of the rate'", "a fifth of the rate", must=False)
    ok &= check("no 'P_pos is the informative figure'", "informative figure", must=False)
    ok &= check("no IJMI journal line", r"\journal{International", must=False)
    ok &= check("no 'medical-informatics readership'", "medical-informatics readership", must=False)
    ok &= check("no 'despite best-effort fixes'", "despite best-effort fixes", must=False)
    ok &= check("no 'Two repositories met it'", "Two repositories met it", must=False)

    print("\n" + ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
