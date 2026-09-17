# -*- coding: utf-8 -*-
"""Does the shipped model that still loads give the same predictions under the libraries it resolved to?

Why this exists. In the July 2026 build of Dai et al. (enoch0307/streamlitapp_cn), the
unpinned requirements file resolved scikit-learn to 1.9.0 and CatBoost to 1.2.10. One shipped
model (Multi.pkl) failed to load, which is a visible failure. The other (Binary.pkl) loaded with
an InconsistentVersionWarning and produced predictions. A crash is safe in the sense that nobody
uses its output; a model that loads and quietly predicts something different is not. A
pre-submission review of the manuscript (17 September 2026) asked whether that happened.
This script measures it.

What the model is. Binary.pkl is a scikit-learn Pipeline of a StandardScaler and a
CatBoostClassifier. The pickle records the versions it was built with: scikit-learn 1.6.1 (the
estimators' _sklearn_version) and CatBoost 1.2.8 (the build information CatBoost embeds in its
model). Both are read from the file's bytes below, without unpickling.

Design. A 2 x 2 of those two libraries, one clean python:3.11-slim container per cell (the
article specifies Python 3.11):
  training            scikit-learn 1.6.1, CatBoost 1.2.8   the versions recorded in the pickle
  catboost_resolved   scikit-learn 1.6.1, CatBoost 1.2.10  only CatBoost moves
  sklearn_resolved    scikit-learn 1.9.0, CatBoost 1.2.8   only the library that raised the warning moves
  resolved            scikit-learn 1.9.0, CatBoost 1.2.10  what the as-declared install resolved to in July
Every cell that scores is compared with training, input by input. A cell whose container cannot
score records the error instead, since a combination that fails outright is a visible failure,
not a silent one. Every other package is pinned to the July resolution (numpy 2.4.6, pandas 3.0.3, joblib 1.5.3,
openpyxl 3.1.5); the numpy and pandas versions of training are not recorded in the pickle. The
model and the configuration spreadsheet are downloaded from the commit current on the access
date and are not redistributed. A grid of inputs is drawn inside the training container from
the ranges and categories the application itself offers (变量1.xlsx), with a fixed seed, and the
same grid is scored in every container the way app.py scores it: one column per spreadsheet row,
in spreadsheet order, named positionally, passed to predict_proba.

Output: analiz/silent-drift-check.json -> archive results/
        analiz/rerun-loglari/silent-drift/ (Dockerfiles, probe script, logs) -> archive re-execution/logs/silent-drift/

Requires Docker; not part of scripts/reproduce.py.

Usage: python analiz/scripts/34_silent_drift_check.py
"""
import csv
import datetime
import hashlib
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request

from paths import BASE, out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = "enoch0307/streamlitapp_cn"
FILES = ["Binary.pkl", "变量1.xlsx"]
SEED = 20260917
N_RANDOM = 2000
COMMON = ["numpy==2.4.6", "pandas==3.0.3", "joblib==1.5.3", "openpyxl==3.1.5"]
ENVS = {
    "training": ["scikit-learn==1.6.1", "catboost==1.2.8"],
    "catboost_resolved": ["scikit-learn==1.6.1", "catboost==1.2.10"],
    "sklearn_resolved": ["scikit-learn==1.9.0", "catboost==1.2.8"],
    "resolved": ["scikit-learn==1.9.0", "catboost==1.2.10"],
}
REFERENCE = "training"
WORK = BASE / "analiz" / "rerun-loglari" / "silent-drift"

PROBE = r'''# -*- coding: utf-8 -*-
"""Score one fixed grid of inputs through Binary.pkl, the way app.py does."""
import ast, csv, json, random, sys, warnings
import joblib, numpy, pandas, sklearn
MODE = sys.argv[1]            # "make-grid-and-score" or "score"
COLS = ['dietary_character', 'Vital_capacity', 'Pharyngeal_function', 'Oral_function',
        'Esophageal_function', 'Airway_protection_function', 'Masticatory_and_buccal muscles',
        'F0Hz', 'Jitter', 'Shimmer']
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    model = joblib.load("/in/Binary.pkl")
    caught = sorted({"%s: %s" % (x.category.__name__, str(x.message)[:160]) for x in w})
if MODE == "make-grid-and-score":
    V = pandas.read_excel("/in/变量1.xlsx")
    rng = random.Random(__SEED__)
    specs = []
    for name, k in zip(V["原变量名称"].tolist(), V["取值"].tolist()):
        k = ast.literal_eval(str(k))
        if isinstance(k, dict) and "step" in k:
            n = int(round((k["max"] - k["min"]) / k["step"]))
            specs.append(("num", [round(k["min"] + i * k["step"], 10) for i in range(n + 1)]))
        else:
            specs.append(("cat", list(k.values())))
    rows = []
    for _ in range(__N__):
        rows.append([rng.choice(vals) for _, vals in specs])
    for corner in ("min", "max"):
        rows.append([(vals[0] if corner == "min" else vals[-1]) for _, vals in specs])
    with open("/out/grid.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([COLS] + rows)
X = pandas.read_csv("/out/grid.csv")
X.columns = COLS
with warnings.catch_warnings(record=True) as w2:
    warnings.simplefilter("always")
    P = model.predict_proba(X)
    caught2 = sorted({"%s: %s" % (x.category.__name__, str(x.message)[:160]) for x in w2})
json.dump({"sklearn": sklearn.__version__, "numpy": numpy.__version__, "pandas": pandas.__version__,
           "catboost": __import__("catboost").__version__, "joblib": joblib.__version__,
           "load_warnings": caught, "predict_warnings": caught2,
           "model_type": type(model).__name__,
           "steps": [type(s).__name__ for _, s in getattr(model, "steps", [])],
           "n": int(P.shape[0]), "proba": [[float(v) for v in r] for r in P]},
          open("/out/%s.json" % sys.argv[2], "w"))
print("scored", P.shape, "with sklearn", sklearn.__version__, "catboost", __import__("catboost").__version__)
'''.replace("__SEED__", str(SEED)).replace("__N__", str(N_RANDOM))


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def recorded_versions(data):
    """Versions the pickle itself records, read from its bytes (no unpickling)."""
    sk = sorted(set(m.decode() for m in re.findall(rb"_sklearn_version\x94\x8c.(\d+\.\d+\.\d+)", data)))
    cb = sorted(set(m.decode() for m in re.findall(rb"Branch: tags/v(\d+\.\d+\.\d+)", data)))
    return {"scikit-learn": sk, "catboost": cb}


def compare(a, b):
    diffs = [max(abs(x - y) for x, y in zip(ra, rb)) for ra, rb in zip(a, b)]
    flips = sum(1 for ra, rb in zip(a, b) if ra.index(max(ra)) != rb.index(max(rb)))
    return {"n_inputs": len(a), "identical_rows": sum(1 for d in diffs if d == 0.0),
            "max_abs_probability_difference": max(diffs),
            "mean_abs_probability_difference": sum(diffs) / len(diffs),
            "class_flips": flips}


def main():
    commit = [r for r in json.loads(result("commit-provenance.json").read_text(encoding="utf-8"))["repositories"]
              if r["repo"] == REPO][0]["commit"]
    WORK.mkdir(parents=True, exist_ok=True)
    for stale in WORK.glob("*"):
        if stale.is_file():
            stale.unlink()
    build = WORK / "_build"
    (build / "in").mkdir(parents=True, exist_ok=True)
    (build / "out").mkdir(parents=True, exist_ok=True)
    for stale in list((build / "out").glob("*")) + list(build.glob("Dockerfile.*")):
        stale.unlink()
    hashes = {}
    recorded = None
    for fn in FILES:
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, commit, urllib.parse.quote(fn))
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "dysphagia-repro-audit"}), timeout=120).read()
        (build / "in" / fn).write_bytes(data)
        hashes[fn] = hashlib.sha256(data).hexdigest()
        if fn == "Binary.pkl":
            recorded = recorded_versions(data)
    print("  versions recorded in Binary.pkl:", recorded)
    (build / "probe.py").write_text(PROBE, encoding="utf-8")
    (WORK / "probe.py").write_text(PROBE, encoding="utf-8")

    sh(["docker", "pull", "-q", "python:3.11-slim"])
    digest = sh(["docker", "image", "inspect", "python:3.11-slim", "--format", "{{index .RepoDigests 0}}"]).stdout.strip()
    logs = {}
    for env, pins in ENVS.items():
        dockerfile = ("FROM %s\nWORKDIR /w\nRUN pip install --no-cache-dir %s %s\nCOPY probe.py /w/probe.py\n"
                      % (digest, " ".join(pins), " ".join(COMMON)))
        (build / ("Dockerfile." + env)).write_text(dockerfile, encoding="utf-8")
        (WORK / ("Dockerfile." + env)).write_text(dockerfile, encoding="utf-8")
        tag = "audit-drift-" + env.replace("_", "-")
        b = sh(["docker", "build", "--no-cache", "--progress=plain", "-f", "Dockerfile." + env, "-t", tag, "."], cwd=build)
        logs[env] = {"build_exit": b.returncode}
        (WORK / ("build-" + env + ".log")).write_text(b.stdout + b.stderr, encoding="utf-8")
        print("  %-16s build exit %d" % (env, b.returncode))
    order = [(REFERENCE, "make-grid-and-score")] + [(e, "score") for e in ENVS if e != REFERENCE]
    for env, mode in order:
        if logs[env]["build_exit"] != 0:
            continue
        r = sh(["docker", "run", "--rm", "--network", "none",
                "-v", "%s:/in:ro" % (build / "in"), "-v", "%s:/out" % (build / "out"),
                "audit-drift-" + env.replace("_", "-"), "python", "/w/probe.py", mode, env])
        logs[env]["run_exit"] = r.returncode
        (WORK / ("run-" + env + ".log")).write_text(r.stdout + r.stderr, encoding="utf-8")
        tail = (r.stdout + r.stderr).strip().splitlines()
        if r.returncode != 0:
            errs = [ln for ln in tail if "Error" in ln and not ln.startswith(" ")]
            logs[env]["run_error"] = (errs[-1] if errs else (tail[-1] if tail else ""))[:300]
        print("  %-16s run exit %d  %s" % (env, r.returncode, tail[-1][:120] if tail else ""))

    res = {}
    for env in ENVS:
        p = build / "out" / (env + ".json")
        if p.exists():
            res[env] = json.loads(p.read_text(encoding="utf-8"))
    comparisons = {}
    for env in ENVS:
        if env != REFERENCE and env in res and REFERENCE in res:
            comparisons["%s_vs_%s" % (env, REFERENCE)] = compare(res[REFERENCE]["proba"], res[env]["proba"])
    spread = None
    if REFERENCE in res:
        p1 = [r[1] for r in res[REFERENCE]["proba"]]
        spread = {"min_p_class1": min(p1), "max_p_class1": max(p1), "distinct_values": len(set(p1)),
                  "predicted_class1": sum(1 for r in res[REFERENCE]["proba"] if r[1] > r[0])}
    for env in ENVS:
        sh(["docker", "rmi", "-f", "audit-drift-" + env.replace("_", "-")])
    grid_rows = None
    if (build / "out" / "grid.csv").exists():
        with open(build / "out" / "grid.csv", encoding="utf-8") as f:
            grid_rows = sum(1 for _ in csv.reader(f)) - 1

    payload = {
        "generated_by": "34_silent_drift_check.py",
        "run_on": datetime.date.today().isoformat(),
        "repo": REPO, "commit": commit, "files_sha256": hashes,
        "versions_recorded_in_pickle": recorded,
        "base_image": "python:3.11-slim", "base_image_digest": digest,
        "common_pins": COMMON,
        "environments": {e: {"pins": ENVS[e], "logs": logs.get(e),
                             "versions": ({k: res[e][k] for k in ("sklearn", "catboost", "numpy", "pandas", "joblib")}
                                          if e in res else None),
                             "load_warnings": res[e]["load_warnings"] if e in res else None,
                             "predict_warnings": res[e]["predict_warnings"] if e in res else None,
                             "model_type": res[e]["model_type"] if e in res else None,
                             "steps": res[e]["steps"] if e in res else None}
                         for e in ENVS},
        "grid": {"seed": SEED, "random_draws": N_RANDOM, "corners": 2, "rows": grid_rows,
                 "source": "ranges and categories offered by the application (变量1.xlsx)",
                 "reference_output_spread": spread},
        "reference": REFERENCE,
        "comparisons": comparisons,
        "scope": ("Binary.pkl only: Multi.pkl does not load under the resolved scikit-learn, so its failure "
                  "is visible and was reported in July. The numpy and pandas versions used in training are "
                  "not recorded in the pickle and are held at the July resolution. The model and spreadsheet "
                  "are fetched from the access-date commit and not redistributed; the grid is regenerated by "
                  "the released probe. Equal outputs on this grid do not prove equal outputs on every input."),
    }
    p = out("silent-drift-check.json")
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  comparisons:", json.dumps(comparisons))
    print("  written:", p)


if __name__ == "__main__":
    main()
