#!/usr/bin/env python3
"""
13_backward_coverage.py — backward-coverage check against two independent reviews.

A reviewer asked for an upper-bound argument on channel coverage: our discovery
uses GitHub Search, Papers with Code, and open-access full-text mining, which
defines a tool-reachable universe rather than a topic universe. This script tests
that universe against the study sets of two independent syntheses of the same
literature (Kwok 2025, 24 studies; Silva/CoDAS 2025, 64 records), neither of which
used our channels.

Procedure, per study: resolve the DOI to a PubMed Central ID, retrieve the
open-access full text through the NCBI BioC service, and mine it for code-repository
URLs with the same regex and tool-denylist as the code-link mining script. Then ask
whether any repository so found is already in our census.

Reported honestly in three buckets, because full text is not retrievable for every
study: (a) code-declaring and already in our census, (b) code-declaring and NOT in
our census (a genuine miss), (c) not assessable (no OA full text). Studies with OA
full text and no repository URL count as code-unavailable, which is a finding, not a
miss.

Output: analiz/backward-coverage.json + printed summary.
"""
import csv, json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out as out_path

OUT = out_path("backward-coverage.json")
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
BIOC = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json"
IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"

RX = re.compile(r'(?:https?://)?(?:www\.)?(github\.com|gitlab\.com|zenodo\.org|osf\.io|codeocean\.com)/'
                r'([A-Za-z0-9_.\-/]+)', re.I)
TOOL_DENY = {"pytorch", "tensorflow", "keras-team", "huggingface", "scikit-learn", "scikit",
             "numpy", "pandas", "matplotlib", "opencv", "ultralytics", "open-mmlab",
             "google-research", "facebookresearch", "nnunet", "mic-dkfz", "pyradiomics",
             "monai", "project-monai", "streamlit", "pallets", "python", "conda",
             "conda-forge", "docker", "microsoft", "nvidia", "openai", "scipy", "seaborn",
             "plotly", "librosa", "mne-tools", "biopython"}


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
        if len(parts) >= 2 and parts[0].lower() not in ("about", "features", "topics",
                                                        "search", "orgs"):
            return f"{parts[0]}/{parts[1]}".replace(".git", "").rstrip(".,);:'\"")
        return None
    return None


def load_review_dois():
    """Return {doi: source} for both reviews, de-duplicated."""
    # Both files are required. They were previously guarded with if exists(),
    # which meant a missing comparator pool produced an empty set and a
    # "zero leakage" result rather than an error.
    dois = {}
    for logical, tag in (("kwok-matches", "kwok"), ("codas-matches", "codas")):
        for r in csv.DictReader(open(inp(logical), encoding="utf-8")):
            d = (r.get("doi") or "").strip().lower()
            if d:
                dois.setdefault(d, set()).add(tag)
    return dois


def load_census():
    """Repository names already in our census (the 22)."""
    # The inventory now carries a closed decision for every candidate, so census
    # membership is read straight off it: the 22 rows marked yes. It previously
    # also accepted needs-check and then had to subtract one repository by name
    # (greenapple-sea, a data deposit dropped at intake), which meant the census
    # could not be reconstructed from the released file alone.
    inv = inp("repo-inventory")
    names = {(r["repo"] or "").strip().lower()
             for r in csv.DictReader(open(inv, encoding="utf-8"))
             if (r.get("include") or "").strip().lower() == "yes"}
    if len(names) != 22:
        sys.exit(f"census should be 22 repositories, inventory gives {len(names)}")
    return names


def doi_to_pmcid(doi):
    url = IDCONV + "?tool=makalec&email=tuncersefa@gmail.com&format=json&ids=" + \
        urllib.parse.quote(doi)
    d = get(url)
    if not d:
        return None
    for rec in d.get("records", []):
        if rec.get("pmcid"):
            return rec["pmcid"]
    return None


def main():
    dois = load_review_dois()
    census = load_census()
    print("=" * 72)
    print("BACKWARD COVERAGE — iki bagimsiz derlemenin calismalarina karsi")
    print("=" * 72)
    print("  Kwok 2025 + CoDAS 2025, benzersiz DOI: %d" % len(dois))
    print("  Census repo sayisi (karsilastirma tabani): %d" % len(census))
    print("-" * 72)

    res = {"in_census": [], "code_not_in_census": [], "oa_no_code": [], "not_assessable": []}
    for i, (doi, srcs) in enumerate(sorted(dois.items()), 1):
        pmcid = doi_to_pmcid(doi)
        time.sleep(0.35)
        if not pmcid:
            res["not_assessable"].append({"doi": doi, "src": sorted(srcs),
                                          "reason": "no PMC id"})
            continue
        txt = get(f"{BIOC}/{pmcid}/unicode", as_json=False)
        time.sleep(0.35)
        if not txt:
            res["not_assessable"].append({"doi": doi, "src": sorted(srcs), "pmcid": pmcid,
                                          "reason": "no OA full text"})
            continue
        repos = set()
        for host, path in RX.findall(txt):
            r = norm(host, path)
            if r and r.split("/")[0].lower() not in TOOL_DENY:
                repos.add(r)
        if not repos:
            res["oa_no_code"].append({"doi": doi, "src": sorted(srcs), "pmcid": pmcid})
            continue
        hit = sorted(r for r in repos if r.lower() in census)
        entry = {"doi": doi, "src": sorted(srcs), "pmcid": pmcid, "repos": sorted(repos)}
        if hit:
            entry["matched"] = hit
            res["in_census"].append(entry)
        else:
            res["code_not_in_census"].append(entry)
        if i % 20 == 0:
            print("  ...%d/%d islendi" % (i, len(dois)))

    n_code = len(res["in_census"]) + len(res["code_not_in_census"])
    print("-" * 72)
    print("  Tam-metin degerlendirilemedi (OA degil / PMC yok) : %d" % len(res["not_assessable"]))
    print("  OA tam-metin var, kod deposu BEYAN EDILMEMIS      : %d" % len(res["oa_no_code"]))
    print("  Kod deposu beyan eden calisma                     : %d" % n_code)
    if n_code:
        print("     -> census'umuzda BULUNAN                     : %d (%.0f%%)"
              % (len(res["in_census"]), 100 * len(res["in_census"]) / n_code))
        print("     -> census'umuzda BULUNMAYAN (gercek kacak)   : %d" % len(res["code_not_in_census"]))
    if res["code_not_in_census"]:
        print("\n  KACANLAR (elle vet gerekir):")
        for e in res["code_not_in_census"]:
            print("    %-42s %s" % (e["doi"][:42], ", ".join(e["repos"][:3])))
    print("=" * 72)

    OUT.write_text(json.dumps(
        {"n_unique_dois": len(dois), "census_size": len(census),
         "counts": {k: len(v) for k, v in res.items()},
         "code_declaring": n_code, "detail": res}, indent=2), encoding="utf-8")
    print("[written] %s" % OUT)


if __name__ == "__main__":
    main()
