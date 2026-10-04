"""CLA economics bridge (derivative). One structure, distinct configurations, unknowns kept unknown.

Configurations (each with its own economic unit):
  C01      read-only tracking                     per active household-month
  C02      approved checkout execution            per permitted attempted action  (gate closed -> not computed)
  C03      comparison / referral handoff          per eligible attributable transaction, rolled to household-month
  C04a     exception assistance (drafting)        per active household-month and per draft
  C04b     human exception case resolution        per case and per active household-month
  C07      partner-distributed tracking           per partner MAU-month (startup side) + partner-side lower bound
  C01+C03  explicit combination                   per active household-month (costs and revenue shown, not hidden)

Scenarios:
  observed         only sourced unit prices, program rules and derived assumptions; every behavioural or
                   workload input is UNKNOWN (None) and every dependent output stays blank.
  illustrative_A   conditional illustration using CLA's original base-case assumptions. NOT a central estimate.
  illustrative_B   conditional illustration using CLA's original upside assumptions. NOT an established company.

Rules: apply each factor once; round only in value_display; activation appears once in cohort maths
(a x r_t x c_t); human minutes are priced once at labour_jpy_per_min whether founder or paid, and fixed
costs exclude case handling; past receipts never become referral revenue.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SCEN = ["observed", "illustrative_A", "illustrative_B"]

# key, config, description, unit, unit_class, status, (observed, A, B), source_ids, note
# status: sourced | rule | derived_assumption | scenario
INPUTS = [
    ("fx", "ALL", "JPY per USD for API list prices", "JPY/USD", "ratio", "derived_assumption", (155, 155, 155), "CLA-S090", "Search-reported 2026 average ~158; not an official rate"),
    ("small_in", "ALL", "Small-model input list price (Claude Haiku 4.5)", "USD/M tokens", "usd", "sourced", (1.0, 1.0, 1.0), "CLA-S091", "Official unit price; workload is separate"),
    ("small_out", "ALL", "Small-model output list price", "USD/M tokens", "usd", "sourced", (5.0, 5.0, 5.0), "CLA-S091", ""),
    ("mid_in", "ALL", "Mid-model input list price (Claude Sonnet 5.5)", "USD/M tokens", "usd", "sourced", (2.0, 2.0, 2.0), "CLA-S091", ""),
    ("mid_out", "ALL", "Mid-model output list price", "USD/M tokens", "usd", "sourced", (10.0, 10.0, 10.0), "CLA-S091", ""),
    ("labor_jpy_per_min", "ALL", "Human minute priced once (paid staff or founder at replacement cost)", "JPY/minute", "jpy", "derived_assumption", (50, 50, 50), "CLA-S073", "From Tokyo CS postings JPY 1,650-1,750/h x ~1.75 load; not a wage statistic"),
    ("line_price", "C01", "LINE official account additional message (<=200k/month)", "JPY/message", "jpy", "sourced", (3, 3, 3), "CLA-S050", "Search extract of LY notice effective 2026-10-01"),
    ("store_fee", "ALL", "Billing/app-store fee on subscriptions", "share", "share", "scenario", (None, 0.15, 0.15), "", "Not researched"),
    # C01
    ("orders_hh", "C01", "Physical-goods orders per active household-month", "orders/household-month", "count", "scenario", (None, 4, 6), "", "No measured frequency (MIC gives spend, not orders)"),
    ("emails_per_order", "C01", "Commerce emails per order reaching the service", "emails/order", "count", "scenario", (None, 3, 3), "", "Depends on capture method and merchant"),
    ("tok_in_email", "C01", "Input tokens per parsed email", "tokens", "tokens", "scenario", (None, 3000, 2500), "", "Workload assumption, not measured"),
    ("tok_out_email", "C01", "Output tokens per parsed email", "tokens", "tokens", "scenario", (None, 300, 250), "", ""),
    ("retry_overhead", "ALL", "Retry/failed-parse multiplier on model workload", "multiplier", "ratio", "scenario", (None, 1.15, 1.10), "", ""),
    ("notif_per_order", "C01", "User notifications per order", "messages/order", "count", "scenario", (None, 2, 2), "", ""),
    ("line_share", "C01", "Share of notifications sent as paid LINE messages", "share", "share", "scenario", (None, 0.25, 0.0), "", ""),
    ("hosting_c01", "C01", "Variable hosting for tracking", "JPY/household-month", "jpy", "scenario", (None, 6, 3), "", ""),
    ("support_c01_rate", "C01", "Support contacts for a read-only tracker (NOT shared with C02/C04)", "contacts/household-month", "count", "scenario", (None, 0.03, 0.015), "", "Separated per product (Grok v2 correction)"),
    ("support_c01_min", "C01", "Minutes per tracker support contact", "minutes", "minutes", "scenario", (None, 8, 6), "", ""),
    ("ingest_exc_rate", "C01", "Ingestion exceptions needing human review (incl. false positives)", "cases/household-month", "count", "scenario", (None, 0.05, 0.02), "", ""),
    ("ingest_exc_min", "C01", "Minutes per ingestion review", "minutes", "minutes", "scenario", (None, 4, 3), "", ""),
    ("paid_share_c01", "C01", "Active households paying a tracker subscription", "share", "share", "scenario", (None, 0.05, 0.10), "", "Willingness to pay unmeasured; Parcel's listed price is not a ceiling or evidence of payment"),
    ("price_c01", "C01", "Tracker subscription list price", "JPY/month", "jpy", "scenario", (None, 480, 480), "", ""),
    ("passive_affiliate", "C01", "Affiliate revenue from historical receipts (no qualifying click)", "JPY/household-month", "jpy", "rule", (0, 0, 0), "GRO-S039;CLA-S030", "Rule zero: not a commission-generating event. Distinct from unknown."),
    # C02
    ("c02_permitted_path", "C02", "A connected permitted path exists for the intended cross-merchant execution task", "boolean", "flag", "rule", (False, False, False), "CLA-S046;GRO-S038", "None established among researched surfaces; standalone merchants and wallets unresearched"),
    # C03
    ("c03_eligible_share_booked", "C03", "Share of orders whose program x interface is approved for a personal-assistant surface", "share", "share", "rule", (0, 0, 0), "CLA-S124;CLA-S125;GRO-S038", "Underwriting exclusion: Rakuten restricts closed/one-to-one tools except approved corporate partners; Amazon/Yahoo/ASP terms for this surface unread. Not a measured zero of opportunity."),
    ("c03_eligible_share_if_approved", "C03", "Share of orders eligible IF program approvals were obtained", "share", "share", "scenario", (None, 0.75, 0.85), "", "Conditional on approvals that do not exist today"),
    ("handoff_share", "C03", "Eligible orders started through the assistant", "share", "share", "scenario", (None, 0.15, 0.30), "", "No observed behaviour"),
    ("completion", "C03", "Handoff -> user completes purchase on merchant site", "share", "share", "scenario", (None, 0.65, 0.80), "", ""),
    ("attribution", "C03", "Completed -> commission credited (window, no override, eligible item)", "share", "share", "scenario", (None, 0.70, 0.85), "", ""),
    ("aov", "C03", "Average order value of referred orders", "JPY/order", "jpy", "scenario", (None, 5000, 6000), "", ""),
    ("comm_rate", "C03", "Commission rate", "share of order value", "share", "scenario", (None, 0.03, 0.04), "CLA-S030;CLA-S031", "Search-reported ranges; official tables unread by CLA"),
    ("cap_per_order", "C03", "Ordinary per-item reward cap (Rakuten)", "JPY/order", "jpy", "sourced", (1000, 1000, 1000), "GRO-S039", "Observed by GRO on the guideline page; treated as one item per order here"),
    ("clawback", "C03", "Share reversed by cancellation/return", "share", "share", "scenario", (None, 0.07, 0.05), "", ""),
    ("passthrough", "C03", "Share of commission returned to user", "share", "share", "scenario", (None, 0.25, 0.10), "", ""),
    ("sessions", "C03", "Comparison sessions per active household-month", "sessions/household-month", "count", "scenario", (None, 3, 4), "", ""),
    ("tok_in_sess", "C03", "Input tokens per session", "tokens", "tokens", "scenario", (None, 15000, 12000), "", ""),
    ("tok_out_sess", "C03", "Output tokens per session", "tokens", "tokens", "scenario", (None, 1500, 1200), "", ""),
    ("hosting_c03", "C03", "Variable hosting for comparison", "JPY/household-month", "jpy", "scenario", (None, 6, 3), "", ""),
    ("support_c03_rate", "C03", "Support contacts for comparison/handoff", "contacts/household-month", "count", "scenario", (None, 0.03, 0.015), "", ""),
    ("support_c03_min", "C03", "Minutes per comparison support contact", "minutes", "minutes", "scenario", (None, 8, 6), "", ""),
    # C04 shared incidence
    ("affected_share", "C04", "Active households with >=1 exception in the month", "share", "share", "scenario", (None, 0.40, 0.40), "", "0.40 is CLA's proposed proceed threshold, not an observed rate"),
    ("incidents_per_affected", "C04", "Exceptions per affected household-month", "cases/household-month", "count", "scenario", (None, 1, 1), "", ""),
    # C04a drafting
    ("draft_uptake", "C04a", "Detected exceptions for which a draft is generated and used", "share", "share", "scenario", (None, 0.5, 0.7), "", ""),
    ("tok_in_draft", "C04a", "Input tokens per draft", "tokens", "tokens", "scenario", (None, 6000, 5000), "", ""),
    ("tok_out_draft", "C04a", "Output tokens per draft", "tokens", "tokens", "scenario", (None, 800, 600), "", ""),
    ("draft_qa_share", "C04a", "Drafts reviewed by a human before sending", "share", "share", "scenario", (None, 0.10, 0.05), "", ""),
    ("draft_qa_min", "C04a", "Minutes per human draft review", "minutes", "minutes", "scenario", (None, 3, 2), "", ""),
    ("user_min_per_draft", "C04a", "Minutes the USER still spends per drafted case", "minutes", "minutes", "scenario", (None, 10, 8), "", "Benefit-side cost borne by user; not provider cost and not zero"),
    # C04b human resolution
    ("submission_prob", "C04b", "Affected households that submit the case to the service", "share", "share", "scenario", (None, 0.5, 0.25), "", ""),
    ("human_share", "C04b", "Submitted cases handled by a human", "share", "share", "scenario", (None, 1.0, 0.5), "", ""),
    ("base_min", "C04b", "First-touch minutes per handled case", "minutes", "minutes", "scenario", (None, 15, 10), "", "Includes unsuccessful/unresolved cases"),
    ("repeat_contacts", "C04b", "Repeat contacts per handled case", "contacts/case", "count", "scenario", (None, 0.5, 0.3), "", ""),
    ("repeat_min", "C04b", "Minutes per repeat contact", "minutes", "minutes", "scenario", (None, 5, 4), "", ""),
    ("escalation_prob", "C04b", "Handled cases escalated", "share", "share", "scenario", (None, 0.2, 0.1), "", ""),
    ("escalation_min", "C04b", "Extra minutes per escalation", "minutes", "minutes", "scenario", (None, 20, 15), "", ""),
    ("fp_cases", "C04b", "False-positive cases opened per active household-month", "cases/household-month", "count", "scenario", (None, 0.05, 0.02), "", ""),
    ("fp_min", "C04b", "Minutes per false-positive case", "minutes", "minutes", "scenario", (None, 3, 2), "", ""),
    # C07 partner
    ("partner_fee", "C07", "Fee paid by partner per MAU-month", "JPY/MAU-month", "jpy", "scenario", (None, 40, 80), "", "CLA's earlier JPY 32-40 was a derived break-even, not a quote"),
    ("support_transfer", "C07", "Share of tracker support absorbed by partner", "share", "share", "scenario", (None, 0.5, 0.5), "", "Transferred, not eliminated: appears as partner-side cost"),
    ("partner_integration_per_mau", "C07", "Amortised integration/onboarding/sales cost per MAU-month (startup side)", "JPY/MAU-month", "jpy", "scenario", (None, None, None), "", "Unknown in every scenario: no sales or integration evidence"),
    # cohort
    ("cpi", "COHORT", "Acquisition cost per acquired user", "JPY/acquired", "jpy", "scenario", (None, 450, 300), "CLA-S070;CLA-S071", "Dated third-party benchmarks"),
    ("activation", "COHORT", "a = P(activated | acquired)", "share", "share", "scenario", (None, 0.21, 0.374), "", "Applied exactly once"),
    ("p_active_m3", "COHORT", "P(active in month 3 | activated)", "share", "share", "scenario", (None, 0.20, 0.35), "", ""),
    ("churn_after_m3", "COHORT", "Monthly churn after month 3 among activated", "share/month", "share", "scenario", (None, 0.08, 0.05), "", ""),
]

UNIT_OF = {k: (u, uc) for k, _c, _d, u, uc, *_r in INPUTS}


# ---------------- None-propagating arithmetic -----------------------------------------------
def _ok(*xs):
    return all(x is not None for x in xs)


def mul(*xs):
    if not _ok(*xs):
        return None
    out = 1.0
    for x in xs:
        out *= x
    return out


def add(*xs):
    return sum(xs) if _ok(*xs) else None


def sub(a, b):
    return a - b if _ok(a, b) else None


def div(a, b):
    return a / b if _ok(a, b) and b != 0 else None


def mn(a, b):
    return min(a, b) if _ok(a, b) else None


# ---------------- Cohort maths: activation counted once ---------------------------------------
def retention_given_activated(p3, churn, horizon=36):
    """r_t = P(active at t | activated): month1=1, month2 interpolated, month3+=p3*(1-churn)^(t-3)."""
    if not _ok(p3, churn):
        return None
    r = []
    for t in range(1, horizon + 1):
        r.append(1.0 if t == 1 else (1 + p3) / 2 if t == 2 else p3 * (1 - churn) ** (t - 3))
    return r


def contribution_per_acquired(c, a=None, r=None, q=None):
    """Return month-t contribution per ACQUIRED user. Use (a, r) OR q, never both."""
    if q is not None and (a is not None or r is not None):
        raise ValueError("double-count guard: pass (a, r) or q, not both")
    if c is None:
        return None
    if q is not None:
        return [qt * c for qt in q]
    if a is None or r is None:
        return None
    return [a * rt * c for rt in r]


def payback_month(cac, monthly):
    if cac is None or monthly is None:
        return None
    cum = 0.0
    for t, x in enumerate(monthly, start=1):
        cum += x
        if cum >= cac:
            return t
    return "never"  # not within horizon (distinct from unknown=None)


# ---------------- Computation -------------------------------------------------------------
def compute(v):
    o = {}
    o["cost_per_email"] = mul(add(mul(v["tok_in_email"], v["small_in"]), mul(v["tok_out_email"], v["small_out"])), 1e-6, v["fx"], v["retry_overhead"])
    o["c01_emails"] = mul(v["orders_hh"], v["emails_per_order"])
    o["c01_inference"] = mul(o["c01_emails"], o["cost_per_email"])
    o["c01_notif"] = mul(v["orders_hh"], v["notif_per_order"], v["line_share"], v["line_price"])
    o["c01_support"] = mul(v["support_c01_rate"], v["support_c01_min"], v["labor_jpy_per_min"])
    o["c01_ingest_review"] = mul(v["ingest_exc_rate"], v["ingest_exc_min"], v["labor_jpy_per_min"])
    o["c01_cost"] = add(o["c01_inference"], o["c01_notif"], v["hosting_c01"], o["c01_support"], o["c01_ingest_review"])
    o["c01_sub_revenue"] = mul(v["paid_share_c01"], v["price_c01"], sub(1.0, v["store_fee"]) if v["store_fee"] is not None else None)
    o["c01_revenue"] = add(o["c01_sub_revenue"], v["passive_affiliate"])
    o["c01_contribution"] = sub(o["c01_revenue"], o["c01_cost"])
    o["c01_breakeven_paid_share"] = div(o["c01_cost"], mul(v["price_c01"], sub(1.0, v["store_fee"]) if v["store_fee"] is not None else None))

    # C02: gate closed -> deliberately not computed
    o["c02_contribution_per_attempt"] = None  # gate: no connected permitted path; structure only

    # C03
    o["c03_net_per_txn"] = mul(mn(mul(v["aov"], v["comm_rate"]), v["cap_per_order"]), sub(1.0, v["clawback"]) if v["clawback"] is not None else None, sub(1.0, v["passthrough"]) if v["passthrough"] is not None else None)
    # Underwriting exclusion is a rule zero: booked volume is 0 whatever the (unknown) behaviour
    o["c03_txn_booked"] = 0.0 if v["c03_eligible_share_booked"] == 0 else mul(v["orders_hh"], v["c03_eligible_share_booked"], v["handoff_share"], v["completion"], v["attribution"])
    o["c03_txn_if_approved"] = mul(v["orders_hh"], v["c03_eligible_share_if_approved"], v["handoff_share"], v["completion"], v["attribution"])
    o["c03_revenue_booked"] = 0.0 if o["c03_txn_booked"] == 0 else mul(o["c03_txn_booked"], o["c03_net_per_txn"])
    o["c03_revenue_if_approved"] = mul(o["c03_txn_if_approved"], o["c03_net_per_txn"])
    o["cost_per_session"] = mul(add(mul(v["tok_in_sess"], v["mid_in"]), mul(v["tok_out_sess"], v["mid_out"])), 1e-6, v["fx"], v["retry_overhead"])
    o["c03_cost"] = add(mul(v["sessions"], o["cost_per_session"]), v["hosting_c03"], mul(v["support_c03_rate"], v["support_c03_min"], v["labor_jpy_per_min"]))
    o["c03_contribution_booked"] = sub(o["c03_revenue_booked"], o["c03_cost"])
    o["c03_contribution_if_approved"] = sub(o["c03_revenue_if_approved"], o["c03_cost"])

    # C04a drafting
    o["c04_cases"] = mul(v["affected_share"], v["incidents_per_affected"])
    o["c04a_drafts"] = mul(o["c04_cases"], v["draft_uptake"])
    o["cost_per_draft"] = mul(add(mul(v["tok_in_draft"], v["mid_in"]), mul(v["tok_out_draft"], v["mid_out"])), 1e-6, v["fx"], v["retry_overhead"])
    o["c04a_cost"] = add(mul(o["c04a_drafts"], o["cost_per_draft"]), mul(o["c04a_drafts"], v["draft_qa_share"], v["draft_qa_min"], v["labor_jpy_per_min"]))
    o["c04a_user_minutes"] = mul(o["c04a_drafts"], v["user_min_per_draft"])
    o["c04a_breakeven_revenue"] = o["c04a_cost"]

    # C04b human case resolution (failures, unresolved and false positives all cost minutes)
    o["c04b_handled_cases"] = mul(o["c04_cases"], v["submission_prob"], v["human_share"])
    o["c04b_min_per_handled"] = add(v["base_min"], mul(v["repeat_contacts"], v["repeat_min"]), mul(v["escalation_prob"], v["escalation_min"]))
    o["c04b_labor"] = add(mul(o["c04b_handled_cases"], o["c04b_min_per_handled"], v["labor_jpy_per_min"]), mul(v["fp_cases"], v["fp_min"], v["labor_jpy_per_min"]))
    o["c04b_cost_per_handled_case"] = div(o["c04b_labor"], o["c04b_handled_cases"])
    o["reviewer_300_check"] = mul(0.40, 1, 1, 1, 15, v["labor_jpy_per_min"])  # all affected submit, all human, 15 min

    # C07 partner distribution (startup side and partner-side lower bound)
    o["c07_startup_cost"] = add(o["c01_inference"], v["hosting_c01"], mul(o["c01_support"], sub(1.0, v["support_transfer"]) if v["support_transfer"] is not None else None), o["c01_ingest_review"], v["partner_integration_per_mau"])
    o["c07_startup_cost_excl_integration"] = add(o["c01_inference"], v["hosting_c01"], mul(o["c01_support"], sub(1.0, v["support_transfer"]) if v["support_transfer"] is not None else None), o["c01_ingest_review"])
    o["c07_contribution"] = sub(v["partner_fee"], o["c07_startup_cost"])
    o["c07_contribution_excl_integration"] = sub(v["partner_fee"], o["c07_startup_cost_excl_integration"])
    o["c07_partner_min_benefit"] = add(v["partner_fee"], mul(o["c01_support"], v["support_transfer"]))
    o["c07c04b_contribution_excl_integration"] = sub(o["c07_contribution_excl_integration"], o["c04b_labor"])

    # Explicit combination C01+C03 (shared hosting/support NOT netted: both products' costs listed)
    o["c0103_contribution_booked"] = sub(add(o["c01_revenue"], o["c03_revenue_booked"]), add(o["c01_cost"], o["c03_cost"]))

    # Cohort (activation once) for C03-if-approved and C01
    r = retention_given_activated(v["p_active_m3"], v["churn_after_m3"])
    for name, c in (("c03_if_approved", o["c03_contribution_if_approved"]), ("c01", o["c01_contribution"])):
        monthly = contribution_per_acquired(c, a=v["activation"], r=r)
        o[f"payback_{name}"] = payback_month(v["cpi"], monthly) if (c is not None and c > 0) else (None if c is None else "never")
        o[f"ltv36_per_acquired_{name}"] = sum(monthly) if monthly is not None else None
    return o


# output metadata: key -> (config, description, unit, unit_class, formula, gate_fields)
OUT_META = {
    "cost_per_email": ("C01", "Model cost per parsed email (official price x workload assumption)", "JPY/email", "jpy", "(tok_in*small_in+tok_out*small_out)/1e6*fx*retry_overhead"),
    "c01_emails": ("C01", "Emails processed", "emails/household-month", "count", "orders_hh*emails_per_order"),
    "c01_inference": ("C01", "Tracking inference cost", "JPY/household-month", "jpy", "c01_emails*cost_per_email"),
    "c01_notif": ("C01", "Paid notification cost", "JPY/household-month", "jpy", "orders_hh*notif_per_order*line_share*line_price"),
    "c01_support": ("C01", "Tracker support cost", "JPY/household-month", "jpy", "support_c01_rate*support_c01_min*labor"),
    "c01_ingest_review": ("C01", "Ingestion review cost", "JPY/household-month", "jpy", "ingest_exc_rate*ingest_exc_min*labor"),
    "c01_cost": ("C01", "Tracking variable cost", "JPY/household-month", "jpy", "sum of C01 cost lines + hosting_c01"),
    "c01_sub_revenue": ("C01", "Subscription revenue", "JPY/household-month", "jpy", "paid_share*price*(1-store_fee)"),
    "c01_revenue": ("C01", "Total revenue (subscription + rule-zero passive affiliate)", "JPY/household-month", "jpy", "c01_sub_revenue+passive_affiliate"),
    "c01_contribution": ("C01", "Tracking contribution", "JPY/household-month", "jpy", "c01_revenue-c01_cost"),
    "c01_breakeven_paid_share": ("C01", "Paid share needed to cover C01 variable cost", "share", "share", "c01_cost/(price*(1-store_fee))"),
    "c02_contribution_per_attempt": ("C02", "Execution contribution per permitted attempt", "JPY/attempt", "jpy", "NOT COMPUTED: no connected permitted path (gate)"),
    "c03_net_per_txn": ("C03", "Net retained commission per attributable transaction (cap, clawback, pass-through applied once)", "JPY/transaction", "jpy", "min(aov*comm_rate,cap)*(1-clawback)*(1-passthrough)"),
    "c03_txn_booked": ("C03", "Attributable transactions under current underwriting gates", "transactions/household-month", "count", "orders*eligible_booked*handoff*completion*attribution"),
    "c03_txn_if_approved": ("C03", "Attributable transactions IF program approvals obtained", "transactions/household-month", "count", "orders*eligible_if_approved*handoff*completion*attribution"),
    "c03_revenue_booked": ("C03", "Booked referral revenue (personal-assistant surface)", "JPY/household-month", "jpy", "c03_txn_booked*c03_net_per_txn"),
    "c03_revenue_if_approved": ("C03", "Conditional referral revenue IF approved", "JPY/household-month", "jpy", "c03_txn_if_approved*c03_net_per_txn"),
    "cost_per_session": ("C03", "Model cost per comparison session", "JPY/session", "jpy", "(tok_in_sess*mid_in+tok_out_sess*mid_out)/1e6*fx*retry_overhead"),
    "c03_cost": ("C03", "Comparison variable cost", "JPY/household-month", "jpy", "sessions*cost_per_session+hosting_c03+support"),
    "c03_contribution_booked": ("C03", "Comparison contribution under current gates", "JPY/household-month", "jpy", "c03_revenue_booked-c03_cost"),
    "c03_contribution_if_approved": ("C03", "Comparison contribution IF approved (conditional)", "JPY/household-month", "jpy", "c03_revenue_if_approved-c03_cost"),
    "c04_cases": ("C04", "Exceptions per active household-month", "cases/household-month", "count", "affected_share*incidents_per_affected"),
    "c04a_drafts": ("C04a", "Drafts used", "drafts/household-month", "count", "c04_cases*draft_uptake"),
    "cost_per_draft": ("C04a", "Model cost per draft", "JPY/draft", "jpy", "(tok_in_draft*mid_in+tok_out_draft*mid_out)/1e6*fx*retry_overhead"),
    "c04a_cost": ("C04a", "Drafting provider cost incl. human QA", "JPY/household-month", "jpy", "drafts*cost_per_draft+drafts*qa_share*qa_min*labor"),
    "c04a_user_minutes": ("C04a", "User minutes still spent (benefit-side; not zero)", "minutes/household-month", "minutes", "drafts*user_min_per_draft"),
    "c04a_breakeven_revenue": ("C04a", "Revenue needed to cover drafting cost (payment mechanism unknown)", "JPY/household-month", "jpy", "=c04a_cost"),
    "c04b_handled_cases": ("C04b", "Human-handled cases", "cases/household-month", "count", "c04_cases*submission_prob*human_share"),
    "c04b_min_per_handled": ("C04b", "Minutes per handled case incl. repeats and escalation", "minutes/case", "minutes", "base_min+repeat_contacts*repeat_min+escalation_prob*escalation_min"),
    "c04b_labor": ("C04b", "Human resolution labour incl. false positives", "JPY/household-month", "jpy", "handled*min_per_handled*labor+fp_cases*fp_min*labor"),
    "c04b_cost_per_handled_case": ("C04b", "Labour per handled case (break-even per-case fee before other costs)", "JPY/case", "jpy", "c04b_labor/c04b_handled_cases"),
    "reviewer_300_check": ("C04b", "Reviewer arithmetic: 0.40 x 1 case x all submit x all human x 15 min x labour", "JPY/household-month", "jpy", "0.40*1*1*1*15*labor"),
    "c07_startup_cost": ("C07", "Startup variable cost per partner MAU incl. integration", "JPY/MAU-month", "jpy", "inference+hosting+support*(1-transfer)+ingest_review+integration"),
    "c07_startup_cost_excl_integration": ("C07", "Startup variable cost per partner MAU excl. unknown integration", "JPY/MAU-month", "jpy", "inference+hosting+support*(1-transfer)+ingest_review"),
    "c07_contribution": ("C07", "Startup contribution per partner MAU (integration unknown -> blank)", "JPY/MAU-month", "jpy", "partner_fee-c07_startup_cost"),
    "c07_contribution_excl_integration": ("C07", "Startup contribution per MAU before integration/sales cost (upper bound)", "JPY/MAU-month", "jpy", "partner_fee-c07_startup_cost_excl_integration"),
    "c07_partner_min_benefit": ("C07", "Partner must realise at least this benefit per MAU (fee + transferred support), before its own integration cost", "JPY/MAU-month", "jpy", "partner_fee+support*transfer"),
    "c07c04b_contribution_excl_integration": ("C07+C04b", "Partner-fee tracking PLUS human case resolution (upper bound)", "JPY/MAU-month", "jpy", "c07_contribution_excl_integration-c04b_labor"),
    "c0103_contribution_booked": ("C01+C03", "Explicit combination under current gates", "JPY/household-month", "jpy", "(c01_revenue+c03_revenue_booked)-(c01_cost+c03_cost)"),
    "payback_c03_if_approved": ("COHORT", "Payback month per acquired user, C03 if approved (0 = not within 36 months; blank = unknown)", "month", "months", "a*r_t*c_t cumulative >= cpi"),
    "ltv36_per_acquired_c03_if_approved": ("COHORT", "36-month contribution per acquired user, C03 if approved", "JPY/acquired", "jpy", "sum_t a*r_t*c_t"),
    "payback_c01": ("COHORT", "Payback month per acquired user, C01", "month", "months", "a*r_t*c_t cumulative >= cpi"),
    "ltv36_per_acquired_c01": ("COHORT", "36-month contribution per acquired user, C01", "JPY/acquired", "jpy", "sum_t a*r_t*c_t"),
}

GATES = {
    "c03_revenue_booked": ("restricted or unresolved by program x surface", "Rakuten closed-tool restriction (search extract); Amazon/Yahoo/ASP surface terms unread", "excluded from investment case", "unknown"),
    "c03_contribution_booked": ("restricted or unresolved by program x surface", "as above", "excluded from investment case", "unknown"),
    "c02_contribution_per_attempt": ("no connected permitted path established", "standalone merchants/wallets unresearched", "execution not approved", "unknown"),
    "c01_revenue": ("passive affiliate = rule zero", "n/a", "subscription unmeasured", "unknown beyond rule zero"),
}


def scenario_inputs(i):
    return {k: vals[i] for k, _c, _d, _u, _uc, _s, vals, *_r in INPUTS}


def display(x, unit_class):
    if x is None:
        return ""
    if isinstance(x, (bool, str)):
        return str(x)
    places = {"jpy": 2, "share": 4, "count": 4, "minutes": 2, "months": 0, "tokens": 0, "usd": 2, "ratio": 4}.get(unit_class, 4)
    return f"{x:.{places}f}"


def exact(x):
    if x is None:
        return ""
    if isinstance(x, (bool, str)):
        return str(x)
    return repr(float(x))


RULE_ZERO_OUTPUTS = ("c03_txn_booked", "c03_revenue_booked")


def status_of_output(key, val, scen):
    if key in ("c02_contribution_per_attempt",):
        return "gated_not_computed"
    if key in RULE_ZERO_OUTPUTS and val == 0:
        return "rule_zero_underwriting_exclusion"
    if key == "reviewer_300_check":
        return "conditional_sensitivity_not_observed"
    if val == "never":
        return "not_within_36_months"
    if val is None:
        return "unknown"
    if scen == "observed":
        return "calculated_from_sourced_or_rule_inputs"
    return "calculated_conditional_illustration"


HEADER = ["config", "scenario", "variable_id", "kind", "description", "unit", "unit_class", "value_exact", "value_display",
          "status", "permission_status", "applicability_status", "underwriting_treatment", "commercial_amount",
          "formula", "source_ids", "note"]


def build_rows():
    rows = []
    for i, s in enumerate(SCEN):
        v = scenario_inputs(i)
        for k, c, d, u, uc, st, vals, src, note in INPUTS:
            val = vals[i]
            stt = st if val is not None else "unknown"
            rows.append([c, s, k, "input", d, u, uc, exact(val), display(val, uc), stt, "", "", "", "", "", src, note])
        o = compute(v)
        for k, (c, d, u, uc, f) in OUT_META.items():
            val = o[k]
            perm, appl, under, comm = GATES.get(k, ("", "", "", ""))
            rows.append([c, s, k, "output", d, u, uc, exact(val), display(val, uc), status_of_output(k, val, s), perm, appl, under, comm, f, "", ""])
    return rows


def write(path=os.path.join(HERE, "bridge_outputs.csv")):
    rows = build_rows()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)
    return path


def stress_grid(path=os.path.join(HERE, "c04_stress_grid.csv")):
    """C04b labour per active household-month vs a JPY 32-40 partner fee. Conditional sensitivity, not observed rates."""
    A = scenario_inputs(1)
    c01_core = compute(A)["c07_startup_cost_excl_integration"]  # illustrative_A tracking core cost per MAU
    labor = A["labor_jpy_per_min"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["affected_share", "cases_per_affected", "submission_prob", "human_share", "minutes_per_handled_case", "labor_jpy_per_min",
                    "labor_jpy_per_household_month_exact", "fee_32_covers_labor_alone", "fee_40_covers_labor_alone",
                    "fee_40_covers_labor_plus_tracking_core_illustrativeA", "tracking_core_illustrativeA_exact"])
        for p in (0.05, 0.10, 0.25, 0.50, 1.0):
            for h in (0.25, 0.5, 1.0):
                for m in (5, 10, 15, 30):
                    lab = 0.40 * 1 * p * h * m * labor
                    w.writerow([0.40, 1, p, h, m, labor, repr(lab), lab <= 32, lab <= 40, lab + c01_core <= 40, repr(c01_core)])
    # analytic bound: max (submission x human_share x minutes) affordable
    return path, {"max_psm_fee32_labor_only": 32 / (0.40 * labor), "max_psm_fee40_labor_only": 40 / (0.40 * labor),
                  "max_psm_fee40_after_tracking_core": (40 - c01_core) / (0.40 * labor), "tracking_core_A": c01_core}


if __name__ == "__main__":
    print("wrote", write())
    p, b = stress_grid()
    print("wrote", p, b)
