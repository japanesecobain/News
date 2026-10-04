"""CLA economics model: Japan-first commerce agent (tracking, affiliate handoff, subscription, B2B2C).

Reproducible: `python3 economics_model.py` recomputes every output, writes
../04_economics_model.csv and economics_model.xlsx (live Excel formulas), and
prints a reconciliation check between the Python results and the formulas.

All inputs are labelled FACT (sourced, scope-limited) or ASSUMPTION (no source;
reversible). Monetary unit: JPY unless stated. Period: per active user per month
unless stated. Nothing here is a forecast.
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(HERE, "..", "04_economics_model.csv")
OUT_XLSX = os.path.join(HERE, "economics_model.xlsx")

SCEN = ["downside", "base", "upside"]

# (id, key, concept, description, unit, (down, base, up), fact_or_assumption, source_ids, limitation, sensitivity)
INPUTS = [
    ("CLA-V01", "fx", "ALL", "Exchange rate used to convert USD API prices", "JPY per USD", (155, 155, 155), "ASSUMPTION", "CLA-S090", "Search-reported 2026 average ~158; not an official rate", "low"),
    ("CLA-V02", "cpi", "ALL", "Paid cost per app install", "JPY/install", (600, 450, 300), "ASSUMPTION anchored on third-party benchmarks", "CLA-S070;CLA-S071", "Benchmarks are dated (2019 shopping CPI USD 3.59; JP iOS USD 2.63 / Android 1.67) and not category-specific for utilities", "high"),
    ("CLA-V03", "p_signup", "ALL", "Install -> account created", "share", (0.60, 0.70, 0.80), "ASSUMPTION", "", "No JP benchmark found", "medium"),
    ("CLA-V04", "p_perm", "ALL", "Account -> grants inbox access or sets up forwarding", "share", (0.25, 0.40, 0.55), "ASSUMPTION", "CLA-S060", "No permission-conversion benchmark found; Visa JP survey shows distrust of delegation but did not measure inbox connection", "high"),
    ("CLA-V05", "p_ingest", "ALL", "Permission -> at least one order correctly ingested within 7 days", "share", (0.60, 0.75, 0.85), "ASSUMPTION", "CLA-S040;CLA-S041", "Amazon removed item names from confirmation emails (2026-07-08, documented for US; JP applicability unverified)", "high"),
    ("CLA-V06", "p_ret3", "ALL", "Activated user still active in month 3", "share of activated", (0.10, 0.20, 0.35), "ASSUMPTION", "CLA-S072", "Shopping-app benchmark is D30 ~4% of installs in APAC (Adjust); a passive tracker may differ", "high"),
    ("CLA-V07", "churn", "ALL", "Monthly churn of users active after month 3", "share/month", (0.12, 0.08, 0.05), "ASSUMPTION", "", "No source", "high"),
    ("CLA-V08", "horizon", "ALL", "Maximum lifetime counted (no perpetual LTV)", "months", (36, 36, 36), "ASSUMPTION", "", "Cap chosen to avoid perpetual LTV", "low"),
    ("CLA-V09", "orders", "ALL", "Physical-goods online orders per active user", "orders/month", (3, 4, 6), "ASSUMPTION", "CLA-S020", "MIC: JPY 47,300/month per net-shopping household (2025, 2+ person households, includes services); order count not published in sources found", "high"),
    ("CLA-V10", "emails_per_order", "C01", "Commerce emails per order (confirm, ship, deliver)", "emails/order", (3, 3, 3), "ASSUMPTION", "", "Varies by merchant", "low"),
    ("CLA-V11", "tok_in_email", "C01", "Input tokens per parsed email after HTML stripping", "tokens", (3500, 3000, 2500), "ASSUMPTION", "", "Not measured", "low"),
    ("CLA-V12", "tok_out_email", "C01", "Output tokens per parsed email (structured JSON)", "tokens", (400, 300, 250), "ASSUMPTION", "", "Not measured", "low"),
    ("CLA-V13", "small_in", "C01", "Small-model input price (Claude Haiku 4.5)", "USD per M tokens", (1.0, 1.0, 1.0), "FACT", "CLA-S091", "List price cached 2026-09-25; any comparable small model would do", "low"),
    ("CLA-V14", "small_out", "C01", "Small-model output price (Claude Haiku 4.5)", "USD per M tokens", (5.0, 5.0, 5.0), "FACT", "CLA-S091", "List price cached 2026-09-25", "low"),
    ("CLA-V15", "overhead", "ALL", "Retry / failed-parse / re-validation multiplier on inference", "multiplier", (1.20, 1.15, 1.10), "ASSUMPTION", "", "Not measured", "low"),
    ("CLA-V16", "notif_per_order", "C01", "User notifications per order", "messages/order", (2, 2, 2), "ASSUMPTION", "", "", "low"),
    ("CLA-V17", "line_share", "C01", "Share of notifications sent as paid LINE messages (rest via free push)", "share", (0.50, 0.25, 0.0), "ASSUMPTION", "CLA-S050", "", "medium"),
    ("CLA-V18", "line_cost", "C01", "LINE official account additional message price (<=200k/month)", "JPY/message", (3, 3, 3), "FACT", "CLA-S050", "Effective 2026-10-01 per LY Corp notice (search-reported); plan fees ignored", "low"),
    ("CLA-V19", "hosting", "ALL", "Variable hosting/storage/monitoring", "JPY/active/month", (12, 6, 3), "ASSUMPTION", "", "Not measured", "medium"),
    ("CLA-V20", "support_rate", "ALL", "Support contacts", "contacts/active/month", (0.05, 0.03, 0.015), "ASSUMPTION", "", "", "high"),
    ("CLA-V21", "support_min", "ALL", "Minutes per support contact", "minutes", (12, 8, 6), "ASSUMPTION", "", "", "medium"),
    ("CLA-V22", "labor_min", "ALL", "Fully loaded human cost (paid or replacement cost of founder time)", "JPY/minute", (50, 50, 50), "ASSUMPTION derived from wage postings", "CLA-S073", "Tokyo CS postings JPY 1,650-1,750/hour x ~1.75 load factor ~= JPY 3,000/hour", "medium"),
    ("CLA-V23", "exc_rate", "ALL", "Ingestion/handoff exceptions needing human review", "exceptions/active/month", (0.10, 0.05, 0.02), "ASSUMPTION", "", "Includes mis-matched packages, wrong item, disputed attribution", "high"),
    ("CLA-V24", "exc_min", "ALL", "Minutes per exception", "minutes", (5, 4, 3), "ASSUMPTION", "", "", "medium"),
    ("CLA-V25", "coverage", "C03", "Share of user's orders at merchants with a usable affiliate/handoff path", "share", (0.60, 0.75, 0.85), "ASSUMPTION", "CLA-S030;CLA-S031;CLA-S033", "Amazon/Rakuten/Yahoo have affiliate programs; some retailers have none; Amazon Creators API gated by 10 sales/30 days", "high"),
    ("CLA-V26", "handoff", "C03", "Share of eligible orders started through the agent", "share", (0.05, 0.15, 0.30), "ASSUMPTION", "CLA-S060", "No observed data; Visa JP survey: 27% would not delegate even if accuracy concerns resolved", "very high"),
    ("CLA-V27", "completion", "C03", "Handoff -> user completes purchase on merchant site", "share", (0.50, 0.65, 0.80), "ASSUMPTION", "", "", "high"),
    ("CLA-V28", "attributable", "C03", "Completed purchase -> commission credited (cookie survives, no point-site override, eligible category, not cancelled pre-ship)", "share", (0.50, 0.70, 0.85), "ASSUMPTION", "CLA-S032;CLA-S034", "Last-click attribution; point sites and rebates can overwrite (Honey precedent)", "high"),
    ("CLA-V29", "aov", "C03", "Average order value of agent-referred orders", "JPY/order", (4000, 5000, 6000), "ASSUMPTION", "", "No verified JP AOV for this behaviour", "medium"),
    ("CLA-V30", "comm", "C03", "Blended gross commission rate", "share of order value", (0.02, 0.03, 0.04), "FACT-RANGE (search-reported)", "CLA-S030;CLA-S031", "Rakuten 2-4% by genre; Amazon JP category rates ~2-8% (cap removed 2024-08-07); exact current tables not opened", "high"),
    ("CLA-V31", "clawback", "C03", "Cancellations/returns reversing commission", "share", (0.10, 0.07, 0.05), "ASSUMPTION", "", "", "medium"),
    ("CLA-V32", "passthrough", "C03", "Share of commission returned to the user to compete with point sites/rebates", "share", (0.40, 0.25, 0.10), "ASSUMPTION", "CLA-S035", "Rakuten Rebates (10M registered, 1,000+ stores) sets the user's reference point", "high"),
    ("CLA-V33", "sessions", "C03", "Shopping-assistance sessions", "sessions/active/month", (2, 3, 4), "ASSUMPTION", "", "", "medium"),
    ("CLA-V34", "tok_in_sess", "C03", "Input tokens per session (catalog results + history)", "tokens", (20000, 15000, 12000), "ASSUMPTION", "", "Not measured", "medium"),
    ("CLA-V35", "tok_out_sess", "C03", "Output tokens per session", "tokens", (2000, 1500, 1200), "ASSUMPTION", "", "Not measured", "low"),
    ("CLA-V36", "mid_in", "C03", "Mid-tier model input price (Claude Sonnet 5.5)", "USD per M tokens", (2.0, 2.0, 2.0), "FACT", "CLA-S091", "List price cached 2026-09-25", "low"),
    ("CLA-V37", "mid_out", "C03", "Mid-tier model output price (Claude Sonnet 5.5)", "USD per M tokens", (10.0, 10.0, 10.0), "FACT", "CLA-S091", "List price cached 2026-09-25", "low"),
    ("CLA-V38", "price", "SUB", "Consumer subscription list price", "JPY/month", (480, 480, 480), "ASSUMPTION", "", "No WTP evidence", "high"),
    ("CLA-V39", "store_fee", "SUB", "App-store / billing fee", "share", (0.15, 0.15, 0.15), "ASSUMPTION", "", "Small-business rate assumed; alternative billing may change it", "low"),
    ("CLA-V40", "paid_conv", "SUB", "Active users who pay", "share of actives", (0.02, 0.05, 0.10), "ASSUMPTION", "", "No WTP evidence", "very high"),
    ("CLA-V41", "paid_exc_rate", "SUB", "Human-handled exception cases per paying user (missing parcel, refund chase)", "cases/paid user/month", (0.30, 0.20, 0.10), "ASSUMPTION", "", "", "high"),
    ("CLA-V42", "paid_exc_min", "SUB", "Minutes per paid exception case", "minutes", (20, 15, 10), "ASSUMPTION", "", "", "high"),
    ("CLA-V43", "b2b2c_fee", "C07", "Partner fee per monthly active user", "JPY/MAU/month", (20, 40, 80), "ASSUMPTION", "", "No benchmark found; must be tested with partners", "very high"),
    ("CLA-V44", "partner_support_share", "C07", "Share of support absorbed by partner", "share", (0.5, 0.5, 0.5), "ASSUMPTION", "", "", "medium"),
    ("CLA-V45", "team_fixed", "ALL", "Minimum team at replacement cost (2 engineers + 1 ops/support lead), not in contribution", "JPY/month", (3000000, 3000000, 3000000), "ASSUMPTION", "", "Used only for break-even scale", "medium"),
    ("CLA-V46", "casa_usd", "C01", "Annual Gmail restricted-scope CASA Tier 2 assessment (self-serve lab)", "USD/year", (720, 540, 540), "FACT", "CLA-S011", "TAC Security list prices; excludes engineering remediation time; legacy track cited at USD 15k-75k", "low"),
    ("CLA-V47", "households", "MKT", "Japanese households", "households", (55700000, 55700000, 55700000), "ASSUMPTION (2020 census figure not re-verified in this run)", "", "Verify against latest census/estimates", "low"),
    ("CLA-V48", "netshop_share", "MKT", "Households using net shopping", "share", (0.569, 0.569, 0.569), "FACT (scope: 2+ person households, 2025)", "CLA-S020", "Applied to all households as an approximation", "low"),
    ("CLA-V49", "heavy_share", "MKT", "Net-shopping households that are heavy multi-merchant buyers (>=3 merchants, >=4 orders/month)", "share", (0.05, 0.10, 0.20), "ASSUMPTION", "", "No statistic found", "very high"),
    ("CLA-V50", "adoption", "MKT", "Eligible households reached and retained as actives", "share", (0.01, 0.03, 0.10), "ASSUMPTION", "", "No statistic found", "very high"),
]

# Outputs: (id, key, concept, description, unit, python_fn, excel_template, period)
# Excel template uses {key} placeholders that become cell refs for the scenario column.
OUTPUTS = [
    ("CLA-O01", "cost_per_email", "C01", "Inference cost per parsed commerce email", "JPY/email",
     lambda v: (v["tok_in_email"] * v["small_in"] + v["tok_out_email"] * v["small_out"]) / 1e6 * v["fx"] * v["overhead"],
     "({tok_in_email}*{small_in}+{tok_out_email}*{small_out})/1000000*{fx}*{overhead}"),
    ("CLA-O02", "inf_track", "C01", "Tracking inference cost", "JPY/active/month",
     lambda v: v["orders"] * v["emails_per_order"] * v["cost_per_email"],
     "{orders}*{emails_per_order}*{cost_per_email}"),
    ("CLA-O03", "notif", "C01", "Notification cost", "JPY/active/month",
     lambda v: v["orders"] * v["notif_per_order"] * v["line_share"] * v["line_cost"],
     "{orders}*{notif_per_order}*{line_share}*{line_cost}"),
    ("CLA-O04", "support", "ALL", "Human support cost", "JPY/active/month",
     lambda v: v["support_rate"] * v["support_min"] * v["labor_min"],
     "{support_rate}*{support_min}*{labor_min}"),
    ("CLA-O05", "recovery", "ALL", "Human exception/recovery cost", "JPY/active/month",
     lambda v: v["exc_rate"] * v["exc_min"] * v["labor_min"],
     "{exc_rate}*{exc_min}*{labor_min}"),
    ("CLA-O06", "m1_cost", "C01", "Tracking-only variable cost", "JPY/active/month",
     lambda v: v["inf_track"] + v["notif"] + v["hosting"] + v["support"] + v["recovery"],
     "{inf_track}+{notif}+{hosting}+{support}+{recovery}"),
    ("CLA-O07", "m1_contrib", "C01", "Tracking-only contribution (no revenue; past orders are not attributable)", "JPY/active/month",
     lambda v: -v["m1_cost"], "-{m1_cost}"),
    ("CLA-O08", "attr_orders", "C03", "Successful attributable orders", "orders/active/month",
     lambda v: v["orders"] * v["coverage"] * v["handoff"] * v["completion"] * v["attributable"],
     "{orders}*{coverage}*{handoff}*{completion}*{attributable}"),
    ("CLA-O09", "net_rev_order", "C03", "Net realised revenue per attributable order (after clawback and pass-through, each applied once)", "JPY/order",
     lambda v: v["aov"] * v["comm"] * (1 - v["clawback"]) * (1 - v["passthrough"]),
     "{aov}*{comm}*(1-{clawback})*(1-{passthrough})"),
    ("CLA-O10", "m2_rev", "C03", "Affiliate revenue", "JPY/active/month",
     lambda v: v["attr_orders"] * v["net_rev_order"], "{attr_orders}*{net_rev_order}"),
    ("CLA-O11", "cost_per_session", "C03", "Inference cost per shopping session", "JPY/session",
     lambda v: (v["tok_in_sess"] * v["mid_in"] + v["tok_out_sess"] * v["mid_out"]) / 1e6 * v["fx"] * v["overhead"],
     "({tok_in_sess}*{mid_in}+{tok_out_sess}*{mid_out})/1000000*{fx}*{overhead}"),
    ("CLA-O12", "inf_shop", "C03", "Shopping-session inference cost", "JPY/active/month",
     lambda v: v["sessions"] * v["cost_per_session"], "{sessions}*{cost_per_session}"),
    ("CLA-O13", "m2_cost", "C03", "Affiliate-handoff assistant variable cost", "JPY/active/month",
     lambda v: v["inf_shop"] + v["hosting"] + v["support"] + v["recovery"],
     "{inf_shop}+{hosting}+{support}+{recovery}"),
    ("CLA-O14", "m2_contrib", "C03", "Affiliate-handoff assistant contribution", "JPY/active/month",
     lambda v: v["m2_rev"] - v["m2_cost"], "{m2_rev}-{m2_cost}"),
    ("CLA-O15", "combo_contrib", "C01+C03", "Tracking + handoff combined contribution (shared hosting/support counted once)", "JPY/active/month",
     lambda v: v["m2_rev"] - (v["m1_cost"] + v["inf_shop"]), "{m2_rev}-({m1_cost}+{inf_shop})"),
    ("CLA-O16", "net_price", "SUB", "Net subscription revenue per payer", "JPY/payer/month",
     lambda v: v["price"] * (1 - v["store_fee"]), "{price}*(1-{store_fee})"),
    ("CLA-O17", "paid_exc_cost", "SUB", "Human exception handling cost per payer", "JPY/payer/month",
     lambda v: v["paid_exc_rate"] * v["paid_exc_min"] * v["labor_min"], "{paid_exc_rate}*{paid_exc_min}*{labor_min}"),
    ("CLA-O18", "m3_contrib", "SUB", "Freemium subscription contribution (all actives incur tracking cost)", "JPY/active/month",
     lambda v: v["paid_conv"] * (v["net_price"] - v["paid_exc_cost"]) - v["m1_cost"],
     "{paid_conv}*({net_price}-{paid_exc_cost})-{m1_cost}"),
    ("CLA-O19", "m4_cost", "C07", "B2B2C variable cost (no notification cost; partner absorbs part of support)", "JPY/MAU/month",
     lambda v: v["inf_track"] + v["hosting"] + v["support"] * (1 - v["partner_support_share"]) + v["recovery"],
     "{inf_track}+{hosting}+{support}*(1-{partner_support_share})+{recovery}"),
    ("CLA-O20", "m4_contrib", "C07", "B2B2C contribution", "JPY/MAU/month",
     lambda v: v["b2b2c_fee"] - v["m4_cost"], "{b2b2c_fee}-{m4_cost}"),
    ("CLA-O21", "act_rate", "ALL", "Activated users per install", "share",
     lambda v: v["p_signup"] * v["p_perm"] * v["p_ingest"], "{p_signup}*{p_perm}*{p_ingest}"),
    ("CLA-O22", "cac_act", "ALL", "Paid acquisition cost per activated user", "JPY/activated user",
     lambda v: v["cpi"] / v["act_rate"], "{cpi}/{act_rate}"),
    ("CLA-O23", "cac_ret", "ALL", "Paid acquisition cost per user still active in month 3", "JPY/retained user",
     lambda v: v["cac_act"] / v["p_ret3"], "{cac_act}/{p_ret3}"),
    ("CLA-O24", "tail_months", "ALL", "Expected active months from month 3 for a retained user (capped)", "months",
     lambda v: (1 - (1 - v["churn"]) ** (v["horizon"] - 2)) / v["churn"], "(1-(1-{churn})^({horizon}-2))/{churn}"),
    ("CLA-O25", "act_months", "ALL", "Expected active months per activated user (m1=1, m2 interpolated, m3+ retained tail)", "months",
     lambda v: 1 + (1 + v["p_ret3"]) / 2 + v["p_ret3"] * v["tail_months"], "1+(1+{p_ret3})/2+{p_ret3}*{tail_months}"),
    ("CLA-O26", "val_act_m2", "C03", "Contribution per activated user over lifetime (affiliate)", "JPY/activated user",
     lambda v: v["m2_contrib"] * v["act_months"], "{m2_contrib}*{act_months}"),
    ("CLA-O27", "val_act_m3", "SUB", "Contribution per activated user over lifetime (subscription)", "JPY/activated user",
     lambda v: v["m3_contrib"] * v["act_months"], "{m3_contrib}*{act_months}"),
    ("CLA-O28", "val_act_combo", "C01+C03", "Contribution per activated user over lifetime (tracking+handoff)", "JPY/activated user",
     lambda v: v["combo_contrib"] * v["act_months"], "{combo_contrib}*{act_months}"),
    ("CLA-O29", "max_cpi_m2", "C03", "Maximum sustainable paid cost per install (affiliate), floor 0", "JPY/install",
     lambda v: max(0.0, v["val_act_m2"] * v["act_rate"]), "MAX(0,{val_act_m2}*{act_rate})"),
    ("CLA-O30", "max_cpi_m3", "SUB", "Maximum sustainable paid cost per install (subscription), floor 0", "JPY/install",
     lambda v: max(0.0, v["val_act_m3"] * v["act_rate"]), "MAX(0,{val_act_m3}*{act_rate})"),
    ("CLA-O31", "max_cpi_combo", "C01+C03", "Maximum sustainable paid cost per install (tracking+handoff), floor 0", "JPY/install",
     lambda v: max(0.0, v["val_act_combo"] * v["act_rate"]), "MAX(0,{val_act_combo}*{act_rate})"),
    # Frontiers (solved analytically; other inputs held at the scenario values)
    ("CLA-F01", "f_min_handoff", "C03", "FRONTIER: minimum handoff share for affiliate contribution >= 0", "share",
     lambda v: v["m2_cost"] / (v["orders"] * v["coverage"] * v["completion"] * v["attributable"] * v["net_rev_order"]),
     "{m2_cost}/({orders}*{coverage}*{completion}*{attributable}*{net_rev_order})"),
    ("CLA-F02", "f_min_attr_orders", "C03", "FRONTIER: minimum attributable orders per active for affiliate contribution >= 0", "orders/active/month",
     lambda v: v["m2_cost"] / v["net_rev_order"], "{m2_cost}/{net_rev_order}"),
    ("CLA-F03", "f_min_coverage", "C03", "FRONTIER: minimum eligible merchant coverage for affiliate contribution >= 0 (>1 = impossible)", "share",
     lambda v: (v["m2_cost"] / (v["orders"] * v["handoff"] * v["completion"] * v["attributable"] * v["net_rev_order"])) if v["handoff"] > 0 else None,
     "{m2_cost}/({orders}*{handoff}*{completion}*{attributable}*{net_rev_order})"),
    ("CLA-F04", "f_max_human_min", "C03", "FRONTIER: maximum human minutes per active per month before affiliate contribution < 0 (negative = none affordable)", "minutes/active/month",
     lambda v: (v["m2_rev"] - v["inf_shop"] - v["hosting"]) / v["labor_min"], "({m2_rev}-{inf_shop}-{hosting})/{labor_min}"),
    ("CLA-F05", "f_max_human_min_per_order", "C03", "FRONTIER: maximum human minutes per attributable order", "minutes/order",
     lambda v: ((v["m2_rev"] - v["inf_shop"] - v["hosting"]) / v["labor_min"] / v["attr_orders"]) if v["attr_orders"] > 0 else None, "({m2_rev}-{inf_shop}-{hosting})/{labor_min}/{attr_orders}"),
    ("CLA-F06", "f_min_handoff_cac", "C03", "FRONTIER: minimum handoff share to recover paid CAC within the capped lifetime", "share",
     lambda v: (v["cac_act"] / v["act_months"] + v["m2_cost"]) / (v["orders"] * v["coverage"] * v["completion"] * v["attributable"] * v["net_rev_order"]),
     "({cac_act}/{act_months}+{m2_cost})/({orders}*{coverage}*{completion}*{attributable}*{net_rev_order})"),
    ("CLA-F07", "f_min_paid_conv", "SUB", "FRONTIER: minimum paid conversion for subscription contribution >= 0", "share of actives",
     lambda v: v["m1_cost"] / (v["net_price"] - v["paid_exc_cost"]), "{m1_cost}/({net_price}-{paid_exc_cost})"),
    ("CLA-F08", "f_min_paid_conv_cac", "SUB", "FRONTIER: minimum paid conversion to recover paid CAC within the capped lifetime", "share of actives",
     lambda v: (v["cac_act"] / v["act_months"] + v["m1_cost"]) / (v["net_price"] - v["paid_exc_cost"]),
     "({cac_act}/{act_months}+{m1_cost})/({net_price}-{paid_exc_cost})"),
    ("CLA-F09", "f_min_b2b2c_fee", "C07", "FRONTIER: minimum partner fee per MAU for B2B2C contribution >= 0", "JPY/MAU/month",
     lambda v: v["m4_cost"], "{m4_cost}"),
    ("CLA-F10", "f_actives_fixed_m2", "C03", "Actives needed for affiliate contribution to cover the minimum team (blank if contribution <= 0)", "active users",
     lambda v: v["team_fixed"] / v["m2_contrib"] if v["m2_contrib"] > 0 else None,
     'IF({m2_contrib}>0,{team_fixed}/{m2_contrib},"n/a")'),
    ("CLA-F11", "f_actives_fixed_m4", "C07", "MAUs needed for B2B2C contribution to cover the minimum team (blank if contribution <= 0)", "MAU",
     lambda v: v["team_fixed"] / v["m4_contrib"] if v["m4_contrib"] > 0 else None,
     'IF({m4_contrib}>0,{team_fixed}/{m4_contrib},"n/a")'),
    # Market sizing (software revenue, not GMV)
    ("CLA-M01", "eligible_hh", "MKT", "Eligible heavy multi-merchant households", "households",
     lambda v: v["households"] * v["netshop_share"] * v["heavy_share"], "{households}*{netshop_share}*{heavy_share}"),
    ("CLA-M02", "active_hh", "MKT", "Retained active households", "households",
     lambda v: v["eligible_hh"] * v["adoption"], "{eligible_hh}*{adoption}"),
    ("CLA-M03", "annual_rev_m2", "MKT", "Annual affiliate revenue (one active per household)", "JPY/year",
     lambda v: v["active_hh"] * v["m2_rev"] * 12, "{active_hh}*{m2_rev}*12"),
    ("CLA-M04", "annual_contrib_m2", "MKT", "Annual affiliate contribution before fixed costs and CAC", "JPY/year",
     lambda v: v["active_hh"] * v["m2_contrib"] * 12, "{active_hh}*{m2_contrib}*12"),
    ("CLA-M05", "annual_rev_m3", "MKT", "Annual subscription revenue", "JPY/year",
     lambda v: v["active_hh"] * v["paid_conv"] * v["net_price"] * 12, "{active_hh}*{paid_conv}*{net_price}*12"),
]


def compute(values):
    v = dict(values)
    for _id, key, _c, _d, _u, fn, _x in OUTPUTS:
        v[key] = fn(v)
    return v


def scenario_inputs(idx):
    return {key: vals[idx] for (_id, key, _c, _d, _u, vals, *_rest) in INPUTS}


def payback_months(v, contrib_key):
    """Months until cumulative contribution per activated user >= CAC per activated user (None if never within horizon)."""
    c = v[contrib_key]
    if c <= 0:
        return None
    cum = 0.0
    for m in range(1, int(v["horizon"]) + 1):
        if m == 1:
            alive = 1.0
        elif m == 2:
            alive = (1 + v["p_ret3"]) / 2
        else:
            alive = v["p_ret3"] * (1 - v["churn"]) ** (m - 3)
        cum += c * alive
        if cum >= v["cac_act"]:
            return m
    return None


def sensitivity(base_v, down_v, up_v, output_key):
    """One-at-a-time: move each input to its downside and upside value, holding others at base."""
    rows = []
    for (_id, key, concept, desc, unit, vals, *_r) in INPUTS:
        if vals[0] == vals[2]:
            continue
        lo = dict(base_v); lo[key] = vals[0]
        hi = dict(base_v); hi[key] = vals[2]
        r_lo = compute(lo)[output_key]
        r_hi = compute(hi)[output_key]
        rows.append((_id, key, vals[0], vals[2], r_lo, r_hi, abs(r_hi - r_lo)))
    rows.sort(key=lambda r: -r[6])
    return rows


def fmt(x):
    if x is None:
        return ""
    if isinstance(x, float):
        if abs(x) >= 1000:
            return f"{x:.0f}"
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def main():
    results = {s: compute(scenario_inputs(i)) for i, s in enumerate(SCEN)}
    for s in SCEN:
        v = results[s]
        v["payback_m2"] = payback_months(v, "m2_contrib")
        v["payback_m3"] = payback_months(v, "m3_contrib")
        v["payback_combo"] = payback_months(v, "combo_contrib")

    rows = []
    header = ["concept_id", "scenario", "variable_id", "input_or_output", "description", "value", "unit", "period",
              "formula_or_dependency", "fact_or_assumption", "source_ids", "sensitivity", "limitation"]
    for i, s in enumerate(SCEN):
        for (vid, key, concept, desc, unit, vals, fa, src, lim, sens) in INPUTS:
            rows.append([concept, s, vid, "input", f"{key}: {desc}", fmt(vals[i]), unit, "per month unless unit says otherwise",
                         "", fa, src, sens, lim])
        for (oid, key, concept, desc, unit, _fn, xl) in OUTPUTS:
            rows.append([concept, s, oid, "output", f"{key}: {desc}", fmt(results[s][key]), unit, "per month unless unit says otherwise",
                         xl.replace("{", "").replace("}", ""), "CALCULATION", "", "", "Inherits all input limitations"])
        for pid, key, concept, desc in [("CLA-P01", "payback_m2", "C03", "Payback month of paid CAC per activated user (affiliate); blank = not within 36 months or contribution <= 0"),
                                        ("CLA-P02", "payback_m3", "SUB", "Payback month of paid CAC per activated user (subscription); blank = never"),
                                        ("CLA-P03", "payback_combo", "C01+C03", "Payback month of paid CAC per activated user (tracking+handoff); blank = never")]:
            rows.append([concept, s, pid, "output", f"{key}: {desc}", fmt(results[s][key]), "month", "cohort",
                         "monthly simulation in economics_model.py: payback_months()", "CALCULATION", "", "", "Survival curve is an assumption"])

    # Sensitivity rows (affiliate contribution, base)
    base_v = scenario_inputs(1)
    for (vid, key, lo, hi, r_lo, r_hi, swing) in sensitivity(base_v, scenario_inputs(0), scenario_inputs(2), "m2_contrib"):
        rows.append(["C03", "sensitivity(base)", vid, "output",
                     f"m2_contrib when {key} moves {fmt(lo)} -> {fmt(hi)} (others at base)",
                     f"{fmt(r_lo)} -> {fmt(r_hi)}", "JPY/active/month", "per month", "one-at-a-time recompute", "CALCULATION", "", f"swing {fmt(swing)}", ""])
    for (vid, key, lo, hi, r_lo, r_hi, swing) in sensitivity(base_v, scenario_inputs(0), scenario_inputs(2), "m3_contrib"):
        rows.append(["SUB", "sensitivity(base)", vid, "output",
                     f"m3_contrib when {key} moves {fmt(lo)} -> {fmt(hi)} (others at base)",
                     f"{fmt(r_lo)} -> {fmt(r_hi)}", "JPY/active/month", "per month", "one-at-a-time recompute", "CALCULATION", "", f"swing {fmt(swing)}", ""])

    # Bridge test: tracking users who never delegate (handoff = 0) at base
    nd = dict(base_v); nd["handoff"] = 0.0
    nd_v = compute(nd)
    rows.append(["C01+C03", "base, handoff=0", "CLA-B01", "output",
                 "combo_contrib when tracking users never delegate a purchase (handoff share = 0)",
                 fmt(nd_v["combo_contrib"]), "JPY/active/month", "per month", "m2_rev(handoff=0) - (m1_cost + inf_shop)", "CALCULATION", "", "", "Assumes they still open shopping sessions; without sessions = m1_contrib"])

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    # Console summary
    keys = ["cost_per_email", "inf_track", "m1_cost", "m1_contrib", "attr_orders", "net_rev_order", "m2_rev", "inf_shop", "m2_cost",
            "m2_contrib", "combo_contrib", "m3_contrib", "m4_cost", "m4_contrib", "act_rate", "cac_act", "cac_ret", "act_months",
            "max_cpi_m2", "max_cpi_m3", "max_cpi_combo", "f_min_handoff", "f_min_attr_orders", "f_min_coverage", "f_max_human_min",
            "f_max_human_min_per_order", "f_min_handoff_cac", "f_min_paid_conv", "f_min_paid_conv_cac", "f_min_b2b2c_fee",
            "f_actives_fixed_m2", "f_actives_fixed_m4", "eligible_hh", "active_hh", "annual_rev_m2", "annual_contrib_m2", "annual_rev_m3",
            "payback_m2", "payback_m3", "payback_combo"]
    print(f"{'key':28s}" + "".join(f"{s:>16s}" for s in SCEN))
    for k in keys:
        print(f"{k:28s}" + "".join(f"{fmt(results[s][k]):>16s}" for s in SCEN))
    print("bridge (handoff=0) combo_contrib base:", fmt(nd_v["combo_contrib"]))
    print("\nTop sensitivities for m2_contrib (base):")
    for r in sensitivity(base_v, None, None, "m2_contrib")[:8]:
        print("  ", r[1], fmt(r[4]), "->", fmt(r[5]))
    print("\nTop sensitivities for m3_contrib (base):")
    for r in sensitivity(base_v, None, None, "m3_contrib")[:6]:
        print("  ", r[1], fmt(r[4]), "->", fmt(r[5]))

    write_xlsx()
    return results


def write_xlsx():
    try:
        import openpyxl
        from openpyxl.styles import Font
    except ImportError:
        print("openpyxl not installed; skipping xlsx")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inputs"
    ws.append(["variable_id", "key", "concept", "description", "unit", "downside", "base", "upside", "fact_or_assumption", "source_ids", "limitation"])
    for c in ws[1]:
        c.font = Font(bold=True)
    row_of = {}
    for r, (vid, key, concept, desc, unit, vals, fa, src, lim, sens) in enumerate(INPUTS, start=2):
        ws.append([vid, key, concept, desc, unit, vals[0], vals[1], vals[2], fa, src, lim])
        row_of[key] = ("Inputs", r)
    cs = wb.create_sheet("Calc")
    cs.append(["output_id", "key", "concept", "description", "unit", "downside", "base", "upside", "formula"])
    for c in cs[1]:
        c.font = Font(bold=True)
    col = {"downside": "F", "base": "G", "upside": "H"}
    for r, (oid, key, concept, desc, unit, _fn, xl) in enumerate(OUTPUTS, start=2):
        row_of[key] = ("Calc", r)
    for r, (oid, key, concept, desc, unit, _fn, xl) in enumerate(OUTPUTS, start=2):
        cells = []
        for s in SCEN:
            expr = xl
            for k, (sheet, rr) in sorted(row_of.items(), key=lambda kv: -len(kv[0])):
                ref = f"{sheet}!{col[s]}{rr}" if sheet == "Inputs" else f"{col[s]}{rr}"
                expr = expr.replace("{" + k + "}", ref)
            cells.append("=" + expr)
        cs.append([oid, key, concept, desc, unit] + cells + [xl.replace("{", "").replace("}", "")])
    for sheet in (ws, cs):
        for column, width in zip("ABCDEFGHIJK", (11, 18, 9, 70, 22, 13, 13, 13, 30, 22, 50)):
            sheet.column_dimensions[column].width = width
    wb.save(OUT_XLSX)
    print("wrote", OUT_XLSX)


if __name__ == "__main__":
    main()
