> **NOTE ON AUTHORSHIP OF THE CODING.** This file is the live coding record referenced by
> the manuscript. One procedural provision below is obsolete: it was written when the study
> still planned a methodologist/librarian third author as an independent co-coder and
> adjudicator. The study pivoted to two authors, so no methodologist coded or adjudicated
> anything. Coding responsibility was S.T. for the computational block and N.K.T. for the
> clinical block, and screening reliability was assessed instead by a released, blind,
> rule-based re-coding of every screened record. The coding definitions themselves are
> unchanged and were applied as written.

# Transparency rubric — coding guide (written for two independent coders)

**Purpose:** to make two coders assign the **same** code to every item of `transparency-rubric.csv`, and so to achieve high inter-rater agreement (κ). General rule: look for evidence in the **article text plus the linked repository or supplement**; if something is not stated, code it **"not reported"** rather than assuming. Record the **access date** for every repository or DOI, because these change over time. Pilot **repository #1 (VFSS_analysis)** is coded jointly for calibration, and its values are given below as the worked example.

## Code and environment (computational axis, S.T.)
| Item | How it is coded (categories) | Example: repository #1 |
|---|---|---|
| `code_stmt` | Mention of code sharing: **explicit-URL / on-request / none** | explicit-URL |
| `repo_accessible` | Does the URL work (HTTP 200, not empty)? **yes/no** plus access date | yes (2026-07-13) |
| `license` | LICENSE in the repository: **OSI-approved / present-nonstandard / NONE** | **NONE** |
| `readme_run_instructions` | Instructions for running: **yes / partial / no** | yes |
| `dependency_file` | **requirements / environment.yml / Dockerfile / pyproject / none** (list all) | environment.yml plus setup.py |
| `versions_pinned` | Versions fixed **and mutually consistent**: **pinned / partial / none** | **partial** (torch unpinned; the environment is internally inconsistent) |
| `random_seed` | Is a seed stated: **yes / no / na** | not stated |
| `compute_reported` | Hardware and runtime (GPU/CPU): **yes / no** | GPU implied (nvidia-cu12); CPU undocumented |

## Data and model
| Item | Categories | Repository #1 |
|---|---|---|
| `data_availability` | **open / controlled / on-request / none** plus a public identifier | sample only; the full data are private |
| `model_weights` | Are weights shared under a persistent DOI: **yes / no** | yes (Zenodo, CC-BY) |
| `model_card` | Model card or datasheet: **yes / no** | no |

## Validation
| Item | Categories |
|---|---|
| `external_validation` | Independent cohort or open data: **yes / no** |
| (additional) `subject_wise_cv` | LOSO or subject-wise: **yes / no / unclear** |

## Clinical (clinical axis, N.K.T.)
| Item | Categories |
|---|---|
| `reference_standard` | **VFSS/FEES instrumental (gold) / clinical / screening-surrogate** plus a validity note |
| (additional) `rater_reliability` | κ or ICC for the reference label, with the number of raters and the blinding procedure: value or not reported |
| (additional) `spectrum` | Aetiology (stroke / head-and-neck cancer / neurodegenerative / mixed) plus healthy against patient composition plus consecutive against convenience sampling |

## Re-run (Layer B — the code-available subset)
| Item | Categories |
|---|---|
| `rerun_verdict` | **fully / partial / not-reproduced / not-attemptable** plus a barrier note (missing data / GPU only / missing weights / dependency conflict) |

**Disagreement resolution:** the two coders code independently, **Cohen κ** is reported, and disagreements are settled by consensus or, failing that, by a third adjudicator (the methodologist). *(This last provision is the obsolete one described in the note above: no methodologist joined the study.)* Every uncertain cell is coded "not reported" with a free-text note.
