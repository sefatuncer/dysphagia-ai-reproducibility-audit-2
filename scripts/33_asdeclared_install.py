# -*- coding: utf-8 -*-
"""As-declared install attempt for every release that declares an environment but was never built.

Why this exists. The three builds of July 2026 covered two repositories that met the entry
condition and one feasibility pilot. Three further releases declare an environment file and
were never built, because none ships trained weights, so none could reach inference. A
pre-submission review of the manuscript (17 September 2026) asked for the install step to be tried for all of them
under one protocol, so that "code that installs" is observed rather than left unmeasured
wherever an environment is declared. This script does that and nothing more: it tries to
install what the repository declares; it does not repair, and it does not run the code.

What is held fixed, and what is not. Each requirements file is taken from the commit the
repository pointed at on its logged access date (results/commit-provenance.json), so the
repository side does not drift. The package index is read on the day this script runs, so
a dependency declared without an exact version resolves to whatever the index serves that
day; that is part of what an as-declared install tests, and the run date is recorded.

Protocol, identical for every target: base image python:3.10-slim, recorded by digest. The
environment files name no interpreter version, but other files do: a development-container
file in aht4005 names Python 3.11, the tsukagoshi56 READMEs ask for Python 3.9 or later (one
shows a conda environment with 3.10), and the Video-SwinUNet README shows a conda environment
with Python 3.8. One image is used for all, and the only failure is a line pip cannot parse,
which no interpreter version avoids. README steps outside the environment file (such as a
CUDA-specific index for PyTorch) are not followed, because the file is what is tested.
Then: COPY the requirements file; `pip --version`; then
`pip install --no-cache-dir -r requirements.txt`, with network access during the build,
no retries, no index changes, and no edits to the file. Outcome: installed (exit 0) or
failed (non-zero), with the first pip error line.

Two checks follow a successful install, both with the network off, because pip exiting 0
does not show that the environment is usable: `pip check`, which reports installed packages
whose declared requirements are not met, and an import of every declared distribution under
its import name, which shows whether the resolved versions load together. Neither runs the
repository's own code.

Requires Docker. Not part of scripts/reproduce.py, which must run without it.

Output: analiz/asdeclared-install.json -> archive results/
        analiz/rerun-loglari/install-checks/<target>.log and Dockerfile -> archive re-execution/logs/install-checks/

Usage: python analiz/scripts/33_asdeclared_install.py
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from paths import BASE, out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_IMAGE = "python:3.10-slim"
TARGETS = [
    # study, repository, environment file in the repository
    ("C", "aht4005/dysphagia-risk-calculator", "requirements.txt"),
    ("G", "tsukagoshi56/liquid_swallowing_segmentation", "requirements.txt"),
    ("G", "tsukagoshi56/swallowing_segmentation_with_ssl_gru", "requirements.txt"),
    ("M", "SimonZeng7108/Video-SwinUNet", "requirements.txt"),
]
DOCKERFILE = """FROM {image}
WORKDIR /w
COPY requirements.txt .
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt
"""
LOG_DIR_WORKING = BASE / "analiz" / "rerun-loglari" / "install-checks"
# distribution name -> import name, where the two differ
IMPORT_NAME = {"scikit-learn": "sklearn", "sklearn": "sklearn", "pillow": "PIL",
               "ml-collections": "ml_collections", "opencv-python": "cv2", "simpleitk": "SimpleITK"}
IMPORT_PROBE = r'''
import importlib, json, sys
out = {}
for mod in sys.argv[1:]:
    try:
        m = importlib.import_module(mod)
        out[mod] = "ok " + str(getattr(m, "__version__", ""))
    except BaseException as e:
        out[mod] = "%s: %s" % (type(e).__name__, str(e).splitlines()[0][:200] if str(e) else "")
print(json.dumps(out))
'''


def declared_imports(req_text):
    mods = []
    for ln in req_text.splitlines():
        ln = ln.split("#")[0].strip()
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9_.\-]*)", ln)
        if not m:
            continue
        name = m.group(1)
        mod = IMPORT_NAME.get(name.lower(), name.replace("-", "_"))
        if mod not in mods:
            mods.append(mod)
    return mods


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def resolved_versions(log):
    """Package versions pip reports in its 'Successfully installed' line."""
    m = re.search(r"Successfully installed (.+)", log)
    if not m:
        return None
    pairs = {}
    for tok in m.group(1).split():
        name, _, ver = tok.rpartition("-")
        if name:
            pairs[name] = ver
    return pairs


def redact(text):
    """Remove host-specific paths, which identify a machine account and add nothing."""
    text = re.sub(r"[A-Za-z]:\\\\?Users\\\\?[^\\\s\"']+", "<host-path>", text)
    text = re.sub(r"/c/Users/[^/\s\"']+", "<host-path>", text)
    text = re.sub(r"/Users/[^/\s\"']+", "<host-path>", text)
    return text


def main():
    commits = {r["repo"]: r for r in json.loads(result("commit-provenance.json").read_text(encoding="utf-8"))["repositories"]}
    LOG_DIR_WORKING.mkdir(parents=True, exist_ok=True)
    work = LOG_DIR_WORKING / "_build"
    work.mkdir(exist_ok=True)

    pull = sh(["docker", "pull", "-q", BASE_IMAGE])
    digest = sh(["docker", "image", "inspect", BASE_IMAGE, "--format", "{{index .RepoDigests 0}}"]).stdout.strip()
    docker_version = sh(["docker", "version", "--format", "{{.Server.Version}}"]).stdout.strip()
    docker_host = sh(["docker", "info", "--format", "{{.OperatingSystem}} | {{.Architecture}} | {{.NCPU}} CPUs | {{.MemTotal}} bytes"]).stdout.strip()
    print("  base image %s  digest %s" % (BASE_IMAGE, digest))
    print("  docker %s  (%s)" % (docker_version, docker_host))

    rows = []
    for study, repo, envfile in TARGETS:
        cm = commits[repo]
        sha = cm["commit"]
        tag = "audit-install-" + re.sub(r"[^a-z0-9]+", "-", repo.lower())
        name = repo.replace("/", "__")
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, sha, envfile)
        req = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "dysphagia-repro-audit"}), timeout=60).read()
        d = work / name
        d.mkdir(exist_ok=True)
        (d / "requirements.txt").write_bytes(req)
        dockerfile = DOCKERFILE.format(image=digest or BASE_IMAGE)
        (d / "Dockerfile").write_text(dockerfile, encoding="utf-8")

        started = datetime.datetime.now(datetime.timezone.utc)
        t0 = time.time()
        proc = sh(["docker", "build", "--no-cache", "--progress=plain", "-t", tag, "."], cwd=d)
        seconds = round(time.time() - t0)
        log = redact(proc.stdout + proc.stderr)
        (LOG_DIR_WORKING / (name + ".log")).write_text(log, encoding="utf-8")
        (LOG_DIR_WORKING / (name + ".Dockerfile")).write_text(dockerfile, encoding="utf-8")
        (LOG_DIR_WORKING / (name + ".requirements.txt")).write_bytes(req)

        errors = [ln.strip() for ln in log.splitlines() if re.search(r"\bERROR\b|error:", ln)]
        pip_err = [e for e in errors if "pip" in e.lower() or "requirement" in e.lower() or "ERROR:" in e]
        size = None
        pip_check = imports = None
        if proc.returncode == 0:
            size = sh(["docker", "image", "inspect", tag, "--format", "{{.Size}}"]).stdout.strip()
            pc = sh(["docker", "run", "--rm", "--network", "none", tag, "pip", "check"])
            pip_check = {"exit_code": pc.returncode,
                         "lines": [ln.strip() for ln in (pc.stdout + pc.stderr).splitlines() if ln.strip()][:20]}
            mods = declared_imports(req.decode("utf-8", "replace"))
            ip = sh(["docker", "run", "--rm", "--network", "none", tag, "python", "-c", IMPORT_PROBE] + mods)
            try:
                imports = json.loads(ip.stdout.strip().splitlines()[-1])
            except Exception:
                imports = {"probe_failed": redact((ip.stdout + ip.stderr).strip())[:400]}
            with open(LOG_DIR_WORKING / (name + ".log"), "a", encoding="utf-8") as f:
                f.write("\n\n### pip check (network off), exit %d\n%s\n" % (pc.returncode, redact(pc.stdout + pc.stderr)))
                f.write("\n### import of declared distributions (network off)\n%s\n" % json.dumps(imports, indent=1))
            sh(["docker", "rmi", "-f", tag])
        row = {
            "study": study, "repo": repo, "environment_file": envfile,
            "commit": sha, "access_date": cm["access_date"],
            "requirements_sha256": hashlib.sha256(req).hexdigest(),
            "requirements_lines": [ln for ln in req.decode("utf-8", "replace").splitlines() if ln.strip()],
            "base_image": BASE_IMAGE, "base_image_digest": digest,
            "built_utc": started.isoformat(timespec="seconds"), "seconds": seconds,
            "exit_code": proc.returncode,
            "outcome": "installed" if proc.returncode == 0 else "failed",
            "first_error": (pip_err or errors or [None])[0],
            "image_size_bytes": int(size) if size and size.isdigit() else None,
            "pip_check": pip_check,
            "imports": imports,
            "all_declared_imports_load": (all(str(v).startswith("ok") for v in imports.values())
                                          if isinstance(imports, dict) and imports else None),
            "resolved_versions": resolved_versions(log),
            "log": "re-execution/logs/install-checks/%s.log" % name,
        }
        rows.append(row)
        print("  %-2s %-52s %-9s %5ds  %s | pip check %s | imports %s"
              % (study, repo[:52], row["outcome"], seconds, (row["first_error"] or "")[:90],
                 pip_check and pip_check["exit_code"], row["all_declared_imports_load"]))

    by_study = {}
    for r in rows:
        by_study.setdefault(r["study"], []).append(r["outcome"] == "installed")
    payload = {
        "generated_by": "33_asdeclared_install.py",
        "run_on": datetime.date.today().isoformat(),
        "protocol": ("as-declared install of the repository's own environment file, taken from the "
                     "commit current on the access date, in a fresh python:3.10-slim container; no "
                     "repair, no index change; after a successful install, pip check and an import of "
                     "every declared distribution with the network off; the repository's code not run"),
        "base_image": BASE_IMAGE, "base_image_digest": digest,
        "docker_version": docker_version, "docker_host": docker_host,
        "why": ("Three releases declared an environment file but were never built, because none ships "
                "trained weights. Installing what they declare observes the install half of the fourth "
                "conjunct for every release that declares an environment."),
        "limits": ("The repository side is fixed at the access-date commit; the package index is read on "
                   "the run date, so unpinned dependencies resolve to that day's versions. A successful "
                   "install, a clean pip check and loadable imports do not show that the code runs."),
        "n_targets": len(rows),
        "n_installed": sum(r["outcome"] == "installed" for r in rows),
        "n_pip_check_clean": sum(1 for r in rows if r["pip_check"] and r["pip_check"]["exit_code"] == 0),
        "n_imports_load": sum(1 for r in rows if r["all_declared_imports_load"]),
        "study_level": {s: ("installed" if any(v) else "failed") for s, v in by_study.items()},
        "rows": rows,
    }
    p = out("asdeclared-install.json")
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n  installed: %d of %d repositories; by release: %s" % (payload["n_installed"], len(rows), payload["study_level"]))
    print("  written: %s" % p)


if __name__ == "__main__":
    main()
