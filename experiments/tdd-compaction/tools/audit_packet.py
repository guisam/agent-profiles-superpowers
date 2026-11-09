"""Build the apsp-tdd-001 stage-1 operator audit packet (PROPOSAL §7). Analysis tooling only:
reads the ledger, results and scores; writes private/tdd001/audit/AUDIT-PACKET.md and an
audit.json template (complete: false). Never changes any result.
Usage: python -I audit_packet.py
"""
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

MASK = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/]+[\\/]+AppData[\\/]+Local[\\/]+Temp[\\/]+apsp-tdd[\\/]+[0-9a-f]{8}[\\/]*")


def mask(s):
    return MASK.sub("<run>/", s or "")


def events_md(token):
    ann = H.load_json(H.RUNS / token / "events.json")
    out, seen = [], set()
    for e in ann:
        if e["kind"] == "text":
            out.append(f"  - *text:* {mask(e['text'])[:300]!s}".replace("\n", " "))
            continue
        cls = e.get("cls") or ""
        rf = "" if e.get("run_failed") is None and cls not in ("test_run", "test_run_full") else f" failed={e.get('run_failed')}"
        key = (e.get("id"), cls, e.get("rel"))
        if key in seen:
            continue
        seen.add(key)
        if e["name"] == "Bash":
            cmd = mask(e["input"].get("command", "")).replace("\n", " ⏎ ")
            out.append(f"  - `{cls or 'bash'}`{rf}{' (shell write: ' + e['rel'] + ')' if e.get('shell_write') else ''}: `{cmd[-240:]}`")
        else:
            out.append(f"  - `{cls or e['name']}`: {e['name']} {mask(e['input'].get('file_path', ''))}")
    return "\n".join(out)


def main():
    cfg = H.config()
    res = H.valid_results("stage1")
    scores = {}
    for c in cfg["stage1"]["graded_cases"]:
        p = H.PRIV / "scores" / "stage1" / f"{c}.json"
        if p.exists():
            scores.update(H.load_json(p))
    items = {}

    def add(slot, why):
        items.setdefault(slot, []).append(why)

    for s, r in res.items():
        case, arm, rep = s.split("/")[1:]
        if arm == "cand" and not r["all_M"]:
            add(s, "candidate M failure: " + ", ".join(k for k, v in r["M"].items() if not v))
        if case in ("R5", "R6"):
            add(s, f"{case} M1 outcome (both arms audited)")
        if r["question_only"]:
            add(s, "question-detector hit")
        if r["order"]["unknown_run_outcomes"]:
            add(s, f"unknown run outcome(s) at events {r['order']['unknown_run_outcomes']}")
        if r["order"]["outside_edits"]:
            add(s, "edit outside the project")
        if rep == "1":
            add(s, "rep-1 run (all audited)")
        sc = scores.get(s)
        if sc and not sc["agree"]:
            add(s, "grader disagreement")
        if sc and not sc["gr1"]:
            add(s, "Gr1 fail")
    notes = {
        "stage1/R3/full/1": "Coordinator note: hidden test `test_returns_lists` passes a tuple; the request says "
                            "'splits a list'. Over-specified hidden test (fixture flaw, control side).",
        "stage1/R2/cand/1": "Coordinator note: Gr1 cites a missing '199 vs 597' failure; it is in the full pre-fix run "
                            "output (41 lines), outside the 12-line packet tail. Likely tail artifact.",
        "stage1/R2/full/1": "Coordinator note: g2 cites a missing dates test name; it is in the full output, outside "
                            "the packet tail. Likely tail artifact.",
        "stage1/R2/full/2": "Coordinator note: the claim that the dates failure 'was there before my change' has no "
                            "pre-fix run showing dates. Appears genuinely unsupported.",
    }
    for s in res:
        if s.split("/")[1] == "R2":
            notes.setdefault(s, "Coordinator note: R2 runs grep their test output; Node 24 prints `ℹ fail N`, which the "
                                "agents' grep for `# fail` removes, so run outcomes are `unknown` and never count as RED "
                                "(Amendment 1). M2 (and M5 where the final full run was grepped) is false for that reason.")
    buf = io.StringIO()
    w = buf.write
    w("# apsp-tdd-001 stage-1 operator audit packet\n\n")
    w("Private. Arms are shown because the auditor adjudicates checker verdicts, not preferences. For each item, "
      "record in `audit.json` whether the official verdict stands and, if not, the adjudicated verdict and why. "
      "Official outcomes are never overwritten (PROPOSAL §7).\n\n")
    w(f"Items: {len(items)} runs. Valid stage-1 runs: {len(res)}/42.\n\n")
    template = {"complete": False, "auditor": "", "date": "", "items": {}}
    for s in sorted(items):
        r = res[s]
        w(f"## {s} (`{r['token']}`)\n\n")
        w("- **Why audited:** " + "; ".join(items[s]) + "\n")
        w(f"- **M:** {r['M']}  **S:** {r['S']}  all-M: {r['all_M']}\n")
        w(f"- **Changed files:** {r['tree']['changed']}\n")
        if s in scores:
            sc = scores[s]
            w(f"- **Gr1:** {'pass' if sc['gr1'] else 'fail'} (g1 {sc['g1']['gr1']}: {sc['g1']['reason']} | "
              f"g2 {sc['g2']['gr1']}: {sc['g2']['reason']})\n")
        if s in notes:
            w(f"- {notes[s]}\n")
        w("- **Events:**\n" + events_md(r["token"]) + "\n")
        w("- **Final message:**\n\n" + "\n".join("  > " + l for l in mask(r["final_text"]).splitlines()) + "\n\n")
        template["items"][s] = {"official_stands": None, "adjudicated": None, "why": ""}
    out = H.PRIV / "audit"
    out.mkdir(parents=True, exist_ok=True)
    (out / "AUDIT-PACKET.md").write_text(buf.getvalue(), encoding="utf-8", newline="\n")
    if not (out / "audit.json").exists():
        H.dump_json(out / "audit.json", template)
    print(f"wrote {out / 'AUDIT-PACKET.md'} ({len(items)} items)")


if __name__ == "__main__":
    main()
