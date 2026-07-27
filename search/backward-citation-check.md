# Geriye-Dönük Atıf Taraması — Korpus Tamlık Kontrolü (İş #3)

**Amaç:** OSF kaydını kilitlemeden önce, bilinen disfaji-AI derlemelerinin dahil-çalışma listelerini korpusla karşılaştırıp eksik var mı bak. **Durum: Kwok + CODAS TAMAMLANDI (niceliksel); 633-biblio = insan (WoS).**

## Kaynak 1 — Wong/Kwok et al. JMIR 2025;27:e65551 ✅ TAMAMLANDI
- **Başlık:** "Current Technological Advances in Dysphagia Screening: A Systematic Scoping Review" (HK PolyU). Kapsam: disfaji **TARAMA**, **24 çalışma** (ref [35]-[58]), 2979 katılımcı. QUADAS-2+M + TRIPOD+AI 5. AI-alanı.
- **Modalite (Kwok):** akustik 54% (13/24), vibratuar 38% (9/24), nazal-akış 8%, EMG 8%, strain/motion 8%, optik 4%; multimodal 25%.
- Tam metin: https://www.jmir.org/2025/1/e65551 · PDF: PolyU IRA 10397/115215 · PMID 40324167.

### Eşleşme sonucu (`kwok-24-eslesme.csv`)
**Kwok 24 → korpusta VAR = 13 · YOK = 11.** Eksik 11'in kırılımı:
| Durum | Ref | Not |
|---|---|---|
| **Kapsam-dışı (pre-2010, tasarımca doğru)** | 35(2008), 44(2004), 54(2008), 55(2009) | 2010–2026 filtresi dışında → eksiklik değil |
| **KAPSAM-İÇİ EKSİK (eklenecek)** | 45(2011 ArtifMed), 40(2022 IEEE TASLP), 41(2024 ICASSP), 50(2023 BSPC), 51(2023 DSP), 56(2019 **Dysphagia** s00455), 57(2021 ISCAS) | **7 çalışma** |

### Yorum (önemli bulgu)
- Kapsam-içi 20 Kwok çalışmasından **13'ü (65%) korpusta** → açık-API araması makul ama tam değil.
- **7 eksiğin 6'sı IEEE/mühendislik venue'su** (TASLP, ICASSP, ISCAS, DSP, BSPC) → **"kurumsal IEEE Xplore/Scopus araması şart" tezini NİCELİKSEL kanıtlar** (protokol §3.3 + metodolog paketi). Açık-API'ler CS-venue'ları kısmen kaçırıyor.
- 1 eksik (ref 56, Dysphagia s00455 2019) PubMed-indeksli olmasına rağmen kaçmış → arama-dizesi terim-duyarlılığı kütüphaneci/PRESS ile gözden geçirilmeli.
- **Aksiyon:** 7 kapsam-içi eksik, kurumsal arama sonrası korpusa `source=backward_citation` ile eklenecek → PRISMA "other methods" kolu. (Çoğu kurumsal IEEE aramasıyla zaten gelecek.)

## Kaynak 2 — CODAS 2025 scoping ✅ TAMAMLANDI
- **Künye:** Silva et al., "Artificial intelligence in the diagnosis and management of dysphagia: a scoping review." **CoDAS 2025;37(4):e20240305** (DOI 10.1590/2317-1782/e20240305en). 61 dahil çalışma; EMBASE/LILACS/Livivo/PubMed/Scopus/Cochrane/WoS + gri. Referans-standart çoğunlukla VFSS; DL baskın. Açık PDF (codas.org.br).
- **Eşleşme (`codas-eslesme.csv`):** kaynakçadan **64 benzersiz DOI → korpusta VAR=44 (%69)**; korpusta olmayan 20'nin 16'sı arka-plan/belirsiz, **4'ü AI-disfaji**; bunların 2'si pre-2010 (kapsam-dışı, doğru) → **2 gerçek kapsam-içi boşluk:**
  - `10.1038/s41598-023-34999-8` — Sci Rep 2023;13:7835, "Machine learning predictive model for aspiration screening in hospitalized patients with acute stroke" (PubMed-indeksli → arama-dizesi duyarlılığı sorusu). ⚠️ **DOI düzeltmesi (16 Tem):** ilk çıkarımda son karakter kesilip `-x` yazılmıştı (Crossref/OpenAlex 404); başlıkla doğru DOI `-8` teyit edildi. Ayrıca OpenAlex bu DOI için **bozuk kayıt** döndü (1968 kataliz makalesine bağlı) → `06_backward_additions.py` Crossref-öncelikli yapıldı (DOI tescil otoritesi = kanonik metadata). Küçük ama ironik meta-bulgu: metadata altyapısının kendisi de tekrarlanabilirlik hatası taşıyor.
  - `10.1109/access.2020.3019532` — IEEE Access 2020, semantik segmentasyon (yine **IEEE** boşluğu).

## Kaynak 3 — 633-bibliyometri (WoS 2000–2025) ⏳ İNSAN (WoS erişimi)
Geniş liste; çekirdek referans çapraz-kontrolü **kurumsal WoS** gerektirir → insan.

## SONUÇ (iki gold-derleme birleşik)
- **Korpus tamlığı ~%65-70** (Kwok kapsam-içi 13/20; CODAS 44/64) → açık-API araması makul ama tam değil.
- **Boşluklar sistematik olarak IEEE/mühendislik venue'larında** (TASLP, ICASSP, ISCAS, DSP, IEEE Access) → **kurumsal IEEE Xplore + Scopus araması PAZARLIKSIZ** (protokol §3.3; metodolog paketi). Bu artık **niceliksel kanıtlı.**
- **Eklenecek kapsam-içi eksikler:** Kwok'tan 7 + CODAS'tan 2 ≈ **~9 çalışma** (çoğu kurumsal IEEE aramasıyla zaten gelecek) → `source=backward_citation`, PRISMA "other methods" kolu. Listeler: `kwok-24-eslesme.csv`, `codas-eslesme.csv`.

## Yöntem (tekrarlanabilir)
Kwok PDF → PyMuPDF metin → ref [35]-[58] `[doi:]`/`[Medline:]` regex → `combined-corpus.csv` DOI+PMID eşleme. Aynı akış CODAS/633 için tekrar kullanılır. Ham: `scratchpad/kwok-text.txt`, sonuç: `kwok-24-eslesme.csv`.
