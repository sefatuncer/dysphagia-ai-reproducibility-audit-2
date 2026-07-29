> ⚠️ **PLANNED UNDER THE PRE-PIVOT DESIGN, NOT EXECUTED AS DESCRIBED.**
> This file belongs to the study's earlier systematic-review-style design, which assumed
> dual independent human screening, a methodologist/librarian third author, PRESS review,
> and institutional database access. **The study pivoted to a two-author meta-research
> re-execution census with an objective, machine-checkable inclusion criterion.** None of
> the methodologist-dependent procedures below were carried out. What was actually done is
> reported in the manuscript, and screening reliability was instead assessed by a released,
> blind, rule-based re-coding of every screened record. This file is retained as design
> history so the change of plan is auditable, not concealed.

# Institutional search strings and PRESS form — ready to run (execution: human)

**Purpose:** whoever holds institutional access, or a librarian, can **copy and paste** the strings below, export the results into a single folder, and run the merge script. The open APIs were already searched (PubMed 865 + Europe PMC 513 + Semantic Scholar 391 + OpenAlex 1890 → **2171 after deduplication**); this step would take the corpus from roughly 65–70% completeness to a full systematic search. The gaps are systematically in IEEE and engineering venues, quantified in `backward-citation-check.md`.

> ⚠️ **PRESS FIRST:** the librarian (the intended methodologist third author) should audit the six items in the PRESS form below and approve the MeSH-to-Emtree mapping, the wildcards and the field tags **before the institutional search is locked**. Ref 56 (Dysphagia s00455, 2019) is PubMed-indexed and was still missed, so term sensitivity needs PRESS review; the suggested additions are `deglut*`, `penetrat*` and `aspiration`.

---

## Per platform: the string and the export steps

### 1) Scopus (Advanced Search → paste)
```
TITLE-ABS-KEY ( dysphagia OR deglutition OR swallow* OR aspiration OR penetrat* )
AND TITLE-ABS-KEY ( "artificial intelligence" OR "machine learning" OR "deep learning"
 OR "neural network*" OR "deep neural" OR convolutional OR transformer* OR "random forest"
 OR "support vector" OR radiomics OR "computer-aided" OR "computer aided" OR "automated classification"
 OR "automatic detection" OR "predictive model" )
AND PUBYEAR > 2009 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
```
**Export:** select all → Export → **CSV** (or RIS) → all fields (citation information, abstract, keywords) → `search-results/scopus-records.csv`.

### 2) Web of Science Core Collection (Advanced Search → TS=Topic)
```
TS=( (dysphagia OR deglutition OR swallow* OR aspiration OR penetrat*)
 AND ("artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network*"
 OR convolutional OR transformer* OR "random forest" OR "support vector" OR radiomics
 OR "computer-aided" OR "computer aided") )
```
Timespan **2010–2026** · Indexes: **SCI-EXPANDED, ESCI** (plus CPCI-S for conferences).
**Export:** Records → **tab-delimited** or RIS, "Full Record" → `search-results/wos-records.txt`.

### 3) IEEE Xplore (Command Search — the computer-science and engineering venues are critical)
```
("All Metadata":dysphagia OR "All Metadata":deglutition OR "All Metadata":swallow*
 OR "All Metadata":aspiration)
AND ("All Metadata":"artificial intelligence" OR "All Metadata":"machine learning"
 OR "All Metadata":"deep learning" OR "All Metadata":"neural network"
 OR "All Metadata":convolutional OR "All Metadata":transformer OR "All Metadata":radiomics
 OR "All Metadata":"computer-aided")
```
Filter: **2010–2026**. **Export:** Results → Download → **CSV (citation and abstract)** → `search-results/ieee-records.csv`.

### 4) Embase (Emtree plus .tw. — the librarian verifies the Emtree terms)
```
('dysphagia'/exp OR dysphagia:ti,ab,kw OR deglutition:ti,ab,kw OR swallow*:ti,ab,kw
 OR aspiration:ti,ab,kw)
AND ('artificial intelligence'/exp OR 'machine learning'/exp OR 'deep learning':ti,ab,kw
 OR 'convolutional neural network'/exp OR 'neural network*':ti,ab,kw OR transformer*:ti,ab,kw
 OR 'random forest':ti,ab,kw OR 'support vector machine'/exp OR radiomics:ti,ab,kw
 OR 'computer aided':ti,ab,kw)
AND [2010-2026]/py
```
**Export:** select all → Export → **RIS or CSV**, "Full record" → `search-results/embase-records.ris`.

### 5) ACM Digital Library (optional, for computer-science breadth)
```
[[All: dysphagia] OR [All: deglutition] OR [All: swallow*]]
AND [[All: "machine learning"] OR [All: "deep learning"] OR [All: "neural network"]
 OR [All: "artificial intelligence"] OR [All: convolutional]]
```
Publication date: **2010–2026**. **Export:** → **BibTeX or CSV** → `search-results/acm-records.bib`.

---

## PRESS 2015 — librarian audit form (six items)

| # | PRESS item | Current state / librarian approval |
|---|---|---|
| 1 | **Translation of research question** | The dysphagia concept AND the AI concept AND 2010–2026; confirm alignment with the PCC |
| 2 | **Boolean and proximity operators** | The AND/OR structure; are the wildcard (`*`) and the field tag (tiab / TS / .tw. / All Metadata) correct on each platform? |
| 3 | **Subject headings** | Is the mapping between MeSH `Deglutition Disorders` and `Artificial Intelligence` and Emtree `dysphagia/exp` and `machine learning/exp` complete? Any missing heading? |
| 4 | **Text-word searching** | Are `swallow*`, `deglut*`, `neural network*` and `transformer*` sufficient? **Suggested additions:** `penetrat*`, `aspiration`, `auscultation`, `videofluoroscop*`, `endoscop*` for modality sensitivity |
| 5 | **Spelling, syntax, line numbers** | Is the syntax free of errors on each platform; are quotation marks and parentheses balanced? |
| 6 | **Limits and filters** | Years 2010–2026; **do not apply the language filter at the search level** — apply it at screening, to avoid losing records; document type includes conference papers |

**A known gap to fix:** ref 56 (Dysphagia 2019, s00455) is PubMed-indexed and was still missed, so item 4 text-word sensitivity should be increased. **PRESS output:** the approved final strings plus a PRISMA-S search-reporting supplement.

---

## Merge workflow (after the institutional exports arrive)

1. Place the exports in the search-results folder under the names given above.
2. Normalize each source to the common schema (doi, pmid, title, year, venue, source), following the existing `01_*` and combined-corpus pipeline; add a small parser for each new source.
3. **Merge and deduplicate** against `combined-corpus.csv` (normalized title plus DOI), flagging new records as `source=scopus|wos|ieee|embase|acm`.
4. Add the **9 backward-citation absences** (`backward-citation-additions.csv`, DOIs verified) as `source=backward_citation`, forming the "other methods" arm.
5. Re-run `04_prisma_counts.py` for real identification and deduplication counts.
6. Load into Rayyan or Covidence for **dual independent screening**.

> **Expectation:** the institutional search would mainly add computer-science and engineering records from IEEE and Scopus, which the open APIs miss. The net number of new unique records is probably a few hundred; the real value is **stability of the denominator**.
