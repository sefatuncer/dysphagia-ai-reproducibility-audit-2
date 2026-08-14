> ⚠️ **PLANNED UNDER THE PRE-PIVOT DESIGN, NOT EXECUTED AS DESCRIBED.**
> This file belongs to the study's earlier systematic-review-style design, which assumed
> dual independent human screening, a methodologist/librarian third author, PRESS review,
> and institutional database access. **The study pivoted to a two-author meta-research
> re-execution census with an objective, machine-checkable inclusion criterion.** None of
> the methodologist-dependent procedures below were carried out. What was actually done is
> reported in the manuscript, and screening reliability was instead assessed by a released,
> blind, rule-based re-coding of every screened record. This file is retained as design
> history so the change of plan is auditable, not concealed.

# Statistical analysis plan (SAP)

> ⚠️ **v2 ADAPTATION (re-execution census).** This plan partly retains the pre-pivot language of a systematic review over the whole literature ("denominator A"). **In the v2 design the denominator is the code-available, discoverable set**, not the whole literature. Consequently the **numerical two-proportion comparison against radiology (Newcombe) is NOT APPLIED**, because the denominators do not match; see §5 (v2). Radiology serves only as a conceptual reference frame. The primary analysis is the Wilson 95% interval (study level N=18 primary, repository level N=22 as sensitivity; `09_census_synthesis.py`). RS4 (κ) clinical reliability is reported for the subset with accessible full text (§4).

**Status:** design document, published with the archive for audit. It is **not** a timestamped pre-registration and **no claim is made that it predates the analysis**; no registry entry exists. The manuscript states the same in its Design and registration section. (Corrected in v1.1.0: this line previously read "locked before any outcome data were seen", a temporal-priority claim the study does not make and cannot evidence.)
**Software:** Python (`scripts/03_analysis.py`) — fixed seed, pinned versions; every figure is produced by script, so that the article's reproducibility thesis is applied to its own analysis.

## 1. Estimands
**Denominator A (transparency, all included studies):** the sharing rate for each binary item — (a) code, (b) a data-access statement or accessible data, (c) trained weights, (d) an environment or dependency file, (e) a model card, (f) an open license. Additionally: seed, README run instructions, version pinning, external validation, compute reporting.
**Denominator B (the code-available subset):** the re-executability verdict — **not a proportion**, but a descriptive count plus a barrier taxonomy.

> **NUMERATOR of the primary code-sharing estimand.** For the headline rate and the radiology comparison, "code sharing" means **a statement plus a resolvable URL plus an accessible repository** (`code_stmt ∈ {yes, explicit_url}` AND `repo_accessible = yes`). **Statement only**, where the URL is dead or absent, is reported separately as a secondary figure. This definition maps conceptually onto the "source-code availability" measured by Venkatesh 2022. **v2:** because the denominators do not match, the Newcombe numerical comparison is not applied and radiology is used only as a conceptual frame (see §5, v2).
> **Applicable denominator per item.** TRIPOD+AI applies to all included studies; **CLAIM only to the imaging subset**, **STARD only to the diagnostic subset**, **TRIPOD to the prediction-model subset**. Every reporting-standard item is reported against its own applicable denominator, which is what the "state the denominator explicitly" rule in §2 requires.

## 2. Primary analysis
- For every item, a **proportion with a Wilson 95% interval** (Wilson is the correct choice for small denominators and extreme proportions; the normal approximation is not used).
- The denominator is stated **explicitly** for every item, and "not reported" is a **separate category** — nothing is imputed.
- **Multiplicity and power.** This is an **estimation** study with no confirmatory hypothesis test. Intervals quantify precision only, no contrast between strata is interpreted inferentially, and therefore no classical multiplicity correction is applied; the manuscript states this explicitly. **v2:** there is no confirmatory comparison at all, the radiology–Newcombe test having been removed (§5). Because the study is a **census** of the eligible literature, an a-priori power calculation is not applicable; the widths of the Wilson intervals convey the precision obtained.

## 3. Stratification (pre-specified, no fishing)
Only these strata: **modality** (VFSS/FEES/acoustic/sEMG/HRM/wearable/clinical) · **year band** (2010–19 / 2020–22 / 2023–26) · **venue type** (clinical / engineering and computer science / informatics) · **task** (diagnosis / screening / severity / monitoring). Where a sub-cell contains fewer than 5 studies, it is reported descriptively only; the interval is wide and is not interpreted.

## 4. Reliability (κ)
- **Screening κ:** Cohen κ for each **independent** pair (S.T. ↔ methodologist; N.K.T. ↔ methodologist) rather than for the married co-author pair. **A 95% interval (bootstrap, `03_analysis.py:cohen_kappa_ci`, fixed seed) plus the Landis–Koch interpretation.**
- **Rubric κ:** double coding on a calibration set giving item-wise κ; any item below 0.6 triggers clarification of the codebook and re-calibration. **The calibration N and the extent of double coding are fixed in a single form** (calibration of 8–10 studies, after which **at least 20%** of the included set is double coded).
- **κ by scale type:** **ordinal** items (RS3 PAS/DIGEST/FOIS) take a **weighted κ** (linear or quadratic, so that a disagreement between adjacent categories does not count as a full disagreement); **nominal** items take an unweighted Cohen κ.
- **The κ paradox (skewed marginals):** for items with an extreme base rate — a model card, for example, is absent almost everywhere — κ can be paradoxically low even when observed agreement is high. Therefore **observed agreement (po) and PABAK** are reported alongside κ, and the Landis–Koch label is interpreted cautiously in that context.

## 5. Comparison analysis (radiology) — v2 (CONCEPTUAL, no numerical Newcombe)
⚠️ **v2 DECISION.** The denominator of this study is the **code-available, discoverable set**, whereas the radiology figures are **unconditional** rates over all studies — Venkatesh 2022 (34%, 73/218) and Lee 2025 (39.9%, 107/268). Because the denominators do not match, **the two-proportion difference with a Newcombe 95% interval is NOT APPLIED and NOT REPORTED.**
- Radiology is used only as a **conceptual availability-versus-executability frame** in the Introduction: availability in a neighbouring field is roughly 34–40%; availability is necessary but not sufficient; we measure the downstream step, executability, and find that it collapses to approximately zero. **No numerical difference is claimed.**
- The headline is the dysphagia executability result itself (0/18 re-executable out of the box, with a Wilson interval); radiology is qualitative context in the Introduction.
- ❌ **The "deep learning about 11.5%" comparison was REMOVED** (Lee 2025 in fact reports 39.9%; the citation was corrected and the use made conceptual). The only verified neighbouring-field anchors are Venkatesh 34% and Lee 39.9%, both conceptual only.

## 6. Layer B (re-run) — descriptive
- Verdict counts: **re-executable / partial / not-reproduced / not-attemptable**, plus the frequency of each barrier category (dependency conflict, GPU only, missing weights, missing data, code error, missing post-processing, and so on).
- **No proportion is claimed** (N is small and selection is non-random). The framing is that **even a best-case subset does not run out of the box**, which is a strong lower bound plus evidence on the depth of the barriers. Pilot repository #1 is presented as a full case.
- **Sample = census:** **every** included study with a code-sharing statement and a resolvable URL enters re-execution. There is no subjective "apparently runnable" gate, which would introduce selection bias; repositories that cannot be run still produce information, via a `not_attemptable` verdict. The two pilots that preceded the plan are reported **separately** as feasibility work rather than inside the primary count.
- **Hardware-neutral against hardware-caused failure:** in a CPU-only harness the **GPU-only** verdict is reported separately, and **the lower-bound claim rests only on hardware-neutral failures** (dependency conflict, missing weights, code error, absent license). F4 verdicts are stratified into hardware-caused and hardware-neutral.
- **Tolerance for metric reproduction, by output type:**
  (a) **classification metrics** (accuracy, AUC, F1) → within an absolute **±5 points** or within the reported **95% interval**;
  (b) **continuous output** (area, distance, pixel-mm) → within a relative **±5%** or within the reported measurement error or repeatability margin;
  (c) where no reference metric, interval or example data exist → **"metric reproduction not attemptable"**, with nothing imputed. Re-executability always takes priority; metric reproduction is secondary.

## 7. Triage validation
A random sample of about 200 records is screened against a human gold standard to establish the **sensitivity, specificity and PPV** of the deterministic regex flags (`t_bucket`, `t_review_like`, `t_has_ai`), together with a confusion matrix. The purpose is to show that triage **excluded no eligible study**, that is, to provide evidence of high recall. Triage is an organizational device, not an exclusion box in the flow diagram.

## 8. Sensitivity analyses (pre-specified)
(a) excluding preprints · (b) excluding healthy-only cohorts · (c) by half of the year range · (d) restricted to the high-confidence core found in at least 3 sources. Is the main result robust to each?

## 9. Missing data and deviations
- The distinction between "not reported" and "no" is preserved, and both are reported separately.
- Any deviation from the protocol is recorded as a **time-stamped amendment** and declared in the article.

## 10. Output figures (produced by script)
F1 flow diagram · F2 item-wise proportions with Wilson intervals (forest) · F3 modality × year heat map (**N is printed in every cell; cells with N<5 are greyed or flagged so that colour intensity is not read as signal**) · F4 re-run verdicts and barrier taxonomy (**stratified into hardware-neutral and GPU-only**) · T1 radiology conceptual context (its own proportions with Wilson intervals; **no Newcombe difference**, v2 §5) · T2 distribution of the clinical taxonomy (RS1–RS6) over the RS-applicable subset.
> **Figure production:** every figure is generated by `03_analysis.py` (fixed seed, standard library only) from the real rubric data; the 11.5% comparison was removed, the radiology denominator 73/218 was verified, and a bootstrap 95% interval was added for κ.
