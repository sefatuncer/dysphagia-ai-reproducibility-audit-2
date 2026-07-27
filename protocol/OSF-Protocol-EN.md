> ⚠️ **SUPERSEDED (pre-pivot v1).** This is the OLD systematic-review protocol (PRISMA-ScR, dual screening, κ, methodologist as 3rd author, IJMI-primary, 34% numeric comparison). The study pivoted to a re-execution census; the CURRENT registration form is **`OSF-kayit-formu.md` (v2)**, and it is what should be posted on OSF. This file is kept only as design history. Do **not** register or submit from it. (Not AI-trace-cleaned for this reason.)

---

# OSF Registration Protocol (Draft, EN) — v1 / SUPERSEDED

**Working title:** Open science, code and data availability, and computational reproducibility in dysphagia artificial-intelligence research: a meta-research systematic review with containerized re-execution

**Registry:** Open Science Framework (OSF Registries). *Note: PROSPERO does not accept scoping or meta-research reviews; OSF is used.*
**Reporting guideline:** PRISMA 2020 and PRISMA-ScR (adapted for a meta-research review).
**Version:** Draft v0.1 (13 Jul 2026) — to be finalized and made public before screening begins.

**Authors (proposed):** Sefa Tunçer, PhD (co-first; reproducibility / software axis) · Nazife Kapan Tunçer, MD (co-first; clinical validity axis) · [Methodologist / health-sciences librarian — to be confirmed, 3rd author].
**Contributions (CRediT):** Conceptualization — S.T. (reproducibility), N.K.T. (clinical); Methodology — all; Software / containerization — S.T.; Data curation / charting — S.T., N.K.T.; Formal analysis — S.T.; Clinical appraisal / validation — N.K.T.; Writing — all.

> **[DECISIONS — LOCKED 13 Jul 2026]**
> 1. **Language scope:** English-language studies with extractable full text (single canonical criterion; identical in manuscript §2.2 and the screening form). ✅
> 2. **Time window:** 2010–2026. ✅
> 3. **Reproduction tolerance (Layer B) — by output type:** classification metrics within ±5 percentage points OR the reported 95% CI; continuous outputs within relative ±5% OR the reported measurement error; if no reference metric/CI/sample data are shared → "metric reproduction not attemptable" (no imputation). Priority is always re-executability. ✅
> 4. **Methodologist / health-sciences librarian as 3rd author:** YES (PRESS search review + κ adjudication). ✅
> 5. **LLM-assisted screener:** NOT in the primary protocol; may be reconsidered as an optional supplement after main findings. ✅

---

## 1. Background and rationale

Artificial-intelligence (AI) research in dysphagia (swallowing disorders) is expanding rapidly (~633 records in a 2025 bibliometric mapping; ~60 studies in a 2025 diagnosis/assessment scoping review). However, the **transparency and reproducibility** of this literature have not been examined:

- Kwok/Wong et al. (JMIR 2025;27:e65551) appraised 24 dysphagia-screening AI studies with QUADAS-2 (plus a model domain) and TRIPOD+AI, reporting that **no study performed external validation**. That review assessed *methodological quality and risk of bias only* — code availability, data-sharing statements, model cards, environment specification, and computational reproducibility were **not examined**.
- A 61-study scoping review of AI in dysphagia diagnosis/management (CODAS 2025) organizes the field by algorithm and modality but does **not** mention code sharing, data sharing, open-source availability, model cards, or reproducibility.
- In adjacent fields, code-sharing has been quantified (radiology AI: source-code availability 34% [73/218], Venkatesh et al. 2022; model availability in radiology ~39.9%, Lee et al. 2025), but **no equivalent figure exists for dysphagia AI.** (An earlier unsourced "~11.5%" figure was removed after verification — see manuscript reference notes.)

**Gap.** No study has audited the open-science practices (code/data/model availability, reporting-standard adherence) or the **actual computational reproducibility** of dysphagia-AI research. This review measures both, and proposes a dysphagia-AI minimum reporting/transparency set. Because it uses only published articles and public repositories, no ethics approval is required.

## 2. Objectives and review questions

**Objective:** To map and quantify the transparency, open-science compliance, and computational reproducibility of AI studies in dysphagia diagnosis, assessment, severity classification, and rehabilitation monitoring, and to attempt containerized re-execution of the code-available subset.

- **RQ1.** What proportion of eligible studies provide (a) source code, (b) a data-availability statement / accessible data, (c) trained model weights, (d) an environment/dependency specification, (e) a model card/datasheet, and (f) an open license?
- **RQ2.** To what extent do studies comply with the open-science/reproducibility items of TRIPOD+AI (and CLAIM for imaging studies)?
- **RQ3.** Among studies with public code, how many can be **re-executed** in a clean containerized (CPU) environment (i.e., the artifact installs, runs, and produces its own documented output)? *Secondarily, only where sample/reference data are shared:* how many reproduce the reported primary metric within a predefined tolerance? *(Most studies' test cohorts are private → metric reproduction is structurally limited; this is itself a finding.)*
- **RQ4 (clinical).** What reference standards (e.g., VFSS/FEES vs clinical/screening surrogates) and patient-selection characteristics underlie these models, and how do reference-standard validity and spectrum bias affect the clinical interpretability of reproducibility?

## 3. Eligibility criteria (PCC)

- **Population / dataset context:** human swallowing/dysphagia data (any age; healthy and/or patient populations).
- **Concept:** development, validation, or application of an AI/ML/DL model for dysphagia/swallowing **diagnosis, screening, assessment, severity classification, or rehabilitation monitoring**, using any modality (VFSS, FEES, acoustic/cervical auscultation, surface EMG, high-resolution manometry, wearable/IMU, or clinical/tabular data).
- **Context:** any clinical or laboratory setting; peer-reviewed primary research.

**Include:** peer-reviewed primary studies meeting the Concept above.
**Exclude:** non-AI studies; reviews, editorials, commentaries, protocols; conference abstracts without a full text; studies that do not describe a computational model; esophageal-motility-only studies unrelated to oropharyngeal swallowing; duplicate reports of the same model/cohort (keep the most complete).
**Time window:** 2010–2026. **Language:** English-language studies with extractable full text (canonical criterion; identical in manuscript §2.2 and screening form).

## 4. Information sources

PubMed/MEDLINE, Scopus (Embase-indexed), Web of Science Core Collection, IEEE Xplore, ACM Digital Library; grey literature via Google Scholar (first 200 records). **Backward citation screening** of Kwok e65551 (n=24), the CODAS scoping review (n=61), and the 2025 bibliometric set (n=633). Search dates and hit counts will be recorded per source.

## 5. Search strategy (example — to be finalized with a librarian, PRESS-reviewed)

**PubMed (title/abstract + MeSH):**
```
("Deglutition Disorders"[Mesh] OR dysphagia[tiab] OR deglutition[tiab] OR swallow*[tiab])
AND
("Artificial Intelligence"[Mesh] OR "artificial intelligence"[tiab] OR "machine learning"[tiab]
 OR "deep learning"[tiab] OR "neural network*"[tiab] OR convolutional[tiab] OR transformer*[tiab]
 OR "random forest"[tiab] OR "support vector"[tiab] OR radiomics[tiab]
 OR "computer-aided"[tiab] OR "computer aided"[tiab])
```
**Scopus / IEEE Xplore:** analogous `TITLE-ABS-KEY` translation of the two concept blocks. No methodological filter is applied (to maximize sensitivity for a transparency audit).

## 6. Study selection

Records imported to Rayyan/Covidence, deduplicated. **Two independent reviewers** (N.K.T. clinical lens, S.T. technical lens) screen title/abstract then full text; **Cohen's κ** reported at each stage; disagreements resolved by consensus or a third reviewer. A **PRISMA 2020 flow diagram** documents the process.

## 7. Optional: LLM-assisted screening (NOT in primary protocol; optional supplement only)
If adopted later, a fixed-version large language model is used as a **third, independent** screener at the title/abstract stage. The exact model version, full prompts, temperature, and run date will be published in the supplement; AI-vs-human agreement (κ) is reported as a secondary methodological finding. **This does not replace dual human screening**, and the LLM's non-determinism is documented — consistent with the review's own transparency thesis.

## 8. Data charting — Transparency Rubric (core)

Each included study is coded on the following items (operational definitions in brackets). Kappa on a 20% double-charted sample.

| Domain | Item (coding) |
|---|---|
| **Bibliographic/clinical** | author, year, country, modality, task, model type, sample size, primary metric |
| **Code availability** | code statement present (yes/no) · URL given (yes/no) · repo accessible = HTTP 200 & non-empty at check date (yes/no; record date) · license (OSI-approved / present-nonstandard / none) · README with run instructions (yes/no) · dependency file (requirements.txt / environment.yml / Dockerfile / pyproject / none) · versions pinned (yes/no) · random seed reported (yes/no) |
| **Data availability** | data statement present (yes/no) · data status (open / controlled-access / on-request / none) · public identifier/DOI (yes/no) |
| **Model artifacts** | trained weights shared (yes/no) · model card/datasheet present (yes/no) |
| **Reporting adherence** | TRIPOD+AI open-science items (item-by-item) · CLAIM items (imaging studies) |
| **Validation** | internal only / external validation (independent cohort) · subject-wise (LOSO) CV (yes/no/unclear) · held-out test set (yes/no) |
| **Compute** | hardware/compute reported (yes/no) |
| **Clinical appraisal (N.K.T.)** | reference standard (VFSS/FEES instrumental gold standard / clinical / screening surrogate) · patient selection (consecutive-representative / case-control / convenience) · spectrum bias risk (low/some/high) · clinical applicability note |

Proportions reported with **95% Wilson CIs**, stratified by modality and publication year; compared to the radiology benchmark (34%).

## 9. Layer B — Containerized computational reproducibility

**Eligible subset (census — no subjective gate):** every included study with a public, resolvable code repository enters re-execution. There is no "apparently runnable" pre-filter — studies that fail to build still yield informative *not-attemptable* verdicts, and this avoids selection bias toward easy-to-run repositories. The two pre-registration feasibility pilots are reported separately from the primary corpus-wide count.
**Procedure (on 32 GB RAM / 16-core / Docker Desktop, CPU):**
1. Build a Docker image pinning declared dependencies.
2. Run **inference/evaluation** on provided or sample data (not re-training).
3. **First, re-executability:** does the artifact install, run, and emit its own documented output? *Then, only where sample/reference data exist:* attempt to reproduce the reported **primary metric** within the predefined tolerance.
4. Log all steps, Dockerfiles, and barriers; publish them in `analiz/rerun-loglari/`.

**Reproduction outcome rubric:**
- *Not attemptable* — no public code.
- *Build/run failure* — code present, environment not reconstructable.
- *Runs, not reproduced* — runs but primary metric outside tolerance.
- *Partially reproducible* — some reported results reproduced.
- *Fully reproducible* — primary metric within tolerance (**absolute ≤5 pp OR within reported 95% CI**).

**Scope limit:** CPU inference only; GPU-scale re-training is out of scope and recorded as a barrier. **Pilot:** `BSEL-UC3M/VFSS_analysis` (nnU-Net; Zenodo-archived weights) — verify license and CPU-inference feasibility first.

## 10. Data synthesis
Descriptive quantitative synthesis (proportions + 95% CIs), stratified by modality and year; narrative synthesis of reproducibility barriers; comparison with adjacent fields. **Primary output:** a proposed **minimum reporting and transparency checklist for dysphagia-AI studies.**

## 11. Ethics
Only published articles and public repositories are analyzed; no human participants or new data. No ethics approval required. A single-line institutional exemption note will be obtained where a target journal requests one.

## 12. Dissemination
Target journals: **International Journal of Medical Informatics (Q1, primary)**, with **JAMIA** or **Journal of Biomedical Informatics** as strong Q1 alternatives — all fee-free via the traditional (subscription) route; OA only if a TÜBİTAK Read&Publish quota applies (bonus, not assumed). **Dysphagia is NOT a primary target** — a clinical journal whose readership/reviewer pool does not fit a containerized-re-execution meta-research (genre mismatch → desk-reject risk); it is at most a conditional fallback if the manuscript is heavily reframed around the clinical axis. A **preprint (medRxiv or arXiv cs.CY/q-bio) is posted immediately before submission**, after confirming the target journal's preprint policy.

## 13. Amendments
Any deviation from this protocol will be documented with date and rationale as an OSF amendment and reported in the manuscript.

---

*Derived from `../Protokol.md`. Finalize the five [DECISIONS] above, then register on OSF and make public before screening.*
