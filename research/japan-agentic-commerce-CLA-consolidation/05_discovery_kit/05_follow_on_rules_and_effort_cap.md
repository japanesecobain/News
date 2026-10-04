# Follow-on rules and effort cap

## Effort cap (a budget, not a statistical design)

| Item | Cap | Note |
|---|---|---|
| Activity-selected interviews (`ACT`) | ~12 | Japanese multi-merchant shoppers who bought online recently from at least 2 independent platforms; record seller-level too. Include people satisfied with current tools. Do not recruit for interest in AI. |
| Incident-selected extension (`INC`) | up to 8 | People with a recent post-purchase problem. Only if deeper mechanism detail is useful. Reported separately. |
| Founder time | about 35–45 hours total | Recruitment about 8h; interviews about 1h each; coding about 0.5h each; synthesis about 6h |
| Cash | Incentives about ¥2,000–3,000 per person (assumption) | No paid ads; no tools that require participant credentials |

These caps are not power calculations or population thresholds. Stop early once the allocation decision is clear. Filling all 20 slots is not required.

## How to read the round (rationale, not invented cut-offs)

For each job J1–J4, summarise **from the ACT group only**:

- how many participants show at least one `MATERIAL` residual burden after their own strongest tool;
- what that burden consists of: minutes, contacts, cash tied up, or uncertainty;
- which existing tool already handles it for the others.

Use the INC group only to understand mechanism and cost structure for J4. Report counts, such as "5 of 12", not percentages for the market.

**Select a job for a follow-on only if all three hold:**

1. More than one ACT participant shows a `MATERIAL` residual burden for that job that their current tools did not remove.
2. A plausible **permitted** operating path exists for that job's data and interface (see `../03_derivatives/CLA-D03_permission_gates.csv`). Execution and referral revenue on a personal-assistant surface are not currently established.
3. The burden is not already solved, in the participants' own accounts, by a free substitute they could adopt with little setup: carrier LINE, Parcel, Gmail, or in-mall agents.

**If no job meets all three, park the theme.** That is an opportunity-cost decision to move effort to other themes. It is not proof that no consumer company can exist.

If more than one job qualifies, choose the one with the clearest net effort reduction per participant and the least permission dependency. **Choose at most one.**

## The four possible follow-ons (pick at most one)

| Job | Follow-on | What it measures | Value counts if… | Must also measure |
|---|---|---|---|---|
| J3 Delivery coordination | **Substitute benchmark.** Participants' own recent orders compared across current workflow vs Parcel vs Gmail vs carrier LINE. Participants use only tools they choose; the researcher never handles credentials. | Missed or late information, time to answer "where is it / when", setup and privacy friction | A workflow gives the same or better answer with materially less effort after setup | Coverage by merchant and carrier; whether amazon.co.jp messages carry item and tracking fields (`VQ-10`) |
| J1 Offer selection | **No-purchase comparison task.** For a real upcoming need, the participant shops as usual; separately, the researcher prepares a comparison from public information with no affiliate links. Nobody buys anything through the researcher. | Time, uncertainty and errors (wrong variant, delivered-price surprises) for the participant's own process vs the prepared comparison | The **same** correct choice reached with materially less effort or uncertainty also counts. A changed choice is not required. | Researcher minutes per comparison, including dead ends; monetisation stays "unresolved" (Rakuten closed-tool restriction; other programmes unread) |
| J2 Checkout | **Permitted-path memo** (desk only). For merchants named by participants: data access → merchant/platform permission → preparation → user approval → payment authentication → merchant acceptance. | Whether one connected permitted path exists | n/a. No execution test unless the memo documents a path | Contracting party, clause, customer country, authentication, validation status |
| J4 Exceptions | **Timed case assistance** on participants' real open cases. Arm A: drafts and reminders only. Arm B: human coordination without account access; the user acts. | Participant minutes and contacts saved; time-to-resolution | The **same** legitimate outcome with fewer contacts and less work also counts | Provider minutes for **every** case, including unresolved, escalated and false-positive ones. Report the full distribution and the total, not the share of "profitable" cases. Price or payer only if evidenced. |

## Rules that carry through

- A failed J4 follow-on retires that specific service, not J1–J3.
- A same-choice or same-outcome result can pass on meaningful net effort reduction, after setup and privacy friction.
- Majority-positive cases do not establish positive total economics. Report aggregate provider minutes and the loss tail.
- Do not set economic pass/fail thresholds until their inputs (price or payer, provider minutes, incidence) are observed. Until then, state the rationale and the ambiguity.
- Willingness to try a research concierge is not willingness to adopt or pay for an independent product.
- Not in scope:
  - fundraising, branding or paid acquisition at scale
  - universal integrations
  - an automatic pivot to B2B or B2B2C
  - an exception-service default
