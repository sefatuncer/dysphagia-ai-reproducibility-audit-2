# Layer B re-run verdict — repository C-repo-002 (UofTNeurology/masa-open-source)
# Date: 2026-07-14 | Environment: python:3.10-slim Docker, as-declared pip install | SECOND, REPUTABLE-VENUE CASE

## Metadata
- Study: **Saab R, et al.** (Balachandar, Mahdi, Nashnoush, … Khosravani), *Machine-learning assisted swallowing assessment … post-stroke dysphagia,* **Frontiers in Neuroscience 2023;17:1302132** (10.3389/fnins.2023.1302132) — **Web of Science indexed and in good standing**, unlike the venue of repository #1 (delisted), which closes the "showcase" objection that the audit only re-runs artifacts from problematic journals. ⚠️ *Correction (16 Jul): this record first named "Alkhadrawi et al." in error; the Crossref author list contains no Alkhadrawi and the first author is Rami Saab.*
- Modality: acoustic (spectral analysis of swallowing sounds, CNN) | Task: post-stroke dysphagia screening (TOR-BSST label)
- License: present (LICENSE.md) | Trained weights: **absent** | Example data: **absent** (the user must supply their own .wav)

## 1. As-declared (faithful) attempt — re-executability
- Command: `docker run python:3.10-slim → pip install -r requirements.txt`
- Result: **BUILD_FAIL** (EXIT=1)
- Error: `ERROR: pocketsphinx-0.1.15-cp37-cp37m-win_amd64.whl is not a supported wheel on this platform`
- Root cause: `requirements.txt` pins one dependency **to the developer's local machine**:
  `pocketsphinx @ file:///C:/Users/[redacted]/pipwin/pocketsphinx-0.1.15-cp37-cp37m-win_amd64.whl`
  → (a) the path `file:///C:/Users/[redacted]/...` exists on no other machine; (b) a cp37 + win_amd64 wheel installs only under Windows Python 3.7. **Non-portable dependency specification.**
- Runs out of the box: **no** (fails at the first `pip install` step).

## 2. Best-effort repairs (friction taxonomy)
Not attempted, as it is not needed for the primary finding. Had it been required: replace the pocketsphinx line with a PyPI release and add the system packages `swig` / `libpulse`. The absence of weights and data blocks inference independently of the environment.

## 3. Inference (CPU)
**not_attemptable** — no trained weights and no example or supplied data, so inference cannot be attempted.

## 4. Comparison
- Re-executable (did the environment build): **no** (non-portable dependency).
- Metric reproduction: **not applicable** (no weights, no data).

## 5. VERDICT
**not_re_executable (environment) + not_attemptable (inference)**
- Barrier categories: `undeclared_dependency` / **`hardcoded_local_path` (non-portable wheel)** · `missing_weights` · `missing_data` · `platform_locked` (cp37/win)
- One sentence: *A repository from a reputable journal (Front Neurosci) cannot be installed out of the box because `requirements.txt` pins a non-portable wheel to a developer's local Windows path; since neither weights nor data are shared, inference cannot be attempted either.*

## 6. Provenance (DO NOT DELETE)
Captured build output: [`as-declared.log`](as-declared.log) (the failing `pip install` and its exit code) · repository clone: shallow clone of the default branch, working copy not retained · accessed 11 July 2026 · `requirements.txt` line 30 (pocketsphinx `file://`).

**Limitation, stated rather than papered over:** we recorded the access date but not the upstream commit SHA at the time of the clone, and the working clone was not kept. A third party can therefore reach *a* state of this repository, but not provably the state we observed. We do not reconstruct a SHA after the fact, because a SHA read today would identify a different state and would be a fabricated record of provenance in a paper whose subject is provenance. The same limitation applies to the other audited repositories and is reported in the manuscript.

## Audit value
This yields verdicts covering **two distinct classes of friction in two reputable repositories**:
- repository #1 (VFSS): crashes out of the box (dependency conflict + NameError + missing post-processing) → structurally identical output after five repairs.
- repository #2 (masa): cannot be installed out of the box (non-portable local-path wheel) and ships neither weights nor data → not_attemptable.
→ This strengthens the lower-bound argument that even a best-case subset does not run out of the box, and it widens the barrier taxonomy.
