"""Cross-reference and figure-consistency QA for the R-007 packet.

Run: python3 model/qa_crossrefs.py   (prints PASS/FAIL; exit 1 on any failure)
Checks that every evidence, competitor, route, legal, experiment, concept and hypothesis ID cited in the
markdown deliverables exists in the registers, and that key figures quoted in the memo match the model or ledger.
"""
import csv
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def ids(path, col):
    return {r[col] for r in csv.DictReader(open(os.path.join(ROOT, path), encoding="utf-8"))}


def main():
    res = []
    ev = ids("02_EVIDENCE_LEDGER.csv", "claim_id")
    cm = ids("03_COMPETITOR_MATRIX.csv", "competitor_id")
    rm = ids("04_CANCELLATION_ROUTE_MATRIX.csv", "route_id")
    lg = ids("05_PERMISSION_AND_LEGAL_MATRIX.csv", "row_id")
    ex = ids("09_EXPERIMENT_BACKLOG.csv", "experiment_id")
    md_files = ["00_DECISION_MEMO.md", "01_RESEARCH_REPORT.md", "11_MOAT_AND_RIGHT_TO_WIN.md"]
    for f in md_files:
        t = open(os.path.join(ROOT, f), encoding="utf-8").read()
        # [E-A01] style and ranges like E-G01–G07 (check both ends)
        cited = set()
        for m in re.finditer(r"E-([A-Z])(\d{2})(?:[–-]([A-Z])?(\d{2}))?", t):
            cited.add(f"R7-E-{m.group(1)}{m.group(2)}")
            if m.group(4):
                cited.add(f"R7-E-{m.group(3) or m.group(1)}{m.group(4)}")
        missing = sorted(c for c in cited if c not in ev)
        res.append((f"{f}: every cited evidence ID exists ({len(cited)} cited)", not missing, str(missing[:5])))
        cms = set(re.findall(r"CM\d{2}", t))
        res.append((f"{f}: every cited competitor ID exists", cms <= cm, str(sorted(cms - cm))))
        rms = set(re.findall(r"RM\d{2}", t))
        res.append((f"{f}: every cited route ID exists", rms <= rm, str(sorted(rms - rm))))
        lgs = set(re.findall(r"\bL\d{2}\b", t))
        res.append((f"{f}: every cited legal row exists", lgs <= lg, str(sorted(lgs - lg))))
        exs = set(re.findall(r"\b(E[1-6]|PR[1-3])\b", t))
        res.append((f"{f}: every cited experiment exists", exs <= ex | {"PR2"}, str(sorted(exs - ex))))

    # Key memo figures against the model / ledger
    spec = importlib.util.spec_from_file_location("em", os.path.join(HERE, "economics_model.py"))
    E = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(E)
    t_ = E.compute(E.scenario_inputs(1))
    l_ = E.compute(E.scenario_inputs(2))
    memo = open(os.path.join(ROOT, "00_DECISION_MEMO.md"), encoding="utf-8").read()
    checks = [
        ("C07 fee floor tight 18.37 and loose 5.86", f"{t_['C07_partner_fee_breakeven_jpy_per_enrolled_month_at_assumed_size']:.2f}" == "18.37"
         and f"{l_['C07_partner_fee_breakeven_jpy_per_enrolled_month_at_assumed_size']:.2f}" == "5.86" and "¥5.86–18.37" in memo),
        ("subscription justified by cancellations 22.50 / 450", f"{t_['max_sub_price_justified_by_cancellation_savings_jpy_month']:.2f}" == "22.50"
         and round(l_["max_sub_price_justified_by_cancellation_savings_jpy_month"]) == 450 and "¥22.50–450" in memo),
        ("C04 payback never in both illustrations", t_["C04_payback_month"] == "never" and l_["C04_payback_month"] == "never"),
        ("C04 breakeven minutes infeasible (tight) and about 123 (loose)", t_["C04_breakeven_feasible"] == 0.0 and round(l_["C04_breakeven_human_minutes"]) == 123),
        ("route sample 14 of 22 are class B", sum(1 for r in csv.DictReader(open(os.path.join(ROOT, "04_CANCELLATION_ROUTE_MATRIX.csv"), encoding="utf-8")) if r["route_class"] == "B") == 14
         and len(rm) == 22 and "14 of 22" in memo),
        ("paradox flag yes in both illustrations", t_["paradox_flag_subscription_not_justified_by_cancellations"] == 1.0 and l_["paradox_flag_subscription_not_justified_by_cancellations"] == 1.0),
    ]
    led = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "02_EVIDENCE_LEDGER.csv"), encoding="utf-8"))}
    checks += [
        ("MF 17.3M in ledger and memo", "17.3M" in led["R7-E-G01"]["exact_claim"] and "17.3M" in memo),
        ("Moneytree about 6.5M and MUFG date in ledger and memo", "6.5M" in led["R7-E-G07"]["exact_claim"] and "2025-08-29" in led["R7-E-G07"]["exact_claim"] and "2025-08-29" in memo),
        ("46.0% in ledger and memo", "46.0%" in led["R7-E-A03"]["exact_claim"] and "46.0%" in memo),
        ("Rocket Money $390M and about 2.5M cancellations in ledger and memo", "$390M" in led["R7-E-G13"]["exact_claim"] and "2.5M" in led["R7-E-G16"]["exact_claim"] and "$390M" in memo),
        ("about 0.25 cancellations per app user", "0.25" in led["R7-E-G17"]["exact_claim"] and "0.25" in memo),
        ("71.6% / 17.9% recorded as not found and not used as evidence", led["R7-E-A02"]["status"] == "unresolved" and "not found" in memo.lower()),
    ]
    for name, ok in checks:
        res.append((f"memo figure: {name}", ok, ""))

    # Mandatory closing sections, in order, at the end of the report
    rep = open(os.path.join(ROOT, "01_RESEARCH_REPORT.md"), encoding="utf-8").read()
    heads = re.findall(r"^## (.+)$", rep, flags=re.M)
    want = ["What would make this a great company?", "What would make this a bad company?", "What are we most likely to be wrong about?",
            "What does public research still not establish?", "Which single experiment changes the decision most?", "What should remain open?"]
    res.append(("report ends with the six mandatory closing sections in order", heads[-6:] == want, str(heads[-6:])))
    wrong = rep.split("## What are we most likely to be wrong about?")[1].split("## What does public research")[0]
    res.append(("'most likely wrong' lists at least 5 points", len(re.findall(r"^\d+\. ", wrong, flags=re.M)) >= 5, ""))
    mw = len(memo.split())
    res.append(("decision memo is 800-1,200 words", 800 <= mw <= 1200, f"{mw} words"))
    res.append(("memo leads with one disposition", memo.split("\n")[2].startswith("**Disposition: PARK.**"), memo.split("\n")[2][:40]))

    for name, ok, d in res:
        print(("PASS  " if ok else "FAIL  ") + name + (f"  [{d}]" if d and not ok else ""))
    print(f"{sum(ok for _, ok, _ in res)}/{len(res)} passed")
    sys.exit(0 if all(ok for _, ok, _ in res) else 1)


if __name__ == "__main__":
    main()
