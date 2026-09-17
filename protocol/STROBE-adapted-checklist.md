# Adapted STROBE checklist for a cross-sectional design whose unit of observation is a research artifact

**Why this document exists.** The article states that it reports against an adapted
Strengthening the Reporting of Observational Studies in Epidemiology, or STROBE,
checklist. A compliance claim that cannot be checked is exactly the kind of claim this
study audits in others, so the completed checklist is published rather than asserted.

**Why STROBE and not something else.** No reporting guideline fits this design exactly.
PRISMA 2020 and PRISMA-ScR presuppose a synthesis of studies, MOOSE presupposes a
meta-analysis of observational studies, and STARD and TRIPOD, with their risk of bias
companions, presuppose human participants and an accuracy or effect estimate. What
remains is a cross-sectional design whose unit of observation is an artifact rather than
a person, so the STROBE items are read with that substitution, and the items that do not
survive it are marked with the reason rather than silently dropped.

**Where it is published.** The same checklist is Online Resource 1 of the article. This
copy is kept in the archive under the same identifier as the rest of the materials and
adds pointers to the files that hold the underlying records.

**Locators.** The article has unnumbered headings, so the locators name the section. They
also refer to Tables 1 to 5, Figs. 1 and 2 and Online Resources 2 to 6 of the article.
This copy was matched to the article on 17 September 2026.

| # | STROBE item | Reading for a design whose unit is an artifact | Where addressed |
|---|---|---|---|
| 1a | Design in title or abstract | Same | Title, which says audit, the Abstract, and Methods, Study Design, which says cross-sectional meta-research audit |
| 1b | Informative abstract | Same | Abstract, which gives channels, set size, imaging share, signals, builds and the clinical axis |
| 2 | Background and rationale | Same | Introduction |
| 3 | Objectives and pre-specified hypotheses | Estimation, and no hypotheses are tested | Introduction, which states three questions and that no hypothesis is tested |
| 4 | Study design | Same | Methods, Study Design |
| 5 | Setting, locations and dates | Services queried and every date on which something was read or built | Methods, Eligibility and Discovery, Methods, Data Extraction, Methods, Containerized Reruns, Results, Discovery and Inclusion, the footnotes of Table 3, and Online Resource 2, sections S2 and S4. Each result file in `results/` carries its own access date |
| 6a | Eligibility criteria, sources and selection | Inclusion rule, its provenance and the unit rules | Methods, Eligibility and Discovery, with the four criteria and when the fourth was added. Online Resource 2, section S8. Fig. 1. `search/repo-inventory.csv` carries a closed decision and a reason for every candidate |
| 6b | Matching criteria | **Not applicable**, since no matched design is used | Not applicable |
| 7 | Outcomes, exposures, confounders | Signals and verdicts, with no exposure or confounder structure | Methods, Data Extraction, Methods, Containerized Reruns, and Online Resource 2, section S1 |
| 8 | Data sources and measurement | Scripted intake against live repositories, intake of two pilots by hand, clinical coding from full text | Methods, Data Extraction, Methods, Reference Standard Taxonomy, Methods, Containerized Reruns. Scripts `08`, `19` and `20` in `scripts/`, with `transparency/repo-intake-table.csv` as the record |
| 9 | Bias | An inventory of biases specific to this design in place of a risk of bias instrument | Methods, Study Design, Online Resource 2, section S8, Methods, Reference Standard Taxonomy, and Methods, Containerized Reruns |
| 10 | Study size | Set fixed by what the discovery channels reached, not chosen | Methods, Statistical Analysis, and Results, Discovery and Inclusion, for the recall of the channels against a comparator pool |
| 11 | Quantitative variables | Binary signals, with the composite as a conjunction within a repository | Methods, Data Extraction, and Methods, Containerized Reruns |
| 12a | Statistical methods | Proportions with Wilson intervals, agreement of the rule against the record, and κ, PABAK and bootstrap intervals for each channel | Methods, Study Design, Methods, Statistical Analysis, and Online Resource 2, section S3. Script `11` produces the agreement statistics |
| 12b | Subgroups and interactions | Release level primary, with imaging and other input, releases linked to a publication, the scripted channels only and the repository level as descriptive views | Methods, Statistical Analysis, and Table 1. Script `31` computes the strata |
| 12c | Missing data | Not assessable kept distinct from absent, unreadable files recorded as undetermined, and missingness driven by retrievability named | Methods, Data Extraction, Methods, Statistical Analysis, Results, Label Provenance, and Online Resource 2, section S8 |
| 12d | Sampling strategy | **Not applicable**, since this is an enumeration rather than a sample | Methods, Eligibility and Discovery |
| 12e | Sensitivity analyses | Disputed screening records, the fourth criterion read back in, the subset from the scripted channels only, and readings of the composite that require only pinning or any declared environment | Methods, Study Design, Methods, Eligibility and Discovery, Results, What the Repositories Carried, and Online Resource 2, section S5. Scripts `28` and `31` |
| 13a–c | Numbers at each stage, reasons and flow | Candidates through inclusion, by channel, with reasons | Results, Discovery and Inclusion, and Fig. 1 |
| 14a | Descriptive characteristics | Modality, channel, link to a publication and signals for each release | Results, Discovery and Inclusion, Table 1, Fig. 2, and Online Resources 4 and 5. `transparency/repo-intake-table.csv` gives the record for each repository |
| 14b | Missing data per variable | Same | Results, Label Provenance, Table 4, Fig. 2, where an empty cell marks a signal not observed, and Online Resource 4, where fields are marked not measured |
| 15 | Outcome data | Signal counts and the distribution of verdicts | Tables 1 and 2, Fig. 2, and Results, Reruns |
| 16a | Unadjusted estimates and precision | Proportions with intervals, and the derived composite given without one | Table 1, footnote c, and Results, Reruns |
| 16b | Category boundaries | **Not applicable**, since no continuous variable is categorized | Not applicable |
| 16c | Relative risk | **Not applicable**, since no risks are compared | Not applicable |
| 17 | Other analyses | Journal policy, printed statement and repository, the exploratory clinical axis, the strata, the install checks and the comparison of library versions. The policy mapping, the strata and the two container checks were added after the main analysis and are post hoc | Results, What the Transparency Signal Delivers and Table 3, Results, Label Provenance and Table 4, Results, What the Repositories Carried, Methods, Containerized Reruns and Results, Reruns, and Online Resource 2, sections S4 and S6. Scripts `30`, `31`, `33` and `34` |
| 18 | Key results | Same | Discussion, opening paragraphs |
| 19 | Limitations | Same | Discussion, Limitations |
| 20 | Interpretation | Same | Discussion |
| 21 | Generalizability | Bounded to what the stated channels reach | Results, Discovery and Inclusion, Discussion, and Discussion, Limitations |
| 22 | Funding | Same | Title page, Statements and Declarations |

## Items where the substitution changes the meaning

Item 6b on matching and item 12d on sampling presuppose a sampled design that makes
comparisons. This is an enumeration of what a stated procedure reaches, so neither
applies, and marking them not applicable is a design statement rather than an omission.
Items 16b and 16c presuppose categorized continuous variables and a comparison of risks,
and there are none. The estimands are proportions, and their intervals are descriptive
indicators of imprecision, as stated under Statistical Analysis in Methods.

## What this checklist does not do

It records where each item is addressed. It does not certify that the item is addressed
*well*, and it is not a risk of bias assessment. The article states separately, and
deliberately, that no formal risk of bias instrument was applied and why.
