# -*- coding: utf-8 -*-
"""Re-issue the code-link mining extraction without its de-duplication step.

Why this exists. `10_code_link_mining.py` skips any repository already present in the
candidate inventory before it records a link (`if key in existing: continue`). The
inventory at that point already held the GitHub-channel candidates and the two
feasibility pilots, so a repository that the mining channel did reach, but that another
source had found first, was dropped without a trace. The article reported that the
retained repositories of the two productive channels do not overlap at all, and built an
interpretation on it. That zero cannot be read from the released record, because the
pipeline removed exactly the links that would have shown an overlap.

What this does. It re-issues the same Europe PMC query with the same page limit, reads
every open-access full text through the same NCBI BioC service, applies the same
extraction expression and infrastructure denylist, and records every repository link
with the article it came from, with no de-duplication against the inventory. It then
reports which of the 22 included repositories appear among the mined links.

What it cannot do. It is a re-issue, not a replay: it runs on the date recorded in the
output, the search index has moved since 16 July 2026, and a different result set is
possible. It therefore measures whether the channel reaches the included repositories
now, which bounds, but does not reconstruct, what it reached on the original date.

Output: analiz/mining-overlap-check.json -> archive results/

Usage: python analiz/scripts/32_mining_overlap_check.py
"""
import csv
import datetime
import json
import re
import sys
import time
import urllib.parse
import urllib.request

from paths import out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
BIOC = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json"
UA = {"User-Agent": "dysphagia-repro-audit"}

# Identical to 10_code_link_mining.py.
QUERY = ('(dysphagia OR deglutition OR swallowing) '
         'AND ("deep learning" OR "machine learning" OR "neural network" OR "artificial intelligence" OR CNN) '
         'AND (github OR gitlab OR zenodo OR "code is available" OR "code available" OR "publicly available") '
         'AND (OPEN_ACCESS:y) AND (FIRST_PDATE:[2010 TO 2026])')
RX = re.compile(r'(?:https?://)?(?:www\.)?(github\.com|gitlab\.com|zenodo\.org|osf\.io|codeocean\.com)/'
                r'([A-Za-z0-9_.\-/]+)', re.I)
TOOL_DENY = {"pytorch", "tensorflow", "keras-team", "huggingface", "scikit-learn", "scikit", "numpy",
             "pandas", "matplotlib", "opencv", "ultralytics", "open-mmlab", "google-research",
             "facebookresearch", "nnunet", "mic-dkfz", "pyradiomics", "monai", "project-monai",
             "streamlit", "pallets", "python", "conda", "conda-forge", "docker", "microsoft",
             "nvidia", "openai", "scipy", "seaborn", "plotly"}
MAX_PAGES = 4


def get(url, as_json=True):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=35) as r:
            return json.load(r) if as_json else r.read().decode("utf-8", "ignore")
    except Exception:
        return None


def norm(host, path):
    host = host.lower()
    parts = path.strip("/").split("/")
    if host in ("github.com", "gitlab.com"):
        if len(parts) >= 2 and parts[0].lower() not in ("about", "features", "topics", "search", "orgs"):
            return f"{parts[0]}/{parts[1]}".replace(".git", "").rstrip(".,);:'\"")
    return None


def main():
    today = datetime.date.today().isoformat()
    included = []
    for r in csv.DictReader(result("included-studies.csv").open(encoding="utf-8-sig")):
        for repo in r["repositories"].split(";"):
            included.append((r["study_id"], repo.strip(), r["discovery_channel"]))

    pmcids, token, pages = [], "*", 0
    while pages < MAX_PAGES:
        d = get(f"{EPMC}/search?query={urllib.parse.quote(QUERY)}&format=json&pageSize=100"
                f"&resultType=lite&cursorMark={urllib.parse.quote(token)}")
        if not d or "resultList" not in d:
            break
        for res in d["resultList"].get("result", []):
            if res.get("pmcid") and res.get("inEPMC") == "Y":
                pmcids.append(res["pmcid"])
        nxt = d.get("nextCursorMark")
        if not nxt or nxt == token:
            break
        token, pages = nxt, pages + 1
        time.sleep(1)
    print("  open-access full texts to scan: %d" % len(pmcids))

    links = {}   # repo(lower) -> set of pmcids
    unread = 0
    for i, pmcid in enumerate(pmcids):
        txt = get(f"{BIOC}/{pmcid}/unicode", as_json=False)
        if not txt:
            unread += 1
            continue
        for host, path in RX.findall(txt):
            repo = norm(host, path)
            if repo and repo.split("/")[0].lower() not in TOOL_DENY:
                links.setdefault(repo.lower(), set()).add(pmcid)
        if (i + 1) % 50 == 0:
            print("  ...%d/%d scanned, %d distinct repository links" % (i + 1, len(pmcids), len(links)))
        time.sleep(0.4)

    rows, reached = [], 0
    for sid, repo, channel in included:
        hit = sorted(links.get(repo.lower(), []))
        reached += bool(hit)
        rows.append({"study": sid, "repo": repo, "recorded_channel": channel,
                     "reached_by_mining_on_reissue": bool(hit), "pmcids": hit})
        print("  %-2s %-58s %-8s mining re-issue: %s" % (sid, repo[:58], channel, ", ".join(hit) or "-"))

    by_channel = {}
    for r in rows:
        c = by_channel.setdefault(r["recorded_channel"], {"repositories": 0, "reached": 0})
        c["repositories"] += 1
        c["reached"] += int(r["reached_by_mining_on_reissue"])

    payload = {
        "generated_by": "32_mining_overlap_check.py",
        "reissued_on": today,
        "original_query_date": "2026-07-16",
        "query": QUERY,
        "max_pages": MAX_PAGES,
        "n_fulltexts_listed": len(pmcids),
        "n_fulltexts_unreadable": unread,
        "n_distinct_repository_links": len(links),
        "included_repositories_reached": reached,
        "by_recorded_channel": by_channel,
        "why": ("10_code_link_mining.py drops a link already present in the candidate "
                "inventory before recording it, so the released record cannot show whether "
                "the mining channel also reached repositories that another source found "
                "first. This re-issue records every link."),
        "limits": ("A re-issue on a later date against a moved search index, not a replay of "
                   "the original run. It shows what the channel reaches now."),
        "rows": rows,
    }
    p = out("mining-overlap-check.json")
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n  included repositories reached on re-issue: %d of %d" % (reached, len(rows)))
    print("  by recorded channel: %s" % json.dumps(by_channel))
    print("  written: %s" % p)


if __name__ == "__main__":
    main()
