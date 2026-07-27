#!/usr/bin/env python3
"""
11_screening_kappa.py — inter-coder reliability of the scope screening.

Rater 1 = the recorded scope decisions in the released candidate list
          (`analiz/repo-envanteri-ek.csv`, column `include`).
Rater 2 = an INDEPENDENT, BLIND, rule-based re-application of the pre-stated
          inclusion rule (this script), using only OBJECTIVE features
          (repository type, repository name, paper title) and NOT the recorded
          decisions or the human reviewer's free-text `notes`.

Reports simple agreement, Cohen's kappa, and PABAK (prevalence-and-bias-adjusted
kappa, appropriate here because the marginals are highly skewed toward exclusion).
This is an AUTOMATED reliability check — reported honestly as such, not as a
second human reader. Fixed, deterministic; no randomness.
"""
import csv, sys
from pathlib import Path
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

CSV = Path(__file__).resolve().parents[1] / "repo-envanteri-ek.csv"

# Objective operationalization of the inclusion rule (blind to rater-1 labels/notes).
TOOL_LIBS = (
    "yolo", "opencv", "labelme", "labelimg", "opensmile", "silero", "soxr",
    "ggplot", "/bwa", "trimmomatic", "dcm2niix", "h2o-3", "/h2o", "econml",
    "boxmot", "medcat", "darknet", "deepwalk", "decagon", "knowddi",
    "graphembedding", "pygat", "/gat", "skipgnn", "/line", "/deepwalk",
)
SCOPE_KW = ("dysphag", "swallow", "deglutit", "aspiration", "penetrat", "vfss", "fees")


def rater2_blind(row) -> int:
    """Independent rule-based decision: include (1) / exclude (0)."""
    if (row.get("type") or "").strip().lower() != "code":
        return 0                                   # archive/data link, not a code repo
    name = (row.get("repo") or "").lower()
    if any(lib in name for lib in TOOL_LIBS):
        return 0                                   # widely used tool/library citation
    title = (row.get("paper") or "").lower()
    if any(k in title for k in SCOPE_KW):
        return 1                                   # in-scope study code repo
    return 0                                       # code repo but not scope-relevant


def rater1(row) -> int:
    return 1 if (row.get("include") or "").strip().lower() in ("yes", "borderline", "y") else 0


def cohen_kappa(a, b):
    n = len(a)
    both1 = sum(1 for x, y in zip(a, b) if x == 1 and y == 1)
    both0 = sum(1 for x, y in zip(a, b) if x == 0 and y == 0)
    a1b0 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    a0b1 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    po = (both1 + both0) / n
    p_a1, p_b1 = (both1 + a1b0) / n, (both1 + a0b1) / n
    p_a0, p_b0 = 1 - p_a1, 1 - p_b1
    pe = p_a1 * p_b1 + p_a0 * p_b0
    kappa = (po - pe) / (1 - pe) if pe != 1 else float("nan")
    pabak = 2 * po - 1                              # prevalence-and-bias-adjusted kappa
    return dict(n=n, both1=both1, both0=both0, a1b0=a1b0, a0b1=a0b1,
                po=po, pe=pe, kappa=kappa, pabak=pabak)


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    r1 = [rater1(r) for r in rows]
    r2 = [rater2_blind(r) for r in rows]
    k = cohen_kappa(r1, r2)
    print("=" * 60)
    print(f"SCREENING RELIABILITY (open-access mining channel, n={k['n']})")
    print("  Rater 1 = recorded decisions; Rater 2 = blind rule-based re-coding")
    print("-" * 60)
    print(f"  agree include (1,1): {k['both1']}   agree exclude (0,0): {k['both0']}")
    print(f"  disagree (r1=1,r2=0): {k['a1b0']}   disagree (r1=0,r2=1): {k['a0b1']}")
    print(f"  simple agreement (Po): {k['po']:.3f} ({100*k['po']:.1f}%)")
    print(f"  chance agreement (Pe): {k['pe']:.3f}")
    print(f"  Cohen's kappa: {k['kappa']:.3f}")
    print(f"  PABAK:         {k['pabak']:.3f}   (skewed marginals -> report alongside kappa)")
    print("=" * 60)
    print("Rater-1 include count:", sum(r1), "| Rater-2 include count:", sum(r2))


if __name__ == "__main__":
    main()
