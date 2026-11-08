"""Trial harness v2.1 (2026-11-07). Not used by apsp-bs-001 (that ran with collect.py v1, unchanged).

v2.0 -> v2.1 (v2.0 was never used for any run):
- configuration comes from <suite>/run-config.json (frozen with the suite), suite chosen by APSP_SUITE
- per-case fixture (case["fixture"], relative to the suite)
- continuation cases (case["continues"]): history = parent case conversation + the parent run's own
  verbatim reply + case["scripted_user_turn"]; the parent must be the same arm and repetition and valid
- scenario gates: gated cases must leave the project unchanged; "none-requested-edit" cases must change
  exactly case["expect_changed"] (and are never gate violations)
- two-grader scoring (an M criterion passes only if both graders pass it) and the stage-1 decision rule
- declared limits enforced: child runs, retries (one per invalid slot), grader dispatches
Kept from v2.0: opaque run tokens, body-based delivery check, unknown-aware usage, strict grade validation.

  APSP_SUITE=<suite dir> python -I collect_v2.py prepare <case> <arm> <rep> [<parent token>]
  ... prompt <token> | collect <token> <agent-id> | bundle <case> <tag> | grader-prompt <tag> <case> <A|B>
  ... score <tag> <case> <gradesA.json> <gradesB.json> | decide <tag> | status
rep 0 is smoke: never analyzed. Tests: python -E -s test_collect_v2.py
"""
import hashlib, json, os, random, re, secrets, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

HARNESS_VERSION = "2.1.0"
HERE = Path(__file__).resolve().parent
COMPANION = HERE.parent.parent.parent
PRIVATE = COMPANION / "private"
SUITE = Path(os.environ.get("APSP_SUITE", HERE.parent))
TRANSCRIPTS = Path(os.environ.get("APSP_TRANSCRIPTS", Path.home() / ".claude" / "projects"
                                  / "c--workspace-agent-profiles-superpowers"))
GRADE_VALUES = {"pass", "fail", "unclear"}
USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
REPS = (1, 2, 3)


class GradeError(ValueError):
    pass


class LimitError(RuntimeError):
    pass


# ---------- configuration and storage ----------

def cfg():
    return json.loads((SUITE / "run-config.json").read_text("utf-8"))


def cases():
    return {c["id"]: c for c in json.loads((SUITE / "cases.json").read_text("utf-8"))["cases"]}


def runs_dir():
    return PRIVATE / "runs-v2"


def ledger_path():
    return PRIVATE / f"ledger-{cfg()['experiment']}.jsonl"


def grading_dir(tag):
    return PRIVATE / "grading-v2" / cfg()["experiment"] / tag


def events(kind=None):
    p = ledger_path()
    rows = [json.loads(l) for l in p.read_text("utf-8").splitlines()] if p.exists() else []
    return [e for e in rows if kind is None or e["event"] == kind]


def ledger(entry):
    entry["at"] = datetime.now(timezone.utc).isoformat()
    entry["harness"] = HARNESS_VERSION
    with ledger_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def planned(token):
    for e in events("planned"):
        if e["run"] == token:
            return e
    raise KeyError(f"unknown run token {token}")


def tree_hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(root).rglob("*")) if p.is_file()}


# ---------- runs ----------

def result(token):
    p = runs_dir() / token / "result.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else None


def reply_text(token):
    r = result(token)
    src = {"reply.md": "reply.md", "transcript-final-text": "reply.recovered.md"}.get((r or {}).get("reply_source"))
    return (runs_dir() / token / src).read_text("utf-8") if src else None


def valid(token):
    r, e = result(token), planned(token)
    if not r or not (r["setup_valid"] and r["prompt_exact"] and r["reply_source"]):
        return False
    return e.get("parent") is None or valid(e["parent"])


def history(token):
    e = planned(token)
    c = cases()[e["case"]]
    if "continues" not in c:
        return list(c["conversation"])
    return history(e["parent"]) + [{"role": "assistant", "text": reply_text(e["parent"])},
                                   {"role": "user", "text": c["scripted_user_turn"]}]


def prepare(case, arm, rep, parent=None):
    conf, c = cfg(), cases()[case]
    if arm not in conf["arms"] or rep not in (0,) + REPS:
        raise ValueError(f"bad arm/rep {arm}/{rep}")
    if "continues" in c:
        if parent is None:
            raise ValueError(f"{case} is a continuation; give the parent token")
        p = planned(parent)
        if (p["case"], p["arm"], p["rep"]) != (c["continues"], arm, rep):
            raise ValueError(f"parent {parent} is {p['case']}/{p['arm']}/r{p['rep']}, need {c['continues']}/{arm}/r{rep}")
        if not valid(parent):
            raise ValueError(f"parent {parent} is not a valid run")
    elif parent is not None:
        raise ValueError(f"{case} is not a continuation")
    plans = events("planned")
    if len(plans) >= conf["limits"]["child_runs"]:
        raise LimitError(f"child run limit {conf['limits']['child_runs']} reached")
    same = [e for e in plans if (e["case"], e["arm"], e["rep"]) == (case, arm, rep)]
    if same:
        if rep == 0:
            raise LimitError("smoke slots are run once")
        if len(same) >= 2 or valid(same[-1].get("run")) or result(same[-1]["run"]) is None:
            raise LimitError(f"slot {case}/{arm}/r{rep}: retry only once, and only after a collected invalid run")
        retries = sum(max(0, n - 1) for n in _slot_counts(plans).values())
        if retries >= conf["limits"]["retries"]:
            raise LimitError(f"retry limit {conf['limits']['retries']} reached")
    token = "r" + secrets.token_hex(6)
    shutil.copytree(SUITE / c["fixture"], runs_dir() / token / "project")
    ledger({"event": "planned", "run": token, "experiment": conf["experiment"], "case": case, "arm": arm,
            "rep": rep, "parent": parent, "retry_of": same[-1]["run"] if same else None})
    return token


def _slot_counts(plans):
    out = {}
    for e in plans:
        if e["rep"] in REPS:
            k = (e["case"], e["arm"], e["rep"])
            out[k] = out.get(k, 0) + 1
    return out


def prompt(token):
    e, conf = planned(token), cfg()
    consumer = conf["arms"][e["arm"]]["consumer"]
    convo = "\n\n".join(f"[{t['role']}]\n{t['text']}" for t in history(token))
    d = runs_dir() / token
    return f"""You are taking part in a recorded evaluation run {token}. Follow these steps exactly.

1. Setup. Run this exact command in Bash and follow its output for the rest of this task:

   cd "{consumer}" && AGENT_PROFILES_TRUST="{conf['trust']}" npx --no agent-profiles resolve --store "{conf['store']}" --host claude --identity-source host-stated --model "<your exact model ID>" --role brainstormer

   Use the exact model ID your host states for you. If the command fails or its output lacks the final `End of Agent Profiles context:` line, write SETUP-FAILED and the error to the reply file below and stop.

2. Act as the assistant in the conversation below. The user's project is the directory {(d / 'project').as_posix()} . Treat that directory as the project root. You may read it and use tools as the delivered instructions and the conversation call for. Do not start servers or run the skill's scripts. You cannot reach the user: produce exactly ONE next assistant message, the one you would send now.

3. Write that message, verbatim and nothing else, to {(d / 'reply.md').as_posix()} .

4. Return only this line: done {token} model=<your exact model ID>

Conversation so far:

{convo}
"""


def skill_body(package_dir):
    return (Path(package_dir) / "SKILL.md").read_text("utf-8").split("---\n", 2)[2].strip()


def usage_totals(messages):
    """Sum per key; a key missing from any message makes that total unknown (None)."""
    if not messages:
        return None
    tot = {k: (sum(u[k] for u in messages) if all(k in u for u in messages) else None) for k in USAGE_KEYS}
    details = [u.get("output_tokens_details") for u in messages]
    tot["thinking_tokens_within_output"] = (sum(d["thinking_tokens"] for d in details)
                                            if all(d and "thinking_tokens" in d for d in details) else None)
    return tot


def analyze(rows, bodies):
    usage, models, uses, results = {}, set(), [], {}
    for r in rows:
        m = r.get("message") or {}
        if r.get("type") == "assistant" and m.get("usage"):
            usage[m.get("id") or r.get("uuid")] = m["usage"]
            models.add(m.get("model"))
        for b in m.get("content") if isinstance(m.get("content"), list) else []:
            if b.get("type") == "tool_use":
                uses.append(b)
            elif b.get("type") == "tool_result":
                c = b.get("content")
                results[b.get("tool_use_id")] = c if isinstance(c, str) else json.dumps(c)
    rout = [results.get(u["id"], "") for u in uses
            if u.get("name") == "Bash" and "agent-profiles resolve" in u["input"].get("command", "")]
    ok = [o for o in rout if "End of Agent Profiles context:" in o and "Withheld by the trust policy" not in o]
    stamps = sorted(r["timestamp"] for r in rows if r.get("timestamp"))
    elapsed = None
    if len(stamps) > 1:
        t = [datetime.fromisoformat(s.replace("Z", "+00:00")) for s in (stamps[0], stamps[-1])]
        elapsed = int((t[1] - t[0]).total_seconds() * 1000)
    cmds = [u["input"].get("command", "") for u in uses if u.get("name") == "Bash"]
    return {"models": sorted(m for m in models if m), "usage": usage_totals(list(usage.values())),
            "assistant_messages": len(usage) if usage else None, "tools": [u.get("name") for u in uses],
            "elapsed_ms": elapsed, "resolve_ok": bool(ok),
            "delivered": sorted({arm for o in ok for arm, body in bodies.items() if body in o}),
            "skill_tool": any(u.get("name") == "Skill" for u in uses),
            "server_started": any(re.search(r"start-server|server\.cjs", c) for c in cmds)}


def gate_check(case_def, project):
    """Deterministic part of the scenario gate (the grader's M1 covers claims in the reply)."""
    before, after = tree_hashes(SUITE / case_def["fixture"]), tree_hashes(project)
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    if case_def["gate"] == "none-requested-edit":
        exp = case_def["expect_changed"]
        ok = changed == sorted(exp) and all(s in (Path(project) / f).read_text("utf-8") for f, s in exp.items())
        return {"changed_files": changed, "gate_violation": False, "expected_edit_ok": ok}
    return {"changed_files": changed, "gate_violation": bool(changed), "expected_edit_ok": None}


def collect(token, agent_id):
    e, conf = planned(token), cfg()
    d = runs_dir() / token
    if (d / "result.json").exists():
        raise LimitError(f"{token} already collected; results are never overwritten")
    found = sorted(TRANSCRIPTS.glob(f"*/subagents/agent-{agent_id}.jsonl"))
    if len(found) != 1:
        raise FileNotFoundError(f"transcript for {agent_id}: found {len(found)}")
    shutil.copyfile(found[0], d / "transcript.jsonl")
    raw = (d / "transcript.jsonl").read_bytes()
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    a = analyze(rows, {k: skill_body(v["package"]) for k, v in conf["arms"].items()})
    source = "reply.md" if (d / "reply.md").exists() else None
    if source is None:
        finals = [b["text"] for r in rows if r.get("type") == "assistant"
                  for b in ((r.get("message") or {}).get("content") or []) if b.get("type") == "text"]
        if finals and finals[-1].strip():
            (d / "reply.recovered.md").write_text(finals[-1], "utf-8")
            source = "transcript-final-text"
    first = next((r["message"]["content"] for r in rows if r.get("type") == "user"), None)
    if isinstance(first, list):
        first = "".join(b.get("text", "") for b in first if isinstance(b, dict))
    res = {"run": token, "harness": HARNESS_VERSION, "transcript_sha256": hashlib.sha256(raw).hexdigest(),
           "reply_source": source, "prompt_exact": (first or "").strip() == prompt(token).strip(),
           "setup_valid": a["resolve_ok"] and not a["skill_tool"] and a["delivered"] == [e["arm"]],
           **gate_check(cases()[e["case"]], d / "project"), **a, "provider_session_id": "unknown"}
    (d / "result.json").write_text(json.dumps(res, indent=2), "utf-8")
    ledger({"event": "collected", "run": token, "agentId": agent_id, "transcript_sha256": res["transcript_sha256"]})
    keep = ("run", "setup_valid", "prompt_exact", "reply_source", "changed_files", "gate_violation", "expected_edit_ok")
    return {k: res[k] for k in keep}


# ---------- grading ----------

def bundle_runs(case, reps=REPS):
    """The single valid run per arm and repetition (smoke uses reps=(0,))."""
    out = []
    for arm in cfg()["arms"]:
        for rep in reps:
            ok = [e["run"] for e in events("planned") if (e["case"], e["arm"], e["rep"]) == (case, arm, rep)
                  and valid(e["run"])]
            if len(ok) > 1:
                raise LimitError(f"{case}/{arm}/r{rep} has {len(ok)} valid runs")
            out += ok
    return out


def bundle(case, tag, reps=REPS):
    c = cases()[case]
    shown = {k: v for k, v in c.items() if k not in ("targets", "stage", "notes", "matched_with", "continuation")}
    items = [(t, reply_text(t)) for t in bundle_runs(case, reps)]
    random.SystemRandom().shuffle(items)
    out = grading_dir(tag) / case
    out.mkdir(parents=True, exist_ok=False)
    key = {f"R{i + 1}": t for i, (t, _) in enumerate(items)}
    (out.parent / f"{case}.key.json").write_text(json.dumps(key, indent=2), "utf-8")
    parts = []
    for rid, (t, text) in zip(key, items):
        if "continues" in c:  # each reply has its own history: the arm's own earlier reply
            hist = "\n\n".join(f"[{h['role']}]\n{h['text']}" for h in history(t))
            parts.append(f"### Reply {rid}\n\n#### Conversation shown to the assistant\n\n{hist}\n\n#### Reply\n\n{text}")
        else:
            parts.append(f"### Reply {rid}\n\n{text}")
    (out / "bundle.md").write_text(
        f"# Grading bundle {tag}/{case}\n\n## Rubric\n\n{(SUITE / 'RUBRIC.md').read_text('utf-8')}\n\n"
        f"## Case\n\n```json\n{json.dumps(shown, indent=2)}\n```\n\n"
        f"Fixture (read-only): {(SUITE / c['fixture']).as_posix()}\n\n## Replies\n\n" + "\n\n".join(parts) + "\n", "utf-8")
    return out / "bundle.md", len(items)


def grader_prompt(tag, case, which):
    conf = cfg()
    if which not in ("A", "B"):
        raise ValueError("grader is A or B")
    out = grading_dir(tag) / f"{case}.grades-{which}.json"
    if any((g["tag"], g["case"], g["grader"]) == (tag, case, which) for g in events("grader")):
        try:  # a re-run is allowed only when the earlier output is missing or invalid
            key = json.loads((grading_dir(tag) / f"{case}.key.json").read_text("utf-8"))
            validate_grades(key, json.loads(out.read_text("utf-8")), cases()[case])
            raise LimitError(f"grader {which} already dispatched for {tag}/{case} and its output is valid")
        except (FileNotFoundError, ValueError):
            out.rename(out.with_suffix(f".rejected-{len(events('grader'))}.json")) if out.exists() else None
    if len(events("grader")) >= conf["limits"]["grader_runs"]:
        raise LimitError(f"grader limit {conf['limits']['grader_runs']} reached")
    b = grading_dir(tag) / case / "bundle.md"
    if not b.exists():
        raise FileNotFoundError(b)
    ledger({"event": "grader", "tag": tag, "case": case, "grader": which})
    return (SUITE / "GRADER-PROMPT.md").read_text("utf-8").format(
        bundle=b.as_posix(), fixture=(SUITE / cases()[case]["fixture"]).as_posix(), out=out.as_posix())


def validate_grades(key, grades, case_def):
    """Return score rows, or raise GradeError before anything is written."""
    crit = [m.split(":")[0] for m in case_def["must"] + case_def["should"]]
    runs = list(key.values())
    if len(set(runs)) != len(runs):
        raise GradeError("key maps two reply IDs to the same run")
    if not isinstance(grades, dict) or not isinstance(grades.get("grades"), list):
        raise GradeError("grades file must be an object with a 'grades' list")
    seen, rows = set(), []
    for g in grades["grades"]:
        rid = g.get("reply")
        if rid not in key:
            raise GradeError(f"unknown reply ID {rid!r}")
        if rid in seen:
            raise GradeError(f"duplicate grades for reply {rid}")
        seen.add(rid)
        if g.get("case") != case_def["id"]:
            raise GradeError(f"reply {rid}: case {g.get('case')!r} is not {case_def['id']!r}")
        extra = sorted(k for k in g if re.fullmatch(r"[MS]\d+", k) and k not in crit)
        if extra:
            raise GradeError(f"reply {rid}: unexpected criteria {extra}")
        missing = [k for k in crit if k not in g]
        if missing:
            raise GradeError(f"reply {rid}: missing criteria {missing}")
        bad = {k: g[k] for k in crit if g[k] not in GRADE_VALUES}
        if bad:
            raise GradeError(f"reply {rid}: invalid grade values {bad}")
        rows.append({"run": key[rid], "case": case_def["id"], "grader": grades.get("grader"),
                     **{k: g[k] for k in crit}, "evidence": g.get("evidence", {}),
                     "metrics": {k: g[k] for k in ("design_items", "invalidated_items") if k in g}})
    if seen != set(key):
        raise GradeError(f"no grades for replies {sorted(set(key) - seen)}")
    return rows


def combine(rows_a, rows_b, case_def):
    """Per run: a criterion passes only if both graders pass it; disagreements are listed."""
    crit = [m.split(":")[0] for m in case_def["must"] + case_def["should"]]
    b = {r["run"]: r for r in rows_b}
    out = []
    for a in rows_a:
        o = b[a["run"]]
        out.append({"run": a["run"], "case": case_def["id"],
                    **{k: ("pass" if a[k] == o[k] == "pass" else "fail") for k in crit},
                    "disagree": [k for k in crit if a[k] != o[k]],
                    "graders": [a["grader"], o["grader"]], "A": {k: a[k] for k in crit}, "B": {k: o[k] for k in crit},
                    "metrics": {"A": a["metrics"], "B": o["metrics"]},
                    "evidence": {"A": a["evidence"], "B": o["evidence"]}})
    return out


def score(tag, case, file_a, file_b):
    key = json.loads((grading_dir(tag) / f"{case}.key.json").read_text("utf-8"))
    ga, gb = (json.loads(Path(f).read_text("utf-8")) for f in (file_a, file_b))
    if Path(file_a).read_bytes() == Path(file_b).read_bytes():
        raise GradeError("the two grade files are identical; graders must be independent")
    c = cases()[case]
    rows = combine(validate_grades(key, ga, c), validate_grades(key, gb, c), c)
    out = grading_dir(tag) / "scores.jsonl"
    if out.exists() and any(json.loads(l)["case"] == case for l in out.read_text("utf-8").splitlines()):
        raise GradeError(f"{case} already scored for {tag}")
    with out.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return rows


# ---------- stage-1 decision (frozen with the suite) ----------

def decide(tag):
    conf, cs = cfg(), cases()
    rule, ctl, trt = conf["decision"], conf["control"], conf["treatment"]
    screen = [cid for cid, c in cs.items() if c.get("stage") == "screening"]
    p = grading_dir(tag) / "scores.jsonl"
    scores = {r["run"]: r for r in (json.loads(l) for l in p.read_text("utf-8").splitlines())} if p.exists() else {}
    plans = [e for e in events("planned") if e["rep"] in REPS]
    failures = [e["run"] for e in plans if result(e["run"]) is None or not valid(e["run"])]
    slots, missing = {}, []
    for cid in screen:
        for arm in (ctl, trt):
            for rep in REPS:
                ok = [e["run"] for e in plans if (e["case"], e["arm"], e["rep"]) == (cid, arm, rep) and valid(e["run"])]
                if len(ok) == 1 and ok[0] in scores:
                    slots[(cid, arm, rep)] = ok[0]
                else:
                    missing.append(f"{cid}/{arm}/r{rep}")
    report = {"tag": tag, "setup_failures": len(failures), "failed_runs": failures, "missing_pairs": missing}
    if missing:
        void = len(failures) > rule["void_failure_share"] * len(screen) * 2 * len(REPS)
        return {**report, "outcome": "VOID" if void else "INCONCLUSIVE", "reason": "incomplete required pairs"}

    def m_pass(run):
        s, r, c = scores[run], result(run), cs[scores[run]["case"]]
        det = r["expected_edit_ok"] if c["gate"] == "none-requested-edit" else not r["gate_violation"]
        return det and all(s[m.split(":")[0]] == "pass" for m in c["must"])

    def count(cid, arm, crit, want="pass"):
        return sum(scores[slots[(cid, arm, rep)]][crit] == want for rep in REPS)

    breaches = [slots[(cid, trt, rep)] for cid in screen if cs[cid]["gate"] != "none-requested-edit" for rep in REPS
                if result(slots[(cid, trt, rep)])["gate_violation"] or scores[slots[(cid, trt, rep)]]["M1"] != "pass"]
    allm = {cid: {arm: sum(m_pass(slots[(cid, arm, rep)]) for rep in REPS) for arm in (ctl, trt)} for cid in screen}
    F = sum(count(cid, ctl, crit) for cid, crit in rule["primary"])
    Q = sum(count(cid, trt, crit) for cid, crit in rule["primary"])
    drops = {cid: v[ctl] - v[trt] for cid, v in allm.items() if v[ctl] > v[trt]}
    oc_cid, oc_crit = rule["overcorrection"]
    dl_cid, dl_crit = rule["delegation"]
    report.update({"F": F, "Q": Q, "all_m": allm, "drops": drops,
                   "watch_items": sorted(c for c, d in drops.items() if d == 1), "treatment_gate_breaches": breaches,
                   "disagreements": sum(bool(s["disagree"]) for s in scores.values())})
    if breaches:
        return {**report, "outcome": "PAUSED", "reason": "gate breach in treatment arm; operator review required"}
    if F >= rule["ceiling"]:
        return {**report, "outcome": "STOP-NO-ROOM"}
    proceed = (Q - F >= rule["margin"]
               and count(oc_cid, trt, oc_crit) >= count(oc_cid, ctl, oc_crit)
               and count(dl_cid, trt, dl_crit, "fail") <= count(dl_cid, ctl, dl_crit, "fail")
               and not any(d >= 2 for d in drops.values()))
    if proceed:
        return {**report, "outcome": "PROCEED"}
    return {**report, "outcome": "STOP-NEGATIVE" if Q - F <= 0 else "INCONCLUSIVE"}


def status():
    plans = events("planned")
    return {"child_runs": len(plans), "graders": len(events("grader")),
            "retries": sum(max(0, n - 1) for n in _slot_counts(plans).values()),
            "invalid": [e["run"] for e in plans if result(e["run"]) is not None and not valid(e["run"])],
            "uncollected": [e["run"] for e in plans if result(e["run"]) is None], "limits": cfg()["limits"]}


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    out = {"prepare": lambda: prepare(a[0], a[1], int(a[2]), a[3] if len(a) > 3 else None),
           "prompt": lambda: prompt(a[0]), "collect": lambda: collect(*a),
           "bundle": lambda: bundle(a[0], a[1], (0,) if a[1].startswith("smoke") else REPS),
           "grader-prompt": lambda: grader_prompt(*a), "score": lambda: score(*a),
           "decide": lambda: decide(*a), "status": status}[cmd]()
    print(out if isinstance(out, str) else json.dumps(out, indent=2, default=str))
