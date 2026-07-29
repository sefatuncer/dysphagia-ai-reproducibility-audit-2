> ⚠️ **PLANNED UNDER THE PRE-PIVOT DESIGN, NOT EXECUTED AS DESCRIBED.**
> This file belongs to the study's earlier systematic-review-style design, which assumed
> dual independent human screening, a methodologist/librarian third author, PRESS review,
> and institutional database access. **The study pivoted to a two-author meta-research
> re-execution census with an objective, machine-checkable inclusion criterion.** None of
> the methodologist-dependent procedures below were carried out. What was actually done is
> reported in the manuscript, and screening reliability was instead assessed by a released,
> blind, rule-based re-coding of every screened record. This file is retained as design
> history so the change of plan is auditable, not concealed.

# Screening form — title/abstract and full text (dual independent screening)

Two screeners (N.K.T. through the clinical lens, S.T. through the open-science and technical lens) apply this form **independently**, followed by **Cohen κ**, then consensus or a third adjudicator. Records are loaded into Rayyan or Covidence, and each is marked **include / exclude / unclear (→ full text)**.

## INCLUDE (all must hold)
1. A **primary study** — not a review, editorial, commentary, protocol or abstract-only record.
2. It describes an **AI, machine-learning or deep-learning model** (development or validation).
3. It applies that model to the diagnosis, screening, assessment, severity classification or rehabilitation monitoring of **dysphagia or swallowing**.
4. Any **modality** (VFSS · FEES · acoustic or cervical auscultation · sEMG · HRM · wearable or IMU · clinical tabular data).

## EXCLUDE (any one is sufficient — record the code)
- **E1** — no AI, machine learning or deep learning.
- **E2** — review, systematic review, editorial, commentary, protocol, or conference abstract only (no full text).
- **E3** — does not describe a computational model.
- **E4** — **oesophageal motility only**, unrelated to oropharyngeal swallowing.
- **E5** — a **duplicate** report of the same model or cohort (keep the most complete version).
- **E6** — language: **not English with extractable full text** (the canonical criterion, locked in the record and identical to §2.2 of the article).

## Borderline cases (clarified for κ consistency)
- **Cancer and radiotherapy:** *prediction of post-radiotherapy dysphagia* (modelling a dysphagia outcome) → **INCLUDE**. *Radiotherapy dose or treatment planning* that is not dysphagia AI → **EXCLUDE as E3/E4**. The `likely_cancer_rt` flag in `combined-corpus.csv` marks where this decision is needed.
- **Swallow detection or counting in healthy participants only** → **INCLUDE** (assessment AI); add the note `spectrum=healthy-only`.
- **Bibliometric, scoping or benchmark papers** → **EXCLUDE as E2** (not primary).
- Records carrying the **`likely_review` flag** (n ≈ 195) → rapid E2 screen.

## Decision flow
Title and abstract → {include, exclude (code), unclear} → unclear records go to full text → final decision at full text (include, or exclude with a code). Flow counts are recorded at every stage.
