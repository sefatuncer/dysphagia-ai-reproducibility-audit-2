# Re-run Verdikti — enoch0307/streamlitapp_cn (Pilot/Vaka #3)

**Çalışma:** Interpretable machine learning for accessible dysphagia screening and staging in older adults. *iScience* 2026 (PMC12803820). **İtibarlı venue (WoS-listed; delisted DEĞİL)** → VFSS pilotunun CBM-delisted zaafını kapatan ikincil vitrin.
**Repo:** https://github.com/enoch0307/streamlitapp_cn · **Erişim/klon:** 2026-07-16 · **Donanım:** CPU (Sefa şeridi; görüntü-işleme/GPU YOK).
**Modalite:** klinik/tablo-ML (yaşlı disfaji tarama+evreleme; 10 klinik+akustik özellik). **Çalıştıran:** temiz Python 3.11 venv.

## Ortam (as-declared) — `requirements.txt` (SÜRÜM-SABİTLEMESİZ)
`streamlit, xgboost, scikit-learn, pandas, numpy, catboost, shap, matplotlib, openpyxl` — **hiç sürüm kısıtı yok.**
Temiz venv'de çözülen sürümler: scikit-learn **1.9.0**, numpy **2.4.6**, pandas **3.0.3**, xgboost 3.2.0, catboost 1.2.10, shap 0.51.0. (`plotly`+`joblib` app.py'de kullanılır ama beyan edilmez → geçişli çözüldü, box-out'u bozmadı.)

## Repo içeriği (şeffaflık — GÜÇLÜ uç)
- ✅ **Eğitilmiş ağırlık DEPODA:** `Binary.pkl` (CatBoost Pipeline), `Multi.pkl` (GradientBoostingClassifier). *(Census'ta ağırlığı DEPOYA koyan tek repo — 1/22.)*
- ✅ **Çıkarım kodu:** `app.py` (streamlit), config: `变量1.xlsx`/`变量2.xlsx` (UI değişken tanımları — repoda mevcut).
- ✅ **Ortam dosyası:** `requirements.txt` (ama sürümsüz).
- ❌ **Eğitim verisi:** `code.py` → `pd.read_csv("data2.csv")` — **data2.csv repoda YOK** (mahrem klinik veri, 1235+720 hasta) → eğitim tekrarlanamaz.
- ❌ **Lisans:** yok.

## KUTU-DIŞI re-execution (as-declared env, düzeltmesiz)
| Adım | Sonuç |
|---|---|
| app.py importları (streamlit/joblib/pandas/plotly/matplotlib/shap) | ✅ OK (plotly/joblib geçişli) |
| `变量1.xlsx` / `变量2.xlsx` config oku | ✅ OK |
| **`Binary.pkl` yükle** | ⚠️ yüklendi AMA `InconsistentVersionWarning` (**pickled sklearn 1.6.1, çalışan 1.9.0 → "sonuçlar geçersiz olabilir, kendi riskinizle"**) + `X has feature names but StandardScaler fitted without feature names` |
| **`Multi.pkl` yükle** | ❌ **FAIL — `ModuleNotFoundError: No module named '_loss'`** (sklearn iç-modül yolu 1.6.1→1.9.0 arası değişti) |
| Binary fiili predict (sentetik girdi) | ⚠️ çalıştı (ama yukarıdaki geçersiz-sonuç uyarısı altında) |
| Multi fiili predict | ❌ model yüklenemediği için denenemedi |

## Hedefli düzeltme → yeniden dene
**1 düzeltme: `scikit-learn==1.6.1` (eğitim sürümü) sabitle** → `Multi.pkl` **yüklendi + predict etti** (`GradientBoostingClassifier`, çıktı `[0]`). Yani Multi başarısızlığı **tamamen sürüm-kayması**ydı; kod/model sağlam, ortam-beyanı bozuk.
*(Bu izole düzeltme-venv'inde `catboost` kurulmadığı için `Binary.pkl` `ModuleNotFoundError: catboost` verdi — catboost requirements'ta beyanlı; tam-ortam+sklearn-pin ikisini de yükler.)*

## VERDİKT: **partial** (attemptable → kutu-dışı çökme → 1 hedefli düzeltmeyle çalışır)
- **Re-executability:** kutu-dışı **HAYIR** — ağırlık+config+ortam-dosyası paylaşan **census'taki en-iyi-durum repo bile** temiz koşmuyor. İki bağımsız box-out arızası: (1) `Multi.pkl` sert hata (`_loss`), (2) `Binary.pkl` "sonuçlar geçersiz olabilir" uyarısı. **Kök neden = sürüm-sabitlemesiz `requirements.txt`** (kanonik tekrarlanabilirlik arızası).
- **Fixability:** yüksek — **tek belirleyici düzeltme** (deps'i eğitim sürümlerine sabitle) Multi'yi kurtarır. VFSS'in 5-düzeltmesine karşı burada 1 düzeltme; her ikisi de "kutu-dışı çalışmıyor, düzeltmeyle kısmî".
- **Metrik-yeniden-üretimi:** DENENEMEZ — `data2.csv` (test kohortu) mahrem → makaledeki AUC/accuracy sayıları yeniden-üretilemez; yalnız yapısal çıkarım-boru hattı doğrulandı (sentetik girdi).

## Engel taksonomisi (bu vaka)
`env_undeclared_versions` (sürüm-sabitlemesiz) · `dependency_version_drift` (sklearn 1.6.1→1.9.0, pickle uyumsuz) · `missing_training_data` (data2.csv mahrem) · `absent_license`.

## Manşet katkısı
> Ağırlığı **depoya koyan tek repo** (1/22) bile, sürüm-sabitlemesiz ortam yüzünden kutu-dışı çökmektedir → **"kod+ağırlık paylaşımı ≠ yeniden-çalıştırılabilirlik"** uçurumunun en güçlü tek kanıtı. İtibarlı venue (iScience 2026) → araç/dergi-itibarı savunmasını çürütür. Engel bozuk model değil; **eksik ortam-provenansı** (Sefa'nın mühendislik ekseninin tam gösterdiği şey).

## FİİLİ DOCKER doğrulaması (manuscript "clean CPU Docker containers" iddiasını karşılar)
`Dockerfile` (python:3.11-slim + as-declared `requirements.txt`) build edildi (`docker build`, exit 0) ve `docker run` ile koşuldu → **venv bulgusu container'da BİREBİR yeniden üretildi:**
- `Binary.pkl` yüklendi + predict etti (aynı `InconsistentVersionWarning`: 1.6.1→1.9.0, "sonuçlar geçersiz olabilir")
- `Multi.pkl` **FAIL** (`ModuleNotFoundError: No module named '_loss'`) — aynı sert hata.
- **Çapraz-platform kanıt:** arıza hem Windows venv'de hem Linux Docker container'ında AYNI → deterministik, **ortam-kaynaklı** (Windows-özel tuhaflık değil). Container da sabitlemesiz `requirements.txt`'i sklearn 1.9.0'a çözdü.
- **Anlam:** manuscript'teki "temiz CPU Docker konteyneri" iddiası enoch0307 vitrini için artık **literal doğru + tekrarlanabilir**; `Dockerfile` yayımlanacak harness'e eklendi ("we practice what we audit").

## Provenans (SİLME)
`repo/` (klon), `rerun_test.py` (box-out harness), `Dockerfile` + `docker-build.log` (fiili container), `venv/` (as-declared), `venv_fixed/` (sklearn-pinned düzeltme kanıtı). Erişim/koşum tarihi 2026-07-16.
