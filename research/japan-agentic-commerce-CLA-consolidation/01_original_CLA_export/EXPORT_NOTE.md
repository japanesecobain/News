# Original CLA packet: export note

**Status: recovered, not reconstructed.**

- **Location:** the original files are unchanged at `research/japan-agentic-commerce-CLA/` in this repository.
- **Commit:** they were committed to branch `claude/affectionate-rubin-u8nx1x` as commit `ebd8cdf7184ad8b5915d6f0daf5eb3f564bef70e` on 2026-10-04 and pushed during the first assignment, before this consolidation's "no commits/pushes" instruction.
- **Working tree:** clean against that commit at the start of this pass (`git status` showed no modifications).

## Contents

| Item | Status |
|---|---|
| `00_decision_memo.md`, `01_research_report.md` | Present (original) |
| CSVs `02`–`08` | Present (original) |
| `model/economics_model.py`, `model/economics_model.xlsx` | Present (original) |
| `model/build_registers.py`, `claims.py`, `registers.py`, `sources.py` | Present (original builder and dependency files) |
| `README.md` | Present (original) |
| Retained validation results from 2026-10-04 | **Not available as files.** The original 141/141 workbook-vs-Python check and the register cross-reference check printed to the console only; no log file was kept. A **new** read-only re-run is in `../04_qa/QA_original_CLA_rerun.txt`. It is not a historical receipt. |

## Files in this folder

- `MANIFEST_CLA_original.csv`: relative path, bytes, SHA-256, git blob ID at `ebd8cdf`, and a worktree-versus-commit check (16 of 16 match).
- `CLA_original_packet_ebd8cdf.tar.gz`: `git archive` of that directory taken from the commit itself, not the working tree. SHA-256 `cba76917bfb10a8202ffb5115a808673b8ee46407f88ec5081225a8018ada323`.

## Caveats found in this pass

The originals stay as they were committed. Corrections live only in `../03_derivatives/`.
- The original `04_economics_model.csv` saved display-rounded values (`../04_qa/QA_original_CLA_roundtrip_discrepancies.csv`).
- Several original conclusions are superseded in `../02_claim_adjudication_ledger.csv`.
