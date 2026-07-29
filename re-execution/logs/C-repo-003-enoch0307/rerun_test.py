#!/usr/bin/env python3
"""
enoch0307/streamlitapp_cn - OUT-OF-THE-BOX re-execution test (the as-declared environment).
It mirrors the inference path of app.py exactly: imports, then load the models with
joblib, then read the configuration spreadsheets, then predict on synthetic input using
the shipped model.
Question: does a repository that ships both weights (.pkl) and configuration run inference out of the box?
Each step has its own try/except, which yields the barrier taxonomy.
"""
import sys, traceback
sys.stdout.reconfigure(encoding="utf-8")
REPO = "repo"
def step(name, fn):
    try:
        r = fn(); print(f"[OK ] {name}"); return r
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:300]}")
        return None

print("="*70); print("enoch0307 OUT-OF-THE-BOX RE-EXECUTION (as-declared, clean virtual environment)"); print("="*70)

# 1) the imports of app.py (declared and used)
def imp():
    import streamlit, joblib, pandas, plotly.express, matplotlib, shap
    return True
step("app.py imports (streamlit/joblib/pandas/plotly/matplotlib/shap)", imp)

import joblib, pandas as pd, numpy as np, warnings
warnings.simplefilter("always")

# 2) load the shipped weights (the heart of re-executability)
import os
mb = step("load Binary.pkl (joblib)", lambda: joblib.load(os.path.join(REPO,"Binary.pkl")))
mm = step("load Multi.pkl (joblib)",  lambda: joblib.load(os.path.join(REPO,"Multi.pkl")))
print(f"     Binary type: {type(mb).__name__ if mb is not None else 'ABSENT'} | Multi type: {type(mm).__name__ if mm is not None else 'ABSENT'}")

# 3) read the configuration spreadsheets (the UI variables of app.py)
v1 = step("read 变量1.xlsx", lambda: pd.read_excel(os.path.join(REPO,"变量1.xlsx")))
v2 = step("read 变量2.xlsx", lambda: pd.read_excel(os.path.join(REPO,"变量2.xlsx")))
if v1 is not None: print(f"     变量1 columns: {list(v1.columns)[:8]}")

# 4) synthetic input built from the feature sets in app.py, then an actual prediction
binary_cols = ['dietary_character','Vital_capacity','Pharyngeal_function','Oral_function',
    'Esophageal_function','Airway_protection_function','Masticatory_and_buccal muscles','F0Hz','Jitter','Shimmer']
multi_cols = ['BMI','dietary_character','Vital_capacity','Pharyngeal_function','Oral_function',
    'Esophageal_function','Tongue_muscles','Masticatory_and_buccal muscles','Pharyngeal_muscles','Shimmer']

def pred(model, cols, label):
    if model is None: raise RuntimeError("the model did not load (the previous step FAILED)")
    X = pd.DataFrame([[1.0]*len(cols)], columns=cols)  # synthetic mid-value input
    y = model.predict(X)
    proba = getattr(model,"predict_proba",lambda x:None)(X)
    return (y, proba)
step("actual Binary prediction (synthetic input)", lambda: pred(mb, binary_cols, "binary"))
step("actual Multi prediction (synthetic input)",  lambda: pred(mm, multi_cols, "multi"))

print("="*70); print("TEST COMPLETE - the [FAIL] lines above constitute the barrier taxonomy.")
