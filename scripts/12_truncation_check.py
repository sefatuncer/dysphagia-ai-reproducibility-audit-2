#!/usr/bin/env python3
"""
12_truncation_check.py — quantify the GitHub top-N truncation limitation.

The discovery script takes only the first page (15 repositories, ranked by stars)
per search term. Zero-star academic repositories can therefore be missed. A
reviewer asked how large that loss actually is, so this script re-runs every
GitHub search term with full pagination, applies the same blind, rule-based
scope test used for the screening-reliability check, and reports how many
in-scope candidates sit BEYOND rank 15.

Output: analiz/truncation-check.json + a printed summary.
Unauthenticated GitHub search is limited to ~10 requests/min and caps result
sets at 1000, both of which are recorded in the output.
"""
import json, sys, time, urllib.request, urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

OUT = out("truncation-check.json")
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
PER_PAGE = 100
ORIGINAL_CUTOFF = 15          # what 07_repo_discovery.py actually kept per term
MAX_PAGES = 4                 # 400 results per term is far beyond any plausible tail

GH_QUERIES = [
    "dysphagia deep learning", "dysphagia machine learning", "dysphagia segmentation",
    "swallowing deep learning", "swallowing segmentation", "swallowing classification",
    "VFSS deep learning", "videofluoroscopy swallowing", "FEES swallowing endoscopy",
    "swallowing sound classification", "cervical auscultation swallow",
    "swallowing EMG classification", "deglutition neural network",
    "bolus segmentation fluoroscopy", "hyoid bone tracking swallow",
    "penetration aspiration deep learning", "swallow detection accelerometer",
]

TOOL_LIBS = (
    "yolo", "opencv", "labelme", "labelimg", "opensmile", "silero", "soxr",
    "ggplot", "/bwa", "trimmomatic", "dcm2niix", "h2o-3", "/h2o", "econml",
    "boxmot", "medcat", "darknet", "deepwalk", "decagon", "knowddi",
    "graphembedding", "pygat", "/gat", "skipgnn", "/line", "/deepwalk",
)
SCOPE_KW = ("dysphag", "swallow", "deglutit", "aspiration", "penetrat", "vfss", "fees")


def in_scope(full_name, description):
    """Same blind rule as the screening-reliability check (name + description)."""
    name = (full_name or "").lower()
    if any(lib in name for lib in TOOL_LIBS):
        return False
    text = name + " " + (description or "").lower()
    return any(k in text for k in SCOPE_KW)


def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            print("  ! %s (attempt %d)" % (str(e)[:70], attempt + 1))
            time.sleep(20)
    return None


def main():
    known = set()
    ham = inp("repo-inventory-raw")
    if ham.exists():
        import csv
        known = {(r["repo"] or "").strip().lower()
                 for r in csv.DictReader(open(ham, encoding="utf-8"))}

    per_term, tail_hits = {}, {}
    for q in GH_QUERIES:
        seen, page = [], 1
        while page <= MAX_PAGES:
            url = ("https://api.github.com/search/repositories?q=%s&sort=stars"
                   "&order=desc&per_page=%d&page=%d"
                   % (urllib.parse.quote(q), PER_PAGE, page))
            d = get(url)
            if not d or "items" not in d:
                break
            total = d.get("total_count", 0)
            seen.extend(d["items"])
            if len(d["items"]) < PER_PAGE or len(seen) >= min(total, MAX_PAGES * PER_PAGE):
                break
            page += 1
            time.sleep(7)
        tail = seen[ORIGINAL_CUTOFF:]
        hits = [{"repo": it["full_name"], "stars": it.get("stargazers_count", 0),
                 "rank": ORIGINAL_CUTOFF + i + 1,
                 "already_known": it["full_name"].lower() in known,
                 "description": (it.get("description") or "")[:110]}
                for i, it in enumerate(tail)
                if in_scope(it["full_name"], it.get("description"))]
        per_term[q] = {"retrieved": len(seen), "total_count": total if seen else 0,
                       "tail_examined": len(tail), "in_scope_in_tail": len(hits)}
        tail_hits[q] = hits
        print("  [%-36s] cekilen=%-4d kuyruk=%-4d kapsam-ici-kuyrukta=%d"
              % (q[:36], len(seen), len(tail), len(hits)))
        time.sleep(7)

    all_hits = {h["repo"]: h for hs in tail_hits.values() for h in hs}
    novel = {k: v for k, v in all_hits.items() if not v["already_known"]}

    print("\n" + "=" * 70)
    print("TRUNCATION CHECK — 07_repo_discovery.py terim basina ilk %d'i aliyordu"
          % ORIGINAL_CUTOFF)
    print("=" * 70)
    print("  Terim sayisi                         : %d" % len(GH_QUERIES))
    print("  Kuyrukta (rank>%d) kapsam-ici benzersiz repo: %d"
          % (ORIGINAL_CUTOFF, len(all_hits)))
    print("  Bunlardan envanterde OLMAYAN          : %d" % len(novel))
    if novel:
        print("\n  Envanterde olmayan kuyruk adaylari (elle vet gerekir):")
        for r, v in sorted(novel.items(), key=lambda x: -x[1]["stars"])[:40]:
            print("    rank%-4d stars%-5d %-52s %s"
                  % (v["rank"], v["stars"], r, v["description"][:60]))
    else:
        print("\n  Kuyrukta envantere eklenecek yeni kapsam-ici repo YOK.")
        print("  -> top-%d kirpmasi bu terim kumesi icin kayip uretmiyor." % ORIGINAL_CUTOFF)

    OUT.write_text(json.dumps(
        {"cutoff": ORIGINAL_CUTOFF, "per_page": PER_PAGE, "max_pages": MAX_PAGES,
         "note": "unauthenticated GitHub search: ~10 req/min, 1000-result cap",
         "per_term": per_term, "tail_in_scope_unique": len(all_hits),
         "tail_novel": novel}, indent=2), encoding="utf-8")
    print("\n[written] %s" % OUT)


if __name__ == "__main__":
    main()
