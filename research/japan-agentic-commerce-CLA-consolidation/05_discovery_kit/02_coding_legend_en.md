# Coding legend (English) for the job-comparison interviews

Code each **purchase × job** observation as one row in `03b_purchase_job_sheet.csv`. Code each person once in `03a_participant_sheet.csv`. Keep **observed or recalled facts** separate from **stated intentions**.

## Units and selection

| Field | Codes | Rule |
|---|---|---|
| `selection_arm` | `ACT` (activity-selected, ~12) / `INC` (incident-selected, ≤8) | Never pool ACT and INC when describing how common something is. INC deepens mechanisms only. |
| `unit_role` | `IND` individual / `HHC` household coordinator | Use one `household_id` per household. When two members are interviewed, mark shared purchases `shared_with` so they are counted once. |
| `platform` | `AMZ`, `RKT` (Rakuten Ichiba), `YSH` (Yahoo! Shopping), `SHP` (Shopify store), `BRD` (other brand or retailer site), `C2C`, `OTH` | Independent retail platform level. |
| `seller` | Free text or `1P` (platform sells) / `3P` (marketplace seller) | Seller level within a platform. "Two merchants" must say which level. |
| `window` | `D30` (last 30 days) / `D90` (last 90 days) / `PROSP` (prospective diary, if any) | Retrospective and prospective measures are different measurements. Never add them together. |

## Jobs

| Code | Job | What to capture |
|---|---|---|
| `J1` | Offer selection / comparison | Trigger, starting point, number of sites compared, criteria (price, shipping, points, date), recalled minutes, uncertainty, satisfaction with choice |
| `J2` | Checkout (with saved details) | Saved address/payment (Y/N), friction type (`OTP`, `COUPON`, `POINTS`, `ADDRESS`, `ERROR`, `NONE`), recalled minutes |
| `J3` | Delivery coordination | Information channel (`CARRIER_LINE`, `CARRIER_MEMBER`, `MERCHANT_APP`, `EMAIL`, `GMAIL_VIEW`, `PARCEL`, `OTHER_APP`, `NONE`), changes made, redelivery (Y/N), missed information |
| `J4` | Exception | Type (`LATE`, `MISSING`, `DAMAGED`, `WRONG`, `CANCEL`, `RETURN`, `REFUND`, `OTHER`), contacts, minutes, cash tied up, outcome, refund evidence state |

## Effort and outcome

| Field | Codes or scale | Note |
|---|---|---|
| `minutes_recalled` | Number, or bin `<5`, `5-15`, `15-30`, `30-60`, `>60` | The participant's recall of the original task. **Interview reconstruction time is not task time.** |
| `contacts` | Integer | Messages or calls to merchant or carrier, including repeats |
| `apps_touched` | Integer | Distinct apps, sites or inboxes used for the job |
| `uncertainty` | 0 none / 1 mild / 2 notable / 3 high | As described by the participant |
| `cash_tied_jpy`, `cash_tied_days` | Numbers | For refunds and returns |
| `outcome` | `RES_FULL`, `RES_PARTIAL`, `UNRESOLVED`, `ABANDONED`, `NA` | A closed incident can still have been costly; code effort regardless of outcome |
| `refund_state` | `REQUESTED`, `REPORTED_ISSUED`, `FUNDS_SEEN`, `NA` | Never upgrade `REPORTED_ISSUED` to `FUNDS_SEEN` without the participant's own confirmation |
| `current_tool` / `tool_satisfaction` | Tool code / 1–5 | Record satisfied users fully |
| `residual_burden` | `NONE` / `MINOR` / `MATERIAL` / `UNCLEAR` | See the coding rule below |
| `provenance` | `MEM` recall / `SELF_LOOK` participant checked own device / `SHOWN` shown on participant's screen | Never `COPIED`. Order and tracking numbers are not transcribed. |

**Coding rule for `MATERIAL`.** This is a pre-declared screening definition, not a market threshold. Code `MATERIAL` when the participant's current tools did **not** remove the burden **and** any one of the following holds:
- 15 or more recalled minutes on the job;
- 2 or more contacts;
- cash tied up for 7 or more days;
- uncertainty 2 or higher;
- the participant names it as the task they least want to do.

Code `UNCLEAR` when the account is too thin to tell. Two coders should code the first three interviews independently and reconcile their differences.

## Opportunity and censoring

- `purchases_in_window` is the denominator for J1–J3 observations (the opportunities to use).
- A participant with no exception in the window is coded `J4 = NONE_IN_WINDOW`. That is **not** evidence that exception help has no value, and it is not "churn".
- Low event frequency limits what can be observed. It does not establish product rejection.

## Stated intentions (keep separate)

| Field | Codes |
|---|---|
| `would_try_research_concierge` | `Y` / `N` / `MAYBE` (help from a person in this study) |
| `would_adopt_independent_product` | `Y` / `N` / `MAYBE` |
| `delegation_ceiling` | `NONE` / `SUGGEST` / `PREPARE_WITH_CONFIRM` / `EXECUTE_WITH_CONFIRM` (as stated) |
| `record_shown` | `YES` / `DECLINED` / `NOT_ASKED` |

A shown record is evidence about that capture method only. A refusal applies to that method only.
