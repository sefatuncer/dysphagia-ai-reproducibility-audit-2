# -*- coding: utf-8 -*-
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
    rng = random.Random(20260917)
    specs = []
    for name, k in zip(V["原变量名称"].tolist(), V["取值"].tolist()):
        k = ast.literal_eval(str(k))
        if isinstance(k, dict) and "step" in k:
            n = int(round((k["max"] - k["min"]) / k["step"]))
            specs.append(("num", [round(k["min"] + i * k["step"], 10) for i in range(n + 1)]))
        else:
            specs.append(("cat", list(k.values())))
    rows = []
    for _ in range(2000):
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
