#!/usr/bin/env python3
"""
01_enrich_epmc.py - pre-screening enrichment (reproducible pipeline)

Purpose: take combined-corpus.csv (2171 records, titles only) and add, for every record,
the ABSTRACT, the publication type (pubType) and a review flag from Europe PMC. Dual
independent human screening is performed ON TOP of this; the script only enriches the
data and DECIDES NOTHING.

Input : kaynaklar/arama-sonuclari/combined-corpus.csv
Output: kaynaklar/arama-sonuclari/combined-corpus-enriched.csv (adds abstract, pub_types, epmc_is_review, epmc_found, has_abstract)
Cache (resume) : analiz/epmc-cache.jsonl (resumes where it left off if interrupted)
Log   : stdout (line-by-line progress)

Note: public bibliographic APIs only; no patient data. The access date is written to the log.
"""
import csv, json, os, sys, time, urllib.request, urllib.parse

BASE   = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CORPUS = "kaynaklar/arama-sonuclari/combined-corpus.csv"
OUT    = "kaynaklar/arama-sonuclari/combined-corpus-enriched.csv"
CACHE  = "analiz/epmc-cache.jsonl"
PMID_BATCH = 40
DOI_BATCH  = 20
DELAY = 0.34  # seconds; a polite request rate

def fetch(query, page_size):
    params = urllib.parse.urlencode({"query": query, "resultType": "core",
                                     "format": "json", "pageSize": page_size})
    url = BASE + "?" + params
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MakaleC-repro-audit/1.0 (research)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:
            sys.stdout.write(f"  ! retry {attempt+1}: {e}\n"); sys.stdout.flush()
            time.sleep(2 * (attempt + 1))
    return None

def extract(res):
    abstract = (res.get("abstractText") or "").replace("\n", " ").strip()
    pts = []
    ptl = res.get("pubTypeList", {})
    if isinstance(ptl, dict):
        raw = ptl.get("pubType", [])
        if isinstance(raw, str): raw = [raw]
        pts = [str(p) for p in raw]
    is_review = any("review" in p.lower() for p in pts)
    return abstract, "; ".join(pts), is_review

def load_cache():
    cache = {}
    if os.path.exists(CACHE):
        for line in open(CACHE, encoding="utf-8"):
            line = line.strip()
            if line:
                d = json.loads(line); cache[d["key"]] = d
    return cache

def append_cache(fh, key, abstract, pub_types, is_review, found):
    rec = {"key": key, "abstract": abstract, "pub_types": pub_types,
           "epmc_is_review": found and is_review, "epmc_found": found}
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
    return rec

def main():
    rows = list(csv.DictReader(open(CORPUS, encoding="utf-8")))
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] corpus={len(rows)} records")
    cache = load_cache()
    print(f"  cache={len(cache)} records (resume)")
    cf = open(CACHE, "a", encoding="utf-8")

    # --- PMID pass ---
    pmid_rows = [r for r in rows if r.get("pmid", "").strip()]
    todo = [r["pmid"].strip() for r in pmid_rows if ("pmid:" + r["pmid"].strip()) not in cache]
    print(f"  PMID: {len(pmid_rows)} records, {len(todo)} to fetch")
    for i in range(0, len(todo), PMID_BATCH):
        batch = todo[i:i+PMID_BATCH]
        q = "(" + " OR ".join(f"EXT_ID:{p}" for p in batch) + ") AND SRC:MED"
        data = fetch(q, len(batch))
        got = {}
        if data:
            for res in data.get("resultList", {}).get("result", []):
                pm = str(res.get("pmid", "")).strip()
                if pm: got[pm] = extract(res)
        for p in batch:
            if p in got:
                a, pt, rv = got[p]; append_cache(cf, "pmid:"+p, a, pt, rv, True)
            else:
                append_cache(cf, "pmid:"+p, "", "", False, False)
        print(f"    pmid {i+len(batch)}/{len(todo)}  (found in this batch={len(got)}/{len(batch)})"); sys.stdout.flush()
        time.sleep(DELAY)

    cache = load_cache()  # refresh

    # --- DOI pass (records without a PMID) ---
    doi_rows = [r for r in rows if not r.get("pmid", "").strip() and r.get("doi", "").strip()]
    todo_doi = [r["doi"].strip().lower() for r in doi_rows if ("doi:" + r["doi"].strip().lower()) not in cache]
    print(f"  DOI-only: {len(doi_rows)} records, {len(todo_doi)} to fetch")
    for i in range(0, len(todo_doi), DOI_BATCH):
        batch = todo_doi[i:i+DOI_BATCH]
        q = "(" + " OR ".join(f'DOI:"{d}"' for d in batch) + ")"
        data = fetch(q, len(batch))
        got = {}
        if data:
            for res in data.get("resultList", {}).get("result", []):
                dd = str(res.get("doi", "")).strip().lower()
                if dd: got[dd] = extract(res)
        for d in batch:
            if d in got:
                a, pt, rv = got[d]; append_cache(cf, "doi:"+d, a, pt, rv, True)
            else:
                append_cache(cf, "doi:"+d, "", "", False, False)
        print(f"    doi {i+len(batch)}/{len(todo_doi)}  (found={len(got)}/{len(batch)})"); sys.stdout.flush()
        time.sleep(DELAY)

    cf.close()
    cache = load_cache()

    # --- write the enriched CSV ---
    add_cols = ["abstract", "pub_types", "epmc_is_review", "epmc_found", "has_abstract"]
    fieldnames = list(rows[0].keys()) + add_cols
    n_abs = 0
    with open(OUT, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=fieldnames); w.writeheader()
        for r in rows:
            key = None
            if r.get("pmid", "").strip(): key = "pmid:" + r["pmid"].strip()
            elif r.get("doi", "").strip(): key = "doi:" + r["doi"].strip().lower()
            c = cache.get(key, {}) if key else {}
            abstract = c.get("abstract", "")
            r2 = dict(r)
            r2["abstract"] = abstract
            r2["pub_types"] = c.get("pub_types", "")
            r2["epmc_is_review"] = "yes" if c.get("epmc_is_review") else ""
            r2["epmc_found"] = "yes" if c.get("epmc_found") else ""
            r2["has_abstract"] = "yes" if abstract else ""
            if abstract: n_abs += 1
            w.writerow(r2)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] WRITTEN {OUT}")
    print(f"  with abstract: {n_abs}/{len(rows)} ({100*n_abs//len(rows)}%)")
    print("  DONE.")

if __name__ == "__main__":
    main()
