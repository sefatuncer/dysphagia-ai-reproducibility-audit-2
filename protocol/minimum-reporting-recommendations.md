# Minimum-reporting RECOMMENDATION SET for dysphagia AI — v1.0 (final)

> ⚠️ **This is a set of RECOMMENDATIONS, not a "standard" or a "checklist".** A formal standard would require a Delphi or consensus process, which this study did not run. Calling it a checklist or a standard would be an overclaim, so it is presented as recommendations throughout.
>
> **Status: final for v1.1.0 of this archive.** The ordering was fixed against the completed audit, foregrounding the items violated most often. The observed frequency behind that ordering is given below and matches Table 6 of the article.

## Core items, ordered by how often the audit found them missing

| Item | Observed in this audit | Scale |
|---|---|---|
| Pinned **and** portable environment specification | **0/18** | study level, N=18 |
| Trained weights retrievable | **2/18** | study level, N=18 |
| Open (OSI-approved) license | **3/18** | study level, N=18 |
| Usable sample or test data | **4/18** | study level, N=18 |
| Run instructions | **7/18** | study level, N=18 |
| Rater reliability reported (RS4) | **0/4 applicable** (0/6 counting all) | full-text subset, k=6 |
| Reference standard stated and justified (RS1, RS2) | heterogeneous; no study reported a single instrumental standard with justification | full-text subset, k=6 |
| External validation | **not measured in this audit** | — |

The first five are the packaging items and are measured for every included study. The
two clinical items were assessable only where full text could be retrieved. External
validation is retained because it is standard in this literature's appraisal, but
this audit did not measure it and the row says so rather than implying a frequency.

**Purpose.** The **constructive output** of the study: not only to measure irreproducibility but to propose a remedy. These are field-specific reporting and transparency recommendations for dysphagia-AI studies.

**Derivation and anchoring.** Every item is **explicitly anchored** to an existing guideline (TRIPOD+AI, CLAIM, STARD, QUADAS-2, FAIR, model cards). The dysphagia-specific items sit exactly where the generic guidelines are **silent**, and that is where the contribution lies. The anchor is given for every item.

**Two-part structure:** Part A (engineering and open science, S.T.) × Part B (clinical and dysphagia-specific, N.K.T., derived from RS1–RS6 in `reference-standard-taxonomy-RS1-RS6.md`) × Part C (evaluation, shared). This pairing is what a generic radiology-AI checklist cannot supply for dysphagia.

**Use:** as an author self-audit at submission, extending the data-availability statement many journals already require. Each item is marked Reported (page or section) / Not applicable (with a reason) / Not reported. It is deliberately not framed as a supplementary file to be filed and forgotten; the point is that the author checks before submitting, and that a reader can check the same items afterwards from the archive.

---

## Part A — Reproducibility and open science (engineering axis, S.T.)
| # | Item | Anchor | Why (evidence from the pilots) |
|---|---|---|---|
| A1 ⭐ | **Source code publicly available** at a persistent URL, not "on request" | TRIPOD+AI 20; FAIR | "On request" is equivalent to unavailable |
| A2 ⭐ | **An open license on the code** (OSI-approved) | FAIR; a dysphagia-specific gap | Without a license the code cannot be legally reused (the pilot had none) |
| A3 ⭐ | **An environment or dependency file with PINNED versions** (requirements / environment.yml / **Dockerfile**) | TRIPOD+AI; dysphagia-specific | In the pilot the declared dependencies **could not be resolved against each other** |
| A4 | **A fixed random seed, reported** | TRIPOD+AI | Non-determinism defeats exact reproduction |
| A5 ⭐ | **A data-access statement and route** (open / controlled / restricted with a reason) | STARD; TRIPOD+AI | VFSS and FEES data are confidential; state the route honestly rather than omitting it |
| A6 | **Trained weights archived** under a persistent DOI (Zenodo) | FAIR | Inference without retraining |
| A7 | **A model card or datasheet** (intended use, training data, limits) | Model Cards (Mitchell 2019) | Scope and failure modes |
| A8 | **Compute and hardware reported, with CPU inference feasible or documented** | dysphagia-specific (our Layer B) | Reproduction should not require the authors' exact GPU |
| A9 | **A working minimal example** (sample input plus expected output) | dysphagia-specific good practice | Verification without confidential data (the pilot did this well) |

## Part B — Clinical validity, dysphagia-specific (clinical axis, N.K.T., RS1–RS6)
| # | Item | Anchor | Taxonomy |
|---|---|---|---|
| B1 ⭐ | **State and justify the reference standard** (instrumental VFSS/FEES against a clinical or screening proxy) | STARD; QUADAS-2 domain 3 | RS1 |
| B2 ⭐ | **Rater reliability of the reference label** (κ or ICC; number of raters; blinding) | **beyond QUADAS-2**, which does not ask | RS4 |
| B3 ⭐ | **Patient spectrum and selection** (aetiology; severity; healthy against patient; consecutive against convenience) | QUADAS-2 domain 1; **the matrix is dysphagia-specific** | RS5 |
| B4 | **A proxy-leakage statement** (does the model predict the gold standard or a proxy for it) | **beyond QUADAS-2** | RS2 |
| B5 | **Label scale and granularity** (PAS/DIGEST/FOIS; the loss incurred by reducing to binary) | **dysphagia-specific** | RS3 |
| B6 | **Bolus and task standardization** (IDDSI consistency, volume, protocol) | dysphagia-specific | — |
| B7 | **Modality-specific acquisition** (VFSS: frame rate, ROI, dose; FEES: scope; acoustic: microphone, SNR; sEMG: electrodes; HRM: catheter) | CLAIM (imaging), extended for dysphagia | — |
| B8 ⭐ | **A clinical outcome definition** (PAS, aspiration, penetration, severity — explicit and clinically meaningful) | STARD; TRIPOD+AI | RS6 |
| B9 ⭐ | **An honest statement of intended use** (screening, diagnosis, monitoring; do not claim deployment-readiness without external validation) | TRIPOD+AI | RS6 |

## Part C — Evaluation rigour (shared)
| # | Item | Anchor | Why |
|---|---|---|---|
| C1 ⭐ | **External or independent validation** (a second cohort or open data) | TRIPOD+AI; STARD | A single-cohort AUC does not generalize; this is the leading acceptance discriminator (Kwok reports 0/24) |
| C2 ⭐ | **Subject-wise (LOSO) cross-validation**, with no record-level leakage | dysphagia and biosignal specific | Frame- or record-level splitting leaks and inflates the metric |
| C3 | **An untouched, separate test set** | TRIPOD+AI | Prevents optimistic bias |
| C4 | **Calibration and clinical utility** (calibration curve, decision curve, net benefit) | TRIPOD+AI | AUC ignores clinical decision value |
| C5 | **Uncertainty** (intervals; appropriate tests such as DeLong) | TRIPOD+AI | A point estimate overstates precision |
| C6 | **A strong baseline plus ablation** (a clinical score and a well-tuned classical ML model) | dysphagia-specific good practice | Guards against deep learning for its own sake |

---
*Final for v1.1.0. The core ordering is fixed against the completed audit and is given at the top of this document with the observed frequency behind each item. The anchors are given for reviewer confidence. There was no Delphi process, so these are recommendations rather than a standard, and they should be read as a proposal open to criticism.*
