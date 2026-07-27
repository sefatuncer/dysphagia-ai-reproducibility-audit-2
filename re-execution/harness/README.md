# Layer B — Genel Docker Re-run Harness (repo #2..N için)

Pilotu (repo #1, VFSS_analysis) **tekrar-kullanılabilir** protokole genelleştirir. Amaç: her kod-açık çalışmayı AYNI, denetlenebilir adımlarla yeniden koşmak → tutarlı verdikt + engel taksonomisi. **⚠️ Sistematik uygulama KAYIT SONRASI** (dahil-set kesinleşince); şablon şimdi hazırlanır.

**Donanım:** 32 GB / 16 çekirdek / Docker 29 / **CPU** (GPU-ölçekli yeniden-eğitim kapsam DIŞI — belgeli sınır).

## Adımlar (her repo)
### 0. Intake (önce vet et — `repo-intake.md` doldur)
Lisans · CPU-uyumu · örnek/sağlanan veri · bağımlılık dosyası · ağırlık DOI. **Lisans yoksa** = ilk şeffaflık bulgusu (yeniden-kullanım yasal engeli), yine de re-executability denenir.

### 1. "As-declared" (faithful) deneme — BİRİNCİL BULGU
Repoyu **belgelendiği gibi** kur/koş. Amaç: *kutu-dışı çalışıyor mu?* (re-executability). **Tam hata mesajını kaydet** → `rerun-loglari/<repo-id>/as-declared.log`. Çoğu repoda BAŞARISIZ beklenir; başarısızlık **manşet bulgudur**.

### 2. Best-effort minimal düzeltmeler — SÜRTÜNME TAKSONOMİSİ
Çalışması için gereken HER müdahale numaralandırılır (bağımlılık downgrade, eksik-beyansız paket, kod-hatası fix, eksik artefakt). Bunlar **nicelleştirilmiş sürtünme** = ikinci bulgu.

### 3. Çıkarım (CPU) — eğitim DEĞİL
Sağlanan/örnek veriyle çıkarımı koştur. GPU-only işlem varsa CPU-yaması dene; olmazsa `not_attemptable(GPU-only)`.

### 4. Karşılaştırma — re-executability ÖNCE, metrik SONRA
- **Önce:** artefakt çalışıp **kendi belgelenen çıktısını** üretti mi?
- **Sonra (yalnız örnek/referans veri varsa):** raporlanan metrik tolerans içinde mi (±5 pp/%95 GA; sürekli seri için yakın-eşitlik atol/rtol).
- Mahrem test kohortu = metrik-repro yapısal olarak imkânsız → bunu **bulgu** olarak kaydet.

### 5. Verdikt + log
`re_executable / partial / not_reproduced / not_attemptable` + engel taksonomisi + düzeltme sayısı → `verdikt-log.template.md` doldur → `rerun-loglari/<repo-id>/`.

## Engel taksonomisi (sabit kategoriler — sentez için)
`dep_conflict` · `unpinned_versions` · `undeclared_dependency` · `typo_package` · `code_bug` (import/path) · `missing_weights` · `missing_postprocessing_artifact` · `gpu_only_op` · `missing_data` · `undocumented_step` · `license_absent`.

## Dosyalar
- `Dockerfile.template` — parametrik CPU ortamı (base/py-sürümü değiştir).
- `verdikt-log.template.md` — repo başına standart verdikt (rerun-crash-findings.txt deseni).
- `repo-intake.md` — repo başına vet formu (İş #6 ile ortak).
- Referans desen: `../../pilot-run/` (repo #1 tam vaka) + `../rerun-loglari/`.
