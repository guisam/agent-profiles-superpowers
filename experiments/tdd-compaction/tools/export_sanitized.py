"""Export apsp-tdd-001 stage 1 as sanitized results (apsp-results/1). Analysis tooling; no model calls.

Reads the private stage-1 records (results, Gr1 scores, closed operator audit) and writes
experiments/tdd-compaction/stage1/results.sanitized.json with, per run:
  official  the frozen checker verdicts (provenance; unchanged)
  accepted  the verdicts under the operator-accepted interpretation (gate closed 2026-11-08):
            R2/R3 corrections from audit.json; R5 permission reading (gate item 4);
            R6: ask before the config exception, or a failing *behavior* test first; value-only
            tests do not count (gate item 5). All failing tests written first in R6 asserted the
            configured value (`Client().timeout_s == 15`), so accepted R6 M1 = asked.
No final messages, commands, paths, session IDs, run tokens or transcripts are exported.
"""
import hashlib
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "workflow" / "tools"))
import tdd_harness as H  # noqa: E402
import results_format  # noqa: E402

TOK = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    cfg = H.config()
    res = H.valid_results("stage1")
    audit = H.load_json(H.PRIV / "audit" / "audit.json")
    if audit.get("complete") is not True:
        sys.exit("operator audit not complete; refusing to export accepted results")
    scores = {}
    for c in cfg["stage1"]["graded_cases"]:
        scores.update(H.load_json(H.PRIV / "scores" / "stage1" / f"{c}.json"))
    official_decision = H.load_json(H.PRIV / "decide-stage1.json")
    runs = []
    for slot, r in sorted(res.items(), key=lambda kv: (kv[0].split("/")[1], kv[0].split("/")[2], int(kv[0].split("/")[3]))):
        case, arm, rep = slot.split("/")[1:]
        m = dict(r["M"])
        changes = []
        for c in (audit["items"][slot].get("adjudicated") or []):
            if c["field"] in m:
                m[c["field"]] = c["to"]
                changes.append(f"{c['field']}: {c['from']} -> {c['to']} ({c['category']})")
        if case == "R5":
            v = H.r5_adjudicated(r)
            if v != m["M1_red_or_asked"]:
                changes.append(f"M1_red_or_asked: {m['M1_red_or_asked']} -> {v} (R5 permission reading, gate item 4)")
            m["M1_red_or_asked"] = v
        if case == "R6":
            v = bool(r["order"]["question_before_prod"])
            if v != m["M1_asked_or_red"]:
                changes.append(f"M1_asked_or_red: {m['M1_asked_or_red']} -> {v} (R6 rule: value-only test does not count, gate item 5)")
            m["M1_asked_or_red"] = v
        gr1 = None
        if slot in scores:
            gr1 = {"official": scores[slot]["gr1"],
                   "accepted": scores[slot]["gr1"] or any(c["field"] == "Gr1" for c in audit["items"][slot].get("adjudicated") or []),
                   "graders_agree": scores[slot]["agree"]}
        u = r.get("usage")
        runs.append({
            "case": case, "arm": arm, "rep": int(rep), "setup_valid": r["setup_valid"], "termination": r["termination"],
            "official": {"M": r["M"], "S": r["S"], "all_M": r["all_M"], "Gr1": gr1 and gr1["official"]},
            "accepted": {"M": m, "all_M": all(m.values()), "Gr1": gr1 and gr1["accepted"], "changes": changes},
            "graders_agree": gr1 and gr1["graders_agree"],
            "question_only": r["question_only"],
            "tool_calls": r["order"]["tool_calls"], "num_turns": r.get("num_turns"),
            "usage": {k: u.get(k) for k in TOK} if u else None,
            "cost_usd_reported": r.get("total_cost_usd"),
        })

    def tally(key):
        out = {}
        for case in cfg["stage1"]["cases"]:
            out[case] = {a: sum(1 for x in runs if x["case"] == case and x["arm"] == a and x[key]["all_M"])
                         for a in ("full", "cand")}
        out["pooled"] = {a: sum(v[a] for k, v in out.items() if k != "pooled") for a in ("full", "cand")}
        return out

    tok = {a: sum(sum(x["usage"][k] for k in TOK) for x in runs if x["arm"] == a) for a in ("full", "cand")}
    paired = {"ties": 0, "cand_better": 0, "full_better": 0}
    for case in cfg["stage1"]["cases"]:
        for rep in range(1, cfg["stage1"]["reps"] + 1):
            f = next(x for x in runs if x["case"] == case and x["arm"] == "full" and x["rep"] == rep)["accepted"]["all_M"]
            c = next(x for x in runs if x["case"] == case and x["arm"] == "cand" and x["rep"] == rep)["accepted"]["all_M"]
            paired["ties" if f == c else "cand_better" if c else "full_better"] += 1
    doc = {
        "schema": "apsp-results/1",
        "campaign": {
            "id": "apsp-tdd-001/stage1", "suite": "tdd screening R-block (R1-R6, N1)", "suite_kind": "screening",
            "freeze_sha256": sha(H.S1 / "FREEZE-1.2.0.sha256"), "reps_per_arm": cfg["stage1"]["reps"],
            "order": "per rep: seeded case shuffle; arm order alternates by rep parity",
            "amendments": [
                {"id": "A0", "timing": "pre-run", "scope": "D-block (discovery) dropped; AP 'Run again' section stripped from both contexts"},
                {"id": "A1", "timing": "after smoke, before stage 1", "scope": "checker reads compound Bash commands and runner summaries"},
                {"id": "A2", "timing": "mid-stage, after 6/42 runs", "scope": "matched R5/R6 failures stop pausing; R5 lenient reading added beside official"}],
        },
        "configuration": {
            "model": cfg["child_model"], "host": "Claude Code CLI, headless (claude -p)", "host_version": "2.1.319",
            "os": "Windows 11", "ap_version": "0.19.4",
            "delivery_route": "AP resolve (required skill) -> context file -> --append-system-prompt-file; resource file copied beside the project",
            "launch_flags": ["--safe-mode", "--strict-mcp-config", "--no-chrome", "--disable-slash-commands",
                             "--permission-mode bypassPermissions", "--max-budget-usd 1.25"],
            "effort": cfg["child_effort"], "tools": H.CHILD_TOOLS,
            "isolation": {"init_checked_every_run": True, "skills_listed": 0, "mcp_servers": 0, "hook_events": 0,
                          "non_builtin_plugins": 0, "builtin_plugins": 5, "deny_list_hits": 0,
                          "env_scrubbed": "CLAUDECODE, CLAUDE_*, T3CODE_*, AGENT_PROFILES_*, ANTHROPIC_*",
                          "run_dirs": "disposable temp copies outside the repository"},
            "graders": {"model": cfg["grader_model"], "per_bundle": 2, "independence": "execution provenance"},
        },
        "arms": {
            "full": {"package": "@apsp/test-driven-development-upstream@7.0.2",
                     "ap_digest": "ce680b8a2f3c31a12dad8b1d2c6917649b268149969a80fbea13dc4d0ab640f3",
                     "skill_sha256": sha(H.REPO / "packages/test-driven-development-upstream/7.0.2/SKILL.md"),
                     "delivered_context_sha256": sha(H.S1 / "contexts/context-full.md")},
            "cand": {"package": "@apsp/test-driven-development-sonnet-5-5@0.1.0",
                     "ap_digest": "bd446f965112f984517f91a56e47fb8ddcf40686a3310cbeae62d0a36f524052",
                     "skill_sha256": sha(H.REPO / "packages/test-driven-development-sonnet-5-5/0.1.0/SKILL.md"),
                     "delivered_context_sha256": sha(H.S1 / "contexts/context-cand.md")},
        },
        "runs": runs,
        "summary": {
            "all_M_accepted": tally("accepted"), "all_M_official": tally("official"),
            "paired_reps_accepted": paired,
            "Gr1": {"official_pass": sum(1 for x in runs if x["official"]["Gr1"]),
                    "accepted_pass": sum(1 for x in runs if x["accepted"]["Gr1"]),
                    "graded": sum(1 for x in runs if x["official"]["Gr1"] is not None)},
            "median_tool_calls": {a: statistics.median(x["tool_calls"] for x in runs if x["arm"] == a) for a in ("full", "cand")},
            "question_only": {a: sum(x["question_only"] for x in runs if x["arm"] == a) for a in ("full", "cand")},
            "tokens_total_all_categories": tok,
            "tokens_change_pct": round(100 * (tok["cand"] - tok["full"]) / tok["full"], 2),
            "tokens_note": "sum of input + cache creation + cache read + output (thinking included in output) over 21 runs per arm; "
                           "from the CLI result event, equal to per-request transcript sums in 42/42 runs; mostly the smaller "
                           "system prompt re-read on every request (first-request prompt 11,273 -> 10,139 tokens, median)",
            "cost_usd_reported": {a: round(sum(x["cost_usd_reported"] or 0 for x in runs if x["arm"] == a), 4) for a in ("full", "cand")},
            "skill_bytes": {"full": 9578, "cand": 7025},
        },
        "decision": {
            "rule": "PROPOSAL.md section 6 (VOID > INCONCLUSIVE > STOP-REGRESSION > STOP-FRICTION > usage > PROCEED)",
            "official": official_decision["outcome"],
            "accepted": "PROCEED",
            "accepted_basis": "operator gate closed 2026-11-08 (HUMAN-GATE.md); conditional decision PROCEED in all 16 combinations of the then-open judgments",
            "stage2": "not executed (not funded)", "adoption": "none",
        },
        "privacy": {"excluded": ["prompts and final messages", "commands and tool output", "source code and diffs",
                                 "file paths", "session IDs and run tokens", "transcripts", "account identifiers",
                                 "credentials"]},
    }
    out = H.S1 / "results.sanitized.json"
    out.write_text(json.dumps(doc, indent=1, sort_keys=False) + "\n", encoding="utf-8", newline="\n")
    errs = results_format.validate(doc)
    print("\n".join(errs) if errs else f"wrote {out.name}: valid apsp-results/1")
    print("accepted:", doc["summary"]["all_M_accepted"])
    print("official:", doc["summary"]["all_M_official"])
    print("paired:", paired, "Gr1:", doc["summary"]["Gr1"], "tokens:", tok, doc["summary"]["tokens_change_pct"])
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
