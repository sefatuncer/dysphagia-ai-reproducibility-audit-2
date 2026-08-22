#!/usr/bin/env python3
"""
24_rs_coding_evidence.py - turn the clinical coding into a checkable evidence file.

WHY THIS SCRIPT EXISTS
----------------------
The RS1-RS6 coding was done by one clinician and there is no second coder in a
two-author team, so it carries no agreement statistic. An agreement coefficient would
not have helped in any case: on RS4 every study in the assessable subset takes the same
value, so the marginal is degenerate and kappa is undefined for the same reason it is
uninformative in the screening table.

What a reader actually needs is not a coefficient but the ability to check a code. This
script emits one row per study per item, carrying the code, the basis recorded for it
(quoted from the source text where the item turns on a statement), and how firm that
basis is. Reliability is not claimed; auditability is provided instead, and the two are
different remedies for different problems.

The evidence_level column is carried through unchanged and matters: `fulltext-verified`
and `abstract+fulltext` rest on the source text, while `inventory-only` records that no
paper could be matched to the repository, so the code is an inference from the modality
and should be read as such.

Input : rs-taxonomy-coding (via paths.py)
Output: rs-coding-evidence.csv
Network: none.
"""
import csv
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

SRC = inp("rs-taxonomy-coding")
OUT = out("rs-coding-evidence.csv")

# item -> (column holding the code, column holding the recorded basis, who assigned it)
# RS2 and RS5 carry the clinician marker in the source header, so they are reported as
# judgment items rather than text-verifiable ones; the manuscript says the same.
# RS1, RS2 and RS5 used to pass None here, so three of the five items reached the
# published file with an empty basis, which is 54 of its 90 rows and includes both
# judgment items. The manuscript states that every code is released beside the basis
# recorded for it, so that gap made a published claim false. The source now carries an
# evidence column for each of the three, holding what the paper states rather than a
# rationale written on the clinician's behalf.
ITEMS = [
    ("RS1 reference-standard type", "RS1_refstd_type", "RS1_evidence", "text-verifiable"),
    ("RS2 target validity and surrogate substitution",
     "RS2_proxy_leakage_[NKT]", "RS2_evidence", "clinician judgment"),
    ("RS3 label scale and granularity", "RS3_scale_granularity", "RS3_binarized",
     "text-verifiable"),
    ("RS4 label reliability", "RS4_rater_reliability_reported", "RS4_evidence",
     "text-verifiable"),
    ("RS5 spectrum", "RS5_spectrum_[NKT]", "RS5_evidence", "clinician judgment"),
]


def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
    out_rows = []
    for r in rows:
        for label, code_col, basis_col, kind in ITEMS:
            code = (r.get(code_col) or "").strip()
            if not code:
                continue
            basis = (r.get(basis_col) or "").strip() if basis_col else ""
            out_rows.append({
                "study_id": r.get("study_id", "").strip(),
                "study": r.get("study", "").strip(),
                "paper": r.get("paper", "").strip(),
                "item": label,
                "code": code,
                "recorded_basis": basis,
                "assigned_by": kind,
                "evidence_level": r.get("evidence_level", "").strip(),
                # Corrections travel with the data rather than only in the paper, so a
                # reader sees what changed without diffing two releases.
                "correction_2026_08_22": r.get("correction_2026-08-22", "").strip(),
            })

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    studies = {r["study_id"] for r in out_rows}
    assessable = {r["study_id"] for r in out_rows
                  if r["evidence_level"] in ("fulltext-verified", "abstract+fulltext")}
    quoted = sum(1 for r in out_rows if "'" in r["recorded_basis"]
                 or '"' in r["recorded_basis"])
    print("  studies coded            : %d" % len(studies))
    print("  of which text-assessable : %d  (the k reported in the manuscript)"
          % len(assessable))
    print("  coded rows written       : %d" % len(out_rows))
    print("  rows carrying a quotation: %d" % quoted)
    print("  written: %s" % OUT)


if __name__ == "__main__":
    main()
