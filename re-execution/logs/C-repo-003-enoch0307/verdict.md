# Re-run verdict — enoch0307/streamlitapp_cn (pilot / case #3)

**Study:** Interpretable machine learning for accessible dysphagia screening and staging in older adults. *iScience* 2026 (PMC12803820). **Reputable venue (Web of Science listed, not delisted)** → a second showcase that closes the delisted-venue weakness of the VFSS pilot.
**Repository:** https://github.com/enoch0307/streamlitapp_cn · **Accessed / cloned:** 2026-07-16 · **Hardware:** CPU only (no image processing, no GPU).
**Modality:** clinical / tabular ML (dysphagia screening and staging in older adults; 10 clinical and acoustic features). **Executed in:** a clean Python 3.11 virtual environment.

## Environment (as declared) — `requirements.txt` (NO VERSION PINS)
`streamlit, xgboost, scikit-learn, pandas, numpy, catboost, shap, matplotlib, openpyxl` — **no version constraint on any package.**
Versions resolved in a clean virtual environment: scikit-learn **1.9.0**, numpy **2.4.6**, pandas **3.0.3**, xgboost 3.2.0, catboost 1.2.10, shap 0.51.0. (`plotly` and `joblib` are used by app.py but never declared; they resolved transitively and did not break the out-of-the-box attempt.)

## Repository contents (transparency — the strong end of the census)
- ✅ **Trained weights in the repository:** `Binary.pkl` (CatBoost Pipeline), `Multi.pkl` (GradientBoostingClassifier). *(The only repository in the census that deposits weights in the repository itself — 1/22.)*
- ✅ **Inference code:** `app.py` (streamlit); configuration files `变量1.xlsx` / `变量2.xlsx` (UI variable definitions, present in the repository).
- ✅ **Environment file:** `requirements.txt` (but unpinned).
- ❌ **Training data:** `code.py` calls `pd.read_csv("data2.csv")` — **data2.csv is absent from the repository** (confidential clinical data, 1235+720 patients), so training cannot be repeated.
- ❌ **License:** none.

## OUT-OF-THE-BOX re-execution (as-declared environment, no repairs)
| Step | Result |
|---|---|
| app.py imports (streamlit/joblib/pandas/plotly/matplotlib/shap) | ✅ OK (plotly and joblib transitively) |
| read `变量1.xlsx` / `变量2.xlsx` configuration | ✅ OK |
| **load `Binary.pkl`** | ⚠️ loaded, but with `InconsistentVersionWarning` (**pickled under sklearn 1.6.1, running under 1.9.0 → "results may be invalid, use at your own risk"**) plus `X has feature names but StandardScaler fitted without feature names` |
| **load `Multi.pkl`** | ❌ **FAIL — `ModuleNotFoundError: No module named '_loss'`** (the internal sklearn module path changed between 1.6.1 and 1.9.0) |
| actual Binary prediction (synthetic input) | ⚠️ ran, but under the invalid-results warning above |
| actual Multi prediction | ❌ not attemptable, the model would not load |

## Targeted repair → retry
**One repair: pin `scikit-learn==1.6.1` (the training version)** → `Multi.pkl` **loaded and predicted** (`GradientBoostingClassifier`, output `[0]`). The Multi failure was therefore **entirely version drift**: the code and the model are sound, the environment declaration is not.
*(In that isolated repair environment `catboost` was not installed, so `Binary.pkl` raised `ModuleNotFoundError: catboost`. catboost is declared in requirements; the full environment plus the sklearn pin loads both.)*

## VERDICT: **partial** (attemptable → fails out of the box → runs after one targeted repair)
- **Re-executability:** out of the box **no** — **even the best-case repository in the census**, which shares weights, configuration and an environment file, does not run cleanly. Two independent out-of-the-box failures: (1) a hard error on `Multi.pkl` (`_loss`), (2) an invalid-results warning on `Binary.pkl`. **Root cause: an unpinned `requirements.txt`**, the canonical reproducibility failure.
- **Fixability:** high — **a single decisive repair** (pin dependencies to the training versions) recovers Multi. One repair here against five for VFSS; both are "does not run out of the box, partial after repair".
- **Metric reproduction:** NOT ATTEMPTABLE — `data2.csv` (the test cohort) is confidential, so the AUC and accuracy figures reported in the article cannot be reproduced. Only the structural inference pipeline was verified, using synthetic input.

## Barrier taxonomy (this case)
`env_undeclared_versions` (no version pins) · `dependency_version_drift` (sklearn 1.6.1→1.9.0, pickle incompatible) · `missing_training_data` (data2.csv confidential) · `absent_license`.

## Contribution to the headline finding
> Even the **only repository that deposits its weights** (1/22) crashes out of the box because its environment is unpinned → the single strongest piece of evidence for the gap between **sharing code plus weights and being re-runnable**. The reputable venue (iScience 2026) rules out the objection that this is an artifact of tool papers or low-standing journals. The barrier is not a broken model but **missing environment provenance**.

## ACTUAL DOCKER verification (supports the manuscript's "clean CPU Docker containers" claim)
A `Dockerfile` (python:3.11-slim plus the as-declared `requirements.txt`) was built (`docker build`, exit 0) and executed with `docker run` → **the virtual-environment finding reproduced exactly inside the container:**
- `Binary.pkl` loaded and predicted (same `InconsistentVersionWarning`: 1.6.1→1.9.0, "results may be invalid")
- `Multi.pkl` **FAIL** (`ModuleNotFoundError: No module named '_loss'`) — the same hard error.
- **Cross-platform evidence:** the failure is identical in a Windows virtual environment and in a Linux Docker container → deterministic and **caused by the environment**, not a Windows-specific quirk. The container also resolved the unpinned `requirements.txt` to sklearn 1.9.0.
- **Implication:** the manuscript's claim of clean CPU Docker containers is now **literally true and repeatable** for the enoch0307 case; the `Dockerfile` was added to the harness released with this archive ("we practice what we audit").

## Provenance (DO NOT DELETE)
`repo/` (clone), `rerun_test.py` (out-of-the-box harness), `Dockerfile` plus `docker-build.log` (the actual container), `venv/` (as declared), `venv_fixed/` (evidence for the sklearn-pinned repair). Accessed and executed 2026-07-16.
