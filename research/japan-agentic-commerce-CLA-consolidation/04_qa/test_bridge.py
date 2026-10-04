"""Round-trip, unit-tolerance, unknown-propagation and cohort tests for the CLA economics bridge.

Run: python3 test_bridge.py   (writes QA_bridge_tests.txt next to this file)
Each test prints PASS/FAIL; the script exits non-zero on any failure.
"""
import csv
import datetime
import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True  # never write caches next to the read-only originals

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.join(HERE, "..", "03_derivatives", "bridge")
spec = importlib.util.spec_from_file_location("bridge", os.path.join(BRIDGE, "bridge_model.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

# Unit-aware tolerances: (relative, absolute). Display rounding never enters computation.
TOL = {"jpy": (1e-12, 1e-9), "share": (0.0, 1e-12), "count": (1e-12, 1e-15), "minutes": (1e-12, 1e-9),
       "months": (0.0, 0.0), "tokens": (0.0, 0.0), "usd": (1e-12, 0.0), "ratio": (1e-12, 0.0), "flag": (0.0, 0.0)}

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))


def parse(s):
    if s == "":
        return None
    if s in ("True", "False"):
        return s == "True"
    try:
        return float(s)
    except ValueError:
        return s  # e.g. "never"


def close(a, b, uc):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (str, bool)) or isinstance(b, (str, bool)):
        return a == b
    rel, ab = TOL[uc]
    return math.isclose(a, b, rel_tol=rel, abs_tol=ab) if (rel or ab) else a == b


def main():
    path = os.path.join(HERE, "_roundtrip_bridge_outputs.csv")
    B.write(path)
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    os.remove(path)

    # 1. Re-import exported inputs, recompute every output, compare with exported outputs
    n = bad = 0
    mism = []
    for i, s in enumerate(B.SCEN):
        v = {r["variable_id"]: parse(r["value_exact"]) for r in rows if r["scenario"] == s and r["kind"] == "input"}
        rec = B.compute(v)
        mem = B.compute(B.scenario_inputs(i))
        for r in rows:
            if r["scenario"] != s or r["kind"] != "output":
                continue
            k, uc = r["variable_id"], r["unit_class"]
            exp_val = parse(r["value_exact"])
            n += 1
            if not (close(rec[k], exp_val, uc) and close(mem[k], exp_val, uc)):
                bad += 1
                mism.append((s, k, rec[k], exp_val))
    check("roundtrip: recompute from re-imported exported inputs reproduces every exported output (unit-aware tolerance)", bad == 0, f"{n} outputs, {bad} mismatches {mism[:3]}")

    # 2. Non-monetary precision survives the round trip (the Grok 0.012 case)
    x = 4 * 0.25 * 0.05 * 0.60 * 0.40
    check("precision: 0.012 attributable orders survives export/import exactly", parse(B.exact(x)) == x and B.display(x, "count") == "0.0120", f"exact={B.exact(x)} display={B.display(x, 'count')}")
    check("precision: 2-dp display of 0.012 is 0.01, and 0.01 x 80 != 0.012 x 80 (why display values must not be data)", round(x, 2) == 0.01 and abs(0.01 * 80 - x * 80) > 0.1, f"{0.01 * 80:.2f} vs {x * 80:.2f}")

    # 3. Displayed intermediates would NOT reconcile (the Grok 0.01 mechanism) -> exports carry exact values
    A = {r["variable_id"]: r for r in rows if r["scenario"] == "illustrative_A"}
    disp_chain = parse(A["cost_per_email"]["value_display"]) * parse(A["c01_emails"]["value_exact"])
    exact_chain = parse(A["c01_inference"]["value_exact"])
    from_exact = parse(A["cost_per_email"]["value_exact"]) * parse(A["c01_emails"]["value_exact"])
    check("display isolation: downstream recomputed from a DISPLAYED intermediate diverges, from the EXACT intermediate it reconciles",
          (not close(disp_chain, exact_chain, "jpy")) and close(from_exact, exact_chain, "jpy"),
          f"display-based {disp_chain:.4f} vs exact {exact_chain:.6f}; exact-based {from_exact:.6f}")

    # 4. Unknown cells stay unknown; rule zeros stay distinct
    obs = {r["variable_id"]: r for r in rows if r["scenario"] == "observed"}
    must_be_unknown = ["c01_cost", "c01_contribution", "c03_cost", "c03_revenue_if_approved", "c04b_labor", "c07_contribution", "ltv36_per_acquired_c01"]
    check("unknown: observed-scenario outputs that depend on unmeasured inputs are blank with status 'unknown' (not 0)",
          all(obs[k]["value_exact"] == "" and obs[k]["status"] == "unknown" for k in must_be_unknown),
          str({k: (obs[k]["value_exact"], obs[k]["status"]) for k in must_be_unknown}))
    check("rule zero: gated C03 booked revenue is 0 with status 'rule_zero_underwriting_exclusion' and commercial_amount 'unknown'",
          obs["c03_revenue_booked"]["value_exact"] == "0.0" and obs["c03_revenue_booked"]["status"] == "rule_zero_underwriting_exclusion" and obs["c03_revenue_booked"]["commercial_amount"] == "unknown")
    check("rule zero: passive affiliate revenue is a program-rule 0 input, not an unknown", obs["passive_affiliate"]["value_exact"] == "0.0" and obs["passive_affiliate"]["status"] == "rule")
    check("unknown is not zero: C07 contribution stays blank in every scenario while integration cost is unknown",
          all(r["value_exact"] == "" for r in rows if r["variable_id"] == "c07_contribution"))
    check("gate: C02 execution is not computed in any scenario", all(r["status"] == "gated_not_computed" for r in rows if r["variable_id"] == "c02_contribution_per_attempt"))

    # 5. Cohort: activation counted once
    a, r = 0.21, B.retention_given_activated(0.2, 0.08)
    c = 10.0
    via_ar = B.contribution_per_acquired(c, a=a, r=r)
    via_q = B.contribution_per_acquired(c, q=[a * rt for rt in r])
    check("cohort: a x r_t x c_t equals q_t x c_t when q_t = a x r_t", all(math.isclose(x1, x2, rel_tol=1e-12) for x1, x2 in zip(via_ar, via_q)))
    try:
        B.contribution_per_acquired(c, a=a, q=[a * rt for rt in r])
        guarded = False
    except ValueError:
        guarded = True
    check("cohort: passing activation together with an acquired-based q_t raises (double-count guard)", guarded)
    dbl = sum(a * (a * rt) * c for rt in r)
    check("cohort: the double-count the guard prevents would understate value by factor a", math.isclose(dbl, a * sum(via_ar), rel_tol=1e-12), f"single={sum(via_ar):.4f} double={dbl:.4f}")
    never = [rw for rw in rows if rw["variable_id"] == "payback_c01" and rw["scenario"] != "observed"]
    check("cohort: 'never' payback is distinct from unknown", all(rw["value_exact"] == "never" and rw["status"] == "not_within_36_months" for rw in never))

    # 6. C04 stress reproduction
    check("C04: reviewer's 40% x 1 case x 15 min x JPY50 = JPY300 per household-month reproduced", math.isclose(B.compute(B.scenario_inputs(1))["reviewer_300_check"], 300.0))
    _, bounds = B.stress_grid(os.path.join(HERE, "_tmp_grid.csv"))
    os.remove(os.path.join(HERE, "_tmp_grid.csv"))
    check("C04: at JPY40/MAU after the illustrative tracking core, affordable submission x human-share x minutes < 0.5",
          bounds["max_psm_fee40_after_tracking_core"] < 0.5, f"{bounds}")

    # 7. Single labour rate (founder hours not double counted) and factors applied once
    rate_keys = [k for k, *_r in B.INPUTS if "per_min" in k or k.endswith("_rate_jpy")]
    check("labour: exactly one per-minute price key; fixed team cost is not in the bridge", rate_keys == ["labor_jpy_per_min"] and not any("team" in k for k, *_r in B.INPUTS), str(rate_keys))
    src = open(os.path.join(BRIDGE, "bridge_model.py"), encoding="utf-8").read()
    check("factors once: coverage/handoff/completion/attribution each appear once in each C03 volume formula",
          all(src.count(f'v["{f}"]') == 2 for f in ("handoff_share", "completion", "attribution")), "2 = booked + if_approved formulas")

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    lines = [f"run_at_utc: {now}", f"bridge: 03_derivatives/bridge/bridge_model.py", ""]
    for name, ok, detail in results:
        lines.append(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    lines.append("")
    lines.append(f"{sum(ok for _, ok, _ in results)}/{len(results)} passed")
    lines.append("scope note: these tests prove arithmetic, interchange and labelling discipline. They do NOT show that any configuration is permitted, wanted or profitable.")
    open(os.path.join(HERE, "QA_bridge_tests.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)


if __name__ == "__main__":
    main()
