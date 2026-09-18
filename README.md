# Dysphagia & Swallowing AI — Reproducibility Audit (research artifacts)

Reproducibility artifacts for the meta-research study
*"Available but not runnable out of the box: execution prerequisites and label reporting in shared dysphagia and swallowing AI code."*
The protocol in `protocol/` keeps the working title it was written under.

We audited whether published swallowing/dysphagia-AI code is not just **available** but **re-runnable**, and we release the full measurement pipeline so that the audit is itself reproducible — *we practice what we audit*.

## What is here

| Folder | Contents |
|---|---|
| `scripts/` | Discovery, intake, and analysis scripts, numbered **01–34**: multi-source open-API search & enrichment (01–06), repository discovery / intake / code-link mining / census synthesis (07–10), the blind screening-reliability re-coding (11), post-hoc robustness checks (12–18: search-truncation measurement, backward-citation coverage, reference audit, DOI verification, and verification of every reference's full author list against Crossref), the measurement scripts behind the headline (19 environment pinning and portability, 20 run instructions, 21 re-derivation of every reported number, 23 the usable-sample-data audit), and 24, which turns the clinical coding into one row per study per item with the basis recorded for each. `paths.py` resolves inputs for both this archive and the authors' working tree. Scripts **25–30** were added after a pre-submission review and carry the provenance the first release lacked: the commit each audited repository pointed at on its access date (25), the depositor's published checksum for the external weight archive (26), a re-reading of every intake signal at those commits (27), the screening sensitivity in the direction the disagreements point (28), the publication-confirmed subset (29), and the journal-policy, availability-statement and observed-artifact mapping for the studies where a policy applies (30). Scripts **31–34** were added after a second pre-submission review: strata, joint signal patterns and corrected denominators (31), a re-issue of the code-link mining extraction without its de-duplication step (32), and two checks that need Docker, an as-declared install of every environment file that was never built, followed by `pip check` and an import of each declared distribution (33), and a comparison of one shipped model's predictions across the library versions recorded in its file and those an unpinned install resolved to (34). Statistics are fixed-seed and standard-library only (Wilson and Newcombe intervals, Cohen's κ with BCa bootstrap intervals at 2,000 resamples alongside the plain percentile interval, prevalence- and bias-adjusted κ, and positive/negative specific agreement). |
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

**Docker checks.** Scripts 33 and 34 need Docker and network access and are not run by
`scripts/reproduce.py`. Script 33 installs each declared environment file at the commit recorded in
`results/commit-provenance.json`; script 34 fetches one shipped model and its input spreadsheet from
the recorded commit, which this archive does not redistribute. Their Dockerfiles, probe and logs are
under `re-execution/logs/install-checks/` and `re-execution/logs/silent-drift/`, and base images are
recorded by digest. An install re-run on another day reads the package index of that day, so
unpinned dependencies may resolve differently.

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
the most recent release. **v1.1.6 is the current release and the one the article reports**; its
version DOI is [10.5281/zenodo.22821000](https://doi.org/10.5281/zenodo.22821000), recorded here after the
release because a release cannot contain the DOI minted for it, so the copy inside v1.1.6 itself
does not carry it. v1.1.5 is
[10.5281/zenodo.22819445](https://doi.org/10.5281/zenodo.22819445), superseded and not
withdrawn. v1.1.4 is
[10.5281/zenodo.22813553](https://doi.org/10.5281/zenodo.22813553), superseded and not
withdrawn. v1.1.3 is [10.5281/zenodo.22071534](https://doi.org/10.5281/zenodo.22071534),
superseded and not withdrawn. v1.1.2 is
[10.5281/zenodo.22069521](https://doi.org/10.5281/zenodo.22069521), minted when the release
was published and therefore recorded here from v1.1.3 onward rather than inside v1.1.2
itself. Earlier version DOIs:
v1.1.1 is [10.5281/zenodo.22068273](https://doi.org/10.5281/zenodo.22068273); v1.1.0 is
[10.5281/zenodo.22054994](https://doi.org/10.5281/zenodo.22054994); both are superseded and
neither is withdrawn. v1.0.0 is
[10.5281/zenodo.21629517](https://doi.org/10.5281/zenodo.21629517), which predates the
protocol document and the self-audit checklist and should not be cited for them.

- **v1.1.6** — counts the release whose codes come from an accepted manuscript. One audited
  release has no open published version, and its codes were assigned from the version its authors
  deposited in an institutional repository, which the deposit records as the version accepted for
  publication. The row was held outside the clinical denominator while it already carried a
  confirmed absence for label reliability, which the study's own rule does not allow. It is now
  counted, its spectrum cell is filled from the same source, and the denominator moves from six to
  seven with the reliability count from 0 of 5 to 0 of 6, since one release has no rater. Script 21
  now reads that denominator from the coding file instead of printing it as a constant. Two
  documents are brought up to the counts the article reports: the recommendation set still carried
  the sample data count from before the rule was corrected in August, and the July intake log
  presented its figures as current and now says what superseded them. No other number changes.
- **v1.1.5** — corrects the sensitivity bounds and two location pointers. Script 31 derived the
  point shifts of the screening sensitivity from figures that had already been rounded, which
  moved two of them by 0.1 point, and reported the largest increase only over the signals with a
  nonzero count, leaving out the larger shift a zero row can take. Both bounds are now computed
  from the exact fractions and rounded away from zero, and the increase over every signal is
  recorded beside the earlier figure. In the adapted reporting checklist, the item on unadjusted
  estimates pointed only at the footnote that explains the row given without an interval, and the
  funding item named only the title page heading. No other number changes.
- **v1.1.4** — adds what a second pre-submission review asked for and corrects what it found.
  Script 30 (version 2) corrects the journal-policy mapping, 31 computes strata, joint patterns
  and corrected denominators, and 32 re-issues the code-link mining extraction without its
  de-duplication step. Scripts 33 and 34 need Docker: the environment files that were never
  built were put through an as-declared install (3 of 4 repositories installed with a clean `pip check` and
  loadable imports; Video-SwinUNet failed at the first line of its requirements file), and the
  one shipped model that loaded in July gave identical predictions on all 2,002 scored inputs
  under the library versions recorded in its file and under those its unpinned install resolved
  to. Wording that implied a rule stated in advance, and earlier descriptions of the
  pre-submission review as external review, are corrected. Every number reported before this
  release is unchanged except the policy mapping.
- **v1.1.3** — adds the provenance the earlier releases lacked (scripts 25–30): the commit each
  audited repository pointed at on its access date, recovered for 22 of 23 rows (the exception is
  an empty repository, which has no commit); the depositor's checksum for the external weight
  archive; a re-reading of every intake signal at those commits, which reproduced all 20 scripted
  intake rows; the screening sensitivity in the direction the disagreements point; the
  publication-confirmed subset; and the mapping of journal policy to printed statement to observed
  artifact.
- **v1.1.2** — corrective; the analysis, the data and every reported number are unchanged.
  The protocol's remaining-steps line still listed notifying the authors of the audited
  repositories as a step, contradicting the ethics paragraph of the same document, which
  states that they are not notified. No notification round was carried out, and the
  manuscript and the self-audit checklist both record that item as not met. The earlier
  wording is quoted in place rather than deleted. `CITATION.cff`, which still declared
  v1.1.0 and had never recorded the version DOIs minted for v1.1.0 and v1.1.1, is brought
  up to date.
- **v1.1.1** — corrective; four files described a personal relationship between the two
  authors, which is not an interest in the audited subject matter and is no longer stated.
  The methodological facts that were doing the work remain: the primary measurements are
  script-derived, and the exploratory clinical axis was coded by one clinician with no
  second coder. The article title is corrected in every file that repeats it.
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
  (PROSPERO does not accept this design; see the design details in the article's methods supplement).

---
*Environment for the re-execution harness: CPU-only, 32 GB RAM, 16 cores, Docker. All analysis is reproducible as a frozen-snapshot-plus-fixed-seed pipeline.*
