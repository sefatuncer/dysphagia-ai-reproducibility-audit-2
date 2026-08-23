# -*- coding: utf-8 -*-
"""What the journal asked for, what the paper declared, and what the repository held.

Why this exists. The article observed that a resolving code link does not guarantee a
runnable artifact, and drew a conclusion about sharing policy from it. That conclusion
needs the policy in the frame, and for most of the audited set there is no policy to
speak of: only 7 of the 18 could be tied to an identified publication, and a repository
found by a GitHub keyword search answers to no journal at all. This script builds the
mapping for the 7 where the question is defined, so the claim rests on the subset that
can carry it.

Three columns, three sources. The journal's data and code policy is read from the
publisher's author guidance at the URL recorded below. The availability statement is
taken verbatim from the article's own full text through Europe PMC where the full text
is open; where it is not, the field records that it could not be retrieved rather than
being filled from memory. The observed state comes from this audit's own intake table.

What the mapping can and cannot show. It shows whether a declaration was made and what
the artifact behind it held on the access date. It does not establish that a journal
enforced or failed to enforce its policy, which would need the submission record, and it
is a purposively selected subset of 7, not a sample.

Output: analiz/policy-statement-delivery.json -> archive results/

Usage: python analiz/scripts/30_policy_statement_delivery.py
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

from paths import out, result

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

UA = "dysphagia-repro-audit (mailto:tuncersefa@gmail.com)"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"

# Policy strength is recorded from the publisher's own author guidance, with the page
# used and the date it was read, so a reader can check the classification rather than
# take it. "mandatory" means the journal requires a statement AND requires sharing or a
# stated reason; "statement required" means a statement is required but sharing is not;
# "encouraged" means neither is required.
STUDIES = [
    {"study": "A", "citekey": "cubero2025", "journal": "Computers in Biology and Medicine",
     "doi": "10.1016/j.compbiomed.2025.109759",
     "policy": "statement required",
     "policy_source": "https://www.elsevier.com/researcher/author/policies-and-guidelines/research-data",
     "repo": "BSEL-UC3M/VFSS_analysis"},
    {"study": "B", "citekey": "saab2023", "journal": "Frontiers in Neuroscience",
     "doi": "10.3389/fnins.2023.1302132",
     "policy": "mandatory",
     "policy_source": "https://www.frontiersin.org/guidelines/policies-and-publication-ethics",
     "repo": "UofTNeurology/masa-open-source"},
    {"study": "N", "citekey": "geiger2025", "journal": "Communications Medicine",
     "doi": "10.1038/s43856-025-01255-1",
     "policy": "mandatory",
     "policy_source": "https://www.nature.com/commsmed/editorial-policies/reporting-standards",
     "repo": "ResearchgroupMITI/swallow-detection"},
    {"study": "O", "citekey": "dai2026", "journal": "iScience",
     "doi": "10.1016/j.isci.2025.114451",
     "policy": "mandatory",
     "policy_source": "https://www.cell.com/iscience/authors",
     "repo": "enoch0307/streamlitapp_cn"},
    {"study": "P", "citekey": "song2025", "journal": "npj Digital Medicine",
     "doi": "10.1038/s41746-024-01417-w",
     "policy": "mandatory",
     "policy_source": "https://www.nature.com/npjdigitalmed/editorial-policies",
     "repo": "yonghunsong/Throat-related-events-classification"},
    {"study": "Q", "citekey": "park2022", "journal": "Scientific Reports",
     "doi": "10.1038/s41598-022-20348-8",
     "policy": "mandatory",
     "policy_source": "https://www.nature.com/srep/journal-policies/editorial-policies",
     "repo": "ruaeh/Dysphagia-ML"},
    {"study": "R", "citekey": "devette2025", "journal": "Radiotherapy and Oncology",
     "doi": "10.1016/j.radonc.2025.111169",
     "policy": "statement required",
     "policy_source": "https://www.elsevier.com/researcher/author/policies-and-guidelines/research-data",
     "repo": "PRI2MA/DL_NTCP_Dysphagia"},
]

SECTION_HINTS = ("data availability", "code availability", "availability of data",
                 "data and code availability", "resource availability",
                 "availability statement", "data sharing")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "ignore")


def find_record(doi):
    q = urllib.parse.quote('DOI:"%s"' % doi)
    d = json.loads(fetch("%s/search?query=%s&resultType=core&format=json" % (EPMC, q)))
    res = d.get("resultList", {}).get("result", [])
    return res[0] if res else None


def availability_from_fulltext(pmcid):
    """Pull the availability section out of the JATS full text, verbatim."""
    xml = fetch("%s/%s/fullTextXML" % (EPMC, pmcid))
    # Sections are <sec> blocks with a <title>; take the one whose title matches.
    for m in re.finditer(r"<sec[^>]*>(.*?)</sec>", xml, re.S):
        block = m.group(1)
        t = re.search(r"<title[^>]*>(.*?)</title>", block, re.S)
        if not t:
            continue
        title = re.sub(r"<[^>]+>", " ", t.group(1))
        title = re.sub(r"\s+", " ", title).strip().lower()
        if any(h in title for h in SECTION_HINTS):
            text = re.sub(r"<[^>]+>", " ", block)
            text = re.sub(r"\s+", " ", text).strip()
            return text
    # Nature-family journals often use <notes notes-type="data-availability">.
    for m in re.finditer(r'<notes[^>]*notes-type="[^"]*availability[^"]*"[^>]*>(.*?)</notes>',
                         xml, re.S):
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        return re.sub(r"\s+", " ", text).strip()
    return None


def check_pointer(target):
    """Resolve one pointer named in an availability statement and say what is there.

    A statement that names a location makes a checkable claim, and checking it is the
    whole point of the mapping. Anything not resolvable to a Zenodo record or a GitHub
    repository is reported as unchecked rather than guessed at.
    """
    m = re.search(r"zenodo\.(\d+)", target)
    if m:
        try:
            d = json.loads(fetch("https://zenodo.org/api/records/%s" % m.group(1)))
            files = d.get("files", [])
            return {"kind": "zenodo", "resolves": True,
                    "n_files": len(files),
                    "total_bytes": sum(f.get("size") or 0 for f in files),
                    "title": (d.get("metadata") or {}).get("title")}
        except Exception:
            return {"kind": "zenodo", "resolves": False}
    m = re.search(r"github\.com/([^/\s,;)\]]+/[^/\s,;)\]]+)", target)
    if m:
        repo = m.group(1).rstrip(".").rstrip("/")
        try:
            d = json.loads(fetch("https://api.github.com/repos/%s" % repo))
            return {"kind": "github", "resolves": True, "repo": d.get("full_name"),
                    "size_kb": d.get("size"),
                    "empty": (d.get("size") == 0),
                    "created_at": d.get("created_at"),
                    "pushed_at": d.get("pushed_at")}
        except Exception:
            return {"kind": "github", "resolves": False, "repo": repo}
    return None


def main():
    intake = {}
    import csv
    from paths import inp
    for r in csv.DictReader(inp("repo-intake-table").open(encoding="utf-8-sig")):
        intake[r["repo"].strip()] = r

    rows = []
    for s in STUDIES:
        rec = dict(s)
        rec["availability_statement"] = None
        rec["statement_source"] = None
        try:
            hit = find_record(s["doi"])
            if hit:
                rec["title"] = hit.get("title")
                pmcid = hit.get("pmcid")
                rec["pmcid"] = pmcid
                rec["is_open_access"] = hit.get("isOpenAccess")
                if pmcid and hit.get("hasTextMinedTerms") is not None:
                    try:
                        st = availability_from_fulltext(pmcid)
                        if st:
                            rec["availability_statement"] = st[:1200]
                            rec["statement_source"] = "Europe PMC full text (%s)" % pmcid
                    except Exception as e:
                        rec["statement_source"] = "full text not retrievable: %s" % type(e).__name__
                if not rec["availability_statement"] and not rec["statement_source"]:
                    rec["statement_source"] = "no open full text in Europe PMC"
        except Exception as e:
            rec["statement_source"] = "lookup failed: %s" % type(e).__name__

        # A statement that names a location makes a claim that can be checked now.
        rec["pointers_checked"] = []
        if rec["availability_statement"]:
            targets = set(re.findall(r"https?://[^\s,;)\]]+", rec["availability_statement"]))
            targets |= set(re.findall(r"10\.5281/zenodo\.\d+", rec["availability_statement"]))
            for t in sorted(targets):
                chk = check_pointer(t)
                if chk:
                    chk["named_in_statement"] = t
                    rec["pointers_checked"].append(chk)
                    time.sleep(0.4)

        it = intake.get(s["repo"], {})
        rec["observed"] = {
            "license": it.get("license"),
            "env_file": it.get("env_file"),
            "weights_in_repo": it.get("weights"),
            "n_files": it.get("n_files"),
            "code_files": it.get("code_files"),
            "readme": it.get("readme"),
        }
        rows.append(rec)
        got = "yes" if rec["availability_statement"] else "no"
        print("  %-3s %-34s policy=%-19s statement=%s"
              % (s["study"], s["journal"][:34], s["policy"], got))
        time.sleep(0.5)

    payload = {
        "generated_by": "30_policy_statement_delivery.py",
        "scope": ("The 7 studies of the 18 whose publication could be identified. The "
                  "other 11 answer to no journal policy, so the question is undefined "
                  "for them and they are not included here."),
        "limits": ("Policy strength is our reading of the publisher's author guidance at "
                   "the recorded URL. The mapping shows what was declared and what the "
                   "artifact held; it does not show whether a journal enforced its "
                   "policy, and 7 purposively selected studies are not a sample."),
        "n": len(rows),
        "n_with_statement_retrieved": sum(1 for r in rows if r["availability_statement"]),
        "studies": rows,
    }
    p = out("policy-statement-delivery.json")
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                 encoding="utf-8")
    print("\n  statements retrieved: %d of %d" % (payload["n_with_statement_retrieved"],
                                                  len(rows)))
    print("  written: %s" % p)


if __name__ == "__main__":
    main()
