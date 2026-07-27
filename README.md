# Dysphagia & Swallowing AI — Reproducibility Audit (research artifacts)

Reproducibility artifacts for the meta-research study
*"Available but not executable: a transparency audit and containerized re-execution of open-source artificial-intelligence models for dysphagia and swallowing."*

We audited whether published swallowing/dysphagia-AI code is not just **available** but **re-runnable**, and we release the full measurement pipeline so that the audit is itself reproducible — *we practice what we audit*.

## What is here

| Folder | Contents |
|---|---|
| `scripts/` | Discovery, intake, and analysis scripts, numbered **01–11**: multi-source open-API search & enrichment (01–06), repository discovery / intake / code-link mining / census synthesis (07–10), and the blind screening-reliability re-coding (11). Statistics are fixed-seed and standard-library only (Wilson & Newcombe intervals, Cohen's κ with bootstrap). |
| `transparency/` | Transparency rubric + blank template, codebook, coding guide, the **RS1–RS6** clinical reference-standard taxonomy and its coding, and the statistical analysis plan. |
| `re-execution/` | The containerized re-execution harness (Dockerfile template, intake & verdict templates), the VFSS pilot write-up, and per-repository build/run logs and verdicts for the attempted case studies. |
| `protocol/` | OSF protocol, PRISMA-ScR checklist (transparently declined, with rationale), and the minimum-reporting recommendation set. |
| `search/` | Search records, screening form, institutional search strings, backward-citation check, and record-level bibliographic corpus metadata. |

## What is NOT here (non-distributive)

This archive contains only artifacts **the authors produced**. The audited third-party repositories — their code, trained weights, and any human-derived data (e.g. VFSS/FEES) — are **not re-hosted**. Each audited artifact is referenced to its original repository/DOI, and its license is recorded in the corresponding `re-execution/logs/<repo>/verdikt.md`.

## Licensing (dual)

- **Code** (`scripts/`, harness) — **MIT**, see [`LICENSE-CODE`](LICENSE-CODE).
- **Data & text** (rubric, codebook, taxonomy, logs, protocol, corpus metadata) — **CC-BY-4.0**, see [`LICENSE-DATA`](LICENSE-DATA).

## Citation

If you use these materials, please cite the article and this archive. The archive DOI is minted by Zenodo on first release (see `CITATION.cff` and the Zenodo record).

## Related identifiers

- **Article:** _DOI to be added on acceptance._
- **OSF protocol:** _DOI to be added._

---
*Environment for the re-execution harness: CPU-only, 32 GB RAM, 16 cores, Docker. All analysis is reproducible as a frozen-snapshot-plus-fixed-seed pipeline.*
