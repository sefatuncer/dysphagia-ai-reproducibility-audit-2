#!/usr/bin/env python3
"""
18_verify_author_lists.py — verify the FULL author list of every reference against Crossref.

Script 17 verifies title overlap and the FIRST author only, so a reference can pass it while
its co-author list is wrong. This script compares the complete set of family names in each
bib entry against the author list Crossref returns for that DOI, and reports
missing, extra and out-of-order names.

Input : taslak/latex/refs.bib
Output: analiz/author-list-verification.json plus stdout
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

BIB = "taslak/latex/refs.bib"
OUT = "analiz/author-list-verification.json"
MAILTO = "tuncersefa@gmail.com"
UA = {"User-Agent": f"repro-audit/1.0 (mailto:{MAILTO})"}


def strip_accents(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def clean_name(s):
    """Normalize a family name for comparison: strip LaTeX escapes, accents, case.
    The trailing space of a LaTeX accent command is consumed too, so that a source
    form such as {\\c c}alves does not become 'c alves'."""
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)       # \'{i} or {\c c} -> {i} / {c}
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    s = strip_accents(s).lower().strip()
    s = re.sub(r"[^a-z\- ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def name_matches(name, pool):
    """Match tolerantly: Crossref sometimes drops a nobiliary prefix, so
    'de araujo' and 'araujo' are treated as the same family name."""
    if name in pool:
        return True
    tail = name.split()[-1] if name.split() else name
    for p in pool:
        if p == tail or (p.split()[-1] if p.split() else p) == tail:
            return True
    return False


def parse_bib(path):
    """Yield (key, author_field, doi) for every @article/@book/@misc entry."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    entries = []
    for m in re.finditer(r"@\w+\s*\{\s*([^,]+),", text):
        key = m.group(1).strip()
        start = m.end()
        nxt = text.find("\n@", start)
        body = text[start:nxt if nxt != -1 else len(text)]
        def field(name):
            fm = re.search(name + r"\s*=\s*", body, re.I)
            if not fm:
                return ""
            i = fm.end()
            if body[i] == "{":
                depth = 0
                for j in range(i, len(body)):
                    if body[j] == "{": depth += 1
                    elif body[j] == "}":
                        depth -= 1
                        if depth == 0:
                            return body[i+1:j]
                return ""
            em = re.match(r'"([^"]*)"|([^,\n]*)', body[i:])
            return (em.group(1) or em.group(2) or "").strip() if em else ""
        entries.append((key, " ".join(field("author").split()), field("doi").strip()))
    return entries


def bib_families(author_field):
    """Extract family names from a BibTeX author field ('Last, First and Last, First')."""
    out = []
    for part in re.split(r"\s+and\s+", author_field):
        part = part.strip()
        if not part:
            continue
        if "," in part:
            fam = part.split(",")[0]
        else:
            fam = part.split()[-1] if part.split() else part
        fam = clean_name(fam)
        if fam:
            out.append(fam)
    return out


def crossref_families(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                msg = json.load(r).get("message", {})
            fams = []
            for a in msg.get("author", []) or []:
                fam = a.get("family") or a.get("name") or ""
                fam = clean_name(fam)
                if fam:
                    fams.append(fam)
            return fams, msg.get("title", [""])[0]
        except Exception as e:
            if "404" in str(e):
                return None, "__404__"
            time.sleep(2)
    return None, "__error__"


def main():
    entries = parse_bib(BIB)
    print("=" * 78)
    print("FULL AUTHOR-LIST VERIFICATION vs Crossref")
    print("=" * 78)
    print(f"  bib entries: {len(entries)}")
    print("-" * 78)

    report, n_ok, n_bad, n_skip = [], 0, 0, 0
    for key, author_field, doi in entries:
        bib_f = bib_families(author_field)
        if not doi:
            print(f"  [NO DOI  ] {key:18s} ({len(bib_f)} authors in bib) - cannot verify")
            n_skip += 1
            report.append({"key": key, "status": "no_doi", "bib_authors": bib_f})
            continue
        cr_f, title = crossref_families(doi)
        time.sleep(0.3)
        if cr_f is None:
            print(f"  [UNRESOLVED] {key:18s} doi={doi} ({title})")
            n_skip += 1
            report.append({"key": key, "status": "unresolved", "doi": doi})
            continue
        # A corporate author (a society, academy or committee) is cited under the body's
        # own name, while Crossref lists the constituent committees. Comparing the two
        # is meaningless, so such entries are reported separately rather than as errors.
        CORPORATE = ("academies", "committee", "society", "board", "association",
                     "collaboration", "group", "consortium", "organization")
        if len(bib_f) <= 2 and any(w in " ".join(bib_f) for w in CORPORATE):
            print(f"  [OK (corporate)    ] {key:18s} {' / '.join(bib_f)}")
            n_ok += 1
            report.append({"key": key, "status": "ok_corporate", "bib_authors": bib_f})
            continue

        # "and others" in the bib field means the list is deliberately truncated to
        # "et al.", so names absent from the bib are expected and are not an error.
        truncated = "others" in bib_f
        named = [f for f in bib_f if f != "others"]
        extra = [f for f in named if not name_matches(f, cr_f)]     # in bib, absent from Crossref
        missing = [] if truncated else [f for f in cr_f if not name_matches(f, named)]
        # a truncated list must still start with the real leading authors, in order
        order_ok = all(name_matches(named[i], [cr_f[i]]) for i in range(min(len(named), len(cr_f))))
        if not missing and not extra and order_ok:
            flag = "OK (et al.)" if truncated else "OK"
            print(f"  [{flag:18s}] {key:18s} {len(named)} named of {len(cr_f)} in Crossref")
            n_ok += 1
            report.append({"key": key, "status": "ok", "truncated": truncated,
                           "n_named": len(named), "n_crossref": len(cr_f)})
        else:
            print(f"  [MISMATCH        ] {key:18s} doi={doi}")
            print(f"        bib      ({len(bib_f)}): {', '.join(bib_f)}")
            print(f"        crossref ({len(cr_f)}): {', '.join(cr_f)}")
            if extra:
                print(f"        NOT IN CROSSREF (wrong name): {', '.join(extra)}")
            if missing:
                print(f"        MISSING FROM BIB: {', '.join(missing)}")
            if not order_ok:
                print(f"        AUTHOR ORDER differs from Crossref")
            n_bad += 1
            report.append({"key": key, "status": "mismatch", "doi": doi,
                           "bib_authors": bib_f, "crossref_authors": cr_f,
                           "not_in_crossref": extra, "missing_from_bib": missing,
                           "order_ok": order_ok, "truncated": truncated})

    print("-" * 78)
    print(f"  author list matches Crossref : {n_ok}")
    print(f"  MISMATCH (fix these)         : {n_bad}")
    print(f"  not verifiable (no DOI etc.) : {n_skip}")
    print("=" * 78)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"[written] {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
