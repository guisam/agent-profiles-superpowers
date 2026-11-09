"""Agent-audit evidence dump for apsp-tdd-001 stage 1 (read-only analysis tooling).

For every valid stage-1 run, writes private/tdd001/audit/evidence/<case>-<arm>-<rep>.md with:
every tool call in order (full command / file path), the complete tool output for every Bash
call, the full content of Write/Edit inputs, the final message, and the final-tree diff against
the fixture's initial commit. Never modifies results, ledger, transcripts or trees.
Usage: python -I audit_dump.py
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

MASK = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/]+[\\/]+AppData[\\/]+Local[\\/]+Temp[\\/]+apsp-tdd[\\/]+[0-9a-f]{8}[\\/]*")
MASK2 = re.compile(r"/c/Users/[^/]+/AppData/Local/Temp/apsp-tdd/[0-9a-f]{8}/?")


def mask(s):
    return MASK2.sub("<run>/", MASK.sub("<run>/", s or ""))


def main():
    out = H.PRIV / "audit" / "evidence"
    out.mkdir(parents=True, exist_ok=True)
    disp = {e["token"]: e for e in H.ledger_read() if e["event"] == "dispatch" and e["kind"] == "child"}
    for slot, r in sorted(H.valid_results("stage1").items()):
        d = disp[r["token"]]
        project = Path(d["run_root"]) / "project"
        init, events, result = H.parse_stream((H.RUNS / r["token"] / "stream.jsonl").read_text(encoding="utf-8").splitlines())
        lines = [f"# {slot} (`{r['token']}`)\n", f"Official M: {r['M']}  S: {r['S']}\n",
                 f"Evidence: private/tdd001/runs/{r['token']}/stream.jsonl, transcript.jsonl, events.json; "
                 f"final tree {mask(str(project))}\n"]
        n = 0
        for e in events:
            if e["kind"] == "text":
                lines.append(f"\n### text\n\n{mask(e['text'])}\n")
                continue
            n += 1
            inp = e["input"]
            if e["name"] == "Bash":
                lines.append(f"\n### call {n}: Bash (tool exit {e['exit']})\n\n```sh\n{mask(inp.get('command', ''))}\n```\n"
                             f"\nOutput:\n\n```\n{mask(e['output'])}\n```\n")
            elif e["name"] in ("Write", "Edit", "MultiEdit"):
                body = inp.get("content") if e["name"] == "Write" else \
                    f"--- old\n{inp.get('old_string', '')}\n+++ new\n{inp.get('new_string', '')}"
                lines.append(f"\n### call {n}: {e['name']} {mask(inp.get('file_path', ''))}\n\n```\n{mask(body)}\n```\n")
            else:
                lines.append(f"\n### call {n}: {e['name']} {mask(str(inp)[:300])}\n")
        diff = subprocess.run(["git", "diff", d["base_sha"], "--", ".", ":(exclude)*__pycache__*"], cwd=project,
                              capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=project,
                                   capture_output=True, text=True).stdout.split()
        untracked = [u for u in untracked if "__pycache__" not in u]
        for u in untracked:
            diff += f"\n--- /dev/null (untracked)\n+++ {u}\n" + (project / u).read_text(encoding="utf-8", errors="replace")
        lines.append(f"\n## Final diff vs fixture\n\n```diff\n{mask(diff)}\n```\n")
        lines.append(f"\n## Final message\n\n{mask(r['final_text'])}\n")
        case, arm, rep = slot.split("/")[1:]
        (out / f"{case}-{arm}-{rep}.md").write_text("".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {len(list(out.glob('*.md')))} evidence files to {out}")


if __name__ == "__main__":
    main()
