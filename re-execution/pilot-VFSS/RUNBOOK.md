# RUNBOOK — Layer B Pilot (BSEL-UC3M/VFSS_analysis)

Amaç: Docker re-run yönteminin (Makale C, Layer B) tek repoda çalıştığını kanıtlamak ve
tekrarlanabilirlik sürtünmesini **kanıtla** belgelemek. Repo zaten klonlu (`./VFSS_analysis`),
referans çıktılar yedekli (`./reference_outputs`).

## Ön koşullar
- **Docker Desktop çalışır durumda** (bu makinede kurulu: Docker 29.6.1).
- ~15 GB boş disk (6.1 GB ağırlık + imaj + ara dosyalar), internet.
- Windows: `run_pilot.ps1`; Git Bash/WSL: `run_pilot.sh`.

## Bu klasördeki dosyalar
| Dosya | İş |
|---|---|
| `VFSS_analysis/` | Klonlanmış repo (kod, örnek `healthy_001` AVI, sağlanan çıktılar) |
| `reference_outputs/` | Sağlanan çıktı CSV/AVI'lerinin **yedeği** (run.py bunları üzerine yazar → kıyas için saklandı) |
| `Dockerfile` | Best-effort CPU ortamı (sapmalar yorumlarda) |
| `download_weights.sh` | Zenodo 6.1 GB ağırlıkları indir + `models/`'e aç |
| `run_pilot.sh` / `.ps1` | build → run.py (CPU) → compare (tek komut) |
| `compare.py` | Yeniden üretilen CSV'leri referansla karşılaştır → verdikt |
| `rerun.log`, `compare.log` | Çalıştırınca oluşur (kanıt) |

## Yeniden-üretim hedefi ve tolerans
run.py 4 adım koşar (ön-işleme → nnU-Net çıkarım → etiketli video → 21 parametre). Karşılaştırma:
**yeniden üretilen `data/output_data/.../*.csv`** ↔ **`reference_outputs/.../*.csv`**. Segmentasyon→parametre
deterministik olmalı → tam reprodüksiyon = değerler ~birebir (compare.py: atol 1e-6, rtol 1e-3).
*(Not: ±5 pp/%95 GA eşiği doğruluk-metrikleri içindir; buradaki sürekli parametre serilerinde yakın-eşitlik testi kullanılır.)*

## A) "As-declared" (faithful) denemesi — KANIT için önce bunu dene
Amaç: çalışmanın **beyan edildiği gibi** kurulup kurulmadığını test etmek. **Beklenti: BAŞARISIZ.**
```bash
docker run --rm -v "$PWD/VFSS_analysis":/work/repo -w /work/repo \
  continuumio/miniconda3:24.9.2-0 \
  bash -lc "conda env create -f environment.yml && conda run -n VFSS_env pip install -e . && echo BUILD_OK"
```
**Tam hata mesajını `analiz/` altına kaydet.** Beklenen kırılmalar (statik ön-denetim):
1. `environment.yml` içsel tutarsız: `python=3.10` ama `python_abi=3.13` → conda solve hatası olabilir.
2. **Bağımlılık çelişkisi (headline bulgu):** `scikit-image==0.25.0` → numpy≥1.24; `nnunet==1.7.1` → numpy<1.24 (kaldırılmış `np.bool/np.int`). Aynı anda sağlanamaz.
3. `torch` setup.py'de **sabitlenmemiş** + env nvidia-cu12 (CUDA) wheel'leri taşıyor → sürüm kayması.
4. `setup.py`: `find_namespace_packages(include=["VFSS"])` ama repoda `VFSS/` paketi yok → kurulum boş paket.

## B) Best-effort CPU çalıştırma — yöntemi göstermek için
```bash
bash download_weights.sh          # 6.1 GB (bir kez)
bash run_pilot.sh                 # build → run → compare
# Windows: powershell -File run_pilot.ps1   (ağırlık indirmeyi Git Bash'te yap)
```
Dockerfile'daki **sapmalar** (numpy 1.23.5, scikit-image 0.19.3, CPU torch) tam da (2)-(3) çelişkisini
aşmak için yapıldı → **bunlar raporun bulgusu**: "çalışmayı koşturmak için beyan edilen ortamdan şu sapmalar gerekti."

## Beklenen sonuç ve kanıtladığı
- En olası verdikt: **kısmen / non-trivial ortam cerrahisiyle** reproducible → yöntem çalışır + gerçek bir "reproducibility friction" anlatısı.
- **Ağırlık layout'u (DOĞRULANDI):** zip `models/models_VFSS/nnUNet/2d/TaskXXX` olarak açılır; ama run.py `RESULTS_FOLDER=repo/models` sabitler (senin -e'ini ezer) → **`models/models_VFSS/nnUNet` → `models/nnUNet`** taşı (sonuç: `models/nnUNet/2d/Task010_VFSS/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0..4 + plans.pkl`).
- nnU-Net v1 CPU çıkarımı yavaş; tek örnekte kabul edilebilir.

## Kaydedilecek provenance (kanıt zinciri)
- `models_VFSS.zip.sha256` · build loglarındaki `pip freeze` (gerçek kurulan sürümler) · `rerun.log` · `compare.log` · faithful-deneme hata çıktısı.
- Hepsi `../analiz/rerun-loglari/` altına; rubrik satırı `../analiz/seffaflik-rubrigi.csv`'de (C-repo-001).
