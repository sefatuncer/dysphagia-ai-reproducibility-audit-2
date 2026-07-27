# Eleme Formu — Başlık/Özet & Tam-Metin (çift-bağımsız tarama)

İki tarayıcı (Nazife klinik lens · Sefa açık-bilim/teknik lens) **bağımsız** uygular → **Cohen κ** → uzlaşı/3. hakem. Rayyan/Covidence'a aktar; her kayıt: **dahil / hariç / belirsiz(→tam metin)**.

## DAHİL (hepsi sağlanmalı)
1. **Birincil çalışma** (derleme/editöryal/yorum/protokol/yalnız-özet DEĞİL).
2. Bir **AI/ML/DL modeli** tanımlıyor (geliştirme veya doğrulama).
3. **Disfaji/yutma**'nın tanı / tarama / değerlendirme / şiddet-sınıflama / rehabilitasyon-izlemine uyguluyor.
4. Herhangi **modalite** (VFSS · FEES · akustik/servikal oskültasyon · sEMG · HRM · giyilebilir/IMU · klinik-tablo).

## HARİÇ (biri yeterli — kodu yaz)
- **E1** — AI/ML/DL yok.
- **E2** — Derleme / sistematik derleme / editöryal / yorum / protokol / yalnız-konferans-özeti (tam metin yok).
- **E3** — Hesaplamalı model tanımlamıyor.
- **E4** — Yalnız **özofageal motilite**, orofaringeal yutmayla ilişkisiz.
- **E5** — Aynı model/kohortun **yinelenen** raporu (en tam sürümü tut).
- **E6** — Dil: **İngilizce + çıkarılabilir tam metin DEĞİL** (kanonik ölçüt, kayıtta kilitli; makale §2.2 + OSF ile birebir aynı).

## Sınır durumlar (κ tutarlılığı için netleştirildi)
- **Kanser/RT:** *post-RT disfaji TAHMİNİ* (disfaji sonucu modelliyor) → **DAHİL**. *RT doz/tedavi-planlama*, disfaji-AI değilse → **E3/E4 HARİÇ**. `combined-corpus.csv`'de `likely_cancer_rt` flag'i bu kararı işaret eder.
- **Sağlıklı-sadece yutma tespiti/sayımı** → **DAHİL** (değerlendirme AI); `spectrum=healthy-only` notu düş.
- **Bibliyometri / scoping / benchmark-paper** → **E2 HARİÇ** (birincil değil).
- **`likely_review` flag'li** kayıtlar (n≈195) → hızlı E2 taraması.

## Karar akışı
başlık/özet → {dahil, hariç(kod), belirsiz} → belirsizler tam-metne → tam-metinde son karar (dahil/hariç-kod). PRISMA akış sayıları her aşamada kaydedilir.
