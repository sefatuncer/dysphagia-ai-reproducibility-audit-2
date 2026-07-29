#!/usr/bin/env python3
"""
03_analysis.py — a reproducible implementation of the statistical analysis plan.

Self-contained statistical helpers (no scipy required): Wilson intervals, the Newcombe
interval for a difference of two proportions, and Cohen κ. The script reads the
transparency rubric; while the rubric holds too few rows to analyse (only pilot
repository #1), it DEMONSTRATES that the pipeline works using SYNTHETIC demo rows, and
switches to the real data automatically once enough rows exist. The seed is fixed, so
the run is reproducible — which is the article's own thesis applied to itself.

Usage: PYTHONIOENCODING=utf-8 python analiz/scripts/03_analysis.py
"""
import csv, math, os, random
random.seed(42)
Z = 1.959963985  # 95%

RUBRIC = "analiz/seffaflik-rubrigi.csv"
BINARY_ITEMS = {  # column -> the values counted as sharing / positive
    "code_stmt": {"yes", "explicit-url"},
    "repo_accessible": {"yes"},
    "license": None,   # special case: anything other than NONE counts as present
    "readme_run_instructions": {"yes", "partial"},
    "dependency_file": None,  # special case: anything other than empty/none counts as present
    "random_seed": {"yes"},
    "model_weights": {"yes"},
    "model_card": {"yes"},
    "external_validation": {"yes"},
}

def wilson(k, n):
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    p = k / n
    d = 1 + Z*Z/n
    c = (p + Z*Z/(2*n)) / d
    h = (Z * math.sqrt(p*(1-p)/n + Z*Z/(4*n*n))) / d
    return p, max(0, c-h), min(1, c+h)

def newcombe_diff(k1, n1, k2, n2):
    """Newcombe 95% interval for the difference of two proportions (p1 - p2)."""
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    diff = p1 - p2
    lo = diff - math.sqrt((p1-l1)**2 + (u2-p2)**2)
    hi = diff + math.sqrt((u1-p1)**2 + (p2-l2)**2)
    return diff, lo, hi

def cohen_kappa(pairs):
    """pairs: [(rater1, rater2), ...], categorical."""
    n = len(pairs)
    if n == 0: return float("nan")
    cats = sorted(set(a for a, _ in pairs) | set(b for _, b in pairs))
    po = sum(1 for a, b in pairs if a == b) / n
    m1 = {c: sum(1 for a, _ in pairs if a == c)/n for c in cats}
    m2 = {c: sum(1 for _, b in pairs if b == c)/n for c in cats}
    pe = sum(m1[c]*m2[c] for c in cats)
    return (po - pe) / (1 - pe) if pe != 1 else 1.0

def cohen_kappa_ci(pairs, B=2000):
    """Cohen κ plus a percentile bootstrap 95% interval (SAP §4: a 95% interval for κ
    with the Landis-Koch label). The seed is fixed (random.seed(42)), so the result is
    reproducible. On a small calibration set this shows the uncertainty in κ, where a
    point estimate alone can mislead."""
    k = cohen_kappa(pairs)
    n = len(pairs)
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    boots = []
    for _ in range(B):
        sample = [pairs[random.randrange(n)] for _ in range(n)]
        kb = cohen_kappa(sample)
        if kb == kb:  # i.e. not NaN
            boots.append(kb)
    boots.sort()
    if not boots: return (k, float("nan"), float("nan"))
    lo = boots[int(0.025 * len(boots))]
    hi = boots[min(len(boots)-1, int(0.975 * len(boots)))]
    return (k, lo, hi)

def landis_koch(k):
    for t, lbl in [(0.81,"almost perfect"),(0.61,"substantial"),(0.41,"moderate"),
                   (0.21,"fair"),(0.0,"slight"),(-1,"poor")]:
        if k >= t: return lbl

def positive(col, val):
    val = (val or "").strip().lower()
    if col == "license":
        return val not in ("", "none", "not reported", "na")
    if col == "dependency_file":
        return val not in ("", "none", "not reported", "na")
    return val in BINARY_ITEMS[col]

def load_rows():
    if os.path.exists(RUBRIC):
        rows = list(csv.DictReader(open(RUBRIC, encoding="utf-8")))
        rows = [r for r in rows if r.get("study_id", "").strip()]
        if len(rows) >= 10:
            return rows, False
    # not enough data -> synthetic demo (disabled automatically once real data arrive)
    demo = []
    for i in range(40):
        demo.append({
            "study_id": f"SYN-{i:03d}",
            "code_stmt": random.choice(["yes","none","none","none"]),
            "repo_accessible": random.choice(["yes","no","no"]),
            "license": random.choice(["MIT","NONE","NONE","NONE"]),
            "readme_run_instructions": random.choice(["yes","partial","no","no"]),
            "dependency_file": random.choice(["requirements","none","none"]),
            "random_seed": random.choice(["yes","no","no","no","no"]),
            "model_weights": random.choice(["yes","no","no","no"]),
            "model_card": random.choice(["yes","no","no","no","no","no"]),
            "external_validation": random.choice(["yes","no","no","no"]),
        })
    return demo, True

def main():
    rows, synthetic = load_rows()
    n = len(rows)
    print("="*66)
    print(f"TRANSPARENCY ANALYSIS  (N={n})" + ("  [SYNTHETIC DEMO - awaiting real data]" if synthetic else "  [REAL DATA]"))
    print("="*66)
    print(f"{'Item':26s}{'k/N':>10s}{'rate':>8s}{'  Wilson 95% CI':>18s}")
    print("-"*66)
    results = {}
    for col in BINARY_ITEMS:
        k = sum(1 for r in rows if positive(col, r.get(col)))
        p, lo, hi = wilson(k, n)
        results[col] = (k, n)
        print(f"{col:26s}{f'{k}/{n}':>10s}{p:>8.2f}{f'[{lo:.2f}, {hi:.2f}]':>18s}")
    print("-"*66)

    # Radiology comparison (code sharing). The one verified anchor is Venkatesh 2022 = 73/218 (34%).
    # NOTE: the "deep learning about 11.5% (2025)" figure was removed: it could not be sourced and
    # was misattributed to Lee/Eur Radiol 2025, which in fact reports 39.9%.
    k_code, _ = results["code_stmt"]
    kr, nr = 73, 218  # Venkatesh 2022, Radiol Artif Intell - share of studies with accessible code
    pr, rlo, rhi = wilson(kr, nr)
    print(f"Reference (Venkatesh 2022, radiology): {kr}/{nr} = {pr:.2f}  [{rlo:.2f}, {rhi:.2f}]")
    d, lo, hi = newcombe_diff(k_code, n, kr, nr)
    print(f"Code-sharing difference vs radiology 34%: delta={d:+.2f}  Newcombe95=[{lo:+.2f}, {hi:+.2f}]  (contextual, not causal; definition matched on 'accessible code')")
    print("-"*66)

    # Demo κ (calibration) with a 95% bootstrap interval (SAP §4)
    demo_pairs = [(random.choice(["incl","excl"]), random.choice(["incl","excl","excl"])) for _ in range(50)]
    k, klo, khi = cohen_kappa_ci(demo_pairs)
    print(f"Demo κ (calibration example): κ={k:.2f}  95% CI=[{klo:.2f}, {khi:.2f}]  ({landis_koch(k)})  - will change with real screening data")
    print("="*66)
    print("NOTE: the synthetic rows ONLY verify the pipeline; the script switches to real data")
    print("      automatically once the rubric holds at least 10 rows. Wilson, Newcombe and κ")
    print("      implement SAP §2-5.")

if __name__ == "__main__":
    try:
        import sys; sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()
