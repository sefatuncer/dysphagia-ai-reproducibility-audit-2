#!/usr/bin/env python3
"""
09_census_synthesis.py — re-execution census sentezi (GERÇEK Results).

repo-intake-tablosu.csv (15) + 2 derinlemesine pilot → 17 repo (v1).
v2 (2026-07-16): OA-tam-metin kod-madenciliği (script 10) → +5 in-scope repo → N=22.
Yeni: ResearchgroupMITI/swallow-detection (Comms Med, CC0), enoch0307/streamlitapp_cn
(iScience, ATTEMPTABLE — env+ağırlık .pkl), yonghunsong/throat (npj Digit Med),
ruaeh/Dysphagia-ML (Sci Rep — BOŞ repo: linked-but-empty), PRI2MA/DL_NTCP_Dysphagia (borderline).
Üretir: verdikt dağılımı · şeffaflık oranları + Wilson %95 GA · engel taksonomisi frekansı.
Sabit, denetlenebilir kodlama (her repo'nun nesnel sinyali aşağıda; kaynak: intake + pilot verdiktleri).
"""
import csv, math, os, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
Z = 1.959963985

def wilson(k, n):
    if n == 0: return (float("nan"),)*3
    p = k/n; d = 1 + Z*Z/n
    c = (p + Z*Z/(2*n))/d
    h = (Z*math.sqrt(p*(1-p)/n + Z*Z/(4*n*n)))/d
    return p, max(0, c-h), min(1, c+h)

# 22 repo × nesnel sinyaller. alanlar: license, weights_in_repo, weights_anywhere(dış dahil),
#   env_file, sample_data_usable, attemptable, verdict, STUDY_ID (kümelenme/dedup için).
# STUDY_ID: aynı ekip/çalışmanın repo-varyantları aynı id → study-düzeyi payda (bağımsızlık).
#   scut-jol×2, tsukagoshi×3, Yash+Tanishq×2 kümeleniyor → 22 repo = 18 ayrık çalışma.
REPOS = [
 # repo, lic, w_repo, w_any, env, data, attempt, verdict, study_id
 ("VFSS_analysis(pilot1)", 0,0,1,1,1,1,"partial",         "A"),  # ağırlık Zenodo; 5 düzeltme→kısmi
 ("masa(pilot2)",          1,0,0,1,0,0,"not_attemptable", "B"),   # taşınamaz wheel; ağırlık/veri yok
 ("aht4005-risk-calc",     0,0,0,1,0,0,"not_attemptable", "C"),
 ("MinghaoSam-MICCAI24",   1,0,0,0,0,0,"not_attemptable", "D"),   # MIT ama ağırlık yok
 ("scut-jol/CFSCNet",      0,0,0,0,0,0,"not_attemptable", "E"),
 ("scut-jol/swallow_seg",  0,0,0,0,0,0,"not_attemptable", "E"),   # ↑ aynı çalışma (CFSCNet grubu)
 ("kwahid/ABAS",           0,0,0,0,0,0,"not_attemptable", "F"),
 ("tsukagoshi/liquid",     0,0,0,1,0,0,"not_attemptable", "G"),
 ("tsukagoshi/meanteacher",0,0,0,0,0,0,"not_attemptable", "G"),   # ↑ aynı ekip
 ("tsukagoshi/ssl_gru",    0,0,0,1,0,0,"not_attemptable", "G"),   # ↑ aynı ekip
 ("zhengfj1994-viscosity", 0,0,0,0,0,0,"not_attemptable", "H"),
 ("arivv22-sound",         0,0,0,0,0,0,"not_attemptable", "I"),
 ("Kai-Washino",           0,0,0,0,0,0,"not_attemptable", "J"),
 ("YashC1308-sEMG",        0,0,0,0,1,0,"not_attemptable", "K"),   # data/ var ama ağırlık yok
 ("TanishqJoshi-sEMG",     0,0,0,0,1,0,"not_attemptable", "K"),   # ↑ aynı sEMG çalışması
 ("20206666-chew-swallow", 0,0,0,0,0,0,"not_attemptable", "L"),
 ("Video-SwinUNet",        0,0,0,1,1,0,"not_attemptable", "M"),   # Drive link (teyit edilmedi)
 # --- v2: OA-tam-metin kod-madenciliği (script 10) ile eklenen 5 in-scope repo ---
 ("swallow-detection(MITI)",1,0,0,0,1,0,"not_attemptable","N"),   # Comms Med; CC0 + datasets/ ama ağırlık YOK
 ("enoch0307-screening",    0,1,1,1,0,1,"partial",        "O"),   # iScience; FİİLİ RE-RUN: box-out çökme (sklearn drift)→1 pin düzeltmesiyle→kısmi
 ("yonghunsong-throat",     0,0,0,0,0,0,"not_attemptable","P"),   # npj Digit Med; ağırlık/env/lisans YOK
 ("ruaeh-DysphagiaML(bos)", 0,0,0,0,0,0,"not_attemptable","Q"),   # Sci Rep; repo BOŞ = linked-but-empty
 ("PRI2MA-DL_NTCP(border)", 0,0,0,0,0,0,"not_attemptable","R"),   # Radiother Oncol; RT-NTCP prognostik borderline
]
FIELDS = ["license","weights_in_repo","weights_anywhere","env_file","sample_data","attemptable"]

def study_level(field_idx):
    """Study-düzeyi OR-aggregation: bir çalışma, repo-varyantlarından HERHANGİ biri
    sinyali taşıyorsa sinyali taşır (en-cömert; açık-bilim pratiği takım-düzeyi özellik)."""
    studies = {}
    for r in REPOS:
        sid = r[8]
        studies[sid] = studies.get(sid, 0) or r[field_idx]
    return sum(studies.values()), len(studies)

def rate_row(label, k, n):
    p, lo, hi = wilson(k, n)
    print(f"{label:22s}{f'{k}/{n}':>9s}{p:>8.2f}{f'[{lo:.2f}, {hi:.2f}]':>18s}")

def main():
    n = len(REPOS); n_studies = len(set(r[8] for r in REPOS))
    idx = {f: i+1 for i, f in enumerate(FIELDS)}
    labels = {"license":"Açık lisans","weights_in_repo":"Ağırlık DEPODA",
              "weights_anywhere":"Ağırlık (dış dahil)","env_file":"Ortam dosyası",
              "sample_data":"Örnek veri (kullanılır)","attemptable":"Inference attemptable"}

    # ---- BİRİNCİL: STUDY/EKİP DÜZEYİ (bağımsızlık; repo-varyantları kümelenmez) ----
    print("="*70); print(f"RE-EXECUTION CENSUS — ⭐BİRİNCİL: STUDY-DÜZEYİ (N={n_studies} ayrık çalışma)"); print("="*70)
    print("  (repo-varyantları kümelendi: scut-jol×2, tsukagoshi×3, Yash+Tanishq×2 → aynı çalışma)")
    print(f"{'Şeffaflık öğesi':22s}{'k/N':>9s}{'oran':>8s}{'  Wilson %95 GA':>18s}")
    print("-"*70)
    for f in FIELDS:
        ks, ns = study_level(idx[f]); rate_row(labels[f], ks, ns)
    # study-düzeyi verdikt: bir çalışma en-iyi repo-verdiktiyle etiketlenir
    order = {"re_executable":3,"partial":2,"not_reproduced":1,"not_attemptable":0,"attemptable_pending_rerun":1}
    best = {}
    for r in REPOS:
        if r[8] not in best or order.get(r[7],0) > order.get(best[r[8]],0): best[r[8]] = r[7]
    from collections import Counter
    vcs = Counter(best.values())
    full_s = vcs.get("re_executable",0)
    rate_row("→ Kutu-dışı re-exec.", full_s, n_studies)
    print("-"*70)
    print(f"  study-düzeyi verdikt: re_executable={vcs.get('re_executable',0)} · partial={vcs.get('partial',0)} · not_attemptable={vcs.get('not_attemptable',0)}")

    # ---- DUYARLILIK: REPO DÜZEYİ (kümelenmemiş; robustluk kontrolü) ----
    print("\n"+"="*70); print(f"DUYARLILIK: REPO-DÜZEYİ (N={n} repo; kümelenme düzeltmesiz)"); print("="*70)
    print(f"{'Şeffaflık öğesi':22s}{'k/N':>9s}{'oran':>8s}{'  Wilson %95 GA':>18s}")
    print("-"*70)
    for f in FIELDS:
        k = sum(r[idx[f]] for r in REPOS); rate_row(labels[f], k, n)
    print("-"*70)
    vc = Counter(r[7] for r in REPOS)
    print("REPO verdikt dağılımı:")
    for v in ["re_executable","partial","not_reproduced","not_attemptable"]:
        print(f"  {v:20s}: {vc.get(v,0)}")
    full = sum(1 for r in REPOS if r[7]=="re_executable")
    rate_row("→ Kutu-dışı re-exec.", full, n)
    print("="*70)
    print("MANŞET (iki-katmanlı, dürüst):")
    print(f"  • TRANSPARENCY katmanı: {n_studies} çalışmanın ~{study_level(idx['weights_anywhere'])[0]}'i herhangi yerde ağırlık,")
    print(f"    {study_level(idx['license'])[0]}'i açık lisans, {study_level(idx['env_file'])[0]}'i ortam dosyası paylaşıyor (çoğu sistematik eksik).")
    print(f"  • EXECUTION katmanı: yalnız {study_level(idx['attemptable'])[0]}/{n_studies} çalışma inference-attemptable;")
    print(f"    FİİLEN re-run edilen 2 vaka (VFSS_analysis + enoch0307) → İKİSİ DE 'partial' (kutu-dışı çökme→düzeltme);")
    print(f"    kutu-dışı düzeltmesiz TAM re-executable = 0 (hem study hem repo düzeyi; Wilson üst-sınır ~0.15-0.18).")
    print("  • Oranlar study↔repo düzeyinde SAĞLAM (kümelenme manşeti değiştirmez) — robustluk kanıtı.")

if __name__ == "__main__":
    main()
