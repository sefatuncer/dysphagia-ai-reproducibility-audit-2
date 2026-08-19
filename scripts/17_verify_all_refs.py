#!/usr/bin/env python3
"""
17_verify_all_refs.py — verify every bibliography entry against Crossref.

Replaces the field parser used in 14_reference_audit.py, which required each field
to sit on its own line. Entries that packed several fields onto one line had their
DOI missed, so that script reported missing DOIs that were in fact present. Fields
are matched on brace balance here, not on line breaks.

For each entry with a DOI, the DOI is resolved and the returned title and first
author are compared with the entry. A resolving DOI proves nothing on its own: a
wrong DOI resolves to a real but unrelated paper, so both must match.

Output: analiz/reference-verification.json
"""
import json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "taslak" / "latex" / "refs.bib"
TEX = ROOT / "taslak" / "latex" / "makale-AiR.tex"
OUT = ROOT / "analiz" / "reference-verification.json"
UA = {"User-Agent": "MakaleC-refaudit/1.0 (mailto:tuncersefa@gmail.com)"}
STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "is", "are", "an"}


def parse_bib(text):
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", m.group(3), re.S):
            f[fm.group(1).lower()] = " ".join(fm.group(2).split())
        out.append({"key": m.group(2).strip(), **f})
    return out


def words(s):
    s = re.sub(r"\{|\}|\\[a-zA-Z]+|\\", "", s or "").lower()
    return {w for w in re.sub(r"[^a-z0-9 ]", " ", s).split() if w not in STOP}


def sim(a, b):
    A, B = words(a), words(b)
    return len(A & B) / max(1, max(len(A), len(B)))


def crossref(doi):
    try:
        req = urllib.request.Request(
            "https://api.crossref.org/works/" + urllib.parse.quote(doi), headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["message"]
    except Exception as e:
        return {"__error__": str(e)[:50]}


def main():
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    tex = TEX.read_text(encoding="utf-8")
    cited = set()
    for grp in re.findall(r"\\citep?\{([^}]*)\}", tex):
        cited |= {k.strip() for k in grp.split(",")}

    print("=" * 78)
    print("REFERANS DOGRULAMA (duzeltilmis parser)")
    print("=" * 78)
    print("  bib girdisi %d | metinde atif verilen %d" % (len(entries), len(cited)))
    keys = {e["key"] for e in entries}
    miss = sorted(cited - keys)
    unused = sorted(keys - cited)
    if miss:
        print("  !! METINDE VAR, BIB'DE YOK:", miss)
    if unused:
        print("  -- atif verilmemis:", unused)
    print("-" * 78)

    res = {"verified": [], "mismatch": [], "no_doi": [], "unresolved": [],
           "orphan": miss, "unused": unused}
    for e in entries:
        doi = (e.get("doi") or "").strip()
        title = e.get("title", "")
        bf = re.sub(r"\{|\}|\\[a-zA-Z]+", "",
                    re.split(r"\s+and\s+", e.get("author", ""))[0].split(",")[0]).strip()
        if not doi:
            res["no_doi"].append({"key": e["key"], "title": title})
            print("  [DOI-YOK ] %-18s %s" % (e["key"], title[:48]))
            continue
        m = crossref(doi)
        time.sleep(0.35)
        if "__error__" in m:
            res["unresolved"].append({"key": e["key"], "doi": doi, "err": m["__error__"]})
            print("  [COZULMEZ] %-18s %s  <- %s" % (e["key"], doi, m["__error__"]))
            continue
        ct = (m.get("title") or [""])[0]
        au = m.get("author") or []
        cf = au[0].get("family", "") if au else ""
        s = sim(title, ct)
        aok = (not cf) or (not bf) or cf.lower() in bf.lower() or bf.lower() in cf.lower()
        if s >= 0.55 and aok:
            res["verified"].append({"key": e["key"], "doi": doi, "overlap": round(s, 2)})
            print("  [DOGRULANDI] %-16s %-46s (ortusme %.2f)" % (e["key"], title[:46], s))
        else:
            res["mismatch"].append({"key": e["key"], "doi": doi, "overlap": round(s, 2),
                                    "bib_title": title, "crossref_title": ct,
                                    "bib_author": bf, "crossref_author": cf})
            print("  [UYUSMUYOR] %-16s ortusme %.2f  yazar %s" %
                  (e["key"], s, "OK" if aok else "FARKLI"))
            print("              bib      : %s / %s" % (bf, title[:56]))
            print("              crossref : %s / %s" % (cf, ct[:56]))

    print("-" * 78)
    print("  dogrulandi (baslik+yazar esti) : %d" % len(res["verified"]))
    print("  UYUSMUYOR (elle bak)           : %d" % len(res["mismatch"]))
    print("  DOI yok (dogal olabilir)       : %d" % len(res["no_doi"]))
    print("  DOI cozulmedi                  : %d" % len(res["unresolved"]))
    print("=" * 78)
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print("[written] %s" % OUT)


if __name__ == "__main__":
    main()
