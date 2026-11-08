"""Prepare, prompt and collect brainstorming trial runs (see ../PROTOCOL.md).

  python -I collect.py prepare <case> <arm> <rep>   -> prints run id, copies fixture
  python -I collect.py prompt <run-id>              -> prints the exact child prompt
  python -I collect.py collect <run-id> <agent-id>  -> copies transcript, writes result.json
  python -I collect.py selftest
"""
import hashlib, json, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
COMPANION = SUITE.parent.parent
PRIVATE = COMPANION / "private"
RUNS = PRIVATE / "runs"
LEDGER = SUITE / "runs.jsonl"
CONSUMERS = {"full": PRIVATE / "consumers" / "alpha", "cand": PRIVATE / "consumers" / "beta"}
STORE = PRIVATE / "store"
TRUST = PRIVATE / "trust.trial.yaml"  # trial-scoped AP policy, see PROTOCOL.md
EXPERIMENT = "apsp-bs-001"
# Claude Code keeps subagent transcripts per parent session; override with APSP_TRANSCRIPTS.
TRANSCRIPTS = Path.home() / ".claude" / "projects" / "c--workspace-agent-profiles-superpowers"


def cases():
    return {c["id"]: c for c in json.loads((SUITE / "cases.json").read_text("utf-8"))["cases"]}


def tree_hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def ledger(entry):
    entry["at"] = datetime.now(timezone.utc).isoformat()
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_id(case, arm, rep):
    return f"{EXPERIMENT}.{case}.{arm}.r{rep}"


def parse(run):
    case, arm, rep = run.split(".")[1:4]
    return case, arm, int(rep[1:])


def prepare(case, arm, rep):
    assert case in cases() and arm in CONSUMERS
    rid = run_id(case, arm, rep)
    d = RUNS / rid
    if d.exists():
        sys.exit(f"{rid} already prepared; runs are never reused")
    shutil.copytree(SUITE / "fixture", d / "project")
    ledger({"event": "planned", "run": rid, "experiment": EXPERIMENT, "case": case, "arm": arm,
            "rep": rep, "role": "brainstormer", "consumer": CONSUMERS[arm].name})
    print(rid)


def prompt(rid):
    case, arm, _ = parse(rid)
    c = cases()[case]
    convo = "\n\n".join(f"[{t['role']}]\n{t['text']}" for t in c["conversation"])
    d = RUNS / rid
    return f"""You are taking part in a recorded evaluation run {rid}. Follow these steps exactly.

1. Setup. Run this exact command in Bash and follow its output for the rest of this task:

   cd "{CONSUMERS[arm].as_posix()}" && AGENT_PROFILES_TRUST="{TRUST.as_posix()}" npx --no agent-profiles resolve --store "{STORE.as_posix()}" --host claude --identity-source host-stated --model "<your exact model ID>" --role brainstormer

   Use the exact model ID your host states for you. If the command fails or its output lacks the final `End of Agent Profiles context:` line, write SETUP-FAILED and the error to the reply file below and stop.

2. Act as the assistant in the conversation below. The user's project is the directory {(d / 'project').as_posix()} . Treat that directory as the project root. You may read it and use tools as the delivered instructions and the conversation call for. Do not start servers or run the skill's scripts. You cannot reach the user: produce exactly ONE next assistant message, the one you would send now.

3. Write that message, verbatim and nothing else, to {(d / 'reply.md').as_posix()} .

4. Return only this line: done {rid} model=<your exact model ID>

Conversation so far:

{convo}
"""


def tool_events(rows):
    uses, results = [], {}
    for r in rows:
        content = (r.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if b.get("type") == "tool_use":
                uses.append(b)
            elif b.get("type") == "tool_result":
                c = b.get("content")
                results[b.get("tool_use_id")] = c if isinstance(c, str) else json.dumps(c)
    return uses, results


def variant(text):
    """Which SKILL.md body a resolve output carried. Text output names no package, so use the two deletions."""
    a = "Read from how they\ntalk which" in text
    b = "Requirements, scope, tradeoffs, and conceptual choices stay in text." in text
    if a and b:
        return "full"
    if not a and not b and "piece of art. Someone who\ntalks about outcomes" in text:
        return "cand"
    return "unknown"


def analyze(rows):
    usage, models = {}, set()
    for r in rows:
        m = r.get("message") or {}
        if r.get("type") == "assistant" and m.get("usage"):
            usage[m.get("id") or r.get("uuid")] = m["usage"]  # streamed rows repeat one message's usage
            models.add(m.get("model"))
    tot = {k: sum(u.get(k, 0) for u in usage.values()) for k in
           ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")}
    tot["thinking_tokens_within_output"] = sum((u.get("output_tokens_details") or {}).get("thinking_tokens", 0)
                                               for u in usage.values())
    uses, results = tool_events(rows)
    resolves = [u for u in uses if u.get("name") == "Bash" and "agent-profiles resolve" in u["input"].get("command", "")]
    rout = [results.get(u["id"], "") for u in resolves]
    ok = [o for o in rout if "End of Agent Profiles context:" in o and "Withheld by the trust policy" not in o
          and "## Required skill: brainstorming" in o]
    stamps = [r.get("timestamp") for r in rows if r.get("timestamp")]
    elapsed = None
    if len(stamps) > 1:
        t = [datetime.fromisoformat(s.replace("Z", "+00:00")) for s in (min(stamps), max(stamps))]
        elapsed = int((t[1] - t[0]).total_seconds() * 1000)
    cmds = [u["input"].get("command", "") for u in uses if u.get("name") == "Bash"]
    return {
        "models": sorted(m for m in models if m),
        "usage": tot if usage else None,
        "assistant_messages": len(usage),
        "tools": [u.get("name") for u in uses],
        "elapsed_ms": elapsed,
        "resolve_ok": bool(ok),
        "resolve_calls": len(resolves),
        "delivered": sorted({variant(o) for o in ok}),
        "skill_tool": any(u.get("name") == "Skill" for u in uses),
        "server_started": any(re.search(r"start-server|server\.cjs", c) for c in cmds),
    }


def collect(rid, agent_id):
    case, arm, _ = parse(rid)
    d = RUNS / rid
    root = Path(__import__("os").environ.get("APSP_TRANSCRIPTS", TRANSCRIPTS))
    found = sorted(root.glob(f"*/subagents/agent-{agent_id}.jsonl"))
    if len(found) != 1:
        sys.exit(f"transcript for {agent_id}: found {len(found)}")
    shutil.copyfile(found[0], d / "transcript.jsonl")
    raw = (d / "transcript.jsonl").read_bytes()
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    a = analyze(rows)
    before, after = tree_hashes(SUITE / "fixture"), tree_hashes(d / "project")
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    reply = d / "reply.md"
    text = reply.read_text("utf-8") if reply.exists() else None
    source = "reply.md" if text is not None else None
    if text is None:  # child returned the message instead of writing it: recover verbatim, never edit
        finals = [b["text"] for r in rows if r.get("type") == "assistant"
                  for b in ((r.get("message") or {}).get("content") or []) if b.get("type") == "text"]
        if finals and finals[-1].strip():
            (d / "reply.recovered.md").write_text(finals[-1], "utf-8")
            source = "transcript-final-text"
    first = next((r["message"]["content"] for r in rows if r.get("type") == "user"), None)
    if isinstance(first, list):
        first = "".join(b.get("text", "") for b in first if isinstance(b, dict))
    checks = {"prompt_exact": (first or "").strip() == prompt(rid).strip()}
    for chk in cases()[case]["deterministic"]:
        if chk == "resolve_ok":
            checks[chk] = a["resolve_ok"]
        elif chk == "no_skill_tool":
            checks[chk] = not a["skill_tool"]
        elif chk == "reply_written":
            checks[chk] = bool(text and text.strip() and not text.startswith("SETUP-FAILED"))
        elif chk == "fixture_unchanged":
            checks[chk] = not changed
        elif chk == "no_server_started":
            checks[chk] = not a["server_started"]
        elif chk.startswith("fixture_changed_only:"):
            target = chk.split(":", 1)[1]
            ok = changed == [target]
            if ok and case == "C09-quick-clear-task":
                ok = "usage: habit <add|done|list> [name]" in (d / "project" / target).read_text("utf-8")
            checks[chk] = ok
    expected = {"full": "@apsp/brainstorming-upstream@7.0.2", "cand": "@apsp/brainstorming-sonnet-5-5@0.1.0"}[arm]
    setup_valid = a["resolve_ok"] and not a["skill_tool"] and a["delivered"] == [arm]
    result = {"run": rid, "agentId": agent_id, "transcript_sha256": hashlib.sha256(raw).hexdigest(),
              "reply_source": source, "changed_files": changed,
              "checks": checks, "setup_valid": setup_valid, "expected_package": expected, **a,
              "provider_session_id": "unknown", "t3_ids": "unknown"}
    graded = d / ("reply.md" if source == "reply.md" else "reply.recovered.md")
    gtext = graded.read_text("utf-8") if source else None
    result["reply_sha256"] = hashlib.sha256(graded.read_bytes()).hexdigest() if source else None
    result["reply_words"] = len(gtext.split()) if gtext else None
    (d / "result.json").write_text(json.dumps(result, indent=2), "utf-8")
    ledger({"event": "collected", "run": rid, "agentId": agent_id, "transcript": found[0].name,
            "transcript_sha256": result["transcript_sha256"], "setup_valid": setup_valid})
    print(json.dumps({k: result[k] for k in ("run", "models", "delivered", "setup_valid", "checks", "reply_source", "reply_words")}))


def reply_of(d):
    r = json.loads((d / "result.json").read_text("utf-8"))
    src = {"reply.md": "reply.md", "transcript-final-text": "reply.recovered.md"}.get(r["reply_source"])
    return r, ((d / src).read_text("utf-8") if src else None)


def bundle(case, tag):
    """Blind bundle for the held-out grader: shuffled opaque IDs; arm key kept apart."""
    import random
    c = {k: v for k, v in cases()[case].items() if k != "targets"}  # targets name the candidate's deletions
    items = []
    for d in sorted(RUNS.glob(f"{EXPERIMENT}.{case}.*")):
        if not (d / "result.json").exists():
            continue
        r, text = reply_of(d)
        if r["setup_valid"] and text:
            items.append((d.name, text))
    random.SystemRandom().shuffle(items)
    out = PRIVATE / "grading" / tag / case
    out.mkdir(parents=True, exist_ok=False)
    key = {f"R{i + 1}": run for i, (run, _) in enumerate(items)}
    (PRIVATE / "grading" / tag / f"{case}.key.json").write_text(json.dumps(key, indent=2), "utf-8")
    replies = "\n\n".join(f"### Reply {rid}\n\n{text}" for rid, (_, text) in zip(key, items))
    (out / "bundle.md").write_text(
        f"# Grading bundle {tag}/{case}\n\n## Rubric\n\n{(SUITE / 'RUBRIC.md').read_text('utf-8')}\n\n"
        f"## Case\n\n```json\n{json.dumps(c, indent=2)}\n```\n\nFixture (read-only): {(SUITE / 'fixture').as_posix()}\n\n"
        f"## Replies\n\n{replies}\n", "utf-8")
    print(out / "bundle.md", len(items))


def score(tag, case, grades_file):
    key = json.loads((PRIVATE / "grading" / tag / f"{case}.key.json").read_text("utf-8"))
    g = json.loads(Path(grades_file).read_text("utf-8"))
    crit = [m.split(":")[0] for m in cases()[case]["must"] + cases()[case]["should"]]
    rows = []
    for x in g["grades"]:
        run = key[x["reply"]]
        rows.append({"run": run, "case": case, "arm": parse(run)[1], "rep": parse(run)[2], "grader": g.get("grader"),
                     **{k: x.get(k, "missing") for k in crit}, "evidence": x.get("evidence", {})})
    assert sorted(r["run"] for r in rows) == sorted(key.values()), "grader skipped or invented replies"
    with (PRIVATE / "grading" / tag / "scores.jsonl").open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    for r in rows:
        print(r["arm"], r["rep"], {k: r[k] for k in crit})


def selftest():
    rows = [
        {"type": "assistant", "timestamp": "2026-11-07T00:00:00Z", "message": {"id": "m1", "model": "claude-sonnet-5-5",
         "usage": {"input_tokens": 3, "cache_creation_input_tokens": 10, "cache_read_input_tokens": 0, "output_tokens": 5,
                   "output_tokens_details": {"thinking_tokens": 2}},
         "content": [{"type": "tool_use", "id": "t1", "name": "Bash",
                      "input": {"command": "cd x && npx --no agent-profiles resolve --role brainstormer"}}]}},
        {"type": "assistant", "timestamp": "2026-11-07T00:00:01Z", "message": {"id": "m1", "model": "claude-sonnet-5-5",
         "usage": {"input_tokens": 3, "cache_creation_input_tokens": 10, "cache_read_input_tokens": 0, "output_tokens": 5,
                   "output_tokens_details": {"thinking_tokens": 2}},
         "content": []}},
        {"type": "user", "timestamp": "2026-11-07T00:00:02Z", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1",
         "content": "## Required skill: brainstorming\nart. Read from how they\ntalk which ... Requirements, scope, "
                    "tradeoffs, and conceptual choices stay in text.\nEnd of Agent Profiles context: 3 section(s)"}]}},
        {"type": "assistant", "timestamp": "2026-11-07T00:00:04Z", "message": {"id": "m2", "model": "claude-sonnet-5-5",
         "usage": {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 10, "output_tokens": 7},
         "content": [{"type": "tool_use", "id": "t2", "name": "Skill", "input": {}}]}},
    ]
    a = analyze(rows)
    assert a["usage"] == {"input_tokens": 4, "cache_creation_input_tokens": 10, "cache_read_input_tokens": 10,
                          "output_tokens": 12, "thinking_tokens_within_output": 2}, a["usage"]
    assert a["assistant_messages"] == 2 and a["resolve_ok"] and a["skill_tool"] and a["elapsed_ms"] == 4000
    assert a["delivered"] == ["full"] and not a["server_started"]
    root = COMPANION / "packages"
    assert variant("## Required skill: brainstorming\n" + (root / "brainstorming-upstream/7.0.2/SKILL.md").read_text("utf-8")) == "full"
    assert variant((root / "brainstorming-sonnet-5-5/0.1.0/SKILL.md").read_text("utf-8")) == "cand"
    assert variant("withheld") == "unknown"
    assert analyze([])["usage"] is None
    assert parse(run_id("C04-user-controlled-how", "cand", 2)) == ("C04-user-controlled-how", "cand", 2)
    print("selftest ok")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    if cmd == "prepare":
        prepare(args[0], args[1], int(args[2]))
    elif cmd == "prompt":
        print(prompt(args[0]))
    elif cmd == "collect":
        collect(*args)
    elif cmd == "bundle":
        bundle(args[0], args[1])
    elif cmd == "score":
        score(args[0], args[1], args[2])
    elif cmd == "selftest":
        selftest()
