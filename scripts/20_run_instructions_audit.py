#!/usr/bin/env python3
"""
20_run_instructions_audit.py - machine-checkable audit of run instructions (RQ1e).

WHY THIS SCRIPT EXISTS
----------------------
RQ1 asks for five transparency signals, and (e) run instructions was the only one
never tabulated: intake (script 08) records whether a README file exists, which is
not the same question. This script answers the question that was asked, with a
pre-stated and machine-checkable definition, so that RQ1(e) is reported rather than
deferred to the codebook.

OPERATIONAL DEFINITION (applied identically to every repository)
---------------------------------------------------------------
README PRESENT      : a README file exists at the repository root.
RUN INSTRUCTIONS    : the README contains at least one imperative invocation of the
                      artifact, that is, a recognisable install or run command
                      (pip/conda/poetry install, docker build/run, make, a
                      'python <script>' or 'streamlit/uvicorn/flask run' call, or an
                      npm/yarn script) **inside a code context** (a fenced block, an
                      inline code span, an indented code line, or a shell-prompt
                      line), OR a section heading from the fixed set {usage, getting
                      started, how to run, quick start, installation, running,
                      inference, demo, train}.
                      Restricting commands to code contexts is deliberate: matching
                      them in running prose produced false positives on ordinary
                      English ('make more accurate', 'make it possible').
                      Presence of a command is what is measured, not whether the
                      command is correct, complete, or sufficient. This is a weak,
                      generous criterion, chosen deliberately: it can only overstate
                      how well this literature documents execution.

The criterion is generous in the direction that weakens our own claim, which is the
same convention used for every other signal in this audit.

Input : analiz/repo-intake-tablosu.csv (the census repositories and their branches)
        plus the two deep-dive pilots, which intake skips.
Output: analiz/run-instructions-audit.json + a printed study-level summary.

Network: fetches each README from raw.githubusercontent.com at a logged access date.
"""
import csv, json, re, sys, time, urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from paths import inp, out

INTAKE = inp("repo-intake-table")
OUT = out("run-instructions-audit.json")
UA = {"User-Agent": "MakaleC-repro/1.0 (mailto:tuncersefa@gmail.com)"}
ACCESS_DATE = "2026-07-30"

RAW = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"
README_NAMES = ["README.md", "readme.md", "README.MD", "README.rst", "README.txt",
                "README", "Readme.md", "README.markdown"]

# Repository -> study id, identical to the STUDY_ID column of script 09. The two
# pilots (A, B) are added here because intake skips them.
STUDY_OF = {
    "BSEL-UC3M/VFSS_analysis": "A",
    "UofTNeurology/masa-open-source": "B",
    "aht4005/dysphagia-risk-calculator": "C",
    "MinghaoSam/SwallowingFunctionAnalysis": "D",
    "scut-jol/CFSCNet": "E",
    "scut-jol/swallow_segment_system": "E",
    "kwahid/ABAS_swallowing_structures": "F",
    "tsukagoshi56/liquid_swallowing_segmentation": "G",
    "tsukagoshi56/swallowing_segmentation_meanteacher": "G",
    "tsukagoshi56/swallowing_segmentation_with_ssl_gru": "G",
    "zhengfj1994/dysphagia-viscosity-classifier": "H",
    "arivv22/ai-swallowing-sound-classification": "I",
    "Kai-Washino/swallowing-recognition-DLmachine": "J",
    "YashC1308/Larynx-Prediction-using-sEMG-data": "K",
    "TanishqJoshi/Larynx-Function-prediction-using-W-KNN-on-sEMG-data": "K",
    "20206666/Classification-of-chewing-and-swallowing": "L",
    "SimonZeng7108/Video-SwinUNet": "M",
    "ResearchgroupMITI/swallow-detection": "N",
    "enoch0307/streamlitapp_cn": "O",
    "yonghunsong/Throat-related-events-classification": "P",
    "ruaeh/Dysphagia-ML": "Q",
    "PRI2MA/DL_NTCP_Dysphagia": "R",
}
PILOT_BRANCH = {"BSEL-UC3M/VFSS_analysis": "main", "UofTNeurology/masa-open-source": "main"}

CMD = re.compile(
    r"(pip3?\s+install|conda\s+(env\s+create|create|install)|poetry\s+install|"
    r"docker\s+(build|run|compose)|make\s+\w+|python3?\s+[\w./-]+\.py|"
    r"streamlit\s+run|uvicorn\s+|flask\s+run|npm\s+(run|install)|yarn\s+\w+|"
    r"bash\s+[\w./-]+\.sh|sh\s+[\w./-]+\.sh)", re.I)
HEADING = re.compile(
    r"^\s{0,3}#{1,6}\s*.*\b(usage|getting started|how to run|quick ?start|installation|"
    r"install|running|run the|inference|demo|train(ing)?)\b", re.I | re.M)


FENCED = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE = re.compile(r"`[^`\n]+`")
PROMPT = re.compile(r"^\s*(?:\$|>|PS>)\s+.+$", re.M)
INDENTED = re.compile(r"^(?: {4}|\t).+$", re.M)


def code_regions(text):
    """Return only the parts of the README that are code, so that a command matched in
    running English prose is not counted as a run instruction."""
    parts = []
    for rx in (FENCED, INLINE, PROMPT, INDENTED):
        parts.extend(m.group(0) for m in rx.finditer(text))
    return "\n".join(parts)


def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception:
        return None


def audit(repo, branch):
    for name in README_NAMES:
        text = fetch(RAW.format(repo=repo, branch=branch, path=name))
        if text is not None:
            cmd = CMD.search(code_regions(text))
            head = HEADING.search(text)
            return {"repo": repo, "study": STUDY_OF.get(repo, "?"), "access_date": ACCESS_DATE,
                    "readme": name, "readme_present": True, "n_chars": len(text),
                    "command_found": bool(cmd),
                    "command_example": (cmd.group(0).strip() if cmd else ""),
                    "section_found": bool(head),
                    "section_example": (head.group(0).strip()[:60] if head else ""),
                    "run_instructions": bool(cmd or head)}
        time.sleep(0.2)
    return {"repo": repo, "study": STUDY_OF.get(repo, "?"), "access_date": ACCESS_DATE,
            "readme": None, "readme_present": False, "n_chars": 0,
            "command_found": False, "command_example": "",
            "section_found": False, "section_example": "", "run_instructions": False}


def main():
    targets = [(r, PILOT_BRANCH[r]) for r in PILOT_BRANCH]
    for r in csv.DictReader(open(INTAKE, encoding="utf-8")):
        if r["repo"] in STUDY_OF and r["repo"] not in PILOT_BRANCH:
            targets.append((r["repo"], (r.get("default_branch") or "main").strip()))

    print("=" * 76)
    print("RUN-INSTRUCTIONS AUDIT (RQ1e)")
    print("=" * 76)
    print("  run instructions = README contains an install/run command OR a usage-type")
    print("                     section heading (a deliberately generous criterion)")
    print(f"  access date: {ACCESS_DATE}   repositories: {len(targets)}")
    print("-" * 76)

    results = []
    for repo, branch in targets:
        res = audit(repo, branch)
        results.append(res)
        mark = "yes" if res["run_instructions"] else "NO "
        detail = res["command_example"] or res["section_example"] or (
            "" if res["readme_present"] else "no README at the repository root")
        print(f"  {mark}  {repo:62s} {detail[:34]}")
        time.sleep(0.3)

    # ---- study level (primary): a study carries the signal if ANY of its repositories does
    studies_ri, studies_rd = {}, {}
    for r in results:
        studies_ri[r["study"]] = studies_ri.get(r["study"], False) or r["run_instructions"]
        studies_rd[r["study"]] = studies_rd.get(r["study"], False) or r["readme_present"]

    n_studies = len(studies_ri)
    k_ri = sum(1 for v in studies_ri.values() if v)
    k_rd = sum(1 for v in studies_rd.values() if v)
    k_repo_ri = sum(1 for r in results if r["run_instructions"])
    print("-" * 76)
    print(f"  README present      : {k_rd}/{n_studies} studies "
          f"({sum(1 for r in results if r['readme_present'])}/{len(results)} repositories)")
    print(f"  Run instructions    : {k_ri}/{n_studies} studies "
          f"({k_repo_ri}/{len(results)} repositories)")
    print("  NOTE: presence of a command is measured, not its correctness or sufficiency.")
    print("=" * 76)

    OUT.write_text(json.dumps(
        {"access_date": ACCESS_DATE,
         "definition": "README contains an install/run command or a usage-type section "
                       "heading; presence is measured, not correctness or sufficiency",
         "repository_level": results,
         "study_level": {"n_studies": n_studies,
                         "readme_present": k_rd, "run_instructions": k_ri},
         "repo_level": {"n_repositories": len(results),
                        "readme_present": sum(1 for r in results if r["readme_present"]),
                        "run_instructions": k_repo_ri}},
        indent=2), encoding="utf-8")
    print(f"[written] {OUT}")


if __name__ == "__main__":
    main()
