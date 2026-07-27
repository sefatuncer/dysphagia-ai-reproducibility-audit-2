# Kod-Link Mining Vetting Bulguları (Script 10 — OA tam-metin çıkarımı)

**Tarih:** 2026-07-16 · **Yöntem:** `10_code_link_mining.py` — Europe PMC arama (disfaji/yutma × AI × kod-hosting, OPEN_ACCESS, 2010–2026) → **394 OA tam-metin** NCBI BioC ile çekildi → github/gitlab/zenodo/osf/codeocean linkleri regex ile çıkarıldı → mevcut envantere karşı dedup.

**Ham çıktı:** 163 link (143 yeni code-repo + 20 arşiv/veri). `analiz/repo-envanteri-ek.csv`.

## Kritik: geniş-tarama gürültüsü
Tam-metin madenciliği **araç-atıflarını** ve **konu-dışı** makaleleri (disfaji/yutma tesadüfen geçen: H&N-kanser-RT, EEG, Parkinson, ilaç-etkileşimi, özofagus-kanseri) toplu çeker. 143'ün ~135'i elenmeli:
- **Araç/altyapı-atıfı (çalışmanın kendi reposu DEĞİL):** darknet, yolov7, labelme/LabelImg, opensmile, silero-vad, soxr, ggplot2, bwa, Trimmomatic, dcm2niix, h2o-3, EconML, boxmot, medcat + GNN kütüphaneleri (GAT/pyGAT, LINE, deepwalk, SkipGNN, decagon, KnowDDI, GraphEmbedding — hepsi tek off-topic ilaç-etkileşimi makalesi PMC10978847'den).
- **Konu-dışı (disfaji/yutma incidental):** akciğer/özofagus/oral/mide kanseri, EEG/BCI, Parkinson, dementia, MS, ALS, tiroid, diş — hiçbiri disfaji-AI tanı/değerlendirme değil.

## VETTING SONUCU (nesnel: GitHub API + EPMC özet-scope teyidi)

### ✅ YENİ IN-SCOPE code-repo (kendi çalışma reposu + disfaji/yutma-AI)
| repo | makale | dergi/yıl | scope | intake sinyali | verdikt-iskeleti |
|---|---|---|---|---|---|
| `ResearchgroupMITI/swallow-detection` | PMC12678422 | Communications Medicine 2025 | LTHRM'de yutma-olayı tespiti (DL) | **CC0-1.0** lisans; env yok; ağırlık **0**; `datasets/` var; 24 kod dosyası | **not_attemptable** (ağırlık yok) |
| `enoch0307/streamlitapp_cn` | PMC12803820 | iScience 2026 | yorumlanabilir ML disfaji **tarama+evreleme** (1235+720 hasta, dış-doğrulamalı) | lisans yok; **requirements.txt**; **ağırlık VAR** (`Binary.pkl`, `Multi.pkl`); streamlit `app.py`+`code.py` | **ATTEMPTABLE** — CPU-dostu tablo-ML → **GERÇEK RE-RUN ADAYI #2** |
| `yonghunsong/Throat-related-events-classification` | PMC11706958 | npj Digital Medicine 2025 | giyilebilir titreşim-sensörü disfaji izleme (multimodal ensemble) | lisans/env/ağırlık yok; 12 kod dosyası | **not_attemptable** (ağırlık yok) |
| `ruaeh/Dysphagia-ML` | PMC9537337 | Scientific Reports 2022 | inme-sonrası aspirasyon/tüple-besleme ses biyobelirteci ML | lisans/env yok; **repo BOŞ (0 dosya)** | **not_attemptable** — "linked-but-empty" (kod URL'si var ama depo boş) |

### ⚠️ BORDERLINE (disfaji-komşu; kapsam kararı)
| repo | makale | dergi/yıl | not |
|---|---|---|---|
| `PRI2MA/DL_NTCP_Dysphagia` | PMC12520315 | Radiotherapy & Oncology 2025 | RT-sonrası **geç dysphagia NTCP** (prognostik toksisite-tahmini, tanı/değerlendirme DEĞİL). `kwahid/ABAS` sınıfı → census'ta borderline dahil (tutarlılık); ağırlık/env yok → not_attemptable. |
| `greenapple-sea/Esophagus-Motility-Data` | PMC11828345 | PLoS One 2025 | HRM özofageal-motilite **VERİ-ONLY** deposu (0 kod, Apache-2.0). Model yok → re-run census DIŞI; özofageal-faz disfaji-komşu (arşiv olarak not). |

### 📄 IN-SCOPE makale ama KENDİ REPOSU YOK (kod paylaşılmamış)
- **PMC12950097** — *Dysphagia* 2026, "Using ML for Automated Segmentation and Detection of Swallows... Preterm Neonates" (dijital servikal oskültasyon, akustik). Tam-metinde yalnız `chirlu/soxr` (resampling aracı) atfı — **kendi kod deposu paylaşılmamış**. → Şeffaflık paydasında "kod-paylaşımı YOK" örneği; re-run edilebilir repo yok.

### ❌ KAPSAM-DIŞI (elendi)
- `Safnov/1` (PMC13290704) — inme-ilişkili pnömoni (SAP) tahmini; disfaji değerlendirme değil.
- `jhc050998/Strokeformer` (PMC12380291) — inme tromboliz-uygunluk prognozu; disfaji değil (repo ~boş).
- +~135 araç-atıfı/konu-dışı repo.

## Census etkisi
- **Yeni re-execution census repoları: +5** (4 solid in-scope + 1 borderline DL_NTCP) → **N: 17 → 22.**
- **Manşet güçlenir:** artık **2/22 attemptable** (VFSS_analysis partial + enoch0307 — fiili re-run denenecek), ama yine **kutu-dışı 0 tam-re-executable**; ağırlık/lisans/veri sistematik eksik sürüyor.
- **Yeni şeffaflık başarısızlık sınıfı:** `ruaeh/Dysphagia-ML` = "linked-but-empty" (URL çözülüyor ama depo boş) — "kod paylaşımı ≠ yeniden-çalıştırılabilirlik" uçurumunun canlı örneği.
- **Çok-modal keşif kanıtı:** repolar 3 bağımsız kanaldan bulundu (GitHub arama + PwC [script 07] + OA-tam-metin madenciliği [script 10]) → census kapsam-güvenilirliği artar.

## enoch0307/streamlitapp_cn — çıkarım-yolu ön-incelemesi (fiili re-run öncesi)
Repo içeriği: `Binary.pkl`, `Multi.pkl` (joblib modelleri), `app.py` (streamlit çıkarım), `code.py` (eğitim), `requirements.txt` (streamlit/xgboost/scikit-learn/catboost/shap/pandas/numpy/openpyxl), 2 logo. **Saf tablo-ML — CPU-dostu, görüntü-işleme/GPU YOK → Sefa'nın tam şeridi.**
- `code.py` (eğitim): `pd.read_csv("data2.csv")` → **data2.csv repoda YOK** (mahrem klinik veri) → eğitim tekrarlanamaz.
- `app.py` (çıkarım): shipped `Binary.pkl`/`Multi.pkl`'i joblib ile yükler (✓), ama `pd.read_excel("变量1.xlsx")` / `变量2.xlsx` (değişken-config) okur → **bu Excel'ler repoda YOK** → app kutu-dışı `FileNotFoundError` ile çöker.
- **Ön-verdikt (fiili re-run doğrulayacak):** ağırlık+ortam paylaşan **TEK** repo bile eksik yardımcı-dosya (config Excel) yüzünden **kutu-dışı çöker**; makaledeki 10-özellik listesinden config yeniden-kurulursa → muhtemelen **partial** (VFSS deseni: "attemptable ama düzeltme-gerektirir"). 
- **Anlatı değeri:** "kod paylaşımı ≠ yeniden-çalıştırılabilirlik" manşetinin en güçlü tek kanıtı — ağırlığı DA paylaşan repo bile koşmuyor. **enoch0307 = birincil vitrin adayı** (iScience 2026 = itibarlı venue, VFSS'in delisted-CBM sorununu çözer).
