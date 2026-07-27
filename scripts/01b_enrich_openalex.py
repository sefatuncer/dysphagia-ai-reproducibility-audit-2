#!/usr/bin/env python3
"""
01b_enrich_openalex.py — DOI-only kayıtlar için abstract kapsamını yükselt.

Europe PMC PMID kayıtlarını %97 kapladı; DOI-only (medRxiv/IEEE/ACM/OpenAlex) düşük.
OpenAlex abstract_inverted_index'ten abstract'ı yeniden kurar. Yalnız abstract'ı
BOŞ olan satırları doldurur (mevcut Europe PMC abstract'larına dokunmaz).

Girdi/çıktı: kaynaklar/arama-sonuclari/combined-corpus-enriched.csv (yerinde günceller)
Önbellek   : analiz/openalex-cache.jsonl
"""
import csv, json, os, sys, time, urllib.request, urllib.parse

ENR   = "kaynaklar/arama-sonuclari/combined-corpus-enriched.csv"
CACHE = "analiz/openalex-cache.jsonl"
BATCH = 40
DELAY = 0.3
MAILTO = "tuncersefa@gmail.com"

def reconstruct(inv):
    if not inv: return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs: pos[i] = word
    return " ".join(pos[i] for i in sorted(pos)).replace("\n", " ").strip()

def fetch(dois):
    filt = "doi:" + "|".join(dois)
    params = urllib.parse.urlencode({"filter": filt, "per-page": len(dois),
                                     "select": "doi,abstract_inverted_index,type,title",
                                     "mailto": MAILTO})
    url = "https://api.openalex.org/works?" + params
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MakaleC-repro-audit/1.0 (mailto:%s)" % MAILTO})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:
            sys.stdout.write(f"  ! retry {attempt+1}: {e}\n"); sys.stdout.flush()
            time.sleep(2*(attempt+1))
    return None

def load_cache():
    cache = {}
    if os.path.exists(CACHE):
        for line in open(CACHE, encoding="utf-8"):
            line = line.strip()
            if line:
                d = json.loads(line); cache[d["doi"]] = d
    return cache

def main():
    rows = list(csv.DictReader(open(ENR, encoding="utf-8")))
    cache = load_cache()
    cf = open(CACHE, "a", encoding="utf-8")
    todo = [r["doi"].strip().lower() for r in rows
            if r.get("doi", "").strip() and not r.get("abstract", "").strip()
            and r["doi"].strip().lower() not in cache]
    todo = sorted(set(todo))
    print(f"OpenAlex: {len(todo)} DOI (abstract bos) cekilecek")
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i+BATCH]
        data = fetch(batch)
        got = {}
        if data:
            for w in data.get("results", []):
                d = (w.get("doi") or "").replace("https://doi.org/", "").strip().lower()
                if d:
                    got[d] = {"doi": d, "abstract": reconstruct(w.get("abstract_inverted_index")),
                              "type": w.get("type", "")}
        for d in batch:
            rec = got.get(d, {"doi": d, "abstract": "", "type": ""})
            cf.write(json.dumps(rec, ensure_ascii=False) + "\n"); cf.flush()
        print(f"  {i+len(batch)}/{len(todo)} (abstract bulunan bu batch={sum(1 for d in batch if got.get(d,{}).get('abstract'))})")
        time.sleep(DELAY)
    cf.close()

    cache = load_cache()
    n_new = 0
    for r in rows:
        if not r.get("abstract", "").strip():
            d = r.get("doi", "").strip().lower()
            c = cache.get(d)
            if c and c.get("abstract"):
                r["abstract"] = c["abstract"]; r["has_abstract"] = "yes"
                if not r.get("pub_types", "").strip() and c.get("type"):
                    r["pub_types"] = "openalex:" + c["type"]
                n_new += 1
    with open(ENR, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    tot = sum(1 for r in rows if r["has_abstract"] == "yes")
    print(f"OpenAlex ekledi: +{n_new} abstract. TOPLAM abstract: {tot}/{len(rows)} ({100*tot//len(rows)}%). BITTI.")

if __name__ == "__main__":
    main()
