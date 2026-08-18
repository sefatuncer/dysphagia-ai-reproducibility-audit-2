#!/usr/bin/env python3
"""
23_sample_data_audit.py - machine-checkable audit of the "usable sample or test data"
signal, and a drift check on the repositories it reads.

WHY THIS SCRIPT EXISTS
----------------------
Intake (script 08) recorded whether a repository has a directory that looks like a data
directory. It did not record whether that directory holds data. The two are different,
and the difference is the whole point of this study: a directory named `datasets/` that
contains one loader script is a declaration, not an artifact.

Until this script the signal was carried by a hand-coded literal inside script 09, and
that literal was wrong in both directions. Two repositories with an identical recorded
signal (`data_dir=datasets/`) were coded differently, which is what prompted the check.

OPERATIONAL DEFINITION (pre-stated here, applied identically to every repository)
--------------------------------------------------------------------------------
A repository carries USABLE SAMPLE OR TEST DATA if at least one file under a
data-designating directory is a non-empty, non-code, non-documentation file.

  data-designating directory : any path segment whose name contains data, dataset,
        sample, example, demo or test (case-insensitive). This is deliberately
        generous: it favours the audited repository, so the count can only overstate.
  code             : .py .m .r .ipynb .sh .bat .c .cpp .h .hpp .java .js .ts .pl .jl
                     .yaml .yml .json .cfg .ini .toml .make .mk .cmake
  documentation    : .md .rst .html .htm .pdf .tex .bib
  placeholder      : size 0 (.gitkeep and friends)

Everything else counts as data. A repository whose data directory holds only loaders,
only documentation or only placeholders scores 0.

DRIFT CHECK
-----------
Every repository's `pushed_at` is compared with the intake date recorded for it. If a
repository has not been pushed since intake, the tree read today is the tree that was
read at intake, and a difference between this measurement and the recorded coding is a
coding error rather than repository drift. That distinction is reported per repository
and must not be assumed.

Input : repo-intake-table (via paths.py)
Output: sample-data-audit.json
Network: GitHub API, unauthenticated, read-only (trees + repo metadata).
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

INTAKE = inp("repo-intake-table")
OUT = out("sample-data-audit.json")
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
ACCESS_DATE = str(date.today())

DATA_DIR = re.compile(r"(data|dataset|sample|example|demo|test)", re.I)
CODE = {"py", "m", "r", "ipynb", "sh", "bat", "c", "cpp", "h", "hpp", "java",
        "js", "ts", "pl", "jl", "yaml", "yml", "json", "cfg", "ini", "toml",
        "make", "mk", "cmake", "pyc", "mat~"}
DOC = {"md", "rst", "html", "htm", "pdf", "tex", "bib", "txt~"}

# The two in-depth pilots are not in the intake table: they were re-run in full and
# their provisioning is recorded in the re-execution logs, not by the intake script.
# Their coding is stated here with its source rather than inferred from GitHub, because
# the VFSS sample data lives in an external archive that this script does not read.
PILOTS = {
    "BSEL-UC3M/VFSS_analysis": (1, "2026-07-13",
        "sample data ships in the external Zenodo archive, which was downloaded "
        "(6.1 GB) and used for inference; recorded in the pilot write-up"),
    "UofTNeurology/masa-open-source": (0, "2026-07-14",
        "ships neither weights nor data; recorded in the harness verdict log"),
}


def api(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=45).read().decode())
        except urllib.error.HTTPError as e:
            # 409 is what the trees endpoint returns for an empty repository, which is
            # itself one of this study's findings, so it is an answer and not an error.
            if e.code in (404, 409):
                return None
            if e.code in (403, 429) and attempt < 2:
                time.sleep(20)
                continue
            raise
        except Exception:
            if attempt < 2:
                time.sleep(5)
                continue
            raise
    return None


def tree(repo, branch):
    for br in ([branch] if branch else []) + ["main", "master"]:
        t = api("https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (repo, br))
        if t and "tree" in t:
            return t
    return None


def classify(path, size):
    ext = path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    if size == 0:
        return "placeholder"
    if ext in CODE:
        return "code"
    if ext in DOC:
        return "documentation"
    return "data"


def audit(repo, branch, intake_date):
    t = tree(repo, branch)
    if t is None:
        return {"repo": repo, "status": "tree unavailable", "sample_data_usable": None}
    meta = api("https://api.github.com/repos/%s" % repo) or {}
    pushed = (meta.get("pushed_at") or "")[:10]

    counts = {"data": 0, "code": 0, "documentation": 0, "placeholder": 0}
    examples = []
    for node in t.get("tree", []):
        if node.get("type") != "blob":
            continue
        parts = node["path"].split("/")[:-1]
        if not any(DATA_DIR.search(p) for p in parts):
            continue
        kind = classify(node["path"], node.get("size", 0))
        counts[kind] += 1
        if kind == "data" and len(examples) < 3:
            examples.append({"path": node["path"], "bytes": node.get("size", 0)})

    return {
        "repo": repo,
        "status": "read",
        "pushed_at": pushed,
        "intake_date": intake_date,
        # If the repository has not been pushed since intake, today's tree IS the tree
        # that intake saw, so any disagreement is a coding error, not drift.
        "changed_since_intake": bool(pushed and intake_date and pushed > intake_date),
        "files_under_data_dirs": counts,
        "data_file_examples": examples,
        "sample_data_usable": 1 if counts["data"] > 0 else 0,
    }


def main():
    # Resume support. The unauthenticated GitHub limit is 60 calls an hour and this
    # audit needs two per repository, so a run can stop halfway. Previously measured
    # repositories are reused rather than re-read; delete the output file to start over.
    prior = {}
    if OUT.exists():
        try:
            for x in json.loads(OUT.read_text(encoding="utf-8")).get("repositories", []):
                if x.get("status") == "read":
                    prior[x["repo"]] = x
        except Exception:
            prior = {}
    if prior:
        print("  resuming: %d repositories already measured" % len(prior))

    rows = list(csv.DictReader(INTAKE.open(encoding="utf-8-sig")))
    out_rows = []
    stopped = []
    for r in rows:
        repo = r["repo"].strip()
        if not repo:
            continue
        if repo in prior:
            out_rows.append(prior[repo])
            print("  %-62s -> %s  (cached)" % (repo[:62], prior[repo].get("sample_data_usable")))
            continue
        try:
            out_rows.append(audit(repo, r.get("default_branch", "").strip(),
                                  r.get("check_date", "").strip()))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                stopped.append(repo)
                print("  %-62s -> rate limited; re-run later to finish" % repo[:62])
                out_rows.append({"repo": repo, "status": "not read (rate limited)",
                                 "sample_data_usable": None})
                continue
            raise
        print("  %-62s -> %s" % (repo[:62], out_rows[-1].get("sample_data_usable")))

    # The pilots were added to the intake table in v3, so they are normally read above.
    # This block is the fallback for an archive whose table predates that, and it never
    # duplicates a repository the table already carries.
    seen = {x["repo"] for x in out_rows}
    for repo, (val, when, why) in PILOTS.items():
        if repo in seen:
            continue
        out_rows.append({"repo": repo, "status": "recorded (not read from GitHub)",
                         "intake_date": when, "sample_data_usable": val, "source": why})
        print("  %-62s -> %s  (from the re-execution record)" % (repo[:62], val))

    payload = {
        "access_date": ACCESS_DATE,
        "rule": ("a repository carries usable sample or test data if at least one file "
                 "under a data-designating directory is non-empty and is not code or "
                 "documentation; the directory match is deliberately generous"),
        "repositories": out_rows,
        "n_usable": sum(1 for x in out_rows if x.get("sample_data_usable") == 1),
        "n_repositories": len(out_rows),
        "not_read": [x["repo"] for x in out_rows if x.get("sample_data_usable") is None],
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("\n  usable sample or test data: %d of %d repositories"
          % (payload["n_usable"], payload["n_repositories"]))
    print("  written: %s" % OUT)


if __name__ == "__main__":
    main()
