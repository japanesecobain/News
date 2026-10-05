# R-007: Moat and right to win

Workstreams K (moat), L (why now / why not now) and M (founder fit). Evidence IDs (`E-xxx`) refer to `02_EVIDENCE_LEDGER.csv`. Competitor IDs (`CMxx`) refer to `03_COMPETITOR_MATRIX.csv`.

## 1. Conclusion first

**None of the six candidate mechanisms completes the moat chain on current evidence.**

Four are **features or service advantages, not moats**:
- M2: descriptor graph.
- M3: playbooks for web routes.
- M4: direct integrations.
- M5: trust.

Two are **conditional moat candidates**, each blocked by an unresolved permission question:
- **M1: cancellation outcome graph, restricted to hard routes** (phone, written, in person). It requires:
  - providers to accept a company messenger (L01/L02);
  - outcome data to be reusable (L11);
  - handling time to fall measurably with volume (E3).
- **M6: exclusive payer-side distribution** (a bank or card partner). It requires a partner to pay and to choose a startup over Visa or Mastercard tooling or its own PFM. The most natural Japanese partner, MUFG, already owns Moneytree [E-G07, E-G25].

**Status of the two related stop conditions:**
- **Stop condition 7** (MF or Moneytree copy without a barrier): **effectively triggered for C01–C03** and **UNRESOLVED for C04/C05 on hard routes**.
- **Stop condition 9** (outcome data cannot be retained or generalised): **UNRESOLVED**. It is answerable cheaply by counsel (L11).

## 2. Moat chain tests (M1–M6)

**M1. Cancellation outcome graph**
- **Controlled asset:** route-level records of provider × rail × account type × path × required authentication × retention intervention × success or failure × minutes × effective date × later charge state.
- **Mechanism:** each case updates the route playbook. Fewer failed attempts and fewer minutes on the next case; better verification timing.
- **Measurable benefit:** minutes per hard-route request fall, and first-attempt success rises, with cumulative cases. A learning curve in E3; *the benefit must show up against the C04 minute frontier* (§I.2).
- **Replication difficulty:**
  - Web routes (B): low. Help pages, guide sites and one individual's site (解約.com) already map them [E-G11]; general agents navigate them [E-G27].
  - Hard routes (E): medium. Scripts, wait times and acceptance rules are not public.
- **Time to replicate:** months for a funded entrant with volume (inference).
- **Who already has a stronger version:**
  - For **J5**, Money Forward and Moneytree passively observe whether charges stop across millions of linked accounts. This is an inference from their detection features [E-G03, E-G06].
  - For **J4 on hard routes**, no Japanese holder was found [E-G12].
- **Falsifier:** E3 shows minutes per hard-route case do not fall with volume, or providers refuse company messengers (L02), or flows change faster than the learning, or APPI blocks reuse (L11).
- **Classification:** *Conditional moat candidate, hard routes only.* Feature on web routes.

**M2. Descriptor → subscription identity graph**
- **Controlled asset:** a mapping from merchant descriptors to providers and plans.
- **Mechanism:** better detection precision with more data.
- **Measurable benefit:** detection precision and recall (E2).
- **Replication difficulty:** very low for incumbents.
- **Time to replicate:** none needed. They already run it.
- **Who already has a stronger version:** Money Forward (17.3M users), Moneytree (about 6.5M), Zaim [E-G01, E-G07, E-G09]. Platform and carrier rails are opaque to everyone using card data [E-G03].
- **Falsifier:** an incumbent's precision is shown to be poor *and* hard to fix. Nothing suggests that.
- **Classification:** **Feature.**

**M3. Provider playbooks**
- **Controlled asset:** step-by-step cancellation procedures.
- **Mechanism:** faster routing.
- **Measurable benefit:** time to find the route (J3).
- **Replication difficulty:** very low for web routes: scrapeable, and already aggregated free [E-G11, CM13].
- **Time to replicate:** days to weeks.
- **Who already has a stronger version:** guide sites; search; general agents.
- **Falsifier:** procedures change so often that maintained playbooks beat search. Untested; a guide site can maintain them too.
- **Classification:** **Feature.** For hard routes the playbook value is part of M1.

**M4. Direct integrations**
- **Controlled asset:** cancellation APIs or partner privileges with providers.
- **Mechanism:** machine execution (class A).
- **Measurable benefit:** automation rate.
- **Replication difficulty:** would be high, if obtainable.
- **Time to replicate:** n/a.
- **Who already has a stronger version:**
  - Visa/Pinwheel integrate 100–150+ merchants for issuers abroad [E-G25].
  - Gaining providers already cancel in electricity and mobile switching [E-C20, E-C21].
- **Why providers would refuse:** a provider has no reason to give a revenue-reducing agent an API. None was found [E-C24]. Regulation targets obstruction, not APIs [E-A17].
- **Falsifier:** a provider grants an API (none found).
- **Classification:** **Not available.** Feature at best.

**M5. Trust**
- **Controlled asset:** a reputation for safe handling of account actions.
- **Mechanism:** users delegate more and churn less.
- **Measurable benefit:** delegation rate (H05) and retention.
- **Replication difficulty:** trust takes time, but incumbents start far ahead.
- **Time to replicate:** n/a (incumbents start ahead).
- **Who already has a stronger version:** banks, card issuers, Money Forward (listed), Moneytree (MUFG-owned), and the free 188 hotline [E-G07, CM14].
- **Falsifier:** a startup's delegation rate exceeds an incumbent's for the same task. Untestable before launch.
- **Classification:** **Service advantage, not a moat.**

**M6. Distribution through a bank or card partnership**
- **Controlled asset:** an exclusive embed in a partner's app.
- **Mechanism:** low CAC and payer-funded revenue (C07).
- **Measurable benefit:** CAC and the partner fee (C07 frontier: ¥5.86–18.37 per enrolled user-month).
- **Replication difficulty:** high *if* exclusive; low if not.
- **Time to replicate:** a bank sales cycle (long; inference).
- **Who already has a stronger version:**
  - MUFG owns Moneytree [E-G07].
  - Visa and Mastercard sell issuer tooling abroad [E-G25, E-G26].
  - SMBC and other banks were MT LINK clients (dated) [E-G08].
- **Falsifier:** no Japanese issuer will pay at least the C07 floor, or issuers choose network tooling.
- **Classification:** *Conditional moat candidate.* It depends on one discoverable number: partner willingness to pay.

**What must be true for any moat (§32).** A specific hard-route workflow must be:
1. permitted for a company messenger;
2. frequent enough to generate learning;
3. measurably cheaper with volume; and
4. paid for by someone,

and all of this must happen **before** the obstruction ban removes the friction for compliant providers (about 2027–28) [E-A17].

## 3. Why now / why not now

| Force | Direction | Evidence | Strength |
|---|---|---|---|
| Subscription penetration | Why now | Usage common in non-probability samples [E-A14]; SVOD +14.3% in 2025 on price and stacking [E-B07] | Moderate (no probability base) |
| CAA cancellation-friction evidence | Why now, and why not now | About 20% report trouble [E-A01]; 定期購入 about 80–98k consultations a year [E-A04]. The same evidence drives the obstruction ban [E-A17] | Two-sided |
| Better recurring-charge classification | Why not now (for a startup) | Already deployed by incumbents [E-G03, E-G06] | Strong against |
| Capable AI agents | Why not now (for C03) | A general agent navigates web flows for users who already pay [E-G27] | Commoditises C03 |
| Cheap language and call automation | Ambiguous | Providers automating *inbound* lines [E-K01]: may cut call cost or add holder-only gates | Unknown |
| Consumer familiarity with agents | Not established | No Japanese evidence searched | — |
| Regulation simplifies cancellation | Why not now | Ban on refusal, delay and misrepresentation; effort duties; bill as early as 2027 [E-A17, E-E13] | Strong against (for hard-route friction) |
| Mobile Software Competition Act | Ambiguous | Outside payments allowed from 2025-12-18 [E-G30]; may move subscriptions to fragmented rails | Unknown magnitude |
| Incumbent data and distribution | Why not now | MF 17.3M; Moneytree/MUFG; Visa/Mastercard tooling [E-G01, E-G07, E-G25] | Strong against |
| Apple and Google own their rails | Why not now | Only the user can cancel there [E-B03, E-B04] | Strong against (for those rails) |
| Legal barriers | Why not now | Art. 72 boundary contested; analogue enforcement in 2025–26 [E-E03, E-E04]; family-only proxy [E-C10] | Unresolved, leaning against |
| MFA and re-authentication | Why not now | Network PIN on carrier routes [E-C04]; holder-only online flows [E-C10] | Moderate |
| Low frequency and low WTP | Why not now | About 0.25 cancellations per app user at the US analogue [E-G17]; ¥280–540 anchors for tracking [E-G10, E-G05, E-G02] | Strong against B2C |

**Net:**
- **No manufactured "why now".** The only genuinely new force (agents) commoditises the easy part.
- **The regulatory force cuts both ways and has a date.**
- **A window exists only for hard routes, only until about 2027–28, and only if permission holds.**

## 4. Founder fit (Workstream M)

These are factual inputs from the founder profile supplied to this session. **None is a moat.**

| Founder attribute | Relevance to R-007 |
|---|---|
| Bilingual Japanese/English; lived in Japan, Hong Kong and the US | Can read US precedents (Rocket Money, FTC) and Japanese regulation; can run Japanese-language discovery (S8) |
| Investment research (UTEC) | Desk underwriting; hypothesis discipline |
| Business analytics and automation (BASE FOOD) | Instrumenting E2/E3; route-level data design |
| FP&A (Gojo) | Unit economics; frontier modelling |
| Philosophy major, finance minor | Structured argument; useful for the counsel brief and claims discipline |
| Bowdoin College Class of 2028 (current student) | **Bandwidth constraint** for a service-operations business (E3 concierge hours; phone routes run in business hours) |

**Missing capabilities, with the work-order list checked:**
- **Consumer fintech:** missing.
- **Security:** missing. Credential-free design reduces but does not remove the need.
- **Bank and card data infrastructure:** missing. Would come through a partner, and the partners are competitors.
- **Regulatory and legal (Japanese consumer law, Attorney Act):** missing. **Most critical.**
- **Consumer growth:** missing. Intent traffic is held by guide sites.
- **High-volume service operations (contact centre):** missing.
- **Provider and bank partnerships (B2B sales to banks or issuers):** missing. Critical for M6.

**What the ideal cofounder would contribute,** in order:
1. Japanese payments or banking partnership experience (issuer, bank or PFM product), for M6 and the partner-fee question.
2. Contact-centre or consumer-operations leadership, for M1 learning curves and the minutes frontier.
3. A standing relationship with Japanese counsel experienced in Attorney Act and consumer-contract matters. An adviser, not necessarily a cofounder.

The founder profile is strongest at exactly the work this assignment allows (research, discovery, modelling). It is weakest where R-007 would be won or lost (permission, partnerships, operations).

## 5. Checks performed on this file

- **Each moat row completes all seven chain fields, or names the field it cannot complete.** None was left blank to avoid a "feature" verdict.
- **No mechanism is called a moat for AI, Japan localisation, first-mover status, UX, detection, or purchase history** (work order §18).
- **The founder section uses only facts from the supplied profile.** No motivation or experience was invented. The student-bandwidth point is a factual constraint, not a judgment of ability.
