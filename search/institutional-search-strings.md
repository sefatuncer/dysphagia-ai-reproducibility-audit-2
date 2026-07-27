# Kurumsal Arama Dizeleri + PRESS Formu — ANAHTAR-TESLİM (yürütme: insan)

**Amaç:** Kurumsal erişimi olan (Sefa/Nazife) veya kütüphaneci, aşağıdaki dizeleri **kopyala-yapıştır** koşup export etsin → tek klasöre koysun → birleştirme scripti çalışsın. Açık-API'ler (PubMed 865 + EuropePMC 513 + S2 391 + OpenAlex 1890 → **2171 dedup**) zaten koşuldu; bu adım korpusu ~%65-70'ten tam PRISMA'ya çıkarır (boşluklar sistematik olarak IEEE/mühendislik venue'larında — nicel kanıt: `geriye-donuk-atif-kontrolu.md`).

> ⚠️ **PRESS ÖNCE:** kütüphaneci (metodolog 3. yazar) §PRESS formundaki 6 öğeyi denetleyip MeSH/Emtree eşlemesi + wildcard + alan-etiketini onaylamadan **kurumsal aramayı KİLİTLEME**. `ref 56 (Dysphagia s00455 2019)` PubMed-indeksli olmasına rağmen kaçtı → terim-duyarlılığı PRESS'te gözden geçirilecek (öneri: `deglut*`, `penetrat*`, `aspiration` eklemeleri).

---

## Her platform için: dize + export adımları

### 1) Scopus  (Advanced Search → paste)
```
TITLE-ABS-KEY ( dysphagia OR deglutition OR swallow* OR aspiration OR penetrat* )
AND TITLE-ABS-KEY ( "artificial intelligence" OR "machine learning" OR "deep learning"
 OR "neural network*" OR "deep neural" OR convolutional OR transformer* OR "random forest"
 OR "support vector" OR radiomics OR "computer-aided" OR "computer aided" OR "automated classification"
 OR "automatic detection" OR "predictive model" )
AND PUBYEAR > 2009 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
```
**Export:** hepsini seç → Export → **CSV** (veya RIS) → tüm alanlar (Citation information + Abstract + Keywords) → `kaynaklar/arama-sonuclari/scopus-records.csv`.

### 2) Web of Science Core Collection  (Advanced Search → TS=Topic)
```
TS=( (dysphagia OR deglutition OR swallow* OR aspiration OR penetrat*)
 AND ("artificial intelligence" OR "machine learning" OR "deep learning" OR "neural network*"
 OR convolutional OR transformer* OR "random forest" OR "support vector" OR radiomics
 OR "computer-aided" OR "computer aided") )
```
Timespan **2010–2026** · Indexes: **SCI-EXPANDED, ESCI** (+ CPCI-S konferans).
**Export:** Records → **Tab-delimited** veya RIS, "Full Record" → `kaynaklar/arama-sonuclari/wos-records.txt`.

### 3) IEEE Xplore  (Command Search — CS/mühendislik venue KRİTİK)
```
("All Metadata":dysphagia OR "All Metadata":deglutition OR "All Metadata":swallow*
 OR "All Metadata":aspiration)
AND ("All Metadata":"artificial intelligence" OR "All Metadata":"machine learning"
 OR "All Metadata":"deep learning" OR "All Metadata":"neural network"
 OR "All Metadata":convolutional OR "All Metadata":transformer OR "All Metadata":radiomics
 OR "All Metadata":"computer-aided")
```
Filtre: **2010–2026**. **Export:** Results → Download → **CSV (Citation & Abstract)** → `kaynaklar/arama-sonuclari/ieee-records.csv`.

### 4) Embase  (Emtree + .tw. — kütüphaneci Emtree'yi doğrular)
```
('dysphagia'/exp OR dysphagia:ti,ab,kw OR deglutition:ti,ab,kw OR swallow*:ti,ab,kw
 OR aspiration:ti,ab,kw)
AND ('artificial intelligence'/exp OR 'machine learning'/exp OR 'deep learning':ti,ab,kw
 OR 'convolutional neural network'/exp OR 'neural network*':ti,ab,kw OR transformer*:ti,ab,kw
 OR 'random forest':ti,ab,kw OR 'support vector machine'/exp OR radiomics:ti,ab,kw
 OR 'computer aided':ti,ab,kw)
AND [2010-2026]/py
```
**Export:** hepsini seç → Export → **RIS/CSV**, "Full record" → `kaynaklar/arama-sonuclari/embase-records.ris`.

### 5) ACM Digital Library  (opsiyonel, CS breadth)
```
[[All: dysphagia] OR [All: deglutition] OR [All: swallow*]]
AND [[All: "machine learning"] OR [All: "deep learning"] OR [All: "neural network"]
 OR [All: "artificial intelligence"] OR [All: convolutional]]
```
Yayın tarihi: **2010–2026**. **Export:** → **BibTeX/CSV** → `kaynaklar/arama-sonuclari/acm-records.bib`.

---

## PRESS 2015 — Kütüphaneci Denetim Formu (6 öğe)

| # | PRESS öğesi | Mevcut durum / kütüphaneci onayı |
|---|---|---|
| 1 | **Translation of research question** | Disfaji kavramı AND AI kavramı AND 2010–2026; PCC ile uyum onayla |
| 2 | **Boolean & proximity operators** | AND/OR yapısı; her DB'de wildcard (`*`) ve alan-etiketi (tiab/TS/.tw./All-Metadata) doğru mu? |
| 3 | **Subject headings** | MeSH `Deglutition Disorders`, `Artificial Intelligence` ↔ Emtree `dysphagia/exp`, `machine learning/exp` eşlemesi tam mı? Eksik heading? |
| 4 | **Text-word searching** | `swallow*`, `deglut*`, `neural network*`, `transformer*` yeterli mi? **Öneri:** `penetrat*`, `aspiration`, `auscultation`, `videofluoroscop*`, `endoscop*` ekle (modalite-duyarlılığı) |
| 5 | **Spelling, syntax, line numbers** | Her platform sözdizimi hatasız mı; tırnak/parantez dengeli mi? |
| 6 | **Limits & filters** | Yıl 2010–2026; dil filtresi **arama-düzeyinde UYGULAMA** (tarama-düzeyinde uygula → kayıp önle); doküman-tipi konferans dahil |

**Bilinen boşluk (düzeltilecek):** ref 56 (Dysphagia 2019, s00455) PubMed-indeksli olduğu halde kaçtı → öğe-4 metin-word duyarlılığını artır. **PRESS çıktısı:** onaylı final dizeler + PRISMA-S arama-raporlama eki (submission supplement).

---

## Birleştirme workflow (kurumsal export'lar geldikten sonra)

1. Export'ları `kaynaklar/arama-sonuclari/` altına koy (yukarıdaki adlarla).
2. Her kaynağı ortak şemaya normalize et (doi, pmid, title, year, venue, source) — mevcut `01_*`/`combined` boru hattı deseni; yeni kaynaklar için küçük parser eklenir.
3. `combined-corpus.csv` ile **birleştir + dedup** (normalize-başlık + DOI), yeni kayıtları `source=scopus|wos|ieee|embase|acm` flag'le.
4. **9 geriye-atıf eksiğini** (`backward-citation-additions.csv`, DOI'ler doğrulanmış) `source=backward_citation` ile ekle → PRISMA "other methods" kolu.
5. `04_prisma_counts.py`'yi yeniden koş → PRISMA identification/dedup gerçek sayılar.
6. Rayyan/Covidence'a aktar → **çift-bağımsız tarama** (bkz. `yurutme-runbook.md` + tarama SOP).

> **Beklenti:** kurumsal arama ağırlıkla IEEE/Scopus'tan **ek CS/mühendislik kayıtları** getirir (açık-API'lerin kaçırdıkları). Net-yeni benzersiz sayı muhtemelen birkaç yüz; asıl değer **payda kararlılığı** (Q1 hakemi için "çok-veritabanı" engelini kapatır).
