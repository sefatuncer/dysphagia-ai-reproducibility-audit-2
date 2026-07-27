#!/usr/bin/env python3
"""
04_prisma_counts.py — PRISMA-ScR akış sayılarını TEKRARLANABİLİR üret.

Identification (kaynak-bazlı) + dedup + triyaj bucket dağılımı (makine ön-sıralaması,
ELEME DEĞİL) → taslak/prisma-akis-veriler.json + stdout. Screening/eligibility/included
sayıları İNSAN taramasından sonra doldurulur (bilerek boş).
"""
import csv, json, os
try:
    import sys; sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

AS = "kaynaklar/arama-sonuclari/"

def nrows(path, header=True):
    if not os.path.exists(path): return None
    with open(path, encoding="utf-8") as f:
        n = sum(1 for _ in f)
    return n - (1 if header else 0)

def main():
    sources = {
        "PubMed/MEDLINE": nrows(AS+"pubmed-pmids.txt", header=False),
        "Semantic Scholar": nrows(AS+"semanticscholar-records.csv"),
        "Europe PMC": nrows(AS+"europepmc-records.csv"),
        "OpenAlex": nrows(AS+"openalex-records.csv"),
    }
    raw_total = sum(v for v in sources.values() if v)
    combined = nrows(AS+"combined-corpus.csv")
    dupes = raw_total - combined if combined else None

    # triyaj bucket dağılımı
    buckets = {}
    wf = "analiz/tarama-calisma-sayfasi.csv"
    if os.path.exists(wf):
        for r in csv.DictReader(open(wf, encoding="utf-8")):
            b = r.get("t_bucket", "?"); buckets[b] = buckets.get(b, 0) + 1

    data = {
        "identification": {
            "sources_open_api": sources,
            "raw_total_open_api": raw_total,
            "institutional_scopus_wos_ieee": "TBD (insan — PRESS sonrası)",
            "backward_citation": "TBD (İş #3)",
        },
        "deduplication": {"raw": raw_total, "after_dedup": combined, "duplicates_removed": dupes},
        "triage_presort_NOT_exclusion": buckets,
        "screening": {"title_abstract_screened": combined,
                      "note": "Triyaj = organizasyon aracı; ELEME insan çift-tarama + κ ile. Sayılar tarama sonrası."},
        "eligibility": {"full_text_assessed": "TBD", "excluded_with_reasons": "TBD"},
        "included": {"total": "TBD (~60 beklenen)", "layer_b_code_available": "TBD (~5-15)"},
    }
    with open("taslak/prisma-akis-veriler.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("="*58)
    print("PRISMA-ScR — TANIMLAMA & DEDUP (tekrarlanabilir)")
    print("="*58)
    for k, v in sources.items(): print(f"  {k:22s}: {v}")
    print(f"  {'HAM TOPLAM (açık-API)':22s}: {raw_total}")
    print(f"  {'dedup sonrası':22s}: {combined}   (çıkarılan {dupes})")
    print(f"  {'kurumsal DB':22s}: TBD (insan)")
    print("-"*58)
    print("Triyaj ön-sıralama (ELEME DEĞİL):")
    for b, n in sorted(buckets.items(), key=lambda x: -x[1]):
        print(f"  {b:30s}: {n}")
    print("="*58)
    print("→ taslak/prisma-akis-veriler.json yazıldı. Screening/included = insan sonrası.")

if __name__ == "__main__":
    main()
