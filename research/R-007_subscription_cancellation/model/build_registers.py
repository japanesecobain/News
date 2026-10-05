"""Build and validate the R-007 evidence ledger (02) and source register (10).

Run: python3 model/build_registers.py
Exits non-zero if any structural check fails. These checks cover structure, vocabulary,
referential integrity and source-family discipline. They are NOT semantic QA: they do not
show that any claim is true.
"""
import csv
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import evidence as EV  # noqa: E402
import competitors as CMP  # noqa: E402
import routes as RT  # noqa: E402
import legal as LG  # noqa: E402
import experiments as EX  # noqa: E402
import registers as RG  # noqa: E402

CLAIM_FIELDS = ["claim_id", "exact_claim", "origin", "status", "geography", "period", "population", "metric",
                "denominator", "source", "publication_date", "observation_date", "access_date", "exact_locator",
                "supporting_passage", "counterevidence", "limitation", "decision_use",
                # extensions, kept after the required §25 fields
                "verification", "source_families", "wntb", "stage"]
SOURCE_FIELDS = ["source_id", "title", "publisher", "url", "origin", "language", "publication_date", "family",
                 "access_status", "access_date", "used_by_claims", "notes"]


def validate():
    errors, warnings = [], []
    src = {s["source_id"]: s for s in EV.SOURCES}
    if len(src) != len(EV.SOURCES):
        errors.append("duplicate source_id")
    for s in EV.SOURCES:
        if s["origin"] not in EV.ORIGINS:
            errors.append(f"{s['source_id']}: origin '{s['origin']}' not in vocabulary")
        for k in ("title", "publisher", "url", "family", "access_status"):
            if not s.get(k):
                errors.append(f"{s['source_id']}: empty {k}")
        if s["url"].startswith("http") and " " in s["url"]:
            errors.append(f"{s['source_id']}: url contains a space")
    ids = [c["claim_id"] for c in EV.CLAIMS]
    if len(ids) != len(set(ids)):
        errors.append("duplicate claim_id")
    required = CLAIM_FIELDS[:18] + ["verification", "wntb", "stage"]
    used = {}
    for c in EV.CLAIMS:
        cid = c["claim_id"]
        for k in required:
            if not str(c.get(k, "")).strip():
                errors.append(f"{cid}: empty {k}")
        if c["status"] not in EV.STATUSES:
            errors.append(f"{cid}: status '{c['status']}' not in vocabulary")
        if c["origin"] not in EV.ORIGINS:
            errors.append(f"{cid}: origin '{c['origin']}' not in vocabulary")
        if c["verification"] not in EV.VERIFICATION:
            errors.append(f"{cid}: verification '{c['verification']}' not in vocabulary")
        sids = [x for x in c["source"].split(";") if x]
        for sid in sids:
            if sid not in src:
                errors.append(f"{cid}: unknown source {sid}")
            used.setdefault(sid, []).append(cid)
        fams = sorted({src[s]["family"] for s in sids if s in src})
        c["_families"] = fams
        # Discipline rules
        if c["status"] == "directly observed":
            errors.append(f"{cid}: 'directly observed' is impossible in this packet (no page was opened)")
        if c["status"] == "corroborated" and len(fams) < 2:
            errors.append(f"{cid}: 'corroborated' needs >=2 independent source families, has {fams}")
        if c["status"] == "company-reported" and not any(src[s]["origin"] in ("company/provider", "original survey") for s in sids if s in src):
            errors.append(f"{cid}: 'company-reported' without a company or survey-sponsor source")
        if c["status"] == "calculated" and c["origin"] != "analyst calculation":
            errors.append(f"{cid}: calculated claim must have origin 'analyst calculation'")
        if c["verification"] == "extract_of_primary_url" and not any(src[s]["origin"] in ("government/regulator", "company/provider", "original survey") for s in sids if s in src):
            warnings.append(f"{cid}: extract_of_primary_url but no first-party source")
    for sid, s in src.items():
        if sid not in used and "no content extracted" not in s["access_status"]:
            errors.append(f"{sid}: source not used by any claim and not marked 'no content extracted'")
    return errors, warnings, used


def write(used):
    with open(os.path.join(ROOT, "02_EVIDENCE_LEDGER.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CLAIM_FIELDS)
        w.writeheader()
        for c in EV.CLAIMS:
            row = {k: c.get(k, "") for k in CLAIM_FIELDS}
            row["source_families"] = ";".join(c["_families"])
            w.writerow(row)
    with open(os.path.join(ROOT, "10_SOURCE_REGISTER.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SOURCE_FIELDS)
        w.writeheader()
        for s in EV.SOURCES:
            row = {k: s.get(k, "") for k in SOURCE_FIELDS}
            row["access_date"] = EV.ACCESS_DATE
            row["used_by_claims"] = ";".join(used.get(s["source_id"], []))
            w.writerow(row)


def build_competitors(errors):
    ids = {c["claim_id"] for c in EV.CLAIMS}
    seen = set()
    for r in CMP.ROWS:
        if set(r) != set(CMP.FIELDS):
            errors.append(f"{r.get('competitor_id')}: fields mismatch {set(CMP.FIELDS) ^ set(r)}")
            continue
        if r["competitor_id"] in seen:
            errors.append(f"{r['competitor_id']}: duplicate")
        seen.add(r["competitor_id"])
        for k in CMP.FIELDS:
            if not str(r[k]).strip():
                errors.append(f"{r['competitor_id']}: empty {k}")
        for e in r["evidence_ids"].split(";"):
            if e not in ids:
                errors.append(f"{r['competitor_id']}: unknown evidence id {e}")
        if len(r["how_we_lose"]) < 40:
            errors.append(f"{r['competitor_id']}: how_we_lose too thin")
    if errors:
        return
    with open(os.path.join(ROOT, "03_COMPETITOR_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CMP.FIELDS)
        w.writeheader()
        for r in CMP.ROWS:
            w.writerow(r)


def build_routes(errors):
    ids = {c["claim_id"] for c in EV.CLAIMS}
    seen = set()
    counts = {k: 0 for k in "ABCDE"}
    for r in RT.ROWS:
        rid = r.get("route_id")
        if set(r) != set(RT.FIELDS):
            errors.append(f"{rid}: fields mismatch {set(RT.FIELDS) ^ set(r)}")
            continue
        if rid in seen:
            errors.append(f"{rid}: duplicate")
        seen.add(rid)
        for k in RT.FIELDS:
            if not str(r[k]).strip():
                errors.append(f"{rid}: empty {k} (use UNKNOWN)")
        for e in r["evidence_source"].split(";"):
            if e not in ids:
                errors.append(f"{rid}: unknown evidence id {e}")
        rc = r["route_class"]
        if rc not in counts:
            errors.append(f"{rid}: route_class {rc} not in A-E")
            continue
        counts[rc] += 1
        # Consistency rules between class and evidence cells
        if rc == "B" and not r["self_serve_cancel_available"].startswith("Yes"):
            errors.append(f"{rid}: class B needs evidenced self-serve for the user")
        if rc == "C" and (r["concierge_status"] != "permitted"):
            errors.append(f"{rid}: class C needs evidence that a company agent is permitted")
        if rc == "A" and "documented" not in r["third_party_automation_feasibility"].lower():
            errors.append(f"{rid}: class A needs a documented third-party machine path")
        if rc == "D" and r["concierge_status"] not in ("family-only", "not permitted"):
            errors.append(f"{rid}: class D needs evidence that no company agent is accepted")
        if r["concierge_status"] not in ("permitted", "family-only", "not stated", "UNKNOWN", "not permitted"):
            errors.append(f"{rid}: concierge_status vocabulary")
    if errors:
        return None
    with open(os.path.join(ROOT, "04_CANCELLATION_ROUTE_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=RT.FIELDS)
        w.writeheader()
        for r in RT.ROWS:
            w.writerow(r)
    return counts


def build_legal(errors):
    ids = {c["claim_id"] for c in EV.CLAIMS}
    ctypes = {"law", "provider contract", "technical restriction", "unknown"}
    for r in LG.ROWS:
        rid = r.get("row_id")
        if set(r) != set(LG.FIELDS):
            errors.append(f"{rid}: fields mismatch {set(LG.FIELDS) ^ set(r)}")
            continue
        for k in LG.FIELDS:
            if not str(r[k]).strip():
                errors.append(f"{rid}: empty {k}")
        if r["constraint_type"] not in ctypes:
            errors.append(f"{rid}: constraint_type {r['constraint_type']} not in {ctypes}")
        for e in r["evidence_ids"].split(";"):
            if e not in ids:
                errors.append(f"{rid}: unknown evidence id {e}")
        if r["status"].startswith("unresolved") and r["counsel_question"] in ("", "n/a"):
            errors.append(f"{rid}: unresolved row needs a counsel question")
        for word in ("lawful", "legal to", "permitted to", "you may"):
            if word in r["conservative_design_implication"].lower():
                errors.append(f"{rid}: design implication reads like a legal conclusion ('{word}')")
    if errors:
        return
    with open(os.path.join(ROOT, "05_PERMISSION_AND_LEGAL_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LG.FIELDS)
        w.writeheader()
        for r in LG.ROWS:
            w.writerow(r)


def build_experiments(errors):
    ranks = [r["rank"] for r in EX.ROWS]
    if sorted(ranks) != list(range(1, len(EX.ROWS) + 1)):
        errors.append(f"experiment ranks not a permutation: {ranks}")
    for r in EX.ROWS:
        if set(r) != set(EX.FIELDS):
            errors.append(f"{r.get('experiment_id')}: fields mismatch {set(EX.FIELDS) ^ set(r)}")
            continue
        for k in EX.FIELDS:
            if not str(r[k]).strip():
                errors.append(f"{r['experiment_id']}: empty {k}")
        if r["status"] != "designed; not executed":
            errors.append(f"{r['experiment_id']}: status must be 'designed; not executed'")
    for need in ("E1", "E2", "E3", "E4", "E5"):
        if need not in {r["experiment_id"] for r in EX.ROWS}:
            errors.append(f"missing work-order experiment {need}")
    if errors:
        return
    with open(os.path.join(ROOT, "09_EXPERIMENT_BACKLOG.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EX.FIELDS)
        w.writeheader()
        for r in sorted(EX.ROWS, key=lambda x: x["rank"]):
            w.writerow(r)


def build_concepts_hypotheses(errors):
    ids = {c["claim_id"] for c in EV.CLAIMS}
    want_c = [f"R007-C0{i}" for i in range(1, 10)]
    if [c["concept_id"] for c in RG.CONCEPTS] != want_c:
        errors.append("concept register must be exactly R007-C01..C09 in order")
    want_h = [f"H{i:02d}" for i in range(1, 15)]
    if [h["hypothesis_id"] for h in RG.HYPOTHESES] != want_h:
        errors.append("hypothesis register must be exactly H01..H14 in order")
    for rows, fields, idk in ((RG.CONCEPTS, RG.CONCEPT_FIELDS, "concept_id"), (RG.HYPOTHESES, RG.HYP_FIELDS, "hypothesis_id")):
        for r in rows:
            if set(r) != set(fields):
                errors.append(f"{r.get(idk)}: fields mismatch {set(fields) ^ set(r)}")
                continue
            for k in fields:
                if not str(r[k]).strip():
                    errors.append(f"{r[idk]}: empty {k}")
            for e in r["evidence_ids"].split(";"):
                if e not in ids:
                    errors.append(f"{r[idk]}: unknown evidence id {e}")
    if errors:
        return
    for name, rows, fields in (("07_CONCEPT_REGISTER.csv", RG.CONCEPTS, RG.CONCEPT_FIELDS), ("08_HYPOTHESIS_REGISTER.csv", RG.HYPOTHESES, RG.HYP_FIELDS)):
        with open(os.path.join(ROOT, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                w.writerow(r)


def roundtrip():
    """Re-read both CSVs and confirm every field survived unchanged."""
    bad = 0
    rows = list(csv.DictReader(open(os.path.join(ROOT, "02_EVIDENCE_LEDGER.csv"), encoding="utf-8")))
    for r, c in zip(rows, EV.CLAIMS):
        for k in CLAIM_FIELDS[:18]:
            if r[k] != str(c[k]):
                bad += 1
    if len(rows) != len(EV.CLAIMS):
        bad += 1
    srows = list(csv.DictReader(open(os.path.join(ROOT, "10_SOURCE_REGISTER.csv"), encoding="utf-8")))
    if len(srows) != len(EV.SOURCES):
        bad += 1
    return bad


def main():
    errors, warnings, used = validate()
    for w in warnings:
        print("WARN ", w)
    if errors:
        for e in errors:
            print("ERROR", e)
        sys.exit(1)
    write(used)
    cerr = []
    build_competitors(cerr)
    rcounts = build_routes(cerr)
    build_legal(cerr)
    build_experiments(cerr)
    build_concepts_hypotheses(cerr)
    if cerr:
        for e in cerr:
            print("ERROR", e)
        sys.exit(1)
    bad = roundtrip()
    by_status = {}
    for c in EV.CLAIMS:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
    fams = {s["family"] for s in EV.SOURCES}
    print(f"claims={len(EV.CLAIMS)} sources={len(EV.SOURCES)} families={len(fams)} competitors={len(CMP.ROWS)} roundtrip_mismatches={bad}")
    print("status counts:", dict(sorted(by_status.items())))
    print("route classes (purposive sample, not market shares):", rcounts,
          "| concierge_status:", {k: sum(1 for r in RT.ROWS if r["concierge_status"] == k) for k in sorted({r["concierge_status"] for r in RT.ROWS})},
          "| legal rows:", len(LG.ROWS), {k: sum(1 for r in LG.ROWS if r["constraint_type"] == k) for k in ("law", "provider contract", "technical restriction", "unknown")},
          "| architectures:", {k: sum(1 for r in RT.ROWS if r["architecture"] == k) for k in sorted({r["architecture"] for r in RT.ROWS})})
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
