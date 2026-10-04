# Decision Memo: Japan-first Agentic Commerce (CLA)

**Reference date:** 2026-10-04. Research cutoff: 2026-10-04 ~20:50 UTC.
**Evidence base:** About 130 web searches (Japanese and English). **No page could be opened** (network policy blocked fetches), so every fact rests on search-result summaries, cited by ID in the companion files. No interviews, product tests or account access.

## Recommendation: NARROW and PIVOT; do not build the agent as framed

Do **not** build a merchant-neutral consumer purchasing agent, and do **not** build a standalone order and delivery tracking app.

If the founder gives this theme one more cycle, test a single narrowed wedge cheaply (about 3 weeks; roughly ¥30–60k for incentives, plus about ¥30–100k if counsel review is commissioned):
- **Concept:** C04, a post-purchase exception service. It catches return windows, missing refunds, partial cancellations and missing parcels across merchants, then drafts the message the user sends. It never acts in anyone's account.
- **Segment:** heavy multi-merchant households (at least 3 merchants and 4 parcels a month).
- **Product boundary:** read-only data from emails the user forwards, plus handoff to merchant and carrier channels. No checkout, no delivery changes, no stored credentials.
- **Business model to test:** first, whether a **partner** (card issuer, merchant group, carrier) would pay to reduce support load; second, a consumer subscription. Not affiliate.

Move checkout (C02) to **WATCH**, with explicit re-open triggers.

## Why: strongest evidence against the original story

1. **No permitted path to execute purchases in Japan.** The top marketplaces expose only product-search APIs; their order APIs are seller-only (CLA-C007–C009). Amazon actively fights third-party agents:
   - a US injunction against Perplexity (later vacated on CFAA grounds, but contract claims remain);
   - blocking Meta's Muse on 2026-09-20;
   - a seller-side Agent Policy;
   - stripping item names from order emails from 2026-07-08 (documented for the US; **unverified for amazon.co.jp**) (CLA-C001–C005).

   Agent checkout protocols (UCP, ACP, Shopify agentic checkout) are US-first, and none was found live in Japan (CLA-C026–C029). Japan's card-security guidelines also require EMV 3-D Secure at online merchants in principle (CLA-C023). The only Japanese agent-payment evidence is a single Mastercard pilot transaction (CLA-C024).
2. **Free substitutes already cover delivery visibility.**
   - Yamato, Sagawa and Japan Post push LINE notifications (Yamato's are phone-number matched, with no sign-up needed) and own the right to change deliveries (CLA-C019–C021).
   - Yahoo! Shopping's agent covers discovery through post-purchase delivery and re-purchase for its own orders (CLA-C040).
   - Rakuten AI, Rufus and Gmail cover in-platform discovery and purchase-email grouping (CLA-C042, C044, C046).
   - Redelivery fell to about 7.6% in April 2026, and policy is standardising 置き配 (unattended doorstep delivery) (CLA-C073, C074).
3. **Consumers resist delegation.** In Visa's June 2026 Japan survey of AI-using respondents, 27% would not entrust any part of purchasing to AI even if accuracy concerns were resolved (CLA-C078). Japan ranked lowest of seven countries in awareness of agentic shopping assistants (CLA-C079).
4. **Unit economics fail in the base case.** All figures below are per active user per month, from the reconciled model in `04_economics_model.csv`.
   - Tracking-only loses about ¥44. Affiliate handoff loses about ¥31. A ¥480 freemium subscription loses about ¥31.
   - Affiliate needs at least **36%** of eligible orders to start in the agent just to break even. Recovering a ¥450 install cost would need more than 100%, which is impossible.
   - Subscription needs about **17%** of active users paying.
   - **Inference is cheap** (about ¥1 per email). **Human minutes, acquisition and access are the binding costs.**
5. **No moat; poor base rate.** Google's data rules bar ad or sale use of Gmail-derived data (CLA-C012). Google and Apple can localise free tracking at will (CLA-C046, C047). Rakuten Rebates (10M registered users, 1,000+ stores) already owns cross-merchant savings (CLA-C052). Precedents were absorbed or ended: Uketoru (Japanese account-linked tracker), Two Tap (universal checkout), Spring (universal cart) and OpenAI's in-chat checkout (CLA-C054–C056, C027).
6. **Scale is limited even in the upside.** Under generous assumptions, Japan-only consumer affiliate revenue is about **¥1.6B a year** (base: about ¥24M) (CLA-C099). That is not venture scale.

## Strongest evidence for (why not simply stop)

- Read-only email ingestion is **permitted**. "Package delivery tracking" is an explicitly allowed Gmail app type, and Google's annual security audit (required when data is stored server-side) lists at roughly USD 540–720 (CLA-C010, C011, C013). Forwarding avoids the restricted-scope review entirely.
- Incumbents are **single-merchant by design**. Exceptions across merchants (returns, refunds, cancellations) appear under-served. This is unverified, which is exactly why it is worth testing.
- Japanese merchants already pay for post-purchase software: Recustomer serves 200+ brands (CLA-C059). A partner-paid version breaks even on variable cost at about **¥32 per MAU per month** (base model).
- The founder's logistics-operations exposure fits the concierge test and merchant/3PL conversations.

## What changed from the initial story

| Initial story | Corrected |
|---|---|
| "Neutral agent that executes purchases" | Assistance plus handoff; execution is not permitted today |
| "Unified view of orders is missing" | Delivery visibility is well served; cross-merchant *exceptions* may not be |
| "Tracking leads to checkout" | No evidence; tracked orders cannot earn affiliate commission |
| "Japan's complexity is a moat" | Incumbents own each complex surface (points, carriers, LINE) |
| "McKinsey: biggest and fastest-growing" | MGI (Oct 2024) projects e-commerce as the *largest* arena by 2040 revenue but *not* the fastest-growing, and says nothing about consumer versus B2B |

## Decisive unknowns (only primary work resolves them)

1. Do amazon.co.jp confirmation emails still carry item names and tracking numbers? (CLA-E001, one hour)
2. How often do heavy multi-merchant households hit material, unresolved post-purchase exceptions, and will they keep forwarding? (CLA-E002)
3. Will any partner state a fee of at least ¥32/MAU, or an equivalent per-order fee? (CLA-E003)
4. Does a forwarding service for external users trigger telecom-business notification, and does sending inbox content to overseas AI services need extra consent under Japan's privacy law (APPI Art. 28)? (CLA-E009, counsel)

## Next decision and rule

Run **CLA-E001**, then **CLA-E002**: a 14-day consented diary with forwarding and a disclosed human concierge, with 20–30 heavy buyers deliberately including low-pain and non-AI-enthusiast profiles. Run **CLA-E003** in parallel.

- **Proceed** to a C04 prototype only if all three hold:
  - at least 40% report at least one material unresolved exception a month;
  - at least 50% keep forwarding to day 14;
  - at least 20% accept a real paid offer.
- **Stop the consumer path** if fewer than 20% have exceptions or fewer than 30% keep forwarding.
- **If the consumer test fails but E003 produces at least two written pilot interests**, pivot to B2B2C or B2B.
- **If both fail**, close the theme and compare it against the unresearched adjacent themes (B2B logistics interoperability, SKU data infrastructure, physical-AI support).

**Re-open checkout (C02)** only when two of these fire:
- UCP, ACP or Shopify agentic checkout reaches Japanese merchants;
- Japanese issuers make network agent tokens generally available;
- Amazon publishes a licensed agent path;
- Alexa for Shopping launches in Japan.

## Confidence

- **Moderately high** that universal execution is infeasible in Japan under current access rules. Several independent signals agree, though all came from search summaries.
- **Moderate** that standalone tracking is not a business.
- **Low** on demand for the narrowed exception wedge and on any partner fee. No primary data exists.

Re-verify all numbers on source pages before external use.
