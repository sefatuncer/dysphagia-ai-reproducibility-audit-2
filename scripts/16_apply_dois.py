#!/usr/bin/env python3
"""
16_apply_dois.py — write verified DOIs into refs.bib, retry the rejected ones.

Pass 1 (15_resolve_dois.py) accepted 23 DOIs and rejected 13, because Crossref's
best title match was a different paper. Those rejections are the point of the
check: a bibliographic search for the QUADAS-2 tool returns a QUADAS-3 pilot, a
search for the PRISMA 2020 statement returns a later PRISMA commentary, and a
search for Haibe-Kains et al. returns the reply written against it. Accepting any
of those would have produced a citation that resolves and is wrong.

This script writes the 23 verified DOIs, then retries the 13 with the author name
added to the query, applying the same acceptance bar. Whatever still fails is left
without a DOI and listed for the authors, which is the honest outcome.

Also drops bibliography entries left over from the pre-pivot systematic-review
design that the manuscript no longer cites.
"""
import json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "taslak" / "latex" / "refs.bib"
TEX = ROOT / "taslak" / "latex" / "makale-IJMI.tex"
RES = ROOT / "analiz" / "doi-resolution.json"
UA = {"User-Agent": "MakaleC-refaudit/1.0 (mailto:tuncersefa@gmail.com)"}
STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "is", "are"}

# Pre-pivot leftovers: the manuscript is not a systematic review and cites none of
# these. Kept out of the archive so the abandoned design is not implied by the
# bibliography.
DROP = {"prisma2020", "prismascr2018", "press2016", "rayyan2016", "landiskoch1977",
        "newcombe1998"}


def norm(s):
    s = re.sub(r"\{|\}|\\[a-zA-Z]+|\\", "", s or "").lower()
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", s).split() if w not in STOP]


def sim(a, b):
    A, B = set(norm(a)), set(norm(b))
    return len(A & B) / max(1, max(len(A), len(B)))


def retry(title, author):
    q = urllib.parse.urlencode({"query.bibliographic": title[:180],
                                "query.author": author, "rows": 5,
                                "select": "DOI,title,author,container-title"})
    try:
        req = urllib.request.Request("https://api.crossref.org/works?" + q, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["message"]["items"]
    except Exception:
        return []


def main():
    res = json.loads(RES.read_text(encoding="utf-8"))
    bib = BIB.read_text(encoding="utf-8")
    cited = set()
    for grp in re.findall(r"\\citep?\{([^}]*)\}", TEX.read_text(encoding="utf-8")):
        cited |= {k.strip() for k in grp.split(",")}

    applied = {r["key"]: r["doi"] for r in res["resolved"]}
    print("=" * 76)
    print("DOI YAZIMI + IKINCI GECIS")
    print("=" * 76)

    # ---- pass 2: retry the rejected ones with the author in the query ----
    still = []
    for r in res["low_confidence"]:
        if r["key"] in DROP:
            continue
        items = retry(r["crossref_title"] if False else "", "") if False else \
            retry(re.sub(r"\{|\}", "", r.get("bib_first_author", "")) and
                  r.get("crossref_title", ""), r.get("bib_first_author", ""))
        time.sleep(0.5)
        # search using the ORIGINAL bib title, not the wrong crossref one
        best, best_s = None, 0.0
        bib_title = re.search(r"@\w+\{" + re.escape(r["key"]) + r",.*?title\s*=\s*[{\"](.*?)[}\"]\s*,\s*\n",
                              bib, re.S)
        bt = " ".join(bib_title.group(1).split()) if bib_title else ""
        items = retry(bt, r.get("bib_first_author", ""))
        time.sleep(0.5)
        for it in items:
            ct = (it.get("title") or [""])[0]
            s = sim(bt, ct)
            if s > best_s:
                best, best_s = it, s
        if best:
            auth = best.get("author") or []
            cf = auth[0].get("family", "") if auth else ""
            bf = r.get("bib_first_author", "")
            ok = bool(cf) and bool(bf) and (cf.lower() in bf.lower() or bf.lower() in cf.lower())
            if best_s >= 0.72 and ok:
                applied[r["key"]] = best.get("DOI")
                print("  [2.GECIS OK] %-17s -> %s" % (r["key"], best.get("DOI")))
                continue
        still.append(r["key"])
        print("  [ELLE      ] %-17s  (Crossref dogru kaydi dondurmuyor)" % r["key"])

    # ---- write DOIs ----
    n = 0
    for key, doi in applied.items():
        if not doi:
            continue
        m = re.search(r"(@\w+\{" + re.escape(key) + r",)(.*?)(\n\})", bib, re.S)
        if not m or "doi" in m.group(2).lower():
            continue
        bib = bib[:m.end(2)] + ",\n  doi     = {%s}" % doi + bib[m.end(2):]
        n += 1

    # ---- drop pre-pivot leftovers ----
    dropped = []
    for key in DROP:
        if key in cited:
            print("  [KORUNDU  ] %-17s metinde atif var, silinmedi" % key)
            continue
        new = re.sub(r"\n@\w+\{" + re.escape(key) + r",.*?\n\}\n", "\n", bib, flags=re.S)
        if new != bib:
            bib, _ = new, dropped.append(key)

    BIB.write_text(bib, encoding="utf-8")
    print("-" * 76)
    print("  DOI yazilan girdi        : %d" % n)
    print("  silinen pivot-oncesi kayit: %d  %s" % (len(dropped), sorted(dropped)))
    print("  DOI'si hala YOK (elle)   : %d  %s" % (len(still), sorted(still)))
    print("=" * 76)


if __name__ == "__main__":
    main()
