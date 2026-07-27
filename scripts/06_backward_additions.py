#!/usr/bin/env python3
"""
06_backward_additions.py — geriye-atıf eksiklerini metadata ile korpusa hazırla.

Kwok + CODAS geriye-atıf kontrolünde bulunan KAPSAM-İÇİ eksik çalışmaların DOI'lerini
OpenAlex (Crossref fallback) ile zenginleştir → backward-citation-additions.csv.
Kurumsal arama sonrası birleşik korpusa source=backward_citation olarak eklenir.
"""
import csv, json, sys, time, urllib.request, urllib.parse
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

DOIS = [
    ("10.1016/j.artmed.2011.03.002", "Kwok-45"),
    ("10.1109/taslp.2022.3203235", "Kwok-40"),
    ("10.1109/icassp48485.2024.10447365", "Kwok-41"),
    ("10.1016/j.bspc.2022.104533", "Kwok-50"),
    ("10.1016/j.dsp.2022.103815", "Kwok-51"),
    ("10.1007/s00455-018-09974-5", "Kwok-56"),
    ("10.1109/iscas51556.2021.9401353", "Kwok-57"),
    ("10.1038/s41598-023-34999-8", "CODAS"),  # düzeltildi: -x → -8 (Crossref/OpenAlex 404; başlıkla doğrulandı, Sci Rep 2023;13:7835)
    ("10.1109/access.2020.3019532", "CODAS"),
]
OUT = "kaynaklar/arama-sonuclari/backward-citation-additions.csv"
MAILTO = "tuncersefa@gmail.com"

def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"MakaleC/1.0 (mailto:{MAILTO})"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return None

def openalex(doi):
    d = get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}?mailto={MAILTO}")
    if not d: return None
    src = ((d.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    return {"title": d.get("title", ""), "year": d.get("publication_year", ""),
            "venue": src, "type": d.get("type", "")}

def crossref(doi):
    d = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}")
    if not d: return None
    m = d.get("message", {})
    return {"title": (m.get("title") or [""])[0], "year": (m.get("issued", {}).get("date-parts", [[None]])[0][0] or ""),
            "venue": (m.get("container-title") or [""])[0], "type": m.get("type", "")}

def main():
    rows = []
    for doi, review in DOIS:
        # Crossref = DOI tescil otoritesi → bibliyografik metadata için kanonik (title/year/venue).
        # OpenAlex fallback; OpenAlex'in s41598-023-34999-8 için kaydı bozuktu (1968 kataliz makalesine bağlı).
        meta = crossref(doi) or openalex(doi) or {"title": "", "year": "", "venue": "", "type": ""}
        rows.append({"doi": doi, "from_review": review, "source": "backward_citation",
                     "year": meta["year"], "venue": meta["venue"], "title": meta["title"],
                     "include_screen1": "", "exclude_reason": ""})
        print(f"  {doi}  [{meta['year']}] {meta['venue'][:32]:32s} {meta['title'][:55]}")
        time.sleep(0.3)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["doi", "from_review", "source", "year", "venue", "title",
                                          "include_screen1", "exclude_reason"])
        w.writeheader(); w.writerows(rows)
    print(f"\n{len(rows)} kayıt → {OUT}")

if __name__ == "__main__":
    main()
