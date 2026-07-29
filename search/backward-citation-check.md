> ⚠️ **PLANNED UNDER THE PRE-PIVOT DESIGN, NOT EXECUTED AS DESCRIBED.**
> This file belongs to the study's earlier systematic-review-style design, which assumed
> dual independent human screening, a methodologist/librarian third author, PRESS review,
> and institutional database access. **The study pivoted to a two-author meta-research
> re-execution census with an objective, machine-checkable inclusion criterion.** None of
> the methodologist-dependent procedures below were carried out. What was actually done is
> reported in the manuscript, and screening reliability was instead assessed by a released,
> blind, rule-based re-coding of every screened record. This file is retained as design
> history so the change of plan is auditable, not concealed.

# Backward-citation screening — corpus completeness check

**Purpose:** to compare the corpus against the study lists of known dysphagia-AI reviews and see what is missing. **Status: Kwok and CoDAS completed quantitatively; the 633-record bibliometric list requires institutional Web of Science access and remains human work.**

## Source 1 — Wong/Kwok et al. JMIR 2025;27:e65551 ✅ COMPLETED
- **Title:** "Current Technological Advances in Dysphagia Screening: A Systematic Scoping Review" (HK PolyU). Scope: dysphagia **screening**, **24 studies** (refs [35]–[58]), 2979 participants. QUADAS-2+M and TRIPOD+AI, 5 AI domains.
- **Modalities (Kwok):** acoustic 54% (13/24), vibratory 38% (9/24), nasal airflow 8%, EMG 8%, strain or motion 8%, optical 4%; multimodal 25%.
- Full text: https://www.jmir.org/2025/1/e65551 · PDF: PolyU IRA 10397/115215 · PMID 40324167.

### Matching result
**Of the 24 Kwok studies, 13 are present in the corpus and 11 are not.** The 11 absences break down as:

| Status | Ref | Note |
|---|---|---|
| **Out of scope (pre-2010, correctly excluded by design)** | 35 (2008), 44 (2004), 54 (2008), 55 (2009) | Outside the 2010–2026 filter, so not a gap |
| **IN SCOPE AND MISSING (to be added)** | 45 (2011 Artif Med), 40 (2022 IEEE TASLP), 41 (2024 ICASSP), 50 (2023 BSPC), 51 (2023 DSP), 56 (2019 **Dysphagia** s00455), 57 (2021 ISCAS) | **7 studies** |

### Interpretation (an important finding)
- Of the 20 in-scope Kwok studies, **13 (65%) are in the corpus**, so the open-API search is reasonable but not complete.
- **Six of the seven missing studies are in IEEE or engineering venues** (TASLP, ICASSP, ISCAS, DSP, BSPC), which gives **quantitative support to the claim that an institutional IEEE Xplore and Scopus search is required**. Open APIs partly miss computer-science venues.
- One missing record (ref 56, Dysphagia s00455, 2019) is PubMed-indexed and was still missed, so the term sensitivity of the search string needs librarian and PRESS review.
- **Action:** the 7 in-scope absences are to be added after the institutional search with `source=backward_citation`, forming the "other methods" arm of the flow diagram. Most would arrive from an institutional IEEE search in any case.

## Source 2 — CoDAS 2025 scoping review ✅ COMPLETED
- **Citation:** Silva et al., "Artificial intelligence in the diagnosis and management of dysphagia: a scoping review." **CoDAS 2025;37(4):e20240305** (DOI 10.1590/2317-1782/e20240305en). 61 included studies; EMBASE, LILACS, Livivo, PubMed, Scopus, Cochrane, Web of Science plus grey literature. The reference standard is mostly VFSS and deep learning predominates. Open PDF at codas.org.br.
- **Matching:** **64 unique DOIs taken from its reference list** — note that this is the review's bibliography, not its list of included studies — of which **44 (69%) are present in the corpus**. Of the 20 absent, 16 are background or unclear and **4 concern dysphagia AI**; two of those are pre-2010 and correctly out of scope, leaving **2 genuine in-scope gaps**:
  - `10.1038/s41598-023-34999-8` — Sci Rep 2023;13:7835, "Machine learning predictive model for aspiration screening in hospitalized patients with acute stroke" (PubMed-indexed, so again a question of search-string sensitivity). ⚠️ **DOI correction (16 Jul):** the first extraction truncated the final character and produced `-x`, which returns 404 at Crossref and OpenAlex; the correct DOI ending in `-8` was confirmed from the title. OpenAlex additionally returned a **corrupt record** for this DOI, linked to a 1968 catalysis article, so `06_backward_additions.py` was changed to prefer Crossref, the DOI registration authority being the canonical source of metadata. A small but pointed meta-finding: the metadata infrastructure itself carries reproducibility errors.
  - `10.1109/access.2020.3019532` — IEEE Access 2020, semantic segmentation (again an **IEEE** gap).

## Source 3 — the 633-record bibliometric list (Web of Science 2000–2025) ⏳ HUMAN (WoS access)
A broad list; cross-checking its core references requires **institutional Web of Science** and is therefore human work.

## Conclusion (the two reviews combined)
- **Corpus completeness is roughly 65–70%** (Kwok in-scope 13/20; CoDAS 44/64), so the open-API search is reasonable but not complete.
- **The gaps are systematically in IEEE and engineering venues** (TASLP, ICASSP, ISCAS, DSP, IEEE Access), which makes an **institutional IEEE Xplore and Scopus search non-negotiable** for a formal review. This is now quantitatively evidenced.
- **In-scope absences to add:** 7 from Kwok plus 2 from CoDAS, about **9 studies** (most of which an institutional IEEE search would return anyway), entered as `source=backward_citation` in the "other methods" arm.

## Method (reproducible)
The Kwok PDF was converted to text with PyMuPDF, references [35]–[58] were parsed with a `[doi:]` and `[Medline:]` regex, and the results were matched against `combined-corpus.csv` on DOI and PMID. The same pipeline is reused for CoDAS and for the 633-record list.
