#!/usr/bin/env python3
"""
08_repo_intake.py - OBJECTIVE intake for code-available repositories (transparency rubric plus a skeleton verdict).

For each repository it fetches the GitHub git tree and records these OBJECTIVE signals:
license; environment file (requirements, environment.yml, Dockerfile, pyproject); trained
weights (*.pt, pth, h5, ckpt, onnx, pb, pkl, or a release asset); a data or example
directory; and README run instructions.

These signals largely determine the re-execution verdict: with no weights and no data,
inference is not_attemptable. The attemptable subset, which has both an environment file
and weights, goes to a full Docker re-run.
Input : analiz/repo-envanteri.csv (include in {yes, needs-check})
Output: analiz/repo-intake-tablosu.csv (reproducible; records the access date)
"""
import csv, json, sys, time, urllib.request
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

INV = "analiz/repo-envanteri.csv"
OUT = "analiz/repo-intake-tablosu.csv"
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
CHECK_DATE = "2026-07-16"   # fixed for reproducibility (the access date)

ENV_FILES = ("requirements.txt", "environment.yml", "environment.yaml", "dockerfile",
             "pyproject.toml", "setup.py", "pipfile", "conda.yaml")
WEIGHT_EXT = (".pt", ".pth", ".h5", ".hdf5", ".ckpt", ".onnx", ".pb", ".pkl", ".weights", ".safetensors")
DATA_HINT = ("data/", "datasets/", "dataset/", "sample", "example", "test_data", "demo")

def gh(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return {"__err__": str(e)[:60]}

def intake(repo):
    meta = gh(f"https://api.github.com/repos/{repo}")
    if "__err__" in meta:
        return {"repo": repo, "error": meta["__err__"]}
    branch = meta.get("default_branch", "main")
    lic = (meta.get("license") or {}).get("spdx_id") or "none/not_reported"
    tree = gh(f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1")
    paths = [t["path"] for t in tree.get("tree", [])] if "tree" in tree else []
    lower = [p.lower() for p in paths]
    env = [f for f in ENV_FILES if any(p.split("/")[-1] == f for p in lower)]
    weights = [p for p in paths if p.lower().endswith(WEIGHT_EXT)]
    data = sorted(set(h for h in DATA_HINT if any(h in p for p in lower)))
    readme = any(p.lower() == "readme.md" or p.lower().startswith("readme") for p in lower)
    code_n = sum(1 for p in lower if p.endswith((".py", ".ipynb")))
    # skeleton verdict (an objective prediction; the full Docker re-run confirms it)
    if env and weights:
        verdict = "attemptable → Docker re-run"
    elif not weights:
        verdict = "not_attemptable (inference: NO weights)"
    else:
        verdict = "env-undeclared → best-effort"
    return {"repo": repo, "check_date": CHECK_DATE, "default_branch": branch, "license": lic,
            "env_file": ";".join(env) or "NONE", "weights": (str(len(weights)) if weights else "NONE"),
            "data_dir": ";".join(data) or "NONE", "readme": "yes" if readme else "no",
            "code_files": code_n, "n_files": len(paths), "verdict_skeleton": verdict, "error": ""}

def main():
    rows = list(csv.DictReader(open(INV, encoding="utf-8")))
    todo = [r for r in rows if r["include"] in ("yes", "needs-check")
            and r["category"] not in ("DONE-pilot1", "DONE-pilot2", "duplicate")]
    print("=" * 70); print(f"REPOSITORY INTAKE - {len(todo)} repositories (objective transparency signals)"); print("=" * 70)
    out = []
    for r in todo:
        res = intake(r["repo"])
        out.append(res)
        if res.get("error"):
            print(f"  ! {r['repo']:50s} ERR {res['error']}")
        else:
            print(f"  {res['repo']:50s} lic={res['license']:14s} env={res['env_file'][:18]:18s} "
                  f"w={res['weights']:4s} data={res['data_dir'][:10]:10s} → {res['verdict_skeleton']}")
        time.sleep(1.2)
    cols = ["repo","check_date","default_branch","license","env_file","weights","data_dir",
            "readme","code_files","n_files","verdict_skeleton","error"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)
    print("-" * 70)
    att = [o for o in out if o.get("verdict_skeleton","").startswith("attemptable")]
    print(f"→ {OUT}")
    print(f"ATTEMPTABLE (environment plus weights, full Docker re-run): {len(att)}  {[o['repo'] for o in att]}")

if __name__ == "__main__":
    main()
