# Disfaji-AI Asgari-Raporlama ÖNERİ SETİ — v0.2

> ⚠️ **Bu bir "standart" veya "checklist" DEĞİL, ÖNERİ setidir.** Formal bir standart Delphi/konsensüs süreci gerektirir (bizde yok). Hakem düzeltmesi: "checklist/standart" iddiası overclaim → **"recommendations"** olarak sunulur. Nihai sürüm, denetim sonrası **en sık ihlal edilen** maddeler öne çıkarılarak sabitlenir.

**Amaç.** Makale C'nin **yapıcı çıktısı**: sadece tekrarlanamazlığı ölçmek değil, çözümü önermek. Disfaji-AI çalışmaları için alana-özgü raporlama/şeffaflık önerileri.

**Türetim & çapa.** Her madde mevcut kılavuzlara **açıkça çapalanır** (TRIPOD+AI, CLAIM, STARD, QUADAS-2, FAIR/model-cards); disfaji-özgü maddeler jenerik kılavuzların **sustuğu** yerdedir → katkı budur. Kaynak sütunu her maddede.

**İki-yazar yapısı:** Part A (mühendislik/açık-bilim = **Sefa**) × Part B (klinik/disfaji-özgü = **Nazife**, `referans-standart-taksonomisi.md` RS1-6'dan türer) × Part C (değerlendirme, ortak). Bu ikili yapı, jenerik bir radyoloji-AI checklist'inin disfaji için sağlayamayacağı şeydir.

**Kullanım:** submission eki; her madde = Raporlandı (sayfa/bölüm) / Uygulanamaz (gerekçe) / Raporlanmadı.

---

## Part A — Tekrarlanabilirlik & Açık Bilim (mühendislik ekseni · Sefa)
| # | Madde | Kaynak çapası | Neden (pilot kanıtı) |
|---|---|---|---|
| A1 ⭐ | **Kaynak kod halka açık** (kalıcı URL, "on request" değil) | TRIPOD+AI 20; FAIR | "on request" ≈ yok |
| A2 ⭐ | **Kodda açık lisans** (OSI) | FAIR; disfaji-özgü boşluk | Lisanssız = yasal yeniden-kullanılamaz (pilot: yoktu) |
| A3 ⭐ | **Ortam/bağımlılık dosyası + SABİT sürümler** (requirements/environment.yml/**Dockerfile**) | TRIPOD+AI; disfaji-özgü | Pilot: beyan edilen bağımlılıklar **karşılıklı çözülemez** idi |
| A4 | **Rasgele seed sabit + raporlu** | TRIPOD+AI | Non-determinizm exact-repro'yu bozar |
| A5 ⭐ | **Veri-erişim beyanı + rota** (açık/kontrollü/gerekçeli-kısıtlı) | STARD; TRIPOD+AI | VFSS/FEES mahrem → rotayı dürüst belirt, atlama |
| A6 | **Eğitilmiş ağırlıklar arşivli** (kalıcı DOI, Zenodo) | FAIR | Yeniden-eğitimsiz çıkarım |
| A7 | **Model kartı/datasheet** (amaç, eğitim verisi, sınırlar) | Model Cards (Mitchell 2019) | Kapsam + hata modları |
| A8 | **Hesaplama/donanım raporlu + CPU-çıkarım fizibil/belgeli** | disfaji-özgü (bizim Layer B) | Repro yazarın tam GPU'sunu gerektirmemeli |
| A9 | **Çalışan minimal örnek** (örnek girdi + beklenen çıktı) | disfaji-özgü iyi-pratik | Mahrem-veri olmadan doğrulama (pilot bunu iyi yaptı) |

## Part B — Klinik geçerlilik & disfaji-özgü (klinik ekseni · Nazife, RS1-6)
| # | Madde | Kaynak çapası | Taksonomi |
|---|---|---|---|
| B1 ⭐ | **Referans-standart belirt + gerekçelendir** (enstrümantal VFSS/FEES vs klinik/tarama vekili) | STARD; QUADAS-2 alan-3 | RS1 |
| B2 ⭐ | **Referans-etiket rater güvenilirliği** (κ/ICC; rater sayısı; körleme) | **QUADAS-2 ötesi** (jenerik araç sormaz) | RS4 |
| B3 ⭐ | **Hasta spektrumu & seçimi** (etiyoloji; şiddet; sağlıklı-vs-hasta; ardışık-vs-uygun) | QUADAS-2 alan-1; **matris = disfaji-özgü** | RS5 |
| B4 | **Vekil-sızıntısı beyanı** (model altın-standardı mı vekili mi tahmin ediyor) | **QUADAS-2 ötesi** | RS2 |
| B5 | **Etiket skalası & granülarite** (PAS/DIGEST/FOIS; ikiliye indirgeme kaybı) | **disfaji-özgü** | RS3 |
| B6 | **Bolus/görev standardizasyonu** (IDDSI kıvam, hacim, protokol) | disfaji-özgü | — |
| B7 | **Modalite-özgü akizisyon** (VFSS: kare-hızı/ROI/doz; FEES: skop; akustik: mik/SNR; sEMG: elektrot; HRM: kateter) | CLAIM (görüntü); disfaji-özgü genişletme | — |
| B8 ⭐ | **Klinik sonuç tanımı** (PAS/aspirasyon/penetrasyon/şiddet — açık, klinik-anlamlı) | STARD; TRIPOD+AI | RS6 |
| B9 ⭐ | **Dürüst amaç-beyanı** (tarama/tanı/izlem; dış-doğrulama yoksa "deployment-ready" DEME) | TRIPOD+AI | RS6 |

## Part C — Değerlendirme titizliği (ortak)
| # | Madde | Kaynak çapası | Neden |
|---|---|---|---|
| C1 ⭐ | **Dış/bağımsız doğrulama** (ikinci kohort veya açık veri) | TRIPOD+AI; STARD | Tek-kohort AUC ≠ genellenebilir; #1 kabul-ayıracı (Kwok: 0/24) |
| C2 ⭐ | **Denek-bazlı (LOSO) CV** — kayıt-düzeyi sızıntı yok | disfaji/biyosinyal-özgü | Kare/kayıt-düzeyi bölme sızdırır → şişik metrik |
| C3 | **Dokunulmamış ayrık test seti** | TRIPOD+AI | İyimser sapmayı önler |
| C4 | **Kalibrasyon + klinik yarar** (kalibrasyon eğrisi, karar-eğrisi/net-fayda) | TRIPOD+AI | AUC klinik karar-değerini yok sayar |
| C5 | **Belirsizlik** (GA; uygun testler, DeLong) | TRIPOD+AI | Nokta-tahmin kesinliği abartır |
| C6 | **Güçlü baseline + ablasyon** (klinik skor + iyi-ayarlı klasik ML) | disfaji-özgü iyi-pratik | "DL for its own sake"e karşı korur |

---
*DRAFT → denetim sonuçlarına göre sonlandırılır: ~60 çalışmada en sık ihlal edilen maddeler çekirdek yapılır. Kaynak çapaları hakem güvenilirliği içindir. Delphi YOK → "öneri", "standart" değil.*
