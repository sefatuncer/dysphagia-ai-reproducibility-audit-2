> **NOTE ON AUTHORSHIP OF THE CODING.** This file is the live coding record referenced by
> the manuscript. One procedural provision below is obsolete: it was written when the study
> still planned a methodologist/librarian third author as an independent co-coder and
> adjudicator. The study pivoted to two authors, so no methodologist coded or adjudicated
> anything. Coding responsibility was S.T. for the computational block and N.K.T. for the
> clinical block, and screening reliability was assessed instead by a released, blind,
> rule-based re-coding of every screened record. The coding definitions themselves are
> unchanged and were applied as written.

# Transparency rubric — CODEBOOK (exact value sets and decision rules)

**Purpose:** to make two independent coders assign the SAME code to every cell. This file extends `coding-guide.md` with exact value sets and decision rules, and adds the RS1–RS6 clinical block defined in `reference-standard-taxonomy-RS1-RS6.md`. The blank form is `transparency-rubric-template.csv`; calibration uses the κ computation in `03_analysis.py`.

**General rules:**
- Evidence: the article text plus the linked repository or supplement. Anything not stated is **`not_reported`** — never assume, and note that this differs from "no" and is reported separately.
- Record a **`check_date`** for every repository or DOI access, because these change over time.
- Every cell is a value plus, where needed, a free-text note in `notes`.

## A. Code and environment (computational axis, S.T.)
| Column | Permitted values | Decision rule |
|---|---|---|
| `code_stmt` | `explicit_url` / `on_request` / `none` / `not_reported` | Type of code-sharing statement. "On GitHub" plus a link counts as explicit_url |
| `repo_accessible` | `yes` / `no` / `na` | URL returns HTTP 200 and is not empty. `na` means no code |
| `license` | `osi_approved` / `present_nonstandard` / `none` / `not_reported` | LICENSE file or header, referenced against the OSI list |
| `readme_run_instructions` | `yes` / `partial` / `no` / `na` | Are there steps for running the code |
| `dependency_file` | `dockerfile` / `requirements` / `environment_yml` / `pyproject` / `multiple` / `none` | List all of them in `notes`; put the strongest one in the column |
| `versions_pinned` | `pinned` / `partial` / `none` / `na` | Are versions fixed **and mutually consistent**. A contradictory environment is partial |
| `random_seed` | `yes` / `no` / `not_reported` | Is a seed value stated |
| `compute_reported` | `gpu` / `cpu` / `both` / `none` | Hardware and runtime; record in `notes` whether CPU inference is feasible |
| `runnable_example` | `yes` / `no` | Is an example input with its expected output provided |

## B. Data and model
| Column | Permitted values | Decision rule |
|---|---|---|
| `data_availability` | `open` / `controlled` / `on_request` / `none` / `not_reported` | Add the public DOI or identifier in `notes` |
| `model_weights` | `yes` / `no` / `not_reported` | Counted when reachable through a persistent DOI (Zenodo or equivalent) |
| `model_card` | `yes` / `no` | Model card or datasheet |

## C. Evaluation (shared)
| Column | Permitted values | Decision rule |
|---|---|---|
| `external_validation` | `yes` / `no` / `not_reported` | Independent cohort or open data |
| `subject_wise_cv` | `yes` / `no` / `unclear` / `na` | LOSO or subject-wise splitting; a record-level split is no |
| `held_out_test` | `yes` / `no` / `unclear` | An untouched test set |
| `calibration_utility` | `yes` / `no` | Calibration or decision curve, beyond AUC |
| `uncertainty_reported` | `yes` / `no` | Confidence intervals or an appropriate test (DeLong or similar) |

## D. Clinical — reference-standard taxonomy (clinical axis, N.K.T. · RS1–RS6)
| Column | Permitted values | Decision rule |
|---|---|---|
| `rs1_refstandard_type` | `instrumental_gold` (VFSS/MBSS/FEES) / `clinical_exam` / `screening_surrogate` / `patient_reported` / `ai_derived` / `not_reported` | Source of the label |
| `rs2_surrogate_leakage` | `predicts_gold` / `predicts_surrogate` / `mismatch` / `unclear` | Does the model predict the gold standard or a proxy for it |
| `rs3_label_scale` | `pas` / `digest` / `fois` / `mbsimp` / `yale_residue` / `binary_aspiration` / `custom` / `not_reported`, plus `binarized:yes/no` | Ordinal scale, and whether it was reduced to binary |
| `rs4_label_reliability` | a κ or ICC value, or `not_reported`; plus `raters:N`; plus `blinded:yes/no`; plus `consensus/single/provided` | Rater reliability (the weak point) |
| `rs5_spectrum` | `etiology:{stroke/parkinson/hn_cancer/neurodegen/presbyphagia/mixed}` plus `healthy_pct:%` plus `sampling:{consecutive/convenience}` | Spectrum matrix |
| `rs6_clinical_applicability` | `setting:{inpatient/outpatient/tele}` plus `user:{slp/physician/automated}` plus free comment | Clinical meaning |

## E. Metadata and verdict
| Column | Value |
|---|---|
| `study_id`, `first_author`, `year`, `modality`, `task`, `repo_url`, `reference_standard`, `check_date` | free text or categorical |
| `rerun_verdict` | `re_executable` / `partial` / `not_reproduced` / `not_attemptable`, plus a barrier note |

## κ calibration protocol
*(This is the obsolete provision described in the note above: it presupposes a third independent coder, and no methodologist joined the study.)*
1. Once the included set is fixed after screening, select **8–10 studies at random** and have two independent coders code them separately.
2. Compute item-wise Cohen κ (`03_analysis.py`). Any item with **κ < 0.60** triggers a clarification of the codebook and re-calibration.
3. Clinical block (RS1–RS6): N.K.T. with the methodologist; technical block: S.T. with the methodologist, so that independence is genuine.
