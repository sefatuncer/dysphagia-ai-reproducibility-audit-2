#!/usr/bin/env python3
"""
09_census_synthesis.py — synthesis of the re-execution census (the real Results).

repo-intake table (15 repositories) plus the 2 in-depth pilots gave 17 repositories (v1).
v2 (2026-07-16): code-link mining over open-access full texts (script 10) added 5 in-scope
repositories, giving N=22: ResearchgroupMITI/swallow-detection (Comms Med, CC0),
enoch0307/streamlitapp_cn (iScience, ATTEMPTABLE — environment file plus .pkl weights),
yonghunsong/throat (npj Digit Med), ruaeh/Dysphagia-ML (Sci Rep — an EMPTY repository, the
"linked but empty" case), and PRI2MA/DL_NTCP_Dysphagia (borderline).

Produces: the verdict distribution, transparency rates with Wilson 95% intervals, and the
frequency of each barrier category. The coding is fixed and auditable: the objective signal
for every repository is listed below, sourced from intake and the pilot verdicts.
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

# 22 repositories x objective signals. Fields: license, weights_in_repo,
#   weights_anywhere (including external hosting), env_file, sample_data_usable,
#   attemptable, verdict, STUDY_ID (used for clustering and deduplication).
# STUDY_ID: repository variants from the same team or study share an id, so that the
#   study-level denominator respects independence.
#   scut-jol x2, tsukagoshi x3, Yash+Tanishq x2 cluster, so 22 repositories = 18 distinct studies.
REPOS = [
 # repo, lic, w_repo, w_any, env, data, attempt, verdict, study_id
 ("VFSS_analysis(pilot1)", 0,0,1,1,1,1,"partial",         "A"),  # weights on Zenodo; 5 repairs -> partial
 # masa: the one repository entered into the harness OUTSIDE the pre-stated entry rule
 # (it ships neither weights nor data, so `attemptable` is 0 and inference was never
 # reachable). A build WAS attempted and observed to fail on a non-portable wheel, so its
 # verdict is not_reproduced at the build stage, which is evidence the inventory could not
 # have produced. The two stages are reported separately in the manuscript and must not be
 # merged: attemptable=0 is the inference stage, verdict=not_reproduced is the build stage.
 ("masa(pilot2)",          1,0,0,1,0,0,"not_reproduced",  "B"),   # non-portable wheel; observed build failure
 ("aht4005-risk-calc",     0,0,0,1,0,0,"not_attemptable", "C"),
 ("MinghaoSam-MICCAI24",   1,0,0,0,0,0,"not_attemptable", "D"),   # MIT licensed but no weights
 ("scut-jol/CFSCNet",      0,0,0,0,0,0,"not_attemptable", "E"),
 ("scut-jol/swallow_seg",  0,0,0,0,0,0,"not_attemptable", "E"),   # same study as above (CFSCNet group)
 ("kwahid/ABAS",           0,0,0,0,0,0,"not_attemptable", "F"),
 ("tsukagoshi/liquid",     0,0,0,1,0,0,"not_attemptable", "G"),
 ("tsukagoshi/meanteacher",0,0,0,0,0,0,"not_attemptable", "G"),   # same team as above
 ("tsukagoshi/ssl_gru",    0,0,0,1,0,0,"not_attemptable", "G"),   # same team as above
 ("zhengfj1994-viscosity", 0,0,0,0,0,0,"not_attemptable", "H"),
 ("arivv22-sound",         0,0,0,0,0,0,"not_attemptable", "I"),
 ("Kai-Washino",           0,0,0,0,0,0,"not_attemptable", "J"),
 ("YashC1308-sEMG",        0,0,0,0,1,0,"not_attemptable", "K"),   # has data/ but no weights
 ("TanishqJoshi-sEMG",     0,0,0,0,1,0,"not_attemptable", "K"),   # same sEMG study as above
 ("20206666-chew-swallow", 0,0,0,0,0,0,"not_attemptable", "L"),
 ("Video-SwinUNet",        0,0,0,1,1,0,"not_attemptable", "M"),   # Drive link (not verified)
 # --- v2: the 5 in-scope repositories added by code-link mining (script 10) ---
 ("swallow-detection(MITI)",1,0,0,0,1,0,"not_attemptable","N"),   # Comms Med; CC0 and datasets/ but NO weights
 ("enoch0307-screening",    0,1,1,1,0,1,"partial",        "O"),   # iScience; ACTUAL RE-RUN: crashes out of the box (sklearn drift) -> one pin -> partial
 ("yonghunsong-throat",     0,0,0,0,0,0,"not_attemptable","P"),   # npj Digit Med; no weights, environment or license
 ("ruaeh-DysphagiaML(empty)",0,0,0,0,0,0,"not_attemptable","Q"),  # Sci Rep; repository EMPTY = linked but empty
 ("PRI2MA-DL_NTCP(border)", 0,0,0,0,0,0,"not_attemptable","R"),   # Radiother Oncol; RT-NTCP prognostic, borderline
]
FIELDS = ["license","weights_in_repo","weights_anywhere","env_file","sample_data","attemptable"]

# Two repositories that emerged from NONE of the scripted discovery channels and were
# carried forward from the earlier manual selection. The sensitivity analysis excludes
# them, to answer the objection that they are a 9% hole in the claim of reproducible
# discovery. The other 20 came from GitHub and Papers with Code (15) or from
# open-access mining (5).
CARRIED_FORWARD = ("masa(pilot2)", "Video-SwinUNet")

def study_level(field_idx, repos=None):
    """Study-level OR aggregation: a study carries a signal if ANY of its repository
    variants carries it (the most generous reading, since open-science practice is a
    team-level attribute)."""
    studies = {}
    for r in (REPOS if repos is None else repos):
        sid = r[8]
        studies[sid] = studies.get(sid, 0) or r[field_idx]
    return sum(studies.values()), len(studies)

def rate_row(label, k, n):
    p, lo, hi = wilson(k, n)
    print(f"{label:22s}{f'{k}/{n}':>9s}{p:>8.2f}{f'[{lo:.2f}, {hi:.2f}]':>18s}")

def main():
    n = len(REPOS); n_studies = len(set(r[8] for r in REPOS))
    idx = {f: i+1 for i, f in enumerate(FIELDS)}
    labels = {"license":"Open license","weights_in_repo":"Weights in repo",
              "weights_anywhere":"Weights (any host)","env_file":"Environment file",
              "sample_data":"Usable sample data","attemptable":"Inference attemptable"}

    # ---- PRIMARY: STUDY / TEAM LEVEL (independence; repository variants clustered) ----
    print("="*70); print(f"RE-EXECUTION CENSUS - PRIMARY: STUDY LEVEL (N={n_studies} distinct studies)"); print("="*70)
    print("  (repository variants clustered: scut-jol x2, tsukagoshi x3, Yash+Tanishq x2 = one study each)")
    print(f"{'Transparency item':22s}{'k/N':>9s}{'rate':>8s}{'  Wilson 95% CI':>18s}")
    print("-"*70)
    for f in FIELDS:
        ks, ns = study_level(idx[f]); rate_row(labels[f], ks, ns)
    # study-level verdict: a study is labelled with the best verdict among its repositories
    order = {"re_executable":3,"partial":2,"not_reproduced":1,"not_attemptable":0,"attemptable_pending_rerun":1}
    best = {}
    for r in REPOS:
        if r[8] not in best or order.get(r[7],0) > order.get(best[r[8]],0): best[r[8]] = r[7]
    from collections import Counter
    vcs = Counter(best.values())
    full_s = vcs.get("re_executable",0)
    rate_row("-> Re-exec. out of box", full_s, n_studies)
    print("-"*70)
    print(f"  study-level verdicts: re_executable={vcs.get('re_executable',0)} · "
          f"partial={vcs.get('partial',0)} · not_reproduced={vcs.get('not_reproduced',0)} · "
          f"not_attemptable={vcs.get('not_attemptable',0)}")
    print("    (not_reproduced = a build was attempted and observed to fail; not_attemptable =")
    print("     no build was attempted, because weights and data are both absent)")

    # ---- SENSITIVITY: REPOSITORY LEVEL (unclustered; robustness check) ----
    print("\n"+"="*70); print(f"SENSITIVITY: REPOSITORY LEVEL (N={n} repositories; no clustering correction)"); print("="*70)
    print(f"{'Transparency item':22s}{'k/N':>9s}{'rate':>8s}{'  Wilson 95% CI':>18s}")
    print("-"*70)
    for f in FIELDS:
        k = sum(r[idx[f]] for r in REPOS); rate_row(labels[f], k, n)
    print("-"*70)
    vc = Counter(r[7] for r in REPOS)
    print("REPOSITORY verdict distribution:")
    for v in ["re_executable","partial","not_reproduced","not_attemptable"]:
        print(f"  {v:20s}: {vc.get(v,0)}")
    full = sum(1 for r in REPOS if r[7]=="re_executable")
    rate_row("-> Re-exec. out of box", full, n)
    print("="*70)
    print("HEADLINE (two layers):")
    print(f"  - TRANSPARENCY layer: of {n_studies} studies, {study_level(idx['weights_anywhere'])[0]} share weights anywhere,")
    print(f"    {study_level(idx['license'])[0]} an open license, and {study_level(idx['env_file'])[0]} an environment file (most are systematically absent).")
    print(f"  - EXECUTION layer: only {study_level(idx['attemptable'])[0]}/{n_studies} studies are inference-attemptable;")
    print(f"    the 2 cases ACTUALLY re-run (VFSS_analysis and enoch0307) are BOTH 'partial' (crash out of the box, then repair);")
    print(f"    fully re-executable out of the box without repair = 0 (at both study and repository level; Wilson upper bound 0.15-0.18).")
    print("  - The rates are STABLE between study and repository level (clustering does not change the headline).")

    # ---- SENSITIVITY: EXCLUDING the carried-forward repositories (scripted-only census) ----
    kept = [r for r in REPOS if r[0] not in CARRIED_FORWARD]
    ks_n = len(set(r[8] for r in kept))
    print("\n" + "="*70)
    print(f"SENSITIVITY 2: SCRIPTED-ONLY ({len(CARRIED_FORWARD)} carried-forward repositories excluded)")
    print("="*70)
    print(f"  Excluded: {', '.join(CARRIED_FORWARD)} — neither emerged from any scripted channel.")
    print(f"  Remaining: {len(kept)} repositories / {ks_n} studies (GitHub and Papers with Code plus open-access mining only).")
    print(f"{'Transparency item':22s}{'k/N':>9s}{'rate':>8s}{'  Wilson 95% CI':>18s}")
    print("-"*70)
    for f in FIELDS:
        ks, _ = study_level(idx[f], kept); rate_row(labels[f], ks, ks_n)
    best_k = {}
    for r in kept:
        if r[8] not in best_k or order.get(r[7],0) > order.get(best_k[r[8]],0): best_k[r[8]] = r[7]
    vck = Counter(best_k.values())
    rate_row("-> Re-exec. out of box", vck.get("re_executable",0), ks_n)
    print("-"*70)
    print(f"  verdicts: re_executable={vck.get('re_executable',0)} · partial={vck.get('partial',0)} · "
          f"not_attemptable={vck.get('not_attemptable',0)}")
    print("  CONCLUSION: the headline (0 re-executable out of the box) is INDEPENDENT of the carried-forward repositories.")

if __name__ == "__main__":
    main()
