# Layer B — the general Docker re-run harness (repositories #2..N)

This generalizes the pilot (repository #1, VFSS_analysis) into a **reusable** protocol. The aim is to re-run every code-available study through the SAME auditable steps, so that verdicts are consistent and the barriers can be classified.

**Hardware:** 32 GB RAM / 16 cores / Docker 29 / **CPU only**. GPU-scale retraining is out of scope, and that limit is documented rather than implicit.

## Steps (for each repository)

### 0. Intake (vet first — fill in `repo-intake.md`)
License · CPU compatibility · example or supplied data · dependency file · weights DOI. **An absent license** is itself the first transparency finding, a legal barrier to reuse; re-executability is still attempted.

### 1. The "as-declared" (faithful) attempt — THE PRIMARY FINDING
Install and run the repository **exactly as documented**. The question is whether it runs out of the box, that is, re-executability. **Record the complete error message** in `logs/<repo-id>/as-declared.log`. Failure is expected for most repositories, and that failure is the headline finding.

### 2. Best-effort minimal repairs — THE FRICTION TAXONOMY
Every intervention needed to make it run is numbered (dependency downgrade, an undeclared package, a code fix, a missing artifact). These constitute **quantified friction**, the second finding.

### 3. Inference (CPU) — not training
Run inference on the supplied or example data. If an operation is GPU-only, attempt a CPU patch; if that fails, the verdict is `not_attemptable (GPU-only)`.

### 4. Comparison — re-executability first, metrics second
- **First:** did the artifact run and produce **its own documented output**?
- **Then**, only where example or reference data exist: is the reported metric within tolerance (±5 percentage points or the reported 95% interval; for continuous series, near-equality within an absolute and relative tolerance)?
- A confidential test cohort makes metric reproduction structurally impossible; record that as a **finding**.

### 5. Verdict and log
`re_executable / partial / not_reproduced / not_attemptable`, plus the barrier taxonomy and the number of repairs → fill in `verdict-log.template.md` → store under `logs/<repo-id>/`.

## Barrier taxonomy (fixed categories, for synthesis)
`dep_conflict` · `unpinned_versions` · `undeclared_dependency` · `typo_package` · `code_bug` (import or path) · `missing_weights` · `missing_postprocessing_artifact` · `gpu_only_op` · `missing_data` · `undocumented_step` · `license_absent`.

## Files
- `Dockerfile.template` — a parametric CPU environment (change the base image and Python version).
- `verdict-log.template.md` — the standard verdict form, one per repository.
- `repo-intake.md` — the vetting form, one per repository.
- Reference pattern: `../pilot-VFSS/` (repository #1 as a full case) and `../logs/`.
