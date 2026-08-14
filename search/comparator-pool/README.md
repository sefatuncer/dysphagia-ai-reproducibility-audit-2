# Comparator pool — the 83 records behind the coverage bound

These two files are the input to `scripts/13_backward_coverage.py`. They define
the comparator pool used for two numbers in the manuscript: the coverage bound
(how many in-scope repositories the three discovery channels missed) and the
first code-sharing rate reported for this literature.

| File | What it is | Rows |
|---|---|---|
| `kwok-24-matches.csv` | The 24 studies **included** by the dysphagia-screening systematic review (Kwok et al.), matched to our corpus | 24 |
| `codas-matches.csv` | The **reference list** of the AI-in-dysphagia scoping review (CoDAS), matched to our corpus | 64 |

De-duplicated, the two give **83 unique DOIs**.

## The pool is not a curated set of AI studies, and this matters

Only `kwok-24-matches.csv` is a curated included-study set. `codas-matches.csv`
is a bibliography, so it contains record types for which "did this study share a
repository?" is not a well-posed question — reporting guidelines, narrative
reviews, clinical papers with no computational model. Those records stay in the
denominator of the published rate, which therefore understates sharing among
studies that actually present a model.

Two further limits on the same number:

- **"Assessable" means PMC-indexed.** Full text could not be retrieved for 44 of
  the 83 records, and every one of those was excluded for the same reason: no PMC
  identifier. The unreadable half is not a random half. It is richer in
  engineering venues, where code sharing is most common, so the direction of the
  bias is downward.
- **The check is blind in the same way the channels are.** It mines full texts
  with the same expression and tool denylist as the discovery channel it is meant
  to validate, so a repository that channel cannot see is one this check cannot
  see either. Both the miss rate and the sharing rate are therefore lower bounds,
  not estimates.

## Columns

`kwok-24-matches.csv`: `ref` (reference number in the source review), `author`,
`year`, `doi`, `pmid`, `in_corpus` (whether the record appears in our own
discovery corpus).

`codas-matches.csv`: `doi`, `in_corpus`, `ai_dysphagia_gap` (whether the record
falls in the AI-in-dysphagia scope), `ctx` (the citation string as printed in the
source review, kept so each match can be checked by eye).

The DOIs and citation strings are third-party bibliographic data; see
`../corpus-metadata/README.md` for the licence position on that. The `in_corpus`
and `ai_dysphagia_gap` columns are our own coding.
