# Şeffaflık Rubriği — Kodlama Kılavuzu (çift-bağımsız kodlayıcı için)

**Amaç:** `seffaflik-rubrigi.csv`'nin her öğesini iki kodlayıcının **aynı** şekilde kodlaması → yüksek κ (değerlendiriciler-arası uyum). Genel kural: kanıtı **makale metni + bağlı repo/ek**'te ara; belirtilmemişse **"not reported"** (varsayma). Repo/DOI **erişim tarihini** kaydet (canlı değişir). Pilot **repo #1 (VFSS_analysis)** kalibrasyon için birlikte kodlanır (aşağıda örnek değerler).

## Kod & ortam (Sefa ekseni)
| Öğe | Nasıl kodlanır (kategoriler) | repo #1 örnek |
|---|---|---|
| `code_stmt` | Kod paylaşımından bahis: **explicit-URL / on-request / none** | explicit-URL |
| `repo_accessible` | URL çalışıyor mu (HTTP 200, boş değil)? **yes/no** + erişim tarihi | yes (2026-07-13) |
| `license` | Repo'da LICENSE: **OSI-approved / present-nonstandard / NONE** | **NONE** |
| `readme_run_instructions` | Çalıştırma talimatı: **yes / partial / no** | yes |
| `dependency_file` | **requirements / environment.yml / Dockerfile / pyproject / none** (hepsini yaz) | environment.yml + setup.py |
| `versions_pinned` | Sürümler sabit **ve tutarlı** mı: **pinned / partial / none** | **partial** (torch sabit değil; env tutarsız) |
| `random_seed` | Seed belirtilmiş mi: **yes / no / na** | not stated |
| `compute_reported` | Donanım/süre (GPU/CPU): **yes / no** | GPU ima (nvidia-cu12); CPU belgesiz |

## Veri & model
| Öğe | Kategoriler | repo #1 |
|---|---|---|
| `data_availability` | **open / controlled / on-request / none** + kamusal tanımlayıcı | sample only; tam veri özel |
| `model_weights` | Ağırlık paylaşılmış mı (kalıcı DOI): **yes / no** | yes (Zenodo CC-BY) |
| `model_card` | Model kartı/datasheet: **yes / no** | no |

## Doğrulama
| Öğe | Kategoriler |
|---|---|
| `external_validation` | Bağımsız kohort/açık veri: **yes / no** |
| (ek) `subject_wise_cv` | LOSO/denek-bazlı: **yes / no / unclear** |

## Klinik (Nazife ekseni)
| Öğe | Kategoriler |
|---|---|
| `reference_standard` | **VFSS/FEES-instrumental (gold) / clinical / screening-surrogate** + geçerlilik notu |
| (ek) `rater_reliability` | Referans-etiket κ/ICC + değerlendirici sayısı/körleme: değer / not reported |
| (ek) `spectrum` | Etiyoloji (inme/H&N kanser/nörodejen/karışık) + sağlıklı-vs-hasta + ardışık-vs-uygun-örneklem |

## Re-run (Layer B — kod-açık alt-küme)
| Öğe | Kategoriler |
|---|---|
| `rerun_verdict` | **fully / partial / not-reproduced / not-attemptable** + engel notu (eksik veri / GPU-only / eksik ağırlık / dep-çelişkisi) |

**Anlaşmazlık çözümü:** İki kodlayıcı bağımsız kodlar → **Cohen κ** raporlanır → uzlaşı, çözülmezse 3. hakem (metodolog). Belirsiz her hücrede "not reported" + serbest not.
