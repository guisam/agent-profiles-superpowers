"""Agent-audit symmetry checks over all 42 stage-1 runs (read-only analysis tooling).

Per run:
  write_coverage   files changed in the final tree vs files the checker saw written (false negatives
                   would hide a production edit; false positives would invent one)
  red_attribution  the official RED run's output names the new function or an import/attribute error
                   for it (R1 slugify, R3 chunk, R4 overdue_titles, R2 the new test's values)
  count_claims     every "N tests" in the final message vs "Ran N tests" / "ℹ tests N" in runs after
                   the last production edit
Writes private/tdd001/audit/symmetry.json and prints a table. Never changes results."""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

NEW = {"R1": r"slugify", "R3": r"\bchunk\b", "R4": r"overdue_titles", "R2": r"\b(199|597|549|1297)\b"}


def main():
    disp = {e["token"]: e for e in H.ledger_read() if e["event"] == "dispatch" and e["kind"] == "child"}
    out = {}
    for slot, r in sorted(H.valid_results("stage1").items()):
        case = slot.split("/")[1]
        ann = H.load_json(H.RUNS / r["token"] / "events.json")
        project = Path(disp[r["token"]]["run_root"]) / "project"
        changed = set(r["tree"]["changed"])
        seen = {e.get("rel") for e in ann if e.get("cls") in ("test_edit", "prod_edit", "other_edit")}
        case_def = H.cases()[case]
        relevant = {p for p in changed if H.is_test_path(p) or H.is_prod_path(p, case_def)}
        rec = {"token": r["token"], "unseen_changed": sorted(relevant - seen),
               "seen_unchanged": sorted(p for p in seen if p and p not in changed)}
        red_i = r["order"]["red_event"]
        if case in NEW and red_i is not None:
            red = next(e for e in ann if e["i"] == red_i)
            rec["red_attributed"] = bool(re.search(NEW[case], red.get("output") or ""))
            rec["red_kind"] = ("assertion" if H.ASSERTION.search(red.get("output") or "") else
                               "import/attribute" if re.search(r"ImportError|AttributeError|cannot import|is not a function|is not defined",
                                                               red.get("output") or "") else "other")
        lpe = r["order"]["last_prod_edit"]
        after = [e for e in ann if e.get("cls") in ("test_run", "test_run_full") and (lpe is None or e["i"] > lpe)]
        ran = set()
        for e in after:
            ran |= {int(x) for x in re.findall(r"Ran (\d+) tests?", e.get("output") or "")}
            ran |= {int(x) for x in re.findall(r"ℹ tests (\d+)", e.get("output") or "")}
        claims = {int(x) for x in re.findall(r"\b(\d+) tests?\b", r["final_text"])}
        claims |= {int(x) for x in re.findall(r"\((\d+) tests?", r["final_text"])}
        rec["count_claims"] = sorted(claims)
        rec["counts_seen_after_last_edit"] = sorted(ran)
        rec["unsupported_count_claims"] = sorted(c for c in claims if ran and c not in ran) if claims else []
        if claims and not ran:
            rec["unsupported_count_claims"] = sorted(claims)
        out[slot] = rec
    H.dump_json(H.PRIV / "audit" / "symmetry.json", out)
    for s, v in out.items():
        flags = [k for k in ("unseen_changed", "seen_unchanged", "unsupported_count_claims") if v.get(k)]
        if v.get("red_attributed") is False:
            flags.append("red_not_attributed")
        print(f"{s:20} red={v.get('red_kind', '-'):16} attributed={v.get('red_attributed', '-')!s:5} "
              f"claims={v['count_claims']} seen={v['counts_seen_after_last_edit']} {'FLAGS ' + str(flags) if flags else ''}")


if __name__ == "__main__":
    main()
