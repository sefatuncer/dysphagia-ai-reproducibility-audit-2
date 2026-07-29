#!/usr/bin/env python3
"""
10_code_link_mining.py - extract code-repository links from open-access FULL TEXTS (to widen the census).

A GitHub search misses repositories that are only cited inside articles. This script
searches Europe PMC open-access full texts (dysphagia/swallowing x AI x code hosting),
extracts github, gitlab, zenodo and osf URLs from the full text by regular expression,
deduplicates them against the existing inventory, and reports the new candidates.
Reproducible, and behind no paywall: open-access full text only.

Output: analiz/repo-envanteri-ek.csv (the new candidates) plus a stdout summary.
"""
import csv, json, re, sys, time, urllib.request, urllib.parse
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
INV = "analiz/repo-envanteri.csv"
OUT = "analiz/repo-envanteri-ek.csv"
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}

QUERY = ('(dysphagia OR deglutition OR swallowing) '
         'AND ("deep learning" OR "machine learning" OR "neural network" OR "artificial intelligence" OR CNN) '
         'AND (github OR gitlab OR zenodo OR "code is available" OR "code available" OR "publicly available") '
         'AND (OPEN_ACCESS:y) AND (FIRST_PDATE:[2010 TO 2026])')

RX = re.compile(r'(?:https?://)?(?:www\.)?(github\.com|gitlab\.com|zenodo\.org|osf\.io|codeocean\.com)/'
                r'([A-Za-z0-9_.\-/]+)', re.I)
BIOC = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json"
# common infrastructure and tool repositories (NOT a study's own repository) - excluded
TOOL_DENY = {"pytorch","tensorflow","keras-team","huggingface","scikit-learn","scikit","numpy",
    "pandas","matplotlib","opencv","ultralytics","open-mmlab","google-research","facebookresearch",
    "nnunet","mic-dkfz","pyradiomics","monai","project-monai","streamlit","pallets","python",
    "conda","conda-forge","docker","microsoft","nvidia","openai","scipy","seaborn","plotly"}

def get(url, as_json=True):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=35) as r:
            return json.load(r) if as_json else r.read().decode("utf-8", "ignore")
    except Exception as e:
        return None

def search(page_token="*"):
    q = urllib.parse.quote(QUERY)
    url = f"{EPMC}/search?query={q}&format=json&pageSize=100&resultType=lite&cursorMark={urllib.parse.quote(page_token)}"
    return get(url)

def norm(host, path):
    host = host.lower(); parts = path.strip("/").split("/")
    if host == "github.com" or host == "gitlab.com":
        if len(parts) >= 2 and parts[0].lower() not in ("about","features","topics","search","orgs"):
            repo = f"{parts[0]}/{parts[1]}"
            return repo.replace(".git", "").rstrip(".,);:'\"")
        return None
    if host == "zenodo.org": return f"zenodo:{parts[-1]}" if parts else None
    if host == "osf.io": return f"osf:{parts[0]}" if parts else None
    if host == "codeocean.com": return f"codeocean:{parts[-1]}" if parts else None
    return None

def main():
    existing = set()
    try:
        for r in csv.DictReader(open(INV, encoding="utf-8")):
            existing.add(r["repo"].lower())
    except Exception: pass

    print("=" * 68); print("CODE-LINK MINING - Europe PMC open-access full text"); print("=" * 68)
    # 1) search (a few pages)
    pmcids = []
    token = "*"; pages = 0
    while pages < 4:
        d = search(token)
        if not d or "resultList" not in d: break
        for res in d["resultList"].get("result", []):
            if res.get("pmcid") and res.get("inEPMC") == "Y":
                pmcids.append((res["pmcid"], res.get("title", "")[:80]))
        nxt = d.get("nextCursorMark")
        print(f"  search page {pages+1}: +{len(d['resultList'].get('result', []))} results, {len(pmcids)} open-access PMC")
        if not nxt or nxt == token: break
        token = nxt; pages += 1; time.sleep(1)

    # 2) look for repository links in each open-access full text (via NCBI BioC PMC-OA;
    #    fullTextXML is empty for the most recent articles)
    found = {}
    for i, (pmcid, title) in enumerate(pmcids):
        txt = get(f"{BIOC}/{pmcid}/unicode", as_json=False)
        if not txt: continue
        hits = set()
        for host, path in RX.findall(txt):
            r = norm(host, path)
            if r and not (r.split("/")[0].lower() in TOOL_DENY): hits.add(r)
        for r in hits:
            key = r.lower()
            if "github.com/" in ("github.com/" + key) and "/" in r and not r.startswith(("zenodo","osf","codeocean")):
                if key in existing: continue
                found.setdefault(r, {"repo": r, "type": "code", "pmcid": pmcid, "paper": title})
            else:
                found.setdefault(r, {"repo": r, "type": "archive/data", "pmcid": pmcid, "paper": title})
        if (i + 1) % 20 == 0:
            print(f"  ...{i+1}/{len(pmcids)} full texts scanned, {len(found)} links")
        time.sleep(0.4)

    # 3) keep only code repositories (github/gitlab) that are NEW, i.e. absent from the inventory
    new_code = {k: v for k, v in found.items()
                if v["type"] == "code" and k.lower() not in existing}
    cols = ["repo", "type", "pmcid", "paper", "include", "notes"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for v in sorted(found.values(), key=lambda x: (x["type"], x["repo"])):
            v["include"] = ""; v["notes"] = ""; w.writerow(v)
    print("-" * 68)
    print(f"Open-access full texts scanned: {len(pmcids)} · total links: {len(found)} · NEW code repositories: {len(new_code)}")
    for r in sorted(new_code): print(f"  + {r}")
    print(f"-> {OUT}  (all links; the new code repositories are vetted via `include`)")

if __name__ == "__main__":
    main()
