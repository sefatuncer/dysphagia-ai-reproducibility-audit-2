#!/usr/bin/env python3
"""
10_code_link_mining.py — açık-erişim TAM-METİNLERDEN kod-deposu linklerini çıkar (census genişletme).

GitHub-arama makalelere-gömülü repoları kaçırır. Europe PMC OA tam-metinlerinde
(dysphagia/swallow × AI × kod-hosting) arayıp fullTextXML'den github/gitlab/zenodo/osf
URL'lerini regex ile çıkarır → mevcut envantere karşı dedup → yeni adaylar.
Tekrarlanabilir; paywall YOK (yalnız OA tam-metin).

Çıktı: analiz/repo-envanteri-ek.csv (yeni adaylar) + stdout özet.
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
# yaygın altyapı/araç repoları (çalışmanın kendi reposu DEĞİL) — elenir
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

    print("=" * 68); print("KOD-LİNK MINING — Europe PMC OA tam-metin"); print("=" * 68)
    # 1) arama (birkaç sayfa)
    pmcids = []
    token = "*"; pages = 0
    while pages < 4:
        d = search(token)
        if not d or "resultList" not in d: break
        for res in d["resultList"].get("result", []):
            if res.get("pmcid") and res.get("inEPMC") == "Y":
                pmcids.append((res["pmcid"], res.get("title", "")[:80]))
        nxt = d.get("nextCursorMark")
        print(f"  arama sayfa {pages+1}: +{len(d['resultList'].get('result', []))} sonuç, {len(pmcids)} OA-PMC")
        if not nxt or nxt == token: break
        token = nxt; pages += 1; time.sleep(1)

    # 2) her OA tam-metinde repo linki ara (NCBI BioC PMC-OA — fullTextXML yeni makalelerde boş)
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
            print(f"  ...{i+1}/{len(pmcids)} tam-metin tarandı, {len(found)} link")
        time.sleep(0.4)

    # 3) yalnız code-repo (github/gitlab), envanterde olmayan, YENİ adaylar
    new_code = {k: v for k, v in found.items()
                if v["type"] == "code" and k.lower() not in existing}
    cols = ["repo", "type", "pmcid", "paper", "include", "notes"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for v in sorted(found.values(), key=lambda x: (x["type"], x["repo"])):
            v["include"] = ""; v["notes"] = ""; w.writerow(v)
    print("-" * 68)
    print(f"Taranan OA tam-metin: {len(pmcids)} · toplam link: {len(found)} · YENİ code-repo: {len(new_code)}")
    for r in sorted(new_code): print(f"  + {r}")
    print(f"→ {OUT}  (tüm linkler; yeni code-repolar `include` ile vet edilecek)")

if __name__ == "__main__":
    main()
