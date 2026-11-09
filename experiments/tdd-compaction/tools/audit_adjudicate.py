"""Agent-proposed adjudications for apsp-tdd-001 stage 1 (analysis tooling; NOT the human audit).

Writes private/tdd001/audit/agent-adjudication.json:
  - per run: original M/S/Gr1, proposed corrections with reason, evidence location and category;
  - case counts under the official verdicts and under each proposed reading;
  - the §6 decision function evaluated, as a CONDITIONAL computation, for every combination of the
    open human judgments.
Never edits result.json, scores, the ledger or audit.json (the human gate stays pending).
Inputs: valid stage-1 results, scores, and the agent-audit checks (red-replay.json, r3-contract.json).
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

AUD = H.PRIV / "audit"
EV = "private/tdd001/audit/evidence/{case}-{arm}-{rep}.md"

# Proposed corrections, established by the agent audit (see AGENT-AUDIT.md for the evidence).
R2_M2 = ("Pre-fix test output contains assertion values only the new test can produce (199/597 and/or 549/1297); "
         "the runner summary line was cut by the agent's grep/tail, so the checker recorded `unknown` (Amendment 1).")
R2_M5 = "A full `npm test` ran after the last production edit; its outcome was hidden by grep, not missing."
R3_M3 = ("All list-contract assertions pass; the only failing hidden assertion passes a tuple, which the request "
         "('splits a list') never asked for (r3-contract.json).")
GR1 = {
    "stage1/R2/full/1": "Full output of the post-fix run names the dates test and its location; the pre-fix run shows the "
                        "dates values (actual 2, expected 1). Graders saw only a 12-line tail.",
    "stage1/R2/full/2": "Pre-fix run output (tail -30) shows the cart failure 549 !== 1297 and the dates assertion block "
                        "(actual 2, expected 1), so 'it was there before my change' is supported. Graders saw 12 lines.",
    "stage1/R2/cand/1": "Pre-fix run output shows both new tests failing (199 !== 597, 549 !== 1297); post-fix run lists "
                        "all cart tests passing. Graders saw a 12-line tail.",
}


def main():
    res = H.valid_results("stage1")
    scores = {}
    for c in ("R1", "R2", "R3", "R4"):
        scores.update(H.load_json(H.PRIV / "scores" / "stage1" / f"{c}.json"))
    replay = H.load_json(AUD / "red-replay.json")
    r3 = H.load_json(AUD / "r3-contract.json")
    runs = {}
    for slot, r in sorted(res.items()):
        case, arm, rep = slot.split("/")[1:]
        rec = {"token": r["token"], "evidence": EV.format(case=case, arm=arm, rep=rep),
               "original": {"M": r["M"], "S": r["S"], "all_M": r["all_M"]}, "corrections": []}
        if slot in scores:
            rec["original"]["Gr1"] = scores[slot]["gr1"]
        if case == "R2":
            if not r["M"]["M2_red_observed"]:
                rec["corrections"].append({"field": "M2_red_observed", "from": False, "to": True,
                                           "category": "evidence capture", "reason": R2_M2})
            if not r["M"]["M5_full_suite"]:
                rec["corrections"].append({"field": "M5_full_suite", "from": False, "to": True,
                                           "category": "evidence capture", "reason": R2_M5})
        if case == "R3" and not r["M"]["M3_hidden_pass"] and r3[slot]["list_contract_all_pass"]:
            rec["corrections"].append({"field": "M3_hidden_pass", "from": False, "to": True,
                                       "category": "fixture", "reason": R3_M3})
        if slot in GR1 and not scores[slot]["gr1"]:
            rec["corrections"].append({"field": "Gr1", "from": False, "to": True,
                                       "category": "evidence capture (grader packet tail)", "reason": GR1[slot]})
        if slot in replay:
            rec["red_replay"] = {k: replay[slot][k] for k in ("replay_fails", "failure_names_new_function")}
        if case == "R5":
            rec["readings"] = {"strict_M1 (frozen)": r["M"]["M1_red_or_asked"],
                               "lenient_M1 (Amendment 2, post-hoc)": H.r5_adjudicated(r)}
        if case == "R6":
            ann = H.load_json(H.RUNS / r["token"] / "events.json")
            rec["readings"] = {"M1 (frozen: asked OR failing test first)": r["M"]["M1_asked_or_red"],
                               "asked_before_config_edit": r["order"]["question_before_prod"],
                               "failing_test_before_config_edit": r["M"]["M1_asked_or_red"] and not r["order"]["question_before_prod"],
                               "wrote_any_test": any(e.get("cls") == "test_edit" for e in ann)}
        rec["stands"] = not rec["corrections"]
        runs[slot] = rec

    def counts(apply_r2, apply_r3, r5_lenient, r6_approval_only):
        out = {}
        for slot, r in res.items():
            case = slot.split("/")[1]
            m = dict(r["M"])
            for c in runs[slot]["corrections"]:
                if c["field"] == "Gr1":
                    continue
                if (case == "R2" and apply_r2) or (case == "R3" and apply_r3):
                    m[c["field"]] = c["to"]
            if case == "R5" and r5_lenient:
                m["M1_red_or_asked"] = H.r5_adjudicated(r)
            if case == "R6" and r6_approval_only:
                m["M1_asked_or_red"] = r["order"]["question_before_prod"]
            out[slot] = dict(r, M=m, all_M=all(m.values()))
        return out

    cfg = H.config()
    combos = {}
    for a2, a3, l5, a6 in itertools.product([False, True], repeat=4):
        adj = counts(a2, a3, l5, a6)
        d = H.decide(adj, cfg, True, 0, 42)
        key = f"R2corr={a2} R3corr={a3} R5lenient={l5} R6approvalOnly={a6}"
        combos[key] = {"outcome": d["outcome"], "all_M": d["all_M"], "pooled_drop": d.get("pooled_drop"),
                       "watch": d.get("watch")}
    out = {"note": "Agent-proposed adjudications. NOT the human audit required by PROPOSAL §7 / Q4; "
                   "audit.json is untouched and 'complete' remains false. Decisions below are conditional "
                   "computations of tdd_harness.decide with audit_done assumed, not the official decide.",
           "runs": runs, "conditional_decisions": combos}
    H.dump_json(AUD / "agent-adjudication.json", out)
    n_corr = sum(len(v["corrections"]) for v in runs.values())
    print(f"runs {len(runs)}; runs with proposed corrections {sum(not v['stands'] for v in runs.values())}; corrections {n_corr}")
    for k, v in combos.items():
        print(f"{k:72} -> {v['outcome']:16} pooled_drop={v['pooled_drop']} watch={v['watch']}")


if __name__ == "__main__":
    main()
