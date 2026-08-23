# -*- coding: utf-8 -*-
"""Record the published checksum of the external weight deposit used in the first case.

Why this exists. The re-execution of the VFSS case downloaded a 6.1 GB weight archive
from Zenodo and used it for inference, and the article stated that we did not checksum
it. Zenodo publishes an MD5 for every deposited file, so the identifier that fixes which
file that was is recoverable from the record even though our copy was deleted.

What this does and does not establish. It records the checksum the depositor published,
so a third party can confirm that the file they download is the file the record holds.
It does NOT establish that the copy we downloaded matched: we did not hash it at the
time, and no later fetch can prove what we held then. The distinction matters, and the
output says so in the file rather than leaving a reader to assume the stronger claim.

Output: analiz/external-deposit-provenance.json -> archive results/

Usage: python analiz/scripts/26_external_deposit_provenance.py
"""
import json
import sys
import urllib.request

from paths import out

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# The weight and sample deposit accompanying the VFSS case, cited in the article as the
# one external archive we downloaded.
RECORD = "17191973"
UA = "dysphagia-repro-audit (mailto:tuncersefa@gmail.com)"


def main():
    url = "https://zenodo.org/api/records/%s" % RECORD
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))

    meta = d.get("metadata", {})
    lic = meta.get("license")
    lic = lic.get("id") if isinstance(lic, dict) else lic

    files = [{"filename": f.get("key"),
              "size_bytes": f.get("size"),
              "checksum_published_by_depositor": f.get("checksum")}
             for f in d.get("files", [])]

    payload = {
        "generated_by": "26_external_deposit_provenance.py",
        "record": RECORD,
        "doi": d.get("doi"),
        "title": meta.get("title"),
        "license": lic,
        "publication_date": meta.get("publication_date"),
        "files": files,
        "what_this_establishes": (
            "The checksum the depositor published for each file in this record. A third "
            "party can use it to confirm that the file they download is the file the "
            "record holds."),
        "what_this_does_not_establish": (
            "That the copy we downloaded matched this checksum. We did not hash the file "
            "at the time of the run and the copy was deleted afterwards, so no later "
            "fetch can prove what we held. The run is repeatable from the record; "
            "bit-identity with our copy is not demonstrable."),
    }
    p = out("external-deposit-provenance.json")
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for f in files:
        print("  %-28s %6.2f GB  %s" % (f["filename"], (f["size_bytes"] or 0) / 1e9,
                                        f["checksum_published_by_depositor"]))
    print("  license: %s  doi: %s" % (lic, d.get("doi")))
    print("  written: %s" % p)


if __name__ == "__main__":
    main()
