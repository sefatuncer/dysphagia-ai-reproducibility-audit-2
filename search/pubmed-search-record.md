> **NOTE ON SCOPE.** Sections 1–4 of this file are the live search record referenced by the
> manuscript: the queries, dates and counts are what was actually run. The closing "next
> steps" section belongs to the study's earlier systematic-review-style design and was **not
> executed as written** — no institutional database search, no dual independent human
> screening and no PRISMA-conformant flow was carried out, and the manuscript neither claims
> them nor reports a PRISMA-ScR-conformant search. That section is retained as design history
> so the change of plan is auditable rather than invisible.

# Search record — PubMed/MEDLINE

**Database:** PubMed/MEDLINE (NCBI E-utilities `esearch`)
**Search date:** 2026-07-13
**Date filter:** 2010–2026 (`2010:2026[pdat]`)
**Total results:** **865 records** → the PMID list is the `pmid` column of `corpus-metadata/pubmed-metadata.csv`

## 1. Query as run (verbatim)
```
("Deglutition Disorders"[Mesh] OR dysphagia[tiab] OR deglutition[tiab] OR swallow*[tiab])
AND
("Artificial Intelligence"[Mesh] OR "artificial intelligence"[tiab] OR "machine learning"[tiab]
 OR "deep learning"[tiab] OR "neural network*"[tiab] OR convolutional[tiab] OR transformer*[tiab]
 OR "random forest"[tiab] OR "support vector"[tiab] OR radiomics[tiab]
 OR "computer-aided"[tiab] OR "computer aided"[tiab])
AND 2010:2026[pdat]
```
PubMed's own translation is returned in `esearchresult.querytranslation`; MeSH expansion was applied automatically.

## 2. Distribution by year (indicative growth trend)
| Period | Records per year |
|---|---|
| 2010–2019 | 12–37 per year (flat, around 20–30) |
| 2020 | 51 · 2021: 64 · 2022: 92 · 2023: 95 |
| 2024 | 128 · 2025: 192 · 2026 (partial, about 7 months): 146 |

**Comment:** dysphagia-AI publications grew roughly eight- to tenfold after 2020, which is the "why now" argument for the study: a reproducibility audit matters most during exactly such an expansion.
*(Note: the per-year `[pdat]` counts sum to about 1008 while the range query returns 865. The difference comes from how PubMed matches date fields. **The authoritative figure is 865**, the range total; the per-year counts serve only to show the trend.)*

## 3. Corpus composition (informs screening) — `pubmed-metadata.csv`
The PMID, year, journal, publication type and title of all 865 records are in `pubmed-metadata.csv`, with empty `include_screen1` and `exclude_reason` columns so that the file is ready for screening.
- **Most frequent venues:** Sci Rep (28) · Dysphagia (22) · IEEE EMBC (18) · Neurogastroenterol Motil (17) · Sensors (16) · Surg Endosc (15) · Laryngoscope (14) · Diagnostics (13) · Comput Biol Med (10).
- **Publication types:** 853 journal articles; about **110 reviews plus 23 systematic reviews, roughly 133 reviews to be excluded**; 32 case reports; 14 validation studies; 20 multicentre studies.
- **Screening signal:** removing the roughly 133 reviews and the head-and-neck cancer surgery and radiotherapy cluster (Surg Endosc, Head Neck, Radiother Oncol) brings the core diagnosis-and-assessment set close to 60, consistent with the scoping estimate.

## 4. Multi-source search (open APIs, 13 July)
| Source | Results | Note |
|---|---|---|
| PubMed/MEDLINE (tiab) | **865** | the core |
| Semantic Scholar (bulk boolean) | **391** | coverage of computer-science and engineering venues (IEEE, ACM, arXiv) that PubMed misses |
| Europe PMC (restricted to TITLE/ABSTRACT) | **513** | PubMed plus preprints. **Lesson:** an unrestricted query matched full text and returned 10,686 noisy records, so the search was restricted to title and abstract |
| OpenAlex (title and abstract union) | **1890** | broad coverage comparable to Scopus or Web of Science; over-retrieves on "swallowing" and narrows at screening |

The records are in `semanticscholar-records.csv`, `europepmc-records.csv` and `openalex-records.csv`. Institutional Scopus, Web of Science and IEEE searches would be added by hand for a formal review; the open sources, in particular Semantic Scholar and OpenAlex, already supply much of the computer-science venue coverage.

### Combined corpus (after deduplication) — `combined-corpus.csv`
- Four sources → 3659 raw rows → **2171 unique** (deduplicated on normalized title).
- **What the extra sources genuinely add:** **177 high-confidence records** that are absent from PubMed but present in Semantic Scholar or Europe PMC, in exactly the venues PubMed and MEDLINE miss — **medRxiv (8) · Research Square (14) · bioRxiv (2)** among preprints, plus **IEEE Sensors Journal (5) · IEEE Access (3) · ACM IMWUT (3) · Biomedical Signal Processing and Control (3)** among computer-science and engineering venues.
- **446 records appear in at least 3 sources**, forming a high-confidence relevant core. The **1131** OpenAlex-only records are broad-match noise and drop out at screening.
- **Automatic flags:** 195 probable **reviews** (to be excluded) · 241 **cancer or radiotherapy** records (a clinical decision, since prediction of post-radiotherapy dysphagia can be in scope). `combined-corpus.csv` carries `sources`, `n_sources`, `likely_review` and `likely_cancer_rt` alongside the empty `include_screen1` and `exclude_reason` columns.
- **Rough candidate pool:** 2171 minus 195 reviews minus about 1131 OpenAlex noise ≈ **850 real candidates**, narrowing after title, abstract and full-text screening to a core diagnosis-and-assessment set of about 60, consistent with the scoping estimate.

## 5. Next steps (pre-pivot design, not executed)
1. Run the remaining databases with institutional access and merge all records.
2. Import into Rayyan or Covidence and deduplicate.
3. **Dual independent** title-and-abstract and then full-text screening with **Cohen κ**.
4. Fill the flow-diagram counts from that process.
