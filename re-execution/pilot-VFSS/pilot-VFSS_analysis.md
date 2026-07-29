# Layer B pilot — BSEL-UC3M/VFSS_analysis (feasibility, plan and outcome)

**Date:** 13 July 2026 · **Purpose:** to demonstrate on a single repository that the Docker re-run method (Layer B) actually works.
**Repository:** https://github.com/BSEL-UC3M/VFSS_analysis · **Weights:** Zenodo 10.5281/zenodo.17191973 · **Source article:** Comput Biol Med 2025, doi:10.1016/j.compbiomed.2025.109759

## Web inspection — verified facts
| Item | Finding |
|---|---|
| Language / dependencies | Python (100%); a conda `environment.yml` plus `setup.py` |
| Framework | **nnU-Net v1** (training and inference) |
| GPU / CPU | CPU compatibility is **not stated explicitly** (nnU-Net v1 falls back to CPU when no GPU is present, but slowly, and some paths may hard-code `.cuda()`) |
| Model weights | **Present and public:** Zenodo `models_VFSS.zip`, **6.1 GB**, **CC-BY-4.0**; placed in `models/` (Task010 default, Task008 secondary) |
| Example data | ✅ **Included:** `data/raw_VFSS/test/healthy_001` (AVI) plus **manual labels, predictions and parameters** |
| How it runs | clone → `conda env create -f environment.yml` → `pip install -e .` → pipeline (pre-processing → nnU-Net inference → labelled video → 21 dysphagia parameters) |
| Metrics | not in the README; in the source article |
| **Code license** | ⚠️ **ABSENT (not stated)** — there is no LICENSE file in the repository |
| Dockerfile | none |

## Feasibility verdict: ✅ HIGH — close to a best-case pilot
- ✅ **Example data are included**, so inference can be run without private patient data, which removes the largest barrier.
- ✅ **Weights are public (CC-BY)** and can be downloaded.
- ✅ **The supplied predictions and parameters give a ready reproduction target**: our re-run output can be compared against the repository's own output within tolerance (segmentation plus the 21 parameters).
- ✅ The conda `environment.yml` can be containerized.
- ⚠️ **CPU inference with nnU-Net v1** is possible but slow and undocumented, so CPU may have to be forced (`CUDA_VISIBLE_DEVICES=""`); if hard-coded `.cuda()` paths appear, a small patch is needed — **which is itself a reproducibility finding** and is recorded in the rubric.
- ⚠️ A 6.1 GB weights download plus the old nnU-Net v1 dependency chain (Python 3.7–3.9, an old PyTorch) makes version pinning essential.

## Three side findings worth recording
1. **The source article is in Computers in Biology and Medicine**, which was **delisted from Web of Science on 17 November 2025**. The code and model are still available and the repository is valid, but the reproducibility of an AI study published in a delisted journal is an interesting case and is used in the discussion.
2. **There is no code license**, so default copyright applies (all rights reserved). Running it for research is not a problem, but it must not be redistributed; and this is the first concrete data point for "license: absent" in the transparency rubric.
3. The study concerns VFSS in **head-and-neck cancer** rather than stroke, but since the scope is dysphagia AI of any aetiology, it is **included**.

## Containerization plan (draft Dockerfile logic)
```
FROM continuumio/miniconda3
# 1) repository and environment
RUN git clone https://github.com/BSEL-UC3M/VFSS_analysis.git /app
WORKDIR /app
RUN conda env create -f environment.yml        # LOG the resolved versions (pip freeze as evidence)
SHELL ["conda","run","-n","<env>","/bin/bash","-c"]
RUN pip install -e .
# 2) weights (may be fetched outside the build; 6.1 GB)
#    Zenodo models_VFSS.zip → /app/models/ ; record the SHA256
# 3) force CPU
ENV CUDA_VISIBLE_DEVICES=""
ENV nnUNet_* ...   # nnU-Net v1 path variables
# 4) inference on the example
#    data/raw_VFSS/test/healthy_001 → preprocess → nnU-Net predict → parameters
```
**Reproduction target:** compare the segmentation and 21 parameters produced by the re-run against the **supplied `predictions` and `parameters`** in the repository, giving a verdict of full, partial or not reproduced against a tolerance of ±5 percentage points or the reported 95% interval.

## Static pre-audit findings (repository cloned; from the real files — this is rubric row C-repo-001)
The repository was cloned and `environment.yml`, `setup.py`, `run.py` and `paths_repository.py` were read. Even before running it, these **reproducibility findings** emerged:

1. **🔴 HEADLINE — the declared dependencies are internally UNSATISFIABLE (empirically confirmed):** nnU-Net v1.7.1 requires numpy < 1.24 (it uses the removed `np.bool` and `np.int`), yet **at least two packages in the declared environment** require numpy ≥ 1.24 — `scikit-image==0.25.0` **and** `MedPy==0.5.2`. In a real build pip returned `ResolutionImpossible`, so running the study required **three mandatory downgrades** (numpy 2.1.3 → 1.23.5, scikit-image 0.25 → 0.19.3, MedPy 0.5.2 → 0.4.0). Evidence: `logs/dep-conflict-pip-resolver.txt`. The study cannot be reproduced "as declared".
2. **`environment.yml` is internally inconsistent:** it specifies `python=3.10` alongside `python_abi=3.13`, the signature of a broken `conda env export`.
3. **`torch` is unpinned** in setup.py while the environment carries nvidia-cu12 (CUDA) wheels, which gives both version drift and an implicit GPU assumption.
4. **No license** (there is no LICENSE file), so default copyright applies and the code must not be redistributed.
5. `setup.py` calls `find_namespace_packages(include=["VFSS"])` but the repository contains no `VFSS/` package, so `pip install -e .` installs an empty package; the study actually runs through `python run.py`, importing modules from the working directory.
6. **The source article is in Comput Biol Med**, delisted from Web of Science on 17 November 2025. The cohort is **head-and-neck cancer** — not stroke, but dysphagia AI and therefore in scope.
7. **A supplied reproduction target exists:** `data/output_data/.../*.csv` (7 parameter series), which was copied to `reference_outputs/`.
8. **🔴 Obscure, fragile and undeclared dependencies:** `VFSS_functions.py` contains `import spicy` — `spicy` being the well-known typo package for scipy — and `environment.yml` duly pins `spicy==0.16.0`; without it the import fails with `ModuleNotFoundError`. In addition `pydicom` is imported at module level but **is not listed in setup.py**, an undeclared dependency.

**Actual re-run (live, 13 July):** the best-effort image **built and its imports work** (numpy 1.23.5 / torch 2.0.1+cpu / skimage 0.19.3 / nnunet 1.7.1 / batchgenerators 0.25.3; provenance in `logs/pip-freeze-best-effort.txt`). The weights (6.1 GB, CC-BY) were downloaded and the layout corrected (`models_VFSS/nnUNet` → `models/nnUNet`). **Five-fold CPU inference completed** (246 frames, about 3.9 hours). **Result:** the code **did not run out of the box** — the declared environment is unsatisfiable (three downgrades plus spicy and pydicom), there is a **NameError crash** (`pathlib.Path` is never imported, in step 3), and post-processing is missing (`postprocessing.json` is absent) → **five documented interventions** were required. After the repairs it ran, and `compare.py` shows **structurally identical output** (7 parameters × 246 frames) but **numerically close rather than identical** (areas within about 0.1%; landmark and distance parameters deviating by up to 6 units), attributable to the skipped post-processing and to environment and CPU-versus-GPU differences. **VERDICT: PARTIAL, not reproducible out of the box.** Evidence: `logs/rerun-crash-findings.txt` and the comparison log; the `rerun_verdict` for C-repo-001 in the rubric was updated accordingly.

**The script set is available** in this folder: `Dockerfile`, `download_weights.sh`, `run_pilot.sh` / `.ps1`, `compare.py` and `RUNBOOK.md`. The heavy part — a 6.1 GB download plus CPU inference — runs as a single command; see the RUNBOOK.

## Outcome
This repository is the **first record** of the Layer B sample, and the pipeline demonstrated here was subsequently applied to the other candidates.
