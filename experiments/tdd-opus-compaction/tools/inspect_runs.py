"""Print compact evidence for selected apsp-tdd-002 stage-1 runs (read-only audit aid).
Usage: python -I inspect_runs.py <case> [<case> ...]"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import opus_harness as O  # noqa: E402

H = O.H
res = H.valid_results("stage1")
for slot in sorted(res):
    if slot.split("/")[1] not in sys.argv[1:]:
        continue
    r = res[slot]
    ann = H.load_json(H.RUNS / r["token"] / "events.json")
    print("=" * 8, slot, r["token"], "M", r["M"], "S", r["S"], "changed", r["tree"]["changed"],
          "unknown", r["order"]["unknown_run_outcomes"])
    for e in ann:
        if e["kind"] == "text":
            print("   TEXT", e["text"][:220].replace("\n", " / "))
            continue
        s = e["input"].get("command") or e["input"].get("file_path") or ""
        s = s.replace("\\", "/").split("/project/")[-1] if "/project/" in s.replace("\\", "/") else s
        extra = ""
        if e["name"] in ("Write", "Edit"):
            extra = " :: " + (e["input"].get("content") or e["input"].get("new_string") or "")[:160].replace("\n", " ")
        print(f"   {e['i']:2} {e['name']:5} {str(e.get('cls')):14} fail={e.get('run_failed')} {s[-170:]!r}{extra}")
    print("   FINAL:", r["final_text"][-420:].replace("\n", " / "))
