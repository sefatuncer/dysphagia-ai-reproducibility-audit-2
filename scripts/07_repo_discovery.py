#!/usr/bin/env python3
"""
07_repo_discovery.py - discover code-available dysphagia and swallowing AI repositories REPRODUCIBLY.

Objective, machine-checkable inclusion criterion: (i) dysphagia or swallowing AI, and
(ii) a publicly available code repository. Sources: the GitHub Search API and the Papers
with Code API. NO subjective screening.
Output: analiz/repo-envanteri-ham.csv, which is then vetted into repo-envanteri.csv.

Note: unauthenticated GitHub search is limited to about 10 requests per minute, hence the
sleep between query terms.
"""
import csv, json, sys, time, urllib.request, urllib.parse
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = "analiz/repo-envanteri-ham.csv"
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}

# dysphagia/swallowing x AI search terms (GitHub full-text repository search)
GH_QUERIES = [
    "dysphagia deep learning", "dysphagia machine learning", "dysphagia segmentation",
    "swallowing deep learning", "swallowing segmentation", "swallowing classification",
    "VFSS deep learning", "videofluoroscopy swallowing", "FEES swallowing endoscopy",
    "swallowing sound classification", "cervical auscultation swallow", "swallowing EMG classification",
    "deglutition neural network", "bolus segmentation fluoroscopy", "hyoid bone tracking swallow",
    "penetration aspiration deep learning", "swallow detection accelerometer",
]
PWC_QUERIES = ["dysphagia", "swallowing", "videofluoroscopy", "deglutition"]

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f"  ! {str(e)[:60]}  ({url[:70]})")
        return None

def github():
    rows = {}
    for q in GH_QUERIES:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=15"
        d = get(url)
        n = 0
        if d and "items" in d:
            for it in d["items"]:
                fn = it["full_name"]
                if fn in rows: continue
                rows[fn] = {
                    "source": "github", "repo": fn, "url": it.get("html_url", ""),
                    "stars": it.get("stargazers_count", 0),
                    "license": (it.get("license") or {}).get("spdx_id") or "",
                    "archived": it.get("archived", False),
                    "pushed_at": (it.get("pushed_at") or "")[:10],
                    "description": (it.get("description") or "").replace("\n", " ")[:160],
                    "found_via": q, "paper": "", "include": "", "notes": "",
                }
                n += 1
        print(f"  GH  [{q[:34]:34s}] +{n}  (total {len(rows)})")
        time.sleep(7)  # rate limit
    return rows

def pwc(rows):
    for q in PWC_QUERIES:
        url = f"https://paperswithcode.com/api/v1/search/?q={urllib.parse.quote(q)}"
        d = get(url)
        n = 0
        if d and "results" in d:
            for res in d["results"]:
                repo = (res.get("repository") or {})
                url_r = repo.get("url", "")
                if not url_r: continue
                fn = url_r.replace("https://github.com/", "").strip("/")
                paper = (res.get("paper") or {}).get("title", "")
                if fn in rows:
                    if not rows[fn]["paper"]: rows[fn]["paper"] = paper[:120]
                    continue
                rows[fn] = {
                    "source": "paperswithcode", "repo": fn, "url": url_r,
                    "stars": repo.get("stars", ""), "license": "", "archived": "",
                    "pushed_at": "", "description": "",
                    "found_via": f"pwc:{q}", "paper": paper[:120], "include": "", "notes": "",
                }
                n += 1
        print(f"  PWC [{q[:34]:34s}] +{n}  (total {len(rows)})")
        time.sleep(2)
    return rows

def main():
    print("=" * 64); print("REPOSITORY DISCOVERY - GitHub and Papers with Code"); print("=" * 64)
    rows = github()
    rows = pwc(rows)
    cols = ["source", "repo", "url", "stars", "license", "archived", "pushed_at",
            "description", "found_via", "paper", "include", "notes"]
    out = sorted(rows.values(), key=lambda r: -(int(r["stars"]) if str(r["stars"]).isdigit() else 0))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    print("-" * 64)
    print(f"TOTAL {len(out)} unique candidate repositories -> {OUT}")
    print("NOTE: `include` is empty; each candidate is vetted against the objective criterion (dysphagia/swallowing AI plus available code).")

if __name__ == "__main__":
    main()
