# Consolidation decision memo (CLA)

**Reference cutoff:** 2026-10-04.

**Executed:** 2026-10-04 21:45–22:10 UTC, which is 2026-10-05 06:45–07:10 JST. This is the same instant as the October 4 cutoff, not a later observation.

**Inputs available to CLA:**
- CLA's own original packet, recovered intact (16 files, hashes match commit `ebd8cdf`)
- Grok v2: `02_new_claims`, `03_competitor_delta`, `04_economics_model` and `05_hypothesis_register` CSVs
- the assignment prompt

**Not supplied to CLA:**
- Grok v1 files, `calculate_r003_v2.py` and the R003 v2 addendum
- Grok's `06`/`07` v2 files
- the reviewer's audit JSON
- the Gemini table

**Direct page reading** remained blocked (HTTP 403 on 6 more hosts tested in this pass). Verification was limited to 6 targeted search extracts.

## Decision

**No consumer job is yet established as worth a prototype.** The next allocation is one bounded **job-comparison discovery round**:
- about 12 activity-selected multi-merchant shoppers, plus up to 8 separately labelled incident-selected participants;
- about 35–45 founder hours;
- no build, no inbox OAuth, no credentials, no purchases.

The round compares four jobs against the strongest tools participants already use: offer selection (J1), checkout (J2), delivery coordination (J3) and exceptions (J4). After it, choose **at most one** follow-on. The kit is in `05_discovery_kit/`.

**A prototype is justified only when all four conditions hold for the same job:**
1. Several activity-selected participants show a material residual burden after their strongest current tool.
2. One connected, permitted operating path exists for that job's data, interface and any monetisation.
3. Provider cost per unit has been observed, including the loss tail, and a payer is evidenced.
4. An acquisition route is identified rather than assumed.

**If no job clears the discovery screen, park the theme.** That is an opportunity-cost decision, not proof that no consumer company can exist. B2B logistics interoperability, SKU data infrastructure and physical-AI support remain unresearched and unscored. B2B2C is not a default rescue.

## Retained constraints

- **Delegated Amazon execution is excluded from the investment case.** The English Program Policies returned at the co.jp URL prohibit Associates from ordering on behalf of others (6(k), observed by Grok and the reviewer). The Japanese operating agreement is unread, so this is an underwriting exclusion, not a measured universal prohibition (ADJ-01).
- **Referral revenue on a personal-assistant surface is not bookable today.** Rakuten's guideline restricts affiliate links in email, LINE, DMs and other closed tools, except for Rakuten-approved corporate partners, and bans automated distribution to those channels (search extract, ADJ-03). Amazon, Yahoo and ASP terms for this surface are unread. Booked C03 revenue is therefore a rule zero under current gates; the commercial opportunity is unknown. Merchant-hosted checkout does not make the referral eligible.
- **No connected permitted execution path is established** for the intended cross-merchant task among the researched surfaces (ADJ-06). Visa's Agentic Ready programme names five Japanese issuers: SB Payment Service, Credit Saison, Sumitomo Mitsui Card, MUFG NICOS and Rakuten Card. It is issuer readiness, not merchant coverage, startup eligibility or scaled volume (ADJ-09). This replaces my earlier "any two announcements" re-open gate.
- **Tracking is not an empty market.** Carrier LINE flows, Parcel (a Japan App Store listing with Japanese carriers named, per Grok), Gmail's Purchases view and in-mall agents all exist (ADJ-18–21). Whether they *adequately* solve a given segment's job is unresolved (H02b).
- **Passive tracking produces no referral event**, a programme-rule zero (G10).
- **A ¥32–40/MAU partner fee cannot fund human case resolution.** The reviewer's ¥300 per household-month reproduces exactly. After an illustrative ¥31.6 tracking core, a ¥40 fee affords submission × human share × minutes of only 0.42, for example 2.8% submission at 15 fully human minutes (ADJ-33). Drafting help and human resolution are different products (C04a, C04b).

## Rejected inferences (mine first)

- **CLA v1: "falsified" consumer delegation.** I set "majority refusal" as the falsifier and then cited 27%, which is not a majority. Correct reading: in an AI-friendly sample (n=4,120, June 2026), about 5% would let AI add items to the cart with self-confirmation, 1% would allow unchecked purchase, and 27% would allow nothing. **H03b is UNRESOLVED with an adverse signal for execution**, not contradicted (ADJ-16). Non-refusers are not adopters.
- **CLA v1: "no permitted path anywhere in Japan."** Standalone merchants and wallets were never researched (ADJ-06).
- **CLA v1: C04-first recommendation with a B2B2C payer.** Withdrawn (ADJ-33).
- **CLA v1: "base case negative" and "not venture-scale."**
  - The contributions came from assumed inputs.
  - The sizing multiplied a two-or-more-person-household usage rate (56.9%) by all households.
  - It used net-shopping spend that includes services (travel is 20.9% of it).

  These figures are withdrawn from decision use (ADJ-26, ADJ-32).
- **CLA v1: Amazon's July 2026 email change meaning lost Amazon data.** The evidence is account-level US reports on *initial confirmation* emails. Nothing shows changes to shipment or refund messages, tracking numbers, or a Japanese rollout (ADJ-24).
- **Gemini:**
  - "3DS blocks headless scraping" is rejected. 3DS is payment authentication, a separate step from data access, merchant permission and merchant acceptance (ADJ-08).
  - "~$540 CASA means inbox parsing is viable" is rejected. A quote is not a compliance budget (ADJ-13).
  - "Fast's collapse proves consumers won't pay" is rejected (ADJ-27).
  - Gemini's universal verdict gets no evidentiary vote (ADJ-38).
  - The A8 role correction is accepted (ADJ-15).
- **Grok v2:**
  - Grok's H02 status rested on the empty-market claim; it is now split into H02a/H02b (ADJ-36).
  - Its tests required a changed choice or outcome. Same result with materially less effort now counts, measured with full provider cost and the loss tail (ADJ-37).
  - Treating OpenAI's checkout change as making chat interfaces impossible is rejected. Deprioritising generic in-chat checkout is a *decision* (ADJ-11).

## Model repairs and QA (`04_qa/QA_RECEIPT.md`)

- **Grok v2 precision defect: reproduced.** The supplied CSV stores 0.01 attributable orders; the exact figure is 0.012, and 0.01 × ¥80 = ¥0.80 ≠ ¥0.96. The in-memory −¥29.04 is correct. Repaired in `GRO-D01`.
- **Grok v2 cohort double count: reproduced** from the row definitions and repaired.
- **The same defect class is in my own export.** The workbook still matches Python on 141/141 formula cells, but that only shows implementation consistency. My saved CSV rounded 81 of 288 cells, and 31 of 138 outputs do not reconcile from saved values; no signs flip.
- **One bridge replaces averaging.** It has distinct configurations (C01, C02 gated, C03, C04a, C04b, C07, plus explicit C01+C03). It keeps full-precision values separate from display values and applies activation once.
  - In the **observed** scenario, every behaviour-dependent contribution is blank, not zero.
  - The illustrative scenarios are conditional frontiers only. For example, C03 "if approved" ranges from −¥21 to +¥181 per household-month, and tracking needs 10.7% of households paying ¥480 under scenario A.
  - The bridge tests pass 17/17. The first run passed 16/17 because of a mis-specified test, which was rewritten.

## Company economics, stated conditionally

I no longer assert a universal "venture-scale" cutoff. The arithmetic is conditional. Covering a minimal team at an assumed ¥3M per month needs contribution × active households ≥ ¥3M:
- about 150,000 actives at ¥20 per household-month;
- about 17,000 actives at ¥180.

Whether either is attractive depends on the founder's goal: a venture-backed platform or a small service. No input to these figures has been observed.

## Independence of the evidence

- Agreement after shared reviewer feedback is not independent corroboration.
- Grok and the reviewer read **one page** for Amazon 6(k).
- CLA and Grok cite **one MGI source family**. It supports only that e-commerce is the largest projected arena by 2040 revenue; it is not the fastest-growing and says nothing about consumer versus B2B (ADJ-25).
- The Rakuten restriction rests on the reviewer's reading and one CLA search extract.

## Unresolved dependencies (`06_verification_queue.csv`)

- **VQ-01 / VQ-02:** the Japanese Amazon agreement and the full Rakuten guideline. These decide referral monetisation.
- **VQ-10:** which fields the founder's own amazon.co.jp messages carry, by message type. A one-hour local check.
- **Job-level residual burden, payer and provider minutes.** Only the discovery round and one follow-on can supply these.
- **The Visa chart base and wording (VQ-06).** These affect wording, not the allocation.
- **The missing Grok and Gemini artifacts (VQ-17 / VQ-18).**

## Confidence

- **High** that no build is justified now, and that delegated execution and assistant-surface referral revenue are not bookable on current evidence.
- **Moderate** that delivery visibility faces strong free substitutes.
- **Low** on which job, if any, carries material residual burden. That is exactly what the discovery round measures.
