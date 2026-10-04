"""Read-only QA of the ORIGINAL CLA packet (commit ebd8cdf).

Nothing in the original directory is written. Three checks:
  1. Workbook formulas (pycel) vs in-memory Python outputs: implementation consistency only.
  2. Exported 04 CSV values vs exact in-memory values: precision lost on export.
  3. Dependency round trip: re-import the exported CSV, recompute every output from the EXPORTED
     inputs and EXPORTED upstream outputs, and compare with the exported value of that output.
     This is the check the reviewer applied to Grok v2; it is run here on CLA's own export.
Outputs: QA_original_CLA_rerun.txt and QA_original_CLA_roundtrip_discrepancies.csv (this folder).
"""
import csv
import datetime
import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True  # never write caches next to the read-only originals

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.abspath(os.path.join(HERE, "..", "..", "japan-agentic-commerce-CLA"))
MODEL_DIR = os.path.join(ORIG, "model")


def load_model():
    spec = importlib.util.spec_from_file_location("cla_model", os.path.join(MODEL_DIR, "economics_model.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)  # module guard prevents main(); nothing is written
    return m


def display_half_unit(x):
    """Half of the last displayed digit under the original fmt(): ints for |x|>=1000, else 4 dp."""
    return 0.5 if abs(x) >= 1000 else 0.00005


def parse(s):
    s = (s or "").strip()
    if s == "":
        return None
    return float(s)


def main():
    m = load_model()
    out_lines = []
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out_lines.append(f"run_at_utc: {now}")
    out_lines.append(f"original_dir: {os.path.relpath(ORIG, os.path.join(HERE, '..', '..', '..'))} (read-only)")

    exact = {s: m.compute(m.scenario_inputs(i)) for i, s in enumerate(m.SCEN)}

    # 1. pycel workbook vs Python
    try:
        from pycel import ExcelCompiler
        xl = ExcelCompiler(filename=os.path.join(MODEL_DIR, "economics_model.xlsx"))
        col = {"downside": "F", "base": "G", "upside": "H"}
        n = bad = 0
        for r, (oid, key, *_x) in enumerate(m.OUTPUTS, start=2):
            for s in m.SCEN:
                xv = xl.evaluate(f"Calc!{col[s]}{r}")
                pv = exact[s][key]
                n += 1
                ok = (xv == "n/a") if pv is None else (isinstance(xv, (int, float)) and math.isclose(float(xv), float(pv), rel_tol=1e-9, abs_tol=1e-9))
                bad += 0 if ok else 1
        out_lines.append(f"[1] workbook formulas vs python: {n} cells, {bad} mismatches (implementation consistency only; not economic validity)")
    except Exception as e:  # pycel missing or workbook unreadable
        out_lines.append(f"[1] workbook check NOT RUN: {e!r}")

    # Load exported CSV
    rows = list(csv.DictReader(open(os.path.join(ORIG, "04_economics_model.csv"), encoding="utf-8")))
    stored = {s: {} for s in m.SCEN}
    for r in rows:
        if r["scenario"] in m.SCEN:
            key = r["description"].split(":", 1)[0].strip()
            stored[r["scenario"]][key] = parse(r["value"])

    # 2. export precision vs exact
    prec = []
    for s in m.SCEN:
        for key, sv in stored[s].items():
            ev = exact[s].get(key)
            if sv is None or ev is None or isinstance(ev, str):
                continue
            prec.append((s, key, ev, sv, abs(ev - sv)))
    lossy = [p for p in prec if p[4] > 1e-12]
    out_lines.append(f"[2] exported values vs exact in-memory: {len(prec)} numeric cells; {len(lossy)} differ from the exact value (rounded on export)")
    worst = sorted(lossy, key=lambda p: -(p[4] / max(abs(p[2]), 1e-12)))[:5]
    for s, key, ev, sv, d in worst:
        out_lines.append(f"     largest relative loss: {s}/{key}: exact {ev!r} stored {sv!r} (rel {d / max(abs(ev), 1e-12):.2e})")

    # 3. dependency round trip from exported values only
    disc = []
    checked = 0
    for s in m.SCEN:
        v = dict(stored[s])
        for oid, key, concept, desc, unit, fn, _xl in m.OUTPUTS:
            sv = stored[s].get(key)
            try:
                rv = fn(v)
            except (TypeError, ZeroDivisionError):
                rv = None
            if sv is None and rv is None:
                continue
            checked += 1
            if sv is None or rv is None:
                disc.append((s, oid, key, unit, sv, rv, None, "one side blank"))
                continue
            d = abs(rv - sv)
            tol = display_half_unit(sv)
            if d > tol:
                disc.append((s, oid, key, unit, sv, rv, d, f"exceeds display half-unit {tol}"))
    out_lines.append(f"[3] dependency round trip (recompute from exported values): {checked} outputs checked; {len(disc)} do not reconcile within their own displayed precision")
    sign_flips = [d for d in disc if d[4] is not None and d[5] is not None and (d[4] > 0) != (d[5] > 0) and abs(d[4]) > 1e-9]
    out_lines.append(f"     sign flips among discrepancies: {len(sign_flips)}")
    out_lines.append("     interpretation: same defect class as Grok v2's 0.01-vs-0.012 export (rounded values saved as data). "
                     "Headline in-memory results are unaffected; the saved table is not a lossless interchange format. Fixed in the derivative bridge (full-precision export + display column).")
    out_lines.append("note: the 2026-10-04 141/141 result was printed to the console only; no log file was retained. This file is a new re-run, not a historical receipt.")

    with open(os.path.join(HERE, "QA_original_CLA_rerun.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    with open(os.path.join(HERE, "QA_original_CLA_roundtrip_discrepancies.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "output_id", "key", "unit", "stored_value", "recomputed_from_stored_inputs", "abs_difference", "note"])
        for d in disc:
            w.writerow([d[0], d[1], d[2], d[3], repr(d[4]), repr(d[5]), "" if d[6] is None else repr(d[6]), d[7]])
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
