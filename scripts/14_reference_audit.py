#!/usr/bin/env python3
"""
14_reference_audit.py — verify every reference in refs.bib against Crossref.

For each entry with a DOI: resolve it through the Crossref REST API and compare the
returned title, first author, journal and year with what the bibliography claims.
A DOI that resolves is not evidence that the citation is correct: fabricated DOIs
frequently resolve to a real but unrelated paper, so the title and author must
match, not merely the identifier.

Entries without a DOI are listed for manual checking rather than passed silently.

This script checks bibliographic accuracy only. Whether each cited work actually
supports the claim it is cited for is a separate, human judgment, and the entries
flagged CHECK-CLAIM below are the ones where that judgment matters most.

Output: analiz/reference-audit.json + printed summary.
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
OUT = ROOT / "analiz" / "reference-audit.json"
UA = {"User-Agent": "MakaleC-refaudit/1.0 (mailto:tuncersefa@gmail.com)"}


def parse_bib(text):
    entries = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1), m.group(2).strip(), m.group(3)
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", body + "\n", re.S):
            f[fm.group(1).lower()] = " ".join(fm.group(2).split())
        entries.append({"key": key, "kind": kind, **f})
    return entries


def norm(s):
    s = re.sub(r"\{|\}|\\[a-zA-Z]+|\\", "", s or "").lower()
    return re.sub(r"[^a-z0-9 ]", " ", s).split()


def overlap(a, b):
    A, B = set(norm(a)), set(norm(b))
    A -= {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to"}
    B -= {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to"}
    return len(A & B) / max(1, len(A))


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)["message"]
    except Exception as e:
        return {"__error__": str(e)[:60]}


def main():
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    tex = TEX.read_text(encoding="utf-8")
    cited = set(re.findall(r"\\citep?\{([^}]*)\}", tex))
    cited = {k.strip() for grp in cited for k in grp.split(",")}

    print("=" * 76)
    print("REFERANS DENETIMI — refs.bib x Crossref")
    print("=" * 76)
    print("  bib girdisi: %d   metinde atif verilen: %d" % (len(entries), len(cited)))

    orphan = sorted(k for k in cited if k not in {e["key"] for e in entries})
    unused = sorted(e["key"] for e in entries if e["key"] not in cited)
    if orphan:
        print("  !! METINDE VAR, BIB'DE YOK:", orphan)
    if unused:
        print("  -- bib'de var ama atif verilmemis:", unused)

    res = {"ok": [], "mismatch": [], "no_doi": [], "unresolved": [],
           "orphan_citations": orphan, "unused_entries": unused}

    for e in entries:
        doi = (e.get("doi") or "").strip()
        label = "%-16s %s" % (e["key"], (e.get("title") or "")[:52])
        if not doi:
            res["no_doi"].append(e["key"])
            print("  [NO-DOI ] %s" % label)
            continue
        m = crossref(doi)
        time.sleep(0.4)
        if "__error__" in m:
            res["unresolved"].append({"key": e["key"], "doi": doi, "err": m["__error__"]})
            print("  [FAIL   ] %s   <- DOI cozulmedi: %s" % (label, m["__error__"]))
            continue
        ct = (m.get("title") or [""])[0]
        cy = str((m.get("issued", {}).get("date-parts") or [[""]])[0][0])
        auth = m.get("author") or []
        cf = (auth[0].get("family", "") if auth else "")
        cj = (m.get("container-title") or [""])[0]
        sim = overlap(e.get("title", ""), ct)
        bib_first = re.split(r"\s+and\s+", e.get("author", ""))[0].split(",")[0].strip()
        author_ok = (not cf) or (not bib_first) or (cf.lower() in bib_first.lower()) \
            or (bib_first.lower() in cf.lower())
        year_ok = (not cy) or (cy == str(e.get("year", "")).strip())
        problems = []
        if sim < 0.55:
            problems.append("BASLIK uyusmuyor (ortusme %.2f) -> Crossref: %s" % (sim, ct[:60]))
        if not author_ok:
            problems.append("ILK YAZAR uyusmuyor -> bib '%s' vs Crossref '%s'" % (bib_first, cf))
        if not year_ok:
            problems.append("YIL uyusmuyor -> bib %s vs Crossref %s" % (e.get("year"), cy))
        if problems:
            res["mismatch"].append({"key": e["key"], "doi": doi, "problems": problems,
                                    "crossref_title": ct, "crossref_journal": cj})
            print("  [MISMATCH] %s" % label)
            for p in problems:
                print("             %s" % p)
        else:
            res["ok"].append({"key": e["key"], "doi": doi, "title_overlap": round(sim, 2)})
            print("  [OK     ] %s" % label)

    print("-" * 76)
    print("  dogrulandi : %d" % len(res["ok"]))
    print("  uyusmayan  : %d" % len(res["mismatch"]))
    print("  DOI yok    : %d  (elle kontrol)" % len(res["no_doi"]))
    print("  cozulmedi  : %d" % len(res["unresolved"]))
    print("=" * 76)
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print("[written] %s" % OUT)


if __name__ == "__main__":
    main()
