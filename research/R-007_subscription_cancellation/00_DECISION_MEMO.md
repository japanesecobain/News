# R-007 Japan Subscription Cancellation Agent: Decision Memo

**Disposition: PARK.** Do not allocate the next validation cycle to this concept. If you want to keep the option open, buy one decisive input first: **E5, a counsel memo**, which needs your authorisation because it costs money.

*As of 2026-10-05. Desk research only. Every source was reached through search extracts; no page could be opened. Numbers marked "illustrative" are conditional on labelled assumptions in `06_ECONOMICS_MODEL.csv`. They are not estimates.*

## The question

Is there a specific Japanese subscription-cancellation workflow that:
- consumers care enough about;
- a startup can execute better than existing tools;
- the economics support; and
- repeated execution can turn into a compounding asset before incumbents or regulation close the gap?

**Not on current evidence.** The broad concept (find every subscription, cancel it for me, prove it stopped) breaks into six jobs. Most are already done for free or by incumbents. The one differentiated job that survives is executing hard cancellations and verifying the stop, and it fails or is unresolved at every gate.

## What would be tested if unparked

This is the best surviving hypothesis, not a recommendation to build.

- **Exact customer:** Japanese adults with at least one *hard-route* cancellation a year: phone-only lines, written forms, in-person visits. The candidate sub-segments are:
  - people aged 50+ caught in 定期購入 trials;
  - parents on learning subscriptions;
  - adult children managing a parent's subscriptions, acting on the parent's written instruction.
- **Exact job:** J4 + J5. "Get this tedious cancellation done and show me the charge stopped." **Not** discovery (J1), routing (J3) or disputes (J6).
- **Product boundary:**
  - **Out:** negotiation, fee or refund disputes, holding credentials, and paid lawyer referrals.
  - **In:** the user's own signed, per-case instruction ("cancel only; accept no offers"). The user does any authentication directly. The service stops at any disagreement.
  - **Verification:** only on card and bank rails, where the next statement can prove the stop. App Store and carrier rails are left to the user's own lists.
- **Operating model:** a human messenger working from route scripts, with a state model in which a cancellation request is not counted as stopped charges (`model/state_model.py`, 13 checked invariants).
- **Payer:** unresolved. Consumer pay-per-cancellation does not pay back in either illustration. The only model whose margins *improve* with low usage is B2B2C: a card issuer or bank paying per enrolled user. Its break-even fee is ¥5.86–18.37 per enrolled user per month (illustrative), and **no Japanese partner price or appetite was found.**
- **Moat hypothesis:** M1, a route-level outcome graph for hard routes only. Each case would make the next one faster and more likely to succeed. It is conditional on providers accepting a company messenger, on the data being lawful to reuse, and on handling time measurably falling. M6, exclusive bank or issuer distribution, is the other conditional candidate.

## Strongest reason for

**There is a real, unoccupied seam.**
- No Japanese service that cancels subscriptions on users' behalf was found.
- Hard routes are where consumers struggle most:
  - 定期購入 phone lines that do not connect before the next shipment;
  - gyms that require written or in-person notice;
  - learning services that are phone-only.
- 定期購入 alone produces about 80–98k consumer-centre consultations a year, roughly one in ten of all consultations.
- In the US, Rocket Money shows a cancellation concierge can sit inside a large business: $390M revenue in 2025, about 2.5M cancellations made for members.

## Strongest reason against

**Everything easy is taken, and everything hard is unresolved or adverse.**
- **Discovery** is held by Money Forward ME (17.3M users) and Moneytree (about 6.5M users, owned by MUFG Bank since 2025-08-29), and by Apple's, Google's, Amazon's and the carriers' own free lists.
- **Routing**, the most-cited trouble ("could not find the cancellation page", 46.0% of those with trouble), is solved free by guide sites. User-run web routes are 14 of 22 sampled routes, and general AI agents already navigate them.
- **On the hard routes:**
  - The only explicit provider rule found (docomo) limits proxies to **family**.
  - Whether a paid messenger falls under Attorney Act Art. 72 is contested. The closest analogue, resignation agencies, saw a police search in October 2025 and an indictment in February 2026.
- **Economics run into the paradox.** Even the US precedent shows only about 0.25 cancellations per app user, cumulative. In illustrations, cancellation savings justify just ¥22.50–450 a month of subscription, below the ¥300–540 at which incumbents already sell tracking.
- **Regulation has a date.** CAA's planned ban on cancellation obstruction (refusal, delay, misrepresentation) targets exactly these frictions, with a bill as early as 2027.

## Stop conditions

Of the ten conditions in work order §29:
- **Effectively triggered for the easy parts of the concept:** 1, 3, 6 and 7.
- **Leaning against:** 4 and 8.
- **UNRESOLVED:** 2, 5, 9 and 10.

None is resolved in the concept's favour (`01_RESEARCH_REPORT.md`, stop-condition table).

## Why PARK, not STOP or WATCH

- **Not STOP:** the binding gate (permission) is unresolved, not answered negatively, and a single counsel opinion can settle it cheaply.
- **Not WATCH:** no external trigger is expected to improve the thesis without your action. The likeliest triggers (reform; incumbents adding "cancel"; Visa or Mastercard bringing issuer tooling to Japan) all make it worse.

**Unpark if any of these happens:**
- **E5:** counsel finds that undisputed conveyance by a company messenger is workable **and** gives a reliable basis for provider acceptance.
- **E6:** a Japanese issuer or bank states a budget at or above the C07 floor.
- **PR1:** at least 30% of an activity-selected segment hit a hard-route cancellation each year, and at least half of those delegated it or gave up.

## Single next test

**E5: a counsel memo on the specified messenger flow** (report §N.3; legal-matrix questions L01–L05 and L11).
- A **negative** answer stops every on-behalf variant, whatever the demand.
- A **positive** answer is the precondition for spending time on PR1 (Japanese interviews reconstructing participants' real cancellations) and E3 (a founder-run, manual concierge measured against the human-minute frontier).

E5 needs authorisation for counsel fees. PR1 and E3 need authorisation for outreach and live accounts.

## Not done, and not to be assumed

- **No source page was opened.** The CAA lead figures (71.6%, 17.9%) were **not found**; only "about 20%" was confirmed in media extracts.
- **Not established:**
  - the billing-rail mix of Japanese subscriptions;
  - Moneytree's manual-entry support and platform coverage;
  - whether any provider accepts a company agent.
- **No legal advice is given.** The legal matrix lists questions for counsel.
- **Outstanding register entries.** Register supersessions are staged in `REGISTER_UPDATES_PENDING.csv` because your local ledgers are not in this environment: R-005 PARKED_BY_OWNER; R-003 unchanged at NO_BUILD / NO_PROTOTYPE; R-007 PARK.
