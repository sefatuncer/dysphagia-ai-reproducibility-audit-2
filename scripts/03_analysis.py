#!/usr/bin/env python3
"""
03_analysis.py — SAP'in tekrarlanabilir uygulaması (Makale C).

Bağımsız istatistik yardımcıları (scipy gerektirmez): Wilson GA, Newcombe iki-oran
farkı GA, Cohen κ. seffaflik-rubrigi.csv'yi okur; henüz yeterli veri yoksa (yalnız
pilot repo #1) SENTETİK demo satırlarıyla çalıştığını KANITLAR — gerçek veri gelince
aynı script koşar. Sabit seed → tekrarlanabilir (makalenin tezi).

Kullanım: PYTHONIOENCODING=utf-8 python analiz/scripts/03_analysis.py
"""
import csv, math, os, random
random.seed(42)
Z = 1.959963985  # %95

RUBRIC = "analiz/seffaflik-rubrigi.csv"
BINARY_ITEMS = {  # kolon -> "paylaşım/olumlu" sayılan değerler
    "code_stmt": {"yes", "explicit-url"},
    "repo_accessible": {"yes"},
    "license": None,   # özel: NONE dışı = var
    "readme_run_instructions": {"yes", "partial"},
    "dependency_file": None,  # boş/none dışı = var
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
    """iki oran farkı (p1-p2) için Newcombe %95 GA."""
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    diff = p1 - p2
    lo = diff - math.sqrt((p1-l1)**2 + (u2-p2)**2)
    hi = diff + math.sqrt((u1-p1)**2 + (p2-l2)**2)
    return diff, lo, hi

def cohen_kappa(pairs):
    """pairs: [(rater1, rater2), ...] kategorik."""
    n = len(pairs)
    if n == 0: return float("nan")
    cats = sorted(set(a for a, _ in pairs) | set(b for _, b in pairs))
    po = sum(1 for a, b in pairs if a == b) / n
    m1 = {c: sum(1 for a, _ in pairs if a == c)/n for c in cats}
    m2 = {c: sum(1 for _, b in pairs if b == c)/n for c in cats}
    pe = sum(m1[c]*m2[c] for c in cats)
    return (po - pe) / (1 - pe) if pe != 1 else 1.0

def cohen_kappa_ci(pairs, B=2000):
    """Cohen κ + yüzdelik bootstrap %95 GA (SAP §4: κ %95 GA + Landis-Koch).
    Sabit seed (random.seed(42)) → tekrarlanabilir. Küçük kalibrasyon setinde
    κ'nin belirsizliğini gösterir (dar sette nokta-κ yanıltıcı olabilir)."""
    k = cohen_kappa(pairs)
    n = len(pairs)
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    boots = []
    for _ in range(B):
        sample = [pairs[random.randrange(n)] for _ in range(n)]
        kb = cohen_kappa(sample)
        if kb == kb:  # NaN değilse
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
    # yetersiz veri → sentetik demo (gerçek veri gelince otomatik devre-dışı)
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
    print(f"MAKALE C — ŞEFFAFLIK ANALİZİ  (N={n})" + ("  [SENTETİK DEMO — gerçek veri bekleniyor]" if synthetic else "  [GERÇEK VERİ]"))
    print("="*66)
    print(f"{'Öğe':26s}{'k/N':>10s}{'oran':>8s}{'  %95 Wilson GA':>18s}")
    print("-"*66)
    results = {}
    for col in BINARY_ITEMS:
        k = sum(1 for r in rows if positive(col, r.get(col)))
        p, lo, hi = wilson(k, n)
        results[col] = (k, n)
        print(f"{col:26s}{f'{k}/{n}':>10s}{p:>8.2f}{f'[{lo:.2f}, {hi:.2f}]':>18s}")
    print("-"*66)

    # radyoloji kıyası (kod paylaşımı) — TEK doğrulanmış çapa: Venkatesh 2022 = 73/218 (%34).
    # NOT: "DL ~%11.5 (2025)" figürü kaldırıldı — kaynaklanamadı + Lee/Eur Radiol 2025'e yanlış
    # atıflıydı (o çalışma %39.9 rapor ediyor). Bkz. taslak/referanslar-iskelet.md ⚠️.
    k_code, _ = results["code_stmt"]
    kr, nr = 73, 218  # Venkatesh 2022, Radiol Artif Intell — erişilebilir kod paylaşan çalışma oranı
    pr, rlo, rhi = wilson(kr, nr)
    print(f"Referans (Venkatesh 2022, radyoloji): {kr}/{nr} = {pr:.2f}  [{rlo:.2f}, {rhi:.2f}]")
    d, lo, hi = newcombe_diff(k_code, n, kr, nr)
    print(f"Kod-paylaşımı farkı vs radyoloji %34: Δ={d:+.2f}  Newcombe95=[{lo:+.2f}, {hi:+.2f}]  (bağlamsal, nedensel değil; tanım-eşlemesi: 'erişilebilir kod')")
    print("-"*66)

    # κ demo (kalibrasyon) — %95 bootstrap GA ile (SAP §4)
    demo_pairs = [(random.choice(["incl","excl"]), random.choice(["incl","excl","excl"])) for _ in range(50)]
    k, klo, khi = cohen_kappa_ci(demo_pairs)
    print(f"κ demo (kalibrasyon örneği): κ={k:.2f}  %95GA=[{klo:.2f}, {khi:.2f}]  ({landis_koch(k)})  — gerçek tarama verisiyle değişecek")
    print("="*66)
    print("NOT: sentetik satırlar YALNIZ pipeline'ı doğrular; gerçek rubrik ≥10 satır olunca")
    print("     otomatik gerçek-veriye geçer. Wilson/Newcombe/κ SAP §2-5 uygular.")

if __name__ == "__main__":
    try:
        import sys; sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()
