# Layer B Re-run Verdikt — repo <REPO-ID> (<repo-url>)
# Tarih: <YYYY-MM-DD> | Ortam: best-effort CPU konteyner (sapmalar belgeli)

## Meta
- Çalışma: <yazar, yıl, dergi> | Modalite: <..> | Model: <..>
- Lisans: <osi/none/..> | Ağırlık: <DOI/yok> | Örnek veri: <var/yok>

## 1. As-declared (faithful) deneme — re-executability
- Sonuç: **[BUILD_OK / BUILD_FAIL / RUN_FAIL]**
- Tam hata (varsa): `rerun-loglari/<REPO-ID>/as-declared.log`
- Kutu-dışı çalışıyor mu: **[EVET / HAYIR]**

## 2. Best-effort düzeltmeler (sürtünme taksonomisi)
| # | Engel kategorisi | Müdahale |
|---|---|---|
| FIX-1 | <dep_conflict/..> | <..> |
| FIX-2 | <undeclared_dependency/..> | <..> |
> Toplam düzeltme sayısı: **N** (nicelleştirilmiş sürtünme)

## 3. Çıkarım (CPU)
- Koştu mu: [EVET/HAYIR] | Süre: <..> | Not: <GPU-only op? postprocessing eksik?>

## 4. Karşılaştırma
- Re-executable (kendi çıktısını üretti): **[EVET/HAYIR]**
- Metrik-repro (yalnız referans/örnek veri varsa): **[tam / kısmi / NA-mahrem-veri]** — detay: <..>

## 5. VERDİKT
**[re_executable / partial / not_reproduced / not_attemptable]**
- Engel kategorileri: <liste>
- Tek-cümle: <..>

## 6. Provenance (SİLME)
Log/dosyalar: `rerun-loglari/<REPO-ID>/` · Docker imaj etiketi: <..> · commit/tag: <..>
