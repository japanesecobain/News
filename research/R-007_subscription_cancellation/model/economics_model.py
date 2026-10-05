"""R-007 economics model: concepts C01-C08, the 'success reduces need' paradox, frontiers and a
bottom-up market per 1M target users.

Run: python3 model/economics_model.py   -> writes ../06_ECONOMICS_MODEL.csv (full precision + display column)

Method rules carried over from R-003 (methods only):
  * Unknown is not zero. An input with no evidence is None in the 'observed' scenario, and every
    output that depends on it is None with status 'unknown'. A rule zero (e.g. no class-A route found)
    is labelled 'rule', not 'unknown'.
  * Scenarios 'illustrative_tight' and 'illustrative_loose' are CONDITIONAL ILLUSTRATIONS built from
    labelled assumptions. They are not estimates and not a range for the truth.
  * One labour price (labor_jpy_per_min = wage x load / 60) prices every human minute exactly once.
  * Activation is counted once in cohorts: LTV = sum_t a * r_t * c_t.
  * Exports carry exact values (repr) for data and a separate rounded column for display only.
"""
import csv
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCEN = ["observed", "illustrative_tight", "illustrative_loose"]
HORIZON = 36

# key, description, unit, unit_class, status, value (observed/rule) OR (tight, loose) for assumptions, evidence
# status: observed (sourced; same in all scenarios) | rule (labelled rule value) | assumption (None in 'observed')
#         | unknown (None everywhere: no evidence and no defensible illustration)
INPUTS = [
    # --- labour, FX, model cost
    ("wage_jpy_per_hour", "Posted hourly wage, Kanto phone operators (job-board average)", "JPY/hour", "jpy", "observed", 1749.0, "R7-E-H02"),
    ("min_wage_jpy_per_hour", "National weighted-average minimum wage FY2025 (comparator only)", "JPY/hour", "jpy", "observed", 1121.0, "R7-E-H01"),
    ("load_factor", "Employer load on posted wage (social insurance, supervision, idle time)", "ratio", "ratio", "assumption", (1.6, 1.3), "none (assumption)"),
    ("fx_jpy_per_usd", "Exchange rate", "JPY/USD", "ratio", "assumption", (160.0, 140.0), "none (assumption)"),
    ("llm_price_in_usd_per_mtok", "Model input price (tight: mid-tier model; loose: small-tier model)", "USD/Mtok", "usd", "assumption", (2.0, 1.0), "R7-E-H03 (prices observed; model choice assumed)"),
    ("llm_price_out_usd_per_mtok", "Model output price (tight: mid-tier model; loose: small-tier model)", "USD/Mtok", "usd", "assumption", (10.0, 5.0), "R7-E-H03"),
    ("llm_in_tokens_per_request", "Input tokens per cancellation request (routing, scripts, logs)", "tokens", "tokens", "assumption", (60000.0, 20000.0), "none (assumption)"),
    ("llm_out_tokens_per_request", "Output tokens per cancellation request", "tokens", "tokens", "assumption", (6000.0, 2000.0), "none (assumption)"),
    ("infra_jpy_per_user_year", "Hosting, storage, monitoring per paying user-year", "JPY/user-year", "jpy", "assumption", (600.0, 200.0), "none (assumption)"),
    # --- demand and the paradox
    ("subs_stock_per_user", "Recurring subscriptions held per target user at start", "count", "count", "assumption", (2.0, 3.0), "R7-E-B07 (SVOD 2.0 per SVOD user: one category only)"),
    ("unwanted_share", "Share of held or new subscriptions the user comes to want cancelled", "share", "share", "assumption", (0.3, 0.5), "R7-E-A12 (19.1% hold an unused one: different metric)"),
    ("help_needed_share", "Share of wanted cancellations the user would hand to the service", "share", "share", "assumption", (0.3, 0.6), "none (H05 untested)"),
    ("new_subs_per_user_year", "New recurring subscriptions started per user-year", "count/yr", "count", "assumption", (1.0, 2.0), "none (assumption)"),
    ("monthly_price_cancelled_sub_jpy", "Monthly price of a typical subscription the user cancels", "JPY/month", "jpy", "assumption", (1000.0, 1500.0), "R7-E-A14 (modal TOTAL spend ≤¥2,000/month)"),
    ("months_saved_per_cancellation", "Months the user would otherwise have kept paying (counterfactual)", "months", "months", "assumption", (3.0, 6.0), "none (counterfactual; untested)"),
    # --- route mix and handling (C03-C05)
    ("share_route_A", "Share of requests with a machine-executable third-party path", "share", "share", "rule", 0.0, "R7-E-C24 (no class-A route found; rule zero)"),
    ("share_route_B", "Share of requests on user-run routes (handoff)", "share", "share", "assumption", (0.5, 0.75), "R7-E-C24 (sample 14/22 = 0.636; NOT a market share)"),
    ("handoff_support_min", "Agent minutes supporting one user-run (B) request", "min", "minutes", "assumption", (6.0, 2.0), "none (assumption)"),
    ("human_min_per_request", "Agent minutes per human-route request (phone, written, visit prep)", "min", "minutes", "assumption", (45.0, 15.0), "R7-E-G18 (US: 2-10 business days lead time; minutes not published)"),
    ("phone_cost_jpy_per_human_request", "Telephony cost per human-route request", "JPY/request", "jpy", "assumption", (100.0, 30.0), "none (assumption)"),
    ("provider_failure_rate", "Share of first attempts that fail and must be redone", "share", "share", "assumption", (0.3, 0.1), "R7-E-B05; R7-E-A10 (failure modes exist; rate unknown)"),
    ("repeat_contacts_per_failure", "Extra attempts per failure", "count", "count", "assumption", (2.0, 1.0), "none (assumption)"),
    ("fraud_identity_min_per_request", "Minutes on identity and instruction checks per request", "min", "minutes", "assumption", (5.0, 2.0), "none (assumption)"),
    ("verification_cost_jpy_per_request", "Cost to verify a stop for one request (statement check or receipt)", "JPY/request", "jpy", "assumption", (50.0, 10.0), "none (assumption); see F.3"),
    ("persist_rate", "Share of accepted cancellations where a charge persists without contractual reason", "share", "share", "assumption", (0.1, 0.03), "R7-E-A08; R7-E-A10 (exists; rate unknown)"),
    # --- prices and revenue
    ("sub_price_jpy_month", "Consumer subscription price (C01/C03/C05)", "JPY/month", "jpy", "assumption", (300.0, 540.0), "R7-E-G10 (¥280); R7-E-G05 (¥360); R7-E-G02 (¥540): anchors, choice assumed"),
    ("payment_fee_rate", "Payment cost as share of revenue (tight: app-store 15%; loose: card 3.6%)", "share", "share", "assumption", (0.15, 0.036), "none (rates not sourced)"),
    ("per_cancel_fee_jpy", "Per-cancellation fee (C04; added in C05)", "JPY/request", "jpy", "assumption", (500.0, 1500.0), "none (assumption)"),
    ("refund_rate", "Refunds and chargebacks as share of revenue", "share", "share", "assumption", (0.05, 0.01), "none (assumption)"),
    ("guide_revenue_per_user_year", "C02 guide revenue (ads or affiliate) per user-year", "JPY/user-year", "jpy", "unknown", None, "none: no source for guide-site revenue"),
    # --- C06 negotiation (legal gate L06)
    ("neg_requests_per_user_year", "Negotiation attempts per user-year", "count/yr", "count", "assumption", (0.2, 0.5), "none (assumption)"),
    ("neg_success_rate", "Share of negotiations that lower the price", "share", "share", "assumption", (0.2, 0.5), "none (no Japan evidence)"),
    ("neg_annual_savings_jpy", "Annual saving per successful negotiation", "JPY/success", "jpy", "assumption", (3000.0, 6000.0), "R7-E-E08 (telecom caps shrink value): no Japan source"),
    ("neg_success_fee_share", "Success fee share of first-year savings", "share", "share", "assumption", (0.35, 0.60), "R7-E-G20 (US Rocket Money 35-60%)"),
    ("neg_minutes", "Agent minutes per negotiation attempt", "min", "minutes", "assumption", (30.0, 15.0), "none (assumption)"),
    # --- C07 B2B2C
    ("partner_fee_jpy_per_enrolled_month", "Partner fee per enrolled user-month", "JPY/user-month", "jpy", "assumption", (20.0, 60.0), "none (no Japan B2B2C price found)"),
    ("partner_enrolled_users", "Enrolled users per partner", "count", "count", "assumption", (50000.0, 200000.0), "none (assumption)"),
    ("partner_engaged_share", "Share of enrolled users who use the service in a year", "share", "share", "assumption", (0.1, 0.3), "none (assumption)"),
    ("partner_integration_jpy", "One-off integration and security review per partner", "JPY/partner", "jpy", "assumption", (20000000.0, 5000000.0), "none (assumption)"),
    ("partner_amortisation_years", "Years over which integration is amortised", "years", "count", "rule", 3.0, "rule (horizon)"),
    ("partner_sales_cost_jpy", "Business-development cost to win one partner (one-off; amortised like integration)", "JPY/partner", "jpy", "assumption", (10000000.0, 3000000.0), "none (assumption); sales cycle not modelled"),
    # --- C08 switching
    ("switches_per_user_year", "Switching events per user-year", "count/yr", "count", "assumption", (0.05, 0.2), "none (assumption)"),
    ("referral_jpy_per_switch", "Referral revenue per completed switch", "JPY/switch", "jpy", "assumption", (2040.0, 4080.0), "R7-E-H04 (¥170/household-month × 12 or 24 months; weak)"),
    ("switch_handling_min", "Agent minutes per switch", "min", "minutes", "assumption", (10.0, 5.0), "none (assumption)"),
    # --- cohort
    ("cac_jpy", "Acquisition cost per acquired user", "JPY/user", "jpy", "assumption", (3000.0, 1000.0), "none (no Japan CAC source)"),
    ("activation", "Share of acquired users who become active payers (a)", "share", "share", "assumption", (0.3, 0.6), "none (assumption)"),
    ("monthly_churn", "Monthly churn of active payers (r_t = (1-churn)^(t-1))", "share", "share", "assumption", (0.10, 0.04), "none (assumption)"),
    ("target_penetration", "Paying share of target users (market illustration only)", "share", "share", "assumption", (0.01, 0.05), "none (assumption)"),
    ("monthly_sub_spend_jpy", "Monthly subscription spend per target user", "JPY/month", "jpy", "assumption", (2000.0, 3000.0), "R7-E-A14 (modal band ≤¥2,000); R7-E-A18 (unresolved)"),
]

INPUT_INDEX = {k: i for i, (k, *_r) in enumerate(INPUTS)}


def scenario_inputs(i):
    """Input dict for scenario index i (0=observed, 1=tight, 2=loose)."""
    v = {}
    for key, _d, _u, _uc, status, val, _e in INPUTS:
        if status in ("observed", "rule"):
            v[key] = val
        elif status == "assumption":
            v[key] = None if i == 0 else val[i - 1]
        elif status == "unknown":
            v[key] = None
        else:
            raise ValueError(status)
    return v


# ---------------- None-propagating arithmetic ----------------
def _n(*xs):
    return any(x is None for x in xs)


def mul(*xs):
    if _n(*xs):
        return None
    out = 1.0
    for x in xs:
        out *= x
    return out


def add(*xs):
    if _n(*xs):
        return None
    return float(sum(xs))


def sub(a, b):
    return None if _n(a, b) else a - b


def div(a, b):
    if _n(a, b) or b == 0:
        return None
    return a / b


# ---------------- cohort (activation counted once) ----------------
def retention_given_activated(churn, horizon=HORIZON):
    if churn is None:
        return None
    return [(1.0 - churn) ** (t - 1) for t in range(1, horizon + 1)]


def contribution_per_acquired(c_month, a=None, r=None, q=None):
    """Sum over months of expected contribution per ACQUIRED user.
    Pass (a, r) OR q (q_t = a * r_t, acquired-based). Passing a together with q double-counts activation."""
    if a is not None and q is not None:
        raise ValueError("activation already inside q_t; passing a and q double-counts activation")
    if c_month is None:
        return None
    if q is not None:
        return [qt * c_month for qt in q]
    if a is None or r is None:
        return None
    return [a * rt * c_month for rt in r]


def payback_month(c_month, cac, a, churn):
    if _n(c_month, cac, a, churn):
        return None
    flows = contribution_per_acquired(c_month, a=a, r=retention_given_activated(churn))
    cum = 0.0
    for t, f in enumerate(flows, start=1):
        cum += f
        if cum >= cac:
            return float(t)
    return "never"


# ---------------- model ----------------
CONCEPTS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08"]


def compute(v):
    o = {}
    L = div(mul(v["wage_jpy_per_hour"], v["load_factor"]), 60.0)
    o["labor_jpy_per_min"] = L
    o["llm_jpy_per_request"] = mul(add(mul(div(v["llm_in_tokens_per_request"], 1e6), v["llm_price_in_usd_per_mtok"]),
                                       mul(div(v["llm_out_tokens_per_request"], 1e6), v["llm_price_out_usd_per_mtok"])), v["fx_jpy_per_usd"])
    B, A = v["share_route_B"], v["share_route_A"]
    H = None if _n(A, B) else 1.0 - A - B
    o["share_route_human"] = H
    fr = mul(v["provider_failure_rate"], v["repeat_contacts_per_failure"])  # rework multiplier on minutes
    o["rework_multiplier"] = None if fr is None else 1.0 + fr

    # Demand and the paradox (requests per user-year)
    f1 = mul(v["subs_stock_per_user"], v["unwanted_share"], v["help_needed_share"])            # year-1 backlog
    fss = mul(v["new_subs_per_user_year"], v["unwanted_share"], v["help_needed_share"])        # steady state
    o["requests_year1_per_user"] = f1
    o["requests_steady_per_user_year"] = fss
    o["paradox_steady_over_year1"] = div(fss, f1)
    savings_per_cancel = mul(v["monthly_price_cancelled_sub_jpy"], v["months_saved_per_cancellation"])
    o["savings_per_cancellation_jpy"] = savings_per_cancel
    o["user_savings_steady_per_year_jpy"] = mul(fss, savings_per_cancel)
    sub_rev_year = mul(v["sub_price_jpy_month"], 12.0)
    o["sub_price_per_helped_cancellation_steady_jpy"] = div(sub_rev_year, fss)
    o["user_net_value_steady_c05_jpy"] = sub(o["user_savings_steady_per_year_jpy"], sub_rev_year)
    o["max_sub_price_justified_by_cancellation_savings_jpy_month"] = div(o["user_savings_steady_per_year_jpy"], 12.0)
    unv = o["user_net_value_steady_c05_jpy"]
    o["paradox_flag_subscription_not_justified_by_cancellations"] = None if unv is None else (1.0 if unv < 0 else 0.0)

    # Per-request costs
    hs_cost = mul(v["handoff_support_min"], L)
    human_cost = add(mul(v["human_min_per_request"], L), v["phone_cost_jpy_per_human_request"])
    fraud = mul(v["fraud_identity_min_per_request"], L)
    llm = o["llm_jpy_per_request"]
    rw = o["rework_multiplier"]
    o["c03_cost_per_request"] = add(mul(v["handoff_support_min"], L, rw), llm, fraud)
    o["c04_cost_per_request"] = add(mul(B, hs_cost, rw), mul(H, mul(v["human_min_per_request"], L), rw), mul(H, v["phone_cost_jpy_per_human_request"]), llm, fraud)
    o["c05_cost_per_request"] = add(o["c04_cost_per_request"], v["verification_cost_jpy_per_request"])

    pf = v["payment_fee_rate"]
    net = lambda x: None if _n(x, pf) else x * (1.0 - pf)
    rr = v["refund_rate"]
    infra = v["infra_jpy_per_user_year"]

    # C01 tracker
    rev = net(sub_rev_year)
    o["C01_revenue_per_user_year"] = rev
    o["C01_cost_per_user_year"] = add(infra, mul(rev, rr))
    # C02 guide / deep link
    o["C02_revenue_per_user_year"] = v["guide_revenue_per_user_year"]
    o["C02_cost_per_user_year"] = infra
    # C03 AI-assisted handoff (subscription)
    o["C03_revenue_per_user_year"] = net(sub_rev_year)
    o["C03_cost_per_user_year"] = add(infra, mul(fss, o["c03_cost_per_request"]), mul(o["C03_revenue_per_user_year"], rr))
    # C04 concierge, pay per cancellation
    fee_net = net(v["per_cancel_fee_jpy"])
    o["C04_revenue_per_user_year"] = mul(fss, fee_net)
    o["C04_cost_per_user_year"] = add(infra, mul(fss, o["c04_cost_per_request"]), mul(o["C04_revenue_per_user_year"], rr))
    # C05 subscription + per-cancellation fee with verified-stop guarantee (fee refunded if charge persists)
    o["C05_revenue_per_user_year"] = add(net(sub_rev_year), mul(fss, fee_net, None if v["persist_rate"] is None else 1.0 - v["persist_rate"]))
    o["C05_cost_per_user_year"] = add(infra, mul(fss, o["c05_cost_per_request"]), mul(o["C05_revenue_per_user_year"], rr))
    # C06 negotiation (legal gate L06 unresolved)
    o["C06_revenue_per_user_year"] = net(mul(v["neg_requests_per_user_year"], v["neg_success_rate"], v["neg_annual_savings_jpy"], v["neg_success_fee_share"]))
    o["C06_cost_per_user_year"] = add(mul(v["neg_requests_per_user_year"], v["neg_minutes"], L), mul(o["C06_revenue_per_user_year"], rr))
    # C08 switching / referral
    o["C08_revenue_per_user_year"] = mul(v["switches_per_user_year"], v["referral_jpy_per_switch"])
    o["C08_cost_per_user_year"] = mul(v["switches_per_user_year"], v["switch_handling_min"], L)

    for c in ["C01", "C02", "C03", "C04", "C05", "C06", "C08"]:
        r_, k_ = o[f"{c}_revenue_per_user_year"], o[f"{c}_cost_per_user_year"]
        o[f"{c}_contribution_per_user_year"] = sub(r_, k_)
        cm = div(o[f"{c}_contribution_per_user_year"], 12.0)
        o[f"{c}_ltv36_per_acquired"] = None if cm is None else (
            None if _n(v["activation"], v["monthly_churn"]) else sum(contribution_per_acquired(cm, a=v["activation"], r=retention_given_activated(v["monthly_churn"]))))
        o[f"{c}_payback_month"] = payback_month(cm, v["cac_jpy"], v["activation"], v["monthly_churn"])

    # C07 B2B2C (per partner-year), service delivered as C05 execution
    enrolled, eng = v["partner_enrolled_users"], v["partner_engaged_share"]
    rev7 = mul(enrolled, v["partner_fee_jpy_per_enrolled_month"], 12.0)
    req7 = mul(enrolled, eng, fss)
    fixed7 = div(add(v["partner_integration_jpy"], v["partner_sales_cost_jpy"]), v["partner_amortisation_years"])
    cost7 = add(mul(req7, o["c05_cost_per_request"]), fixed7)
    o["C07_revenue_per_partner_year"] = rev7
    o["C07_cost_per_partner_year"] = cost7
    o["C07_contribution_per_partner_year"] = sub(rev7, cost7)
    per_user_margin = sub(mul(v["partner_fee_jpy_per_enrolled_month"], 12.0), mul(eng, fss, o["c05_cost_per_request"]))
    o["C07_breakeven_enrolled_users"] = (None if per_user_margin is None else
                                         ("never" if per_user_margin <= 0 else div(fixed7, per_user_margin)))
    o["C07_partner_fee_breakeven_jpy_per_enrolled_month_at_assumed_size"] = div(add(div(fixed7, enrolled), mul(eng, fss, o["c05_cost_per_request"])), 12.0)

    # Frontiers
    # C04: max human minutes per human-route request at which a request breaks even (rev = cost)
    num = None if _n(fee_net, B, hs_cost, rw, H, v["phone_cost_jpy_per_human_request"], llm, fraud, L) else (
        fee_net * (1.0 - (rr or 0.0)) - B * hs_cost * rw - H * v["phone_cost_jpy_per_human_request"] - llm - fraud)
    den = None if _n(H, L, rw) else H * L * rw
    o["C04_breakeven_human_minutes"] = div(num, den)
    o["C04_breakeven_feasible"] = None if num is None else (1.0 if num > 0 else 0.0)
    # C05 per-request breakeven (fee part only; subscription treated as covering infra)
    num5 = None if _n(num, v["verification_cost_jpy_per_request"], fee_net, v["persist_rate"]) else (
        num - v["verification_cost_jpy_per_request"] - fee_net * v["persist_rate"])
    o["C05_breakeven_human_minutes_fee_only"] = div(num5, den)
    # Consumer value test: fee as share of savings per cancellation
    o["C04_fee_share_of_savings"] = div(v["per_cancel_fee_jpy"], savings_per_cancel)

    # Bottom-up market per 1M target users (illustration, not an estimate)
    M = 1_000_000.0
    o["mkt_subscription_gmv_per_1M_users_year"] = mul(M, v["monthly_sub_spend_jpy"], 12.0)
    o["mkt_potential_savings_per_1M_users_year"] = mul(M, o["user_savings_steady_per_year_jpy"])
    o["mkt_switching_gmv_per_1M_users_year"] = None  # no evidence for switching GMV per user; unknown, not zero
    paying = mul(M, v["target_penetration"])
    for c in ["C01", "C03", "C04", "C05", "C06", "C08"]:
        o[f"mkt_{c}_startup_revenue_per_1M_users_year"] = mul(paying, o[f"{c}_revenue_per_user_year"])
        o[f"mkt_{c}_startup_contribution_per_1M_users_year"] = mul(paying, o[f"{c}_contribution_per_user_year"])
    return o


OUTPUT_META = {
    # key: (unit, unit_class, concept, flags)
}


def _meta(key):
    if key.startswith("C0") or key.startswith("mkt_C0"):
        concept = key.split("_")[0] if key.startswith("C0") else key.split("_")[1]
    else:
        concept = "shared"
    unit_class = ("flag" if ("flag" in key or "feasible" in key) else
                  "share" if any(s in key for s in ("share", "over_year1", "multiplier")) else
                  "minutes" if "minutes" in key else
                  "months" if "payback" in key else
                  "count" if ("requests" in key or "enrolled" in key) else "jpy")
    unit = {"flag": "1=yes/0=no", "share": "share/ratio", "minutes": "min", "months": "month", "count": "count", "jpy": "JPY"}[unit_class]
    flags = []
    if concept == "C06":
        flags.append("legal_gate_L06_unresolved")
    if concept == "C08":
        flags.append("conflict_of_interest_gaining_provider_pays")
    if concept == "C02":
        flags.append("revenue_unknown_no_source")
    return unit, unit_class, concept, ";".join(flags)


def exact(x):
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    return repr(float(x))


def display(x, unit_class):
    if x is None:
        return "UNKNOWN"
    if isinstance(x, str):
        return x
    if unit_class == "flag":
        return "yes" if x == 1.0 else "no"
    if unit_class == "share":
        return f"{x:.4f}"
    if unit_class in ("minutes", "months", "count"):
        return f"{x:.2f}"
    return f"{x:,.0f}" if abs(x) >= 100 else f"{x:.2f}"


def status_of_output(x, scenario):
    if x is None:
        return "unknown"
    if x == "never":
        return "not_within_horizon"
    return "calculated_observed" if scenario == "observed" else "calculated_illustrative"


def rows():
    out = []
    for i, s in enumerate(SCEN):
        v = scenario_inputs(i)
        for key, desc, unit, uc, status, _val, ev in INPUTS:
            x = v[key]
            st = status if x is not None else ("unknown" if status != "rule" else "rule")
            if i == 0 and status == "assumption":
                st = "unknown (assumption not used in observed)"
            out.append(dict(scenario=s, concept="input", kind="input", variable_id=key, description=desc, unit=unit, unit_class=uc,
                            value_exact=exact(x), value_display=display(x, uc), status=st, flags="", evidence=ev))
        o = compute(v)
        for key, x in o.items():
            unit, uc, concept, flags = _meta(key)
            out.append(dict(scenario=s, concept=concept, kind="output", variable_id=key, description=key.replace("_", " "), unit=unit,
                            unit_class=uc, value_exact=exact(x), value_display=display(x, uc), status=status_of_output(x, s),
                            flags=flags, evidence="computed in model/economics_model.py"))
    return out


FIELDS = ["scenario", "concept", "kind", "variable_id", "description", "unit", "unit_class", "value_exact", "value_display", "status", "flags", "evidence"]


def write(path=os.path.join(ROOT, "06_ECONOMICS_MODEL.csv")):
    rs = rows()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rs:
            w.writerow(r)
    return rs


def headline():
    lines = []
    for i, s in enumerate(SCEN):
        o = compute(scenario_inputs(i))
        lines.append(f"[{s}]")
        for k in ["labor_jpy_per_min", "requests_year1_per_user", "requests_steady_per_user_year", "paradox_steady_over_year1",
                  "savings_per_cancellation_jpy", "sub_price_per_helped_cancellation_steady_jpy", "user_net_value_steady_c05_jpy",
                  "max_sub_price_justified_by_cancellation_savings_jpy_month", "paradox_flag_subscription_not_justified_by_cancellations",
                  "c03_cost_per_request", "c04_cost_per_request", "c05_cost_per_request", "C04_breakeven_human_minutes", "C04_breakeven_feasible",
                  "C05_breakeven_human_minutes_fee_only", "C04_fee_share_of_savings", "C07_partner_fee_breakeven_jpy_per_enrolled_month_at_assumed_size",
                  "mkt_subscription_gmv_per_1M_users_year", "mkt_potential_savings_per_1M_users_year",
                  "mkt_C01_startup_revenue_per_1M_users_year", "mkt_C04_startup_revenue_per_1M_users_year", "mkt_C05_startup_revenue_per_1M_users_year",
                  "mkt_C05_startup_contribution_per_1M_users_year"]:
            lines.append(f"  {k} = {display(o[k], _meta(k)[1])}")
        for c in ["C01", "C02", "C03", "C04", "C05", "C06", "C08"]:
            lines.append(f"  {c}: contribution/user-yr={display(o[c + '_contribution_per_user_year'], 'jpy')} "
                         f"LTV36/acquired={display(o[c + '_ltv36_per_acquired'], 'jpy')} payback={display(o[c + '_payback_month'], 'months')}")
        lines.append(f"  C07: contribution/partner-yr={display(o['C07_contribution_per_partner_year'], 'jpy')} "
                     f"breakeven enrolled={display(o['C07_breakeven_enrolled_users'], 'count')}")
    return "\n".join(lines)


if __name__ == "__main__":
    write()
    print(headline())
