# Layer B Re-run Verdikt — repo C-repo-002 (UofTNeurology/masa-open-source)
# Tarih: 2026-07-14 | Ortam: python:3.10-slim Docker, as-declared pip install | İKİNCİL İTİBARLI PİLOT

## Meta
- Çalışma: **Saab R, et al.** (Balachandar, Mahdi, Nashnoush, … Khosravani), *Machine-learning assisted swallowing assessment…post-stroke dysphagia,* **Frontiers in Neuroscience 2023;17:1302132** (10.3389/fnins.2023.1302132) — **WoS-indeksli, itibarlı** (repo #1 kaynağı CBM'in aksine delisted DEĞİL → vitrin deliğini kapatır). ⚠️ *Düzeltme (16 Tem): önce hatalı "Alkhadrawi et al." yazılmıştı; Crossref yazar listesinde Alkhadrawi YOK, ilk yazar Rami Saab.*
- Modalite: akustik (yutma-sesi spektral analiz, CNN) | Görev: inme-sonrası disfaji taraması (TOR-BSST etiketi)
- Lisans: VAR (LICENSE.md) | Ağırlık: **YOK** | Örnek veri: **YOK** (kullanıcı kendi .wav'ını hazırlar)

## 1. As-declared (faithful) deneme — re-executability
- Komut: `docker run python:3.10-slim → pip install -r requirements.txt`
- Sonuç: **BUILD_FAIL** (EXIT=1)
- Hata: `ERROR: pocketsphinx-0.1.15-cp37-cp37m-win_amd64.whl is not a supported wheel on this platform`
- Kök neden: `requirements.txt` bir bağımlılığı **geliştiricinin yerel makinesine sabitlemiş**:
  `pocketsphinx @ file:///C:/Users/ramis/pipwin/pocketsphinx-0.1.15-cp37-cp37m-win_amd64.whl`
  → (a) `file:///C:/Users/ramis/...` yolu başka hiçbir makinede yok; (b) cp37 + win_amd64 wheel yalnız Windows Python 3.7'de kurulur. **Taşınamaz bağımlılık spesifikasyonu.**
- Kutu-dışı çalışıyor mu: **HAYIR** (ilk `pip install` adımında çöker).

## 2. Best-effort düzeltmeler (sürtünme taksonomisi)
Denenmedi (birincil bulgu için gerekmez); gerekseydi: pocketsphinx satırını PyPI sürümüne çevir + sistem `swig`/`libpulse` ekle. Ayrıca ağırlık+veri yokluğu inference'ı ayrıca engeller.

## 3. Çıkarım (CPU)
**not_attemptable** — eğitilmiş ağırlık YOK + örnek/sağlanan veri YOK → çıkarım denenemez.

## 4. Karşılaştırma
- Re-executable (env kuruldu mu): **HAYIR** (taşınamaz bağımlılık).
- Metrik-repro: **NA** (ağırlık+veri yok).

## 5. VERDİKT
**not_re_executable (env) + not_attemptable (inference)**
- Engel kategorileri: `undeclared_dependency` / **`hardcoded_local_path` (taşınamaz wheel)** · `missing_weights` · `missing_data` · `platform_locked` (cp37/win)
- Tek-cümle: *İtibarlı bir dergiden (Front Neurosci) çıkan repo, `requirements.txt`'te bir geliştiricinin yerel Windows yoluna sabitlenmiş taşınamaz bir wheel yüzünden kutu-dışı KURULAMIYOR; ağırlık/veri de paylaşılmadığından çıkarım da denenemiyor.*

## 6. Provenance (SİLME)
Ham log: `bieyh2hhx.output` (pip error) · repo klonu: scratchpad/masa (shallow) · commit: main@2026-07-11 · requirements.txt satırı 30 (pocketsphinx file://).

## Denetim değeri
Bu, **iki farklı itibarlı repoda iki farklı sürtünme sınıfı** verdiktini sağlar:
- repo #1 (VFSS): kutu-dışı çökme (dep-çelişkisi + NameError + eksik postprocessing) → 5 düzeltmeyle yapısal-birebir.
- repo #2 (masa): kutu-dışı kurulamaz (taşınamaz local-path wheel) + ağırlık/veri yok → not_attemptable.
→ "en-iyi-durum alt-kümesi bile kutu-dışı çalışmıyor" alt-sınır argümanını güçlendirir; engel taksonomisini genişletir.
