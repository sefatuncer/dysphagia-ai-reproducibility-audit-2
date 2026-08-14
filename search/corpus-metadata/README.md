# Third-party bibliographic metadata — provenance and terms

**These files are not ours to relicense.** The CC BY 4.0 grant in `LICENSE-DATA`
covers the artifacts the authors produced. It does **not** cover this directory,
which redistributes record-level bibliographic metadata retrieved from public
discovery services. Those records remain under the terms of the service each one
came from, and the authors are in no position to place them under a different
licence.

## What is here, and where it came from

| File | Source service | Retrieved | Fields |
|---|---|---|---|
| `europepmc-records.csv` | Europe PMC REST API | 13 July 2026 | `source,id,doi,pmid,year,venue,title` |
| `openalex-records.csv` | OpenAlex API | 13 July 2026 | `source,id,doi,pmid,year,venue,title` |
| `semanticscholar-records.csv` | Semantic Scholar API | 13 July 2026 | `source,id,doi,pmid,year,venue,title` |
| `pubmed-metadata.csv` | NCBI E-utilities (PubMed) | 13 July 2026 | `pmid,year,journal,pubtype,title,include_screen1,exclude_reason` |
| `combined-corpus.csv` | de-duplicated union of the above | 13 July 2026 | adds `dedup_key,sources,n_sources,likely_review,likely_cancer_rt` |
| `backward-citation-additions.csv` | records added by backward citation checking | 16 July 2026 | `doi,from_review,source,year,venue,title,include_screen1,exclude_reason` |

The `include_screen1` and `exclude_reason` columns are **our** screening
decisions recorded against third-party records. Those two columns are authored by
us and fall under `LICENSE-DATA`; the bibliographic fields do not.

## What is deliberately absent

The enriched corpus used during screening carries an `abstract` column populated
from the bibliographic services. **It is not published here.** Abstracts are
third-party content that we are not in a position to republish, and the
manuscript states this in §Data and code availability.

The exclusion is enforced by name in `RELEASE/build-archive.ps1` (`$script:blocked`)
and reported at the end of every build run, so that the guarantee comes from a
stated rule rather than from a file-size threshold that could change.

## Reissuing the searches instead

Because the queries and their retrieval dates are released in full
(`search/pubmed-search-record.md`, `search/institutional-search-strings.md`, and
the query strings inside `scripts/01_enrich_epmc.py`, `01b_enrich_openalex.py`
and `07_repo_discovery.py`), each search can be re-issued against the same
services rather than taken on trust from this snapshot. Re-issuing today will
return more records than the frozen extract: the extract is dated, the databases
are not.
