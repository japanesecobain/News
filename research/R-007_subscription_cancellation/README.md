# R-007 Japan Subscription Cancellation Agent: research packet

**Disposition: PARK.** The single next test is E5 (counsel memo). **Read `00_DECISION_MEMO.md` first.**

| File | Contents |
|---|---|
| `00_RESEARCH_CHARTER.md` | Decision; MECE issue tree A–L with WNTB and falsifiers; stop-condition map; recovery record |
| `00_DECISION_MEMO.md` | 1,126-word decision memo |
| `01_RESEARCH_REPORT.md` | Full report: executive summary; stop-condition table; §A–§N by workstream; the six mandatory closing sections |
| `02_EVIDENCE_LEDGER.csv` | 105 atomic claims with the §25 fields (origin and status kept separate; source families) |
| `03_COMPETITOR_MATRIX.csv` | 19 rows, each judged by how it causes us to lose, with the cheapest credible response |
| `04_CANCELLATION_ROUTE_MATRIX.csv` | 22 provider routes; classes A–E; company-agent status; architecture |
| `05_PERMISSION_AND_LEGAL_MATRIX.csv` | 22 rows separating law, provider contract, technical restriction and unknown; counsel questions (not legal advice) |
| `06_ECONOMICS_MODEL.csv` | C01–C08 at full precision plus a display column; observed (all unknown) and two labelled illustrations |
| `07_CONCEPT_REGISTER.csv` / `08_HYPOTHESIS_REGISTER.csv` | C01–C09 and H01–H14 |
| `09_EXPERIMENT_BACKLOG.csv` | Ranked experiments and primary research (designed, not executed) |
| `10_SOURCE_REGISTER.csv` | 109 sources, 91 families, access status |
| `11_MOAT_AND_RIGHT_TO_WIN.md` | M1–M6 chain tests; why now / why not now; founder fit |
| `12_QA_RECEIPT.md` | Checks performed, defects fixed, deviations and gaps |
| `12_QA_run_log.txt`, `12_QA_economics_tests.txt` | Raw outputs of the final run |
| `REGISTER_UPDATES_PENDING.csv` | Append-only supersessions to apply to the founder's local ledgers |
| `model/` | Data modules (`evidence.py`, `competitors.py`, `routes.py`, `legal.py`, `experiments.py`, `registers.py`), builders and tests |

**Rebuild and check:**

```bash
cd research/R-007_subscription_cancellation
python3 model/check_charter.py
python3 model/build_registers.py      # writes 02, 03, 04, 05, 07, 08, 09, 10
python3 model/state_model.py
python3 model/economics_model.py      # writes 06
python3 model/test_economics.py       # writes 12_QA_economics_tests.txt
python3 model/qa_crossrefs.py
```

**Evidence caveat:** every source was reached through search extracts. No page could be opened (egress 403), so no claim is "directly observed".
