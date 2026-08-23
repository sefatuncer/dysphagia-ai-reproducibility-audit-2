# RUNBOOK — Layer B pilot (BSEL-UC3M/VFSS_analysis)

Purpose: to demonstrate on a single repository that the Docker re-run method (Layer B) works, and
to document reproducibility friction **with evidence**. The repository is cloned into
`./VFSS_analysis` and the reference outputs are backed up in `./reference_outputs`.
*(Neither directory is redistributed in this archive: the repository is third-party code and the
reference outputs are its own output. Both are reconstructed by the steps below.)*

## Prerequisites
- **Docker Desktop running** (the audit machine had Docker 29.6.1).
- About 15 GB free disk (6.1 GB of weights plus the image and intermediate files), and an internet connection.
- Windows: `run_pilot.ps1`; Git Bash or WSL: `run_pilot.sh`.

## Files in this folder
| File | Role |
|---|---|
| `VFSS_analysis/` | The cloned repository (code, the example `healthy_001` AVI, and the supplied outputs) |
| `reference_outputs/` | A **backup** of the supplied output CSV and AVI files, kept for comparison because run.py overwrites them |
| `Dockerfile` | The best-effort CPU environment, with the deviations noted in comments |
| `download_weights.sh` | Downloads the 6.1 GB weights from Zenodo and unpacks them into `models/` |
| `run_pilot.sh` / `.ps1` | build → run.py (CPU) → compare, as a single command |
| `compare.py` | Compares the regenerated CSVs against the reference and issues a verdict |
| `rerun.log`, `compare.log` | Produced when you run this pilot; **not shipped in the archive** (see Provenance below) |

## Reproduction target and tolerance
run.py executes four steps (pre-processing → nnU-Net inference → labelled video → 21 parameters). The comparison is between the **regenerated `data/output_data/.../*.csv`** and **`reference_outputs/.../*.csv`**. The path from segmentation to parameters should be deterministic, so full reproduction means values that agree almost exactly (compare.py uses atol 1e-6, rtol 1e-3).
*(Note: the ±5 percentage point or 95% interval tolerance applies to accuracy metrics; for the continuous parameter series used here, a near-equality test is applied instead.)*

## A) The "as-declared" (faithful) attempt — run this first, for the evidence
The aim is to test whether the study installs **as declared**. **Expectation: it fails.**
```bash
docker run --rm -v "$PWD/VFSS_analysis":/work/repo -w /work/repo \
  continuumio/miniconda3:24.9.2-0 \
  bash -lc "conda env create -f environment.yml && conda run -n VFSS_env pip install -e . && echo BUILD_OK"
```
**Save the complete error message.** The failures anticipated by the static pre-audit were:
1. `environment.yml` is internally inconsistent: `python=3.10` alongside `python_abi=3.13`, which can break the conda solve.
2. **A dependency conflict (the headline finding):** `scikit-image==0.25.0` requires numpy ≥ 1.24, while `nnunet==1.7.1` requires numpy < 1.24 (it uses the removed `np.bool` and `np.int`). The two cannot be satisfied at once.
3. `torch` is **unpinned** in setup.py while the environment carries nvidia-cu12 (CUDA) wheels, which gives version drift.
4. `setup.py` calls `find_namespace_packages(include=["VFSS"])` but the repository has no `VFSS/` package, so the installation produces an empty package.

## B) Best-effort CPU run — to demonstrate the method
```bash
bash download_weights.sh          # 6.1 GB, once
bash run_pilot.sh                 # build → run → compare
# Windows: powershell -File run_pilot.ps1   (fetch the weights from Git Bash)
```
The **deviations** in the Dockerfile (numpy 1.23.5, scikit-image 0.19.3, CPU torch) exist precisely to get past conflicts (2) and (3), and **those deviations are themselves the finding**: this is the set of departures from the declared environment that running the study required.

## Result and what it demonstrates
- The verdict was **partial**: reproducible only after non-trivial environment surgery, which both shows that the method works and yields a concrete account of reproducibility friction.
- **Weights layout (verified):** the zip unpacks as `models/models_VFSS/nnUNet/2d/TaskXXX`, but run.py hard-codes `RESULTS_FOLDER=repo/models`, overriding any environment variable, so **`models/models_VFSS/nnUNet` must be moved to `models/nnUNet`**, giving `models/nnUNet/2d/Task010_VFSS/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0..4` plus `plans.pkl`.
- CPU inference with nnU-Net v1 is slow but acceptable for a single example (246 frames took about 3.9 hours).

## Provenance (the evidence chain, as actually published)
Stored under `../logs/`:
- `pip-freeze-best-effort.txt` — the versions actually installed in the best-effort container.
- `dep-conflict-pip-resolver.txt` — the as-declared attempt: the exact command and the resolver output showing the declared dependency set is unsatisfiable.
- `rerun-crash-findings.txt` — what ran, what crashed, and the comparison result.

**Weights provenance.** The deposit publishes an MD5 for the file we downloaded: `models_VFSS.zip`, 6.15 GB, `md5:4eb596ba49fdecf283bf839681369eb0`, CC-BY-4.0, Zenodo record 17191973, retrieved by `scripts/26_external_deposit_provenance.py` and written to `results/external-deposit-provenance.json`. A third party can use it to confirm that the file they download is the file the record holds. *It does not establish that our copy matched:* we did not hash the file during the run and deleted it afterwards, so bit-identity with what we held is not demonstrable and we do not claim it. *(Corrected 2026-08-23: this paragraph previously read “we did not record a checksum for the 6.1 GB weights download”. That was true of our own copy and remains true, but it left the depositor's published checksum unrecorded when it was retrievable all along. The earlier wording is quoted here rather than deleted.)*

**Not published, stated so the chain is not overclaimed:** the raw `rerun.log` and `compare.log` are not archived; the crash findings file summarises both. The rubric row is C-repo-001 in `../../transparency/transparency-rubric.csv`.
