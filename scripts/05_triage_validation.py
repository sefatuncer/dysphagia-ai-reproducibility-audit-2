#!/usr/bin/env python3
"""
05_triage_validation.py — validate the triage flags against a human gold standard.

TWO MODES:
1) If no sample exists → draw a stratified random sample of about 200 records from the
   screening worksheet, with a FLOOR on the exclude buckets (the real risk being a false
   exclusion) → analiz/triyaj-validasyon-ornek.csv, which carries an empty
   `human_gold_include` column for two humans to fill in independently.
2) If the sample exists and human_gold is filled in → the sensitivity, specificity and PPV
   of the include/exclude decision implied by triage, plus the confusion matrix.

The seed is fixed, so the sample is reproducible.
"""
import csv, os, random
random.seed(2026)
try:
    import sys; sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

WF = "analiz/tarama-calisma-sayfasi.csv"
SAMPLE = "analiz/triyaj-validasyon-ornek.csv"
TARGET = 200
FLOOR_EXCL = 25   # minimum drawn from each exclude bucket (hunting for false excludes)
FLOOR_OTHER = 15

INCLUDE_BUCKETS = {"likely_include", "needs_review", "needs_review_no_abstract"}

def implied_triage_include(bucket):
    return bucket in INCLUDE_BUCKETS  # grey buckets go to a human, so they count as include-side (favouring recall)

def build_sample():
    rows = list(csv.DictReader(open(WF, encoding="utf-8")))
    by = {}
    for r in rows: by.setdefault(r["t_bucket"], []).append(r)
    n_total = len(rows)
    picked = []
    for b, rs in by.items():
        frac = len(rs) / n_total
        floor = FLOOR_EXCL if b.startswith("likely_exclude") else FLOOR_OTHER
        k = min(len(rs), max(floor, round(TARGET * frac)))
        picked += random.sample(rs, k)
    random.shuffle(picked)
    cols = ["dedup_key", "pmid", "doi", "year", "title", "abstract",
            "t_bucket", "t_has_ai", "t_review_like", "t_modality",
            "human_gold_include", "reviewer", "notes"]
    with open(SAMPLE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in picked:
            r = dict(r); r["human_gold_include"] = ""; r["reviewer"] = ""; r["notes"] = ""
            w.writerow(r)
    print(f"Sample generated: {len(picked)} records -> {SAMPLE}")
    from collections import Counter
    print("  bucket distribution:", dict(Counter(x["t_bucket"] for x in picked)))
    print("  TWO HUMANS fill in `human_gold_include` (yes/no) independently, then re-run.")

def score():
    rows = [r for r in csv.DictReader(open(SAMPLE, encoding="utf-8"))
            if r.get("human_gold_include", "").strip().lower() in ("yes", "no")]
    if len(rows) < 20:
        print(f"{len(rows)} records have human_gold filled in (fewer than 20) -> not scored yet.")
        return
    tp = fp = tn = fn = 0
    for r in rows:
        gold = r["human_gold_include"].strip().lower() == "yes"
        pred = implied_triage_include(r["t_bucket"])
        if gold and pred: tp += 1
        elif not gold and pred: fp += 1
        elif not gold and not pred: tn += 1
        else: fn += 1  # gold says include but triage excludes = FALSE EXCLUSION (the critical error)
    sens = tp/(tp+fn) if tp+fn else float("nan")
    spec = tn/(tn+fp) if tn+fp else float("nan")
    ppv = tp/(tp+fp) if tp+fp else float("nan")
    print("="*50)
    print(f"TRIAGE VALIDATION (N={len(rows)})")
    print(f"  TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"  Sensitivity (recall) = {sens:.3f}   <- should be close to 1.0 (no eligible study dropped)")
    print(f"  Specificity          = {spec:.3f}")
    print(f"  PPV                  = {ppv:.3f}")
    if fn > 0:
        print(f"  WARNING: {fn} FALSE EXCLUSIONS -> the triage rules should be loosened (recall takes priority).")
    print("="*50)

def main():
    if not os.path.exists(SAMPLE):
        build_sample()
    else:
        score()

if __name__ == "__main__":
    main()
