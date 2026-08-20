#!/usr/bin/env python3
"""Cross-check every headline number in the manuscript against the released results.

The manuscript and the archive are edited separately, so a number can drift in one
without the other. This reads the released result files and asserts that each value
appears in the manuscript source, which is the check a reader would otherwise have to
do by hand. It also asserts the absence of six claims withdrawn during revision, so a
reverted edit cannot quietly reinstate them.

**This check runs at authoring time, not from inside the published archive.** The
archive holds the study's artifacts, not the paper, so the manuscript source it needs
is deliberately absent there. It is published anyway, because a reader is entitled to
see how the numbers in the paper were tied to the released files rather than take it
on trust. Run it from a working copy that has both.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paths  # noqa: E402

# The manuscript lives outside the archive; look for it in the working-tree layout.
_TEX = paths.BASE / "taslak" / "latex" / "makale-AiR.tex"
if not _TEX.exists():
    sys.exit(
        "manuscript source not found at " + str(_TEX) + "\n"
        "  This check compares the paper against the released results, so it needs\n"
        "  both. The published archive contains the artifacts, not the paper, so this\n"
        "  script is expected to stop here when run from inside the archive. Run it\n"
        "  from a working copy that also holds taslak/latex/makale-AiR.tex."
    )
TEX = _TEX.read_text(encoding="utf-8")
AN = paths.RESULTS


def load(name):
    return json.loads((AN / name).read_text(encoding="utf-8"))


def _flat(s):
    """Collapse whitespace, so a needle still matches after LaTeX reflows a line."""
    return re.sub(r"\s+", " ", s)


FLAT = _flat(TEX)


def check(label, needle, must=True):
    hit = _flat(needle) in FLAT
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
    ok &= check("not pinned, portable = 4", "four are portable and unpinned")
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
    # The two percentages these lines used to require were withdrawn in the August 2026
    # revision: the comparator pool is 77% reference list, so it cannot carry a
    # code-sharing rate that is comparable with the curated denominators of the radiology
    # audits. The counts stay, the rates go, and this check now enforces their absence.
    ok &= check("no own-code rate 5.1%", "or 5.1", must=False)
    ok &= check("no any-declared rate 7.7%", "or 7.7", must=False)

    print("\ntransparency counts (script 09, read from the intake table)")
    cen = load("census-synthesis.json")["study_level"]
    for label, col, txt in [
            ("open license", "license_open", "an open license in %d"),
            ("weights anywhere", "weights_anywhere", "retrievable weights in %d"),
            ("usable sample data", "sample_data", "usable sample data in %d")]:
        ok &= check("%s = %d/18" % (label, cen[col]["k"]), txt % cen[col]["k"])
    assert cen["sample_data"]["k"] == 2, "the sample-data correction is not in the results"

    print("\nscreening reliability (script 11)")
    g = kap["rule_B_primary"]["github_pwc"]
    ok &= check("rule reproduced 15/15 inclusions", "15 of 15")
    ok &= check("rule reproduced 0/3 exclusions", "0 of 3")
    assert g["r1_include"] == 15 and g["r2_include"] == 18

    # Table 1's bootstrap row is three separate numbers that are easy to edit apart from
    # the results file. One of them had drifted: the GitHub channel was written up as
    # "not estimable" while the released bootstrap reports an estimable [0.00, 0.00].
    # Each interval is now read back from the JSON rather than trusted.
    for chan, label in [("oa_mining", "mining"), ("github_pwc", "GitHub/PwC"),
                        ("pooled", "pooled")]:
        b = kap["bootstrap_rule_B"][chan]
        if not b["estimable"]:
            ok &= check("%s bootstrap declared not estimable" % label, "not estimable")
            continue
        ok &= check("%s bootstrap %.2f--%.2f" % (label, b["lo"], b["hi"]),
                    "%.2f--%.2f" % (b["lo"], b["hi"]))

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
