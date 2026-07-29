# Repository intake / vetting form — Layer B candidate

Filled in for every code-available candidate, to establish re-run priority and feasibility. **Note on standing:** whether the source journal is Web of Science indexed matters, because the source of repository #1 (Comput Biol Med) was delisted in November 2025, so a case study from a journal in good standing is needed alongside it.

| Field | Value |
|---|---|
| repo-id | <C-repo-00N> |
| repository URL | <..> |
| source study (author, year, **journal and WoS status**) | <..> |
| modality / task | <..> |
| **license** | osi / nonstandard / **none** (a finding) / — |
| **CPU compatibility** | yes / doubtful (GPU-only operation) / no |
| **example or supplied data** | present (inference can be attempted) / absent (not_attemptable) |
| weights | DOI / in the repository / absent |
| dependency file | dockerfile / requirements / environment.yml / none |
| estimated re-run effort | low / medium / high |
| **priority** | P1 / P2 / P3 |
| note | <..> |

## Known candidate core (from scoping, to be vetted)

| Repository | Modality | Standing / note |
|---|---|---|
| BSEL-UC3M/VFSS_analysis | VFSS (nnU-Net) | ✅ pilot #1 COMPLETED; the source journal is **delisted**, so a second case from a journal in good standing is required |
| SimonZeng7108/Video-SwinUNet | VFSS | ⚠️ **VETTED (14 Jul):** license unclear, data ethically restricted and not shared, GPU implied → **not_attemptable** (inference cannot be run out of the box). A transparency finding. |
| UofTNeurology/masa-open-source | acoustic (DenseNet, stroke) | ⚠️ **VETTED (14 Jul):** a license is present and Docker is provided, but **weights are absent and there is no example data** → inference is **not_attemptable**; only the environment build can be attempted. |
| sdc17/MEPDNet | ~~VFSS~~ | ❌ **VETTED (16 Jul) — OUT OF SCOPE.** Source: Shi et al., *Multi-Encoder Parse-Decoder Network for **Sequential Medical Image Segmentation***, **ICIP 2021** (IEEE, not delisted), license **BSD-3-Clause (OSI)**. However the abstract, `config/cfg.json` (a generic `data/train.npy`, class_num=2) and `utils/dataset.py` (a generic sequential or single dataset) show that it is **not dysphagia or VFSS work** but a generic U-Net-derived architecture paper. It was listed in error during scoping. It violates the eligibility criterion and therefore cannot serve as a case study. |
| PECI-Net | VFSS (bolus segmentation) | ❌ **VETTED (16 Jul) — NO CODE.** Source: *PECI-Net: Bolus segmentation from VFSS…*, **Comput Biol Med 2024** (arXiv 2403.14191). ⚠️ The venue is **the same delisted journal as pilot #1**. **No public official repository could be found on GitHub** (search returned zero results), so the code is inaccessible: a transparency finding, and not_attemptable because there is no artifact to re-run. |

> **Vetting outcome (16 Jul):** the requirement for a second case from a journal in good standing is **already met** by masa (#2, Front Neurosci, not delisted). The remaining scoping candidates were excluded: MEPDNet (out of scope), PECI-Net (no code), Video-SwinUNet (not attemptable). A GitHub sweep ordered by stars returned only two further very low-profile repositories (`zhengfj1994/dysphagia-viscosity-classifier`, `arivv22/ai-swallowing-sound-classification`), both with zero stars, **no license** and no link to a journal in good standing, so neither is suitable as a case study and using them would invite the objection that weak repositories were cherry-picked. **Decision:** no third case study was forced, on integrity grounds; further Layer B cases are drawn from the code-available subset identified by the census itself. The two completed cases (#1 out-of-the-box crash, #2 non-portable dependency) already document two distinct classes of friction.
> **Meta-finding (recorded):** the pool of dysphagia-AI repositories at the intersection of code-available, reputable venue, and weights or data plus a license is **very thin**, which is an independent observation supporting the article's low-reproducibility thesis.
