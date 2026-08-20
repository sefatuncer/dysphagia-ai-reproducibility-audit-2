#!/usr/bin/env python3
"""
04_prisma_counts.py — identification and deduplication counts for the PRE-PIVOT design.

⚠️ NOT THE SOURCE OF ANY NUMBER IN THE PAPER. This script belongs to the study's
earlier systematic-review-style design, which assumed institutional database exports and
dual human screening; see `search/institutional-search-strings.md`, which carries the
same warning. It still writes the "TBD (about 60 expected)" scaffolding of that design,
which the pivoted study contradicts. The flow table published in the article is built
from the repository pipeline (scripts 07, 09 and 10) and not from here, and this
script's output file is deliberately not archived.

It is kept because removing it would leave the planning document pointing at a script
nobody can inspect, and because a reader is entitled to see what the abandoned design
would have computed.

Missing inputs are reported rather than skipped: a count assembled from whichever files
happened to be present is the silent-degradation failure this study audits in others.
"""
import csv, json, os
from paths import out
try:
    import sys; sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

AS = "kaynaklar/arama-sonuclari/"
# The old path wrote into taslak/, which does not exist in the archive, so running this
# from a published copy crashed on the write rather than reporting its missing inputs.
OUT = out("prisma-flow-prepivot.json")
missing = []

def nrows(path, header=True):
    if not os.path.exists(path):
        missing.append(path)
        return None
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

    # Triage bucket distribution. The worksheet was renamed when the archive was
    # translated; this read still carried the old Turkish filename, so the block below
    # was skipped silently and the distribution came out empty without saying so.
    buckets = {}
    wf = "analiz/screening-worksheet.csv"
    if os.path.exists(wf):
        for r in csv.DictReader(open(wf, encoding="utf-8")):
            b = r.get("t_bucket", "?"); buckets[b] = buckets.get(b, 0) + 1
    else:
        missing.append(wf)

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
    with open(OUT, "w", encoding="utf-8") as f:
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
    if missing:
        print("INPUTS NOT FOUND (%d) — the totals above are assembled from what was" % len(missing))
        print("present and are NOT the counts reported in the article:")
        for p in missing:
            print("  - %s" % p)
        print("These inputs belong to the pre-pivot design or carry third-party abstracts")
        print("and are not part of the published archive. See the module docstring.")
        print("="*58)
    print("-> %s written. Screening and included counts follow human screening." % OUT.name)

if __name__ == "__main__":
    main()
