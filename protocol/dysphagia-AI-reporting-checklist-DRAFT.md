# Dysphagia-AI Minimum Reporting & Reproducibility, Recommendation Set, v0.2 (empirically grounded)

> ⚠️ **Terminology.** This is a **recommendation set**, NOT a consensus *standard* and not a formal *checklist*: a formal standard would require a Delphi or consensus process, which this study did not run. The wording is identical to §2.8 of the article, and the words "standard" and "checklist" are avoided as overclaims.

**Purpose.** A domain-specific reporting/transparency **recommendation set** (not a consensus standard; no Delphi) for artificial-intelligence studies in dysphagia (diagnosis, screening, severity, rehabilitation monitoring). It is the constructive deliverable of Makale C, proposing how to fix irreproducibility rather than only measuring it.

**Derivation.** Built on TRIPOD+AI (prediction models), CLAIM (imaging AI), STARD (diagnostic accuracy), and open-science reproducibility guidance (FAIR, model cards, containerization), **specialized** with dysphagia-clinical items where generic checklists are silent.

**Empirically grounded (census N=18 studies / 22 repositories).** Items are no longer a-priori guesses: each ⭐ item is foregrounded because the audit found it **systematically violated**. The observed violation rates (right-most column, "Audit evidence") are the empirical justification and directly rank the recommendations, and the most-violated items are the core. This grounding in a real re-execution census is what distinguishes this recommendation set from a generic reproducibility checklist.

**How authors use it.** Complete as a submission supplement; each item = Reported (page/section) / Not applicable (justify) / Not reported.

---

## Part A, Reproducibility & Open Science  *(engineering axis)*

| # | Item | Why it matters | Report as |
|---|---|---|---|
| A1 ⭐ | **Source code publicly available** (persistent URL, not "on request") | "On request" ≈ unavailable; public code is the floor of reproducibility. **Audit:** even a resolvable URL is not enough, since one linked repository (ruaeh/Dysphagia-ML) was **empty** (a linked-but-empty case) | Repo URL + commit/tag |
| A2 ⭐ | **Open license on the code** (OSI-approved) | No license means all-rights-reserved and legally unreusable. **Audit: absent in 15/18 studies (83%)** | License name |
| A3 ⭐ | **Dependency/environment specification** (requirements.txt / environment.yml / **Dockerfile**) with **pinned versions** | Unpinned/inconsistent deps make the environment unbuildable. **Audit: absent in 12/18; and where present, typically unpinned, the decisive failure in *both* re-executed cases** (VFSS: mutually-unsatisfiable deps; enoch0307: an unpinned `scikit-learn` made a shipped model unloadable, `ModuleNotFoundError: _loss`, fixed only by pinning to the training version) | File(s) + pinned? |
| A4 | **Random seeds fixed and reported** | Non-determinism blocks exact reproduction | Seed value(s) |
| A5 ⭐ | **Data availability statement** with access route (open / controlled / justified-restricted) | VFSS/FEES are privacy-sensitive, so state the route honestly rather than omit it. **Audit: usable sample data in only 4/18 (22%)** | Route + identifier/DUA |
| A6 ⭐ | **Trained model weights archived** (persistent DOI, e.g., Zenodo) | Lets others run inference without retraining, the single biggest re-execution barrier. **Audit: weights available anywhere in only 2/18 (11%); in-repo in 1/18** | Archive DOI |
| A7 | **Model card / datasheet** (intended use, training data, limitations) | Communicates scope + failure modes | Present? |
| A8 | **Compute/hardware reported** (GPU/CPU, time) + **CPU-inference feasible or documented** | Reproducibility shouldn't require the authors' exact GPU | Hardware + feasibility |
| A9 | **A runnable minimal example** (sample input + expected output) | Enables verification without private data (pilot repo did this well, a good practice) | Sample provided? |

## Part B, Clinical validity & dysphagia-specific reporting  *(clinical axis)*

| # | Item | Why it matters | Report as |
|---|---|---|---|
| B1 ⭐ | **Reference standard specified + justified** (instrumental VFSS/FEES gold standard vs clinical/screening surrogate) | A model validated only against a weak surrogate can't claim diagnostic validity. **Audit: reference standards heterogeneous and often surrogate: several models predict a downstream proxy (voice to bedside-screen, voice to clinical outcome, features to a VFSS label) rather than the instrumental gold standard (RS2) | Standard + rationale |
| B2 ⭐ | **Reference-label rater reliability** (inter-/intra-rater κ/ICC; # raters; blinding) | Noisy labels cap achievable performance and hide bias. **Audit: quantitative rater reliability reported in ~0/18**, and even studies acknowledging VFSS's poor inter-rater reliability did not quantify their own labels (corroborated by Kwok 2025, where 75% did not report sampling or blinding) | κ/ICC + raters |
| B3 ⭐ | **Patient spectrum & selection** (etiology: stroke / H&N cancer / neurodegenerative / mixed; severity range; healthy-vs-patient; consecutive vs convenience) | Spectrum bias inflates accuracy; healthy-only cohorts do not reflect clinical use | Cohort description |
| B4 | **Bolus/task standardization** (IDDSI consistency levels, volumes, protocol) | Input variability confounds model claims | Protocol details |
| B5 | **Modality-specific acquisition.** VFSS: frame rate, ROI, radiation; FEES: scope/protocol; acoustic: mic, environment/SNR; sEMG: electrode placement/montage; HRM: catheter | Acquisition drives generalizability | Per-modality params |
| B6 ⭐ | **Clinical outcome definition** (e.g., PAS/aspiration, penetration, safe/unsafe swallow, severity scale), explicit and clinically meaningful | Ambiguous targets prevent comparison and clinical use | Outcome + scale |
| B7 ⭐ | **Honest intended-use statement** (screening vs diagnosis vs monitoring; NOT "deployment-ready" unless externally validated) | Overclaiming clinical readiness is the top reviewer complaint | Intended-use sentence |

## Part C, Evaluation rigor  *(shared)*

| # | Item | Why it matters | Report as |
|---|---|---|---|
| C1 ⭐ | **External / independent validation** (second cohort or open dataset) | Single-cohort AUC ≠ generalisable; #1 separator of accept/reject | Cohort or "none" |
| C2 ⭐ | **Subject-wise (leave-one-subject-out) cross-validation**, no record-level leakage | Frame/record-level splits leak and inflate metrics (auto-reject in biosignal) | Split scheme |
| C3 | **Held-out test set** untouched during development | Prevents optimistic bias | Present? |
| C4 | **Calibration + clinical utility** (calibration curve, decision-curve/net-benefit), not AUC alone | AUC ignores clinical decision value | Metrics reported |
| C5 | **Uncertainty** (CIs; appropriate tests, e.g., DeLong) | Point estimates overstate certainty | CIs/tests |
| C6 | **Strong baselines + ablation** (clinical score + well-tuned classical ML) | Guards against "deep-learning-for-its-own-sake" | Baselines |

---

*Grounded in Makale C's re-execution census (N=18 studies). The three most-violated items are trained weights (2/18), open license (3/18), and pinned environment (both re-executed cases failed on it); these form the recommendation set's core. On the clinical side, rater-reliability reporting (~0/18) is the analogous gap. The dual structure (Part A engineering × Part B clinical) is the two-author contribution: it is what a generic radiology-AI reproducibility checklist cannot provide for the dysphagia domain. It is a domain-specific reporting recommendation set, not a consensus standard (no Delphi), and authors self-complete it as a submission supplement.*
