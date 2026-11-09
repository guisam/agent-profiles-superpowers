"""Agent-audit usage verification (read-only analysis tooling).

1. For every stage-1 run, compare the stream `result.usage` totals with the sum of per-request
   usage in the transcript (deduplicated by message id), to establish what `usage` covers.
2. Sum each usage category per arm and per case; compute the reduction per category.
3. Compare with the expected effect of the smaller system-prompt context.
Writes private/tdd001/audit/usage.json. Missing usage is reported as missing, never zero."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

CATS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def transcript_usage(path):
    seen, tot, n = set(), {c: 0 for c in CATS}, 0
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("type") != "assistant":
            continue
        m = r.get("message", {})
        mid = m.get("id")
        if mid in seen or not m.get("usage"):
            continue
        seen.add(mid)
        n += 1
        for c in CATS:
            tot[c] += m["usage"].get(c, 0) or 0
    return tot, n


def main():
    res = H.valid_results("stage1")
    per_arm = {a: {c: 0 for c in CATS} for a in ("full", "cand")}
    per_case = {}
    requests = {"full": 0, "cand": 0}
    missing, mismatch = [], []
    cost = {"full": 0.0, "cand": 0.0}
    for slot, r in sorted(res.items()):
        case, arm = slot.split("/")[1:3]
        u = r.get("usage")
        if not u:
            missing.append(slot)
            continue
        t, n = transcript_usage(H.RUNS / r["token"] / "transcript.jsonl")
        requests[arm] += n
        if any(t[c] != (u.get(c) or 0) for c in CATS):
            mismatch.append({"slot": slot, "result": {c: u.get(c) for c in CATS}, "transcript": t})
        for c in CATS:
            per_arm[arm][c] += u.get(c) or 0
            per_case.setdefault(case, {"full": 0, "cand": 0})[arm] += u.get(c) or 0
        cost[arm] += r.get("total_cost_usd") or 0
    tot = {a: sum(v.values()) for a, v in per_arm.items()}
    ctx = {a: len((H.S1 / "contexts" / f"context-{a}.md").read_bytes()) for a in ("full", "cand")}
    out = {
        "runs_with_usage": len(res) - len(missing), "runs_missing_usage": missing,
        "result_vs_transcript_mismatches": mismatch,
        "per_arm": per_arm, "total_all_categories": tot,
        "reduction_total_pct": round(100 * (tot["full"] - tot["cand"]) / tot["full"], 2),
        "reduction_by_category_pct": {c: round(100 * (per_arm["full"][c] - per_arm["cand"][c]) / per_arm["full"][c], 2)
                                      for c in CATS if per_arm["full"][c]},
        "api_requests": requests,
        "per_case_total": per_case,
        "cli_cost_usd": {a: round(v, 4) for a, v in cost.items()},
        "context_bytes": ctx,
        "context_bytes_saved": ctx["full"] - ctx["cand"],
    }
    H.dump_json(H.PRIV / "audit" / "usage.json", out)
    print(json.dumps({k: v for k, v in out.items() if k != "per_case_total"}, indent=1))
    print("per case:", {c: (v["full"], v["cand"], round(100 * (v["full"] - v["cand"]) / v["full"], 1)) for c, v in per_case.items()})


if __name__ == "__main__":
    main()
