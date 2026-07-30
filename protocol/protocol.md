# Study protocol

*Released with the artifact archive (Zenodo concept DOI 10.5281/zenodo.21629516, which
resolves to the most recent version) for the
meta-research audit "Available but not executable: a transparency and
execution-prerequisite audit of open-source dysphagia and swallowing
artificial-intelligence models, with three containerized re-execution case
studies."*

> **On timing.** This is a dated record of the inclusion rule, rubric and analysis
> plan, released so that both can be audited against what was actually done. **We
> make no claim that it predates the analysis**, and the manuscript says so in the
> same terms. The study is not registered on a registry platform: PROSPERO does not
> accept meta-research designs, and a registration created after the analysis would
> add a label without adding evidence. The immutable, dated record is the archive
> itself.


**Title:** Available but not executable: a transparency and execution-prerequisite audit of open-source dysphagia and swallowing artificial-intelligence models, with three containerized re-execution case studies


**Contributors / roles:** Sefa Tunçer, PhD — Independent Researcher, Ankara, Türkiye; ORCID 0000-0001-6672-3605; tuncersefa@gmail.com (joint first; reproducibility and software, discovery, intake, analysis, re-execution). Nazife Kapan Tunçer, MD — Department of Physical Medicine and Rehabilitation, Faculty of Medicine, Kırşehir Ahi Evran University, Kırşehir, Türkiye; ORCID 0000-0002-8161-5669 (joint first; clinical validity, RS1–RS6 reference-standard and label appraisal). The candidate pool is machine-generated, and scope and borderline decisions are author judgments applied to a pre-stated rule and released in full for audit. **The two joint first authors are married; this is declared in the manuscript and the primary measurements are script-derived.**

**Description (summary):** We measure whether AI models for dysphagia and swallowing can actually be re-run from their published code, the downstream question beyond code availability. By an objective, machine-checkable inclusion (a public, resolvable code repository), we discover the code-available literature reproducibly, record objective transparency signals, and re-execute each repository in clean CPU Docker containers against a fixed barrier taxonomy, together with a dysphagia-specific reference-standard and label-quality lens (RS1–RS6). Prior dysphagia reviews assessed methodological quality (Kwok, JMIR 2025;e65551) or algorithm maps (CoDAS 2025;e20240305) only. Executability has not been measured.

**Research questions:** RQ1 transparency proportions (license, weights in-repo/anywhere, environment, sample data, run instructions) among code-available repositories; RQ2 out-of-the-box re-executability in a clean CPU container + barrier taxonomy; RQ3 reference-standard validity, label quality, spectrum (clinical reproducibility, RS1–RS6).

**Study design:** Meta-research **re-execution study** (NOT a systematic review; no PRISMA-ScR claim). No human participants/new data → ethics-exempt.

**Eligibility (objective inclusion):** A work is included if it (i) implements AI/ML/DL for dysphagia/swallowing (diagnosis/screening/assessment/severity/rehab-monitoring, any modality), (ii) has a public, resolvable code repository (GitHub/GitLab/Zenodo/OSF), which is machine-checkable, and (iii) is dated 2010–2026. Exclude: personal/learning repos with no study; exact duplicates/variants (grouped at study level); no computational model.

**Discovery (reproducible, no paywall):** Three released channels: GitHub Search API and Papers with Code API (`07_repo_discovery.py`), and open-access full-text code-link mining via the NCBI BioC service (`10_code_link_mining.py`), de-duplicated by repository, plus code-available repositories carried forward from two feasibility pilots. The census assessed 22 code-available repositories corresponding to 18 distinct studies (same-team variants grouped at the study level). Reported as a transparent, re-runnable pipeline, not an exhaustive systematic search; residual repositories are a stated limitation.

**Intake & re-execution:** Objective intake (`08_repo_intake.py`: git tree + releases + README, access date logged) records license/weights/environment/data/run-instructions. Census re-execution in clean CPU Docker: as-declared build → best-effort fixes (friction taxonomy) → CPU inference where data present → verdict (re-executable/partial/not-reproduced/not-attemptable). Hardware-neutral vs GPU-only separated.

**Analysis plan:** Transparency proportions with Wilson 95% CIs (`09_census_synthesis.py`); "not reported" = distinct category (no imputation); estimation study (no confirmatory testing → no multiplicity; census → no a priori power). Study level (N=18, same-team variants grouped) is primary; repository level (N=22) is a sensitivity view and is not corrected for within-team clustering. Re-execution = descriptive verdict counts + barrier frequencies (NOT a rate over all studies; denominator = code-available set). All figures from released fixed-seed scripts.

**Screening reliability:** The one subjective step (the scope decision) is checked by a released, blind, rule-based re-coding of every screened record from both scripted channels (`11_screening_kappa.py`, n=181), reporting the full 2×2, simple agreement, Cohen's κ, PABAK, and positive/negative specific agreement, per channel and pooled. This is an automated check, reported as such, not a second human reader. Two rule versions are implemented and both are reported, because the rule was revised after its first run (the revision raises κ on the mining channel from 0.49 to 0.79).

**Timing and disclosure (transparency):** We make no claim that this document predates the analysis. It is a transparently dated record of the objective inclusion rule, rubric, and analysis plan, posted for audit. At the time of writing we had already completed the reproducible discovery and objective intake of the code-available set, the census re-execution (including three in-depth case studies: VFSS_analysis, masa-open-source, and enoch0307), and a first-pass RS1–RS6 clinical coding. The clinical author finalizes the interpretive RS columns.

**Ethics:** Published literature + public repositories only; no human participants or newly collected/identifiable data, so ethics-committee review was not required. **Consistent with the manuscript, no ethics submission and no formal non-human-subjects determination was sought, and we state this explicitly in lieu of an approval number.** *(This wording is identical to the ethics section of the manuscript. Should an institutional exemption letter be obtained later, this document and the manuscript are to be amended together, so that the two never diverge.)* Data governance: artifacts used within original licenses; where a repository carried no license (15/18) we relied only on local, non-distributive use and claim no general research-use exemption; no re-identification; no redistribution of third-party code/weights/human-derived data. Authors of audited repositories are notified before publication and offered a right to respond (COPE).

**Archive:** This document is released as part of the artifact archive on Zenodo, alongside the
scripts, rubric, codebook and re-execution logs it describes. It first appears in release
v1.1.0; the first release, v1.0.0, is DOI 10.5281/zenodo.21629517 and predates this document.
The concept DOI 10.5281/zenodo.21629516 covers all versions and resolves to the most recent
one; cite it, or the version DOI of the release you are actually reading.

**Remaining steps:** finalize the RS1–RS6 clinical sign-off → notify the authors of the audited
repositories and offer a right to respond → submit. No external registry entry is made; §2.1 of
the manuscript gives the reason.


---
