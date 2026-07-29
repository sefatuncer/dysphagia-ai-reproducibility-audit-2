# Dysphagia & Swallowing AI — Reproducibility Audit (research artifacts)

Reproducibility artifacts for the meta-research study
*"Available but not executable: a transparency and execution-prerequisite audit of open-source dysphagia and swallowing artificial-intelligence models, with three containerized re-execution case studies."*

We audited whether published swallowing/dysphagia-AI code is not just **available** but **re-runnable**, and we release the full measurement pipeline so that the audit is itself reproducible — *we practice what we audit*.

## What is here

| Folder | Contents |
|---|---|
| `scripts/` | Discovery, intake, and analysis scripts, numbered **01–18**: multi-source open-API search & enrichment (01–06), repository discovery / intake / code-link mining / census synthesis (07–10), the blind screening-reliability re-coding (11), and post-hoc robustness checks (12–18: search-truncation measurement, backward-citation coverage, reference audit, DOI verification, and verification of every reference's full author list against Crossref). Statistics are fixed-seed and standard-library only (Wilson and Newcombe intervals, Cohen's κ with clipped asymptotic intervals, and positive/negative specific agreement). |
| `transparency/` | Transparency rubric + blank template, codebook, coding guide, the **RS1–RS6** clinical reference-standard taxonomy and its coding, and the statistical analysis plan. |
| `re-execution/` | The containerized re-execution harness (Dockerfile template, intake & verdict templates), the VFSS pilot write-up, and per-repository build/run logs and verdicts for the attempted case studies. |
| `protocol/` | The study protocol (`protocol.md`: inclusion rule, rubric, analysis plan), the PRISMA-ScR checklist (transparently declined, with rationale), the minimum-reporting recommendation set, and `self-audit-checklist.md`, that recommendation set applied item by item to this study itself. |
| `search/` | Search records, screening form, institutional search strings, backward-citation check, and record-level bibliographic corpus metadata. |

## Design history (read this before the `search/` and `transparency/` planning files)

This study began as a systematic-review-style audit and was **redesigned** partway
through into a two-author meta-research re-execution census with an objective,
machine-checkable inclusion criterion. The earlier design assumed dual independent
human screening, a methodologist or health-sciences librarian as a third author,
PRESS review of the search strategy, and institutional database access. **None of
those methodologist-dependent procedures were carried out**, and the published paper
neither claims them nor reports a PRISMA-ScR-conformant search.

The planning documents from that earlier design are kept in this archive rather than
removed, and each carries a banner at the top saying it was planned but not executed
as written. They are here so that the change of plan is auditable instead of
invisible. Where a file is still the live record of what was actually done (the
codebook and the coding guide), the banner is narrower and says only which
provision became obsolete.

What was actually done in place of dual human screening: a blind, rule-based
re-coding of every screened record, released with the analysis code, reported with
its full contingency tables and with the effect of a mid-course revision to the rule
disclosed.

## Language

Every document in this archive is in English. The authors' working copies are in Turkish;
the versions published here were translated once, and the archive is rebuilt from those
English sources, so that a reader or reviewer can verify every coding decision, verdict and
rubric definition directly.

## What is NOT here (non-distributive)

This archive contains only artifacts **the authors produced**. The audited third-party repositories — their code, trained weights, and any human-derived data (e.g. VFSS/FEES) — are **not re-hosted**. Each audited artifact is referenced to its original repository/DOI, and its license is recorded in the corresponding `re-execution/logs/<repo>/verdict.md`.

## Licensing (dual)

- **Code** (`scripts/`, harness) — **MIT**, see [`LICENSE-CODE`](LICENSE-CODE).
- **Data & text** (rubric, codebook, taxonomy, logs, protocol, corpus metadata) — **CC-BY-4.0**, see [`LICENSE-DATA`](LICENSE-DATA).

## Citation

If you use these materials, please cite both the article and this archive. Each release is
archived on Zenodo with its own version DOI; see `CITATION.cff` and the Zenodo record.

## Version history

- **v1.1.0** — adds the dated protocol document and the self-audit checklist the manuscript
  cites as archived; replaces the census-synthesis and screening-reliability scripts with the
  versions that produce the reported figures; adds the post-hoc robustness checks (12–18);
  and translates every document in the archive into English.
- **v1.0.0** — first release, DOI [10.5281/zenodo.21629517](https://doi.org/10.5281/zenodo.21629517).
  Still available; not withdrawn.

## Related identifiers

- **Article:** _DOI to be added on acceptance._
- **Protocol:** no external registration. The protocol is `protocol/protocol.md` in this
  archive, posted as a dated record with no claim of temporal precedence over the analysis
  (PROSPERO does not accept this design; see §2.1 of the article).

---
*Environment for the re-execution harness: CPU-only, 32 GB RAM, 16 cores, Docker. All analysis is reproducible as a frozen-snapshot-plus-fixed-seed pipeline.*
