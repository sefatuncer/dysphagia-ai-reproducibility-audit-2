# Measurement definitions — the operational rules behind every reported number

**What this is.** The article states each measurement rule in the form needed to
read the result. This document states it in the form needed to *re-apply* it. Where
the two differ, this document governs, and the released script named against each
rule governs over both.

Nothing here is a later rationalization: each rule is the one the corresponding
script implements, and the script is in `scripts/`.

---

## 1. Environment specification: pinned, and portable

Both properties are decided by `scripts/19_env_pinning_audit.py`, not by reading.
A file the parser cannot interpret is recorded as `undetermined`, never as a failure.

**Pinned.** Every declared dependency carries an exact version:

- pip / `requirements.txt`: `==` or an exact archive reference (a wheel or sdist URL
  with a version in the filename, or a VCS reference at an immutable commit).
- conda / `environment.yml`: `=<version>` on every entry, including the Python entry.
- A single unversioned or range-versioned entry (`>=`, `~=`, `^`, a bare package
  name) fails the whole file. There is no partial credit: one loose entry is enough
  for the resolved environment to differ between builds.

**Portable.** The file contains none of:

- a developer-specific absolute path (`/home/<user>/…`, `C:/Users/<user>/…`);
- a local-file dependency source (`file://`, a relative path to a wheel on disk);
- a platform-locked wheel filename (`-cp37-cp37m-win_amd64.whl` and similar);
- a machine-specific conda `prefix:` or a local channel path.

so that the file resolves unchanged on a third machine.

**Why both, and why neither suffices.** A pinned but non-portable file names a
location that exists on one machine only. A portable but unpinned file resolves to
whatever the package index serves on the day of the build. Both failure modes were
observed here, and one of them is exactly how the single weight-shipping repository
in this set broke.

## 2. Run instructions

Decided by `scripts/20_run_instructions_audit.py`. A repository qualifies if its
README contains **either**:

- a recognizable install or run command inside a code context (a fenced block, an
  inline code span, a shell-prompt line, or an indented block): `pip install`,
  `conda env create`, `docker build|run|compose`, `make <target>`, `python <file>.py`,
  `streamlit run`, `uvicorn`, `flask run`, `npm run|install`, `bash|sh <file>.sh`;
- **or** a section heading of a usage type: Usage, Getting started, How to run,
  Quickstart, Installation, Running, Inference, Demo, Training.

Commands are matched **only inside code regions**, because matching them in running
prose produced false positives on ordinary English ("make more accurate", "make it
possible").

The rule is deliberately generous. It measures the *presence* of a command, not
whether the command is correct, complete or sufficient to reach inference. The
resulting proportion can therefore only overstate how well this literature documents
execution.

## 3. Signal aggregation, repository to study

A study carries a signal if **any** of its repositories carries it (disjunction).
This is the rule most favorable to the audited literature, and it is applied
identically to every signal, so no signal is advantaged over another.

Study-level (N=18, same-team variants grouped) is the primary level.
Repository-level (N=22) is a sensitivity view and is **not** corrected for
within-team clustering, so it assumes an independence that same-team variants
violate.

## 4. Harness entry rule

A repository entered the containerized harness if it declared an environment
specification **and** carried either retrievable trained weights or usable sample
data — the minimum for a build to be able to end in inference. The rule is checkable
against `transparency/repo-intake-table.csv`.

Two deviations are on record, in opposite directions, and both are reported in the
article rather than tidied away:

- `SimonZeng7108/Video-SwinUNet` **met** the rule and was **not** attempted. It was
  set aside at vetting on grounds not contained in the rule: unclear license,
  segmentation data described as ethically restricted and not shared, and an implied
  GPU requirement.
- `UofTNeurology/masa-open-source` **did not meet** the rule and **was** attempted,
  as a feasibility pilot run while the set was still being assembled.

This rule narrows a broader provision in `transparency/statistical-analysis-plan.md`
§6, which would have sent every included repository to re-execution. The narrowing
restricts attempts to the best-provisioned repositories, which strengthens rather
than weakens the best-case reading of a null result.

## 5. Verdict definitions

Each repository receives exactly one verdict.

| Verdict | Condition | Evidence type |
|---|---|---|
| **Re-executable** | Builds and runs unmodified and reproduces its documented output, zero code changes | observed |
| **Partial** | Runs and yields structurally consistent output only after documented minimal fixes, or yields incomplete output | observed |
| **Not-reproduced (build/run-failed)** | A build was attempted and observed to fail at the as-declared stage | observed |
| **Not-attemptable (inventory)** | No build was attempted, because retrievable weights are absent and inference could not be launched whatever the build did | inferred |

**The distinguishing feature is the attempt, not the artifact.** A repository that
was attempted takes the observed verdict even where the inventory would have
predicted the inferred one, and the two are never merged in any count.

**Not-reproduced does not require that repair was attempted.** In the one case
carrying this verdict, the build failed on a dependency pinned to a path on a
developer's own machine; a repair path is documented in
`re-execution/logs/C-repo-002-masa/verdict.md` and was not run, because absent
weights and data block inference independently of the environment. The log says so
rather than implying an effort that did not happen.

**Not-attemptable turns on weights, not on data.** Three studies receiving it do
share usable sample data. Data without weights still cannot produce inference, so
the weights criterion is the operative one.

## 6. Harness procedure

1. As-declared build and run attempt in a clean CPU container; captured output
   released per case under `re-execution/`.
2. Documented minimal fixes, each recorded against the fixed barrier taxonomy.
3. Inference on provided or sample data where present. **No retraining.**

Barriers are stratified into hardware-neutral and GPU-only, and only
hardware-neutral barriers ground the conclusion: a repository that cannot install
its dependencies or load its weights fails identically on a GPU.

Metric reproduction against each study's own reported figures was planned but proved
attemptable for essentially no study, because instrumental test data are almost never
shared. Re-execution here therefore means reproducing the artifact's own *documented
output*, not the study's *reported metric*.

## 7. Screening reliability

`scripts/11_screening_kappa.py` re-applies the pre-stated inclusion rule to every
screened record from both scripted channels (n=181), using only the repository name,
paper title and description, and blind to the recorded decisions.

The second rater is an algorithm, not a person, so this is not inter-rater
reliability in the usual sense. It measures how far recorded decisions can be
reproduced by a stated rule; a low value indicates judgment the rule does not
capture, not disagreement between readers.

Three properties of the result matter and are easy to misread:

- **κ is uninformative on both channels, for opposite reasons.** On the mining
  channel only four records fall in the positive class. On the GitHub channel the
  rule included all 18 records it screened, so its marginal is degenerate, chance
  agreement equals observed agreement by construction, and κ is identically 0.00 by
  design rather than by disagreement. `P_pos` is likewise mechanical on that channel
  and is not informative.
- **What carries information is rule-versus-record agreement**: 15 of 15 inclusions
  and 0 of 3 exclusions on GitHub; 4 of 6 inclusions and 157 of 157 exclusions on
  mining. The three GitHub exclusions are exactly the judgment calls on that channel.
- **Every κ here is in-sample.** The rule specification was revised after we observed
  the agreement it produced: an earlier version read the paper title alone, which
  GitHub does not return, and revising it raised κ on the mining channel from 0.49 to
  0.79. Both specifications are released. The values are expected to be optimistic.

Intervals: BCa bootstrap, 2,000 resamples, fixed seed, reported alongside the plain
percentile interval, because where the two diverge the divergence is itself
information about how unstable the estimate is.

## 8. Interval reporting

Wilson intervals throughout, as small-sample fragility bands rather than inferential
confidence statements. They indicate how few observations underlie each proportion,
do not capture selection bias from non-random discovery, and are not used to infer to
the whole dysphagia-AI literature.

**No interval is attached** where a proportion is a logical consequence of a
conjunction rather than a sample quantity, or where the denominator is a purposively
selected subset rather than a sample. Both cases occur here and both are marked in
the article.

## Open license

Read from the repository's own license metadata (`license.spdx_id`) by
`scripts/08_repo_intake.py`, and counted if it is an OSI-approved license or an
equivalent public-domain dedication. One of the three found is CC0-1.0, which permits
reuse but is not OSI-approved, so the criterion is "open" and not "OSI-approved". A
license granted only in prose is not detected, so the count understates.

## Trained weights

Recorded by `scripts/08_repo_intake.py` as two separate signals: weights committed
inside the repository, and weights retrievable from an external archive. Both are
carried in the released intake table, and `scripts/09_census_synthesis.py` reads them
from there. A link that was never resolved does not count as retrievable.

## Usable sample or test data

Decided by `scripts/23_sample_data_audit.py`. A repository carries usable sample or test
data if at least one file under a data-designating directory is non-empty and is neither
code nor documentation; the directory match is deliberately generous, so the count can
only overstate. `scripts/09_census_synthesis.py` cross-checks the intake table against
that measurement on every run and stops if the two disagree.

Note on a correction. Until August 2026 this signal was carried by a hand-coded literal
inside script 09, and it was wrong in both directions on five repositories: one shipping
several hundred image files was coded as having no data, and three whose data
directories hold only a loader or zero-byte placeholders were coded as having it. The
study-level count moved from 4/18 to 2/18. None of the repositories involved had been
pushed since its intake date, so the disagreement was in the coding and not in the
repositories. The correction, and the evidence for it, are in
`results/sample-data-audit.json`.

## Study-level aggregation

`scripts/09_census_synthesis.py` clusters repository variants on `study_id` and takes
the disjunction: a study carries a signal if any of its repositories carries it. That is
the reading most favourable to the audited literature. The same script writes
`transparency/included-studies.csv`, which lists all 18 studies with their repositories,
signals and verdicts.
