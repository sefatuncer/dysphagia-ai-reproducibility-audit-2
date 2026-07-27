# Arama Kaydı — PubMed/MEDLINE (Makale C)

**Veritabanı:** PubMed/MEDLINE (NCBI E-utilities `esearch`)
**Arama tarihi:** 2026-07-13
**Tarih filtresi:** 2010–2026 (`2010:2026[pdat]`)
**Toplam sonuç:** **865 kayıt** → PMID listesi: `pubmed-pmids.txt`

## Kullanılan sorgu (birebir)
```
("Deglutition Disorders"[Mesh] OR dysphagia[tiab] OR deglutition[tiab] OR swallow*[tiab])
AND
("Artificial Intelligence"[Mesh] OR "artificial intelligence"[tiab] OR "machine learning"[tiab]
 OR "deep learning"[tiab] OR "neural network*"[tiab] OR convolutional[tiab] OR transformer*[tiab]
 OR "random forest"[tiab] OR "support vector"[tiab] OR radiomics[tiab]
 OR "computer-aided"[tiab] OR "computer aided"[tiab])
AND 2010:2026[pdat]
```
PubMed'in çeviri kaydı (translation) `esearchresult.querytranslation`'da; MeSH genişletmesi otomatik uygulandı.

## Yıllara göre dağılım (indikatif büyüme trendi)
| Dönem | Kayıt (yıl) |
|---|---|
| 2010–2019 | 12–37/yıl (durağan, ~20-30) |
| 2020 | 51 · 2021: 64 · 2022: 92 · 2023: 95 |
| 2024 | 128 · 2025: 192 · 2026 (kısmi, ~7 ay): 146 |

**Yorum:** Disfaji-AI yayınları 2020 sonrası ~8-10× arttı → makale için güçlü "neden şimdi" gerekçesi (tekrarlanabilirlik denetimi tam da bu patlama anında kritik).
*(Not: per-yıl `[pdat]` sayımları toplamı ~1008; aralık sorgusu 865 → fark PubMed tarih-alanı eşleşme nüansından. **Otoriter figür = 865** aralık-toplamı; yıl sayıları yalnızca trend içindir.)*

## Durum ve kısıtlar
- ⚠️ **Yalnızca PubMed.** Protokoldeki diğer kaynaklar (**Scopus/Embase, Web of Science, IEEE Xplore, ACM DL**) kurumsal erişim/API-anahtarı ister → **Sefa/Nazife'nin kurumsal erişimiyle** aynı sorgu mantığı uyarlanarak koşulacak (kütüphaneci/PRESS gözden geçirmesiyle).
- Bu 865, **dedup öncesi ham havuzdur.** Radyoterapi-toksisite tahmini, baş-boyun kanseri tedavi-planlama, derleme/editöryal vb. **tarama aşamasında** hariç tutulunca çekirdek **tanı+değerlendirme** evreni ~60'a inecek (scoping tahminiyle tutarlı; 633 bibliyometri WoS 2000-2025 idi).
- Geriye-dönük tarama (backward citation): Kwok e65551 (24) + CODAS scoping (61) + 633-bibliyometri referansları eklenecek.

## Havuz kompozisyonu (elemeye ışık tutar) — `pubmed-metadata.csv`
865 kaydın PMID/yıl/dergi/yayın-tipi/başlık'ı `pubmed-metadata.csv`'de; boş `include_screen1` + `exclude_reason` kolonlarıyla → Rayyan/Zotero/Excel'de **doğrudan elemeye hazır**.
- **En sık dergiler:** Sci Rep (28) · Dysphagia (22) · IEEE EMBC (18) · Neurogastroenterol Motil (17) · Sensors (16) · Surg Endosc (15) · Laryngoscope (14) · Diagnostics (13) · Comput Biol Med (10).
- **Yayın tipi:** 853 Journal Article; **~110 Review + 23 Systematic Review ≈ 133 derleme → HARİÇ**; 32 Case Reports; 14 Validation Study; 20 Multicenter.
- **Eleme sinyali:** ~133 derleme + baş-boyun kanseri cerrahi/radyoterapi kümesi (Surg Endosc, Head Neck, Radiother Oncol) çıkınca çekirdek **tanı+değerlendirme ~60**'a yaklaşır (scoping tahminiyle tutarlı).

## Çok-kaynaklı arama (açık API, 13 Tem — "çok-veritabanı" engelini adresler)
| Kaynak | Sonuç | Not |
|---|---|---|
| PubMed/MEDLINE (tiab) | **865** | çekirdek |
| Semantic Scholar (bulk boolean) | **391** | CS/mühendislik venue kapsamı (IEEE/ACM/arXiv) — PubMed'in kaçırdıkları |
| Europe PMC (TITLE/ABSTRACT-kısıtlı) | **513** | PubMed + preprint. **Ders:** alan-kısıtsız sorgu tam-metinde **10.686 gürültü** verdi → title/abstract'a kısıtlandı (PRESS ile kütüphaneci finalize eder) |
| OpenAlex (title/abstract union) | **1890** | geniş breadth (Scopus/WoS-benzeri); "swallowing" üzerinden over-retrieve → taramada daralır |

Kayıtlar `semanticscholar-records.csv`, `europepmc-records.csv`, `openalex-records.csv`'de. Birleştirme+dedup İş #2'de. **Kurumsal Scopus/WoS/IEEE** formal PRISMA için insan tarafında eklenir; ama açık kaynaklar (özellikle S2 + OpenAlex) CS-venue kapsamını büyük ölçüde sağlar → Q1 "çok-veritabanı" beklentisi büyük ölçüde karşılanır.

## Birleşik korpus (dedup, İş #2) — `combined-corpus.csv`
- 4 kaynak → ham 3659 satır → **2171 benzersiz** (normalize-başlık dedup).
- **Çok-kaynağın GERÇEK katkısı:** PubMed'de olmayıp S2/EuropePMC'de olan **177 yüksek-güvenli kayıt** — venue'ları tam da PubMed/MEDLINE'ın kaçırdıkları: **medRxiv (8) · Research Square (14) · bioRxiv (2)** [preprint] + **IEEE Sensors Journal (5) · IEEE Access (3) · ACM IMWUT (3) · Biomedical Signal Processing & Control (3)** [CS/mühendislik]. → "çok-veritabanı" engeli açık API'lerle **somut karşılandı.**
- **446 kayıt ≥3 kaynakta** (yüksek-güven ilgili çekirdek). OpenAlex-only **1131** = geniş-eşleşme gürültüsü (taramada elenir).
- **Auto-flag:** 195 muhtemel **derleme** (HARİÇ) · 241 **kanser/RT** (klinik karar — post-RT disfaji tahmini kapsamda olabilir). `combined-corpus.csv`: `sources`, `n_sources`, `likely_review`, `likely_cancer_rt` + boş `include_screen1`/`exclude_reason` → **elemeye hazır.**
- **Kaba aday havuzu:** 2171 − 195 derleme − ~1131 OpenAlex-gürültü ≈ **~850 gerçek aday** → başlık/özet + tam-metin tarama sonrası çekirdek **tanı+değerlendirme ~60** (scoping tahminiyle tutarlı).

## Sonraki adımlar
1. Diğer veritabanlarını koş (kurumsal) → tüm kayıtları birleştir.
2. Rayyan/Covidence'a aktar, **dedup**.
3. **Çift-bağımsız** başlık/özet → tam-metin eleme + **Cohen κ** (Nazife klinik, Sefa açık-bilim).
4. PRISMA akış diyagramı sayıları buradan doldurulur.
