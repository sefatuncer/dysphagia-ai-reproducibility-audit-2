#!/usr/bin/env python3
"""
09_census_synthesis.py - the transparency and verdict synthesis (v3).

WHAT CHANGED IN v3, AND WHY IT MATTERS
--------------------------------------
Until v3 the 22 x 6 signal matrix was a literal inside this file. That is the defect
this study audits, one level up: the headline proportions were re-derived on every run
from a table nobody could check against the intake record, and the two were free to
disagree. They did. Two repositories with the identical recorded signal
(`data_dir=datasets/`) carried opposite sample-data codes, and re-verification found the
literal wrong in both directions on five repositories.

The matrix now lives in the intake table, which is released, and this script reads it.
Nothing here is hand-entered. Where a signal has its own measurement script, this script
cross-checks the released measurement against the table and stops on a mismatch rather
than reporting a number the archive contradicts.

Two units are reported. The study level (N=18) is primary: repository variants from the
same team are clustered on study_id, and a study carries a signal if any of its
repositories carries it, which is the reading most favourable to the audited literature.
The repository level (N=22) is a sensitivity view. A second sensitivity view drops the
repositories that no scripted channel surfaced.

Input : repo-intake-table (via paths.py); rs-taxonomy-coding for the study labels;
        sample-data-audit.json for the cross-check, if it has been produced
Output: census-synthesis.json and included-studies.csv
Network: none.
"""
import csv
import json
import math
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out, RESULTS

Z = 1.959963985

SIGNALS = [
    ("license_open",     "Open license"),
    ("weights_in_repo",  "Weights in repo"),
    ("weights_anywhere", "Weights (any host)"),
    ("env_spec",         "Environment file"),
    ("sample_data",      "Usable sample data"),
]
# Ranked best-first: a study takes the best verdict among its repositories.
VERDICT_RANK = {"re_executable": 3, "partial": 2, "not_reproduced": 1,
                "not_attemptable": 0}


def wilson(k, n):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = (Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def load_included():
    rows = [r for r in csv.DictReader(inp("repo-intake-table").open(encoding="utf-8-sig"))
            if (r.get("included") or "").strip() == "yes"]
    if not rows:
        sys.exit("09: the intake table has no rows marked included=yes")
    for r in rows:
        for col, _ in SIGNALS:
            v = (r.get(col) or "").strip()
            if v not in ("0", "1"):
                sys.exit("09: %s has a non-binary %s (%r); the intake table is the "
                         "source for this signal and must be complete"
                         % (r["repo"], col, v))
            r[col] = int(v)
        if not (r.get("study_id") or "").strip():
            sys.exit("09: %s has no study_id; clustering cannot be checked" % r["repo"])
    return rows


def crosscheck_sample_data(rows):
    """The sample-data signal has its own measurement script. If its output is present,
    the table must agree with it; a silent disagreement between a released measurement
    and a released table is the failure mode this study reports in others."""
    path = RESULTS / "sample-data-audit.json"
    if not path.exists():
        print("  note: sample-data-audit.json not present, cross-check skipped "
              "(run script 23 to enable it)")
        return
    measured = {}
    for x in json.loads(path.read_text(encoding="utf-8")).get("repositories", []):
        if x.get("sample_data_usable") in (0, 1):
            measured[x["repo"]] = x["sample_data_usable"]
    bad = [(r["repo"], r["sample_data"], measured[r["repo"]])
           for r in rows if r["repo"] in measured and r["sample_data"] != measured[r["repo"]]]
    if bad:
        for repo, table, meas in bad:
            print("  MISMATCH %s: table says %d, script 23 measured %d" % (repo, table, meas))
        sys.exit("09: the intake table disagrees with the released sample-data "
                 "measurement; fix one of them, do not report either.")
    print("  cross-check: sample-data coding agrees with script 23 for %d repositories"
          % sum(1 for r in rows if r["repo"] in measured))


def by_study(rows, col):
    studies = {}
    for r in rows:
        studies[r["study_id"]] = studies.get(r["study_id"], 0) or r[col]
    return sum(studies.values()), len(studies)


def best_verdicts(rows):
    best = {}
    for r in rows:
        sid, v = r["study_id"], r["verdict"]
        if sid not in best or VERDICT_RANK.get(v, 0) > VERDICT_RANK.get(best[sid], 0):
            best[sid] = v
    return best


def report(title, rows, unit):
    print("\n" + "=" * 70)
    print("%s  (N=%d %s)" % (title, len(set(r["study_id"] for r in rows))
                             if unit == "studies" else len(rows), unit))
    print("=" * 70)
    print("%-22s%9s%8s%18s" % ("Transparency item", "k/N", "rate", "  Wilson 95% CI"))
    print("-" * 70)
    block = {}
    for col, label in SIGNALS:
        k, n = by_study(rows, col) if unit == "studies" else (sum(r[col] for r in rows), len(rows))
        p, lo, hi = wilson(k, n)
        print("%-22s%9s%8.2f%18s" % (label, "%d/%d" % (k, n), p, "[%.2f, %.2f]" % (lo, hi)))
        block[col] = {"k": k, "n": n, "wilson": [round(lo, 4), round(hi, 4)]}
    best = best_verdicts(rows)
    counts = Counter(best.values()) if unit == "studies" else Counter(r["verdict"] for r in rows)
    n = len(best) if unit == "studies" else len(rows)
    print("-" * 70)
    print("  verdicts: " + " · ".join("%s=%d" % (v, counts.get(v, 0))
                                      for v in VERDICT_RANK))
    block["verdicts"] = {v: counts.get(v, 0) for v in VERDICT_RANK}
    block["n"] = n
    return block


def write_included_studies(rows):
    """The study-level table the article points at. Without it a reader cannot even
    enumerate the audited set, which is the objection this file answers."""
    labels = {}
    try:
        for r in csv.DictReader(inp("rs-taxonomy-coding").open(encoding="utf-8-sig")):
            labels[r["study_id"].strip()] = (r.get("paper", "").strip(),
                                             r.get("RS1_refstd_type", "").strip())
    except SystemExit:
        print("  note: clinical coding not found; study labels left blank")

    best = best_verdicts(rows)
    per = {}
    for r in rows:
        s = per.setdefault(r["study_id"], {"repos": [], "dates": set()})
        s["repos"].append(r["repo"])
        if r.get("check_date"):
            s["dates"].add(r["check_date"])
        for col, _ in SIGNALS:
            s[col] = max(s.get(col, 0), r[col])
        s["channel"] = r.get("discovery_channel", "")

    path = RESULTS / "included-studies.csv"
    cols = (["study_id", "paper", "reference_standard", "repositories", "n_repositories",
             "discovery_channel", "access_dates"] + [c for c, _ in SIGNALS] + ["verdict"])
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for sid in sorted(per):
            s = per[sid]
            paper, refstd = labels.get(sid, ("", ""))
            row = {"study_id": sid, "paper": paper, "reference_standard": refstd,
                   "repositories": "; ".join(sorted(s["repos"])),
                   "n_repositories": len(s["repos"]),
                   "discovery_channel": s["channel"],
                   "access_dates": "; ".join(sorted(s["dates"])),
                   "verdict": best[sid]}
            row.update({c: s[c] for c, _ in SIGNALS})
            w.writerow(row)
    print("  written: %s  (%d studies)" % (path, len(per)))
    return path


def main():
    rows = load_included()
    crosscheck_sample_data(rows)

    study = report("PRIMARY: STUDY LEVEL", rows, "studies")
    repo = report("SENSITIVITY: REPOSITORY LEVEL", rows, "repositories")
    scripted = [r for r in rows if r.get("discovery_channel") != "carried"]
    scr = report("SENSITIVITY: SCRIPTED-ONLY (carried-forward repositories dropped)",
                 scripted, "studies")
    # The instrument's unit is a code-linked artifact set, and for most of them we could
    # not tie the repository to an identified publication. Reporting the subset where we
    # could is what keeps the phrase "published models" from covering the whole set.
    published = [r for r in rows if (r.get("publication_confirmed") or "") == "yes"]
    pub = report("SENSITIVITY: PUBLICATION-CONFIRMED SUBSET", published, "studies")

    write_included_studies(rows)

    payload = {
        "unit_primary": "study",
        "n_studies": study["n"], "n_repositories": repo["n"],
        "study_level": study, "repository_level": repo, "scripted_only": scr,
        "publication_confirmed": pub,
        "note": ("re_executable is 0 at every level; it is a conjunction fixed by its "
                 "scarcest prerequisite, not a count of observed run failures"),
    }
    dest = out("census-synthesis.json")
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("\n  written: %s" % dest)


if __name__ == "__main__":
    main()
