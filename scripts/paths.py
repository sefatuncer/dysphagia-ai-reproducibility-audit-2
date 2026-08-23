#!/usr/bin/env python3
"""Input and output paths, resolved for whichever layout the scripts are run from.

These scripts run from two directory layouts, and the file names differ between
them because the published archive uses English names:

    working tree                      published archive
    --------------------------------  -----------------------------------------
    analiz/scripts/<script>.py        scripts/<script>.py
    analiz/repo-envanteri-ek.csv      search/repo-inventory-extra.csv
    analiz/repo-envanteri-ham.csv     search/repo-inventory-raw.csv
    analiz/repo-envanteri.csv         search/repo-inventory.csv
    analiz/repo-intake-tablosu.csv    transparency/repo-intake-table.csv
    kaynaklar/kwok-24-eslesme.csv     search/comparator-pool/kwok-24-matches.csv
    kaynaklar/codas-eslesme.csv       search/comparator-pool/codas-matches.csv
    analiz/<name>.json                results/<name>.json

Callers ask for a logical name and get whichever copy is present.

A missing input raises SystemExit. That is deliberate and is the point of this
module: an earlier version of these scripts resolved paths relative to the
working tree only, so running them from inside the published archive raised
FileNotFoundError, and one script guarded a missing input with `if exists()`
and reported a zero instead. In an audit of whether published analyses can be
re-run, an absent input must stop the run loudly rather than produce a number
that looks like a finding.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_UP1 = _HERE.parent

# The archive puts scripts/ beside search/ and transparency/; the working tree
# puts analiz/scripts/ inside analiz/, which sits beside kaynaklar/.
IN_ARCHIVE = (_UP1 / "search").is_dir() and (_UP1 / "transparency").is_dir()

if IN_ARCHIVE:
    BASE = _UP1
    RESULTS = BASE / "results"
    LAYOUT = "archive"
else:
    ANALIZ = _UP1
    BASE = _UP1.parent
    RESULTS = ANALIZ
    LAYOUT = "working tree"

# logical name -> (path in archive, path in working tree), each relative to BASE
_INPUTS = {
    "repo-inventory-extra": ("search/repo-inventory-extra.csv",
                             "analiz/repo-envanteri-ek.csv"),
    "repo-inventory-raw":   ("search/repo-inventory-raw.csv",
                             "analiz/repo-envanteri-ham.csv"),
    # These two resolve to the English source rather than the authors' Turkish working
    # copy, for the same reason rs-taxonomy-coding does: RELEASE/_source-en is what the
    # archive publishes, so a script that read the Turkish copy would produce numbers the
    # archive cannot reproduce. Both Turkish copies are behind the English ones (the
    # inventory lacks the include_reason column; the intake table lacks the "not measured"
    # correction for the two carried-forward pilots), which is exactly the drift this
    # arrangement prevents.
    "repo-inventory":       ("search/repo-inventory.csv",
                             "RELEASE/_source-en/search/repo-inventory.csv"),
    "repo-intake-table":    ("transparency/repo-intake-table.csv",
                             "RELEASE/_source-en/transparency/repo-intake-table.csv"),
    # The clinical coding is authored in Turkish and translated once for release; the
    # English rendering is the one the manuscript reports, so it is the one read here.
    "rs-taxonomy-coding":   ("transparency/rs-taxonomy-coding.csv",
                             "RELEASE/_source-en/transparency/rs-taxonomy-coding.csv"),
    "kwok-matches":         ("search/comparator-pool/kwok-24-matches.csv",
                             "kaynaklar/kwok-24-eslesme.csv"),
    "codas-matches":        ("search/comparator-pool/codas-matches.csv",
                             "kaynaklar/codas-eslesme.csv"),
    # Written by script 06 rather than read, so it is resolved through dest() below.
    "backward-citation-additions": (
        "search/corpus-metadata/backward-citation-additions.csv",
        "kaynaklar/arama-sonuclari/backward-citation-additions.csv"),
}

_IDX = 0 if IN_ARCHIVE else 1


def inp(name):
    """Path to a required input file. Exits if it is not there."""
    try:
        rel = _INPUTS[name][_IDX]
    except KeyError:
        sys.exit(f"paths.py: unknown input name {name!r}")
    p = BASE / rel
    if not p.exists():
        sys.exit(f"paths.py: required input {name!r} not found at {p}\n"
                 f"  layout detected: {LAYOUT}\n"
                 f"  this run cannot produce the reported numbers; fix the input, "
                 f"do not skip it.")
    return p


def out(filename):
    """Path to write a result file to, creating the directory if needed."""
    RESULTS.mkdir(parents=True, exist_ok=True)
    return RESULTS / filename


def dest(name):
    """Where a mapped file belongs in this layout, whether or not it exists yet.

    inp() is for reading and refuses to continue when the file is absent. A script that
    regenerates a published file needs the same two-layout resolution without that
    check, so that re-running it from inside the archive writes beside the copy it
    would replace instead of crashing on a working-tree directory that is not there.
    """
    try:
        rel = _INPUTS[name][_IDX]
    except KeyError:
        sys.exit(f"paths.py: unknown input name {name!r}")
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def require_unarchived(rel, why):
    """Guard for an input that is deliberately absent from the published archive.

    The discovery and screening scripts read the enriched corpus, which carries the
    abstracts the bibliographic services returned and is not ours to republish. Running
    them from inside the archive therefore cannot work, and the failure must say why:
    a bare FileNotFoundError invites the reader to assume the archive is broken, when
    the omission is a stated content policy. The manuscript reports this layer as
    reissuable from the released queries but not reproducible from a snapshot.
    """
    p = BASE / rel if not str(rel).startswith(str(BASE)) else Path(rel)
    if p.exists():
        return p
    sys.exit(f"{Path(rel).name} is not part of the published archive.\n"
             f"  reason : {why}\n"
             f"  layout : {LAYOUT}\n"
             f"  looked : {p}\n"
             f"  This step can be re-issued from the released queries and retrieval\n"
             f"  dates, but it cannot be reproduced from the published snapshot. That\n"
             f"  is stated in the article and in the self-audit checklist; it is not a\n"
             f"  missing file.")


def result(filename, required=True):
    """Path to read a previously written result file from."""
    p = RESULTS / filename
    if required and not p.exists():
        sys.exit(f"paths.py: expected result {filename!r} not found at {p}\n"
                 f"  layout detected: {LAYOUT}\n"
                 f"  run the script that produces it first.")
    return p
