"""Agent-audit RED replay (read-only analysis tooling): for every R1/R3/R4 run, copy the frozen
fixture project (original production code), overlay the run's final test files, run the suite,
and record whether it fails and whether the failure names the new function. This approximates the
RED state using final test files; runs whose test files changed after the RED run are marked.
Writes private/tdd001/audit/red-replay.json."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

NEW = {"R1": "slugify", "R3": "chunk", "R4": "overdue_titles"}


def main():
    disp = {e["token"]: e for e in H.ledger_read() if e["event"] == "dispatch" and e["kind"] == "child"}
    out = {}
    for slot, r in sorted(H.valid_results("stage1").items()):
        case = slot.split("/")[1]
        if case not in NEW:
            continue
        final = Path(disp[r["token"]]["run_root"]) / "project"
        ann = H.load_json(H.RUNS / r["token"] / "events.json")
        red_i = r["order"]["red_event"]
        test_edits_after_red = [e["i"] for e in ann if e.get("cls") == "test_edit" and red_i is not None and e["i"] > red_i]
        with tempfile.TemporaryDirectory(prefix="apsp-tdd-replay-") as td:
            work = Path(td) / "p"
            shutil.copytree(H.S1 / "fixtures" / case / "project", work)
            for p in r["tree"]["changed"]:
                if H.is_test_path(p) and (final / p).exists():
                    (work / p).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(final / p, work / p)
            p = subprocess.run([sys.executable, "-m", "unittest"], cwd=work, capture_output=True, text=True)
            log = p.stdout + p.stderr
        names_new = bool(re.search(rf"(cannot import name '{NEW[case]}'|has no attribute '{NEW[case]}'|"
                                   rf"name '{NEW[case]}' is not defined)", log))
        out[slot] = {"token": r["token"], "replay_fails": p.returncode != 0, "failure_names_new_function": names_new,
                     "assertion_failure": bool(re.search(r"AssertionError", log)),
                     "test_edits_after_red_run": test_edits_after_red,
                     "log_tail": "\n".join(log.strip().splitlines()[-6:])}
    H.dump_json(H.PRIV / "audit" / "red-replay.json", out)
    for s, v in out.items():
        print(f"{s:18} fails={v['replay_fails']!s:5} names_new={v['failure_names_new_function']!s:5} "
              f"test_edits_after_red={v['test_edits_after_red_run']}")


if __name__ == "__main__":
    main()
