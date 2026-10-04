# CLA consolidation package: Japan-first commerce research

This is a derivative package. The originals in `../japan-agentic-commerce-CLA/` are unchanged. **Read `00_consolidation_memo.md` first.**

| Path | Contents |
|---|---|
| `00_consolidation_memo.md` | The decision, retained constraints, rejected inferences, unresolved dependencies, and the single next allocation |
| `01_original_CLA_export/` | Hash manifest and `git archive` of the original CLA packet at commit `ebd8cdf`, plus an export note (recovered, not reconstructed) |
| `02_claim_adjudication_ledger.csv` | 38 adjudications linking CLA, GRO, GEM and reviewer IDs to sources, evidence families, pass type and decision use |
| `03_derivatives/` | Only the affected corrected tables (listed below) |
| `04_qa/` | QA scripts, outputs and `QA_RECEIPT.md` |
| `05_discovery_kit/` | Japanese interview guide, English coding legend, recording sheets, consent and data boundary, follow-on rules, effort cap |
| `06_verification_queue.csv` | Exact pages and artifacts still to verify, and what each one blocks |
| `00_inputs_supplied/` | The Grok v2 CSVs and prompt as supplied (namespaced `GRO_`), with hashes |

Contents of `03_derivatives/`:
- `CLA-D01`: hypotheses
- `CLA-D02`: jobs and concepts
- `CLA-D03`: permission gates
- `CLA-D04`: Amazon lifecycle data scope
- `CLA-D05`: trace state corrections
- `CLA-D06`: new sources
- `GRO-D01`: repaired Grok v2 model rows
- `bridge/`: economics bridge with outputs and the C04 stress grid

**Not supplied to CLA:** Grok v1 files, `calculate_r003_v2.py`, the R003 v2 addendum, Grok `06`/`07` v2, the reviewer's audit JSON, and the Gemini correction table. Nothing in this package substitutes for them.

**Rebuild:**

```bash
cd research/japan-agentic-commerce-CLA-consolidation
python3 03_derivatives/bridge/bridge_model.py
python3 03_derivatives/build_ledger.py
python3 04_qa/qa_original_cla.py
python3 04_qa/qa_grok_v2.py
python3 04_qa/test_bridge.py
```

`qa_original_cla.py` needs pycel for its workbook check; the other checks run without it.

**Repository state:** the assignment did not authorise commits or pushes, so this directory is **uncommitted**. Because the cloud container is ephemeral, it will be lost when the session ends unless it is committed or downloaded.
