# Census intake findings — code-available swallowing-AI repositories (objective, re-execution centred)

> ## ⬆️ v2 UPDATE (16 July, after code-link mining; THIS SECTION IS CURRENT)
> The v1 section below describes **N=17**. Script 10 (code-link mining over open-access full texts) added **5 in-scope repositories**, taking the census from **17 to 22 repositories covering 18 distinct studies** (clustering: scut-jol ×2, tsukagoshi ×3, Yash and Tanishq ×2). Details in `code-mining-vetting.md`. **The primary level is the study (N=18); the repository level (N=22) is reported as sensitivity, and the two agree.**
> - **Current study-level figures (Wilson 95% intervals):** open license **3/18** [0.06, 0.39] · weights **in the repository** **1/18** [0.01, 0.26] · weights including external hosting **2/18** [0.03, 0.33] · environment file **6/18** [0.16, 0.56] · example data **4/18** [0.09, 0.45] · **inference attemptable 2/18** [0.03, 0.33] · **re-executable out of the box 0/18** [upper bound 0.18].
> - **Verdicts:** re_executable **0**, partial **2** (VFSS_analysis and the actual re-run of **enoch0307**, in `C-repo-003-enoch0307/`), not_reproduced **1** (masa: a build was attempted and observed to fail), not_attemptable **15** at study level (0 / 2 / 1 / 19 at repository level). The build stage and the inference stage are reported separately for masa and are not merged: its build failure was observed, while its inference was never reachable.
> - **enoch0307 (case #3):** the only repository that deposits its weights (`Binary.pkl`, `Multi.pkl`) still crashes out of the box, because the environment is unpinned (sklearn 1.6.1 → 1.9.0 gives `ModuleNotFoundError: _loss` on `Multi.pkl`); one pin makes it run, hence **partial**. Verified in both an actual Docker container and a virtual environment, across platforms.
> - **The clinical second axis:** RS1–RS6 were applied (`rs-taxonomy-coding.csv`) → **0/6 of the full-text-accessible studies report rater κ or ICC**, and the reference standards are heterogeneous proxies → **the combined thesis: computational and clinical provenance are both missing.** The remaining 12 studies have no retrievable full text and are coded *not assessable*; the finding is **not** extrapolated to 18.

---

## (v1 — N=17, historical; the v2 section above supersedes it)

**Date of access:** 2026-07-16 · **Method:** reproducible discovery (`07_repo_discovery.py`: GitHub plus Papers with Code) → objective inclusion (`repo-inventory.csv`) → objective intake (`08_repo_intake.py`: git tree, releases, and a README scan for externally hosted weights). **No subjective screening.**

## Scope of the census
- Discovery: a multi-term GitHub search returned **18 raw candidates**, plus Video-SwinUNet from scoping and the 2 pilots (VFSS_analysis, masa).
- Excluded: `excluded-personal-01` (not a study). Deduplication: SheenZhang721 ×2 is the same study as MinghaoSam MICCAI 2024; tsukagoshi56 ×3, scut-jol ×2 and YashC1308 with TanishqJoshi are within-group variants.
- **Taken to intake: 15 repositories** (excluding the pilots and duplicates), plus **2 pilots re-run in depth**.

## Objective transparency signals (the 15 intake repositories)
| Signal | Result | Rate |
|---|---|---|
| **Trained weights in the repository** (*.pt / pth / h5 / ckpt / onnx …) | **0 / 15** | 0% |
| **Weights as a release asset** | **0 / 15** | 0% |
| **Open license** (OSI or present) | **1 / 15** (MinghaoSam, MIT) | 7% |
| **Environment file** (requirements / Dockerfile / environment.yml) | **4 / 15** (aht4005, tsukagoshi/liquid, tsukagoshi/ssl_gru, Video-SwinUNet) | 27% |
| **Externally hosted weights linked from the README** | Video-SwinUNet (Google Drive); the "pretrained/checkpoint" in zhengfj1994 is a **resume or backbone file**, not shipped weights | approximately 0 |
| **Inference ATTEMPTABLE out of the box** | **0 / 15** (no weights and no data) | 0% |

## Pilots (re-run in depth, reported separately)
- **VFSS_analysis** (Cubero, Comput Biol Med 2025): the **only** repository that supplied weights (Zenodo, 6.1 GB, CC-BY) together with example data, so inference was attemptable → **partial** (crashed out of the box, then ran after 5 repairs; structurally identical output, numerically partial). No license.
- **masa** (Saab, Front Neurosci 2023): a non-portable local-path wheel gives **not_re_executable** for the environment; no weights and no data give **not_attemptable** for inference. A license is present.

## HEADLINE (objective)
> **Of 17 code-available swallowing-AI repositories (15 from discovery plus 2 pilots), only one (VFSS_analysis) supplied both the trained weights and the example data needed to run its model — and even that one did not run out of the box (5 repairs → partial). No repository placed weights in the repository or in its releases; one hosted them in an external archive. A license was absent in roughly 15 of 17, and an environment specification in roughly 12 of 17.**
>
> The effective computational reproducibility of the code-available swallowing-AI literature is therefore **approximately zero out of the box** — not because the code fails, but because **trained weights, data and licenses are systematically missing**. This quantifies the **gap** between code sharing, meaning that a URL resolves, and re-executability, meaning that the artifact actually runs.

## Barrier taxonomy (frequency across the census)
| Barrier | Frequency (of 17) |
|---|---|
| **missing_weights** (no trained weights) | 16/17 (all but VFSS) |
| **absent_license** | approximately 15/17 |
| **missing_data** (no example or test data; most are confidential) | approximately 15/17 |
| **env_undeclared** (no environment file) | approximately 12/17 |
| **GPU-oriented** (3D CNN, video, segmentation) | the majority. On the hardware-neutral distinction: the absence of weights is a barrier that precedes hardware entirely |
| dep_conflict / hardcoded_local_path / NameError | in the pilots (VFSS: dependency conflict, NameError, missing post-processing; masa: a non-portable wheel) |

## Notes on honesty
- "not_attemptable (inference)" means that **inference cannot be attempted** without weights and data. Some of these models could be **retrained**, given confidential data and a GPU, but that is out of scope here.
- Intake scanned the git tree, the releases and the README for external hosting; **live Google Drive links were not verified by hand** (Video-SwinUNet). Verifying one or two external hosts would not change the census headline.
- Study-level deduplication of within-group variants is applied at synthesis, and the repository-level and study-level N are reported separately.
