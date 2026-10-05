# R-007 Japan Subscription Cancellation Agent: Research Report

**Status:** complete (Stages 1–11). Sections carry the work-order workstream letter. Each stage's written check is in `12_QA_RECEIPT.md`.

**Evidence convention:**
- `[E-xxx]` refers to a row in `02_EVIDENCE_LEDGER.csv` (`R7-E-xxx`).
- No source page could be opened (egress 403). Every claim rests on search extracts, so no claim is `directly observed`. Statuses follow the ledger vocabulary (company-reported, reported_unopened, corroborated, calculated, inference, unresolved).
- "UNKNOWN" means no public evidence was found. It never means zero.

---

## Executive summary

**Disposition: PARK.** Do not allocate the next validation cycle to R-007 as framed.

The concept is "a Japan-first service that finds all recurring subscriptions, cancels them on the user's behalf, and verifies the charges stopped". **Public evidence does not identify a workflow that consumers demonstrably pay for, that a startup can execute better than free or incumbent tools, that the economics support, and that compounds into an asset before incumbents or regulation close the gap** (work order §32).

**What the evidence supports:**
- **Unwanted recurring charges are common, and a minority report cancellation trouble.** About 20% report trouble [E-A01]. Forgetting is common in two independent surveys [E-A16]. 定期購入 generates about 80–98k consultations a year [E-A04]. This goes beyond "people dislike cancelling", but not far.
- **The easy parts are taken:**
  - Discovery is held by Money Forward (17.3M users) and Moneytree (about 6.5M, MUFG-owned), which detect card and bank subscriptions, and by the platforms' own lists [E-G01–G07, E-B02].
  - Routing, the most-cited trouble (46.0%: "could not find the page"), is solved free by guide sites and search [E-A03, E-G11].
  - User-run web flows are 14 of 22 sampled routes [E-C24]; general AI agents already navigate them [E-G27].

**What survives is narrow:** executing **hard routes** (phone only, written, in person) and **verifying the stop**. Every gate on that workflow is unresolved or adverse:
- **Permission:** UNRESOLVED.
  - Art. 72 is contested, and the closest analogue industry saw enforcement in 2025–26 [E-E03, E-E04].
  - The only explicit provider rule found limits proxies to family [E-C10].
- **Frequency:** low.
  - The US precedent shows about 0.25 cancellations per app user, cumulative [E-G17].
  - Illustrations put steady-state requests at 0.09–0.6 per user-year.
- **Payer:**
  - Pay-per-cancellation does not pay back in either illustration (§I).
  - Cancellation savings justify only ¥22.50–450 a month of subscription against ¥300–540 prices: the paradox.
  - B2B2C works only on an assumed partner fee, and the natural partner (MUFG) owns Moneytree while Visa and Mastercard sell the capability abroad [E-G07, E-G25].
- **Moat:** only conditional candidates (M1, M6).
- **Clock:** an obstruction ban is planned, with a bill as early as 2027 [E-A17].

**Unpark if any of these happens:**
- **E5 counsel memo** finds a paid company messenger for undisputed cancellations workable, with a reliable basis for provider acceptance.
- **E6** finds a Japanese issuer or bank paying at least the illustrative floor (¥5.86–18.37 per enrolled user-month).
- **PR1** shows at least 30% of an activity-selected segment hit a hard-route cancellation each year and that at least half of those delegated it or gave up.

**The single experiment that changes the decision most is E5.**

## Stop-condition assessment (work order §29)

| # | Stop condition | Status | Basis |
|---|---|---|---|
| 1 | Mostly solved by Apple, Google or provider self-service for the target segment | **Effectively triggered** for digital subscription stackers; not triggered for hard-route segments | §B, §C; [E-B03, E-B04, E-C24, E-G29] |
| 2 | Third-party execution blocked across relevant providers | **UNRESOLVED**, leaning against company agents | §E; [E-C10, E-E02–E05] |
| 3 | Too much re-authentication to beat self-service | **Effectively triggered** on user-run routes (the user authenticates anyway); UNKNOWN on hard routes | [E-C04, E-C10] |
| 4 | Frequency too low | **Leaning triggered** for B2C (illustrations; US analogue); UNRESOLVED in Japan | §I; [E-G17] |
| 5 | Human handling destroys contribution | **UNRESOLVED**: infeasible at a ¥500 fee; up to about 123 min at ¥1,500 under loose assumptions | §I.2 |
| 6 | Only durable value is a static guide | **Triggered for web routes** (C02/C03) | [E-G11, E-G27] |
| 7 | MF or Moneytree can copy without a barrier | **Effectively triggered for C01–C03**; UNRESOLVED for C04/C05 on hard routes | §G, §K |
| 8 | Regulation eliminates the friction first | **Leaning**: bill as early as 2027 targets refusal, delay and misrepresentation | [E-A17, E-E13] |
| 9 | Outcome data cannot be retained or generalised | **UNRESOLVED** (counsel question L11) | §E |
| 10 | No credible payer | **UNRESOLVED**; negative for B2C pay-per-use; B2B2C depends on one number | §I, §J |

No condition is resolved in the concept's favour. Two are triggered for the easy parts of the concept, and the rest are unresolved or leaning against. Under the work-order rule ("UNRESOLVED, not favourable inference"), positive underwriting stops here. **PARK** is chosen over STOP because the binding gate (E5) is cheap, and over WATCH because no trigger is expected to improve the thesis without founder action.

## §A. Customer need (Workstream A)

### A.0 Conclusion first

The public record supports three things:
1. Paying for unwanted recurring charges is common.
2. A minority of users report trouble when cancelling.
3. The largest complaint pocket is physical-product 定期購入.

It does **not** show that *execution* is the residual job. The most-cited cancellation trouble is *finding the cancellation route*, which a guide solves. The execution-heavy frictions the public record does show (phone-only 定期購入 lines, written or in-person gym cancellation) cluster around non-cooperative providers. In those cases an agent meets the same obstruction the consumer does, and the remedy is a dispute (J6) or the regulator. These are also exactly the conduct targeted by the 2026–27 obstruction ban.

**Status for the charter beliefs:**
- **A1 holds only directionally.**
- **A2 is UNRESOLVED and leans against.**
- Delegation willingness, willingness to pay (WTP) and minutes per cancellation are UNKNOWN from public data.

### A.1 What the evidence measures, and against what

| Number | What exactly it is | Compared with | Why the difference matters |
|---|---|---|---|
| About 20% ("約2割") report cancellation trouble [E-A01] | CAA 2026 white-paper survey; subscription users among respondents. The base, n and wording are unconfirmed. The lead figures 17.9% and 71.6% were **not found** [E-A02]. | The about 80% who report no trouble | At best 1 in 5 users has had trouble, and "trouble" is undefined. This is incidence, not demand. It says nothing about how many would delegate or pay. |
| 46.0% "could not find the page / it was deep in the site"; 45.7% "procedure complicated / too many steps" [E-A03] | Shares among those who had trouble (multiple answers presumed) | Each other, and the unseen options | The top friction is **J3 routing**, which a deep link or guide removes. "Complicated" mixes J3 and J4. Phone-only, in-person or "charged after cancelling" options were not visible in the extract. |
| 定期購入 consultations: 98,189 (2022), 80,302 (2023), 89,044 or 89,893 (2024) [E-A04] | PIO-NET consultation counts for mail-order recurring physical purchases | About 9.75% of FY2024's 913k total consultations [E-A19] (calendar/fiscal mismatch; order of magnitude only) | A top-tier complaint category, mostly trial-to-subscription traps in cosmetics and supplements, skewing 50+ [E-A05]. These are consultations, not consumers. |
| About 500 "サブスク" consultations per month (FY2021) [E-A08] | Kokusen's subscription code in 2021 | About 6,000 a year, against about 80–98k 定期購入 a year | Most *complaint* volume sits in physical 定期購入, not digital subscriptions. Coding differences mean this is not true incidence. |
| 65+ are 37.7% of all FY2025 consultations [E-A06] | Age share of contract parties, all topics | 29.4% of the population is 65+ [E-A07]; ratio 1.28 [E-A15] | Seniors are over-represented among complainants. This is all topics, not subscriptions, and only hints at a family-assisted segment. |
| 50.5% of subscribers were auto-billed after a forgotten trial; 19.1% hold a barely used, uncancelled subscription [E-A12] | n=330 users of a personal-finance platform (finance-engaged; non-probability) | AZWAY: over half paid for a forgotten subscription, n=300 [E-A13] | Two independent families agree on direction [E-A16, corroborated]. **Forgetting (J1) is the common pain, not inability to cancel.** |
| Modal monthly subscription spend ≤¥2,000 [E-A14] | n=400 CrowdWorks registrants (self-selected, younger) | A forgotten ¥1,000/month service costs ¥12,000 a year only if it runs a full year (illustration, not an estimate) | Money at risk per user is modest, which caps any savings-linked fee. |
| SVOD: about 2.0 services per user (from 1.8); top three = 56.3% of spend [E-B07, E-B08] | GEM Partners estimate, 2025 | Prior year | Few subscriptions per user, concentrated in a few providers. A small playbook covers most SVOD spend, which also makes it easy to copy. |

### A.2 Jobs J1–J6 (kept separate)

"UNKNOWN" means no public evidence was found. Minutes and steps are UNKNOWN for every job; no Japanese timing data was found, so they are measured in the S8 design.

**J1 Discovery: "What am I paying for?"**
- **Trigger:** a statement review, a surprise charge, a trial converting [E-A12], or a budget review.
- **Frequency:** UNKNOWN. About half reviewed within a year [E-A14]; about a third have no review habit [E-A12]. Reviewing is not discovering.
- **Pain:** paying for unused subscriptions. Common in direction [E-A16].
- **Money at risk:** modest; the modal total is ≤¥2,000 a month [E-A14].
- **Workaround:** a monthly statement check (official advice [E-A09]); Apple/Google lists; carrier continuous-charge lists [E-B02].
- **Strongest substitute:** free platform and carrier lists, plus PFM apps (S3).
- **Delegation:** this is data access, not delegation (H04). UNKNOWN.
- **WTP:** UNKNOWN; free substitutes exist.
- **Payer if not the consumer:** UNRESOLVED (S6).

**J2 Optimisation: "Which should I keep?"**
- **Trigger:** price increases, which drove 2025 SVOD growth [E-B07]; budget pressure.
- **Frequency, pain and money at risk:** UNKNOWN (money at risk as J1).
- **Workaround and substitute:** own judgment and usage memory.
- **Delegation:** low by nature, since it is a preference (inference).
- **WTP:** UNKNOWN.
- **Payer:** none identified.

**J3 Routing: "How do I cancel this?"**
- **Trigger:** the decision to cancel.
- **Frequency:** UNKNOWN.
- **Pain:** "could not find the page" is the most-cited trouble (46.0%) [E-A03]. Consumers wrongly believe deleting an app cancels it [E-A09]. The carrier rail is ambiguous about where to cancel [E-B02].
- **Money at risk:** the remaining charges on one subscription.
- **Workaround:** web search, provider help pages, guide sites.
- **Strongest substitute:** provider help page plus search; Apple and Google settings for platform-billed subscriptions [E-B03, E-B04].
- **Delegation:** little need.
- **WTP:** likely low for an information good (inference).
- **Payer:** affiliate or advertising for guide sites (S3).

**J4 Execution: "Cancel it for me."**
- **Trigger:** the route is known but hard: phone-only lines that do not connect before a shipment deadline [E-A05]; a written form or in-store visit [E-B05]; "complicated" procedures [E-A03].
- **Frequency:** UNKNOWN.
- **Pain:** missed deadlines mean another shipment or month is billed.
- **Money at risk:** the next shipment or month (amount UNKNOWN per case).
- **Workaround:** repeated calls, keeping evidence of contact attempts (Kokusen advice [E-A05]), the consumer hotline 188.
- **Strongest substitute:** self plus 188 (free).
- **Delegation:** UNKNOWN. **No Japanese evidence was found on willingness to let a company cancel on one's behalf.**
- **WTP:** UNKNOWN.
- **Payer:** UNKNOWN.

**J5 Verification: "Did it actually stop?"**
- **Trigger:** a charge after cancelling.
- **Frequency:** UNKNOWN. It is a recognised complaint type [E-A08], with concentrated bad actors (about 1,600 consultations for one provider [E-A10]) and gym forms that were "not processed" [E-B05].
- **Money at risk:** continuing charges until noticed.
- **Workaround:** a monthly statement check [E-A09].
- **Strongest substitute:** the statement itself. For platform and carrier rails the statement shows only an aggregate line [E-B06].
- **Delegation:** passive monitoring needs transaction-data access (H04).
- **WTP:** UNKNOWN.
- **Payer:** UNKNOWN.

**J6 Dispute or refund: "They still charged me."**
- **Trigger:** the provider is unresponsive or refuses.
- **Frequency:** UNKNOWN.
- **Pain:** documented [E-A10].
- **Money at risk:** charges already taken.
- **Workaround:** consumer centre (188), card dispute (S5), and in future, injunctions by qualified consumer organisations [E-A17].
- **Strongest substitute:** free public consultation.
- **Delegation:** the legal boundary (弁護士法72条) is untested here (S5).
- **WTP and payer:** UNKNOWN.

**Reading across the jobs.**
- **Where evidence is strongest:**
  - J1 is common and has free substitutes.
  - J3 is the top-reported trouble and has cheap substitutes.
- **Where evidence is weakest:** J4 and J5, the differentiating jobs in the thesis, have the least evidence on frequency, delegation and payment.
- **What the jobs that do show friction have in common:**
  - J4 friction appears in phone-only 定期購入 and in-person gyms.
  - J5 friction appears where providers do not process cancellations.
  - Both are where the provider's cooperation is weakest, and J6 starts there.

### A.3 Is "people dislike cancelling" all we have?

Partly. Three facts go beyond dislike:
- A large, measured complaint category (定期購入, about 10% of all consultations [E-A19]).
- A named failure mode in which a cancellation request did not stop billing [E-A08, E-A10, E-B05].
- An identifiable channel friction: phone-only lines with a deadline [E-A05].

None of them yet shows that a third party can fix the problem better than the consumer plus the free 188 hotline, or that anyone will pay. Under the §32 standard, S2 alone has **not earned continuation**. It earns only the right to test specific routes in S4.

### A.4 Candidate segment pockets

These are hypotheses for later stages to test, not customers selected.

| Pocket | Evidence | Jobs that bind | Why it might matter | Why it might not |
|---|---|---|---|---|
| P1 定期購入 trial-trap victims (50+, cosmetics, phone-only) | [E-A04, E-A05, E-A19] | J4, J5, J6 | Largest measured complaint volume. A concrete channel friction (phone plus deadline). | Providers are often adversarial, so the agent meets the same wall. Disputes border on J6/Attorney Act (S5). One-off events with low repeat use (G2). Directly targeted by the obstruction ban [E-A17]. |
| P2 Digital subscription stackers (younger; SVOD, music, apps) | [E-A12, E-A14, E-B07] | J1, J3 | Many users. Forgetting is common. | Money at risk is modest. Platform and carrier lists are free [E-B02–B04]. A guide suffices for J3. |
| P3 Families of seniors | [E-A06, E-A15] | J1, J4 (via family) | Seniors are over-represented among complainants. Delegation already happens within families. | Not subscription-specific. The natural agent may be the child, not a company. Authority and consent within families is a legal question (S5). |
| P4 Bereaved families | [E-A11] | J1 (without credentials), J4 | High pain at a moment of need. The acting party is not the account holder by definition. | Low frequency per family. Provider bereavement processes vary (S4). The payer is UNKNOWN. |
| P5 Gym and physical memberships | [E-B05] | J4, J5 | A written or in-person channel; a documented "not processed" failure. | Local and fragmented. In person may require the member (S4/S5). |

## §B. The subscription universe by billing and cancellation mechanism (Workstream B)

### B.0 Conclusion first

The rails split into three groups.
- **Platform rails (Apple, Google):** a free, complete cancellation surface exists, but only the user can use it [E-B03, E-B04]. A third party can at best guide a handoff. Card data cannot see which subscription is behind the aggregate charge [E-B01, E-B06].
- **Carrier-billed content:** the carrier lists the charges, and cancellation runs through either the carrier portal or the provider; the evidence conflicts [E-B02].
- **Direct, telco, membership and 定期購入 rails:** these hold the frictions in §A. Their cancellation channels and third-party acceptance are UNKNOWN until S4/S5.

**No public data splits Japanese subscriptions by rail [E-B10].** The size of the "solved by Apple/Google" share (stop condition 1) therefore **cannot be established from public research** and must be measured.

### B.1 Taxonomy

For each category the matrix records the fields work-order §9 asks for. UNKNOWN cells carry the stage that resolves them per provider (`S4` route matrix, `S5` legal matrix). Contract-owner entries marked *inference* come from how each rail works, not from a source, and are checked in S5.

| Field | Platform: Apple | Platform: Google Play | Direct digital (card on file) | Telco / ISP / carrier-billed content | Physical memberships (gym etc.) | Recurring physical products (定期購入) | Professional / learning | Regulated (insurance, finance, utilities, healthcare) |
|---|---|---|---|---|---|---|---|---|
| Billing rail | Apple; one card descriptor APPLE.COM/BILL [E-B01] | Google Play | Provider charges the card or bank directly (by definition) | Phone bill (carrier billing) or the carrier's own plan [E-B02] | Bank debit reported [E-B05]; others UNKNOWN | UNKNOWN per seller (S4) | UNKNOWN (S4) | UNKNOWN (S4) |
| Contract owner | Service provider, with Apple running billing and renewal (inference; S5) | Service provider, with Google running billing (inference; S5) | Service provider | Carrier for plans; content provider for carrier-billed content (inference; S5) | Club operator | Seller | Provider | Regulated entity; named holder (inference; S5) |
| Cancellation channel | User's Apple account; the developer cannot cancel [E-B04] | User's Play settings; the developer can cancel via API [E-B03] | Provider web/app; sometimes deep or complex [E-A03] | Carrier portal or provider site (conflicting [E-B02]) | Written form or in store reported [E-B05] | Phone reported as hard to reach [E-A05] | UNKNOWN (S4) | UNKNOWN (S4) |
| Minimum term | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4/S5) | Campaign contracts may bar cancellation for a period [E-B05] | UNKNOWN (S4/S5) | UNKNOWN (S4/S5) | UNKNOWN (S5) |
| Cancellation deadline | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | A deadline before the next shipment is implied [E-A05] | UNKNOWN (S4) | UNKNOWN (S5) |
| Early-termination cost | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN; statutory limits to check (電気通信事業法; S5) | Penalties possible under campaign terms [E-B05] | UNKNOWN; fee rules to check (S5) | UNKNOWN; statutory mid-term rules to check (特定継続的役務; S5) | UNKNOWN (S5) |
| Authentication | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) |
| Third-party authorisation accepted? | No path found for third parties [E-B04] | No path found for third parties [E-B03] | UNKNOWN (S4/S5) | UNKNOWN (S4/S5) | UNKNOWN (S4/S5) | UNKNOWN (S4/S5) | UNKNOWN (S4/S5) | UNKNOWN (S5) |
| Account holder required? | Effectively yes: only the user or Apple support [E-B04] | Effectively yes for anyone but the developer [E-B03] | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S5) |
| Evidence of completion | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) | Carrier list status, if it updates (S4) [E-B02] | UNKNOWN. Documented failure: form submitted but not processed [E-B05] | UNKNOWN (S4) | UNKNOWN (S4) | UNKNOWN (S4) |
| Next-charge verification | Card shows only APPLE.COM/BILL, so it is ambiguous; Apple-side data needed [E-B06] | UNKNOWN: descriptor format not checked (S3) | Card or bank line if the descriptor matches the brand (S3) | The card shows only the phone-bill total [E-B06]; the carrier list may show it [E-B02] | Bank-debit line (descriptor match UNKNOWN; S3) | Card line, or no further shipment (inference) | UNKNOWN (S4) | UNKNOWN (S4) |

### B.2 What the taxonomy changes

1. **The verification job (J5) is rail-dependent.** On the platform and carrier rails, card or bank data cannot confirm that a *specific* subscription stopped [E-B06]. "Verified stop" therefore needs a second data channel there, or must be limited to the direct, membership and 定期購入 rails.
2. **Execution on platform rails is user-only.** For Apple and Google the best a third party can offer is a guided handoff (route B). It competes with Apple's and Google's own free screens.
3. **The remaining rails are where §A's frictions live, and where every third-party question is open.** S4 and S5 must therefore sample them in particular: phone-only 定期購入, gyms, telco content and direct digital.
4. **Regulated categories are excluded from the first test.** This is a scoping choice, not a finding: cancelling insurance or finance products can carry consequences that border on advice, and identity requirements are strongest there.

## §C. Cancellation-route matrix (Workstream C)

### C.0 Conclusion first

**No sampled route offers a third party a documented machine path (class A). None shows that a company agent is permitted (class C).**

- **Class B, 14 of 22 sampled routes:** user-run web, app or platform flows. A startup can only guide or hand off, and those steps are already guided free by Apple and Google, guide sites, and general AI agents.
- **Class E, 8 of 22:** routes that need a human (phone only, in person, written forms, conditional contracts) or whose channel is unknown. Here a concierge would add value, but **whether providers accept a third-party agent is UNKNOWN for every one of them**.
- **The only explicit agent rule found excludes companies.** docomo limits proxies on individual contracts to family [E-C10]. This is decision-critical and must be confirmed on docomo's own page.
- **The industry already does on-behalf cancellation** in two regulated switches, but the agent is the *gaining provider*:
  - Electricity: the new retailer cancels the old contract [E-C20].
  - Mobile number portability: the new carrier starts the switch and the user consents in the old carrier's portal [E-C21].

The counts describe a purposive sample of 22 routes. **They are not market shares** [E-C24].

### C.1 Which architectures repeat across meaningful categories?

This is the work order's key question, answered from `04_CANCELLATION_ROUTE_MATRIX.csv`.

| Architecture | Sampled routes | Categories it spans | What a startup can add | Who already covers it |
|---|---|---|---|---|
| Web/app self-serve behind the user's login | Netflix, U-NEXT, Amazon Prime, Disney+ direct, Spotify, YouTube Premium, chocoZAP, スタディサプリ (8) | SVOD, music, video, app-based gym, learning | Routing: which rail holds the contract. Deep links, reminders. | Guide sites [CM13], PFM incumbents adding links [CM01–03], general agents [CM19] |
| Platform settings (Apple, Google) | RM01–02 (2) | Every app-billed category | Telling the user to go to Settings | Apple and Google, free [CM04–05] |
| Carrier portal with re-authentication | Disney+ via docomo, dアニメストア (2) | Carrier-billed content | Identity resolution (6 windows for one service [E-C12]) | Carrier lists [CM07] |
| Term contract (cancel ≠ charges stop) | DAZN annual, Adobe annual (2) | Sports streaming, software | Explaining the fee or term; scheduling cancellation for the cheap window | No one, but the value is informational |
| Phone-only with a fee window or retention script | SoftBank 光, 進研ゼミ, NHK (3) | Fibre, learning, broadcast | **A human caller, if third-party callers are accepted (UNKNOWN)** | 188 for disputes [CM14] |
| In person or written | Konami (1); gyms generally [E-B05] | Physical memberships | **A proxy visit or written notice, if accepted (UNKNOWN)** | None found |
| Formal written agency (restricted) | docomo (family only), かんぽ生命 (relationship field, intent call) (2) | Telco, insurance | Preparing paperwork for a *family* agent | — |
| Skip/pause ≠ cancel | Oisix (1) | Food boxes | Avoiding the "skipped, not cancelled" trap | — |
| Gaining-provider switching (mechanism, not a matrix row) | Electricity switching; MNP one-stop | Electricity, mobile | Only as the *new provider's* agent (C08) | Price-comparison and switching sites (not researched here) |

**Reading.** Where execution is easy (B), it is commoditised. Where it is hard (E), permission is unknown, and the one explicit rule excludes companies. A cancellation service would therefore first test, not assume:
- whether providers on phone, in-person and written routes accept an authorised company agent; and
- whether the family member can be the agent while the company prepares and tracks the action. This *family-assisted* design satisfies a family-only rule by construction.

### C.2 Cross-cutting findings from the matrix

1. **The route depends on the billing rail, not the brand.** Netflix has six rails [E-C01], Spotify five [E-C06], dアニメストア six windows [E-C12]. "Cancel Netflix for me" first needs a confirmed rail, which feeds the state model.
2. **The same brand can have different effective dates by rail.** Disney+ via docomo stops immediately, with no refund. Disney+ direct runs to period end [E-C04]. Verification timing is rail-specific.
3. **"Charges continue" is sometimes correct.** DAZN annual continues monthly payments to term end [E-C05]. Adobe annual charges 50% of the remainder [E-C08]. A "charges stopped" metric that ignores the contract would score these as failures.
4. **Provider terms are a recurring obstacle to credential-based execution.** Netflix restricts accounts to the household [E-C22]. U-NEXT bars third-party use of IDs [E-C23]. Whether a one-off cancellation login by an agent breaches these terms is for S5. The compliant pattern is the user logging in (B).
5. **Regulated sectors already have proxy machinery, but tightly scoped.** かんぽ生命 asks the agent's relationship and may phone the policyholder [E-C19]. docomo restricts proxies to family [E-C10]. Both suggest that a *company* agent is the exception, not the rule.

### C.3 What the route matrix does not establish

- **Third-party caller or visitor acceptance** on any phone or in-person route. All 8 E routes are UNKNOWN. This is the single largest gap, and it decides whether C04/C05 exist at all.
- **Steps and minutes as observed.** Step counts come from how-to articles, not observation.
- **Coverage.** Cosmetics and supplement 定期購入 sellers, the largest complaint pocket [E-A04], **could not be sampled**: no seller-specific cancellation evidence was found in one attempt (FANCL). Newspapers, Anytime Fitness Japan and bundled telco content were also not sampled.
- **Confirmation artefacts** (e-mail, screen, written receipt). These are mostly UNKNOWN, but they are what J5 verification would rest on.

## §D. Detection and data acquisition (Workstream D)

### D.0 Conclusion first

**Detection is not a wedge for a new entrant on any billing rail.**
- **Card and bank rails:** Money Forward ME (17.3M users; premium ¥540/month) and Moneytree (about 6.5M users; Grow ¥360/month; owned by MUFG since 2025-08-29) already detect subscriptions [E-G01–G07, E-D03].
- **Platform and carrier rails:** the rail owner's own free list is complete for that rail. Card data cannot see inside these rails, and Money Forward states this itself [E-G03, E-B01, E-B02].

What remains is a single cross-rail view. That serves J1 (forgetting), where standalone trackers already charge ≤¥300 a month [E-G10]. **A startup should borrow detection, not build it.** In a first test that means user-supplied lists or screenshots; at scale, a partner. Its advantage, if any, must come from execution and verification on the fragmented rails.

### D.1 Channel comparison

| Channel | What it sees | Coverage gaps | Permission and regulation | Who already has it | Verdict |
|---|---|---|---|---|---|
| Bank and card aggregation | Card and bank lines; recurring patterns | Platform and carrier charges appear only as aggregate lines (APPLE.COM/BILL, phone bill), as Money Forward confirms [E-G03, E-B06] | Bank data needs 電子決済等代行業 registration or a registered partner (S5). The partners are MT LINK (MUFG-owned) or Money Forward, both competitors [E-G07, E-G08] | Money Forward, Moneytree, Zaim [E-G01–G09] | No advantage. Using a partner means relying on a competitor's pipe. |
| E-mail receipts | Receipts, including platform receipts if mailed (whether every platform mails a per-app receipt: UNKNOWN) | Users who use several mailboxes; Japanese template variety (UNKNOWN) | Gmail restricted scope requires an annual CASA Tier 2 review if data passes through a server (about $500 a year per a secondary source); APPI (S5) [E-D01] | サブトラ (¥280/month) [E-G10] | Feasible but gated. The best second channel for platform rails. |
| App Store and Google Play | The complete list for that rail | Nothing outside the rail | No third-party read API found [E-D02] | Apple and Google, free [E-G29, CM04–05] | The user must show it (screenshot) or act on it. |
| Carrier billing | The continuous-charge list in the carrier portal | Not visible to card data [E-B06] | No third-party route found [E-D02] | Carriers, free [E-B02] | The user must show it or act on it. |
| Manual entry or screenshot | Whatever the user enters | Accuracy and completeness depend on the user | Lowest regulatory burden; APPI for images (S5) | Recur and other free trackers [E-G10] | Adequate for a first test. No moat. |
| Hybrid (incumbent detection plus startup execution) | Incumbent's list; startup acts on the selected item | Depends on a partner | A contract with Money Forward or Moneytree | n/a | A possible "execution layer for PFMs" model. Tested as a C07 variant in S6/S7, but the partners are also the most likely copiers. |

### D.2 Can Moneytree or Money Forward detect the same thing more cheaply and with greater trust?

**Yes, on card and bank rails.** They already do, through regulated connections, at ¥360–540 a month, with brands, and in one case with a megabank owner [E-G02, E-G05, E-G07]. **No one detects inside platform or carrier rails from card data, them included** [E-G03]. Those rails have their own complete free lists, though, so the gap is the *aggregated view*, not missing information.

Detected recurring charges are also not identified contracts, and neither gives authority to cancel. No incumbent was found claiming either [E-G06]. That is the boundary of what detection buys.

## §E. Permission and legal operating boundary (Workstream E)

**This section is not legal advice.** It sorts constraints into law, provider contract, technical restriction and unknown, and states the questions Japanese counsel must answer (E5). Every row of `05_PERMISSION_AND_LEGAL_MATRIX.csv` has a counsel question unless it is purely factual.

### E.0 Conclusion first

**Permission is the binding uncertainty, and the evidence leans against a paid company agent.**

- **No source establishes that a paid company may cancel consumer subscriptions on a user's behalf in Japan.** No source establishes that it may not, either. Stop condition 2 is **UNRESOLVED, not triggered**.
- **Attorney Act Art. 72.**
  - The closest analogue, resignation agencies, suggests conveying a person's own decision is acceptable for a non-lawyer, while negotiation is not [E-E02].
  - Whether ordinary cancellation is a 'legal matter' is contested [E-E04]. The most recent official reasoning (MOJ, 2023) applied a dispute test, but in a different context [E-E05].
  - Enforcement in that analogue industry is current: the モームリ search (2025-10) and indictment (2026-02-24) concerned paid lawyer referrals [E-E03].
- **Provider contracts.** The one explicit agent rule found (docomo) is family-only [E-C10]. かんぽ生命 asks for the agent's relationship to the policyholder and may phone the policyholder to confirm intent [E-C19]. Netflix and U-NEXT terms restrict account use [E-C22, E-C23].
- **Law already compresses some value pools.** Telecom exit fees are capped (¥1,000 mobile; about one month fixed) [E-E08]. 定期購入 sellers already carry display and anti-obstruction duties [E-E06]. An obstruction ban is planned [E-A17].

**What this permits, conservatively, pending counsel:**
- A **messenger** design (使者): the user decides, signs a timestamped instruction, performs any authentication themselves, and the company conveys, tracks and verifies.
- **No negotiation**, no fee contests, no refunds, no retention bargaining.
- **J6 handed to free channels**, never to paid lawyer referrals.

That design is closest to C03 and C05, and to a narrow C04 on routes where providers accept a messenger. **C06 (negotiation) and the bereavement segment carry the most legal exposure.**

### E.1 Matrix summary by constraint type

| Type | Rows | Main content |
|---|---|---|
| Law | 13 | Agency vs messenger (L01); Art. 72 conveying vs negotiating (L03, L04, L06); non-lawyer tie-ups (L05); fees (L07); reform (L08); 定期購入 (L09); telecom caps (L10); APPI (L11); bank data registration (L12); switching mechanisms (L17); bereavement (L19) |
| Provider contract | 3 | Who may act (L02); e-mail API policy (L14); credential use (L16) |
| Technical restriction | 2 | Card data scraping (L13); platform rails (L15) |
| Unknown | 4 | US limited power of attorney transfer (L18); seniors' capacity (L20); any licence regime (L21); marketing claims (L22) |

### E.2 The counsel brief (E5)

These are the questions that would move the decision, ranked by decision value:

1. **L01 + L02:** Is a cancellation conveyed by a company messenger or written-authorised agent effective without the provider's consent? Can providers lawfully insist on the holder or family? Would refusing an authorised agent count as 'refusal' under the planned obstruction ban?
2. **L03:** Where is the Art. 72 line for a paid service that conveys *undisputed* cancellations? Which behaviours cross it: answering retention offers, confirming dates, explaining fees?
3. **L11:** Can route-level outcome data from user cases be retained and reused, and in what form? This decides whether the moat (M1) can exist at all; see stop condition 9.
4. **L05:** What dispute-escalation design is permissible?
5. **L18 / L21 / L22:** Standing authorisation in app terms; any licence regime; permissible claims.

A tightly specified flow for counsel to review is designed in S8. It covers instruction capture, messenger script, authentication by the user, a stop-on-disagreement rule, verification, and referral to 188.

### E.3 Effect on the stop conditions

- **Stop condition 2** (third-party execution blocked across relevant providers): **UNRESOLVED.** One explicit block applies to *company* agents (docomo, family-only, unverified). No sampled provider evidences acceptance of a company agent.
- **Stop condition 9** (outcome data cannot be retained or generalised): **UNRESOLVED** (L11). It is answerable by counsel at low cost.
- **The bereavement segment (P4) and bill negotiation (C06) are dropped from first-test scope** on legal-exposure grounds. That is a scoping decision, not a legal finding.

## §F. Reliability and the state model (Workstream F)

### F.0 Conclusion first

A cancellation is only "done" when a charge that should have appeared does not appear on the rail that bills it, in the first cycle after the effective date. Three things make this hard:
- Some rails cannot be observed with card data (platform and carrier).
- Some contracts *should* keep charging after acceptance (term contracts, fees).
- Several look-alike end states are not cancellation: pause, skip, account deletion, and app deletion.

The state model in `model/state_model.py` makes these distinctions mechanical. It passes 13 structural invariants, and two deliberately injected shortcuts (acceptance → stopped; effective → stopped without a billing cycle) were caught. **That proves the design is internally consistent, not that any route is executable.**

### F.1 States

| Stage of the journey | States |
|---|---|
| Detection | `DETECTED_CHARGE` → `POSSIBLE_SUBSCRIPTION` → `CONFIRMED_SUBSCRIPTION` (provider + rail + account) |
| Instruction | `CANCEL_REQUESTED_BY_USER` → `ROUTE_SELECTED` → `AUTHORIZATION_COLLECTED` or `USER_ACTION_REQUIRED` → `USER_AUTH_REQUIRED` |
| Provider | `PROVIDER_CONTACTED` → `CANCELLATION_ACCEPTED` / `PROVIDER_REJECTED` / `RETENTION_OFFER_ACCEPTED` / `PAUSED_OR_SKIPPED` |
| Contract | `CANCELLATION_SCHEDULED` → `CANCELLATION_EFFECTIVE`, or `CHARGES_CONTINUE_BY_CONTRACT` first |
| Verification | `VERIFICATION_PENDING` → `CHARGE_STOPPED` (the only success) / `CHARGE_PERSISTED` / `CANCELLED_UNVERIFIED` |
| Exits | `DISPUTE_REQUIRED` (J6 hand-off), `FAILED`, `ACCOUNT_DELETED_WITHOUT_CANCEL` |

### F.2 Invariants (machine-checked)

- `CHARGE_STOPPED` cannot be reached without passing through each of:
  - `CANCELLATION_ACCEPTED`
  - `CANCELLATION_EFFECTIVE`
  - `VERIFICATION_PENDING` (at least one billing cycle observed)
- There is no edge from request, contact or acceptance straight to "stopped".
- Pause, skip and account deletion are never success.
- Contractually continuing charges are a different state from persisted charges.
- Disputes are a terminal hand-off. J6 is excluded from scope pending S5.

### F.3 Verification signal by rail

This determines how often J5 can actually be proved.

| Rail | Signal for `CHARGE_STOPPED` | Observable by a card-linked service? |
|---|---|---|
| Card on file with the provider | The expected line is absent next cycle | Yes, if the descriptor matches the brand (accuracy UNKNOWN; E2) |
| Bank debit (gyms, utilities) | The expected debit is absent | Yes, with bank data (needs a registered aggregator; S5) |
| App Store / Google Play | Subscription list status or receipts | **No** (APPLE.COM/BILL is aggregate [E-B01]); needs receipts or a screenshot |
| Carrier billing | Carrier continuous-charge list or phone-bill line item | **No** (only the phone-bill total) [E-B06] |
| Term contracts | No charge **after the term end date** | Yes, but only with contract knowledge [E-C05, E-C08] |

**Implication.** "Verified stop" is cheap to prove only on card and bank rails with clean descriptors. For platform and carrier rails, the honest end state is often `CANCELLED_UNVERIFIED` unless the user shares receipts or screens.

### F.4 Edge cases

All 15 work-order edge cases are mapped in `EDGE_CASES` in `model/state_model.py`. They include annual contracts, bundles, family accounts, unknown billing sources, Apple billing for third parties, trials, windows, early-termination fees, pause versus cancel, retention offers, a charge after confirmation, an account the provider cannot find, multiple accounts, descriptor mismatches, and app or account deletion.

**Two design rules came out of the mapping:**
- Fees and term consequences must be shown to the user before the provider is contacted.
- An agent must never accept a retention offer on the user's behalf.

## §G. Competition (Workstream G)

### G.0 Conclusion first

**No Japanese company was found that cancels consumer subscriptions on the user's behalf [E-G12]. Every adjacent step, however, is held by someone with more distribution:**
- **J1 (discovery):** PFMs and the rail owners' own lists.
- **J3 (routing):** free guide sites and search at the moment of intent.
- **J6 (disputes):** the free public consumer centres.

**The direction abroad is to embed cancellation in the payer's app.** Visa (2026) and Mastercard (2023–25) productise this for issuers, with an explicit motive: fewer disputes and chargebacks [E-G25, E-G26]. In Japan, the most natural issuer-side buyer, MUFG, already owns Moneytree [E-G07].

**The US precedents show both the size and the trap:**
- Rocket Money made $390M revenue in 2025 [E-G13].
- Its cancellations per app user are about 0.25 cumulative [E-G17], so revenue rests on premium subscriptions and negotiation, not on cancellations alone.
- Trim's consumer service ended inside a lender [E-G22].

**The only unoccupied position is execution on hard routes:** phone, written, in-person and non-cooperative providers. That is also where legal exposure (S5) and labour cost (S6) concentrate. Stop condition 7 is **not triggered for J4 on hard routes**, but **is effectively triggered for C01 and C02** (tracker and guide).

### G.1 How we lose, by mechanism

Full rows are in `03_COMPETITOR_MATRIX.csv` (CM01–CM19).

| Mechanism | Who | What it erases | What it does not erase |
|---|---|---|---|
| Distribution plus data incumbents add a "cancel" link or guide | Money Forward (17.3M), Moneytree (6.5M, MUFG), Zaim [CM01–03] | C01 and C02 entirely; most of C03 | Phone, written and in-person execution; verified stop with escalation |
| Rail owners already solve their own rail | Apple, Google, Amazon, carriers [CM04–07] | All four jobs on platform- and carrier-billed subscriptions | Nothing on direct, membership and 定期購入 rails |
| Free guides own the intent moment | 解約.com and SEO how-to sites [CM13] | C02 revenue; cheap acquisition at intent (H1) | Execution |
| A free public channel handles the worst cases | 消費生活センター / 188 [CM14] | Paid J6; part of J4 against obstructive providers | Fast, convenient execution for cooperative-but-tedious providers |
| Payer-side embedding | Visa/Pinwheel, Mastercard [CM09]; Japanese issuers [CM08] | C07 as a startup business, if networks bring tooling to Japan | Hard routes outside network merchant integrations (inference) |
| Horizontal agents commoditise web navigation | ChatGPT agent mode [CM19] | C03 for web flows in the user's own session | Phone, written and in-person routes; accountability for the outcome |
| A foreign entrant with a playbook | Whatssub (Korea) [CM17] | First-mover content advantage | Japanese legal and operational learning (if any accrues) |

### G.2 Cheapest credible incumbent responses if a startup gains traction

The responses listed in the work order:
- **Money Forward adds cancellation:**
  - The cheap version is guides and links beside サブスクレポート, at low cost within weeks to months (inference).
  - The expensive version, human execution, is the startup's only protected ground, and Money Forward could buy it rather than build it.
- **Moneytree adds "Cancel":** the same, delivered through MUFG's bank app. Slower (bank cycles) but with stronger trust (inference).
- **Apple and Google expand coverage:** not needed inside their rails. Expansion beyond their own billing is implausible and unnecessary for them. The Mobile Software Competition Act may instead *shrink* their rails by allowing outside payment [E-G30].
- **Banks and cards add recurring-payment controls:** network products already exist abroad [E-G25, E-G26]. Japan timing is UNKNOWN.
- **Regulation forces simple cancellation:** the CAA proposal targets obstruction from about 2027 [E-A17]. It erodes J4 on cooperative-but-tedious providers first and leaves forgetting (J1) untouched.
- **A general AI agent navigates flows:** already available for web flows [E-G27].

**The common residue that none of these erases cheaply:**
1. Routes requiring a human on the phone, in writing or in person.
2. Verified stop on card rails, tied to an escalation path.
3. Bereavement and family-proxy cases, where the acting party is not the account holder.

These are the most operationally expensive and legally sensitive cases. S4 (route matrix) and S5 (legal) test whether they are executable at all.

### G.3 Rocket Money: what is US-specific and what could transfer

| Element | US fact | Transfer to Japan |
|---|---|---|
| Account-data aggregation | Bank and card aggregation (US banks only [E-G21]) | Only through a registered Japanese aggregator, and the two main ones are competitors (MT LINK/MUFG, Money Forward) [E-G07, E-G08]. **Weak.** |
| Authority to act | Limited power of attorney in the terms of service [E-G19] | **UNRESOLVED** (S5): civil-law agency form, provider acceptance and the Attorney Act boundary. US authority does not transfer by default. |
| Cancellation operations | A human team contacts merchants; 2–10 business days [E-G18] | The operating pattern transfers. Japanese channels (phone, written, in person) and costs are S4/S6 questions. |
| Bill negotiation | 35–60% of first-year savings [E-G20] | UNKNOWN whether Japanese telcos and ISPs negotiate retention prices with agents. No source found. Statutory early-termination limits differ (S5). |
| Pricing | Premium $3–12/month [E-G20] | Japanese comparators are ¥280–540/month for tracking [E-G02, E-G05, E-G10]. The ceiling is lower (inference). |
| Scale and economics | $390M revenue in 2025; 12.75x ARR at its 2021 acquisition; about 0.25 cancellations per app user [E-G13, E-G15, E-G17] | Shows that cancellation alone does not carry the business. The US success came with premium and negotiation revenue and a mortgage parent's distribution. |

## §H. Market sizing, bottom-up (Workstream H)

### H.0 Conclusion first

**No public base exists for the number of Japanese subscription users, cancellation events per user, or the billing-rail mix.** In the observed scenario the market is therefore **UNKNOWN**, not small and not large. The two lead figures (71.6% and 17.9%) were not found [E-A02]; the rail split was not found [E-B10].

The model sizes the market **per 1M target users** under labelled illustrations, to show its *structure*. One thing holds in both illustrations: **what a cancellation service can bill is a small slice of the savings it creates, and the savings are a small slice of subscription spend.**

| Per 1M target users per year | Tight illustration | Loose illustration | What it is |
|---|---|---|---|
| Subscription GMV | ¥24.0bn | ¥36.0bn | Monthly spend × 12 (anchored on a modal band of ≤¥2,000 [E-A14]; not a mean) |
| Potential savings from helped cancellations (steady state) | ¥0.27bn | ¥5.4bn | Requests × months avoided × price |
| Startup revenue, C04 (pay per cancellation) | ¥0.38M | ¥43.4M | Penetration × requests × net fee |
| Startup revenue, C01 (tracker subscription) | ¥30.6M | ¥312.3M | Penetration × subscription |
| Startup contribution, C04 | −¥7.6M | ¥23.8M | — |
| Switching / referred GMV | UNKNOWN | UNKNOWN | No evidence; not zero |

The ¥6,017億 SVOD market [E-B07] is a real comparator for subscription GMV, but it covers one category. It is not used to scale these rows.

**Reading.** C04's revenue per 1M users is 0.14% (tight) to 0.80% (loose) of the savings it creates. The money a consumer pays in this space attaches to the **ongoing subscription** (tracking), which incumbents already sell at ¥360–540 [E-G02, E-G05]. It does not attach to the cancellation event. **Do not read the rows as a TAM.** They are a structural illustration and carry no adoption claim.

## §I. Economics C01–C08 (Workstream I)

### I.0 Conclusion first

Every work-order variable is an input or output of `model/economics_model.py`, exported at full precision in `06_ECONOMICS_MODEL.csv` (372 rows; 23/23 tests in `12_QA_economics_tests.txt`).

In the **observed** scenario every concept is **UNKNOWN**, because frequency, delegation share, handling minutes, CAC and retention have no Japanese evidence. Under the two labelled illustrations, five results hold in both:

1. **The paradox is real in the arithmetic.**
   - Once the backlog is cleared, steady-state requests are 50–67% of the year-1 backlog.
   - The subscription price that helped cancellations alone justify is ¥22.50/month (tight) or ¥450/month (loose). The assumed prices are ¥300 and ¥540.
   - A subscription therefore **cannot be justified by cancellation savings alone**; the flag is "yes" in both. It needs another recurring value. Tracking is that value, and it is commoditised.
2. **Pay-per-cancellation (C04) does not pay back within 36 months in either illustration.**
   - Tight: the ¥500 fee is below the non-labour cost of a request, so break-even minutes are negative (infeasible).
   - Loose: the ¥1,500 fee tolerates up to 123 human minutes per hard-route request, but low frequency (0.6 requests a year) leaves ¥475 of contribution per user-year against ¥1,000 CAC.
3. **Execution is cheap as a feature and weak as a product.**
   - C05 (subscription plus verified stop) looks like C01 (tracker) plus a small execution cost: contribution of ¥2,136 vs ¥2,307 (tight) and ¥6,628 vs ¥5,984 (loose).
   - Its profitability comes from the tracker subscription, the market MF, Moneytree and Zaim already occupy.
4. **B2B2C (C07) is the only model where low frequency helps margins.** The partner pays per enrolled user whether or not anyone cancels.
   - Contribution: ¥0.98M per partner-year (tight) to ¥129.9M (loose), with partner sales and integration costs included.
   - Break-even partner fee: ¥18.37 (tight) or ¥5.86 (loose) per enrolled user-month at the assumed partner sizes.
   - **Every partner input is an assumption.** The likeliest partner (MUFG) owns Moneytree, and Visa and Mastercard sell the same capability abroad [E-G07, E-G25].
5. **Negotiation (C06) and switching (C08) are small.**
   - C06: −¥246 to ¥575 per user-year, with the legal gate L06 unresolved and telecom fees capped.
   - C08: ¥79–778, and the gaining provider pays (conflict of interest).
   - C02 (guide) revenue is UNKNOWN in every scenario (no source), not zero.

### I.1 Where each required variable lives

| Variable | Model key(s) | Status in "observed" |
|---|---|---|
| Active users; eligible subscriptions | `target_penetration` (per 1M); `subs_stock_per_user` | unknown |
| Requests per user per year | `requests_year1_per_user`, `requests_steady_per_user_year` (from stock, inflow, unwanted and help shares) | unknown |
| Automation rate | `share_route_A` | **rule 0** (no class-A route found [E-C24]) |
| User-handoff rate; human handling rate | `share_route_B`; `share_route_human` = 1 − A − B | unknown (the 14/22 sample is *not* used as a market share) |
| Human minutes | `handoff_support_min`, `human_min_per_request`, `fraud_identity_min_per_request`, all priced at one `labor_jpy_per_min` | unknown (wage observed [E-H02]; load assumed) |
| Phone cost; verification cost | `phone_cost_jpy_per_human_request`; `verification_cost_jpy_per_request` | unknown |
| Provider failure rate; repeat contacts | `provider_failure_rate`, `repeat_contacts_per_failure` → `rework_multiplier` | unknown |
| Fraud / identity support | `fraud_identity_min_per_request` | unknown |
| Infra / model cost | `infra_jpy_per_user_year`; `llm_*` (token prices observed [E-H03]; volumes assumed) | unknown |
| Revenue | `C0x_revenue_per_user_year`; C07 per partner | unknown |
| Chargebacks / refunds | `refund_rate`; C05 fee refunded on `persist_rate` | unknown |
| CAC; activation; retention | `cac_jpy`; `activation` (counted once); `monthly_churn` | unknown |
| Contribution; payback | `C0x_contribution_per_user_year`; `C0x_ltv36_per_acquired`; `C0x_payback_month` ("never" ≠ unknown) | unknown |

### I.2 Frontiers that matter more than point values

- **C04 human-minute budget per hard-route request** = (net fee − handoff, phone, model and identity costs) ÷ (labour price × human share × rework). At ¥500 the budget is negative. At ¥1,500 with light handling it is about 123 minutes. **E3 must measure minutes per hard route against this frontier.**
- **Subscription price justified by cancellations** = steady requests × savings per cancellation ÷ 12: ¥22.50 to ¥450 a month. Any consumer subscription above that must be bought for something else.
- **C07 partner fee floor** = (amortised partner fixed cost ÷ enrolled + engaged × requests × cost per request) ÷ 12: ¥5.86 to ¥18.37 per enrolled user-month. **The single partner number to discover in primary research.**

## §J. Business models (Workstream J)

Each model is evaluated independently. The spreadsheet does not choose.

| Model | Alignment with consumer | Conflicts | Transparency | Margin (model) | Frequency / churn | Sales cycle | Regulatory exposure | Incumbent response |
|---|---|---|---|---|---|---|---|---|
| Consumer subscription | Medium: pays for monitoring; success reduces need | Low | High | Positive only via the tracking value (C01/C05) | Paradox: cancellation alone justifies ¥22.50–450/month | None | Low–medium (APPI; claims) | MF ¥540, Moneytree ¥360, サブトラ ¥280 already sell it [E-G02, E-G05, E-G10] |
| Success fee / share of savings | High on paper | Counterfactual disputes (would they have cancelled anyway?) | Low: savings are self-defined (cf. Rocket Money's annualised definition [E-G16]) | Depends on unmeasured counterfactual months | Episodic | None | Medium: fee disputes edge toward J6 | Easy to copy |
| Per-cancellation fee | High (pay on outcome) | Low | High | Negative to thin (C04) | Very low frequency → CAC per transaction | None | Medium–high: closest to paid agency (L03) | Free guides and general agents at the intent moment [CM13, CM19] |
| B2B2C: card issuer, bank, wallet, employer benefit, financial-wellness provider | Medium: the partner wants fewer disputes; the user wants fewer charges | Issuers earn on subscription spend (inference); possible steering | Medium | **Positive in both illustrations, entirely on an assumed partner fee** (C07) | Low frequency helps margins | Long (banks: inference) | High (partner compliance; data) | Visa/Pinwheel, Mastercard abroad; MUFG owns Moneytree [CM09, CM02] |
| Switching / referral | Low–medium: the gaining provider pays | High (steering) | Medium | Small (C08) | Rare events | Medium | Sector rules (not researched) | Price-comparison and switching sites; gaining providers already cancel the old contract [E-C20] |
| Bill-negotiation share | High on paper | Medium | Medium | Small or negative (C06) | Rare | None | **High: legal gate L06** | Not present in Japan, but the value pool is capped [E-E08] |

**What this implies for the payer question (G1, stop condition 10).** The only payer whose economics *improve* with infrequent use is a partner paying per enrolled user. No Japanese partner price, appetite or precedent was found, and the natural partners either own a competitor (MUFG) or can buy network tooling. Consumers have proven willingness to pay ¥280–540 a month for *tracking*, which incumbents supply; there is no evidence they will pay for *cancellation*. **Stop condition 10 is UNRESOLVED and leans negative for B2C. For B2B2C it depends on one discoverable number: partner willingness to pay.**

## §K. Moat (Workstream K)

Full chain tests are in `11_MOAT_AND_RIGHT_TO_WIN.md` §2.

- **Features or service advantages, not moats:** M2 (descriptor graph), M3 (playbooks for web routes), M4 (direct integrations) and M5 (trust).
- **Conditional moat candidates:**
  - **M1, an outcome graph for hard routes only.** It requires company-messenger permission (L01/L02), lawful data reuse (L11) and a measurable learning curve (E3).
  - **M6, exclusive payer-side distribution.** It requires a Japanese partner to pay at least ¥5.86–18.37 per enrolled user-month (illustrative floor) and to choose a startup over network tooling or its own PFM.
- **Stop condition 7:** effectively triggered for C01–C03; UNRESOLVED for C04/C05 on hard routes.

## §L. Why now / why not now (Workstream L)

See `11_MOAT_AND_RIGHT_TO_WIN.md` §3. No manufactured "why now":
- **The genuinely new force cuts against C03.** General AI agents [E-G27] commoditise the easy, web-flow part.
- **The friction evidence cuts both ways.** It also drives the obstruction ban, with a bill as early as 2027 [E-A17].
- **Incumbents hold detection and distribution** [E-G01, E-G07, E-G25].

**A window exists only for hard routes, only until about 2027–28, and only if permission holds.**

## §M. Founder fit (Workstream M)

See `11_MOAT_AND_RIGHT_TO_WIN.md` §4.

- **Strengths:** bilingual research, analytics and FP&A. These fit the discovery and modelling work this assignment allows.
- **Missing:** the capabilities that decide R-007:
  - Japanese consumer-law and Attorney Act expertise.
  - Bank or issuer partnerships.
  - Contact-centre operations.
  - Security and consumer fintech.
- **Constraint:** current-student bandwidth is a factual limit for an operations-heavy concierge.
- **Ideal cofounder:** Japanese payments or bank partnership experience first, consumer operations second, with counsel as a standing adviser.

## §N. Primary research and experiment design (work order §23–24)

**Designed, not executed.** Nothing here was run. Rows that need outreach, spending, live accounts or counsel are marked in `09_EXPERIMENT_BACKLOG.csv` and need separate authorisation.

### N.0 Conclusion first

The smallest high-information sequence:
1. **E5, a counsel memo**, is a binary gate on stop conditions 2 and 9.
2. **PR1, activity-selected reconstruction**, measures rail mix and hard-route frequency, which no public source provides. It runs in parallel with E5.
3. **Only if both are green:** E6 (partner WTP), then E1 (route-coverage extension), then **E3 and E4** (manual concierge with verification).

**E2 (descriptor normalisation) is last.** Incumbents already own that capability (M2).

### N.1 PR1: activity-selected reconstruction

- **Who:** 15–20 adults who cancelled or tried to cancel at least one subscription or 定期購入 in the past 12 months. Quotas for ages 50+ (the P1 skew [E-A05]) and for parents of school-age children (the learning-route skew [E-C16]).
- **Consent boundary:**
  - Participants look at their own statements and subscription lists **on their own screen**. The researcher records only the provider category, rail, route and outcome.
  - No credentials, files, account numbers or the founder's own data.
  - APPI purpose is stated up front, and participants may stop at any time (L11).
- **Prompts (spoken Japanese; prior behaviour only, never "would you use…").** Ask:
  - 「この1年で、やめようとした定額サービスや定期購入を、思い出せるものから3つ教えてください。」
  - 「それぞれ、どこから払っていましたか？カード、携帯料金、App Store、口座振替など、画面で見ながらで大丈夫です。」
  - 「やめようと思ったとき、最初に何をしましたか？そのあとは？」
  - 「電話や来店、書類は必要でしたか？だいたい何分くらいかかりましたか？」
  - 「本当に止まったかは、どうやって確かめましたか？」
  - 「途中で誰かに頼みましたか？家族、サポート窓口、消費生活センターなど。」
  - 「やめられずに、払い続けたものはありますか？そのとき一番面倒だったのは何ですか？」
  - 「これまでに、手続きを人に任せるためにお金を払ったことはありますか？」
- **Record per charge:**
  - Rail and provider category.
  - Route class (A–E, by reconstruction).
  - Steps and recalled minutes.
  - Outcome (stopped, persisted, gave up) and verification method.
  - Who acted, and any paid help.
- **Decision rules:** set in `09_EXPERIMENT_BACKLOG.csv` (proceed at ≥30% with a hard-route case and at least half of those delegating or giving up; kill below 10%).

**PR2 (incident-selected) and PR3 (experts)** are included only where they resolve a WNTB. PR3 tests provider-acceptance practice (E1/D2); PR2 is folded into PR1's quota rather than run separately.

### N.2 E3: manual concierge, after E5 is green

- **Setup:** the founder conveys hard-route cancellations on per-case signed instructions from consenting PR1 participants. **It is not presented as automated.**
- **Measures:** minutes against the C04 frontier (§I.2); verified stop on the next statement (E4); the learning curve (M1).
- **Kill rule:**
  - median minutes above the frontier, **or**
  - verified stop below 60%, **or**
  - majority provider refusal.

### N.3 The flow to put in front of counsel (E5)

1. The user confirms provider, rail and account (`CONFIRMED_SUBSCRIPTION`).
2. The service shows the route, fees, term consequences and expected effective date before acting (informed consent; L07).
3. The user signs a per-case instruction: cancel only; no negotiation; do not accept offers. The method of identity verification is for counsel to specify.
4. The service conveys the instruction through the provider's designated channel, identifying itself as the user's messenger. **Any authentication is done by the user directly** (three-way call or user callback).
5. Any retention offer, dispute or term disagreement means **stop and return to the user** (L03).
6. The acceptance artefact is stored, verification is scheduled after the first billing cycle, and the stop is checked on the user's statement (F.3).
7. If a charge persists, the user is pointed to free channels (188). **No paid referrals** (L05).
8. Data: a route-level outcome record is kept; personal data is deleted under a stated retention policy (L11).

### N.4 Watch triggers (if parked)

- **CAA reform:** the bill text and whether it covers refusal of agents or phone-only routes [E-A17, E-E13].
- **Incumbent moves:**
  - Money Forward or Moneytree adding cancel actions [CM01, CM02].
  - Visa or Mastercard subscription tooling announced for Japanese issuers [CM09].
- **Provider proxy policies:** for example, docomo's family-only rule [E-C10].
- **The モームリ case outcome** [E-E03].
- **Uptake of outside payments** under the Mobile Software Competition Act [E-G30].

## What would make this a great company?

All of these would need to be true at once:
1. **Permission:** counsel confirms that a paid company conveying an undisputed cancellation as the user's messenger is outside Art. 72, **and** that providers cannot refuse a duly instructed messenger. That could come from current law or from the 2027 reform turning "refusal" into a prohibited obstruction (L01–L03, L08).
2. **A definable segment with recurring hard-route cancellations:** at least 30% hit one each year, and at least half of those delegate or give up (PR1). Families managing seniors' subscriptions and parents of children on learning subscriptions are the candidates.
3. **Learning curve:** median handling minutes on hard routes stay below the fee frontier and fall with volume (E3, M1). The outcome graph is lawful to reuse (L11).
4. **A payer at or above the floor:** a partner paying at least about ¥6–18 per enrolled user-month (C07), or consumers paying a per-case fee above cost on hard routes.
5. **Speed:** all of this before compliant providers simplify cancellation under reform (about 2027–28), or the reform makes the company the trusted messenger channel.
6. **Alignment:** verification and free referral (188) instead of switching commissions, negotiation fees or paid lawyer referrals.

## What would make this a bad company?

These are specific failure mechanisms, not generic risk:
- **Unpayable minutes:** paying people to wait on phone lines for a ¥500 fee, where the minute budget is negative before any call starts (§I.2).
- **The paradox:** a subscription users cancel after their one or two backlog cancellations are done. Cancellations alone justify ¥22.50–450 a month.
- **A copyable guide:** shipping a guide or AI navigator that Money Forward, a guide site or a general agent copies within weeks.
- **Drift into disputes:** becoming a de facto dispute shop and taking on Art. 72 or non-lawyer tie-up exposure, as in the 2025–26 resignation-agency enforcement.
- **Competitor-owned pipes:** depending on MT LINK (MUFG-owned) or card-site scraping, so that the supplier is a competitor and a credential incident is existential.
- **Conflicted revenue:** earning from switching commissions that steer users.
- **Reform removes the market:** compliant providers simplify cancellation, leaving only obstructive providers, where an agent fails as often as the consumer does.

## What are we most likely to be wrong about?

1. **Hard-route frequency may be much higher in specific households** (seniors' subscriptions managed by children; learning services) than the illustrations assume. PR1 tests this.
2. **Provider practice may be more permissive than the one rule found.** docomo's family-only proxy rule comes from a combined extract and may be narrower than stated.
3. **Counsel may find undisputed conveyance plainly outside Art. 72.** C04 would then be easier than this packet treats it.
4. **Issuers may have real budgets.** Visa's stated motive, fewer disputes and chargebacks [E-G25], may translate into Japanese issuer demand (E6).
5. **The rail mix may differ.** The self-serve and platform share of a target segment could be lower than the sample suggests, and outside payments under the Mobile Software Competition Act could fragment rails further [E-G30].
6. **Reform could help rather than hurt,** if it obliges providers to accept agents.
7. **Every claim rests on search extracts; no page was opened.** Some figures may be misreported, as the GEM unit error showed.

## What does public research still not establish?

- **The CAA lead figures:** the 71.6% and 17.9% figures, the white paper's base, n, dates, wording and full option list.
- **The billing-rail mix** of Japanese subscriptions.
- **Demand on hard routes:** frequency per user, delegation willingness, and willingness to pay for execution.
- **Execution evidence:**
  - Minutes per hard route.
  - Provider acceptance of company messengers on any phone, written or in-person route.
  - Routes for cosmetics and supplement 定期購入 sellers.
- **Legal questions:**
  - Whether Art. 72 applies to undisputed cancellation conveyance.
  - Whether outcome data may be reused.
  - Whether a licence regime applies.
- **Partner willingness to pay** in Japan.
- **Competitor gaps:**
  - Moneytree's manual-entry support and platform coverage.
  - Paid-user counts for Japanese incumbents.
  - Whether Whatssub's "one-touch" cancellation is executed by Whatssub.
  - ChatGPT agent mode's availability in Japan.

## Which single experiment changes the decision most?

**E5: a counsel memo on the tightly specified messenger flow (§N.3).** It is a binary gate:
- A negative answer **STOPS** every on-behalf variant regardless of demand.
- A positive answer is the precondition for spending on PR1 and E3.

It is the cheapest decisive step (one written opinion). It needs separate authorisation, because counsel fees are expenditure.

## What should remain open?

Kept separate, not merged into one pivot:
- **C07, B2B2C cancellation and verification infrastructure:** open only through E6's partner-fee question.
- **P3, family-assisted management of seniors' subscriptions:** open through PR1 and counsel question L20.
- **P4, bereavement:** open only as *identification without cancellation* (L19); not a first-test segment.
- **C08, switching:** open only through gaining providers, never as a neutral cancellation brand.
- **J5 verification as a feature that PFMs might license:** open, but its natural buyers are the incumbents that could build it.
- **The watch triggers in §N.4.**
- **Other research lines:** R-003 stays NO_BUILD / NO_PROTOTYPE. R-005 stays PARKED_BY_OWNER. Neither is reopened by this work.
