#!/usr/bin/env python3
"""
04_prisma_counts.py — produce the flow-diagram counts REPRODUCIBLY.

Identification (per source) plus deduplication plus the triage bucket distribution (a
machine pre-sort, NOT an exclusion step) → taslak/prisma-akis-veriler.json and stdout.
The screening, eligibility and included counts are filled in after HUMAN screening and
are deliberately left empty here.
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

    # triage bucket distribution
    buckets = {}
    wf = "analiz/tarama-calisma-sayfasi.csv"
    if os.path.exists(wf):
        for r in csv.DictReader(open(wf, encoding="utf-8")):
            b = r.get("t_bucket", "?"); buckets[b] = buckets.get(b, 0) + 1

    data = {
        "identification": {
            "sources_open_api": sources,
            "raw_total_open_api": raw_total,
            "institutional_scopus_wos_ieee": "TBD (human, after PRESS)",
            "backward_citation": "TBD",
        },
        "deduplication": {"raw": raw_total, "after_dedup": combined, "duplicates_removed": dupes},
        "triage_presort_NOT_exclusion": buckets,
        "screening": {"title_abstract_screened": combined,
                      "note": "Triage is an organizational device; exclusion is by human dual screening with kappa. Counts follow screening."},
        "eligibility": {"full_text_assessed": "TBD", "excluded_with_reasons": "TBD"},
        "included": {"total": "TBD (about 60 expected)", "layer_b_code_available": "TBD (about 5-15)"},
    }
    with open("taslak/prisma-akis-veriler.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("="*58)
    print("IDENTIFICATION AND DEDUPLICATION (reproducible)")
    print("="*58)
    for k, v in sources.items(): print(f"  {k:22s}: {v}")
    print(f"  {'RAW TOTAL (open API)':22s}: {raw_total}")
    print(f"  {'after deduplication':22s}: {combined}   ({dupes} removed)")
    print(f"  {'institutional DBs':22s}: TBD (human)")
    print("-"*58)
    print("Triage pre-sort (NOT exclusion):")
    for b, n in sorted(buckets.items(), key=lambda x: -x[1]):
        print(f"  {b:30s}: {n}")
    print("="*58)
    print("-> taslak/prisma-akis-veriler.json written. Screening and included counts follow human screening.")

if __name__ == "__main__":
    main()
