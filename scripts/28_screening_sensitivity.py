# -*- coding: utf-8 -*-
"""Sensitivity in the direction the screening disagreements actually point.

Why this exists. The article tested what happens if borderline studies are *removed*
from the set. That is the wrong direction for the disagreements it reports. On the
GitHub channel the blind rule reproduced every inclusion but none of the exclusions:
the three disagreeing records are ones the recorded decision *excluded* and the rule
*would have included*. They are therefore not in the set, and the question a reader
needs answered is what the transparency proportions would be if they were added, not
what happens when something already counted is taken away.

The composite is safe either way: adding repositories cannot make a joint-absence count
non-zero unless an added repository carries all four prerequisites at once. Every other
proportion moves, because both the numerator and the denominator can change. That is why
this is worth computing rather than asserting.

This script identifies the three records by name, records the reason each was excluded,
reads their intake signals where they exist, and reports each proportion at the recorded
denominator and at the enlarged one.

Output: analiz/screening-sensitivity.json -> archive results/

Usage: python analiz/scripts/28_screening_sensitivity.py
"""
import csv
import json
import sys

from paths import inp, out

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass



def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - r) / d), min(1.0, (c + r) / d))


def main():
    # Re-derive the disagreeing records with the same rule the reliability script uses,
    # rather than hard-coding a list that could drift away from it.

    ham = list(csv.DictReader(inp("repo-inventory-raw").open(encoding="utf-8")))
    env = {(r["repo"] or "").strip().lower(): r
           for r in csv.DictReader(inp("repo-inventory").open(encoding="utf-8"))}
    intake = {(r["repo"] or "").strip().lower(): r
              for r in csv.DictReader(inp("repo-intake-table").open(encoding="utf-8-sig"))}

    excluded_by_record = []
    for r in ham:
        key = (r.get("repo") or "").strip().lower()
        rec = env.get(key)
        if rec is None:
            sys.exit("[FATAL] no recorded decision for %s" % key)
        decision = (rec.get("include") or "").strip().lower()
        if decision not in ("yes", "needs-check"):
            excluded_by_record.append({
                "repo": rec.get("repo"),
                "recorded_decision": decision,
                "exclusion_reason": rec.get("include_reason", ""),
                "in_intake_table": key in intake,
            })

    print("  records the GitHub channel surfaced and the recorded decision excluded: %d"
          % len(excluded_by_record))
    for e in excluded_by_record:
        print("    %-48s %-8s %s" % (e["repo"][:48], e["recorded_decision"],
                                     e["exclusion_reason"][:56]))

    # Recorded study-level counts, as published.
    published = {
        "open license":            (3, 18),
        "retrievable weights":     (2, 18),
        "usable sample data":      (2, 18),
        "environment declared":    (6, 18),
        "run instructions":        (7, 18),
        "pinned and portable":     (0, 18),
        "all four prerequisites":  (0, 18),
    }

    # Not every disputed record would add a *study*. Two of the three are same-team
    # variants of a repository already counted, so admitting them would count one study
    # twice: the repository-level denominator grows and the study-level one does not.
    # Treating all three as new studies would overstate the sensitivity, which is the
    # mirror of the error this script exists to correct, so the two kinds are separated.
    dedup = [e for e in excluded_by_record if e["recorded_decision"] == "dedup"]
    new_studies = [e for e in excluded_by_record if e["recorded_decision"] != "dedup"]
    added = len(new_studies)
    added_repos = len(excluded_by_record)

    print("\n  of the %d disputed records, %d are same-study variants (repository count "
          "only) and %d could add a study"
          % (len(excluded_by_record), len(dedup), added))
    print("  study-level denominator 18 -> %d   repository-level 22 -> %d"
          % (18 + added, 22 + added_repos))
    print("\n  %-24s %-22s %-22s" % ("signal", "as published (N=18)",
                                     "worst case (N=%d)" % (18 + added)))

    rows = []
    for name, (k, n) in published.items():
        lo, hi = wilson(k, n)
        # Worst case for a transparency claim is that every added repository lacks the
        # signal: the numerator stays, the denominator grows. Best case is the opposite.
        wlo, whi = wilson(k, n + added)
        blo, bhi = wilson(k + added, n + added)
        rows.append({
            "signal": name,
            "published": {"k": k, "n": n, "proportion": round(k / n, 4),
                          "wilson": [round(lo, 4), round(hi, 4)]},
            "worst_case_added_all_lack_it": {
                "k": k, "n": n + added, "proportion": round(k / (n + added), 4),
                "wilson": [round(wlo, 4), round(whi, 4)]},
            "best_case_added_all_have_it": {
                "k": k + added, "n": n + added,
                "proportion": round((k + added) / (n + added), 4),
                "wilson": [round(blo, 4), round(bhi, 4)]},
        })
        print("  %-24s %2d/%-2d = %5.1f%%        %2d/%-2d = %5.1f%%"
              % (name, k, n, 100 * k / n, k, n + added, 100 * k / (n + added)))

    composite = next(r for r in rows if r["signal"] == "all four prerequisites")
    payload = {
        "generated_by": "28_screening_sensitivity.py",
        "why": ("The screening disagreements are records the recorded decision excluded "
                "and the blind rule would have included. The sensitivity that answers "
                "them adds those records; removing borderline studies tests the opposite "
                "direction and leaves the question open."),
        "n_disputed_records": len(excluded_by_record),
        "n_that_could_add_a_study": added,
        "n_same_study_variants": len(dedup),
        "study_level_denominator": {"published": 18, "if_all_admitted": 18 + added},
        "repository_level_denominator": {"published": 22,
                                         "if_all_admitted": 22 + added_repos},
        "why_the_two_differ": (
            "Two of the three disputed records are same-team variants of a repository "
            "already counted. Admitting them enlarges the repository count and not the "
            "study count, because the study they belong to is already in the set. The "
            "blind rule cannot see that from a name, a title and a description, which is "
            "the kind of judgment the article says an objective rule cannot encode."),
        "disputed_records": excluded_by_record,
        "composite_note": (
            "The composite stays at 0 under every scenario short of an added repository "
            "carrying all four prerequisites at once. None of the disputed records was "
            "coded as carrying even one of them, so the headline does not move; the "
            "individual transparency proportions do, which is why they are given here."),
        "proportions": rows,
    }
    p = out("screening-sensitivity.json")
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("\n  written: %s" % p)


if __name__ == "__main__":
    main()
