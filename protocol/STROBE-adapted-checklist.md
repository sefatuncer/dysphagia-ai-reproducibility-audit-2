# Adapted STROBE checklist — cross-sectional, unit of observation = research artifact

**Why this document exists.** The article states that it reports in accordance with an
adapted STROBE checklist for cross-sectional studies. A compliance claim that cannot
be checked is exactly the kind of claim this study audits in others, so the completed
checklist is published here rather than asserted in the text.

**Why STROBE and not something else.** No EQUATOR guideline fits this design.
PRISMA 2020 and PRISMA-ScR presuppose a synthesis of studies; MOOSE presupposes
meta-analysis of observational studies; STARD, TRIPOD and their risk-of-bias
companions presuppose human participants and an accuracy or effect estimate. What
remains is a cross-sectional design whose unit of observation is an artifact rather
than a person, so STROBE's items are read with that substitution and the items that
do not survive it are marked, with the reason, rather than silently dropped.

**Not a supplementary file.** It lives in the archive under the same DOI as the rest
of the materials.

| # | STROBE item | Reading for an artifact-unit design | Where / status |
|---|---|---|---|
| 1a | Design in title or abstract | Same | Title: "audit"; Abstract: "meta-research audit" |
| 1b | Informative abstract | Same | Abstract |
| 2 | Background, rationale | Same | §1 |
| 3 | Objectives, pre-specified hypotheses | Estimation, no hypotheses | §1 RQ1, RQ2a, RQ2b, RQ3; §2.7 states no confirmatory testing |
| 4 | Study design | Same | §2.1 |
| 5 | Setting, locations, dates | Discovery services queried, access dates | §2.3 (16 Jul 2026), §2.4 (16 and 30 Jul 2026), §2.6 (pilots 13–14 Jul 2026) |
| 6a | Eligibility criteria, sources, selection | Inclusion rule and its provenance | §2.2 (criteria i–iv, and when iv was added); `search/repo-inventory.csv` carries a closed decision per candidate |
| 6b | Matching criteria | **Not applicable** — no matched design | — |
| 7 | Variables: outcomes, exposures, confounders | Signals and verdicts; no exposure/confounder structure | §2.4 signals; §2.6 verdict definitions |
| 8 | Data sources, measurement | Scripted intake against live repositories | §2.4; `scripts/08`, `19`, `20`; each result file carries its access date |
| 9 | Bias | Design-specific bias inventory in place of a RoB instrument | §2.1 (discovery/selection, classification, verification, retrievability-driven missingness, temporal drift) |
| 10 | Study size | Set fixed by the instrument, not chosen | §2.7 (no a priori size calculation applies) |
| 11 | Quantitative variables handling | Binary signals; composite as logical AND | §2.5, §2.6 |
| 12a | Statistical methods | Proportions with Wilson intervals; κ with BCa and percentile bootstrap | §2.7 |
| 12b | Subgroups and interactions | Study-level primary, repository-level and scripted-only as sensitivity | §2.7, Table 3 |
| 12c | Missing data | "Not assessable" kept distinct from "absent"; retrievability-driven missingness named | §2.3, §3.4 |
| 12d | Sampling strategy | **Not applicable** — enumeration, not a sample | §2.2 |
| 12e | Sensitivity analyses | Scripted-only subset; relaxed composite definition | §2.6, §3.2 |
| 13a–c | Participants: numbers at each stage, reasons, flow | Candidates through inclusion, with reasons | §3.1, Table 2, Figure 1 |
| 14a | Descriptive data | Per-artifact signals | Table 3; `transparency/repo-intake-table.csv` gives the study-level record |
| 14b | Missing data per variable | Same | §3.4 (k=6 vs 18); Table 5 footnote |
| 15 | Outcome data | Signal counts and verdict distribution | Tables 3 and 4; §3.3 |
| 16a–c | Main results, estimates, confidence | Proportions with intervals; derived composite given without one | Tables 3 and 4; Table 4 footnote c |
| 17 | Other analyses | Clinical axis (RS1–RS5) as exploratory secondary | §3.4 |
| 18 | Key results | Same | §4 |
| 19 | Limitations | Same | §4 Limitations |
| 20 | Interpretation | Same | §4 |
| 21 | Generalizability | Bounded to the discoverable code-available slice | §2.2, §4 |
| 22 | Funding | Same | §Funding |

## Items where the substitution changes the meaning

Three items do not carry over cleanly and are recorded here rather than forced:

- **Item 6b (matching)** and **item 12d (sampling)** presuppose a sampled,
  comparison-based design. This is an enumeration of what a stated instrument
  reaches, so neither applies. Marking them "not applicable" is a design statement,
  not an omission.
- **Item 16 (effect estimates)** presupposes an effect. There is none; the estimands
  are proportions, and the intervals are reported as small-sample fragility bands
  with that stated in §2.7.

## What this checklist does not do

It records where each item is addressed. It does not certify that the item is
addressed *well*, and it is not a risk-of-bias assessment. The article states
separately, and deliberately, that no formal risk-of-bias instrument was applied and
why.
