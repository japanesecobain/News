"""Tests for model/economics_model.py: round trip, unknown propagation, rule zeros, activation counted once,
single labour price, breakeven algebra, the paradox, display isolation and gating flags.

Run: python3 model/test_economics.py   (writes ../12_QA_economics_tests.txt; exit 1 on any failure)
These prove arithmetic and labelling discipline only. They do NOT show any configuration is permitted,
wanted or profitable.
"""
import csv
import datetime
import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("em", os.path.join(HERE, "economics_model.py"))
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

TOL = {"jpy": (1e-12, 1e-9), "share": (0.0, 1e-12), "count": (1e-12, 1e-12), "minutes": (1e-12, 1e-9), "months": (0.0, 0.0),
       "tokens": (0.0, 0.0), "usd": (1e-12, 0.0), "ratio": (1e-12, 0.0), "flag": (0.0, 0.0)}
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))


def parse(s):
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return s


def close(a, b, uc):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    rel, ab = TOL[uc]
    return math.isclose(a, b, rel_tol=rel, abs_tol=ab) if (rel or ab) else a == b


def main():
    tmp = os.path.join(HERE, "_rt_econ.csv")
    E.write(tmp)
    rows = list(csv.DictReader(open(tmp, encoding="utf-8")))
    os.remove(tmp)

    # 1. Round trip: recompute every output from re-imported exported inputs
    n = bad = 0
    mism = []
    for i, s in enumerate(E.SCEN):
        v = {r["variable_id"]: parse(r["value_exact"]) for r in rows if r["scenario"] == s and r["kind"] == "input"}
        rec = E.compute(v)
        for r in rows:
            if r["scenario"] != s or r["kind"] != "output":
                continue
            n += 1
            if not close(rec[r["variable_id"]], parse(r["value_exact"]), r["unit_class"]):
                bad += 1
                mism.append((s, r["variable_id"]))
    check("roundtrip: every exported output is reproduced from re-imported exported inputs", bad == 0, f"{n} outputs, {bad} mismatches {mism[:3]}")

    # 2. Display isolation: value_exact equals the in-memory value bit-for-bit for every numeric output, and
    #    rounding in value_display is lossy for at least some outputs (so the display column cannot be data).
    mem = {s: E.compute(E.scenario_inputs(i)) for i, s in enumerate(E.SCEN)}
    exact_ok = all(parse(r["value_exact"]) == mem[r["scenario"]][r["variable_id"]] for r in rows
                   if r["kind"] == "output" and isinstance(mem[r["scenario"]][r["variable_id"]], float))
    lossy = [r["variable_id"] for r in rows if r["kind"] == "output" and r["value_exact"] not in ("", "never")
             and isinstance(parse(r["value_display"].replace(",", "")), float) and parse(r["value_display"].replace(",", "")) != parse(r["value_exact"])]
    check("display isolation: value_exact equals the in-memory value exactly for every numeric output; display rounding is lossy for some outputs",
          exact_ok and len(lossy) > 0, f"lossy display examples: {lossy[:3]} ({len(lossy)} total)")

    # 3. Unknown is not zero
    obs = {r["variable_id"]: r for r in rows if r["scenario"] == "observed"}
    outs = [r for r in rows if r["scenario"] == "observed" and r["kind"] == "output"]
    check("unknown: every observed-scenario output that depends on an assumption is blank with status 'unknown'",
          all(r["value_exact"] == "" and r["status"] == "unknown" for r in outs), f"{sum(1 for r in outs if r['value_exact'] != '')} non-blank")
    check("unknown is not zero: no observed-scenario output equals 0", not any(r["value_exact"] in ("0.0", "-0.0") for r in outs))
    check("C02 revenue is unknown in every scenario (no source), not zero",
          all(r["value_exact"] == "" for r in rows if r["variable_id"] == "C02_revenue_per_user_year"))
    check("rule zero: class-A share is a labelled rule 0 in every scenario",
          all(r["value_exact"] == "0.0" and r["status"] == "rule" for r in rows if r["variable_id"] == "share_route_A"))
    check("switching GMV is unknown (None), not zero, in every scenario",
          all(r["value_exact"] == "" for r in rows if r["variable_id"] == "mkt_switching_gmv_per_1M_users_year"))

    # 4. Activation counted once
    a, ch, c = 0.4, 0.05, 100.0
    r = E.retention_given_activated(ch)
    via_ar = E.contribution_per_acquired(c, a=a, r=r)
    via_q = E.contribution_per_acquired(c, q=[a * x for x in r])
    check("cohort: a*r_t*c equals q_t*c when q_t = a*r_t", all(math.isclose(x, y, rel_tol=1e-12) for x, y in zip(via_ar, via_q)))
    try:
        E.contribution_per_acquired(c, a=a, q=[a * x for x in r])
        guarded = False
    except ValueError:
        guarded = True
    check("cohort: passing activation together with acquired-based q_t raises", guarded)
    check("cohort: 'never' payback is distinct from unknown",
          E.payback_month(1.0, 1e9, 0.5, 0.1) == "never" and E.payback_month(None, 1.0, 0.5, 0.1) is None)

    # 5. One labour price
    rate_keys = [k for k, *_x in E.INPUTS if "per_min" in k]
    check("labour: no per-minute price is an input; the only per-minute price is computed once (wage x load / 60)", rate_keys == [], str(rate_keys))
    src = open(os.path.join(HERE, "economics_model.py"), encoding="utf-8").read()
    check("labour: labor_jpy_per_min is assigned exactly once", src.count('o["labor_jpy_per_min"] =') == 1)

    # 6. Breakeven algebra: plugging breakeven minutes back gives zero per-request margin (C04)
    v = E.scenario_inputs(2)
    o = E.compute(v)
    m = o["C04_breakeven_human_minutes"]
    v2 = dict(v)
    v2["human_min_per_request"] = m
    o2 = E.compute(v2)
    fee_net = v["per_cancel_fee_jpy"] * (1 - v["payment_fee_rate"]) * (1 - v["refund_rate"])
    check("frontier: at breakeven minutes, net fee per request equals cost per request (C04)",
          math.isclose(fee_net, o2["c04_cost_per_request"], rel_tol=1e-9), f"fee_net={fee_net:.6f} cost={o2['c04_cost_per_request']:.6f} m*={m:.4f}")
    ot = E.compute(E.scenario_inputs(1))
    check("frontier: a negative breakeven is reported as infeasible, not as a usable minute budget",
          (ot["C04_breakeven_human_minutes"] < 0) == (ot["C04_breakeven_feasible"] == 0.0))

    # 7. The paradox
    for i in (1, 2):
        oo = E.compute(E.scenario_inputs(i))
        check(f"paradox ({E.SCEN[i]}): steady-state requests do not exceed year-1 backlog when new subs per year ≤ stock",
              oo["requests_steady_per_user_year"] <= oo["requests_year1_per_user"] + 1e-12)
        vv = E.scenario_inputs(i)
        vv["new_subs_per_user_year"] *= 2
        check(f"paradox ({E.SCEN[i]}): steady-state requests scale with the inflow of new subscriptions (doubling inflow doubles them)",
              math.isclose(E.compute(vv)["requests_steady_per_user_year"], 2 * oo["requests_steady_per_user_year"], rel_tol=1e-12))
        check(f"paradox ({E.SCEN[i]}): flag equals sign of user net value",
              oo["paradox_flag_subscription_not_justified_by_cancellations"] == (1.0 if oo["user_net_value_steady_c05_jpy"] < 0 else 0.0))

    # 8. Gating and conflict flags travel with the concept rows
    check("C06 outputs carry the legal gate flag in every scenario",
          all("legal_gate_L06_unresolved" in r["flags"] for r in rows if r["concept"] == "C06"))
    check("C08 outputs carry the conflict-of-interest flag", all("conflict_of_interest" in r["flags"] for r in rows if r["concept"] == "C08"))

    # 9. Every input is labelled with a status and an evidence pointer
    check("inputs: every input has a status in the vocabulary and an evidence field",
          all(st in ("observed", "rule", "assumption", "unknown") and ev for _k, _d, _u, _uc, st, _v, ev in E.INPUTS))

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    lines = [f"run_at_utc: {now}", "model: model/economics_model.py", ""]
    for name, ok, detail in results:
        lines.append(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    lines.append("")
    lines.append(f"{sum(ok for _, ok, _ in results)}/{len(results)} passed")
    lines.append("scope: arithmetic, interchange and labelling discipline only; not permission, demand or profitability.")
    open(os.path.join(ROOT, "12_QA_economics_tests.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)


if __name__ == "__main__":
    main()
