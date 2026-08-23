# -*- coding: utf-8 -*-
"""Every transparency signal for the subset whose publication could be confirmed.

Why this exists. The article promises that "every headline is also reported for those 7",
and then reports five of the seven signals for that subset and not the other two. Run
instructions and the model-card row were given only at N=18. This script computes the
whole column so the promise is kept, and so a reader can see that the subset is not
uniformly better than the full set.

How the subset is defined. A study counts as publication-confirmed when the study-level
table names a journal and year rather than a placeholder ("unclear", "could not be
confirmed", "needs-check", "scoping candidate"). That test is applied here to the
released table rather than to a hard-coded list, so it stays true if the table changes.

Output: analiz/publication-confirmed-subset.json -> archive results/

Usage: python analiz/scripts/29_publication_confirmed_subset.py
"""
import csv
import json
import re
import sys

from paths import inp, out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# A paper field that contains any of these is a placeholder, not a citation.
UNCONFIRMED = ("unclear", "could not be confirmed", "needs-check", "scoping candidate")


def is_confirmed(paper):
    p = (paper or "").strip().lower()
    if not p:
        return False
    if any(u in p for u in UNCONFIRMED):
        return False
    # A confirmed entry names a venue and a year.
    return bool(re.search(r"(19|20)\d{2}", p))


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - r) / d), min(1.0, (c + r) / d))


def main():
    studies = list(csv.DictReader(
        result("included-studies.csv").open(encoding="utf-8-sig")))
    confirmed = [s for s in studies if is_confirmed(s.get("paper"))]
    ids = sorted(s["study_id"] for s in confirmed)
    print("  studies: %d   publication-confirmed: %d  (%s)"
          % (len(studies), len(confirmed), " ".join(ids)))

    # Run instructions live in their own audit, at the repository level.
    ri = json.loads(result("run-instructions-audit.json").read_text(encoding="utf-8"))
    by_study = {}
    for r in ri["repository_level"]:
        by_study.setdefault(str(r.get("study", "")).strip(), []).append(
            bool(r.get("command_found")))
    run_instr = {s: any(v) for s, v in by_study.items()}

    def count(rows, field):
        return sum(1 for r in rows if (r.get(field) or "").strip() == "1")

    n7, n18 = len(confirmed), len(studies)
    rows = [
        ("Open license",           count(confirmed, "license_open"),
                                   count(studies, "license_open")),
        ("Retrievable weights",    count(confirmed, "weights_anywhere"),
                                   count(studies, "weights_anywhere")),
        ("Usable sample data",     count(confirmed, "sample_data"),
                                   count(studies, "sample_data")),
        ("Environment declared",   count(confirmed, "env_spec"),
                                   count(studies, "env_spec")),
        ("Run instructions",       sum(1 for s in confirmed
                                       if run_instr.get(s["study_id"], False)),
                                   sum(1 for s in studies
                                       if run_instr.get(s["study_id"], False))),
        # The model-card row was hand-coded and found in none; there is no released
        # script behind it, and the article says so. It is carried here unchanged rather
        # than recomputed, because recomputing it would imply a measurement that was
        # never scripted.
        ("Model card or datasheet", 0, 0),
    ]

    out_rows = []
    print("\n  %-24s %-18s %-18s" % ("signal", "confirmed (n=%d)" % n7,
                                     "all studies (N=%d)" % n18))
    for name, k7, k18 in rows:
        lo7, hi7 = wilson(k7, n7)
        out_rows.append({
            "signal": name,
            "publication_confirmed": {"k": k7, "n": n7,
                                      "wilson": [round(lo7, 4), round(hi7, 4)]},
            "all_studies": {"k": k18, "n": n18},
        })
        print("  %-24s %2d/%-2d = %5.1f%%     %2d/%-2d = %5.1f%%"
              % (name, k7, n7, 100 * k7 / n7, k18, n18, 100 * k18 / n18))

    payload = {
        "generated_by": "29_publication_confirmed_subset.py",
        "subset_rule": ("The study-level table names a venue and a year, rather than a "
                        "placeholder such as 'unclear' or 'could not be confirmed'."),
        "publication_confirmed_ids": ids,
        "n_publication_confirmed": n7,
        "n_all_studies": n18,
        "composite_all_four": {"publication_confirmed": 0, "all_studies": 0},
        "note": ("The subset is selected on retrievability, which is if anything "
                 "associated with fuller reporting, so it should be read as a best case "
                 "for the full set rather than a representative sample of it. The run "
                 "instruction row is the one where the two differ appreciably, in the "
                 "direction that selection predicts."),
        "rows": out_rows,
    }
    p = out("publication-confirmed-subset.json")
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("\n  written: %s" % p)


if __name__ == "__main__":
    main()
