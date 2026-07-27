# İstatistik Analiz Planı (SAP) — Makale C

> ⚠️ **v2 UYARLAMASI (re-execution census):** Bu SAP kısmen pivot-öncesi (SR/Payda-A/tüm-literatür) dili taşır. **v2 tasarımında payda = kod-açık (keşfedilebilir) set**tir, tüm-literatür değil. Sonuç: **radyoloji ile sayısal iki-oran karşılaştırması (Newcombe) UYGULANMAZ** (payda-uyumsuzluğu; bkz. §5 v2). Radyoloji yalnız kavramsal referans-çerçeve. Birincil analiz Wilson %95 GA (study-düzeyi N=18 birincil, repo-düzeyi N=22 duyarlılık; `09_census_synthesis.py`). RS4 (κ) klinik-güvenilirlik: erişilebilir tam-metin alt-kümesinde raporlanır (§4).

**Durum:** ön-kayıt paketine girer (OSF'de dondurulur). Sonuç verisi görülmeden kilitlenir.
**Yazılım:** Python (`analiz/scripts/03_analysis.py`) — sabit seed, sürümler sabitlenir; tüm figürler script'ten üretilir (makalenin tekrarlanabilirlik tezini kendi analizinde uygular).

## 1. Tahmin hedefleri (estimands)
**Payda A (şeffaflık, tüm dahil ~N):** her ikili öğe için paylaşım oranı — (a) kod, (b) veri-erişim beyanı/erişilebilir veri, (c) eğitilmiş ağırlık, (d) ortam/bağımlılık dosyası, (e) model kartı, (f) açık lisans. Ek: seed, README-çalıştırma, sürüm-sabitleme, dış-doğrulama, hesaplama-raporlama.
**Payda B (kod-açık alt-küme):** re-executability verdikti — **oran değil**, betimsel sayım + engel taksonomisi.

> **Birincil "kod paylaşımı" estimand'ının PAYI (kilit — hakem D3-M5).** Manşet oran ve radyoloji kıyası için "kod paylaşımı" = **beyan + çözülebilir URL + erişilebilir depo** (`code_stmt ∈ {yes, explicit_url}` VE `repo_accessible = yes`). **Salt-beyan** (URL ölü/yok) ikincil raporlanır. Bu tanım, Venkatesh 2022'nin ölçtüğü **"source-code availability" (erişilebilir kod)** ile kavramsal olarak eşlenir. **v2:** payda-uyumsuzluğu nedeniyle Newcombe sayısal-kıyası uygulanmaz; radyoloji yalnız kavramsal çerçeve (bkz. §5 v2).
> **Öğe-başı uygulanabilir payda.** TRIPOD+AI tüm dahil çalışmalara; **CLAIM yalnız görüntüleme-N**, **STARD yalnız tanısal-N**, **TRIPOD prediksiyon-modeli-N** alt-kümesine uygulanır. Her raporlama-standardı öğesi kendi uygulanabilir paydasıyla raporlanır (§2'deki "payda açıkça" kuralı bunu içerir).

## 2. Birincil analiz
- Her öğe için **oran + Wilson %95 GA** (küçük payda + uç oranlar için Wilson doğru seçim; normal-yaklaşım DEĞİL).
- Öğe başına payda **açıkça** raporlanır; "not reported" = **ayrı kategori** (impute YOK).
- **Çoklu-karşılaştırma / güç (hakem D3):** Bu bir **kestirim (estimation)** çalışmasıdır — doğrulayıcı hipotez testi YOK; GA'lar yalnız kesinliği niceler, katmanlar arası hiçbir kontrast inferansiyel yorumlanmaz → klasik multiplicity düzeltmesi **uygulanmaz** (bu metinde açıkça yazılır). **v2:** doğrulayıcı karşılaştırma yok (radyoloji-Newcombe kaldırıldı, §5). Çalışma uygun literatürün **sayımı (census)** olduğundan **a priori güç hesabı N/A**; Wilson GA genişlikleri elde edilen kesinliği iletir.

## 3. Katmanlandırma (ön-belirli, fishing YOK)
Yalnız şu katmanlar: **modalite** (VFSS/FEES/akustik/sEMG/HRM/giyilebilir/klinik) · **yıl-bandı** (2010-19 / 2020-22 / 2023-26) · **dergi tipi** (klinik / mühendislik-CS / informatik) · **görev** (tanı/tarama/şiddet/izlem). Alt-hücre <5 ise yalnız betimsel (GA geniş; yorumlanmaz).

## 4. Güvenilirlik (κ)
- **Tarama κ:** her **bağımsız** çift için Cohen κ (Sefa↔Metodolog; Nazife↔Metodolog) — evli-çift değil (bkz. metodolog paketi). **%95 GA (bootstrap, `03_analysis.py:cohen_kappa_ci`, sabit seed) + Landis-Koch yorumu.**
- **Rubrik κ:** kalibrasyon setinde çift-kodlama → öğe-bazlı κ; <0.6 ise kod defteri netleştirilip yeniden kalibre. **Kalibrasyon N ve çift-kodlama kapsamı = OSF §8 ile TEK forma sabitlenir** (kalibrasyon ~8-10 → sonra dahil-setin **≥%20'si** çift-kodlanır; makale §2.5 buna göre düzeltilir).
- **Ölçek-tipine göre κ:** **ordinal** öğeler (RS3 PAS/DIGEST/FOIS) → **ağırlıklı κ** (lineer/kuadratik; komşu-kategori anlaşmazlığı tam-anlaşmazlık sayılmaz); **nominal** öğeler → ağırlıksız Cohen κ.
- **κ paradoksu (çarpık marjinal):** uç taban-oranlı öğelerde (ör. model-kartı ~herkeste "no") yüksek gözlem-uyumu olsa bile κ paradoksal-düşük çıkabilir → κ yanında **gözlem-uyumu (po) + PABAK** raporlanır; Landis-Koch etiketi bu bağlamda temkinli yorumlanır.

## 5. Kıyas analizi (radyoloji) — v2 (KAVRAMSAL, sayısal Newcombe YOK)
⚠️ **v2 KARAR (hakem D3/H4):** Bu çalışmanın paydası **kod-açık (keşfedilebilir) set**tir; radyoloji figürleri ise **koşulsuz** (tüm-çalışma) oranlardır — Venkatesh 2022 (%34, 73/218) ve Lee 2025 (%39.9, 107/268). Paydalar uyumsuz olduğundan **iki-oran farkı + Newcombe %95 GA testi UYGULANMAZ ve raporlanmaz.**
- Radyoloji yalnızca **kavramsal availability-vs-executability çerçevesi** olarak kullanılır (Giriş): "komşu-alanda erişilebilirlik ~%34-40; erişilebilirlik gerekli ama yeterli değil; biz aşağı-akış adımını (executability) ölçüyor ve onun ≈0'a çöktüğünü buluyoruz." **Sayısal fark iddiası yok.**
- Manşet = disfaji executability sonucunun kendisi (0/18 kutu-dışı re-executable, Wilson GA); radyoloji Introduction'da niteliksel bağlam.
- ❌ **"DL ~%11.5" kıyası KALDIRILDI** (Lee 2025 gerçekte %39.9; doğru atıf + kavramsal kullanım). Tek doğrulanmış komşu-alan çapaları: Venkatesh %34, Lee %39.9 — ikisi de yalnız kavramsal.

## 6. Layer B (re-run) — betimsel
- Verdikt sayımı: **re-executable / partial / not-reproduced / not-attemptable** + engel taksonomisi frekansı (dep-çelişkisi, GPU-only, eksik ağırlık, eksik veri, kod-hatası, eksik postprocessing…).
- **Oran iddiası YOK** (N küçük, seçilim yanlı). Çerçeve: **"en-iyi-durum alt-kümesi bile kutu-dışı çökmüyor"** = güçlü alt-sınır + engel derinliği. Pilot repo #1 tam vaka olarak sunulur.
- **Örneklem = census (ön-kayıtlı):** kod-açık beyanı + çözülebilir URL'si olan **TÜM** dahil çalışmalar re-execution'a alınır (öznel "apparently runnable" kapısı YOK → seçilim yanlılığı önlenir; koşulamayanlar `not_attemptable` verdiktiyle bilgi üretir). İki ön-kayıt-öncesi pilot birincil sayımdan **ayrı** "feasibility" olarak raporlanır.
- **Donanım-nötr vs donanım-nedenli ayrımı (hakem D5-M4):** CPU-only harness'ta **GPU-only** verdikti ayrı raporlanır; **alt-sınır iddiası yalnız donanım-nötr başarısızlıklara** (dep-çelişkisi, eksik ağırlık, kod-hatası, lisanssızlık) dayandırılır. F4 verdiktleri donanım-nedenli/nötr diye stratifiye edilir.
- **RQ3 metrik-üretim toleransı — çıktı-tipine göre (ön-kayıtlı, hakem D3-M4):**
  (a) **sınıflama metriği** (accuracy/AUC/F1) → mutlak **±5 puan** veya raporlanan **%95 GA** içinde;
  (b) **sürekli çıktı** (alan/mesafe/piksel-mm) → **bağıl ±%5** veya raporlanan ölçüm-hatası/tekrarlanabilirlik payı içinde;
  (c) referans metrik/GA/örnek-veri yoksa → **"metrik-üretimi denenemez"** (impute YOK). Öncelik daima re-executability; metrik-üretim ikincil.

## 7. Triyaj validasyonu (hakem-riski kapatır)
Rastgele ~200 kayıt insan-gold taraması → deterministik regex bayraklarının (`t_bucket`, `t_review_like`, `t_has_ai`) **sensitivite/spesifisite/PPV**'si + karışıklık matrisi. Amaç: triyajın **hiçbir uygun çalışmayı elemediğini** göstermek (yüksek recall kanıtı). Triyaj **PRISMA'da eleme kutusu değil**, organizasyon aracıdır.

## 8. Duyarlılık analizleri (ön-belirli)
(a) preprint'leri hariç tut · (b) sağlıklı-sadece kohortları hariç tut · (c) yıl-yarısına göre · (d) yalnız ≥3-kaynak yüksek-güven çekirdek. Ana sonuç bunlara dayanıklı mı?

## 9. Eksik veri & sapma
- "not reported" ≠ "no" ayrımı korunur; her ikisi ayrı raporlanır.
- Protokol-sapması olursa OSF'de **zaman-damgalı amendment** + makalede beyan.

## 10. Çıktı figürleri (script üretir)
F1 PRISMA-ScR akış · F2 öğe-bazlı oran + Wilson GA (forest) · F3 modalite×yıl ısı-haritası (**her hücrede N yazılır; N<5 hücreler gri/işaretli — renk yoğunluğu gürültü olarak okunmaz**) · F4 re-run verdikt + engel taksonomisi (**donanım-nötr vs GPU-only stratifiye**) · T1 radyoloji kavramsal-bağlam (yalnız kendi Wilson GA'lı oranlar; **Newcombe farkı YOK**, v2 §5) · T2 klinik taksonomi (RS1-6) dağılımı (RS-uygulanabilir alt-küme).
> **Figür üretimi:** tüm figürler `03_analysis.py` (sabit seed, stdlib-only) + gerçek rubrik verisinden üretilir; %11.5 kıyası kaldırıldı, radyoloji paydası 73/218 doğrulandı, κ %95 GA (bootstrap) eklendi.
