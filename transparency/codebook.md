# Şeffaflık Rubriği — KOD DEFTERİ (kesin değer kümeleri + karar kuralları)

**Amaç:** İki bağımsız kodlayıcının her hücreyi AYNI kodlaması → yüksek κ. `kodlama-kilavuzu.md`'yi **kesin değer kümeleri + karar kuralları** ile genişletir ve `referans-standart-taksonomisi.md`'nin RS1-6 klinik bloğunu ekler. Boş form: `rubrik-sablonu.csv`. Kalibrasyon: `03_analysis.py` κ.

**Genel kurallar:**
- Kanıt: makale metni + bağlı repo/ek. Belirtilmemiş = **`not_reported`** (VARSAYMA; "no"dan farklı — ayrı raporlanır).
- Repo/DOI erişimi için **`check_date`** kaydet (canlı değişir).
- Her hücre = değer + gerekirse serbest not (`notes`).

## A. Kod & ortam (Sefa ekseni)
| Kolon | İzinli değerler | Karar kuralı |
|---|---|---|
| `code_stmt` | `explicit_url` / `on_request` / `none` / `not_reported` | Kod paylaşımı beyanı tipi. "GitHub'da" + link = explicit_url |
| `repo_accessible` | `yes` / `no` / `na` | URL HTTP 200 + boş değil. `na` = kod yok |
| `license` | `osi_approved` / `present_nonstandard` / `none` / `not_reported` | LICENSE dosyası/başlığı. OSI listesi referans |
| `readme_run_instructions` | `yes` / `partial` / `no` / `na` | Çalıştırma adımları var mı |
| `dependency_file` | `dockerfile` / `requirements` / `environment_yml` / `pyproject` / `multiple` / `none` | Hepsini `notes`'a yaz; en güçlüsü kolona |
| `versions_pinned` | `pinned` / `partial` / `none` / `na` | Sürümler sabit **ve tutarlı** mı. Çelişkili env = partial |
| `random_seed` | `yes` / `no` / `not_reported` | Seed değeri belirtilmiş mi |
| `compute_reported` | `gpu` / `cpu` / `both` / `none` | Donanım+süre; CPU-çıkarım fizibil mi `notes` |
| `runnable_example` | `yes` / `no` | Örnek girdi + beklenen çıktı sağlanmış mı |

## B. Veri & model
| Kolon | İzinli değerler | Karar kuralı |
|---|---|---|
| `data_availability` | `open` / `controlled` / `on_request` / `none` / `not_reported` | + kamusal DOI/tanımlayıcı `notes` |
| `model_weights` | `yes` / `no` / `not_reported` | Kalıcı DOI (Zenodo vb.) ile |
| `model_card` | `yes` / `no` | Model kartı/datasheet |

## C. Değerlendirme (ortak)
| Kolon | İzinli değerler | Karar kuralı |
|---|---|---|
| `external_validation` | `yes` / `no` / `not_reported` | Bağımsız kohort/açık veri |
| `subject_wise_cv` | `yes` / `no` / `unclear` / `na` | LOSO/denek-bazlı; kayıt-düzeyi bölme = no |
| `held_out_test` | `yes` / `no` / `unclear` | Dokunulmamış test seti |
| `calibration_utility` | `yes` / `no` | Kalibrasyon/karar-eğrisi (AUC-ötesi) |
| `uncertainty_reported` | `yes` / `no` | GA/uygun test (DeLong vb.) |

## D. Klinik — Referans-Standart Taksonomisi (Nazife ekseni · RS1-6)
| Kolon | İzinli değerler | Karar kuralı |
|---|---|---|
| `rs1_refstandard_type` | `instrumental_gold` (VFSS/MBSS/FEES) / `clinical_exam` / `screening_surrogate` / `patient_reported` / `ai_derived` / `not_reported` | Etiketin kaynağı |
| `rs2_surrogate_leakage` | `predicts_gold` / `predicts_surrogate` / `mismatch` / `unclear` | Model altın-standardı mı vekili mi tahmin ediyor |
| `rs3_label_scale` | `pas` / `digest` / `fois` / `mbsimp` / `yale_residue` / `binary_aspiration` / `custom` / `not_reported` + `binarized:yes/no` | Ordinal skala + ikiliye indirgeme var mı |
| `rs4_label_reliability` | `kappa/icc değeri` veya `not_reported`; + `raters:N`; + `blinded:yes/no`; + `consensus/single/provided` | Rater güvenilirliği (Aşil topuğu) |
| `rs5_spectrum` | `etiology:{stroke/parkinson/hn_cancer/neurodegen/presbyphagia/mixed}` + `healthy_pct:%` + `sampling:{consecutive/convenience}` | Spektrum matrisi |
| `rs6_clinical_applicability` | `setting:{inpatient/outpatient/tele}` + `user:{slp/physician/automated}` + serbest yorum | Klinik anlam |

## E. Meta + verdikt
| Kolon | Değer |
|---|---|
| `study_id`,`first_author`,`year`,`modality`,`task`,`repo_url`,`reference_standard`,`check_date` | serbest/kategorik |
| `rerun_verdict` | `re_executable` / `partial` / `not_reproduced` / `not_attemptable` + engel notu |

## κ kalibrasyon protokolü
1. Dahil-set kesinleşince (tarama sonrası) **rastgele ~8-10 çalışma** seç → iki bağımsız kodlayıcı ayrı kodlar.
2. Öğe-bazlı Cohen κ (`03_analysis.py`). **κ<0.60** olan öğede kod-defteri netleştirilir → yeniden kalibre.
3. Klinik bloğu (RS1-6): Nazife + metodolog; teknik blok: Sefa + metodolog (gerçek bağımsızlık).
