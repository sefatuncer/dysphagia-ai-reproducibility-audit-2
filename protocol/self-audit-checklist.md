# Minimum-reporting checklist, applied to this study

No EQUATOR reporting guideline fits a meta-research execution-prerequisite audit
with an embedded re-execution case series, and the manuscript says so rather than
claiming conformance to one that does not apply. This file closes that gap in the
only way that is consistent with the paper's own argument: we take the
minimum-reporting recommendation set the study proposes and apply it to the study
itself, item by item, with a pointer to where each item is met.

Every "where" below resolves either to a section of the manuscript or to a file in
this archive. Nothing is marked met on the strength of an intention.

## A. Execution prerequisites (the four conjuncts the paper measures)

| # | Item | Status | Where |
|---|---|---|---|
| A1 | Pinned environment for the analysis code | **Met** | Analysis scripts are standard-library only, with no third-party dependency to pin. Stated in `README.md`; the re-execution harness ships its own `Dockerfile` templates in `re-execution/harness/`. |
| A2 | Trained weights archived with a persistent DOI | **Not applicable** | This study trains no model. No weights exist to archive. |
| A3 | Runnable sample with expected output | **Met, with one qualification** | `python scripts/reproduce.py`, run from the archive root, re-runs the offline analysis and checks it against the published `results/`. The offline steps (11, 21) reproduce their outputs exactly. Scripts 12, 13, 19 and 20 read live repository and database state over the network and each records an access date: re-running them later may legitimately return a different answer, which is the same drift the manuscript reports for the discovery APIs, so `reproduce.py` runs them only under `--with-network` and reports a difference as a difference rather than a failure. *Correction (v1.1.0): an earlier build of this archive failed this item outright — the scripts resolved their inputs relative to the authors' working tree and to file names that the English translation had changed, so none of them ran from inside the archive. `scripts/paths.py` now resolves both layouts and a missing input stops the run instead of being skipped. We record the failure rather than quietly fixing it, because it is exactly the defect this audit measures in others.* |
| A4 | Open license | **Met** | Dual: MIT for code (`LICENSE-CODE`), CC-BY-4.0 for data and text (`LICENSE-DATA`). |

## B. Provenance and reproducibility of the measurement

| # | Item | Status | Where |
|---|---|---|---|
| B1 | Inclusion rule stated before the reader sees the results | **Met** | Manuscript §2.2; `protocol/protocol.md`. No registry entry was made, and the manuscript gives the reason rather than implying one exists. *Correction (v1.1.0): `transparency/statistical-analysis-plan.md` described itself as "locked before any outcome data were seen". The manuscript claims the opposite — the protocol is a dated record with no claim of temporal priority — so the archive was asserting a priority the study does not have. The line is corrected and the previous wording is quoted in place rather than deleted.* |
| B2 | Full candidate list released, included **and** excluded, with reasons | **Met** | `search/`, plus the inventory and code-mining vetting files. |
| B2b | Every artifact a released document points to is actually in the archive | **Met, after correction** | *Correction (v1.1.0): the VFSS pilot runbook listed a weights checksum and the raw `rerun.log` and `compare.log` among its provenance, and the crash-findings file told the reader to "see compare.log". None of the three is in the archive — a document resolving to an artifact that is not there, which is the defect this study measures in others. The runbook now lists what is published and states plainly what is not: no checksum was recorded for the 6.1 GB weights download, so a third party can repeat the run and reach the same verdict but cannot verify bit-identity with the file we downloaded.* |
| B3 | Raw discovery-API responses archived, date-stamped | **Partially met** | `search/corpus-metadata/` releases the record-level bibliographic metadata for every retrieved record, with the verbatim queries and their retrieval dates, so each search can be re-issued. The **raw** responses are deliberately not archived: they carry the abstracts the bibliographic services returned, which are not ours to republish (§Data and code availability). The exclusion is enforced by name in the build script and reported on every build, and the withheld file is named in `search/corpus-metadata/README.md`. The manuscript states that the live APIs drift and that re-running discovery later may surface a different pool. |
| B4 | Analysis deterministic and re-runnable | **Met** | All reported proportions come from released scripts over the frozen, date-stamped extract and involve no randomness. The one resampling procedure, the bootstrap interval for κ in script 11, carries a fixed seed released with it. |
| B5 | Verdict definitions pre-stated, not fitted after the fact | **Met** | Manuscript §2.6. Four mutually exclusive verdicts with explicit criteria. |
| B6 | Observed failures kept distinct from inferred ones | **Met** | Manuscript §2.6 and §3.3. The 15 not-attemptable verdicts are never merged with the 1 observed build failure. |
| B7 | Reliability of the one subjective step measured and released | **Met** | Blind rule-based re-coding of all 181 screened records, full contingency tables, both rule versions. |
| B8 | Mid-course changes to the method disclosed with their effect | **Met** | The screening rule was revised after its first run; the manuscript reports the revision and its numerical effect (κ 0.49 → 0.79 on the mining channel). |
| B9 | Sensitivity analyses for the discovery limitations | **Met** | Two: excluding the two non-scripted repositories (0/16 unchanged), and full-pagination re-run of every GitHub term (the per-term cutoff never bound). |

## C. Reporting honesty

| # | Item | Status | Where |
|---|---|---|---|
| C1 | Denominators stated explicitly; "not reported" never imputed | **Met** | Manuscript §2.7. |
| C2 | Interval estimates interpreted in line with the sampling design | **Met** | Wilson intervals reported as small-sample fragility bands, not as inference to the wider literature. |
| C3 | Clustering acknowledged and handled | **Met** | Study level primary; repository level reported as sensitivity and explicitly not corrected for within-team clustering. |
| C4 | Registration timing stated without over-claiming | **Met** | The protocol is publicly posted and transparently dated. The manuscript makes **no** claim of temporal precedence over the analysis. |
| C5 | Competing interests disclosed, including non-financial ones | **Met** | The two joint first authors are married; declared. |
| C6 | Generative-AI use disclosed, separating method use from writing use | **Met** | Declaration section. |
| C7 | Named third parties notified and offered a right to respond | **Human step, before submission** | Template and recipient list in the manuscript repository. To be dated in §Ethics at submission. |

## D. Clinical axis

| # | Item | Status | Where |
|---|---|---|---|
| D1 | Reference-standard type stated per study | **Met (k=6)** | `transparency/rs-taxonomy-coding.csv`; manuscript Table 5. The instrument itself is published as Table 2. |
| D2 | Label scale and any binarization loss recorded | **Met (k=6)** | Same. |
| D3 | Rater reliability (κ or ICC) recorded, with "not reported" kept distinct from "weak" | **Met (k=6)** | Same. This is the item the audited literature fails: 0/6. |
| D4 | Applicable appraisal instrument named, without producing an unsupported rating | **Met** | Table 5 names the instrument that would apply and states that no formal QUADAS-2 or PROBAST+AI assessment was produced. |
| D5 | Which studies are in which axis, made explicit | **Met** | The k=6 clinical subset is the full-text-accessible subset of the same 18 studies, stated in the Table 5 footnote and in §3.4. Every study in Table 5 is also in the computational set. |

| D6 | Reliability of the clinical coding itself | **Not met** | The RS coding was done by one clinician with no second coder, so it reports no agreement statistic. RS4 asks the audited studies for exactly what this coding does not provide. The manuscript states this in the limitations rather than leaving it for a reader to notice. |

## What this checklist does not claim

It is a self-audit against a recommendation set this study proposes, not
certification against an external standard. The recommendation set has not been
through a consensus process, and we say so in the manuscript. Three items above
are not met by the study text alone: A2 does not apply, C7 is a human step that must
be completed and dated before submission, and D6 is a genuine failure against our own
recommendation set, recorded here rather than omitted.
