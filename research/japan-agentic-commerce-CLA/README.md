# Japan-first Agentic Commerce: CLA research packet

Researcher prefix: **CLA** (Claude). Specialist lens: execution feasibility and economic underwriting. Reference date: 2026-10-04.

**Start with `00_decision_memo.md`.** Before relying on any number, read the limits in `01_research_report.md` §0. No source page could be opened in this run (egress policy), so every fact comes from search-result summaries.

| File | Contents |
|---|---|
| `00_decision_memo.md` | Recommendation, evidence for and against, decisive unknowns, next decision rule |
| `01_research_report.md` | Full analysis: claim audit, permissions matrix, operating traces, economics, competition, consumer, defensibility, tests, closing sections |
| `02_evidence_ledger.csv` | One row per claim–source relationship (CLA-C###) |
| `03_competitor_matrix.csv` | Product × geography × capability (long format) |
| `04_economics_model.csv` | Inputs, outputs, frontiers, sizing, payback, sensitivities, bridge case, for three scenarios |
| `05_hypothesis_register.csv` | H01–H12 plus sub-hypotheses |
| `06_experiment_backlog.csv` | CLA-E001…E010, ordered by decision value per cost |
| `07_concept_register.csv` | C01–C08, variants, and the adjacent themes (NOT RESEARCHED) |
| `08_source_register.csv` | Source provenance and access status (CLA-S###) |
| `model/economics_model.py` | Reproducible model; writes `04` and `economics_model.xlsx` |
| `model/economics_model.xlsx` | The same model as live Excel formulas, recalculated on open; 141/141 cells reconciled with Python via pycel |
| `model/*.py` | Register data and builder (`build_registers.py` validates every cross-reference) |

Rebuild:

```bash
cd model && python3 economics_model.py && python3 build_registers.py
```

`economics_model.py` needs `openpyxl` for the workbook. The pycel reconciliation check is optional.
