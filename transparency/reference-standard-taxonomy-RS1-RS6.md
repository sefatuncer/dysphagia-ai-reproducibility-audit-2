# Clinical reproducibility construct and a dysphagia-specific reference-standard and label-quality taxonomy (RS1–RS6)

**Status:** the taxonomy design and the clinical judgements are the work of N.K.T. (clinical axis). Rows marked `[NKT]` in the accompanying coding table are clinical judgements; rows marked `inventory-only` could not be coded because the full text was not retrieved through the study's channels, which is a finding rather than an outstanding task. The clinical judgements were checked against the source publications on 21-22 August 2026, four were corrected, and the corrected set was reviewed and accepted by the clinician author on 22 August 2026.
**Purpose:** reference-standard validity and spectrum bias, taken alone, are already covered by QUADAS-2 and were applied to this literature by Kwok and Wong (JMIR 2025). This document defines a clinical construct that goes **beyond** QUADAS-2 and is **specific to dysphagia AI**: it enters the audit as a coding block in the rubric, as the clinical anchor of the article's thesis, and as the clinical half of the minimum-reporting recommendations.

---

## 1. Why QUADAS-2 is not sufficient (rationale for the construct)

QUADAS-2 is generic. It passes over the reference-standard domain with a three-level risk judgement (low / high / unclear) and asks whether the reference standard correctly classifies the target condition. It does not interrogate the failure modes that actually matter in dysphagia AI:

- In swallowing assessment **even the gold standard is noisy** — inter-rater reliability of VFSS and FEES scoring is known to be no better than moderate — and QUADAS-2 does not quantify this.
- **Collapsing ordinal scales** (8-point PAS, DIGEST, FOIS) **into binary labels** loses information and shifts the target; QUADAS-2 does not see it.
- **Spectrum contamination** between healthy-volunteer swallows and clinical dysphagia is treated only coarsely in QUADAS-2 domain 1.
- **Proxy leakage** — a model predicting an EAT-10 or bedside proxy rather than the instrumental gold standard — falls outside QUADAS-2 entirely.

**Thesis extension (the clinical anchor of the article):** *containerized re-executability is necessary but not sufficient. Clinical reproducibility additionally requires **label provenance** and **spectrum representativeness**: a model that re-runs perfectly is not clinically reproducible if it rests on weak or unreported labels.*

---

## 2. The taxonomy — coding block (clinical columns added to the rubric)

Coded for every included study, as categories plus a free-text note. The anchor guideline is given, together with the point at which the item goes beyond it.

| # | Item | Categories | Anchor and extension |
|---|---|---|---|
| **RS1** | **Reference-standard type** | instrumental reference (VFSS/MBSS, FEES) / clinical examination (bedside, 3-oz) / screening proxy (EAT-10, GUSS, Yale) / patient-reported / derived from another AI | STARD-compatible; a dysphagia-specific catalogue |
| **RS2** | **Target validity and proxy leakage** | does the model predict the instrumental gold standard or a **proxy** for it? is the label the same construct as the target? | **beyond QUADAS-2** — proxy leakage has no place in the generic tool |
| **RS3** | **Label scale and granularity** | PAS(8) / DIGEST / FOIS / MBSImP / Yale Pharyngeal Residue / binary aspiration / bespoke; **is it reduced to binary** (information loss) | **beyond QUADAS-2** — loss of ordinal granularity |
| **RS4** | **Label reliability** (the weak point) | is rater κ or ICC reported · number of raters · blinding · consensus vs single rater vs supplied annotation | **beyond QUADAS-2** — this is exactly where the low reliability of swallowing scoring sits |
| **RS5** | **Spectrum matrix** | aetiology (stroke / Parkinson / head-and-neck cancer / presbyphagia / mixed) × severity distribution × **healthy-control contamination** (proportion of healthy volunteers) × sampling (consecutive vs convenience) | **beyond QUADAS-2** — a multi-dimensional matrix with clinical meaning |
| **RS6** | **Clinical applicability** | deployment setting (inpatient / outpatient / telehealth) · user (SLP / physician / automated) · decision point; interpretation of what reproducibility means clinically | TRIPOD+AI clinical-utility framing |

---

### Mapping onto the established appraisal instruments

The applicable instrument depends on what a study predicts, so the taxonomy maps onto two
different tools rather than one. This is the mapping the article refers to.

| Target of the study | Applicable instrument | Items of this taxonomy that refine it | Items that fall outside it |
|---|---|---|---|
| **Diagnostic** (the model predicts a current condition, e.g. VFSS-confirmed dysphagia) | QUADAS-2 | RS1 (reference-standard domain, at dysphagia-specific granularity), RS5 (patient selection and spectrum), RS6 (applicability) | RS3 and RS4, which concern the machine-learning label and its measurement rather than the index test |
| **Prognostic** (the model predicts a future outcome, e.g. late toxicity or tube feeding) | PROBAST+AI | RS1 (outcome definition), RS5 (participants), RS6 (intended use) | RS3 and RS4, for the same reason; RS2, since proxy leakage is about construct substitution |

Neither instrument asks for rater reliability of the label (RS4), for the loss incurred by
binarizing an ordinal swallowing scale (RS3), or for proxy leakage (RS2), which is why those
three items are the specific contribution and are reported separately.

## 3. How the construct is used (three places)

1. **Rubric (Layer A):** RS1–RS6 are added to `transparency-rubric.csv` as a clinical block and coded across the census.
2. **Analysis and synthesis:** how many studies exhibit proxy leakage · how many report rater κ · the rate of healthy-control contamination · the distribution of aetiologies → a **clinical reproducibility map** that sits alongside the computational one as a second axis.
3. **Minimum-reporting recommendations (clinical half):** every study should report the reference-standard type, the ordinal scale used and its granularity, rater κ or ICC with the number of raters and the blinding procedure, the aetiological mix, the proportion of healthy controls, and whether sampling was consecutive or by convenience.

---

## 4. Open methodological questions

These are recorded here rather than silently resolved, because they bear on how RS4 and RS5 are interpreted.

1. Is the RS3 scale list complete for the instruments in current clinical use?
2. What threshold defines adequate label reliability for RS4 (κ ≥ 0.6? ICC ≥ 0.75?), and on what published basis?
3. Are the RS5 aetiology categories the right partition for the dysphagia-AI literature?

---

## 5. Application — first-pass coding of the census studies (16 July 2026)

`rs-taxonomy-coding.csv` codes 18 studies against RS1–RS6. The division of labour is recorded explicitly:

- **Objective columns** (verifiable from the text): RS1 reference-standard type · RS3 scale and binarization · RS4 whether rater reliability **is reported** (κ/ICC yes or no).
- **Clinical-interpretation columns** (marked `[NKT]`): the RS2 proxy-leakage judgement · RS5 spectrum risk · the RS4 threshold for adequate reliability · borderline scope decisions.
- The evidence level is given for every row: `abstract+fulltext` (6 studies, firm) against `inventory-only` (no paper match, so the row requires full-text coding).

### Objective preliminary findings (all auditable)

1. **Rater reliability (κ / ICC) is not reported at all in the studies we could read: 0/6** of the full-text-accessible subset (the other 12 of the 18 have no retrievable full text and are coded *not assessable*, so this is **not** extrapolated to 18). What makes this striking is that even studies that **acknowledge** the problem do not quantify their own label reliability — *masa/Saab* notes that "even VFSS by SLP has … poor inter-rater reliability"; *MITI* describes manual expert annotation as "prone to errors". The problem is known but not measured.
2. **The reference standard is heterogeneous and unstandardized:** instrumental reference (VFSS: A, E, G, M, O · manometry: N · CT/MRI segmentation: D, F) / clinical bedside (B) / **proxy outcome** (Q tube feeding and pneumonia · R CTCAE toxicity · C postoperative outcome) / physical (H viscosity) / unclear and low-provenance (I, J, K, L, P). There is no common reference.
3. **Proxy leakage (RS2) is common** `[NKT]`: several models predict not the instrumental gold standard but a **proxy** for it — *B* (voice → bedside screen), *Q* (voice → clinical outcome), *O* (clinical and voice → VFSS-confirmed dysphagia), *R* (dose → toxicity). The model learns a shadow of dysphagia rather than dysphagia.
4. **The code-available subset skews toward low label provenance:** for studies such as I, J, K and L the publication link and the reference standard are unclear, so the repositories that share code may also be those with the weakest label provenance.

### External validation (independent evidence)

The full text of the Kwok and Wong scoping review (JMIR 2025, PMC12089864) reports that **18 of 24 dysphagia-AI studies (75%) either did not describe the sampling approach or did not state whether case-control labels were blinded** — independent confirmation of the finding that label provenance is systematically under-reported.

### Combined thesis (two axes, one argument)

> Dysphagia AI is **reproducible neither computationally nor clinically**, because **both kinds of provenance are systematically missing**:
> - **Computational provenance:** weights, environment and license are absent → 0/18 re-executable out of the box.
> - **Clinical and label provenance:** rater reliability, spectrum and reference standard are under-reported → 0/6 of the readable studies report label κ or ICC (not extrapolated to 18), and the labels themselves are heterogeneous proxies.
>
> Even a model that re-runs perfectly is **not clinically reproducible** if it rests on weak or unreported labels. Each axis is necessary, so the contribution is more than one further audit.

### Status of the coding

- The `inventory-only` rows could not be coded from full text. That is reported as the reason the clinical axis rests on a subset, not carried as work still to do.
- The `[NKT]` judgements were verified against the source publications on 21-22 August 2026. Four rows were corrected and the change is recorded per row in `correction_2026-08-22`; the corrected set was accepted by the clinician author on 22 August 2026.
- One row remains outside the assessable subset by decision rather than by necessity: the Cubero row's published version was not retrieved through the study's channels, and a postprint that would make it assessable was identified afterwards. Reopening it would move the subset from six studies to seven and the reliability count from 0 of 6 to 0 of 7. The authors have not taken that step, and the reason is recorded here so the choice is visible.
