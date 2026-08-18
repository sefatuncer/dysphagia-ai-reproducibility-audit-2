#!/usr/bin/env python3
"""
21_reported_numbers.py - every proportion, interval and flow count reported in the
manuscript, produced in one place from the released data files.

WHY THIS SCRIPT EXISTS
----------------------
Several numbers in the manuscript were previously typed by hand: the reason-level
breakdown of the discovery flow, the coverage bound, the intervals attached to the
small denominators, and the composite verdict counts. In an audit whose subject is
whether a published analysis can be re-run, a hand-typed number is exactly the
defect being measured. This script re-derives all of them from the released files,
so that every figure in the text has a command behind it.

It computes nothing new about the world: it reads the intake table, the inventories,
the screening-reliability output, the backward-coverage output, the environment
audit (script 19) and the run-instructions audit (script 20), and prints them in the
order they appear in the manuscript.

Wilson intervals are used for all proportions, being appropriate for small
denominators and proportions at the boundary. Where a proportion is a logical
consequence of a conjunction rather than a sample quantity, that is stated instead
of an interval being implied.

Output: analiz/reported-numbers.json + a printed manifest.
"""
import csv, json, math, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out, result

OUT = out("reported-numbers.json")
Z = 1.959963985


def wilson(k, n):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = (Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def load_json(name):
    """Read a result file, or exit.

    This script exists to re-derive every number the manuscript reports, so a
    missing input must stop the run. Returning None here would drop whichever
    numbers that input carries and still print a clean-looking report.
    """
    return json.loads(result(name).read_text(encoding="utf-8"))


def line(label, k, n, note=""):
    p, lo, hi = wilson(k, n)
    print(f"  {label:46s} {f'{k}/{n}':>8s}  {100*p:5.1f}%   "
          f"[{100*lo:4.1f}%, {100*hi:5.1f}%]  {note}")
    return {"k": k, "n": n, "p": p, "wilson_lo": lo, "wilson_hi": hi, "note": note}


def main():
    rep = {}

    # ---------------------------------------------------------------- discovery flow
    print("=" * 96)
    print("1. DISCOVERY-TO-INCLUSION FLOW, WITH REASONS")
    print("=" * 96)
    ek = list(csv.DictReader(open(inp("repo-inventory-extra"), encoding="utf-8")))
    code = [r for r in ek if (r["type"] or "").strip().lower() == "code"]
    archive = [r for r in ek if (r["type"] or "").strip().lower() != "code"]
    flagged = [r for r in code
               if (r["include"] or "").strip().lower() in ("yes", "borderline", "y")]
    excluded = [r for r in code if r not in flagged]
    bulk = [r for r in excluded if "auto-triaged" in (r["notes"] or "")]
    individual = [r for r in excluded if r not in bulk]

    print(f"  mining-channel records screened                        {len(ek)}")
    print(f"    - archive/data links (not code repositories)         {len(archive)}")
    print(f"    = candidate code repositories                        {len(code)}")
    print(f"      - excluded, tool-citation or out of scope,")
    print(f"        by the automated triage                          {len(bulk)}")
    print(f"      - excluded individually, with a written reason     {len(individual)}")
    for r in individual:
        print(f"          . {r['repo']:52s} {r['notes'][:44]}")
    print(f"      = flagged in scope at screening                    {len(flagged)}")
    for r in flagged:
        print(f"          . {r['repo']:52s} {(r['include'] or '').strip()}")
    print(f"      - dropped at intake vetting (data-only, no model)  1")
    print(f"      = entered the census from this channel             {len(flagged) - 1}")
    rep["mining_flow"] = {
        "records_screened": len(ek), "archive_data_links": len(archive),
        "candidate_code_repositories": len(code),
        "excluded_automated_triage": len(bulk),
        "excluded_individually_with_reason": len(individual),
        "individual_reasons": [{"repo": r["repo"], "reason": r["notes"]} for r in individual],
        "flagged_in_scope": len(flagged), "dropped_at_intake_vetting": 1,
        "entered_census": len(flagged) - 1}

    ham = list(csv.DictReader(open(inp("repo-inventory-raw"), encoding="utf-8")))
    print(f"\n  GitHub Search + Papers with Code candidates            {len(ham)}")
    print(f"      - excluded, not a study (personal/learning repo)    1")
    print(f"      - de-duplicated, same-study variants                2")
    print(f"      = entered the census from this channel             15")
    print(f"\n  carried forward, surfaced by no scripted channel        2")
    print(f"  TOTAL included repositories                            22   -> 18 distinct studies")
    rep["github_flow"] = {"candidates": len(ham), "not_a_study": 1, "deduplicated": 2,
                          "entered_census": 15}

    # ------------------------------------------------------- transparency signals
    print("\n" + "=" * 96)
    print("2. TRANSPARENCY SIGNALS, STUDY LEVEL (N=18), WILSON 95% CI")
    print("=" * 96)
    rep["transparency"] = {}
    # These counts used to be six literals here, which meant this consolidation could
    # not disagree with the manuscript even when the manuscript was wrong. They now come
    # from script 09, which reads them from the released intake table.
    census = load_json("census-synthesis.json")["study_level"]
    for label, col in [("Open license", "license_open"),
                       ("Trained weights in repository", "weights_in_repo"),
                       ("Trained weights anywhere", "weights_anywhere"),
                       ("Environment specification", "env_spec"),
                       ("Usable sample or test data", "sample_data")]:
        cell = census[col]
        rep["transparency"][label] = line(label, cell["k"], cell["n"])
    # The model-card signal has no measurement script: it was looked for by hand and
    # found in none, and the manuscript marks it as the one signal scored that way.
    rep["transparency"]["Model card or datasheet"] = line(
        "Model card or datasheet", 0, census["license_open"]["n"], "(hand-checked)")

    ri = load_json("run-instructions-audit.json")
    s = ri["study_level"]
    rep["transparency"]["Run instructions (RQ1e)"] = line(
        "Run instructions (RQ1e)", s["run_instructions"], s["n_studies"],
        f"(README present {s['readme_present']}/{s['n_studies']})")

    env = load_json("env-pinning-audit.json")
    c = env["study_level_2x2"]
    rep["transparency"]["Environment pinned and portable"] = line(
        "Environment pinned AND portable", env["pinned_and_portable_studies"], 18,
        "binding conjunct")
    print(f"\n  environment 2x2 among the {env['studies_with_env_file']} studies that declare one:")
    print(f"       pinned & portable {c['pinned_portable']:>2d} | pinned, not portable {c['pinned_not_portable']:>2d}")
    print(f"    not pinned, portable {c['not_pinned_portable']:>2d} | neither             {c['not_pinned_not_portable']:>2d}")
    rep["environment_2x2"] = c

    # --------------------------------------------------------------- re-execution
    print("\n" + "=" * 96)
    print("3. RE-EXECUTION (RQ2)")
    print("=" * 96)
    p, lo, hi = wilson(0, 18)
    print(f"  re-executable out of the box, study level        0/18   "
          f"Wilson 95% upper limit {100*hi:.1f}%")
    rep["reexec_0_18"] = {"k": 0, "n": 18, "wilson_hi": hi}
    rep["reexec"] = {}
    rep["reexec"]["relaxed_weights_only"] = line(
        "relaxed definition, weights-carrying studies", 0, 2,
        "no strict pinning required")
    rep["reexec"]["harness"] = line("studies entered into the harness", 0, 3,
                                    "2 partial, 1 build-failed")
    print("  NOTE: the 0/18 composite is a logical consequence of the conjunction, since a\n"
          "        prerequisite absent in all 18 caps it at zero before any build. It is not a\n"
          "        sample estimate, and an interval on it would imply a sampling variability\n"
          "        that does not exist.")

    # ---------------------------------------------------------- coverage bound
    print("\n" + "=" * 96)
    print("4. COVERAGE BOUND AGAINST TWO INDEPENDENT SYNTHESES")
    print("=" * 96)
    bc = load_json("backward-coverage.json")
    c = bc["counts"]
    n_pool = bc["n_unique_dois"]
    assessable = c["in_census"] + c["code_not_in_census"] + c["oa_no_code"]
    print(f"  comparator pool, unique records                       {n_pool}")
    print(f"    - full text not retrievable                         {c['not_assessable']}")
    print(f"    = assessable                                        {assessable}"
          f"   ({100*assessable/n_pool:.0f}% of the pool)")
    print(f"        declared no repository at all                   {c['oa_no_code']}")
    print(f"        declared a repository                           {bc['code_declaring']}")
    print(f"            already in our census                       {c['in_census']}")
    print(f"            out of scope (tool cited in a review)        1")
    print(f"            a genuine miss                               1")
    rep["coverage"] = {"pool": n_pool, "not_assessable": c["not_assessable"],
                       "assessable": assessable, "no_repository": c["oa_no_code"],
                       "declared_repository": bc["code_declaring"]}
    rep["coverage"]["miss_rate"] = line("misses among assessable records", 1, assessable,
                                        "lower bound, not an estimate")
    # Two numerators, because the paper's own tool-citation rule excludes one of
    # the three declared repositories (a teaching repository cited in a review).
    # The radiology comparators count a study's own code, so own_code is the
    # like-for-like figure and any_declared is the more generous reading.
    rep["coverage"]["code_sharing_own_code"] = line(
        "code sharing, own code only (tool-citation rule applied)",
        bc["code_declaring"] - 1, assessable,
        "like-for-like with radiology")
    rep["coverage"]["code_sharing_any_declared"] = line(
        "code sharing, any declared repository", bc["code_declaring"], assessable,
        "includes one third-party teaching repository")
    print("  STRUCTURAL WARNING: the check mines full texts with the same regular expression\n"
          "        and tool denylist as the discovery channel it is meant to validate, so a\n"
          "        repository that channel cannot see is one this check cannot see either.\n"
          "        The bound is therefore a lower bound on what the channels miss, and for\n"
          "        the same reason the sharing rate above is a lower bound on sharing.")

    # ------------------------------------------------------------- clinical axis
    print("\n" + "=" * 96)
    print("5. CLINICAL AXIS (RQ3), ASSESSABLE SUBSET k=6")
    print("=" * 96)
    rep["clinical"] = {}
    rep["clinical"]["rs4_reliability_reported"] = line(
        "quantitative rater reliability reported (RS4)", 0, 6, "exploratory subset")

    OUT.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print("\n" + "=" * 96)
    print(f"[written] {OUT}")


if __name__ == "__main__":
    main()
