# QA receipt: CLA consolidation

**Run window:** 2026-10-04 21:47–22:10 UTC (2026-10-05 06:47–07:10 JST).
**Environment:** Python 3.11; pycel installed for workbook evaluation. LibreOffice is present but cannot load files in this container. Web page fetches are blocked (HTTP 403); WebSearch only.

| # | Check | Script / artifact | Result | What it does **not** show |
|---|---|---|---|---|
| 1 | Original CLA packet intact versus commit `ebd8cdf` | `01_original_CLA_export/MANIFEST_CLA_original.csv`; `git diff --quiet HEAD` | 16 of 16 files match their committed blobs; the working tree was clean at start and end | That the original conclusions are right |
| 2 | Workbook formulas versus Python (re-run, read-only) | `qa_original_cla.py` → `QA_original_CLA_rerun.txt` [1] | 141 cells, 0 mismatches | Economic validity; this is implementation consistency only |
| 3 | Original CSV export precision | same [2] | 81 of 288 numeric cells were saved rounded (largest relative loss 9.0e-4) | — |
| 4 | Original CSV dependency round trip (recompute from saved values) | same [3] → `QA_original_CLA_roundtrip_discrepancies.csv` | **31 of 138 outputs do not reconcile** within their own displayed precision; 0 sign flips | Same defect class as Grok v2; in-memory headlines are unaffected |
| 5 | Grok v2 precision defect | `qa_grok_v2.py` → `QA_grok_v2.txt` [F1] | **Reproduced.** Exact 0.012; saved 0.01; 0.01 × 80 = 0.80 ≠ 0.96. Upside rows reconcile exactly. | The reviewer's 29-check script was **not supplied**, so it was not re-run. Inputs 4, 0.25, 0.05, 0.60, 0.40 and ¥80 are as the reviewer stated them, cross-checked only against the supplied v2 rows. |
| 6 | Grok v2 cohort definition | same [F2] | **Reproduced** from the row text (acquired-cohort retention × activation); repaired in `GRO-D01` | No numeric payback was wrong yet; the inputs are blank |
| 7 | Grok v2 H02 scope | same [F3] | Mismatch confirmed; split in `CLA-D01` | — |
| 8 | Bridge round trip with unit-aware tolerances | `test_bridge.py` → `QA_bridge_tests.txt` | **17/17 pass.** Re-imported exported inputs reproduce all 129 outputs. | Whether any configuration is permitted, wanted or profitable |
| 9 | Unknown versus zero handling | same | Observed-scenario contributions are blank with status `unknown`. Gated C03 revenue is `rule_zero_underwriting_exclusion`. Passive affiliate revenue is a programme-rule 0. C02 is `gated_not_computed`. | — |
| 10 | Activation counted once | same | a × r_t × c_t = q_t × c_t; passing a together with q raises an error | Retention inputs are unobserved |
| 11 | C04 stress | same + `03_derivatives/bridge/c04_stress_grid.csv` | ¥300 reproduced; at ¥40/MAU after an illustrative ¥31.6 core, submission × human share × minutes ≤ 0.42 | Real incidence or minutes |
| 12 | Ledger and register integrity | `03_derivatives/build_ledger.py` | Every row has the right width; every verification-queue ID referenced exists | Source verification; see `06_verification_queue.csv` |

## Defects found and fixed in this pass (no historical log rewritten)

- **First bridge test run: 16/17.** The display-isolation test was mis-specified: it rounded inputs that were already whole numbers. It was rewritten to test the actual mechanism (a downstream value recomputed from a displayed intermediate) and now passes. The model itself did not change.
- **Bytecode cache.** The first read-only QA import wrote a Python bytecode cache folder (`research/japan-agentic-commerce-CLA/model/__pycache__/`) next to the originals. It is gitignored and was never part of the packet. It was deleted, and the QA scripts now set `sys.dont_write_bytecode`. Original file hashes were unaffected.
- **Interrupted step.** An earlier attempt to re-run the original model by extracting the tar archive and calling `main()` in a scratch copy was interrupted by the user before it ran. Validation was redone in memory instead; nothing was written to the originals.

## Not verified (see `../06_verification_queue.csv`)

- Every external page. Claims rest on search extracts, or on Grok's and the reviewer's own retrievals.
- The Grok and Gemini artifacts that were not supplied.
- The reviewer's audit JSON.
