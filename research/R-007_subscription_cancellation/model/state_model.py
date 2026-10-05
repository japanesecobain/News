"""R-007 cancellation state model (Workstream F). A design artefact, not product code.

Run: python3 model/state_model.py   -> checks the invariants below and prints PASS/FAIL.
The invariants encode the work order's 'never conflate' rules:
  requested ≠ accepted ≠ effective ≠ charges stopped; provider confirmation ≠ proof that billing stopped.
"""
import sys
from collections import deque

sys.dont_write_bytecode = True

# state -> (meaning, evidence that puts a case in this state)
STATES = {
    "DETECTED_CHARGE": ("A recurring charge is observed on a card, bank or carrier bill", "Two or more similar debits (rule UNKNOWN until E2)"),
    "POSSIBLE_SUBSCRIPTION": ("The charge may be a subscription; provider or rail not yet known", "Descriptor match is ambiguous (e.g. APPLE.COM/BILL)"),
    "CONFIRMED_SUBSCRIPTION": ("Provider, billing rail and account identified and confirmed by the user", "User confirmation plus provider/rail evidence"),
    "CANCEL_REQUESTED_BY_USER": ("The user asks the service to cancel", "Explicit user instruction (timestamped)"),
    "ROUTE_SELECTED": ("Route class A-E chosen for this provider and rail", "Route-matrix row"),
    "AUTHORIZATION_COLLECTED": ("Whatever authority the route needs is in hand", "Written instruction or 委任状 (form per S5); none for B"),
    "USER_ACTION_REQUIRED": ("Only the account holder can do the next step (route B or D)", "Route class B/D, or a provider demand"),
    "USER_AUTH_REQUIRED": ("An authentication challenge must be completed by the user", "MFA, network PIN, sign-in"),
    "PROVIDER_CONTACTED": ("The cancellation instruction was sent to the provider", "Call log, form submission, e-mail sent"),
    "PROVIDER_REJECTED": ("The provider refused or demanded something else", "Rejection message; e.g. holder-only or family-only proxy"),
    "RETENTION_OFFER_ACCEPTED": ("The user chose to keep or downgrade after an offer", "User decision recorded"),
    "PAUSED_OR_SKIPPED": ("Paused, suspended or skipped; NOT cancelled", "Provider shows 休会 or skip status"),
    "CANCELLATION_ACCEPTED": ("The provider acknowledged the cancellation", "Acceptance e-mail or screen"),
    "CANCELLATION_SCHEDULED": ("Accepted, with an effective date in the future", "Stated end date (e.g. end of period or term)"),
    "CANCELLATION_EFFECTIVE": ("The contract ended on its stated date", "Date passed; provider status shows ended"),
    "CHARGES_CONTINUE_BY_CONTRACT": ("Charges legitimately continue after acceptance (term contract or fee)", "Term end date or fee in the contract (e.g. DAZN annual, Adobe 50% fee)"),
    "VERIFICATION_PENDING": ("Waiting for the first billing cycle after the effective date", "Calendar plus expected charge date"),
    "CHARGE_STOPPED": ("No charge appeared in the cycle after the effective date, on the billing rail", "Absence of the expected line on the rail that bills it"),
    "CHARGE_PERSISTED": ("A charge appeared after the effective date without a contractual reason", "Statement line after the effective date"),
    "CANCELLED_UNVERIFIED": ("Accepted or effective, but the rail cannot be observed", "e.g. App Store or carrier rail with no list or receipt access"),
    "DISPUTE_REQUIRED": ("Hand-off: refund or dispute needed (J6); out of service scope", "Persisted charge plus provider refusal"),
    "ACCOUNT_DELETED_WITHOUT_CANCEL": ("Account removed or app deleted, but the billing contract may continue", "e.g. app deletion (Kokusen warning); 退会 vs 解約"),
    "FAILED": ("The service could not complete the route", "Route unresolved (E) or abandoned"),
}

TRANSITIONS = {
    "DETECTED_CHARGE": ["POSSIBLE_SUBSCRIPTION", "CONFIRMED_SUBSCRIPTION"],
    "POSSIBLE_SUBSCRIPTION": ["CONFIRMED_SUBSCRIPTION", "FAILED"],
    "CONFIRMED_SUBSCRIPTION": ["CANCEL_REQUESTED_BY_USER"],
    "CANCEL_REQUESTED_BY_USER": ["ROUTE_SELECTED"],
    "ROUTE_SELECTED": ["AUTHORIZATION_COLLECTED", "USER_ACTION_REQUIRED", "FAILED"],
    "AUTHORIZATION_COLLECTED": ["PROVIDER_CONTACTED", "USER_AUTH_REQUIRED"],
    "USER_ACTION_REQUIRED": ["USER_AUTH_REQUIRED", "PROVIDER_CONTACTED", "ACCOUNT_DELETED_WITHOUT_CANCEL", "FAILED"],
    "USER_AUTH_REQUIRED": ["PROVIDER_CONTACTED", "FAILED"],
    "PROVIDER_CONTACTED": ["CANCELLATION_ACCEPTED", "PROVIDER_REJECTED", "RETENTION_OFFER_ACCEPTED", "PAUSED_OR_SKIPPED"],
    "PROVIDER_REJECTED": ["USER_ACTION_REQUIRED", "ROUTE_SELECTED", "FAILED"],
    "RETENTION_OFFER_ACCEPTED": [],
    "PAUSED_OR_SKIPPED": ["CANCEL_REQUESTED_BY_USER"],
    "ACCOUNT_DELETED_WITHOUT_CANCEL": ["ROUTE_SELECTED", "CHARGE_PERSISTED"],
    "CANCELLATION_ACCEPTED": ["CANCELLATION_SCHEDULED", "CANCELLATION_EFFECTIVE", "CHARGES_CONTINUE_BY_CONTRACT"],
    "CANCELLATION_SCHEDULED": ["CANCELLATION_EFFECTIVE", "CHARGES_CONTINUE_BY_CONTRACT"],
    "CHARGES_CONTINUE_BY_CONTRACT": ["CANCELLATION_EFFECTIVE"],
    "CANCELLATION_EFFECTIVE": ["VERIFICATION_PENDING", "CANCELLED_UNVERIFIED"],
    "VERIFICATION_PENDING": ["CHARGE_STOPPED", "CHARGE_PERSISTED", "CANCELLED_UNVERIFIED"],
    "CHARGE_STOPPED": [],
    "CHARGE_PERSISTED": ["PROVIDER_CONTACTED", "DISPUTE_REQUIRED"],
    "CANCELLED_UNVERIFIED": [],
    "DISPUTE_REQUIRED": [],
    "FAILED": [],
}

SUCCESS = {"CHARGE_STOPPED"}
NOT_SUCCESS_BUT_TERMINAL = {"RETENTION_OFFER_ACCEPTED", "CANCELLED_UNVERIFIED", "DISPUTE_REQUIRED", "FAILED"}

# Work-order edge cases -> how the model handles them (evidence where it exists)
EDGE_CASES = [
    ("Annual contract", "CHARGES_CONTINUE_BY_CONTRACT until term end; success test is 'no charge after term end' (R7-E-C05, R7-E-C08)"),
    ("Bundled subscription", "CONFIRMED_SUBSCRIPTION must name the bundle owner; cancelling one component may not stop the bundle charge (UNKNOWN; S4 gap)"),
    ("Family account", "The contract holder may not be the requesting user; route needs the holder (docomo family-only proxies: R7-E-C10)"),
    ("Unknown billing source", "Stays POSSIBLE_SUBSCRIPTION; aggregate descriptors (APPLE.COM/BILL, phone bill) block identification (R7-E-B06)"),
    ("Apple billing for a third-party service", "Route is Apple settings regardless of brand (RM01); provider site cannot cancel it (R7-E-C02, R7-E-C06)"),
    ("Trial", "Deadline before conversion; reminder (J1), not execution; Kokusen warning on auto-conversion (R7-E-A09)"),
    ("Cancellation window", "Deadline field per route (chocoZAP 10th; Oisix skip day-before 23:59; SoftBank 光 renewal month)"),
    ("Early termination fee", "Must be shown to the user before PROVIDER_CONTACTED (informed consent); Adobe 50%, SoftBank 光 fee (R7-E-C08, R7-E-C11)"),
    ("Pause instead of cancellation", "PAUSED_OR_SKIPPED is not success (chocoZAP 休会; Oisix skip: R7-E-C13, R7-E-C15)"),
    ("Retention offer", "RETENTION_OFFER_ACCEPTED only on explicit user decision; an agent must not accept on the user's behalf (design rule)"),
    ("Confirmation but another charge appears", "CHARGE_PERSISTED unless the contract explains it (CHARGES_CONTINUE_BY_CONTRACT); then DISPUTE_REQUIRED"),
    ("Provider cannot locate account", "PROVIDER_REJECTED → back to CONFIRMED_SUBSCRIPTION evidence; often the wrong rail (dアニメストア six windows: R7-E-C12)"),
    ("Multiple accounts", "One CONFIRMED_SUBSCRIPTION per account; detection must not merge them (UNKNOWN frequency)"),
    ("Merchant descriptor differs from brand", "POSSIBLE_SUBSCRIPTION until confirmed; descriptor normalisation is E2's question"),
    ("Account deleted / app deleted", "ACCOUNT_DELETED_WITHOUT_CANCEL; U-NEXT 退会 ≠ 解約; app deletion ≠ cancellation (R7-E-C02, R7-E-A09)"),
]


def reachable(start, blocked=frozenset()):
    seen = {start}
    q = deque([start])
    while q:
        s = q.popleft()
        for t in TRANSITIONS[s]:
            if t not in seen and t not in blocked:
                seen.add(t)
                q.append(t)
    return seen


def paths_avoid(start, goal, must_pass):
    """True if goal is reachable from start WITHOUT passing through must_pass."""
    return goal in reachable(start, blocked=frozenset({must_pass}))


def check():
    results = []
    ok = lambda name, cond: results.append((name, bool(cond)))
    ok("every state has a transition entry and a definition", set(STATES) == set(TRANSITIONS))
    ok("every transition target is a defined state", all(t in STATES for ts in TRANSITIONS.values() for t in ts))
    ok("CHARGE_STOPPED is unreachable without CANCELLATION_ACCEPTED", not paths_avoid("CANCEL_REQUESTED_BY_USER", "CHARGE_STOPPED", "CANCELLATION_ACCEPTED"))
    ok("CHARGE_STOPPED is unreachable without CANCELLATION_EFFECTIVE", not paths_avoid("CANCEL_REQUESTED_BY_USER", "CHARGE_STOPPED", "CANCELLATION_EFFECTIVE"))
    ok("CHARGE_STOPPED is unreachable without VERIFICATION_PENDING (a billing cycle observed)", not paths_avoid("CANCEL_REQUESTED_BY_USER", "CHARGE_STOPPED", "VERIFICATION_PENDING"))
    ok("CANCELLATION_EFFECTIVE is unreachable without PROVIDER_CONTACTED", not paths_avoid("CANCEL_REQUESTED_BY_USER", "CANCELLATION_EFFECTIVE", "PROVIDER_CONTACTED"))
    ok("no direct edge from request or acceptance to CHARGE_STOPPED",
       "CHARGE_STOPPED" not in TRANSITIONS["CANCEL_REQUESTED_BY_USER"] + TRANSITIONS["CANCELLATION_ACCEPTED"] + TRANSITIONS["PROVIDER_CONTACTED"])
    ok("pause/skip and account deletion are not success states", not ({"PAUSED_OR_SKIPPED", "ACCOUNT_DELETED_WITHOUT_CANCEL"} & SUCCESS))
    ok("contractual continuing charges are distinct from persisted charges", "CHARGES_CONTINUE_BY_CONTRACT" != "CHARGE_PERSISTED"
       and "CHARGE_PERSISTED" not in TRANSITIONS["CHARGES_CONTINUE_BY_CONTRACT"])
    ok("disputes are a hand-off terminal (J6 excluded)", TRANSITIONS["DISPUTE_REQUIRED"] == [])
    ok("every non-terminal state can still reach a terminal state", all(
        any(t in reachable(s) for t in SUCCESS | NOT_SUCCESS_BUT_TERMINAL | {"RETENTION_OFFER_ACCEPTED"}) for s in STATES if TRANSITIONS[s]))
    ok("success is reachable from a confirmed subscription", "CHARGE_STOPPED" in reachable("CONFIRMED_SUBSCRIPTION"))
    ok("every edge case is mapped", len(EDGE_CASES) == 15 and all(len(h) > 20 for _, h in EDGE_CASES))
    return results


if __name__ == "__main__":
    res = check()
    for name, passed in res:
        print(("PASS  " if passed else "FAIL  ") + name)
    print(f"{sum(p for _, p in res)}/{len(res)} passed; states={len(STATES)}; edge cases={len(EDGE_CASES)}")
    print("scope: structural invariants of a design artefact. They do not show that any route is executable or permitted.")
    sys.exit(0 if all(p for _, p in res) else 1)
