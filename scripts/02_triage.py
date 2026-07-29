#!/usr/bin/env python3
"""
02_triage.py - deterministic PRE-screening triage (an aid to human screening)

This script DECIDES NOTHING. include_screen1 is left empty for dual independent human screening plus Cohen kappa.
Purpose: to pre-sort the 2171 records with TRANSPARENT regular-expression rules (the rules of the screening form),
flagging obvious excludes such as reviews, editorials and records with no AI, and bringing likely includes to the front.
Every rule is visible in this file, so the pre-sort is fully auditable.

Input : kaynaklar/arama-sonuclari/combined-corpus-enriched.csv
Output: analiz/tarama-calisma-sayfasi.csv (ready for Rayyan or Covidence; the screener1 and screener2 columns are empty)
        plus a stdout summary (bucket counts feeding the flow diagram)
"""
import csv, re, sys
from collections import Counter
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ENR = "kaynaklar/arama-sonuclari/combined-corpus-enriched.csv"
OUT = "analiz/tarama-calisma-sayfasi.csv"

def rx(terms):
    return re.compile("|".join(terms), re.I)

# --- AI / machine-learning / deep-learning signal ---
AI = rx([r"\bartificial intelligence\b", r"\bmachine learning\b", r"\bdeep learning\b",
    r"\bneural network", r"\bconvolutional", r"\bcnn\b", r"\brnn\b", r"\blstm\b", r"\bgru\b",
    r"\btransformer", r"\bu-?net\b", r"\bnnu-?net\b", r"\bresnet", r"\bvgg\b", r"\bdensenet",
    r"\befficientnet", r"\byolo\b", r"\bswin\b", r"\bvision transformer", r"\brandom forest",
    r"\bsupport vector", r"\bsvm\b", r"\bxgboost", r"\bgradient boosting", r"\bdecision tree",
    r"\bnaive bayes", r"\bk-?nearest", r"\bknn\b", r"\bradiomics", r"\bcomputer-?aided",
    r"\bautomat(ic|ed) (detection|segmentation|classification|recognition|analysis)",
    r"\bclassifier", r"\bmachine-?learning", r"\bdeep-?learning", r"\bsupervised learning",
    r"\bunsupervised", r"\bgenerative adversarial", r"\bgan\b", r"\bautoencoder",
    r"\breinforcement learning", r"\bnatural language processing", r"\bnlp\b",
    r"\blarge language model", r"\bfoundation model", r"\bpredicti(ve|on) model",
    r"\bfeature extraction", r"\bfeature selection", r"\bdata-?driven model"])
# weak signals: not counted as AI on their own, but noted
AI_WEAK = rx([r"\blogistic regression", r"\bregression model", r"\bstatistical model", r"\balgorithm"])

# --- review / non-primary ---
REVIEW_TXT = rx([r"\bsystematic review", r"\bscoping review", r"\bnarrative review",
    r"\bliterature review", r"\bmeta-?analys", r"\bumbrella review", r"\bbibliometric",
    r"\bstate[- ]of[- ]the[- ]art review", r"\ba review of\b", r"\breview of the literature"])
REVIEW_PT = {"review", "systematic review", "meta-analysis", "editorial", "comment",
    "letter", "news", "published erratum", "retraction of publication",
    "review-article", "openalex:review", "openalex:editorial", "openalex:letter",
    "openalex:erratum", "openalex:paratext"}
CASE_PT = {"case reports", "openalex:case-report"}
CASE_TXT = rx([r"\bcase report\b", r"\ba case of\b", r"\bcase series\b"])

# --- clinical-domain signal ---
DYS = rx([r"\bdysphagi", r"\bdeglutit", r"\bswallow", r"\baspiration", r"\bpenetrat",
    r"\bbolus", r"\bvfss\b", r"\bvideofluoroscop", r"\bfees\b", r"\boropharyng",
    r"\bpharyngeal", r"\bmbss\b", r"\bmodified barium", r"\bpiecemeal deglutition"])
ESO = rx([r"\besophageal motility", r"\bachalasia", r"\besophageal manometr",
    r"\besophageal spasm", r"\bgastroesophageal"])
OROP = rx([r"\boropharyng", r"\bpharyngeal", r"\bvfss\b", r"\bvideofluoroscop", r"\bfees\b",
    r"\bpenetrat", r"\baspiration", r"\bupper esophageal sphincter", r"\bswallow"])

MODALITIES = {
    "VFSS": rx([r"\bvfss\b", r"\bvideofluoroscop", r"\bmodified barium", r"\bmbss\b", r"\bfluoroscop"]),
    "FEES": rx([r"\bfees\b", r"\bfiberoptic endoscop", r"\bflexible endoscop", r"\bendoscopic evaluation of swallow"]),
    "acoustic": rx([r"\bacoustic", r"\bswallow(ing)? sound", r"\bcervical auscultation", r"\baudio\b", r"\bhnr\b"]),
    "sEMG": rx([r"\bs?emg\b", r"\belectromyograph", r"\bsurface electromyo"]),
    "HRM": rx([r"\bmanometr", r"\bhrm\b", r"\bpressure topography"]),
    "wearable/IMU": rx([r"\bwearable", r"\baccelerometer", r"\bimu\b", r"\binertial", r"\bpiezoelectric", r"\bneck-?worn"]),
    "CT/MRI": rx([r"\bcomputed tomograph", r"\bmagnetic resonance", r"\bmri\b", r"\b ct \b"]),
    "ultrasound": rx([r"\bultrasound", r"\bsonograph"]),
    "clinical/tabular": rx([r"\belectronic health record", r"\behr\b", r"\beat-?10", r"\bgugging", r"\bquestionnaire", r"\bclinical (data|variables|features)"]),
}

def modalities(t):
    return [m for m, r in MODALITIES.items() if r.search(t)]

def main():
    rows = list(csv.DictReader(open(ENR, encoding="utf-8")))
    out = []
    for r in rows:
        title = r.get("title", "") or ""
        abs = r.get("abstract", "") or ""
        t = (title + " . " + abs).lower()
        pts = set(p.strip().lower() for p in (r.get("pub_types", "") or "").split(";") if p.strip())
        has_abs = r.get("has_abstract", "") == "yes"

        ai_hits = sorted(set(m.group(0).lower() for m in AI.finditer(t)))
        has_ai = bool(ai_hits)
        weak_ai = bool(AI_WEAK.search(t))

        review_like = bool(REVIEW_TXT.search(t)) or bool(pts & REVIEW_PT) \
            or r.get("epmc_is_review", "") == "yes" or bool(r.get("likely_review", "").strip())
        case_like = bool(pts & CASE_PT) or bool(CASE_TXT.search(t))
        eso_only = bool(ESO.search(t)) and not bool(OROP.search(t))
        dys = bool(DYS.search(t))
        mods = modalities(t)

        # --- bucket assignment (in priority order) ---
        if review_like:
            bucket, code = "likely_exclude_review", "E2"
        elif case_like and not has_ai:
            bucket, code = "likely_exclude_case_report", "E3"
        elif eso_only:
            bucket, code = "likely_exclude_esophageal", "E4"
        elif has_ai and dys:
            bucket, code = "likely_include", ""
        elif not has_ai:
            if has_abs:
                bucket, code = "likely_exclude_no_AI", "E1/E3"
            else:
                bucket, code = "needs_review_no_abstract", ""
        else:  # has_ai but the dysphagia signal is weak or absent
            bucket, code = "needs_review", ""
        if bucket.startswith("likely_exclude") and not has_abs and not review_like and not (pts & REVIEW_PT):
            # with no abstract, leave even an obvious exclude to a human (a title alone is not enough)
            bucket, code = "needs_review_no_abstract", ""

        out.append({
            "dedup_key": r.get("dedup_key", ""), "pmid": r.get("pmid", ""), "doi": r.get("doi", ""),
            "year": r.get("year", ""), "venue": r.get("venue", ""), "title": title,
            "abstract": abs, "has_abstract": "yes" if has_abs else "",
            "pub_types": r.get("pub_types", ""), "n_sources": r.get("n_sources", ""),
            "t_bucket": bucket, "t_suggested_exclude": code,
            "t_has_ai": "yes" if has_ai else ("weak" if weak_ai else ""),
            "t_ai_terms": "; ".join(ai_hits[:8]),
            "t_dysphagia": "yes" if dys else "", "t_modality": "; ".join(mods),
            "t_review_like": "yes" if review_like else "", "t_esophageal_only": "yes" if eso_only else "",
            "likely_cancer_rt": r.get("likely_cancer_rt", ""),
            "screener1_decision": "", "screener2_decision": "", "screener_notes": "",
        })

    # sort by priority: include > needs_review > needs_review_no_abstract > excludes
    order = {"likely_include": 0, "needs_review": 1, "needs_review_no_abstract": 2,
             "likely_exclude_esophageal": 3, "likely_exclude_case_report": 4,
             "likely_exclude_no_AI": 5, "likely_exclude_review": 6}
    out.sort(key=lambda x: (order.get(x["t_bucket"], 9), -int(x["year"] or 0)))

    with open(OUT, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

    # --- summary ---
    bc = Counter(x["t_bucket"] for x in out)
    print("=" * 60)
    print(f"TRIAGE SUMMARY - {len(out)} records total  ->  {OUT}")
    print("-" * 60)
    for b in sorted(bc, key=lambda k: order.get(k, 9)):
        print(f"  {b:32s} {bc[b]:5d}")
    print("-" * 60)
    incl = bc["likely_include"]; nr = bc["needs_review"] + bc["needs_review_no_abstract"]
    exc = sum(v for k, v in bc.items() if k.startswith("likely_exclude"))
    print(f"  Likely INCLUDE      : {incl}")
    print(f"  Needs a human (grey): {nr}")
    print(f"  Likely EXCLUDE      : {exc}  (confirmed by a human; kappa reported)")
    print(f"  -> Dual human screening focuses first on {incl+nr} records rather than all 2171.")
    mc = Counter(m for x in out if x["t_bucket"] == "likely_include" for m in x["t_modality"].split("; ") if m)
    print("-" * 60)
    print("  Modality distribution among likely includes:", dict(mc.most_common()))
    print("=" * 60)
    print("NOTE: include_screen1 is DELIBERATELY empty. The decision is dual independent human screening plus Cohen kappa.")

if __name__ == "__main__":
    main()
