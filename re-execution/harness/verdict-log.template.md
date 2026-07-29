# Layer B re-run verdict — repository <REPO-ID> (<repo-url>)
# Date: <YYYY-MM-DD> | Environment: best-effort CPU container (deviations documented)

## Metadata
- Study: <author, year, journal> | Modality: <..> | Model: <..>
- License: <osi/none/..> | Weights: <DOI or absent> | Example data: <present or absent>

## 1. As-declared (faithful) attempt — re-executability
- Result: **[BUILD_OK / BUILD_FAIL / RUN_FAIL]**
- Full error, if any: `logs/<REPO-ID>/as-declared.log`
- Runs out of the box: **[YES / NO]**

## 2. Best-effort repairs (friction taxonomy)
| # | Barrier category | Intervention |
|---|---|---|
| FIX-1 | <dep_conflict/..> | <..> |
| FIX-2 | <undeclared_dependency/..> | <..> |
> Total number of repairs: **N** (quantified friction)

## 3. Inference (CPU)
- Did it run: [YES/NO] | Runtime: <..> | Note: <GPU-only operation? missing post-processing?>

## 4. Comparison
- Re-executable (produced its own output): **[YES/NO]**
- Metric reproduction (only where reference or example data exist): **[full / partial / not applicable, confidential data]** — detail: <..>

## 5. VERDICT
**[re_executable / partial / not_reproduced / not_attemptable]**
- Barrier categories: <list>
- One sentence: <..>

## 6. Provenance (DO NOT DELETE)
Logs and files: `logs/<REPO-ID>/` · Docker image tag: <..> · commit or tag: <..>
