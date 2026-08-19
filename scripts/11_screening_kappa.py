#!/usr/bin/env python3
"""
11_screening_kappa.py (v2) — reliability of the scope-screening step, reported
per discovery channel and pooled, with the full 2x2 contingency table.

WHY v2
------
v1 computed agreement over the open-access mining channel only (n=163 records)
but the manuscript described it as "the entire candidate pool spanning all three
channels". That was wrong: the GitHub/Papers-with-Code channel (n=18) was never
included, and 163 is a numeric coincidence (143 OA code repos + 18 GitHub/PwC
+ 2 carried-forward = 163 candidate REPOSITORIES, while the OA channel alone
returned 163 RECORDS = 143 code repos + 20 archive/data links).
v2 screens both scripted channels with one unified blind rule and reports
per-channel and pooled statistics, plus the provenance reconciliation that
explains why the screening-level "include" count (6, OA channel) is not the
census count (22 repositories / 18 studies).

RATERS
------
Rater 1 = the recorded scope decisions in the released candidate lists.
Rater 2 = an INDEPENDENT, BLIND, rule-based re-application of the pre-stated
          inclusion rule (this script), using only OBJECTIVE record features
          (record type, repository name, paper title, repository description)
          and NOT the recorded decisions or the reviewer's free-text notes.

Reports simple agreement (Po), Cohen's kappa with both an asymptotic and a
bootstrap BCa 95% CI, PABAK, the prevalence and bias indices (PI, BI), and
positive/negative specific agreement (Ppos/Pneg). Ppos is reported because kappa
is marginal-driven under the extreme exclusion prevalence of the OA channel
(the "kappa paradox"); Ppos measures agreement on the decision-relevant class
without a chance correction that the skewed marginals distort. PI and BI make the
paradox explicit rather than leaving it to a verbal caveat.

v3 (2026-07-30) adds the bootstrap. The asymptotic (Fleiss) interval assumes cell
counts large enough for a normal approximation, which two of the three tables here
plainly violate (the GitHub channel has an empty cell and n=18). The bootstrap is
BCa over 2,000 resamples with a fixed seed; where the resampling distribution is
degenerate the interval is reported as not estimable rather than printed as a
number. All three intervals are written to the result file. The manuscript quotes
the widest, because BCa's normalizing assumption is the weakest of the three with
only four positive cells, and none of them supports a usable precision claim
anyway; reporting the narrowest would imply a precision the data do not carry.

An important limitation, stated here because it belongs with the numbers: the rule
specification was revised AFTER observing the agreement it produced (see the
sensitivity section below), so the reported kappa is an in-sample measure of how
well a stated rule fits the recorded decisions, and is expected to be optimistic.

This is an AUTOMATED reliability check, reported honestly as such, not as a
second human reader. Deterministic: the bootstrap uses a fixed seed.
"""
import csv, json, math, random, sys
from pathlib import Path

BOOT_N = 2000
BOOT_SEED = 20260730

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

EK = inp("repo-inventory-extra")   # OA full-text code-link mining channel
HAM = inp("repo-inventory-raw")    # GitHub Search API + Papers with Code channel
ENV = inp("repo-inventory")        # consolidated inventory (recorded decisions)
OUT = out("screening-reliability.json")

# ---------------------------------------------------------------- blind rule
# Objective operationalization of the pre-stated inclusion rule, applied blind
# to the recorded decisions and to the reviewer's notes.
TOOL_LIBS = (
    "yolo", "opencv", "labelme", "labelimg", "opensmile", "silero", "soxr",
    "ggplot", "/bwa", "trimmomatic", "dcm2niix", "h2o-3", "/h2o", "econml",
    "boxmot", "medcat", "darknet", "deepwalk", "decagon", "knowddi",
    "graphembedding", "pygat", "/gat", "skipgnn", "/line", "/deepwalk",
)
SCOPE_KW = ("dysphag", "swallow", "deglutit", "aspiration", "penetrat", "vfss", "fees")


def rater2_blind(record_type, repo, paper, description, rule="B"):
    """Independent rule-based decision: include (1) / exclude (0).

    Two rule variants are computed and both are reported, because the rule was
    revised after the first version was run. Full disclosure of that revision:

      Rule A (v1, as first released): scope evidence = the PAPER TITLE only.
      Rule B (v2, unified):           scope evidence = REPOSITORY NAME + PAPER
                                      TITLE + REPOSITORY DESCRIPTION.

    Rule A was revised because it is *inapplicable* to the GitHub/Papers-with-Code
    channel, which returns no paper titles at all (every record would be excluded
    by construction, making the reliability check degenerate). Extending the check
    to every screened record therefore required a feature set defined by what the
    channels actually return. The revision is not neutral in its effect: on the OA
    channel it raises Cohen's kappa from 0.49 to 0.79 (see the sensitivity output),
    and we report both so the reader can judge.
    """
    if record_type != "code":
        return 0                                       # archive/data link, not a code repo
    name = (repo or "").lower()
    if any(lib in name for lib in TOOL_LIBS):
        return 0                                       # widely used tool/library citation
    if rule == "A":
        scope_text = (paper or "").lower()
    else:
        scope_text = " ".join([name, (paper or "").lower(), (description or "").lower()])
    return 1 if any(k in scope_text for k in SCOPE_KW) else 0


# ------------------------------------------------------------------ statistics
def agreement(a, b):
    n = len(a)
    both1 = sum(1 for x, y in zip(a, b) if x == 1 and y == 1)
    both0 = sum(1 for x, y in zip(a, b) if x == 0 and y == 0)
    a1b0 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    a0b1 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    po = (both1 + both0) / n
    p_a1, p_b1 = (both1 + a1b0) / n, (both1 + a0b1) / n
    pe = p_a1 * p_b1 + (1 - p_a1) * (1 - p_b1)
    kappa = (po - pe) / (1 - pe) if pe != 1 else float("nan")
    # asymptotic SE (Fleiss); adequate for a descriptive interval
    if pe != 1 and 0 < po < 1:
        se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2))
        # kappa is bounded above by 1, so the asymptotic interval is clipped rather
        # than reported with an impossible upper limit
        lo = max(-1.0, kappa - 1.959963985 * se)
        hi = min(1.0, kappa + 1.959963985 * se)
    else:
        se = lo = hi = float("nan")
    # specific agreement (Cicchetti-Feinstein): chance-uncorrected, per class
    ppos = 2 * both1 / (2 * both1 + a1b0 + a0b1) if (2 * both1 + a1b0 + a0b1) else float("nan")
    pneg = 2 * both0 / (2 * both0 + a1b0 + a0b1) if (2 * both0 + a1b0 + a0b1) else float("nan")
    # prevalence index and bias index (Byrt et al.): the two quantities that make the
    # "kappa paradox" explicit. A high PI with high Po is why kappa can collapse even
    # when the raters almost always agree.
    pi = abs(both1 - both0) / n
    bi = abs(a1b0 - a0b1) / n
    return dict(n=n, both1=both1, both0=both0, a1b0=a1b0, a0b1=a0b1,
                r1_include=both1 + a1b0, r2_include=both1 + a0b1,
                po=po, pe=pe, kappa=kappa, kappa_se=se, kappa_lo=lo, kappa_hi=hi,
                pabak=2 * po - 1, ppos=ppos, pneg=pneg, pi=pi, bi=bi)


def _kappa_of(pairs):
    """Cohen's kappa for a list of (rater1, rater2) pairs; nan when undefined."""
    n = len(pairs)
    if n == 0:
        return float("nan")
    b1 = sum(1 for x, y in pairs if x == 1 and y == 1)
    b0 = sum(1 for x, y in pairs if x == 0 and y == 0)
    a10 = sum(1 for x, y in pairs if x == 1 and y == 0)
    a01 = sum(1 for x, y in pairs if x == 0 and y == 1)
    po = (b1 + b0) / n
    p_a1, p_b1 = (b1 + a10) / n, (b1 + a01) / n
    pe = p_a1 * p_b1 + (1 - p_a1) * (1 - p_b1)
    return (po - pe) / (1 - pe) if pe != 1 else float("nan")


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _phi_inv(p):
    """Acklam's rational approximation of the standard normal quantile."""
    if p <= 0 or p >= 1:
        return float("-inf") if p <= 0 else float("inf")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl, ph = 0.02425, 1 - 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > ph:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def bootstrap_kappa(a, b, n_boot=BOOT_N, seed=BOOT_SEED, alpha=0.05):
    """BCa bootstrap CI for Cohen's kappa, resampling records with replacement.

    Small, sparse tables make the asymptotic interval unreliable, so this is the
    interval we report. When the resampling distribution is degenerate (kappa
    undefined in a large share of replicates, or no variation at all), no number is
    invented: the interval is returned as not estimable, with the diagnostics.
    """
    pairs = list(zip(a, b))
    n = len(pairs)
    theta = _kappa_of(pairs)
    rng = random.Random(seed)
    reps, undefined = [], 0
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        k = _kappa_of(sample)
        if k != k:                                   # nan
            undefined += 1
        else:
            reps.append(k)
    out = {"n_boot": n_boot, "seed": seed, "undefined_replicates": undefined,
           "method": "BCa", "lo": float("nan"), "hi": float("nan"), "estimable": False}
    if theta != theta or len(reps) < 0.5 * n_boot or not reps:
        out["reason"] = ("kappa is undefined in %d of %d replicates; the resampling "
                         "distribution is degenerate" % (undefined, n_boot))
        return out
    reps.sort()
    # the plain percentile interval is reported alongside BCa, because where the two
    # diverge the divergence is itself information about how unstable the estimate is
    out["percentile_lo"] = reps[max(0, int(math.floor((alpha / 2) * len(reps))))]
    out["percentile_hi"] = reps[min(len(reps) - 1, int(math.ceil((1 - alpha / 2) * len(reps))) - 1)]
    n_less = sum(1 for r in reps if r < theta)
    prop = n_less / len(reps)
    if prop <= 0 or prop >= 1:
        # bias correction is not computable; fall back to the percentile interval
        lo = reps[max(0, int(math.floor((alpha / 2) * len(reps))))]
        hi = reps[min(len(reps) - 1, int(math.ceil((1 - alpha / 2) * len(reps))) - 1)]
        out.update(method="percentile (BCa bias correction not computable)",
                   lo=lo, hi=hi, estimable=True)
        return out
    z0 = _phi_inv(prop)
    # jackknife acceleration
    jack = []
    for i in range(n):
        k = _kappa_of(pairs[:i] + pairs[i + 1:])
        if k == k:
            jack.append(k)
    if len(jack) < 2:
        acc = 0.0
    else:
        m = sum(jack) / len(jack)
        num = sum((m - x) ** 3 for x in jack)
        den = 6 * (sum((m - x) ** 2 for x in jack) ** 1.5)
        acc = num / den if den else 0.0
    za_lo, za_hi = _phi_inv(alpha / 2), _phi_inv(1 - alpha / 2)
    def adj(za):
        d = 1 - acc * (z0 + za)
        return _phi(z0 + (z0 + za) / d) if d != 0 else float("nan")
    a_lo, a_hi = adj(za_lo), adj(za_hi)
    if a_lo != a_lo or a_hi != a_hi:
        return out
    lo = reps[max(0, min(len(reps) - 1, int(math.floor(a_lo * len(reps)))))]
    hi = reps[max(0, min(len(reps) - 1, int(math.ceil(a_hi * len(reps))) - 1))]
    out.update(lo=lo, hi=hi, estimable=True, z0=z0, acceleration=acc)
    return out


def fmt_boot(b):
    if not b.get("estimable"):
        return "not estimable (%s)" % b.get("reason", "degenerate resampling distribution")
    s = "%.2f to %.2f  [%s, %d resamples]" % (b["lo"], b["hi"], b["method"], b["n_boot"])
    if "percentile_lo" in b:
        s += "\n                          plain percentile: %.2f to %.2f" % (
            b["percentile_lo"], b["percentile_hi"])
    return s


def report(title, k, note="", boot=None):
    print("=" * 68)
    print(title)
    if note:
        print("  " + note)
    print("-" * 68)
    print("                     rater2 include   rater2 exclude")
    print(f"  rater1 include  {k['both1']:>10d} {k['a1b0']:>16d}")
    print(f"  rater1 exclude  {k['a0b1']:>10d} {k['both0']:>16d}")
    print("-" * 68)
    print(f"  n = {k['n']}   rater1 includes = {k['r1_include']}   rater2 includes = {k['r2_include']}")
    print(f"  observed agreement  Po = {k['po']:.3f} ({100*k['po']:.1f}%)")
    print(f"  chance agreement    Pe = {k['pe']:.3f}")
    print(f"  Cohen's kappa          = {k['kappa']:.3f}  (asymptotic 95% CI "
          f"{k['kappa_lo']:.2f} to {k['kappa_hi']:.2f})")
    if boot is not None:
        print(f"     bootstrap 95% CI    : {fmt_boot(boot)}")
    print(f"  PABAK                  = {k['pabak']:.3f}")
    print(f"  prevalence index PI    = {k['pi']:.3f}   bias index BI = {k['bi']:.3f}")
    print(f"  positive specific agreement Ppos = {k['ppos']:.3f}")
    print(f"  negative specific agreement Pneg = {k['pneg']:.3f}")
    print()


# ------------------------------------------------------------------- channels
def load_oa(rule="B"):
    """OA full-text code-link mining channel: 163 records (143 code + 20 archive/data)."""
    rows = list(csv.DictReader(open(EK, encoding="utf-8")))
    r1, r2 = [], []
    for r in rows:
        rec_type = (r.get("type") or "").strip().lower()
        r1.append(1 if (r.get("include") or "").strip().lower() in ("yes", "borderline", "y") else 0)
        r2.append(rater2_blind(rec_type, r.get("repo"), r.get("paper"), "", rule))
    return rows, r1, r2


def load_oa_code_only(rule="B"):
    """The same channel restricted to the 143 code repositories.

    Twenty of the 163 records are archive or data links that the extraction denylist
    removes on record type before the scope rule is applied at all. Both raters exclude
    every one of them, so they sit in the (0,0) cell and inflate observed agreement
    without any scope judgment having been made. The 143 are the records the scope
    decision actually ranges over, and reporting kappa on them as well as on the 163
    is what keeps the reliability figure attached to the decision it describes.
    """
    rows = list(csv.DictReader(open(EK, encoding="utf-8")))
    r1, r2 = [], []
    for r in rows:
        rec_type = (r.get("type") or "").strip().lower()
        if rec_type != "code":
            continue
        r1.append(1 if (r.get("include") or "").strip().lower() in ("yes", "borderline", "y") else 0)
        r2.append(rater2_blind(rec_type, r.get("repo"), r.get("paper"), "", rule))
    return rows, r1, r2


def load_github(rule="B"):
    """GitHub Search API + Papers with Code channel: 18 candidate repositories.

    Recorded decisions live in the consolidated inventory: 'yes'/'needs-check'
    entered the census, 'no' (not a study) and 'dedup' (same-study variant of an
    already-included repository) did not.
    """
    ham = list(csv.DictReader(open(HAM, encoding="utf-8")))
    env = {(r["repo"] or "").strip().lower(): (r["include"] or "").strip().lower()
           for r in csv.DictReader(open(ENV, encoding="utf-8"))}
    r1, r2 = [], []
    for r in ham:
        key = (r.get("repo") or "").strip().lower()
        decision = env.get(key)
        if decision is None:
            raise SystemExit(f"[FATAL] no recorded decision for {key} in {ENV.name}")
        r1.append(1 if decision in ("yes", "needs-check") else 0)
        r2.append(rater2_blind("code", r.get("repo"), r.get("paper"), r.get("description"), rule))
    return ham, r1, r2


def main():
    oa_rows, oa1, oa2 = load_oa("B")
    gh_rows, gh1, gh2 = load_github("B")

    _, oc1, oc2 = load_oa_code_only("B")

    k_oa = agreement(oa1, oa2)
    k_oc = agreement(oc1, oc2)
    k_gh = agreement(gh1, gh2)
    k_all = agreement(oa1 + gh1, oa2 + gh2)

    b_oa = bootstrap_kappa(oa1, oa2)
    b_oc = bootstrap_kappa(oc1, oc2)
    b_gh = bootstrap_kappa(gh1, gh2)
    b_all = bootstrap_kappa(oa1 + gh1, oa2 + gh2)

    report(f"CHANNEL 1 — open-access full-text code-link mining (n={k_oa['n']} records)",
           k_oa, "143 code repositories + 20 archive/data links; extreme exclusion prevalence.\n"
                 "  20 of the 163 are archive/data links that BOTH raters exclude on record type\n"
                 "  alone, so that share of the agreement is free of any scope judgment.",
           b_oa)
    report(f"CHANNEL 1b — the same channel, code repositories only (n={k_oc['n']})",
           k_oc, "the 20 archive/data links are dropped before the scope rule applies, so\n"
                 "  this is the subset the scope decision actually ranges over", b_oc)
    report(f"CHANNEL 2 — GitHub Search API + Papers with Code (n={k_gh['n']} repositories)",
           k_gh, "scope-enriched by construction; the discriminative burden is de-duplication "
                 "and\n  is-this-a-study, which an objective rule cannot see", b_gh)
    report(f"POOLED — both scripted channels (n={k_all['n']} screened records)", k_all,
           "the 2 carried-forward repositories are excluded: they were not screening decisions.\n"
           "  UNIT WARNING: these are screened RECORDS, not the 22 repositories or 18 studies\n"
           "  of the census; the pooled figure mixes two channels with opposite prevalence and\n"
           "  should be read with the per-channel values, not alone.", b_all)

    # -------------------------------------------------- rule-revision sensitivity
    _, oaA1, oaA2 = load_oa("A")
    _, ghA1, ghA2 = load_github("A")
    kA_oa, kA_gh = agreement(oaA1, oaA2), agreement(ghA1, ghA2)
    print("=" * 68)
    print("SENSITIVITY — effect of the blind-rule revision (full disclosure)")
    print("=" * 68)
    print("  Rule A (v1): scope evidence = paper title only")
    print("  Rule B (v2): scope evidence = repository name + paper title + description")
    print("-" * 68)
    print(f"{'':24s}{'kappa':>10s}{'Ppos':>10s}{'Po':>10s}{'r2 incl':>10s}")
    for lbl, kk in (("OA mining, rule A", kA_oa), ("OA mining, rule B", k_oa),
                    ("GitHub/PwC, rule A", kA_gh), ("GitHub/PwC, rule B", k_gh)):
        print(f"  {lbl:22s}{kk['kappa']:>10.3f}{kk['ppos']:>10.3f}{kk['po']:>10.3f}{kk['r2_include']:>10d}")
    print("-" * 68)
    print("  Rule A is DEGENERATE on the GitHub/PwC channel: that channel returns no")
    print("  paper titles, so rule A excludes all 18 records by construction. Extending")
    print("  the reliability check to every screened record is why the rule was revised.")
    print("  The revision is not neutral: on the OA channel it raises kappa 0.49 -> 0.79.")
    print("  Both variants are released; neither changes the 0/18 headline (below).")
    print()

    # ------------------------------------------------- provenance reconciliation
    print("=" * 68)
    print("PROVENANCE RECONCILIATION — why the screening 'include' counts are not 22")
    print("=" * 68)
    oa_incl = sum(oa1)
    gh_incl = sum(gh1)
    print(f"  OA mining channel      : {k_oa['n']} records screened "
          f"({sum(1 for r in oa_rows if (r.get('type') or '').strip().lower() == 'code')} code repos, "
          f"{sum(1 for r in oa_rows if (r.get('type') or '').strip().lower() != 'code')} archive/data links)")
    print(f"                           -> {oa_incl} flagged in scope at screening")
    print(f"                           -> 1 dropped at intake vetting (data-only repo, no code)")
    print(f"                           => 5 repositories entered the census")
    print(f"  GitHub/PwC channel     : {k_gh['n']} candidate repositories screened")
    print(f"                           -> {gh_incl} retained (1 non-study personal repo excluded,")
    print(f"                              2 same-study duplicates de-duplicated)")
    print(f"                           => 15 repositories entered the census")
    print(f"  Carried forward        : 2 repositories not surfaced by either scripted channel")
    print(f"                           (masa-open-source, Video-SwinUNet)")
    print(f"                           => 2 repositories entered the census")
    print("-" * 68)
    print(f"  TOTAL CENSUS           : 5 + 15 + 2 = 22 repositories = 18 distinct studies")
    print("  NOTE: VFSS_analysis (deep-dive pilot #1) was ALSO independently surfaced by the")
    print("        GitHub channel, so it is counted there and is not a carried-forward repo.")
    print("=" * 68)

    print("=" * 68)
    print("IN-SAMPLE STATUS (reported with the numbers, not only in the limitations)")
    print("=" * 68)
    print("  The rule specification was revised after observing the agreement it produced,")
    print("  so every kappa above is an IN-SAMPLE measure of how well a stated rule fits the")
    print("  recorded decisions. It is expected to be optimistic and is not an out-of-sample")
    print("  reliability estimate. Both rule variants are released.")
    print("=" * 68)

    OUT.write_text(json.dumps(
        {"rule_B_primary": {"oa_mining": k_oa, "oa_mining_code_only": k_oc,
                            "github_pwc": k_gh, "pooled": k_all},
         "bootstrap_rule_B": {"oa_mining": b_oa, "oa_mining_code_only": b_oc,
                              "github_pwc": b_gh, "pooled": b_all},
         "denylist_sensitivity_note": (
             "kappa was recomputed on the 143 code repositories alone, dropping the 20 "
             "archive/data links that the extraction denylist removes before the scope "
             "rule applies and that both raters therefore exclude on record type. The "
             "value is unchanged to two decimals, so the free agreement those records "
             "contribute is not what carries the figure"),
         "rule_A_sensitivity": {"oa_mining": kA_oa, "github_pwc_degenerate": kA_gh},
         "in_sample": True,
         "in_sample_note": ("the rule specification was revised after observing the "
                            "agreement it produced; the reported kappa is an in-sample "
                            "measure of rule fit and is expected to be optimistic"),
         "free_agreement_note": ("20 of the 163 mining-channel records are archive/data "
                                 "links excluded by both raters on record type alone"),
         "census": {"from_oa_mining": 5, "from_github_pwc": 15, "carried_forward": 2,
                    "repositories": 22, "studies": 18}},
        indent=2), encoding="utf-8")
    print(f"[written] {OUT}")


if __name__ == "__main__":
    main()
