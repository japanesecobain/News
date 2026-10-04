"""Reproduce the reviewer's two Grok v2 findings from the SUPPLIED Grok file, then write a repaired derivative.

Inputs (read-only): ../00_inputs_supplied/GRO_v2/GRO_04_economics_model_v2.csv, GRO_05_hypothesis_register_v2.csv
Not supplied to CLA: Grok v1 CSVs, calculate_r003_v2.py, the reviewer's audit JSON, R003_v2_addendum,
06/07 v2 files. The v1 base inputs used below (4, 0.25, 0.05, 0.60, 0.40; net JPY 80/order) are the
reviewer-stated values, cross-checked only against the rows that ARE in the supplied v2 file.
Outputs: QA_grok_v2.txt (this folder); ../03_derivatives/GRO-D01_economics_model_v2_repaired.csv
"""
import csv
import datetime
import os
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
SUP = os.path.join(HERE, "..", "00_inputs_supplied", "GRO_v2")
DER = os.path.join(HERE, "..", "03_derivatives")


def money2(x):
    """Two-decimal display rounding (the formatter the reviewer reports was applied to counts)."""
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    rows = list(csv.DictReader(open(os.path.join(SUP, "GRO_04_economics_model_v2.csv"), encoding="utf-8")))
    get = {(r["concept_id"], r["scenario"], r["variable_id"]): r for r in rows}
    log = [f"run_at_utc: {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}",
           "scope: supplied GRO_04_economics_model_v2.csv only; calculate_r003_v2.py and audit JSON NOT supplied, so the reviewer's 29-check run was not reproduced"]

    # ---- Finding 1: precision defect -------------------------------------------------------
    b = {k: Decimal(get[("C02", "v1_base", k)]["value"]) for k in ("attempts", "failed_attempts", "attributable_orders", "affiliate_revenue_if_payable", "contribution_if_revenue_payable_and_support_is_30")}
    success = (b["attempts"] - b["failed_attempts"]) / b["attempts"]          # 0.6, implied by exported rows
    exact_attr = Decimal("4") * Decimal("0.25") * Decimal("0.05") * Decimal("0.60") * Decimal("0.40")  # reviewer-stated v1 inputs
    net_per_order = Decimal("80")                                            # reviewer-stated
    log.append(f"[F1] exported attempts={b['attempts']} failed={b['failed_attempts']} -> implied execution success {success} (matches reviewer-stated 0.60)")
    log.append(f"[F1] exact attributable orders from reviewer-stated inputs = {exact_attr}; exported = {b['attributable_orders']}; 2-dp display of exact = {money2(exact_attr)}")
    log.append(f"[F1] exact x 80 = {exact_attr * net_per_order} (exported revenue {b['affiliate_revenue_if_payable']}); exported count x 80 = {b['attributable_orders'] * net_per_order}")
    log.append(f"[F1] revenue / exported count implies JPY {b['affiliate_revenue_if_payable'] / b['attributable_orders']} per order, inconsistent with 80 -> the saved table does not reconcile")
    log.append(f"[F1] headline contribution {b['contribution_if_revenue_payable_and_support_is_30']} = exact revenue 0.96 - 30 -> in-memory headline correct; defect is interchange/QA, not new economics")
    f1 = (b["attributable_orders"] == money2(exact_attr)) and (exact_attr * net_per_order == b["affiliate_revenue_if_payable"]) and (b["attributable_orders"] * net_per_order != b["affiliate_revenue_if_payable"])
    log.append(f"[F1] REPRODUCED: {f1}")
    u = {k: Decimal(get[("C02", "v1_upside", k)]["value"]) for k in ("attempts", "failed_attempts", "attributable_orders", "affiliate_revenue_if_payable")}
    log.append(f"[F1] upside rows reconcile exactly: attributable {u['attributable_orders']} = attempts x success(0.8) x share(0.7) -> {u['attempts'] * Decimal('0.8') * Decimal('0.7')}; revenue/order = {u['affiliate_revenue_if_payable'] / u['attributable_orders']}")

    # ---- Finding 2: cohort double count ----------------------------------------------------
    act = get[("C02", "cohort", "activation_rate")]
    ret = get[("C02", "cohort", "retained_fraction_by_month")]
    pay = get[("C02", "cohort", "simple_cac_over_active_contribution")]
    ret_is_acquired_based = "acquired" in (ret["description"] + ret["denominator"]).lower()
    formula_multiplies_activation = "activation x retained fraction" in pay["limitation"].lower()
    f2 = ret_is_acquired_based and formula_multiplies_activation
    log.append(f"[F2] retained_fraction_by_month denominator='{ret['denominator']}', description='{ret['description']}'")
    log.append(f"[F2] payback row states: '{pay['limitation']}'")
    log.append(f"[F2] REPRODUCED (activation would be applied twice once inputs are filled): {f2}; inputs currently blank so no numeric payback is wrong yet")

    # ---- Finding 3: H02 status scope -------------------------------------------------------
    hyp = {r["hypothesis_id"]: r for r in csv.DictReader(open(os.path.join(SUP, "GRO_05_hypothesis_register_v2.csv"), encoding="utf-8"))}
    h2 = hyp["H02"]
    log.append(f"[F3] H02 text tests adequacy ('{h2['hypothesis'][:60]}...') but evidence_status='{h2['evidence_status']}' rests on closed_scope='{h2['closed_scope'][:70]}...' -> split into H02a/H02b in CLA-D01")

    with open(os.path.join(HERE, "QA_grok_v2.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))

    # ---- Repaired derivative ---------------------------------------------------------------
    out = os.path.join(DER, "GRO-D01_economics_model_v2_repaired.csv")
    hdr = list(rows[0].keys()) + ["value_exact", "value_display", "permission_status", "applicability_status", "underwriting_treatment", "commercial_amount", "repair_note"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        for r in rows:
            key = (r["concept_id"], r["scenario"], r["variable_id"])
            exact, note = r["value"], ""
            perm = appl = under = comm = ""
            if key == ("C02", "v1_base", "attributable_orders"):
                exact = str(exact_attr.normalize())
                note = "REPAIR: exact 0.012 from reviewer-stated v1 inputs (4 x 0.25 x 0.05 x 0.60 x 0.40); consistent with exported revenue 0.96 at JPY 80/order. 0.01 was a 2-dp display value saved as data."
            if key == ("C02", "cohort", "retained_fraction_by_month"):
                r = dict(r)
                r["variable_id"] = "retention_given_activated_by_month"
                r["description"] = "r_t = P(active in month t | activated). Used as a x r_t x c_t with activation_rate a applied exactly once."
                r["denominator"] = "activated_cohort"
                note = "REPAIR: renamed and re-based on the activated cohort so activation appears once. Alternative convention q_t = P(active at t | acquired) must then NOT be multiplied by activation. Still blank (unknown)."
            if key == ("C02", "cohort", "simple_cac_over_active_contribution"):
                r = dict(r)
                r["limitation"] = "Cohort month-t contribution per acquired user = a x r_t x c_t (or q_t x c_t). Never a x q_t. Both rates blank."
                note = "REPAIR: formula text corrected; value retained only as an identity, not a payback."
            if r["concept_id"] == "GATE":
                if r["scenario"] == "delegated_amazon_execution":
                    perm, appl, under, comm = ("adverse clause in retrieved English text (6(k), on-behalf orders)", "Japanese operating agreement unreconciled", "exclude from current investment case", "unknown (not an observed universal zero)")
                elif r["scenario"] == "comparison_then_user_click":
                    perm, appl, under, comm = ("unresolved by program and surface; Rakuten restricts closed/one-to-one tools except approved corporate partners (search extract)", "unresolved", "exclude until program x surface approval is confirmed", "unknown")
                elif r["scenario"] == "passive_tracking":
                    perm, appl, under, comm = ("n/a", "n/a", "not a commissionable event", "0 by program rule (no qualifying click) - distinct from unknown")
            disp = r["value"] if key != ("C02", "v1_base", "attributable_orders") else "0.01"
            w.writerow([r[k] for k in rows[0].keys()] + [exact, disp, perm, appl, under, comm, note])
    print("wrote", os.path.relpath(out, HERE))


if __name__ == "__main__":
    main()
