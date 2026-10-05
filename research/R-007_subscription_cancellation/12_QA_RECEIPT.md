# R-007 QA receipt

This records the checks actually performed, with their results. It is not a checklist written in advance. The raw output of the final clean run is in `12_QA_run_log.txt`.

**Run date:** 2026-10-05 (UTC).

**Environment:**
- Python 3.11, cloud container.
- WebFetch and curl were blocked by the egress proxy (HTTP 403) for every research host tried. WebSearch extracts were the only access to sources.
- No page was opened.

## 1. Final clean run (all scripts, in order)

| # | Script | What it checks | Result | What it does **not** show |
|---|---|---|---|---|
| 1 | `model/check_charter.py` | Every A–L branch has WNTB rows with falsifier, source/test and consequence; every §29 stop condition is mapped; H01–H14 are present | **PASS** | That the beliefs are right |
| 2 | `model/build_registers.py` | Ledger and source register (§25 fields, status and origin vocabularies, ≥2 families for "corroborated", no "directly observed", every source used); competitor, route, legal, experiment, concept and hypothesis registers (fields, vocabularies, every evidence ID resolves, route-class consistency rules, legal-conclusion lint); CSV round trip | **PASS**: 105 claims, 109 sources, 91 families; 19 competitors; 22 routes (A 0, B 14, C 0, D 0, E 8); 22 legal rows; 8 experiments; C01–C09; H01–H14; 0 round-trip mismatches | Truth of any claim; completeness of the search |
| 3 | `model/state_model.py` | 13 structural invariants (stopped needs accepted, effective and a verification cycle; pause ≠ success; contractual charges ≠ persisted; and others) | **13/13**. A mutation test (two injected shortcuts) was detected in a separate run | That any route is executable or permitted |
| 4 | `model/economics_model.py` | Writes `06_ECONOMICS_MODEL.csv` (372 rows, exact and display columns) | Written | — |
| 5 | `model/test_economics.py` | Round trip (225 outputs); display isolation; unknown ≠ zero; rule zero; activation counted once with the guard; a single labour price; break-even algebra; infeasibility flag; paradox monotonicity and flag; gating and conflict flags; input labelling | **23/23** (`12_QA_economics_tests.txt`) | That any configuration is permitted, wanted or profitable |
| 6 | `model/qa_crossrefs.py` | Every `[E-xxx]`, CMxx, RMxx, Lxx and experiment ID cited in the memo, report and moat file exists; 12 memo figures match the model or ledger; the six closing sections are in order; at least five "wrong about" points; memo length and lead | **31/31** | That the prose is persuasive or complete |

No `__pycache__` was written: every script sets `sys.dont_write_bytecode`, and a search after the run found none.

## 2. Stage checks (moved here from the report)

Each stage was closed with a written check before the next stage began.

### S1 (charter)

`check_charter.py` passed at the time (re-run above). The semantic notes are in the charter, §7.

### S2 (customer need, taxonomy)

**Mechanical:** 30 claims and 36 sources in 23 families. The §25 fields and vocabularies hold, the "corroborated" rule holds, and the round trip had 0 mismatches.

**Semantic:**
- **Every number in §A–B has a comparator.** The Sensor Tower USD figures are used only to show that a rail split *cannot* be derived.
- **The lead figures 71.6% and 17.9% are not used anywhere.**
- **J4/J5 delegation, WTP and minutes are UNKNOWN throughout.**

**Corrections:**
1. Taxonomy cells holding general knowledge ("usually none", "monthly cut-off common", "strong identity checks") were replaced with UNKNOWN and the stage that resolves them.
2. An unverifiable Statistics Bureau URL I had written into R7-S035 was replaced with the topics index, and the exact page was marked UNRESOLVED.
3. The GEM extract's unit error ("6,017 billion yen") was corrected to ¥601.7bn.

### S3 (competition, detection)

**Mechanical:** 63 claims, 67 sources, 50 families; 19 competitor rows, all fields filled; every evidence ID resolves.

**Semantic:**
- **Rows are judged by loss mechanism.**
- **The work-order traps are applied:** downloads ≠ users (Zaim); store availability ≠ adoption (Subcut, Unsub.ai); detected charge ≠ contract ≠ authority (Moneytree).

**Corrections:**
1. An unsourced Japan population denominator (about 123.5M) was removed from E-G01.
2. CM05's loss mechanism was rewritten from a cross-reference into its own mechanism.

### S4 (routes, state model)

**Mechanical:**
- 87 claims, 90 sources, 73 families; 22 routes; class-consistency rules hold.
- State model 13/13; mutation test caught.

**Semantic:**
- **The counts are labelled as a purposive sample.**
- **docomo's family-only rule is flagged as decision-critical but unverified.**
- **Adobe was set to class E, not B.** No extract established its cancellation channel, and I did not fill it from general knowledge.
- **Sampling bias toward large, easy providers is disclosed.**

### S5 (legal)

**Mechanical:**
- 100 claims, 104 sources, 86 families; 22 legal rows.
- Every unresolved row has a counsel question.
- The legal-conclusion lint caught L17's first wording ("…is lawful and routine…"), which was rewritten.

**Semantic:**
- **No row states that an activity is lawful or unlawful.**
- **Analogies are labelled.**
- **The モームリ matter is described as charges, not a conviction.**

### S6 (economics)

**Mechanical:** model and tests as in §1.

**Defect:** the first test run was 22/23. The display-isolation test probed a value exactly representable at 2 dp (1,749 × 1.6 / 60 = 46.64), so it could not fail. It was rewritten to test the mechanism across all outputs, and the model was unchanged. **This repeats a test-design error from the consolidation bridge (2026-10-04).** The lesson: test the mechanism, not a hand-picked value.

**Semantic:**
- **Observed scenario all UNKNOWN.**
- **Every number names its scenario.**
- **The 14/22 sample share is not used as a market share.**
- **Partner sales cost was added** after the first C07 run, so B2B2C is not flattered.

### S7 (moat, why now, founder fit)

**Mechanical:** six moat rows, each with all seven chain fields.

**Semantic:**
- **No banned "moats".**
- **Why-now forces are scored in both directions.**
- **Founder facts come only from the supplied profile.**

### S8 (experiments)

**Mechanical:** 8 rows, ranks 1–8; E1–E5 present; all "designed; not executed".

**Semantic:**
- **Prompts ask only about prior behaviour.**
- **No founder data, credentials or files are used.**
- **Thresholds are labelled as decision rules.**

### S9–S11 (report, memo, QA)

**Mechanical:** `qa_crossrefs.py` 31/31; memo 1,126 words.

**Semantic checks on the final synthesis:**
- **The memo leads with one disposition (PARK)** and states customer, job, boundary, operating model, payer, strongest reasons for and against, moat hypothesis and single next test.
- **The report ends with the six mandatory sections**, with seven "most likely wrong" points.
- **The stop-condition table resolves none in the concept's favour.** The disposition follows the rule "UNRESOLVED, not favourable inference".
- **No legal advice:** the legal content is framed as questions for counsel.
- **Model product names (used only as API price anchors) were replaced with tier labels** before closing, so no model identifier appears in the packet.

## 3. Deviations from the work order (disclosed, not hidden)

1. **Local project files were not available.** The `/Users/japanesecobain/...` operating files, registers and Complete Work documents were not in this container. The standard *as written in the work order* was applied. Register supersessions are staged in `REGISTER_UPDATES_PENDING.csv`, which is append-only: the original OPEN row for R-007 is kept and the PARK row supersedes it.
2. **No primary source was opened.** Work order §6 asks that primary sources be opened before any statement is promoted. That was impossible (egress 403), so nothing is promoted to "directly observed".
3. **Status vocabulary extension: `reported_unopened`.** It means the named non-company source reports the claim per a search extract and the page was not opened. It is strictly weaker than "directly observed". Company self-statements keep "company-reported".
4. **Origin vocabulary extension: `community/forum`,** for Apple Community, RevenueCat and Adobe forums, and review sites.
5. **Extra columns:**
   - Ledger: `verification`, `source_families`, `wntb`, `stage`.
   - Route matrix: `route_id`, `route_class`, `concierge_status`, `route_class_rationale`, `architecture`.
   - All required columns are present, in the required order, first.
6. **ID collision:** the charter's WNTB beliefs E1–E3 (legal) share labels with experiments E1–E5. In `09_EXPERIMENT_BACKLOG.csv`, the `wntb_and_hypotheses` column refers to *beliefs*; everywhere else E1–E6 are experiments.
7. **Section order:** report sections are lettered by workstream (A–N), not by stage. Stage checks moved from the report to this receipt so the report ends with the mandatory sections.
8. **Additional files:** `12_QA_economics_tests.txt`, `12_QA_run_log.txt`, `REGISTER_UPDATES_PENDING.csv`, `README.md` and the `model/` scripts.

## 4. Not verified, and what each gap blocks

| Not verified | Blocks |
|---|---|
| CAA 2026 white paper: base, n, dates, wording, full option list; the 71.6% and 17.9% figures | A1 magnitude |
| docomo's family-only proxy rule (combined extract) | E1 / stop condition 2 |
| Every statute and guideline text (Civil Code, Attorney Act, Consumer Contract Act, Specified Commercial Transactions Act, Telecommunications Business Act, Banking Act, APPI); the MOJ 2023 guidance; CAA committee materials | §E as a whole (counsel memo E5) |
| Provider help pages and terms (Netflix, U-NEXT, DAZN, Adobe, SoftBank, Konami, Benesse, NHK, かんぽ) | Route matrix cells |
| Money Forward and Moneytree feature pages (Moneytree help 9119773 located but not read) | C2, L1 detail |
| Rocket Money SEC filings and terms (extracts only) | US precedent detail |
| Billing-rail mix; hard-route frequency; delegation; WTP; minutes; partner fees | Primary research (PR1, E6, E3) |

## 5. Authorisation boundary respected

- **Done:** public research (search extracts), local-file inspection, calculations, research files and experiment design.
- **Not done:** outreach, account linking, cancellation attempts, purchases, spending, OAuth, credential entry, provider calls, form submissions, legal representation and live account actions.
- **Not used:** the founder's private data, the Gmail or Drive connectors, and any R-005 work. R-003 was not reopened.
- **Commit and push:** the work order does not authorise them by default. After the session's stop hook flagged untracked files, the user explicitly approved committing and pushing this folder only (2026-10-05). No PR was opened.
