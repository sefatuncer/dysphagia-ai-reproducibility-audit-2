# Census Intake Bulguları — kod-açık yutma-AI repoları (NESNEL, re-execution merkezli)

> ## ⬆️ v2 GÜNCELLEME (16 Tem — code-mining sonrası; BU BÖLÜM GÜNCELDİR)
> Aşağıdaki v1 bölümü **N=17**'ye aittir. **Script 10 (OA-tam-metin code-link mining) → +5 in-scope repo → census N: 17 → 22 repo / 18 ayrık çalışma** (kümelenme: scut-jol×2, tsukagoshi×3, Yash+Tanishq×2). Ayrıntı: `code-mining-vetting.md`. **Birincil = study-düzeyi (N=18); repo-düzeyi (N=22) duyarlılık — uyuşuyor.**
> - **Güncel study-düzeyi (Wilson %95 GA):** açık lisans **3/18** [0.06, 0.39] · ağırlık DEPODA **1/18** [0.01, 0.26] · ağırlık dış-dahil **2/18** [0.03, 0.33] · ortam **6/18** [0.16, 0.56] · örnek-veri **4/18** [0.09, 0.45] · **inference-attemptable 2/18** [0.03, 0.33] · **kutu-dışı re-executable 0/18** [üst 0.18].
> - **Verdikt:** re_executable **0**, partial **2** (VFSS_analysis + **enoch0307 fiili re-run**, `C-repo-003-enoch0307/`), not_attemptable **16** (study) / 20 (repo).
> - **enoch0307 (pilot #3):** ağırlığı DEPODA paylaşan tek repo (`Binary.pkl`/`Multi.pkl`) → kutu-dışı yine çöküyor (sabitlemesiz ortam: sklearn 1.6.1→1.9.0 → `Multi.pkl` `ModuleNotFoundError:_loss`) → 1 pin düzeltmesiyle çalışır = **partial.** Fiili Docker + venv, çapraz-platform doğrulandı.
> - **KLİNİK 2. eksen:** RS1-6 uygulandı (`rs-taksonomi-kodlama.csv`) → **~0/18 rater κ raporluyor**; heterojen+vekil referans-standart → **birleşik tez: hesaplamalı+klinik provenans ikisi de eksik.**

---

## (v1 — N=17, tarihsel; yukarıdaki v2 geçerlidir)
**Tarih/erişim:** 2026-07-16 · **Yöntem:** tekrarlanabilir keşif (`07_repo_discovery.py`: GitHub + PwC) → nesnel dahil (`repo-envanteri.csv`) → nesnel intake (`08_repo_intake.py`: git-tree + releases + README dış-host taraması). **Öznel tarama YOK.**

## Census kapsamı
- Keşif: GitHub çok-terimli arama → **18 ham aday** + Video-SwinUNet (scoping) + 2 pilot (VFSS_analysis, masa).
- Elenen: `devilalreddy/Learnings` (çalışma değil). Dedup: SheenZhang721×2 = MinghaoSam MICCAI2024 (1 çalışma); tsukagoshi56×3, scut-jol×2, YashC1308+TanishqJoshi = grup-içi varyantlar.
- **İntake edilen: 15 repo** (pilot+dedup hariç) + **2 pilot derinlemesine re-run**.

## NESNEL şeffaflık sinyalleri (15 intake reposu)
| Sinyal | Sonuç | Oran |
|---|---|---|
| **Depoda eğitilmiş ağırlık** (*.pt/pth/h5/ckpt/onnx…) | **0 / 15** | %0 |
| **Releases'te ağırlık asset'i** | **0 / 15** | %0 |
| **Açık lisans** (OSI/present) | **1 / 15** (yalnız MinghaoSam MIT) | %7 |
| **Ortam dosyası** (requirements/Dockerfile/environment) | **4 / 15** (aht4005, tsukagoshi/liquid, tsukagoshi/ssl_gru, Video-SwinUNet) | %27 |
| **README dış-host ağırlık linki** | Video-SwinUNet (Google Drive); zhengfj1994 "pretrained/checkpoint" = **resume/backbone**, shipped ağırlık değil | ~0 |
| **Kutu-dışı inference ATTEMPTABLE** | **0 / 15** (ağırlık+veri yok) | %0 |

## Pilotlar (derinlemesine re-run, ayrı raporlanır)
- **VFSS_analysis** (Cubero, CBM 2025): **TEK** repo ağırlık (Zenodo 6.1 GB CC-BY) + örnek veri sağladı → attemptable → **partial** (kutu-dışı çökme → 5 düzeltme; yapısal-birebir, sayısal-kısmi). Lisans YOK.
- **masa** (Saab, Front Neurosci 2023): taşınamaz local-path wheel → **not_re_executable (env)**; ağırlık/veri yok → **not_attemptable (inference)**. Lisans VAR.

## MANŞET (nesnel, otonom-üretilmiş)
> **17 kod-açık yutma-AI reposunun (15 keşif + 2 pilot) yalnızca 1'i (VFSS_analysis) modelini çalıştırmak için gereken eğitilmiş ağırlıkları + örnek veriyi sağladı — ve o bile kutu-dışı çalışmadı (5 düzeltme → kısmi). Hiçbir repo ağırlığı depoya veya releases'e koymadı (1'i dış arşivde barındırdı). Lisans ~15/17'de, ortam-spesifikasyonu ~12/17'de yoktu.**
>
> Yani kod-açık yutma-AI literatürünün **fiili hesaplamalı tekrarlanabilirliği kutu-dışı ≈ 0'dır** — kod başarısız olduğu için değil, **eğitilmiş ağırlık, veri ve lisans sistematik olarak eksik** olduğu için. Bu, "kod paylaşımı" (URL çözülüyor mu) ile "yeniden-çalıştırılabilirlik" (fiilen koşuyor mu) arasındaki **uçurumu** nicel gösterir.

## Engel taksonomisi (frekans, census)
| Engel | Frekans (17) |
|---|---|
| **missing_weights** (eğitilmiş ağırlık yok) | 16/17 (VFSS hariç) |
| **absent_license** | ~15/17 |
| **missing_data** (örnek/test verisi yok; çoğu mahrem) | ~15/17 |
| **env_undeclared** (ortam dosyası yok) | ~12/17 |
| **GPU-oriented** (3D-CNN/video/segmentasyon) | çoğunluk (donanım-nötr ayrımı: ağırlık-yokluğu zaten donanım-öncesi engel) |
| dep_conflict / hardcoded_local_path / NameError | pilotlarda (VFSS: dep+NameError+postproc; masa: taşınamaz wheel) |

## Not (dürüstlük)
- "not_attemptable (inference)" = ağırlık+veri olmadan **çıkarım denenemez**; bazıları **eğitilebilir** (mahrem veri + GPU ile) ama bu kapsam-dışı (GPU-yeniden-eğitim + mahrem veri).
- İntake git-tree + releases + README-dış-host taradı; **canlı Google Drive linkleri elle teyit edilmedi** (Video-SwinUNet) — submission öncesi bir-iki dış-host teyidi eklenebilir, ama census manşetini değiştirmez.
- Study-düzeyi dedup (grup-varyantları) sentervde uygulanır; repo-düzeyi ve study-düzeyi N ayrı raporlanır.
