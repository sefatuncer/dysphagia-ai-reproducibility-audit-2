# Klinik Tekrarlanabilirlik Konstrüktü + Disfaji-Özgü Referans-Standart & Etiket-Kalitesi Taksonomisi

**Sahip:** Nazife (eş-birinci, klinik eksen) · **Durum:** TASLAK → **Nazife onayı gerekir** (bu, onun eş-birinciliğini savunan entelektüel çekirdek).
**Amaç:** Hakem uyarısını kapatmak — "referans-standart geçerliliği + spektrum yanlılığı" **tek başına QUADAS-2 ile örtüşür** (Kwok/JMIR 2025 zaten uyguladı). Bu doküman, QUADAS-2'yi **AŞAN**, disfaji-AI'a **özgü**, dış-kaynaklanamaz bir klinik katkı tanımlar; rubriğe kodlama bloğu, makale tezine çapa ve **asgari-raporlama önerilerinin klinik yarısı** olarak girer.

---

## 1. Neden QUADAS-2 yetmez (konstrüktün gerekçesi)
QUADAS-2 jeneriktir: referans-standart alanını **ikili risk-yargısıyla** (düşük/yüksek/belirsiz) geçer ve "referans standart hedef durumu doğru sınıflar mı?" diye sorar. Disfaji-AI'ın **asıl** kırılganlıklarını sorgulamaz:
- Yutma değerlendirmesinde **altın standart bile gürültülüdür** (VFSS/FEES skorlamasının rater-arası güvenilirliği bilinen biçimde ılımlı) — QUADAS-2 bunu nicelemez.
- Ordinal skalaların (PAS 8-puan, DIGEST, FOIS) **ikiliye ezilmesi** = bilgi kaybı + hedef-kaymasını QUADAS-2 görmez.
- "Sağlıklı gönüllü yutması" ile "klinik disfaji" arasındaki **spektrum kontaminasyonu** QUADAS-2 alan-1'de kabaca geçer.
- **Vekil-sızıntısı** (modelin enstrümantal altın-standart yerine EAT-10/bedside vekilini tahmin etmesi) QUADAS-2 kapsamı dışıdır.

**Tez uzantısı (makalenin klinik çapası):** *"Konteynerize yeniden-koşulabilirlik (Sefa ekseni) GEREKLİdir ama YETERLİ değildir. Klinik tekrarlanabilirlik ayrıca **etiket-provenansı** ve **spektrum temsiliyeti** ister — kusursuz tekrarlanan bir model zayıf/önyargılı etiketlere dayanıyorsa klinik olarak tekrarlanabilir değildir."*

---

## 2. Taksonomi — kodlama bloğu (rubriğe eklenecek klinik kolonlar)
Her dahil edilen çalışma için kodlanır. Kategoriler + serbest not. QUADAS-2/STARD/TRIPOD+AI çapası ve **nerede aştığı** işaretli.

| # | Öğe | Kategoriler | Çapa & AŞMA |
|---|---|---|---|
| **RS1** | **Referans-standart tipi** | instrumental-gold (VFSS/MBSS·FEES) / klinik-muayene (bedside, 3-oz) / tarama-vekili (EAT-10, GUSS, Yale) / hasta-bildirimli / diğer-AI-türevli | STARD-uyumlu; disfaji-özgü katalog |
| **RS2** | **Hedef geçerliliği & vekil-sızıntısı** | model enstrümantal altın-standardı mı yoksa **vekili** mi tahmin ediyor? etiket ile hedef aynı mı? | **QUADAS-2 ötesi** — vekil-sızıntısı jenerik araçta yok |
| **RS3** | **Etiket skalası & granülarite** | PAS(8) / DIGEST / FOIS / MBSImP / Yale Pharyngeal Residue / ikili-aspirasyon / özel; **ikiliye indirgeme var mı** (bilgi kaybı) | **QUADAS-2 ötesi** — ordinal granülarite kaybı |
| **RS4** | **Etiket güvenilirliği** (Aşil topuğu) | rater κ/ICC raporlandı mı · rater sayısı · körleme · konsensüs vs tek-rater vs sağlanan-anotasyon | **QUADAS-2 ötesi** — yutma-skorlamasının düşük güvenilirliği tam burada |
| **RS5** | **Spektrum matrisi** | etiyoloji (inme/Parkinson/baş-boyun-kanseri/presbifaji/karışık) × şiddet dağılımı × **sağlıklı-kontrol kontaminasyonu** (sağlıklı gönüllü oranı) × örnekleme (ardışık vs uygun) | **QUADAS-2 ötesi** — çok-boyutlu matris; klinik-anlam |
| **RS6** | **Klinik uygulanabilirlik** | dağıtım ortamı (yatan/ayaktan/tele) · kullanıcı (SLP/hekim/otomatik) · karar-noktası; "tekrarlanabilirliğin klinik anlamı" yorumu | TRIPOD+AI klinik-yarar çerçevesi |

---

## 3. Çıktıya nasıl bağlanır (üç yerde iş görür)
1. **Rubrik (Layer A):** RS1–RS6, `seffaflik-rubrigi.csv`'ye klinik blok olarak eklenir → tüm ~60 çalışmada kodlanır (Nazife + gerçek bağımsız 3. tarayıcı; κ).
2. **Analiz/sentez:** kaç çalışma vekil-sızıntısı yapıyor · kaçında rater κ raporlu · sağlıklı-kontrol kontaminasyon oranı · etiyoloji dağılımı → **klinik tekrarlanabilirlik haritası** (Sefa'nın hesaplamalı haritasının yanında ikinci eksen).
3. **Asgari-raporlama önerileri (klinik yarısı):** her çalışma şunu raporlamalı — referans-standart tipi, kullanılan ordinal skala + granülarite, rater κ/ICC + rater sayısı + körleme, etiyoloji karışımı, sağlıklı-kontrol oranı, ardışık-vs-uygun örnekleme. **Bu klinik yarıyı Nazife üretir** (teknik yarıyı Sefa).

---

## 4. Eş-birincilik testi (dürüst)
- **Bu taksonominin TASARIMI** ne metodoloğun (SR tekniği) ne Sefa'nın (yazılım) yapabileceği iştir → yapılırsa **eş-birincilik otantik.**
- Yürütmede sığ kalırsa (sadece "değerlendirme" tekrarı olursa) → Nazife **güçlü katkıda-bulunan**; kariyer zararı yok çünkü birinci-yazarlık ihtiyacı başka çalışmayla zaten karşılanıyor. (Bu bir izole-C notu değil; genel ilke.)
- **Ölçüt:** RS2/RS3/RS4/RS5 gerçekten kodlanıp analiz edilip **ayrı bir bulgu** üretiyorsa (ör. "%X çalışma rater güvenilirliği raporlamıyor; %Y sağlıklı-kontrol kontaminasyonu var") → eş-birincilik savunulur.

## 5. Nazife'ye sorular (onaydan önce netleşmeli)
1. RS3 skala listesi tam mı? (Türkiye/klinik pratikte ek ölçek?)
2. RS4 için eşik: "yeterli güvenilirlik" tanımı (κ≥0.6? ICC≥0.75?) — literatür-dayanaklı.
3. RS5 etiyoloji kategorileri disfaji-AI literatürüne uygun mu?
4. Bu taksonomiyi **eş-birinci olarak sahiplenmeye** hazır mı, yoksa güçlü-katkıda-bulunan mı tercih?

---

## 6. UYGULAMA — census çalışmalarına ilk-geçiş kodlama (16 Tem 2026)
**Durum:** `analiz/rs-taksonomi-kodlama.csv` oluşturuldu (18 çalışma × RS1-6). **Dürüst iş bölümü:**
- **NESNEL sütunlar (ben — metinden doğrulanabilir, Nazife teyit eder):** RS1 referans-standart tipi · RS3 ölçek + binarizasyon · RS4 rater-güvenilirliği **raporlanmış mı** (κ/ICC evet/hayır).
- **KLİNİK-YORUM sütunları (Nazife — otantik klinik yargı, `[NAZIFE]` işaretli):** RS2 vekil-sızıntısı yargısı · RS5 spektrum-riski · RS4 "yeterli κ" eşiği · borderline kapsam (F/R/K).
- Kanıt-düzeyi her satırda: `abstract+fulltext` (6 çalışma, sağlam) vs `inventory-only` (paper eşleşmedi → Nazife tam-metinden kodlamalı).

### NESNEL ön-bulgular (2. manşet çekirdeği — hepsi denetlenebilir)
1. **Rater-güvenilirliği (κ/ICC) neredeyse HİÇ raporlanmıyor: ~0/18** erişilebilir metinde. Çarpıcı olan: sorunu **kabul eden** çalışmalar bile kendi etiket güvenilirliğini vermiyor — *masa/Saab*: "even VFSS by SLP has ... **poor inter-rater reliability**"; *MITI*: manuel uzman anotasyonu "**prone to errors**". Yani sorun biliniyor ama nicelenmiyor.
2. **Referans-standart HETEROJEN + standartsız:** enstrümantal-altın (VFSS: A,E,G,M,O · manometri: N · CT/MRI-seg: D,F) / klinik-bedside (B) / **vekil-sonuç** (Q tüp-besleme+pnömoni · R CTCAE-toksisite · C postop-sonuç) / fiziksel (H viskozite) / belirsiz-düşük-provenans (I,J,K,L,P). Ortak bir referans yok.
3. **Vekil-sızıntısı (RS2) yaygın [Nazife teyit]:** birkaç model enstrümantal altın-standardı DEĞİL bir **vekili** tahmin ediyor — *B* (ses→bedside-tarama), *Q* (ses→klinik-sonuç), *O* (klinik+ses→VFSS-teyitli disfaji), *R* (doz→toksisite). Model "disfajiyi" değil, disfajinin bir gölgesini öğreniyor.
4. **Kod-açık alt-küme düşük-etiket-provenansına eğik:** I/J/K/L gibi çalışmaların yayın-bağı/referans-standardı belirsiz → "kod paylaşan" repolar aynı zamanda etiket-provenansı en zayıf olanlar olabilir.

### DIŞ DOĞRULAMA (bağımsız kanıt)
Kwok/Wong scoping (JMIR 2025, PMC12089864) tam-metni: disfaji-AI çalışmalarının **18/24'ü (%75) örnekleme yaklaşımını tanımlamadı veya vaka-kontrol etiketlerinin körlenip körlenmediğini belirtmedi.** → Bizim "etiket-provenansı sistematik olarak eksik-raporlu" bulgumuzu bağımsızca doğrular.

### 🎯 BİRLEŞİK TEZ (iki eksen, tek argüman — otantik iki-yazar gerekçesi)
> Disfaji-AI **ne hesaplamalı ne de klinik olarak tekrarlanabilir** — çünkü **iki provenans da sistematik olarak yok:**
> - **Hesaplamalı provenans (Sefa ekseni):** ağırlık/ortam/lisans eksik → 0/18 kutu-dışı re-executable.
> - **Klinik/etiket provenansı (Nazife ekseni):** rater-güvenilirliği/spektrum/referans-standart eksik-raporlu → 0/18 etiket κ raporluyor; heterojen vekil-etiketler.
>
> Kusursuz tekrarlanan bir model bile zayıf/raporlanmamış etiketlere dayanıyorsa **klinik olarak tekrarlanabilir değildir.** Bu birleşik çerçeve, her iki eksenin **gerçekten gerekli** olduğunu gösterir → eş-birincilik otantik; katkı "bir denetim daha"yı aşar.

### Kalan (Nazife — insan)
- `inventory-only` satırları (D,E,F,G,H,I,J,K,L,M,C) tam-metinden kodla (özellikle RS4 κ, RS5 spektrum).
- `[NAZIFE]` sütunlarındaki klinik yargıları onayla/düzelt; RS4 "yeterli güvenilirlik" eşiğini literatürle sabitle.
- §5 sorularını yanıtla → nesnel ön-bulgular + klinik yorum = §3.4 nihai.
