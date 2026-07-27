# Layer B Pilotu — BSEL-UC3M/VFSS_analysis (fizibilite + plan)

**Tarih:** 13 Tem 2026 · **Amaç:** Docker re-run yönteminin (Layer B) gerçekten yürüdüğünü tek repoda kanıtlamak.
**Repo:** https://github.com/BSEL-UC3M/VFSS_analysis · **Ağırlıklar:** Zenodo 10.5281/zenodo.17191973 · **Kaynak makale:** Comput Biol Med 2025, doi:10.1016/j.compbiomed.2025.109759

## Web incelemesi — doğrulanan gerçekler
| Öğe | Bulgu |
|---|---|
| Dil / bağımlılık | Python (%100); **conda `environment.yml`** + `setup.py` |
| Çerçeve | **nnU-Net v1** (eğitim + çıkarım) |
| GPU/CPU | CPU-uyumu **açıkça belirtilmemiş** (nnU-Net v1 GPU yoksa CPU'ya düşer, ama yavaş; bazı yollar `.cuda()` sabit olabilir) |
| Model ağırlıkları | **Var, halka açık:** Zenodo `models_VFSS.zip` **6.1 GB**, **CC-BY-4.0**; `models/` klasörüne konur (Task010 varsayılan, Task008 alt) |
| Örnek veri | ✅ **DAHİL:** `data/raw_VFSS/test/healthy_001` (AVI) + **manuel etiketler + predictions + parametreler** |
| Çalıştırma | clone → `conda env create -f environment.yml` → `pip install -e .` → pipeline (ön-işleme → nnU-Net çıkarım → etiketli video → 21 disfaji parametresi) |
| Metrik | README'de yok; kaynak makalede |
| **Kod lisansı** | ⚠️ **YOK (belirtilmemiş)** — repo'da LICENSE dosyası yok |
| Dockerfile | Yok |

## Fizibilite verdikti: ✅ YÜKSEK — neredeyse en-iyi-durum pilot
- ✅ **Örnek veri dahil** → özel hasta verisi olmadan çıkarım koşulabilir (en büyük engel kalkıyor).
- ✅ **Ağırlıklar halka açık (CC-BY)** → indirilebilir.
- ✅ **Sağlanan predictions + parametreler = hazır yeniden-üretim hedefi** → bizim re-run çıktımızı repo'nun kendi çıktısına karşı tolerans içinde kıyaslarız (segmentasyon + 21 parametre).
- ✅ conda `environment.yml` → konteynerize edilebilir.
- ⚠️ **nnU-Net v1 CPU çıkarımı** mümkün ama yavaş + belgelenmemiş → CPU'ya zorlamak gerekebilir (`CUDA_VISIBLE_DEVICES=""`); `.cuda()` sabit yolları çıkarsa küçük yama gerekir → **bu bizzat bir tekrarlanabilirlik bulgusu** (rubriğe işlenir).
- ⚠️ 6.1 GB ağırlık indirmesi + eski nnU-Net v1 bağımlılık zinciri (Python 3.7-3.9 / eski PyTorch) → sürüm sabitleme şart.

## İki kayda değer YAN BULGU (rapora malzeme)
1. **Kaynak makale Computers in Biology and Medicine'de** — ki bizim §5 listemizde **17 Kas 2025'te WoS'tan çıkarılmış (delisted)** dergi. Kod/model hâlâ duruyor, repo geçerli; ama "delisted dergide yayımlanmış AI çalışmasının reprodüklenebilirliği" ilginç bir vaka → tartışmada kullanılır.
2. **Kod lisansı yok** → varsayılan telif (tüm haklar saklı). Bizim *araştırma amaçlı çalıştırmamız* sorun değil, ama **redistribütasyon yapma**; ve bu, şeffaflık rubriğinde "lisans: yok" olarak ilk somut veri noktamız.
3. Çalışma **baş-boyun kanseri** VFSS'i (inme değil) — ama kapsamımız "disfaji AI (her etiyoloji)" olduğu için **dahil**.

## Somut konteynerizasyon planı (taslak Dockerfile mantığı)
```
FROM continuumio/miniconda3
# 1) repo + ortam
RUN git clone https://github.com/BSEL-UC3M/VFSS_analysis.git /app
WORKDIR /app
RUN conda env create -f environment.yml        # sürümleri LOGLA (pip freeze → kanıt)
SHELL ["conda","run","-n","<env>","/bin/bash","-c"]
RUN pip install -e .
# 2) ağırlıklar (build dışında da olabilir; 6.1 GB)
#    Zenodo models_VFSS.zip → /app/models/ ; SHA256 kaydet
# 3) CPU'ya zorla
ENV CUDA_VISIBLE_DEVICES=""
ENV nnUNet_* ...   # nnU-Net v1 yol değişkenleri
# 4) örnek üzerinde çıkarım
#    data/raw_VFSS/test/healthy_001 → preprocess → nnU-Net predict → parametreler
```
**Yeniden-üretim hedefi:** re-run'ın ürettiği segmentasyon + 21 parametreyi repo'daki **sağlanan `predictions` + `parameters`** ile karşılaştır → verdikt (**±5 pp / %95 GA** eşiğiyle: tam / kısmi / üretilemez).

## Beklenen sonuç ve kanıtladığı şey
- **En olası:** "çalışır ama küçük ortam/CPU yamaları gerekti" → *kısmen–tam reproducible*; yöntemin işlediğini kanıtlar + gerçek bir "reproducibility friction" anlatısı verir.
- Bu pilot başarılıysa, aynı boru hattı diğer 4-14 repoya (Video-SwinUNet, MEPDNet, PECI-Net, masa-open-source) ölçeklenir.

## Statik ön-denetim bulguları (repo klonlandı — gerçek dosyalardan; = rubrik satırı C-repo-001)
Repo `pilot-run/VFSS_analysis`'e klonlandı; `environment.yml`, `setup.py`, `run.py`, `paths_repository.py` okundu. Çalıştırmadan önce bile şu **tekrarlanabilirlik bulguları** çıktı:
1. **🔴 HEADLINE — Beyan edilen bağımlılıklar içsel olarak SAĞLANAMAZ (EMPİRİK DOĞRULANDI):** nnU-Net v1.7.1 numpy<1.24 gerektirir (kaldırılmış `np.bool/np.int`); ama beyan edilen ortamda **EN AZ İKİ paket** numpy≥1.24 ister — `scikit-image==0.25.0` **ve** `MedPy==0.5.2`. Gerçek build'de pip `ResolutionImpossible` verdi → çalışmayı koşturmak **üç zorunlu düşürme** gerektirdi (numpy 2.1.3→1.23.5, scikit-image 0.25→0.19.3, MedPy 0.5.2→0.4.0). Kanıt: `rerun-loglari/dep-conflict-pip-resolver.txt`. Çalışma "beyan edildiği gibi" reprodüklenemez.
2. **environment.yml tutarsız:** `python=3.10` ama `python_abi=3.13` (bozuk `conda env export`).
3. **`torch` sabitlenmemiş** (setup.py) ama env nvidia-cu12 (CUDA) wheel'leri taşıyor → sürüm kayması + GPU varsayımı.
4. **Lisans YOK** (repo'da LICENSE dosyası yok) → varsayılan telif; redistribütasyon yapma.
5. `setup.py`: `find_namespace_packages(include=["VFSS"])` ama repoda `VFSS/` paketi yok → `pip install -e .` boş paket kurar; çalışma `python run.py` ile cwd'den modül import ederek yürür.
6. **Kaynak makale Comput Biol Med'de** — 17 Kas 2025'te WoS'tan **delisted** (§5). Kohort **baş-boyun kanseri** (inme değil ama disfaji-AI → kapsamda).
7. **Sağlanan yeniden-üretim hedefi:** `data/output_data/.../*.csv` (7 parametre serisi) → `reference_outputs/`'a yedeklendi.

8. **🔴 Obskür/kırılgan + eksik-beyan bağımlılıklar:** `VFSS_functions.py` `import spicy` yapıyor — `spicy`, scipy'nin ünlü **typo-paketi**, environment.yml'de `spicy==0.16.0` diye pinlenmiş; kurulmazsa `ModuleNotFoundError`. Ayrıca `pydicom` modül-seviyesinde import ediliyor ama **setup.py'de listelenmemiş** (eksik-beyan bağımlılık).

**Fiili re-run (canlı, 13 Tem):** Best-effort imaj **kuruldu ve import'lar çalışıyor** (numpy 1.23.5 / torch 2.0.1+cpu / skimage 0.19.3 / nnunet 1.7.1 / batchgenerators 0.25.3; provenance: `rerun-loglari/pip-freeze-best-effort.txt`). Ağırlıklar (6.1 GB, CC-BY) indirildi; layout düzeltildi (`models_VFSS/nnUNet` → `models/nnUNet`). **5-fold CPU inference tamamlandı** (246 kare, ~3.9 saat). **SONUÇ:** kod **kutu-dışı çalışmadı** — beyan-ortamı çözülemez (3 düşürme + spicy/pydicom) + **NameError çökme** (`pathlib.Path` import edilmemiş, Step 3'te) + postprocessing eksik (`postprocessing.json` yok) → **5 belgelenmiş müdahale** gerekti. Düzeltmelerden sonra çalıştı; `compare.py`: **yapısal birebir** (7 parametre × 246 kare) ama **sayısal yakın-ama-birebir-değil** (alanlar ~%0.1 içinde; landmark/mesafe parametreleri ≤6 birim sapma) → postprocessing atlanması + ortam/CPU-vs-GPU sapmaları. **VERDİKT: PARTIAL / kutu-dışı-tekrarlanamaz.** Kanıt: `rerun-loglari/rerun-crash-findings.txt` + `compare.log`; rubrik `rerun_verdict` (C-repo-001) güncellendi.

**Betik seti hazır** (`pilot-run/`): `Dockerfile`, `download_weights.sh`, `run_pilot.sh`/`.ps1`, `compare.py`, `RUNBOOK.md`. Ağır kısım (6.1 GB indirme + CPU çıkarım) tek komut; Sefa çalıştırır (bkz. RUNBOOK).

## Sonraki eylem
- [ ] Sefa: `environment.yml`'yi çek, nnU-Net v1 CPU çıkarım yolunu doğrula (küçük yama gerekli mi); Dockerfile'ı yaz; `healthy_001` üzerinde çıkarımı koştur; çıktıyı sağlanan predictions ile kıyasla. Logları `rerun-loglari/`'na koy.
- [ ] Not: bu repo aynı zamanda Layer B örnekleminin **1. kaydı** olur.
