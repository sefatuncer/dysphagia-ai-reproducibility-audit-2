# Repo Intake / Vet Formu — Layer B adayı (İş #6 + #7 ortak)

Her kod-açık aday için doldur → re-run önceliği + fizibilite. **İtibar notu:** kaynak dergi WoS-indeksli mi (repo #1 kaynağı CBM Kas 2025 delisted → vitrin için itibarlı repo şart).

| Alan | Değer |
|---|---|
| repo-id | <C-repo-00N> |
| repo URL | <..> |
| kaynak çalışma (yazar, yıl, **dergi + WoS durumu**) | <..> |
| modalite / görev | <..> |
| **lisans** | osi / nonstandard / **none** (bulgu) / — |
| **CPU-uyumu** | evet / şüpheli(GPU-only op) / hayır |
| **örnek/sağlanan veri** | var(çıkarım denenebilir) / yok(not_attemptable) |
| ağırlıklar | DOI / repoda / yok |
| bağımlılık dosyası | dockerfile/requirements/environment.yml/none |
| tahmini re-run eforu | düşük / orta / yüksek |
| **öncelik** | P1 / P2 / P3 |
| not | <..> |

## Bilinen aday çekirdeği (scoping'den — vet edilecek)
| repo | modalite | itibar/not |
|---|---|---|
| BSEL-UC3M/VFSS_analysis | VFSS (nnU-Net) | ✅ pilot #1 YAPILDI; kaynak CBM **delisted** → ikincil pilot şart |
| SimonZeng7108/Video-SwinUNet | VFSS | ⚠️ **VET EDİLDİ (14 Tem):** lisans belirsiz + veri etik-kısıtlı (paylaşılmıyor) + GPU-ima → **not_attemptable** (inference kutu-dışı YOK). Şeffaflık bulgusu. |
| UofTNeurology/masa-open-source | akustik (DenseNet, inme) | ⚠️ **VET EDİLDİ (14 Tem):** lisans VAR (Docker'lı) ama **ağırlık YOK + örnek veri YOK** → inference **not_attemptable**; yalnız env-build denenebilir. |
| sdc17/MEPDNet | ~~VFSS~~ | ❌ **VET EDİLDİ (16 Tem) — KAPSAM DIŞI.** Kaynak: Shi et al., *Multi-Encoder Parse-Decoder Network for **Sequential Medical Image Segmentation***, **ICIP 2021** (IEEE, delisted değil), lisans **BSD-3-Clause (OSI)**. ANCAK abstract + `config/cfg.json` (jenerik `data/train.npy`, class_num=2) + `utils/dataset.py` (jenerik Seq/Single dataset) → **disfaji/VFSS DEĞİL**, jenerik U-Net-türevi mimari makalesi. Scoping'de yanlış listelenmiş. PCC uygunluğu ihlali → pilot olamaz. |
| PECI-Net | VFSS (bolus seg) | ❌ **VET EDİLDİ (16 Tem) — KOD YOK.** Kaynak: *PECI-Net: Bolus segmentation from VFSS…*, **Comput Biol Med 2024** (arXiv 2403.14191, doi:10.1016/j.compbiomed.2024.108241 civarı). ⚠️ CBM = **pilot #1 ile aynı delisted dergi** (itibar zayıf). GitHub'da **halka açık resmi repo bulunamadı** (search total=0) → kod erişilemez = **şeffaflık bulgusu**; not_attemptable (re-run edilecek artefakt yok). |
> **Vet sonucu (16 Tem):** İtibarlı-ikincil pilot şartı **masa (#2, Front Neurosci, delisted değil)** ile ZATEN karşılandı. Kalan scoping adayları elendi: MEPDNet (kapsam-dışı), PECI-Net (kod yok), Video-SwinUNet (not_attemptable). GitHub taraması (★-sıralı) yalnız 2 çok düşük-profilli ek repo verdi (`zhengfj1994/dysphagia-viscosity-classifier`, `arivv22/ai-swallowing-sound-classification` — ikisi de ★0, **lisanssız**, itibarlı-dergi bağı yok → showcase'e uygun değil, "cherry-pick zayıf repo" eleştirisi riski). **Karar:** zorlama 3. pilot YAPILMADI (integrity); ≥~10 gerçek Layer B örneği **tarama-sonrası kod-açık alt-kümeden** çekilecek. İki tamamlanan pilot (#1 kutu-dışı-çökme, #2 taşınamaz-bağımlılık) iki farklı sürtünme sınıfını zaten belgeliyor.
> **Meta-bulgu (kaydet):** Kod-açık + itibarlı-venue + (ağırlık+veri/lisans) kesişimindeki disfaji-AI reposu havuzu **çok ince** → bu, makalenin düşük-tekrarlanabilirlik tezini destekleyen bağımsız bir gözlem.
> Ek adaylar tarama+rubrik sonrası (kod-açık alt-küme) buraya eklenir. Hedef ≥~10 (gerçekçi 4-8 koşulabilir).
