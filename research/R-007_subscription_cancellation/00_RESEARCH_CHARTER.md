# R-007 Japan Subscription Cancellation Agent: Research Charter

**Status:** charter (Stage 1 of 11).
**Written:** 2026-10-05 01:45 UTC (10:45 JST).
**Scope:** desk research, calculations and experiment design only. No build, outreach, account linking, cancellation, spending, OAuth, credential entry, form submission or legal representation is authorised.

## 0. Recovery record (done before any research)

| Item requested by the work order | Found? | What was used instead |
|---|---|---|
| `/Users/japanesecobain/Documents/New project/research/` and every file listed in §3 (`codex-transition/*`, `OPPORTUNITY_PORTFOLIO.csv`, `MOAT_AND_RIGHT_TO_WIN_FRAMEWORK.md`, `NEXT_RESEARCH_ALLOCATION.md`, `SOURCE_REGISTER.md`) | **No.** This session runs in a cloud container. A filesystem-wide search for each filename returned nothing. | Nothing substituted. |
| Sakamoto / Complete Work files (`OPERATING_MANUAL.md`, `FEEDBACK_LEDGER.md`, `SAKAMOTO_MASTER_PROMPT.md`, `SAKAMOTO_GOJI_CODEX_UPDATE_20260929.md`, acceptance tests) | **No** (same search). The 8 GitHub repositories reachable from this session were also checked; none contains them. | The standard **as written in the R-007 work order §2** is applied. It is not represented as the current local version, and no one's views are imputed. |
| R-003 material | **Yes**, in this repository: `research/japan-agentic-commerce-CLA/` (commit `ebd8cdf`) and `research/japan-agentic-commerce-CLA-consolidation/` (commits `d1a10db`, `9c1061c`) | Used **only** for methods (§6). No R-003 business conclusion is inherited. |
| Primary-source access | Direct page reads are **blocked**: HTTP 403 from the egress proxy on caa.go.jp, rocketmoney.com, getmoneytree.com, and earlier on stat.go.jp, apple.com, rakuten and others. Only WebSearch result extracts are available. | Every claim is recorded as *search extract; page not opened*. A claim the decision depends on that cannot be opened stays **UNRESOLVED**. It is never promoted to "directly observed". |

**Register supersessions.** These are recorded in `REGISTER_UPDATES_PENDING.csv`. The real decision and opportunity ledgers are not in this environment, so the entries must be appended there when the founder's local files are available. Nothing historical is overwritten.
- `R-005` → `PARKED_BY_OWNER`
- `R-003` → `NO_BUILD / NO_PROTOTYPE` (unchanged)
- `R-007` → `OPEN: charter written`

## 1. Decision

> Should Aoi allocate the next validation cycle to a Japan-first subscription service whose differentiating job is **"make an unwanted recurring charge stop for me, and prove it stopped"**, not "show me my subscriptions"? If so, test exactly which customer, subscription type, cancellation mechanism, execution boundary, payer and moat hypothesis first?

Possible dispositions: **PROCEED** (one bounded test) / **NARROW-REFRAME** / **WATCH** / **PARK** / **STOP**.
- Missing evidence is recorded as `UNRESOLVED`, never as a favourable inference.
- The §29 stop conditions are mapped to the beliefs in §3.
- A B2B or B2B2C answer must earn its own evidence. It is not a default fallback.

## 2. Definitions (fixed for the whole packet)

| Term | Meaning | Not the same as |
|---|---|---|
| **Recurring charge** | A repeated debit seen on a card, bank, carrier bill or platform | A subscription contract. It may be an instalment, a utility, or an unknown merchant. |
| **Subscription** | A contract with renewal terms, an identified provider, account and plan | A recurring charge |
| **Billing route** | Who collects payment: App Store, Google Play, carrier billing, card on file with the provider, bank debit, convenience-store payment, etc. | Contract owner |
| **Contract owner** | The legal counterparty (provider or platform) and the named account holder | Billing route |
| **Cancellation requested** | An instruction sent | Cancellation accepted |
| **Cancellation accepted** | The provider confirms receipt or termination | Cancellation effective |
| **Cancellation effective** | The contract ends on a stated date | Charges stopped |
| **Charges stopped** | No further charge in the billing cycle after the effective date, observed on the billing route | A provider confirmation email |
| **On-behalf execution** | A third party performs the provider-facing cancellation steps | User-authenticated handoff, where the user performs the auth steps |

## 3. MECE issue tree with What We Need To Believe (WNTB)

At charter time, the current evidence for every row is "leads only (work order §6), unverified". The columns are `belief → falsifier → best source/test → decision consequence`.

### A. Customer need

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| A1 | A definable segment repeatedly experiences *cancellation* friction that costs material money or time, beyond "dislikes cancelling" | Friction concentrates in rare one-off events, or the money at risk per event is small relative to effort | CAA 2026 white paper and methodology; PIO-NET 定期購入 consultations; activity-selected reconstruction (E3 design) | No continuation: "people dislike cancelling" is insufficient (§32) |
| A2 | J4 (execution) and J5 (verification) are distinct residual jobs, not just J1 (discovery) or J3 (routing) | Friction is overwhelmingly *finding* the page or *forgetting*. Both are solved by a list plus guide (C01/C02). | CAA question wording; complaint categories; interview reconstruction | Reframe to a guide or tracker, which faces strong substitutes |

### B. Existing substitutes

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| B1 | Apple and Google self-service does not already cover most of the target segment's unwanted charges | The target segment's subscriptions are mostly platform-billed | Billing-route mix from surveys; route matrix | Stop condition 1 |
| B2 | Provider self-service plus PFM lists (Moneytree, Money Forward) leave a gap that users *act on* | Users who see the charge cancel easily themselves | Route-matrix step counts; interviews | Stop |

### C. Detection and data access

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| C1 | The startup can learn which subscriptions exist through a permitted, low-friction channel | Every channel needs regulated registration, restricted scopes, or manual entry users will not do | Banking Act (電子決済等代行業) rules; aggregator partner terms; Gmail policy; E2 design | Detection becomes the cost centre; C01 is commoditised |
| C2 | Detection is not a differentiator that incumbents already do better | Moneytree and Money Forward already auto-detect subscriptions | Product documentation | Differentiation must come entirely from D/F |

### D. Cancellation execution

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| D1 | Cancellation architectures repeat across economically meaningful categories, so a playbook can be reused | Each provider is idiosyncratic | Route matrix (§10) | No scalable operations |
| D2 | A meaningful subset is executable on-behalf (route C) or by a short user handoff (route B) that beats self-service | Most meaningful routes are D (account holder must act) or need MFA at each step | Route matrix; provider terms | Stop condition 3 |

### E. Legal and regulatory permission

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| E1 | Conveying a consumer's cancellation intent for a fee is permissible for undisputed cancellations | Attorney Act Art. 72 risk attaches to ordinary paid cancellation agency, or providers' terms bar third parties across relevant providers | Primary law; agency-service analogues such as 退職代行; counsel memo (E5) | Stop condition 2 |
| E2 | J6 (disputes and refunds) can be cleanly excluded or referred | Verification failures routinely turn into disputes the service cannot touch | Legal matrix; state model | J6 is excluded; J5 value is capped |
| E3 | Outcome data can be retained and generalised lawfully | APPI or contracts prevent reuse | APPI analysis | Stop condition 9 (moat dies) |

### F. Reliability and failure modes

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| F1 | Request → effective → charge-stopped can be completed with bounded human minutes and an observable verification signal | Human minutes per success exceed what any payer pays; verification needs data the service does not have | State model; E3/E4 design; economics frontier | Stop condition 5 |

### G. Economics and payer

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| G1 | A payer exists (consumer, issuer, employer or partner) whose willingness to pay exceeds the cost to serve | Free substitutes cap consumer price near zero; the partner fee is below cost | Price benchmarks (Moneytree Grow, MF premium, Rocket Money); model frontiers | Stop condition 10 |
| G2 | Usage frequency sustains the business despite the "success reduces need" paradox | Cancellation events per user per year are too few to retain a subscription | Frequency evidence; model | Must add recurring value (C06/C08/C09), which brings conflicts |

### H. Distribution

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| H1 | Acquisition at the moment of intent (wanting to cancel X) is reachable affordably | Intent moments are owned by search, the platform or the provider page | Search and channel analysis; later test | Episodic acquisition breaks the economics |

### I. Defensibility

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| I1 | Repeated execution creates an asset (outcome graph, playbooks, trust, distribution) that improves the next cancellation and is hard to copy | Procedures are scrapeable from help pages; incumbents hold larger data; providers change flows often | Moat chain test (§18) | Feature, not company (stop condition 7) |

### J. Founder right to win

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| J1f | The founder plus an identifiable cofounder profile can supply the missing capabilities: security, consumer fintech, legal, operations | The required capabilities are all absent and expensive to acquire | Capability map | Lowers priority. It is not decisive alone. |

### K. Why now / why not now

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| K1 | A specific recent change makes this newly feasible or newly needed, *and* regulation will not erase the friction before an asset forms | CAA reforms or platform changes simplify cancellation broadly within the startup's runway | CAA 2026 review materials; timelines | Stop condition 8 |

### L. Downside and incumbent response

| ID | What we need to believe | Falsifier | Best source/test | Consequence if false |
|---|---|---|---|---|
| L1 | The cheapest credible incumbent response (Money Forward or Moneytree adding "Cancel"; banks or cards adding controls; a generic agent) does not erase the wedge before the asset forms | Their existing distribution plus a guide or handoff feature replicates the core value | Competitor analysis | Stop condition 7 |

**Priority (decision-critical × uncertain):**
1. **E1** permission
2. **D2** route mix
3. **B1** platform share
4. **G1** payer and cost to serve
5. **L1** incumbent response
6. **A2** residual job

A1 matters but is the most likely to come back as "real but generic". It cannot carry continuation alone.

## 4. Mapping: §29 stop conditions → beliefs → hypotheses

| Stop condition (§29) | Beliefs | Hypotheses (§22) |
|---|---|---|
| 1. Mostly solved by Apple/Google/self-service | B1, B2 | H03 |
| 2. Third-party execution blocked across relevant providers | E1, D2 | H06 |
| 3. Too much reauthentication to beat self-service | D2, F1 | H07 |
| 4. Frequency too low | G2 | H08, H10 |
| 5. Human handling destroys contribution | F1, G1 | H07, H09 |
| 6. Only durable value is a static guide | A2, I1 | H02, H11 |
| 7. Money Forward/Moneytree can copy without a barrier | L1, I1, C2 | H12 |
| 8. Regulation eliminates the friction first | K1 | H12, H13 |
| 9. Outcome data cannot be retained or generalised | E3 | H11 |
| 10. No credible payer | G1 | H09 |

H01 maps to A1, H04 to C1, H05 to D2 and F1, H13 to K1 and J1f, and H14 to G2 and I1.

## 5. Sequencing (Complete Work: finish, verify, then move on)

| Stage | Output |
|---|---|
| S1 | This charter, plus check |
| S2 | Customer need and subscription taxonomy (§8–9) → report sections A/B; ledger rows |
| S3 | Competition and detection (§11, §14) → `03_COMPETITOR_MATRIX.csv` |
| S4 | Route matrix and state model (§10, §13) → `04_CANCELLATION_ROUTE_MATRIX.csv` |
| S5 | Permission and legal (§12) → `05_PERMISSION_AND_LEGAL_MATRIX.csv` |
| S6 | Market sizing, economics and business model (§15–17) → `06_ECONOMICS_MODEL.csv` and `model/` |
| S7 | Moat, why now, founder fit (§18–20) → `11_MOAT_AND_RIGHT_TO_WIN.md` |
| S8 | Primary-research and experiment design (§23–24) → `09_EXPERIMENT_BACKLOG.csv` |
| S9–S11 | Report, decision memo, registers 07/08/10, QA |

Each stage closes with a written check before the next starts.

## 6. Methods carried over from R-003 (methods only, not conclusions)

- **Separate the questions:** permission ≠ customer value ≠ allocation decision.
- **No path found ≠ prohibition.**
- **Unknown inputs stay blank (unknown), not zero.** A *rule zero* (for example, a programme pays nothing for an event) is labelled separately from *unknown*.
- **Scenarios are conditional illustrations, not central estimates.** Store full-precision values and round only for display. Re-import exports and recompute dependencies with unit-aware tolerances.
- **Count activation exactly once** in cohort maths. Price human minutes once, and do not double-count founder time.
- **Record evidence origin separately from claim status.** Agreement after shared feedback is not independent corroboration. One release cited by many outlets is one source family.
- **Analyse competitors by how they cause us to lose**, not as logo lists.

## 7. Charter check (performed 2026-10-05)

- **Mechanical** (`model/check_charter.py`, run below): every branch A–L has at least one WNTB with a falsifier, source/test and consequence. Every §29 stop condition maps to at least one belief. Each of H01–H14 maps to a branch.
- **Semantic:**
  - Every falsifier is observable rather than a restatement of the belief.
  - A1 is explicitly prevented from carrying continuation alone.
  - Definitions separate requested, accepted, effective and stopped.
  - The B2B2C path is held to G1, H1 and I1 like any other.
