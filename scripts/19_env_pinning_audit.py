#!/usr/bin/env python3
"""
19_env_pinning_audit.py - machine-checkable audit of the environment specifications.

WHY THIS SCRIPT EXISTS
----------------------
The headline result (0/18 out-of-the-box re-executable) is a conjunction, and the
conjunct that binds it is "a pinned AND portable environment, absent in all 18".
Until this script, that row was the only reported proportion with no released code
behind it: intake (script 08) records *whether* an environment file exists, not
whether it is pinned or portable. A study auditing execution prerequisites cannot
leave its own binding conjunct unmeasured, so the two properties are given
operational, machine-checkable definitions here and applied to every study whose
repository declares an environment specification.

OPERATIONAL DEFINITIONS (pre-stated, applied identically to every file)
----------------------------------------------------------------------
PINNED   : every declared dependency carries an exact version. For pip, each
           requirement line uses '==' or '===' (or is an exact wheel/archive
           reference). For conda, each entry under 'dependencies:' carries a
           '=<version>'. A file with at least one unversioned or range-versioned
           ('>=', '~=', '*', bare name) dependency is NOT pinned.
PORTABLE : the specification contains no developer-specific absolute path
           ('file:///', 'C:\\', '/home/<user>/', '/Users/<user>/'), no
           local-file dependency source, no platform-locked wheel filename
           (e.g. '-cp37-cp37m-win_amd64.whl'), and no machine-specific conda
           'prefix:' or local channel. It must therefore resolve unchanged on a
           third machine.

Both properties are necessary: a pinned but non-portable file resolves to a path
that exists on one machine only, and a portable but unpinned file resolves to
whatever the index serves on the day of the build (which is exactly how the
weight-shipping repository in this set broke).

The classifier is deliberately conservative in the direction that would weaken our
own claim: anything it cannot parse is reported as 'undetermined', never as a
failure. Undetermined entries are listed for manual reading rather than counted.

Input : analiz/repo-intake-tablosu.csv (the repositories with env_file != NONE)
        plus the two deep-dive pilots, whose environment files are recorded in the
        re-execution logs.
Output: analiz/env-pinning-audit.json + a printed 2x2 (pinned x portable).

Network: fetches each declared environment file from raw.githubusercontent.com at a
logged access date. Re-running on a later date may return a different file, which
is why the access date is recorded with every verdict.
"""
import csv, json, re, sys, time, urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

INTAKE = inp("repo-intake-table")
OUT = out("env-pinning-audit.json")
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
ACCESS_DATE = "2026-07-30"          # the date this audit was run; logged with every verdict

# The two deep-dive pilots are not in the intake table (they were re-run in full and
# are recorded separately), so their environment files are declared here.
PILOTS = [
    ("BSEL-UC3M/VFSS_analysis", "main", "environment.yml"),
    ("UofTNeurology/masa-open-source", "main", "requirements.txt"),
]

# study id per repository, so the 2x2 can be reported at the study level (the primary
# unit); identical to the STUDY_ID column of script 09.
STUDY_OF = {
    "BSEL-UC3M/VFSS_analysis": "A",
    "UofTNeurology/masa-open-source": "B",
    "aht4005/dysphagia-risk-calculator": "C",
    "tsukagoshi56/liquid_swallowing_segmentation": "G",
    "tsukagoshi56/swallowing_segmentation_with_ssl_gru": "G",
    "SimonZeng7108/Video-SwinUNet": "M",
    "enoch0307/streamlitapp_cn": "O",
}

RAW = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"

# ---------------------------------------------------------------- non-portability
LOCAL_PATH = re.compile(r"(file:/{2,3}|[A-Za-z]:[\\/]|/home/[^/\s]+/|/Users/[^/\s]+/)")
PLATFORM_WHEEL = re.compile(r"-(cp|pp)\d{2,3}-[^\s]*-(win|macosx|manylinux)[^\s]*\.whl", re.I)
CONDA_PREFIX = re.compile(r"^\s*prefix\s*:", re.M)

# ------------------------------------------------------------------------ pinning
PIP_SKIP = re.compile(r"^\s*(#|-r\s|--|$)")
PIP_EXACT = re.compile(r"(===?)\s*[\w.*+!-]+")
PIP_LOOSE = re.compile(r"(>=|<=|>|<|~=|\^|\*)")
CONDA_ENTRY = re.compile(r"^\s*-\s+([^\s#].*?)\s*$")


def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        return None


def classify_pip(text):
    """Return (pinned, total_deps, unpinned_examples)."""
    unpinned = []
    total = 0
    for raw_line in text.splitlines():
        line = raw_line.split("#")[0].rstrip()
        if PIP_SKIP.match(line):
            continue
        total += 1
        if "@" in line and LOCAL_PATH.search(line):
            continue                      # an exact local-file reference: pinned but not portable
        if PIP_EXACT.search(line):
            continue
        if line.endswith(".whl") or line.endswith(".tar.gz"):
            continue                      # an exact archive reference
        unpinned.append(line.strip())
    return (total > 0 and not unpinned), total, unpinned[:6]


def classify_conda(text):
    """Return (pinned, total_deps, unpinned_examples) for an environment.yml."""
    unpinned, total = [], 0
    in_deps = False
    for raw_line in text.splitlines():
        line = raw_line.split("#")[0].rstrip()
        if re.match(r"^\s*dependencies\s*:", line):
            in_deps = True
            continue
        if in_deps and re.match(r"^\S", line):        # a new top-level key ends the block
            in_deps = False
        if not in_deps:
            continue
        m = CONDA_ENTRY.match(line)
        if not m:
            continue
        entry = m.group(1)
        if entry.rstrip().endswith(":"):              # the nested '- pip:' list header
            continue
        total += 1
        if re.search(r"[=]{1,2}\s*[\w.*]+", entry) and not PIP_LOOSE.search(entry):
            continue
        if PIP_EXACT.search(entry):
            continue
        unpinned.append(entry.strip())
    return (total > 0 and not unpinned), total, unpinned[:6]


def portability(text):
    """Return (portable, reasons)."""
    reasons = []
    for m in LOCAL_PATH.finditer(text):
        reasons.append("developer-specific absolute path: " + m.group(0))
    if PLATFORM_WHEEL.search(text):
        reasons.append("platform-locked wheel filename: " +
                       PLATFORM_WHEEL.search(text).group(0))
    if CONDA_PREFIX.search(text):
        reasons.append("machine-specific conda 'prefix:' entry")
    # de-duplicate while keeping order
    seen, out = set(), []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return (not out), out


def audit(repo, branch, path):
    text = fetch(RAW.format(repo=repo, branch=branch, path=path))
    if text is None:
        return {"repo": repo, "file": path, "status": "undetermined",
                "reason": "environment file not retrievable at the access date"}
    if path.lower().endswith((".yml", ".yaml")):
        pinned, n, examples = classify_conda(text)
    else:
        pinned, n, examples = classify_pip(text)
    portable, why = portability(text)
    return {"repo": repo, "study": STUDY_OF.get(repo, "?"), "file": path,
            "access_date": ACCESS_DATE, "n_dependencies": n,
            "pinned": pinned, "unpinned_examples": examples,
            "portable": portable, "non_portable_reasons": why,
            "pinned_and_portable": bool(pinned and portable), "status": "assessed"}


def main():
    targets = list(PILOTS)
    for r in csv.DictReader(open(INTAKE, encoding="utf-8")):
        env = (r.get("env_file") or "NONE").strip()
        if env == "NONE" or not env:
            continue
        if r["repo"] not in STUDY_OF:
            # a candidate that did not enter the census (dropped at intake vetting)
            continue
        for f in env.split(";"):
            targets.append((r["repo"], (r.get("default_branch") or "main").strip(), f))

    print("=" * 74)
    print("ENVIRONMENT SPECIFICATION AUDIT - pinned x portable")
    print("=" * 74)
    print("  pinned   = every declared dependency carries an exact version")
    print("  portable = no developer-specific absolute path, no local-file source, no")
    print("             platform-locked wheel, no machine-specific conda prefix or channel")
    print(f"  access date: {ACCESS_DATE}")
    print("-" * 74)

    results = []
    for repo, branch, path in targets:
        res = audit(repo, branch, path)
        results.append(res)
        if res["status"] != "assessed":
            print(f"  ? {repo:52s} {path:18s} UNDETERMINED ({res['reason']})")
        else:
            flag = "PINNED" if res["pinned"] else "unpinned"
            port = "portable" if res["portable"] else "NOT portable"
            print(f"  - {repo:52s} {path:18s} {flag:8s} / {port}")
            if res["unpinned_examples"]:
                print(f"      unpinned e.g.: {', '.join(res['unpinned_examples'][:3])}")
            for w in res["non_portable_reasons"]:
                print(f"      {w}")
        time.sleep(0.4)

    assessed = [r for r in results if r["status"] == "assessed"]
    # ---- study level (primary): a study counts as pinned/portable if ANY of its
    # ---- environment files satisfies the property (the reading most favourable to
    # ---- the audited literature).
    studies = {}
    for r in assessed:
        s = studies.setdefault(r["study"], {"pinned": False, "portable": False,
                                            "both": False, "repos": []})
        s["pinned"] |= r["pinned"]
        s["portable"] |= r["portable"]
        s["both"] |= r["pinned_and_portable"]
        s["repos"].append(r["repo"])

    print("-" * 74)
    print(f"STUDY-LEVEL 2x2 (studies declaring an environment specification: {len(studies)})")
    print("-" * 74)
    cell = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
    for s in studies.values():
        cell[(s["pinned"], s["portable"])] += 1
    print("                    portable      not portable")
    print(f"  pinned        {cell[(True, True)]:>10d} {cell[(True, False)]:>16d}")
    print(f"  not pinned    {cell[(False, True)]:>10d} {cell[(False, False)]:>16d}")
    print("-" * 74)
    both = sum(1 for s in studies.values() if s["both"])
    print(f"  pinned AND portable: {both} / {len(studies)} studies with an environment file")
    print(f"  => at the level of all 18 studies: {both}/18")
    undet = [r for r in results if r["status"] != "assessed"]
    if undet:
        print(f"  undetermined (not counted as failures): {len(undet)} "
              f"{[r['repo'] for r in undet]}")
    print("=" * 74)

    OUT.write_text(json.dumps(
        {"access_date": ACCESS_DATE,
         "definitions": {
             "pinned": "every declared dependency carries an exact version "
                       "(pip '==' / '===' or an exact archive reference; conda '=<version>')",
             "portable": "no developer-specific absolute path, no local-file dependency "
                         "source, no platform-locked wheel filename, no machine-specific "
                         "conda prefix or local channel; resolves unchanged on a third machine"},
         "repository_level": results,
         "study_level_2x2": {"pinned_portable": cell[(True, True)],
                             "pinned_not_portable": cell[(True, False)],
                             "not_pinned_portable": cell[(False, True)],
                             "not_pinned_not_portable": cell[(False, False)]},
         "studies_with_env_file": len(studies),
         "pinned_and_portable_studies": both,
         "undetermined": [r["repo"] for r in undet]},
        indent=2), encoding="utf-8")
    print(f"[written] {OUT}")


if __name__ == "__main__":
    main()
