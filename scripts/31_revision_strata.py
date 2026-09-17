# -*- coding: utf-8 -*-
"""Strata, joint patterns and corrected denominators requested in pre-submission review.

Why this exists. A pre-submission review of the manuscript (17 September 2026) found that it
reported every signal for the whole set but for no subset a reader of an imaging
journal would ask about, that it gave the binding conjunct only over all 18 studies
although it is measurable only where an environment file exists, that it capped a
relaxed composite by a single conjunct rather than by the joint pattern, that it gave
the backward-coverage check a denominator of all assessable records rather than of the
in-scope records that declared a repository, and that the clinical reliability item was
reported over six studies although one has no rater at all. Each of those numbers is
computed here from the released tables, so none is typed by hand.

Definitions fixed here, and why.
* Imaging: a repository whose model input is a medical image series: VFSS or other
  radiographic video, cine-MRI, or CT (including radiotherapy-planning CT). Smartphone
  video of a fluid, acoustic, manometric, electromyographic, wearable and tabular
  inputs are non-imaging. A study is imaging if any of its repositories is. The earlier
  count (VFSS and cine-MRI only) is kept as a narrow sensitivity definition, because the
  article reported it.
* Publication-linked: the rule of 29_publication_confirmed_subset.py, unchanged.
* Scripted only: discovery channel other than "carried".
* Signals are aggregated to a study by disjunction, as in 09_census_synthesis.py.

Output: analiz/revision-strata.json -> archive results/

Usage: python analiz/scripts/31_revision_strata.py
"""
import csv
import json
import math
import re
import sys
from itertools import product

from paths import inp, out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

IMAGING = {"VFSS", "VFSS/video", "Cine-MRI", "CT", "RT/imaging"}
IMAGING_NARROW = {"VFSS", "VFSS/video", "Cine-MRI"}
UNCONFIRMED = ("unclear", "could not be confirmed", "needs-check", "scoping candidate")
FEASIBILITY_PILOTS = {"BSEL-UC3M/VFSS_analysis": "2026-07-13",
                      "UofTNeurology/masa-open-source": "2026-07-14"}


def is_confirmed(paper):
    p = (paper or "").strip().lower()
    if not p or any(u in p for u in UNCONFIRMED):
        return False
    return bool(re.search(r"(19|20)\d{2}", p))


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return [round(max(0.0, (c - r) / d), 4), round(min(1.0, (c + r) / d), 4)]


def main():
    studies = list(csv.DictReader(result("included-studies.csv").open(encoding="utf-8-sig")))
    inventory = {r["repo"]: r for r in csv.DictReader(inp("repo-inventory").open(encoding="utf-8-sig"))}
    intake = {r["repo"]: r for r in csv.DictReader(inp("repo-intake-table").open(encoding="utf-8-sig"))}
    pin = json.loads(result("env-pinning-audit.json").read_text(encoding="utf-8"))
    run = json.loads(result("run-instructions-audit.json").read_text(encoding="utf-8"))
    commits = json.loads(result("commit-provenance.json").read_text(encoding="utf-8"))
    cover = json.loads(result("backward-coverage.json").read_text(encoding="utf-8"))
    screen = json.loads(result("screening-reliability.json").read_text(encoding="utf-8"))
    sens = json.loads(result("screening-sensitivity.json").read_text(encoding="utf-8"))

    pin_by_repo = {r["repo"]: r for r in pin["repository_level"]}
    run_by_repo = {r["repo"]: r for r in run["repository_level"]}
    commit_by_repo = {r["repo"]: r for r in commits["repositories"]}

    # ---------------------------------------------------------------- repository level
    repo_rows = []
    for s in studies:
        for repo in [x.strip() for x in s["repositories"].split(";")]:
            inv, it = inventory.get(repo, {}), intake.get(repo, {})
            pr, rr, cm = pin_by_repo.get(repo), run_by_repo.get(repo, {}), commit_by_repo.get(repo, {})
            modality = inv.get("modality", "")
            code_files = (it.get("code_files") or "").strip()
            repo_rows.append({
                "study": s["study_id"], "repo": repo, "modality": modality,
                "imaging": modality in IMAGING,
                "discovery_channel": s["discovery_channel"],
                "feasibility_pilot": repo in FEASIBILITY_PILOTS,
                "intake_method": "by hand, before the scripted intake" if repo in FEASIBILITY_PILOTS else "script",
                "intake_date": FEASIBILITY_PILOTS.get(repo, it.get("check_date") or s["access_dates"]),
                "license_open": (it.get("license_open") or "").strip() == "1",
                "weights_in_repo": (it.get("weights_in_repo") or "").strip() == "1",
                "weights_anywhere": (it.get("weights_anywhere") or "").strip() == "1",
                "env_spec": (it.get("env_spec") or "").strip() == "1",
                "pinned": bool(pr and pr["pinned"]),
                "portable": bool(pr and pr["portable"]),
                "pinned_and_portable": bool(pr and pr["pinned_and_portable"]),
                "sample_data": (it.get("sample_data") or "").strip() == "1",
                "readme": bool(rr.get("readme_present")),
                "run_instructions": bool(rr.get("run_instructions")),
                "code_files": code_files if code_files not in ("", "not measured") else "not measured",
                "commit_on_access_date": cm.get("commit") or ("none (empty repository)" if cm.get("status") != "resolved" else ""),
            })

    # --------------------------------------------------------------------- study level
    SIGNALS = ["license_open", "weights_in_repo", "weights_anywhere", "env_spec", "pinned",
               "portable", "pinned_and_portable", "sample_data", "readme", "run_instructions"]
    study_rows = []
    for s in studies:
        rs = [r for r in repo_rows if r["study"] == s["study_id"]]
        row = {"study": s["study_id"], "paper": s["paper"],
               "repositories": "; ".join(r["repo"] for r in rs),
               "modality": "; ".join(sorted({r["modality"] for r in rs})),
               "imaging": any(r["imaging"] for r in rs),
               "imaging_narrow": any(r["modality"] in IMAGING_NARROW for r in rs),
               "publication_linked": is_confirmed(s["paper"]),
               "discovery_channel": s["discovery_channel"],
               "feasibility_pilot": any(r["feasibility_pilot"] for r in rs),
               "intake_method": "; ".join(sorted({r["intake_method"] for r in rs})),
               "access_dates": s["access_dates"],
               "verdict": s["verdict"]}
        # The study-level table is the published source for these five; recompute the
        # rest from the repository rows by disjunction.
        for f in ("license_open", "weights_in_repo", "weights_anywhere", "env_spec", "sample_data"):
            row[f] = (s[f] or "").strip() == "1"
        for f in ("pinned", "portable", "pinned_and_portable", "readme", "run_instructions"):
            row[f] = any(r[f] for r in rs)
        measured = [r["code_files"] for r in rs if r["code_files"] != "not measured"]
        row["code_file_present"] = (any(int(x) > 0 for x in measured) if measured else "not measured")
        # A conjunction is evaluated within a repository and then aggregated, never the
        # reverse, so two repositories cannot jointly satisfy what neither satisfies.
        row["strict_intake_conjuncts"] = any(r["weights_anywhere"] and r["sample_data"] and r["pinned_and_portable"] for r in rs)
        row["pinned_only_intake_conjuncts"] = any(r["weights_anywhere"] and r["sample_data"] and r["pinned"] for r in rs)
        row["env_declared_intake_conjuncts"] = any(r["weights_anywhere"] and r["sample_data"] and r["env_spec"] for r in rs)
        row["n_prerequisites_env_declared"] = max(int(r["weights_anywhere"]) + int(r["sample_data"]) + int(r["env_spec"]) for r in rs)
        row["n_prerequisites_strict"] = max(int(r["weights_anywhere"]) + int(r["sample_data"]) + int(r["pinned_and_portable"]) for r in rs)
        row["commits"] = "; ".join(r["commit_on_access_date"] for r in rs)
        study_rows.append(row)

    # ------------------------------------------------------------------------- strata
    strata = {
        "all": study_rows,
        "imaging": [r for r in study_rows if r["imaging"]],
        "non_imaging": [r for r in study_rows if not r["imaging"]],
        "imaging_narrow_VFSS_cineMRI": [r for r in study_rows if r["imaging_narrow"]],
        "publication_linked": [r for r in study_rows if r["publication_linked"]],
        "not_publication_linked": [r for r in study_rows if not r["publication_linked"]],
        "scripted_only": [r for r in study_rows if r["discovery_channel"] != "carried"],
    }
    TABLE_SIGNALS = ["license_open", "weights_in_repo", "weights_anywhere", "env_spec",
                     "pinned_and_portable", "sample_data", "run_instructions", "readme"]
    strata_out = {}
    for name, rows in strata.items():
        n = len(rows)
        strata_out[name] = {"n": n, "ids": [r["study"] for r in rows], "signals": {}}
        for f in TABLE_SIGNALS:
            k = sum(1 for r in rows if r[f])
            strata_out[name]["signals"][f] = {"k": k, "n": n, "wilson": wilson(k, n)}
        k = sum(1 for r in rows if r["code_file_present"] is False)
        strata_out[name]["signals"]["no_code_file"] = {"k": k, "n": n, "wilson": wilson(k, n)}
        strata_out[name]["signals"]["model_card"] = {"k": 0, "n": n, "wilson": wilson(0, n),
                                                     "note": "hand-searched, carried unchanged"}
        v = {}
        for r in rows:
            v[r["verdict"]] = v.get(r["verdict"], 0) + 1
        strata_out[name]["verdicts"] = v

    repo_imaging = sum(1 for r in repo_rows if r["imaging"])
    repo_imaging_narrow = sum(1 for r in repo_rows if r["modality"] in IMAGING_NARROW)

    # ------------------------------------------------------------ composite and joints
    env_studies = [r for r in study_rows if r["env_spec"]]
    k_pp = sum(1 for r in env_studies if r["pinned_and_portable"])
    patterns = {}
    for r in study_rows:
        key = "+".join(x for x, on in (("weights", r["weights_anywhere"]), ("sample", r["sample_data"]),
                                       ("env", r["env_spec"])) if on) or "none"
        patterns.setdefault(key, []).append(r["study"])
    dist_env = {str(i): sum(1 for r in study_rows if r["n_prerequisites_env_declared"] == i) for i in range(4)}
    dist_strict = {str(i): sum(1 for r in study_rows if r["n_prerequisites_strict"] == i) for i in range(4)}
    composite = {
        "strict_pinned_and_portable": {
            "intake_upper_bound": sum(r["strict_intake_conjuncts"] for r in study_rows),
            "ids": [r["study"] for r in study_rows if r["strict_intake_conjuncts"]]},
        "pinned_only": {
            "intake_upper_bound": sum(r["pinned_only_intake_conjuncts"] for r in study_rows),
            "ids": [r["study"] for r in study_rows if r["pinned_only_intake_conjuncts"]]},
        "environment_declared": {
            "intake_upper_bound": sum(r["env_declared_intake_conjuncts"] for r in study_rows),
            "ids": [r["study"] for r in study_rows if r["env_declared_intake_conjuncts"]]},
        "observed_verdict_of_those_ids": {r["study"]: r["verdict"] for r in study_rows
                                          if r["pinned_only_intake_conjuncts"] or r["env_declared_intake_conjuncts"]},
        "conditional_pinned_and_portable": {"k": k_pp, "n": len(env_studies), "wilson": wilson(k_pp, len(env_studies)),
                                            "ids_with_environment_file": [r["study"] for r in env_studies]},
        "joint_patterns_weights_sample_env": patterns,
        "n_prerequisites_met_env_declared": dist_env,
        "n_prerequisites_met_strict": dist_strict,
    }

    # -------------------------------------------------------------- backward coverage
    census_repos = {r["repo"].lower(): r for r in repo_rows}
    in_scope = []
    for d in cover["detail"]["in_census"]:
        for m in d.get("matched", []):
            in_scope.append({"doi": d["doi"], "repo": m, "in_set": True,
                             "channel": census_repos.get(m.lower(), {}).get("discovery_channel")})
    for d in cover["detail"]["code_not_in_census"]:
        edu = any("pytorchmedicalai" in x.lower() for x in d["repos"])
        if not edu:
            in_scope.append({"doi": d["doi"], "repo": "; ".join(d["repos"]), "in_set": False, "channel": None})
    n_in_scope = len(in_scope)
    k_instrument = sum(1 for x in in_scope if x["in_set"])
    k_scripted = sum(1 for x in in_scope if x["in_set"] and x["channel"] not in (None, "carried"))
    coverage = {
        "assessable_records": cover["counts"]["in_census"] + cover["counts"]["code_not_in_census"] + cover["counts"]["oa_no_code"],
        "declaring_a_repository": cover["code_declaring"],
        "in_scope_declaring": n_in_scope,
        "educational_tool_excluded": 1,
        "records": in_scope,
        "recall_whole_instrument": {"k": k_instrument, "n": n_in_scope, "wilson": wilson(k_instrument, n_in_scope)},
        "recall_scripted_channels_as_recorded": {"k": k_scripted, "n": n_in_scope, "wilson": wilson(k_scripted, n_in_scope)},
        "note": ("The one in-scope record already in the set is a carried-forward feasibility pilot, "
                 "so on the released record the scripted channels reached neither in-scope record. "
                 "10_code_link_mining.py dropped links already in the inventory before recording "
                 "them, so whether mining also reached it is not recoverable from that record; "
                 "see mining-overlap-check.json."),
    }

    # --------------------------------------------------------------- screening summary
    pooled = screen["rule_B_primary"]["pooled"]
    any_include = pooled["both1"] + pooled["a1b0"] + pooled["a0b1"]
    disagree = pooled["a1b0"] + pooled["a0b1"]
    screening = {
        "rule_vs_record_disagreements": {"k": disagree, "n": pooled["n"]},
        "disagreements_among_records_with_any_include": {"k": disagree, "n": any_include,
                                                         "wilson": wilson(disagree, any_include)},
        "positive_specific_agreement_pooled": round(pooled["ppos"], 3),
        "per_channel": {c: {k: screen["rule_B_primary"][c][k] for k in
                            ("n", "both1", "both0", "a1b0", "a0b1", "po", "kappa", "pabak", "ppos", "pneg")}
                        for c in ("oa_mining", "oa_mining_code_only", "github_pwc", "pooled")},
        "pre_revision_rule_A": {c: {k: v for k, v in screen["rule_A_sensitivity"][c].items()
                                    if k in ("n", "both1", "both0", "a1b0", "a0b1", "po", "kappa", "pabak", "ppos")}
                                for c in screen["rule_A_sensitivity"] if isinstance(screen["rule_A_sensitivity"][c], dict)},
        "bootstrap": {c: {k: screen["bootstrap_rule_B"][c][k] for k in
                          ("n_boot", "seed", "undefined_replicates", "method", "lo", "hi", "percentile_lo", "percentile_hi")}
                      for c in screen["bootstrap_rule_B"]},
        "why_pooled_exceeds_both_channels": ("Recorded inclusion prevalence is 15/18 on GitHub and 6/163 on "
                                             "mining. Pooling lowers expected agreement (pe) below either "
                                             "channel's, so kappa rises for a reason unrelated to how well the "
                                             "rule reproduces decisions within a channel."),
        "pe": {c: round(screen["rule_B_primary"][c]["pe"], 3) for c in ("oa_mining", "github_pwc", "pooled")},
    }

    # ------------------------------------------------------------ sensitivity summary
    # The point shifts are computed from the counts, not from the proportions already rounded to
    # four places in screening-sensitivity.json: rounding twice moved two of them by 0.1 point.
    shifts = []
    exact = []
    for p in sens["proportions"]:
        a = p["published"]["k"] / p["published"]["n"]
        w = p["worst_case_added_all_lack_it"]["k"] / p["worst_case_added_all_lack_it"]["n"]
        b = p["best_case_added_all_have_it"]["k"] / p["best_case_added_all_have_it"]["n"]
        shifts.append({"signal": p["signal"],
                       "worst_case_points": round(100 * (w - a), 1),
                       "best_case_points": round(100 * (b - a), 1)})
        exact.append({"signal": p["signal"], "worst": 100 * (w - a), "best": 100 * (b - a)})
    zero_rows = ("pinned and portable", "all four prerequisites")
    nonzero = [x for x in exact if x["signal"] not in zero_rows]
    # The text quotes these as bounds, so they are rounded away from zero: a bound must not be
    # tighter than the value it bounds.
    ceil1 = lambda x: math.ceil(abs(x) * 10 - 1e-9) / 10 * (1 if x >= 0 else -1)
    sensitivity = {
        "per_signal_point_shift": shifts,
        "max_decrease_points": ceil1(min(x["worst"] for x in nonzero)),
        "max_increase_points_nonzero_signals": ceil1(max(x["best"] for x in nonzero)),
        "max_increase_points_any_signal": ceil1(max(x["best"] for x in exact)),
        "bounds_are_rounded_away_from_zero": True,
    }

    payload = {
        "generated_by": "31_revision_strata.py",
        "definitions": {
            "imaging": sorted(IMAGING), "imaging_narrow": sorted(IMAGING_NARROW),
            "publication_linked": "29_publication_confirmed_subset.py rule",
            "scripted_only": "discovery channel other than carried",
            "feasibility_pilots": FEASIBILITY_PILOTS,
            "carried_forward": "repositories not surfaced by the scripted channels: " +
                               ", ".join(r["repo"] for r in repo_rows if r["discovery_channel"] == "carried"),
        },
        "repositories": {"n": len(repo_rows), "imaging": repo_imaging, "imaging_narrow": repo_imaging_narrow},
        "strata": strata_out,
        "composite": composite,
        "backward_coverage": coverage,
        "screening": screening,
        "sensitivity": sensitivity,
        "study_rows": study_rows,
        "repository_rows": repo_rows,
    }
    p = out("revision-strata.json")
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("  repositories: %d  imaging %d (narrow %d)" % (len(repo_rows), repo_imaging, repo_imaging_narrow))
    hdr = ["all", "imaging", "non_imaging", "publication_linked", "not_publication_linked", "scripted_only"]
    print("  %-22s" % "signal" + "".join("%-14s" % h[:13] for h in hdr))
    for f in TABLE_SIGNALS + ["no_code_file"]:
        print("  %-22s" % f + "".join("%-14s" % ("%d/%d" % (strata_out[h]["signals"][f]["k"], strata_out[h]["n"])) for h in hdr))
    print("  verdicts:", {h: strata_out[h]["verdicts"] for h in hdr})
    print("  composite:", json.dumps({k: v for k, v in composite.items() if k != "joint_patterns_weights_sample_env"}))
    print("  patterns:", json.dumps(patterns))
    print("  coverage:", json.dumps({k: coverage[k] for k in ("recall_whole_instrument", "recall_scripted_channels_as_recorded")}))
    print("  screening:", json.dumps({k: screening[k] for k in ("rule_vs_record_disagreements", "disagreements_among_records_with_any_include", "positive_specific_agreement_pooled", "pe")}))
    print("  sensitivity:", json.dumps({k: v for k, v in sensitivity.items() if k != "per_signal_point_shift"}))
    print("  written: %s" % p)


if __name__ == "__main__":
    main()
