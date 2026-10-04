# CLA-D05: State and provenance corrections to CLA's operating traces

**Scope.** This corrects Trace A (tracking) and Trace B (handoff) in the original `01_research_report.md` §3.3. The original files are unchanged. These corrections are design rules for any later prototype. Nothing here is built or tested.

## 1. Evidence provenance

| Original assumption | Corrected rule |
|---|---|
| "DKIM/SPF/DMARC check" makes forwarded mail authenticated merchant mail | A **manual forward** is a new message from the user, so the merchant's original authentication cannot be established from it. An **auto-forward** may keep the original DKIM signature, but SPF fails and body or header changes can break it. Record every item as `user_supplied` (forwarded, pasted, screenshot or redacted) unless the original message, with verifiable signatures, was examined. **Never** derive an action, payment state or refund state from user-supplied text alone. |
| Redacted record = anonymous | Order numbers, tracking numbers and order-page links can still identify a person after redaction. Do not retain them unless a stated purpose needs them, and keep local-review consent separate from retention consent and from upload-to-AI consent. |

## 2. Lifecycle states that must stay distinct

| Collapsed in v1 | Separate states |
|---|---|
| "Refund received" | `REFUND_REQUESTED` (by user) → `REFUND_REPORTED_ISSUED` (merchant message) → `FUNDS_RECEIVED` (user's card or bank statement, shown voluntarily) |
| Missing confirmation = order failed or payment pending | `NO_CONFIRMATION_SEEN`, an evidence gap and **not a payment state**, distinct from `PAYMENT_STATE_UNKNOWN` |
| Order = parcel | Order ↔ package is **one-to-many** (split shipments, partial cancellation). Package-level states are `IN_TRANSIT / DELIVERED / EXCEPTION / UNKNOWN / TRACKED_IN_MERCHANT_APP`. Order closure follows return-window and refund states, not delivery. |
| "Delivered" | Only the carrier- or merchant-reported event, with its timestamp. Never inferred. |

## 3. Mandates and idempotency

| v1 wording | Correction |
|---|---|
| "Mandates are idempotent" / "max-price mandate" | A **local mandate** records what the user approved. It can only **detect** a mismatch afterwards (amount above the approved maximum, duplicate confirmation). It does **not** enforce a spend cap or idempotency at the merchant. Merchant-side enforcement exists only where a merchant or protocol integration provides it. None was established for the intended task (CLA-D03 G03, G14). |
| "A second confirmation is flagged as duplicate" | Correct only as detection. The user resolves it on the merchant's surface. |

## 4. Identifiers and matching

| v1 wording | Correction |
|---|---|
| Upsert keyed on merchant + order ID | Key on **(user/tenant ID, merchant, order ID)**. Order numbers are not globally unique across users, and household members can share mailboxes. |
| "Mandate stores the JAN"; match by JAN | A missing or ambiguous JAN, or one JAN covering several variants or sellers, **never** produces `CONFIRMED_MATCH`. Use `CANDIDATE_MATCH` and ask the user to confirm the variant. |

## 5. Cost accounting for the states above

- Every `NEEDS_REVIEW`, `UNKNOWN` and false-positive case costs human minutes, including cases that end unresolved. The bridge's C04b labour line counts handled, unresolved, escalated and false-positive cases.
- A case the **user** resolves is not free. The user's minutes are reported as a benefit-side cost (`c04a_user_minutes`), not as zero.
