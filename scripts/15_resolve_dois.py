#!/usr/bin/env python3
"""
15_resolve_dois.py — resolve missing DOIs by Crossref title search, and verify.

The reference audit found that most bibliography entries carried no DOI, which
means none of them could be checked mechanically. This script searches Crossref by
title, then accepts a candidate only if the returned title and first author both
match the entry. Anything below that bar is left alone and reported, because an
unverified DOI is worse than no DOI: a wrong one resolves to a real but unrelated
paper and looks correct.

Nothing is written back automatically. The script prints a patch and writes a JSON
report; applying it is a separate, deliberate step.

Output: analiz/doi-resolution.json
"""
import json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "taslak" / "latex" / "refs.bib"
OUT = ROOT / "analiz" / "doi-resolution.json"
UA = {"User-Agent": "MakaleC-refaudit/1.0 (mailto:tuncersefa@gmail.com)"}

STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "is", "are"}


def parse_bib(text):
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", m.group(3) + "\n", re.S):
            f[fm.group(1).lower()] = " ".join(fm.group(2).split())
        out.append({"key": m.group(2).strip(), **f})
    return out


def norm(s):
    s = re.sub(r"\{|\}|\\[a-zA-Z]+|\\", "", s or "").lower()
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", s).split() if w not in STOP]


def sim(a, b):
    A, B = set(norm(a)), set(norm(b))
    if not A or not B:
        return 0.0
    return len(A & B) / max(len(A), len(B))


def search(title, author):
    q = urllib.parse.urlencode({"query.bibliographic": title[:200], "rows": 5,
                                "select": "DOI,title,author,container-title,issued"})
    try:
        req = urllib.request.Request("https://api.crossref.org/works?" + q, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["message"]["items"]
    except Exception as e:
        print("   ! arama hatasi: %s" % str(e)[:50])
        return []


def main():
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    todo = [e for e in entries if not (e.get("doi") or "").strip()]
    print("=" * 76)
    print("DOI COZUMLEME — Crossref baslik aramasi + dogrulama")
    print("=" * 76)
    print("  DOI'si olmayan girdi: %d" % len(todo))
    print("  Kabul esigi: baslik ortusmesi >= 0.72 VE ilk yazar soyadi eslesmesi")
    print("-" * 76)

    res = {"resolved": [], "low_confidence": [], "not_found": []}
    for e in todo:
        title = e.get("title", "")
        bib_first = re.split(r"\s+and\s+", e.get("author", ""))[0].split(",")[0].strip()
        bib_first = re.sub(r"\{|\}|\\[a-zA-Z]+", "", bib_first).strip()
        items = search(title, bib_first)
        time.sleep(0.5)
        best, best_s = None, 0.0
        for it in items:
            ct = (it.get("title") or [""])[0]
            s = sim(title, ct)
            if s > best_s:
                best, best_s = it, s
        if not best:
            res["not_found"].append(e["key"])
            print("  [YOK    ] %-17s %s" % (e["key"], title[:44]))
            continue
        auth = best.get("author") or []
        cf = auth[0].get("family", "") if auth else ""
        author_ok = bool(cf) and bool(bib_first) and (
            cf.lower() in bib_first.lower() or bib_first.lower() in cf.lower())
        rec = {"key": e["key"], "doi": best.get("DOI"), "overlap": round(best_s, 2),
               "crossref_title": (best.get("title") or [""])[0],
               "crossref_first_author": cf, "bib_first_author": bib_first,
               "journal": (best.get("container-title") or [""])[0]}
        if best_s >= 0.72 and author_ok:
            res["resolved"].append(rec)
            print("  [COZULDU] %-17s %-42s -> %s" % (e["key"], title[:42], best.get("DOI")))
        else:
            res["low_confidence"].append(rec)
            print("  [DUSUK  ] %-17s ortusme %.2f  yazar-eslesme %s" %
                  (e["key"], best_s, "EVET" if author_ok else "HAYIR"))
            print("            bib      : %s / %s" % (bib_first, title[:56]))
            print("            crossref : %s / %s" % (cf, rec["crossref_title"][:56]))

    print("-" * 76)
    print("  cozuldu (yuksek guven) : %d" % len(res["resolved"]))
    print("  dusuk guven (ELLE)     : %d" % len(res["low_confidence"]))
    print("  bulunamadi (ELLE)      : %d" % len(res["not_found"]))
    print("=" * 76)
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print("[written] %s" % OUT)


if __name__ == "__main__":
    main()
