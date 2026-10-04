"""Write CSV registers 02, 03, 05, 06, 07, 08 and validate cross-references."""
import csv
import os
import re

from claims import CLAIMS
from registers import COMPETITORS, CONCEPTS, EXPERIMENTS, HYPOTHESES
from sources import ACCESSED, SOURCES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (name, r[0], len(r), len(header))
            w.writerow(r)
    print(f"{name}: {len(rows)} rows")


def main():
    src_ids = {s[0] for s in SOURCES}
    assert len(src_ids) == len(SOURCES), "duplicate source ids"
    claim_ids = [c[0] for c in CLAIMS]
    assert len(set(claim_ids)) == len(claim_ids), "duplicate claim ids"
    hyp_ids = {h[0] for h in HYPOTHESES}
    exp_ids = {e[0] for e in EXPERIMENTS}
    concept_ids = {c[0] for c in CONCEPTS}

    # 08 source register
    write("08_source_register.csv",
          ["source_id", "title", "publisher", "canonical_url", "language", "publication_date", "event_or_effective_date",
           "data_period", "accessed_at", "geography", "source_type", "source_family", "access_status", "limitations"],
          [[s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], ACCESSED, s[8], s[9], s[10], s[11], s[12]] for s in SOURCES])

    # 02 evidence ledger (one row per claim-source relationship)
    rows = []
    for (cid, hid, conc, text, srcs, geo, period, asof, origin, status, soc, why, conf, lim, impl) in CLAIMS:
        assert hid in hyp_ids, (cid, hid)
        for c in conc.split(";"):
            assert c in concept_ids or c in ("ALL", "SUB"), (cid, c)
        for sid, loc in srcs:
            assert sid in src_ids, (cid, sid)
            rows.append([cid, hid, conc, text, sid, loc, geo, period, asof, origin, status, soc, why, conf, lim, impl])
    write("02_evidence_ledger.csv",
          ["claim_id", "hypothesis_id", "concept_id", "claim_text", "source_id", "source_locator", "geography", "metric_period",
           "observed_as_of", "evidence_origin", "claim_status", "support_or_contradict", "reasoning_summary", "confidence",
           "limitation", "decision_implication"], rows)

    # 03 competitor matrix
    for r in COMPETITORS:
        for sid in r[18].split(";"):
            assert sid in src_ids, (r[0], sid)
    write("03_competitor_matrix.csv",
          ["entity_id", "company", "product", "geography", "customer", "payer", "capability", "access_level",
           "availability_status", "first_available_date", "current_as_of", "adoption_metric", "adoption_value",
           "adoption_unit", "adoption_period", "coverage", "pricing", "dependency", "source_ids", "limitation"],
          [list(r) for r in COMPETITORS])

    # 05 hypothesis register
    for h in HYPOTHESES:
        for field in (h[3], h[4]):
            for cid in filter(None, field.split(";")):
                assert cid in claim_ids, (h[0], cid)
        for eid in re.findall(r"CLA-E\d{3}", h[7] + h[6]):
            assert eid in exp_ids, (h[0], eid)
    write("05_hypothesis_register.csv",
          ["hypothesis_id", "hypothesis", "status", "supporting_claim_ids", "contradicting_claim_ids", "confidence",
           "key_unknown", "falsification_test", "decision_implication"], [list(h) for h in HYPOTHESES])

    # 06 experiment backlog
    for e in EXPERIMENTS:
        for hid in e[2].split(";"):
            assert hid in hyp_ids, (e[0], hid)
    write("06_experiment_backlog.csv",
          ["experiment_id", "concept_id", "hypothesis_id", "target_segment", "recruitment_or_access", "method", "baseline",
           "metric", "denominator", "proceed_threshold", "stop_threshold", "threshold_rationale", "sample_plan",
           "cost_assumption", "safety_boundary", "limitation", "decision_unlocked"], [list(e) for e in EXPERIMENTS])

    # 07 concept register
    for c in CONCEPTS:
        for field in (c[15], c[16]):
            for cid in filter(None, field.split(";")):
                assert cid in claim_ids, (c[0], cid)
    write("07_concept_register.csv",
          ["concept_id", "theme", "segment", "job", "proposed_solution", "payer", "frequency", "current_alternative",
           "entry_surface", "permissions", "distribution", "revenue_logic", "defensibility_hypothesis", "primary_risk",
           "validation_status", "supporting_claim_ids", "disconfirming_claim_ids", "cheapest_next_test"],
          [list(c) for c in CONCEPTS])

    # Every source should be cited at least once somewhere
    cited = {sid for c in CLAIMS for sid, _ in c[4]} | {sid for r in COMPETITORS for sid in r[18].split(";")}
    uncited = sorted(src_ids - cited)
    print("uncited sources:", uncited or "none")
    print("claims:", len(CLAIMS), "| sources:", len(SOURCES))


if __name__ == "__main__":
    main()
