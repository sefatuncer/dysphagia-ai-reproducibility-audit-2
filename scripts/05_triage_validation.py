#!/usr/bin/env python3
"""
05_triage_validation.py — triyaj bayraklarını insan-gold'a karşı doğrula.

İKİ MOD:
1) Örnek YOKsa → tarama-calisma-sayfasi.csv'den katmanlı rastgele ~200 kayıt çek
   (hariç-bucket'lara TABAN — asıl risk yanlış-hariç) → analiz/triyaj-validasyon-ornek.csv
   (boş `human_gold_include` kolonu; iki insan bağımsız doldurur).
2) Örnek VARsa ve human_gold dolu → triyajın implied dahil/hariç kararının
   sensitivite/spesifisite/PPV'si + karışıklık matrisi.

Sabit seed → tekrarlanabilir.
"""
import csv, os, random
random.seed(2026)
try:
    import sys; sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

WF = "analiz/tarama-calisma-sayfasi.csv"
SAMPLE = "analiz/triyaj-validasyon-ornek.csv"
TARGET = 200
FLOOR_EXCL = 25   # her hariç-bucket'tan en az (yanlış-hariç avı)
FLOOR_OTHER = 15

INCLUDE_BUCKETS = {"likely_include", "needs_review", "needs_review_no_abstract"}

def implied_triage_include(bucket):
    return bucket in INCLUDE_BUCKETS  # gri = insana → dahil-tarafı sayılır (recall lehine)

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
    print(f"Örnek üretildi: {len(picked)} kayıt → {SAMPLE}")
    from collections import Counter
    print("  bucket dağılımı:", dict(Counter(x["t_bucket"] for x in picked)))
    print("  İKİ İNSAN `human_gold_include`'ı bağımsız doldurur (yes/no) → tekrar koş.")

def score():
    rows = [r for r in csv.DictReader(open(SAMPLE, encoding="utf-8"))
            if r.get("human_gold_include", "").strip().lower() in ("yes", "no")]
    if len(rows) < 20:
        print(f"human_gold dolu {len(rows)} kayıt (<20) → henüz skorlanmıyor.")
        return
    tp = fp = tn = fn = 0
    for r in rows:
        gold = r["human_gold_include"].strip().lower() == "yes"
        pred = implied_triage_include(r["t_bucket"])
        if gold and pred: tp += 1
        elif not gold and pred: fp += 1
        elif not gold and not pred: tn += 1
        else: fn += 1  # gold-include ama triyaj-hariç = YANLIŞ-HARİÇ (kritik)
    sens = tp/(tp+fn) if tp+fn else float("nan")
    spec = tn/(tn+fp) if tn+fp else float("nan")
    ppv = tp/(tp+fp) if tp+fp else float("nan")
    print("="*50)
    print(f"TRİYAJ VALİDASYONU (N={len(rows)})")
    print(f"  TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"  Sensitivite (recall) = {sens:.3f}   ← 1.0'a yakın olmalı (uygun çalışma elenmedi)")
    print(f"  Spesifisite          = {spec:.3f}")
    print(f"  PPV                  = {ppv:.3f}")
    if fn > 0:
        print(f"  ⚠️ {fn} YANLIŞ-HARİÇ → triyaj kuralları gevşetilmeli (recall öncelik).")
    print("="*50)

def main():
    if not os.path.exists(SAMPLE):
        build_sample()
    else:
        score()

if __name__ == "__main__":
    main()
