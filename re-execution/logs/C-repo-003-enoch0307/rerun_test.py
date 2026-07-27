#!/usr/bin/env python3
"""
enoch0307/streamlitapp_cn — KUTU-DIŞI re-execution testi (as-declared ortam).
app.py'nin çıkarım-yolunu birebir taklit eder: import → joblib model yükle →
config Excel oku → shipped modelle sentetik girdi üzerinde predict.
Amaç: shipped ağırlık (.pkl) + config paylaşan repo kutu-dışı çıkarım yapıyor mu?
Her adım ayrı try/except → engel taksonomisi.
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

print("="*70); print("enoch0307 KUTU-DIŞI RE-EXECUTION (as-declared clean venv)"); print("="*70)

# 1) app.py'nin importları (declared+used)
def imp():
    import streamlit, joblib, pandas, plotly.express, matplotlib, shap
    return True
step("app.py importları (streamlit/joblib/pandas/plotly/matplotlib/shap)", imp)

import joblib, pandas as pd, numpy as np, warnings
warnings.simplefilter("always")

# 2) shipped ağırlık yükle (re-executability'nin kalbi)
import os
mb = step("Binary.pkl yükle (joblib)", lambda: joblib.load(os.path.join(REPO,"Binary.pkl")))
mm = step("Multi.pkl yükle (joblib)",  lambda: joblib.load(os.path.join(REPO,"Multi.pkl")))
print(f"     Binary tip: {type(mb).__name__ if mb is not None else 'YOK'} | Multi tip: {type(mm).__name__ if mm is not None else 'YOK'}")

# 3) config Excel oku (app.py UI değişkenleri)
v1 = step("变量1.xlsx oku", lambda: pd.read_excel(os.path.join(REPO,"变量1.xlsx")))
v2 = step("变量2.xlsx oku", lambda: pd.read_excel(os.path.join(REPO,"变量2.xlsx")))
if v1 is not None: print(f"     变量1 kolonları: {list(v1.columns)[:8]}")

# 4) app.py'deki özellik setleriyle sentetik girdi + fiili predict
binary_cols = ['dietary_character','Vital_capacity','Pharyngeal_function','Oral_function',
    'Esophageal_function','Airway_protection_function','Masticatory_and_buccal muscles','F0Hz','Jitter','Shimmer']
multi_cols = ['BMI','dietary_character','Vital_capacity','Pharyngeal_function','Oral_function',
    'Esophageal_function','Tongue_muscles','Masticatory_and_buccal muscles','Pharyngeal_muscles','Shimmer']

def pred(model, cols, label):
    if model is None: raise RuntimeError("model yüklenemedi (önceki adım FAIL)")
    X = pd.DataFrame([[1.0]*len(cols)], columns=cols)  # sentetik orta-değer girdi
    y = model.predict(X)
    proba = getattr(model,"predict_proba",lambda x:None)(X)
    return (y, proba)
step("Binary model fiili predict (sentetik girdi)", lambda: pred(mb, binary_cols, "binary"))
step("Multi model fiili predict (sentetik girdi)",  lambda: pred(mm, multi_cols, "multi"))

print("="*70); print("TEST BİTTİ — yukarıdaki [FAIL] satırları engel taksonomisi.")
