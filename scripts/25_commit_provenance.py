# -*- coding: utf-8 -*-
"""Recover the commit each audited repository pointed at on its access date.

Why this exists. The audit reported repository state at a logged date but recorded no
commit identifier, so a third party could reach *a* state of each repository and not
provably the state we observed. The article's own recommendation set asks others to
record exactly that, and marked the item "Not met here". The identifier is recoverable
after the fact: GitHub returns the commit history filtered by date, so the first commit
at or before the access timestamp is the tip the tree was read from.

What it does NOT establish. A recovered tip is the commit that was current on that date;
it is not proof that our reading of that tree was correct, and it cannot recover state
for a repository that has since been deleted or made private. Both outcomes are recorded
rather than smoothed over: a repository that cannot be resolved is written out as such.

Rate limits. Unauthenticated GitHub allows 60 requests an hour, which covers the 23 rows
at one date each. Set GITHUB_TOKEN to raise the ceiling; the script works without it.

Output: analiz/commit-provenance.json  ->  archive results/commit-provenance.json

Usage: python analiz/scripts/25_commit_provenance.py
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

from paths import inp, out

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://api.github.com/repos/%s/commits?until=%s&per_page=1"
UA = "dysphagia-repro-audit (mailto:tuncersefa@gmail.com)"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/vnd.github+json"})
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8")), r.headers


def main():
    rows = list(csv.DictReader(inp("repo-intake-table").open(encoding="utf-8-sig")))
    print("  repositories in intake table: %d" % len(rows))

    results = []
    resolved = 0
    for i, r in enumerate(rows, 1):
        repo = r["repo"].strip()
        date = r.get("check_date", "").strip()
        if not repo or not date:
            continue
        until = "%sT23:59:59Z" % date
        rec = {"repo": repo, "access_date": date, "commit": None,
               "commit_date": None, "status": None}
        try:
            data, _ = get_json(API % (repo, until))
            if isinstance(data, list) and data:
                rec["commit"] = data[0]["sha"]
                rec["commit_date"] = data[0]["commit"]["committer"]["date"]
                rec["status"] = "resolved"
                resolved += 1
            else:
                # The repository exists but reports no commit at or before that date.
                rec["status"] = "no-commit-at-or-before-access-date"
        except urllib.error.HTTPError as e:
            if e.code == 409:
                # GitHub answers the commits endpoint with 409 "Git Repository is empty"
                # when a repository has no commit at all. That is not a failure of this
                # recovery: it corroborates the empty-repository finding from a different
                # endpoint. For such a repository the provenance is the repository record
                # itself, so we take the creation and last-push timestamps instead. Where
                # those two are the same instant, the repository has been empty since it
                # was created and its state on the access date is not in question.
                rec["status"] = "empty-repository (HTTP 409: no commit exists)"
                try:
                    meta, _ = get_json("https://api.github.com/repos/%s" % repo)
                    rec["created_at"] = meta.get("created_at")
                    rec["pushed_at"] = meta.get("pushed_at")
                    rec["size_kb"] = meta.get("size")
                    # Report the interval rather than a boolean: how close the two
                    # timestamps have to be before "untouched since creation" is a fair
                    # description is a judgment, and the reader should make it from the
                    # number. GitHub stamps pushed_at at creation, so a gap of a second
                    # or two means nothing was ever pushed.
                    if rec["created_at"] and rec["pushed_at"]:
                        import datetime as _dt
                        fmt = "%Y-%m-%dT%H:%M:%SZ"
                        rec["seconds_between_creation_and_last_push"] = int(
                            (_dt.datetime.strptime(rec["pushed_at"], fmt)
                             - _dt.datetime.strptime(rec["created_at"], fmt)).total_seconds())
                except Exception:
                    pass
            else:
                # 404 covers deleted, renamed and now-private repositories alike; the API
                # does not distinguish them for an unauthenticated caller, so neither do we.
                rec["status"] = "http-%d" % e.code
        except Exception as e:
            rec["status"] = "error: %s" % type(e).__name__
        results.append(rec)
        print("  [%2d/%d] %-52s %s  %s" % (i, len(rows), repo[:52],
                                           (rec["commit"] or "-")[:12], rec["status"]))
        time.sleep(0.6)

    empty = sum(1 for r in results if r["status"].startswith("empty-repository"))
    payload = {
        "generated_by": "25_commit_provenance.py",
        "n_empty_repositories": empty,
        "what_this_is": ("The tip commit each audited repository pointed at on its "
                         "logged access date, recovered after the fact from the GitHub "
                         "commits API. It fixes which tree the reported signals were "
                         "read from. It does not verify that our reading of that tree "
                         "was correct."),
        "n_rows": len(results),
        "n_resolved": resolved,
        "n_unresolved": len(results) - resolved,
        "repositories": results,
    }
    p = out("commit-provenance.json")
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("\n  resolved   : %d of %d" % (resolved, len(results)))
    print("  unresolved : %d" % (len(results) - resolved))
    print("  written    : %s" % p)


if __name__ == "__main__":
    main()
