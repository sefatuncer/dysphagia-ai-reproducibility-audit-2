# Code-link mining: vetting findings (script 10 — extraction from open-access full texts)

**Date:** 2026-07-16 · **Method:** `10_code_link_mining.py` — a Europe PMC search (dysphagia or swallowing × AI × code hosting, OPEN_ACCESS, 2010–2026) retrieved **394 open-access full texts** through the NCBI BioC service; github, gitlab, zenodo, osf and codeocean links were extracted by regular expression and deduplicated against the existing inventory.

**Raw output:** 163 links (143 new code repositories plus 20 archive or data links), recorded in `repo-inventory-extra.csv`.

## The central problem: noise from broad mining
Full-text mining sweeps up **tool citations** and **off-topic** articles in which dysphagia or swallowing appears only incidentally (head-and-neck cancer radiotherapy, EEG, Parkinson disease, drug interactions, oesophageal cancer). About 135 of the 143 had to be excluded:
- **Tool or infrastructure citations, not the study's own repository:** darknet, yolov7, labelme and LabelImg, opensmile, silero-vad, soxr, ggplot2, bwa, Trimmomatic, dcm2niix, h2o-3, EconML, boxmot, medcat, and a cluster of graph-neural-network libraries (GAT/pyGAT, LINE, deepwalk, SkipGNN, decagon, KnowDDI, GraphEmbedding), all of which come from a single off-topic drug-interaction article (PMC10978847).
- **Off-topic, with dysphagia or swallowing incidental:** lung, oesophageal, oral and gastric cancer, EEG and brain-computer interfaces, Parkinson disease, dementia, multiple sclerosis, ALS, thyroid and dental work — none of which is dysphagia-AI diagnosis or assessment.

## VETTING RESULT (objective: GitHub API plus Europe PMC abstract-scope confirmation)

### ✅ New IN-SCOPE code repositories (the study's own repository, and dysphagia or swallowing AI)
| Repository | Article | Journal / year | Scope | Intake signal | Skeleton verdict |
|---|---|---|---|---|---|
| `ResearchgroupMITI/swallow-detection` | PMC12678422 | Communications Medicine 2025 | swallow-event detection in long-term HRM (deep learning) | **CC0-1.0** license; no environment file; **0** weights; a `datasets/` folder; 24 code files | **not_attemptable** (no weights) |
| `enoch0307/streamlitapp_cn` | PMC12803820 | iScience 2026 | interpretable ML for dysphagia **screening and staging** (1235+720 patients, externally validated) | no license; **requirements.txt** present; **weights PRESENT** (`Binary.pkl`, `Multi.pkl`); streamlit `app.py` plus `code.py` | **ATTEMPTABLE** — CPU-friendly tabular ML → **the second candidate for an actual re-run** |
| `yonghunsong/Throat-related-events-classification` | PMC11706958 | npj Digital Medicine 2025 | wearable vibration-sensor dysphagia monitoring (multimodal ensemble) | no license, environment file or weights; 12 code files | **not_attemptable** (no weights) |
| `ruaeh/Dysphagia-ML` | PMC9537337 | Scientific Reports 2022 | ML on a voice biomarker for post-stroke aspiration and tube feeding | no license or environment file; **the repository is EMPTY (0 files)** | **not_attemptable** — "linked but empty": the code URL resolves, the repository has no content |

### ⚠️ BORDERLINE (adjacent to dysphagia; a scope decision)
| Repository | Article | Journal / year | Note |
|---|---|---|---|
| `PRI2MA/DL_NTCP_Dysphagia` | PMC12520315 | Radiotherapy & Oncology 2025 | NTCP prediction of **late dysphagia** after radiotherapy: prognostic toxicity prediction, not diagnosis or assessment. It belongs to the same class as `kwahid/ABAS`, so it is included in the census as borderline for consistency; no weights or environment file, hence not_attemptable. |
| `greenapple-sea/Esophagus-Motility-Data` | PMC11828345 | PLoS One 2025 | An HRM oesophageal-motility **data-only** deposit (no code, Apache-2.0). There is no model, so it falls outside the re-execution census; noted as an archive because the oesophageal phase is adjacent to dysphagia. |

### 📄 IN-SCOPE article with NO REPOSITORY OF ITS OWN (code not shared)
- **PMC12950097** — *Dysphagia* 2026, "Using ML for Automated Segmentation and Detection of Swallows … Preterm Neonates" (digital cervical auscultation, acoustic). The full text cites only `chirlu/soxr`, a resampling tool, so **no repository of its own was shared**. It is therefore an instance of "code not shared" in the transparency denominator, with no repository to re-run.

### ❌ OUT OF SCOPE (excluded)
- `Safnov/1` (PMC13290704) — prediction of stroke-associated pneumonia; not dysphagia assessment.
- `jhc050998/Strokeformer` (PMC12380291) — prognosis of thrombolysis eligibility in stroke; not dysphagia (the repository is nearly empty).
- Plus roughly 135 tool citations and off-topic repositories.

## Effect on the census
- **New re-execution census repositories: +5** (4 solidly in scope plus the borderline DL_NTCP) → **N: 17 → 22.**
- **The headline strengthens:** **2/22 are now attemptable** (VFSS_analysis, partial, and enoch0307), yet **none is fully re-executable out of the box**; weights, licenses and data remain systematically absent.
- **A new class of transparency failure:** `ruaeh/Dysphagia-ML` is "linked but empty" — the URL resolves and the repository has no content — a live instance of the gap between code sharing and re-executability.
- **Evidence of multi-modal discovery:** the repositories were found through three independent channels (GitHub search and Papers with Code in script 07, and open-access full-text mining in script 10), which increases confidence in the coverage of the census.

## enoch0307/streamlitapp_cn — preliminary inspection of the inference path (before the actual re-run)

> ⚠️ **Corrected by the actual re-run.** The preliminary inspection below concluded that the configuration spreadsheets were absent from the repository and that the app would therefore fail with `FileNotFoundError`. **The actual re-run found both `变量1.xlsx` and `变量2.xlsx` present, and they loaded successfully**; the repository failed out of the box for a different reason, namely dependency version drift on `Multi.pkl`. The authoritative record is `C-repo-003-enoch0307/verdict.md`. This section is retained unedited so that the correction is visible rather than silently overwritten.

Repository contents: `Binary.pkl`, `Multi.pkl` (joblib models), `app.py` (streamlit inference), `code.py` (training), `requirements.txt` (streamlit, xgboost, scikit-learn, catboost, shap, pandas, numpy, openpyxl), and two logo files. **Purely tabular ML: CPU-friendly, with no image processing and no GPU requirement.**
- `code.py` (training): `pd.read_csv("data2.csv")` → **data2.csv is absent from the repository** (confidential clinical data), so training cannot be repeated.
- `app.py` (inference): loads the shipped `Binary.pkl` and `Multi.pkl` through joblib (✓), and reads `pd.read_excel("变量1.xlsx")` and `变量2.xlsx` for the variable configuration → *the preliminary inspection recorded these spreadsheets as absent; see the correction above.*
- **Preliminary verdict, to be confirmed by the actual re-run:** even the **only** repository that shares both weights and an environment file fails out of the box; if the configuration can be reconstructed from the ten-feature list in the article, the outcome is likely **partial**, following the VFSS pattern of attemptable but requiring repair.
- **Narrative value:** this is the single strongest piece of evidence for the headline that code sharing is not re-executability, since even the repository that also shares weights does not run. enoch0307 is therefore the primary case-study candidate: iScience 2026 is a venue in good standing, which resolves the delisted-journal problem attaching to the VFSS pilot.
