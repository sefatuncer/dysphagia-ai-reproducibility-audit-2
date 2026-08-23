# Dysphagia & Swallowing AI — Reproducibility Audit (research artifacts)

Reproducibility artifacts for the meta-research study
*"Available but not executable: auditing the execution prerequisites of shared code in dysphagia and swallowing artificial-intelligence
studies."*

We audited whether published swallowing/dysphagia-AI code is not just **available** but **re-runnable**, and we release the full measurement pipeline so that the audit is itself reproducible — *we practice what we audit*.

## What is here

| Folder | Contents |
|---|---|
| `scripts/` | Discovery, intake, and analysis scripts, numbered **01–24**: multi-source open-API search & enrichment (01–06), repository discovery / intake / code-link mining / census synthesis (07–10), the blind screening-reliability re-coding (11), post-hoc robustness checks (12–18: search-truncation measurement, backward-citation coverage, reference audit, DOI verification, and verification of every reference's full author list against Crossref), the measurement scripts behind the headline (19 environment pinning and portability, 20 run instructions, 21 re-derivation of every reported number, 23 the usable-sample-data audit), and 24, which turns the clinical coding into one row per study per item with the basis recorded for each. `paths.py` resolves inputs for both this archive and the authors' working tree. Statistics are fixed-seed and standard-library only (Wilson and Newcombe intervals, Cohen's κ with BCa bootstrap intervals at 2,000 resamples alongside the plain percentile interval, prevalence- and bias-adjusted κ, and positive/negative specific agreement). |
| `transparency/` | Transparency rubric + blank template, codebook, coding guide, the **RS1–RS6** clinical reference-standard taxonomy and its coding, the objective per-repository intake table (the machine-recorded license, environment, weights and data signals behind each verdict), and the statistical analysis plan. |
| `re-execution/` | The containerized re-execution harness (Dockerfile template, intake & verdict templates), the VFSS pilot write-up, and per-repository build/run logs and verdicts for the attempted case studies. |
| `protocol/` | The study protocol (`protocol.md`: inclusion rule, rubric, analysis plan), the PRISMA-ScR checklist (transparently declined, with rationale), the minimum-reporting recommendation set, and `self-audit-checklist.md`, that recommendation set applied item by item to this study itself. |
| `search/` | Search records, screening form, institutional search strings, backward-citation check, record-level bibliographic corpus metadata, and the **candidate-repository inventory** at three stages: raw discovery output, the code-link-mining additions, and the vetted inventory with the inclusion decision and reason for every candidate. |

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

## Running the analysis

Python 3.10+ and the standard library only — there are no third-party dependencies to install.
Run from the archive root:

```bash
python scripts/reproduce.py          # everything below, in order, with a pass/fail summary
```

Or run an individual step:

```bash
python scripts/11_screening_kappa.py       # screening reliability -> results/screening-reliability.json
python scripts/12_truncation_check.py      # search-truncation check (network)
python scripts/13_backward_coverage.py     # coverage bound + sharing rate (network)
python scripts/19_env_pinning_audit.py     # environment pinning x portability (network)
python scripts/20_run_instructions_audit.py # run-instruction signal (network)
python scripts/21_reported_numbers.py      # re-derives every number in the manuscript
```

**Offline vs. network.** Scripts 11 and 21 run entirely from released files and reproduce their
outputs exactly. Scripts 12, 13, 19 and 20 query live services (GitHub, `raw.githubusercontent.com`,
Crossref, Europe PMC) at the access date recorded in each result file. Re-running them today may
return different values, because repositories and databases change; that is a property of what is
being measured, not an error. The values in `results/` are the ones the manuscript reports, each
stamped with the date it was measured.

`scripts/paths.py` resolves input locations, so the same scripts run from this archive and from
the authors' working tree. A missing input stops the run with an error rather than being skipped.

## Language

Every document in this archive is in English. The authors' working copies are in Turkish;
the versions published here were translated once, and the archive is rebuilt from those
English sources, so that a reader or reviewer can verify every coding decision, verdict and
rubric definition directly.

## What is NOT here (non-distributive)

This archive redistributes no third-party **code, trained weights, or human-derived data**. The audited repositories — including any VFSS/FEES material — are **not re-hosted**. Each audited artifact is referenced to its original repository/DOI, and its license is recorded in the corresponding `re-execution/logs/<repo>/verdict.md`.

It does redistribute **record-level bibliographic metadata** from Europe PMC, OpenAlex, Semantic Scholar and PubMed, which is not ours to relicense — see [`search/corpus-metadata/README.md`](search/corpus-metadata/README.md) for per-file provenance, retrieval dates, and terms. It deliberately does **not** redistribute the abstracts those services returned; that exclusion is enforced by name in the build script and reported on every build.

## Licensing (dual)

- **Code** (`scripts/`, harness) — **MIT**, see [`LICENSE-CODE`](LICENSE-CODE).
- **Data & text we produced** (rubric, codebook, taxonomy, logs, protocol, inventories, screening decisions) — **CC-BY-4.0**, see [`LICENSE-DATA`](LICENSE-DATA).
- **Third-party bibliographic metadata** (`search/corpus-metadata/`, and the bibliographic fields in `search/comparator-pool/`) — **not ours to relicense**; remains under the terms of the originating service.

## Citation

If you use these materials, please cite both the article and this archive. Each release is
archived on Zenodo with its own version DOI; the concept DOI
[10.5281/zenodo.21629516](https://doi.org/10.5281/zenodo.21629516) cites all versions and
resolves to the most recent one. See `CITATION.cff` and the Zenodo record.

## Version history

All versions share the concept DOI
[10.5281/zenodo.21629516](https://doi.org/10.5281/zenodo.21629516), which always resolves to
the most recent release. Version DOIs: v1.1.1 is
[10.5281/zenodo.22068273](https://doi.org/10.5281/zenodo.22068273), published 23 August 2026,
and it is the version the article reports; v1.1.0 is
[10.5281/zenodo.22054994](https://doi.org/10.5281/zenodo.22054994), which this release
corrects and which is not withdrawn; v1.0.0 is
[10.5281/zenodo.21629517](https://doi.org/10.5281/zenodo.21629517), which predates the
protocol document and the self-audit checklist and should not be cited for them.

- **v1.1.0** — adds the dated protocol document and the self-audit checklist the manuscript
  cites as archived; replaces the census-synthesis and screening-reliability scripts with the
  versions that produce the reported figures; adds the post-hoc robustness checks (12–18);
  adds three measurement scripts (19–21) that put a released command behind the
  pinned-and-portable environment row, the run-instruction signal (RQ1e) and every reported
  proportion; adds a bootstrap interval and the prevalence and bias indices to the
  screening-reliability output; archives the machine-readable script outputs under
  `results/`; and translates every document in the archive into English.
- **v1.0.0** — first release, DOI [10.5281/zenodo.21629517](https://doi.org/10.5281/zenodo.21629517).
  Still available; not withdrawn.

## Related identifiers

- **Article:** _DOI to be added on acceptance._
- **Protocol:** no external registration. The protocol is `protocol/protocol.md` in this
  archive, posted as a dated record with no claim of temporal precedence over the analysis
  (PROSPERO does not accept this design; see §2.1 of the article).

---
*Environment for the re-execution harness: CPU-only, 32 GB RAM, 16 cores, Docker. All analysis is reproducible as a frozen-snapshot-plus-fixed-seed pipeline.*
