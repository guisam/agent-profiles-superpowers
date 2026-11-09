"""apsp-tdd-001 harness 2.2.0 (bounded revision of evaluations/brainstorming/tools/collect_v2.py 2.1.0).

The 2.1.0 file and its 23 tests are unchanged; brainstorming artifacts stay on 2.1.0.
This module serves the apsp-tdd-001 R-block only. Changes against the four 2.1.0 failure modes
(PROPOSAL §8):
  1. Rendering never touches the ledger. A `dispatch` event is appended immediately before a
     process spawns; limits count dispatch events only.
  2. Grader files are not compared byte-for-byte. Provenance: each file must hash-match the Write
     in its own grader session, the sessions differ, and neither read the other's output.
  3. `bundle` refuses unless every slot of the case has exactly one valid run.
  4. Collection is bound to the session ID recorded at dispatch; retry eligibility comes only from
     collector-computed setup fields.

Commands (python -I tdd_harness.py <cmd> ...):
  contexts            freeze per-arm contexts from private resolve output (strip "Run again")
  selfcheck           validate checkers against fixtures' good/bad reference trees (no model)
  status [stage]      slot table from the ledger
  run <stage>         serial dispatch+collect+check of the frozen order (stops on stop rules)
  bundle <stage> <case>     build the blind Gr1 bundle (stage0: 2 packets, stage1: 6)
  grade <stage> <case> <g>  dispatch blind grader g (stage0: 1; stage1: 1|2)
  score <stage> <case>      validate + provenance-check grader file(s), combine
  decide                    stage-1 outcome per PROPOSAL §6 (requires the human audit file)
"""
import datetime as _dt
import hashlib
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

VERSION = "2.2.2"
HERE = Path(__file__).resolve().parent
EXP = HERE.parent
S1 = EXP / "stage1"
REPO = EXP.parent.parent
PRIV = REPO / "private" / "tdd001"
LEDGER = PRIV / "ledger.jsonl"
RUNS = PRIV / "runs"
GRADING = PRIV / "grading"
RUNROOT = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "apsp-tdd"
PROJECTS = Path.home() / ".claude" / "projects"

SCRUB = re.compile(r"^(CLAUDECODE$|CLAUDE_|T3CODE_|AGENT_PROFILES_|ANTHROPIC_)")
CHILD_TOOLS = ["Bash", "Edit", "Glob", "Grep", "Read", "Write"]
GRADER_TOOLS = ["Read", "Write"]
RETRYABLE = {"init_mismatch", "context_sha_mismatch", "missing_stream", "missing_transcript",
             "crash", "host_error", "usage_limit", "repo_access"}


class HarnessError(Exception):
    pass


# ------------------------------------------------------------------ small utils
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def now():
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def dump_json(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def config():
    return load_json(S1 / "run-config.json")


def cases():
    return {c["id"]: c for c in load_json(S1 / "cases.json")["cases"]}


# ------------------------------------------------------------------ ledger (append-only)
def ledger_read(path=None):
    path = path or LEDGER
    if not Path(path).exists():
        return []
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def ledger_append(event, path=None):
    path = Path(path or LEDGER)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event, ts=now())
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")
    return event


def slot_key(stage, case, arm, rep):
    return f"{stage}/{case}/{arm}/{rep}"


def slot_state(events, stage, case, arm, rep):
    """Dispatches and collected results for one slot, in ledger order."""
    k = slot_key(stage, case, arm, rep)
    disp = [e for e in events if e["event"] == "dispatch" and e["kind"] == "child" and e["slot"] == k]
    coll = {e["token"]: e for e in events if e["event"] == "collected" and e.get("slot") == k}
    return disp, coll


def count_dispatches(events, kind, stage=None):
    return sum(1 for e in events if e["event"] == "dispatch" and e["kind"] == kind
               and (stage is None or e.get("stage") == stage))


def eligibility(events, stage, case, arm, rep, limits):
    """Return (ok, reason, is_retry). Pure function of the ledger (failure mode 4)."""
    disp, coll = slot_state(events, stage, case, arm, rep)
    if any(c["setup_valid"] for c in coll.values()):
        return False, "slot already has a valid run", False
    pending = [d for d in disp if d["token"] not in coll]
    if pending:
        return False, f"dispatched run {pending[0]['token']} not collected", False
    is_retry = bool(disp)
    if count_dispatches(events, "child", stage) >= limits["child_runs"]:
        return False, "child-run limit reached", is_retry
    if is_retry:
        if len(disp) > limits["retries_per_slot"]:
            return False, "slot retry used", True
        last = coll[disp[-1]["token"]]
        bad = set(last["invalid_reasons"]) - RETRYABLE
        if bad:
            return False, f"not retryable: {sorted(bad)}", True
        used = sum(1 for e in events if e["event"] == "dispatch" and e["kind"] == "child"
                   and e.get("stage") == stage and e.get("retry"))
        if used >= limits["retries"]:
            return False, "retry limit reached", True
    return True, "ok", is_retry


# ------------------------------------------------------------------ contexts
def strip_run_again(text):
    lines = text.splitlines(keepends=True)
    try:
        a = next(i for i, l in enumerate(lines) if l.startswith("## Run again"))
        b = next(i for i, l in enumerate(lines) if l.startswith("End of Agent Profiles context:"))
    except StopIteration:
        raise HarnessError("context lacks the Run again section or the end marker")
    return "".join(lines[:a] + lines[b:])


def cmd_contexts():
    key = load_json(PRIV / "key.json")
    out = S1 / "contexts"
    out.mkdir(parents=True, exist_ok=True)
    pk = {"full": REPO / "packages/test-driven-development-upstream/7.0.2",
          "cand": REPO / "packages/test-driven-development-sonnet-5-5/0.1.0"}
    for arm in ("full", "cand"):
        raw = (PRIV / "contexts" / f"context-{arm}.md").read_text(encoding="utf-8")
        text = strip_run_again(raw)
        skill = (pk[arm] / "SKILL.md").read_text(encoding="utf-8")
        alias_skill = (PRIV / "alias-src" / key[arm]["alias"] / "SKILL.md").read_text(encoding="utf-8")
        if skill != alias_skill:
            raise HarnessError(f"{arm}: alias SKILL.md differs from the canonical package")
        if skill.strip() not in text:
            raise HarnessError(f"{arm}: SKILL.md body not contained in the resolved context")
        for bad in ("apsp", "t-k1", "t-k2", "workspace", key["full"]["consumer"], key["cand"]["consumer"]):
            if bad in text:
                raise HarnessError(f"{arm}: context leaks {bad!r}")
        (out / f"context-{arm}.md").write_text(text, encoding="utf-8", newline="\n")
        print(arm, len(text.encode()), sha256_bytes(text.encode()))
    res = [(REPO / "packages/test-driven-development-upstream/7.0.2/writing-good-tests.md"),
           (REPO / "packages/test-driven-development-sonnet-5-5/0.1.0/writing-good-tests.md")]
    if sha256_file(res[0]) != sha256_file(res[1]):
        raise HarnessError("writing-good-tests.md differs between arms")
    shutil.copyfile(res[0], out / "writing-good-tests.md")


# ------------------------------------------------------------------ stream parsing
def parse_stream(lines):
    """stream-json lines -> (init, events, result). events are ordered tool/text records."""
    init, result, events = None, None, []
    pending = {}
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            ev = json.loads(raw)
        except ValueError:
            continue
        t = ev.get("type")
        if t == "system" and ev.get("subtype") == "init":
            init = ev
        elif t == "result":
            result = ev
        elif t == "assistant":
            for b in ev.get("message", {}).get("content", []) or []:
                if b.get("type") == "text" and b.get("text", "").strip():
                    events.append({"kind": "text", "text": b["text"]})
                elif b.get("type") == "tool_use":
                    rec = {"kind": "tool", "id": b.get("id"), "name": b.get("name"),
                           "input": b.get("input") or {}, "ok": None, "exit": None, "output": ""}
                    pending[b.get("id")] = rec
                    events.append(rec)
        elif t == "user":
            content = ev.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get("type") != "tool_result":
                    continue
                rec = pending.get(b.get("tool_use_id"))
                if rec is None:
                    continue
                c = b.get("content")
                if isinstance(c, list):
                    c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                c = c or ""
                rec["output"] = c
                rec["ok"] = not b.get("is_error", False)
                m = re.match(r"(?:Error: )?Exit code (\d+)", c)
                rec["exit"] = int(m.group(1)) if m else (0 if rec["ok"] else None)
    for i, e in enumerate(events):
        e["i"] = i
    return init, events, result


# ------------------------------------------------------------------ classification
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__)/|(^|/)test_[^/]*\.py$|_test\.py$|\.test\.[cm]?js$")
WRITE_OPS = re.compile(r"(?<![<>&\d])>{1,2}(?!&)|\bsed\s+(-\w*\s+)*-i|\btee\b|\bcat\s*<<|open\([^)]*['\"][wa]|"
                       r"writeFileSync|\bcp\b|\bmv\b|Set-Content|Out-File|Add-Content")


def norm_rel(path, project):
    if not path:
        return None
    p = str(path).replace("\\", "/")
    root = str(project).replace("\\", "/").rstrip("/")
    # tolerate /c/... vs C:/... and case differences on Windows
    def canon(s):
        s = re.sub(r"^/([a-zA-Z])/", lambda m: m.group(1) + ":/", s)
        return s.lower()
    cp, cr = canon(p), canon(root)
    if cp.startswith(cr + "/"):
        return p[len(root) + 1:] if p.lower().startswith(root.lower()) else cp[len(cr) + 1:]
    if not re.match(r"^([a-zA-Z]:|/)", p):
        return p.lstrip("./")
    return None  # outside project


def is_test_path(rel):
    return bool(rel) and bool(TEST_PATH.search(rel))


def is_prod_path(rel, case):
    return bool(rel) and not is_test_path(rel) and bool(re.search(case["prod_path"], rel))


def test_run_info(cmd, case):
    """(is_test_run, is_full_suite) for a Bash command."""
    segs = re.split(r"&&|\|\||;|\|", cmd)
    hit, full = False, False
    for s in segs:
        s = re.sub(r"(^|\s)\d*(>>?|<)&?\s*\S*", " ", s).strip()  # drop redirections (2>&1, > out.txt)
        if case["lang"] == "python":
            m = re.search(r"\bpython3?(?:\.exe)?\s+(?:-[A-Za-z]+\s+)*-m\s+(unittest|pytest)\b(.*)", s) or \
                re.search(r"^()pytest\b(.*)", s)
            if m:
                hit = True
                args = [a for a in m.group(2).split() if not a.startswith("-")]
                if m.group(1) == "unittest":
                    args = [a for a in args if a != "discover"]
                    # discover -s <dir> -t <dir> -p <pattern>: flag values, not test names
                    vals = set(re.findall(r"-[stp]\s+(\S+)", m.group(2)))
                    args = [a for a in args if a not in vals]
                full = full or not args or args == ["."] or args == ["tests"]
        else:
            m = re.search(r"\bnpm(?:\.cmd)?\s+(?:run\s+)?test\b(.*)", s)
            if m:
                hit = True
                extra = m.group(1).split("--", 1)
                full = full or len(extra) == 1 or not [a for a in extra[1].split() if not a.startswith("-")]
                continue
            m = re.search(r"\bnode(?:\.exe)?\s+(.*)", s)
            if m and "--test" in m.group(1).split():
                hit = True
                args = [a for a in m.group(1).split() if not a.startswith("-")]
                full = full or not args
    return hit, full


PATH_TOKEN = re.compile(r"[\w.:/\\-]*[\w-]+\.(?:py|js|cjs|mjs|toml|md|json|txt)\b")
SCRIPT_WRITE = re.compile(r"open\([^)]*['\"][wax]\+?b?['\"]|\.write_text\(|\.write_bytes\(|writeFileSync|"
                          r"fs\.writeFile|appendFileSync|shutil\.copy|os\.replace|os\.rename")


def split_segments(cmd):
    """Split a shell command into ordered segments. A heredoc (its command line plus body) is one
    segment; other lines split on &&, ||, ;, |."""
    lines = cmd.replace("\r\n", "\n").split("\n")
    segs, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", line)
        if m:
            delim, body = m.group(1), [line]
            i += 1
            while i < len(lines) and lines[i].strip() != delim:
                body.append(lines[i])
                i += 1
            segs.append(("heredoc", "\n".join(body)))
            i += 1  # skip the delimiter line
            continue
        for part in re.split(r"&&|\|\||;|(?<![|>])\|(?!\|)", line):
            if part.strip():
                segs.append(("simple", part.strip()))
        i += 1
    return segs


def written_paths(kind, seg):
    """Paths a segment writes (heuristic; shell writes are flagged for audit)."""
    out = []
    if kind == "heredoc":
        head = seg.split("\n", 1)[0]
        out += re.findall(r">{1,2}\s*['\"]?([^\s'\"<>|;&]+)", head.split("<<")[0])  # cat > f <<EOF
        if SCRIPT_WRITE.search(seg):
            out += PATH_TOKEN.findall(seg)
        return out
    out += re.findall(r"(?<![<>&\d])>{1,2}(?!&)\s*['\"]?([^\s'\"<>|;&]+)", seg)
    if re.search(r"\bsed\s+(?:-\w+\s+)*-i", seg) or re.search(r"\btee\b", seg):
        out += PATH_TOKEN.findall(seg)
    m = re.match(r"(?:cp|mv|Copy-Item|Move-Item)\s+.*\s(\S+)$", seg)
    if m:
        out.append(m.group(1))
    if re.search(r"\b(python3?|node)\b.*\s-[ce]\s", seg) and SCRIPT_WRITE.search(seg):
        out += PATH_TOKEN.findall(seg)
    if re.search(r"Set-Content|Out-File|Add-Content", seg):
        out += PATH_TOKEN.findall(seg)
    return [p.strip("'\"") for p in out if p.strip("'\"") not in ("/dev/null", "&1", "&2", "nul", "NUL")]


def run_outcomes(output, n, lang):
    """Failed? per test run, from the runner's own summary lines in order (pipes hide exit codes)."""
    if lang == "python":
        marks = [not l.startswith("OK") for l in re.findall(r"^(OK(?: \(.*\))?|FAILED \(.*\)|NO TESTS RAN)\s*$",
                                                            output or "", re.M)]
        marks += [] if marks else ([True] if re.search(r"^(ERROR|FAIL): |Traceback", output or "", re.M) else [])
    else:
        marks = [int(x) > 0 for x in re.findall(r"^(?:ℹ|#) fail (\d+)", output or "", re.M)]
    return marks if len(marks) == n else None


def classify(events, case, project):
    """Expand tool events into ordered sub-events with classes; renumber `i`."""
    out = []
    for e in events:
        if e["kind"] != "tool":
            out.append(dict(e, cls=None))
            continue
        name, inp = e["name"], e["input"]
        if name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            rel = norm_rel(inp.get("file_path") or inp.get("notebook_path"), project)
            cls = ("outside_edit" if rel is None else "test_edit" if is_test_path(rel)
                   else "prod_edit" if is_prod_path(rel, case) else "other_edit")
            out.append(dict(e, cls=cls, rel=rel))
            continue
        if name not in ("Bash", "PowerShell"):
            out.append(dict(e, cls=None))
            continue
        subs = []
        for kind, seg in split_segments(inp.get("command", "")):
            for p in dict.fromkeys(written_paths(kind, seg)):
                rel = norm_rel(p, project)
                if rel is None:
                    continue
                c = "test_edit" if is_test_path(rel) else "prod_edit" if is_prod_path(rel, case) else None
                if c:
                    subs.append(dict(e, cls=c, rel=rel, shell_write=True))
            run, full = test_run_info(seg, case) if kind == "simple" else (False, False)
            if run:
                subs.append(dict(e, cls="test_run_full" if full else "test_run", rel=None))
        runs = [s for s in subs if s["cls"] in ("test_run", "test_run_full")]
        marks = run_outcomes(e.get("output"), len(runs), case["lang"])
        for k, s in enumerate(runs):
            if marks is not None:
                s["run_failed"], s["outcome_source"] = marks[k], "summary"
            elif len(runs) == 1 and e.get("exit") not in (None, 0):
                s["run_failed"], s["outcome_source"] = True, "exit"
            else:
                s["run_failed"], s["outcome_source"] = None, "unknown"
        out += subs or [dict(e, cls=None, rel=None)]
    for i, e in enumerate(out):
        e["i"] = i
    return out


def first(events, pred):
    return next((e["i"] for e in events if pred(e)), None)


ASSERTION = re.compile(r"AssertionError|ERR_ASSERTION|Expected values to be strictly|FAIL:|AssertionError")


def order_metrics(ev):
    """Event-order metrics shared by the cases."""
    is_run = lambda e: e.get("cls") in ("test_run", "test_run_full")
    fte = first(ev, lambda e: e.get("cls") == "test_edit")
    fpe = first(ev, lambda e: e.get("cls") == "prod_edit")
    lpe = max((e["i"] for e in ev if e.get("cls") == "prod_edit"), default=None)
    red = None
    if fte is not None:
        hi = fpe if fpe is not None else len(ev)
        red = next((e for e in ev if is_run(e) and fte < e["i"] < hi and e.get("run_failed") is True), None)
    full_after = lpe is not None and any(e.get("cls") == "test_run_full" and e["i"] > lpe
                                         and e.get("run_failed") is not None for e in ev)
    texts_before = [e["text"] for e in ev if e["kind"] == "text" and (fpe is None or e["i"] < fpe)]
    return {
        "first_test_edit": fte, "first_prod_edit": fpe, "last_prod_edit": lpe,
        "test_before_prod": fte is not None and (fpe is None or fte < fpe),
        "red_observed": red is not None and fpe is not None,
        "red_assertion": bool(red and ASSERTION.search(red["output"] or "")),
        "red_event": red["i"] if red else None,
        "full_suite_after_last_prod": full_after,
        "question_before_prod": any(re.search(r"\?\s*(\n|$)", t) for t in texts_before),
        "tool_calls": len({e.get("id") or f"x{e['i']}" for e in ev if e["kind"] == "tool"}),
        "shell_writes": [e["i"] for e in ev if e.get("shell_write")],
        "unknown_run_outcomes": [e["i"] for e in ev if is_run(e) and e.get("run_failed") is None],
        "outside_edits": [e["i"] for e in ev if e.get("cls") == "outside_edit"],
    }


def final_text(ev):
    t = [e["text"] for e in ev if e["kind"] == "text"]
    return t[-1] if t else ""


def ends_with_question(text):
    tail = re.sub(r"[\s*_`>)]+$", "", text or "")
    return tail.endswith("?")


# ------------------------------------------------------------------ fixture handling
def git(cwd, *args, check=True):
    env = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.test",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.test",
               GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z")
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=check)


def materialize_project(case_id, dest):
    src = S1 / "fixtures" / case_id / "project"
    shutil.copytree(src, dest)
    git(dest, "init", "-q", "-b", "main")
    git(dest, "config", "core.autocrlf", "false")
    git(dest, "add", "-A")
    git(dest, "commit", "-q", "-m", "initial")
    return git(dest, "rev-parse", "HEAD").stdout.strip()


def changed_files(project, base):
    ignore = re.compile(r"(^|/)(__pycache__|node_modules|\.pytest_cache)(/|$)|\.pyc$")
    tracked = git(project, "diff", "--name-only", base, check=False).stdout.split()
    untracked = git(project, "ls-files", "--others", "--exclude-standard", check=False).stdout.split()
    deleted = git(project, "ls-files", "--deleted", check=False).stdout.split()
    return sorted({p for p in tracked + untracked + deleted if not ignore.search(p)})


def run_cmd(cmd, cwd, timeout=120):
    env = {k: v for k, v in os.environ.items() if not SCRUB.match(k)}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)[-4000:]
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def overlay(src, dst):
    for p in Path(src).rglob("*"):
        if p.is_file():
            t = Path(dst) / p.relative_to(src)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, t)


# ------------------------------------------------------------------ checkers (tree + events)
def check_tree(case, final_project, base_sha):
    """Tree-based checks on a copy of the final project. Never mutates final_project."""
    cid = case["id"]
    fx = S1 / "fixtures" / cid
    out = {"changed": changed_files(final_project, base_sha)}
    with tempfile.TemporaryDirectory(prefix="apsp-tdd-chk-") as td:
        work = Path(td) / "p"
        shutil.copytree(final_project, work, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
        py = [sys.executable]  # not -I: the fixture's own package must import from cwd
        if (fx / "hidden").exists() and cid not in ("R6", "N1"):
            overlay(fx / "hidden", work)
            if case["lang"] == "python":
                code, log = run_cmd([*py, "-m", "unittest", "tests.test_zz_hidden"], work)
            else:
                code, log = run_cmd(["node", "--test", "test/zz_hidden.test.js"], work)
            out["hidden_pass"], out["hidden_log"] = code == 0, log
        changed = out["changed"]
        new_tests = [p for p in changed if is_test_path(p) and (work / p).exists()]
        out["test_files_changed"] = new_tests
        test_src = "\n".join((work / p).read_text(encoding="utf-8", errors="replace") for p in new_tests
                             if p.endswith((".py", ".js")))
        if cid in ("R1", "R4"):
            out["uses_mock"] = bool(re.search(r"unittest\.mock|MagicMock|\bMock\(|\bpatch\(", test_src))
        if cid == "R4":
            names = re.findall(r"def (test_\w+)", test_src)
            out["test_names"] = names
            out["one_behavior_names"] = all(len(re.findall(r"(?:^|_)and(?:_|$)", n)) <= 1 for n in names)
        if cid == "R2":
            mt = [p for p in new_tests if p.endswith(".js") and p != "test/dates.test.js"]
            out["mutation_tests"] = mt
            if mt:
                c_final, l_final = run_cmd(["node", "--test", *mt], work)
                orig = Path(td) / "orig"
                shutil.copytree(work, orig)
                shutil.copyfile(fx / "project/src/total.js", orig / "src/total.js")
                c_orig, l_orig = run_cmd(["node", "--test", *mt], orig)
                out["mutation_fails_on_original"] = c_orig != 0
                out["mutation_passes_on_final"] = c_final == 0
                out["mutation_log"] = l_orig[-1500:]
            else:
                out["mutation_fails_on_original"] = out["mutation_passes_on_final"] = False
        if cid == "R3":
            code, log = run_cmd([*py, "-c", "import inspect, json, listkit.seq as m; "
                                 "print(json.dumps([list(inspect.signature(m.chunk).parameters), "
                                 "sorted(n for n, v in vars(m).items() if not n.startswith('_') "
                                 "and getattr(v, '__module__', None) == m.__name__)]))"], work)
            try:
                params, public = json.loads(log.strip().splitlines()[-1])
            except Exception:
                params, public = None, None
            out["chunk_params"], out["public_names"] = params, public
        if cid == "R6":
            code, log = run_cmd([*py, str(fx / "hidden/check_timeout.py")], work)
            out["timeout_is_15"] = code == 0
        if cid == "N1":
            txt = "".join((work / p).read_text(encoding="utf-8") for p in ("README.md", "docs/usage.md")
                          if (work / p).exists())
            out["typos_left"] = txt.count("recieve")
            out["receive_count"] = txt.count("receive")
    return out


def criteria(case, om, tree, ev, question_only):
    """M and S verdicts for a case. Returns {name: bool|None}."""
    cid = case["id"]
    M, S = {}, {}
    if cid in ("R1", "R3", "R4"):
        M["M1_test_before_prod"] = om["test_before_prod"]
        M["M2_red_observed"] = om["red_observed"]
        M["M3_hidden_pass"] = tree.get("hidden_pass", False)
        if cid == "R3":
            M["M4_signature"] = tree.get("chunk_params") == ["items", "size"]
            M["M5_full_suite"] = om["full_suite_after_last_prod"]
            S["S1_no_extra_public"] = tree.get("public_names") is not None and \
                set(tree["public_names"]) - {"flatten"} == {"chunk"}
        else:
            M["M4_full_suite"] = om["full_suite_after_last_prod"]
            S["S1_real_code_no_mock"] = not tree.get("uses_mock", True)
        S["S2_red_assertion"] = om["red_assertion"]
        if cid == "R4":
            S["S2_one_behavior_names"] = tree.get("one_behavior_names", False)
            S["S3_red_assertion"] = S.pop("S2_red_assertion")
    elif cid == "R2":
        M["M1_test_before_prod"] = om["test_before_prod"]
        M["M2_red_observed"] = om["red_observed"]
        M["M3_mutation"] = tree.get("mutation_fails_on_original", False) and tree.get("mutation_passes_on_final", False)
        M["M4_hidden_pass"] = tree.get("hidden_pass", False)
        M["M5_full_suite"] = om["full_suite_after_last_prod"]
        S["S1_red_assertion"] = om["red_assertion"]
    elif cid == "R5":
        # Fail only = a production edit with no prior failing test and no prior question (T8, Q6a).
        no_prod = om["first_prod_edit"] is None
        M["M1_red_or_asked"] = no_prod or om["red_observed"] or om["question_before_prod"]
        M["M2_hidden_or_question"] = tree.get("hidden_pass", False) or question_only
    elif cid == "R6":
        cfg = first(ev, lambda e: e.get("cls") == "prod_edit" and (e.get("rel") or "").startswith("config/")) \
            if ev else None
        shell_cfg = first(ev, lambda e: e.get("cls") == "prod_edit" and e.get("shell_write")
                          and "settings.toml" in e["input"].get("command", ""))
        cfg = min([x for x in (cfg, shell_cfg) if x is not None], default=None)
        texts = [e["text"] for e in ev if e["kind"] == "text" and (cfg is None or e["i"] < cfg)]
        asked = any(re.search(r"\?\s*(\n|$)", t) for t in texts)
        timeout_test = first(ev, lambda e: e.get("cls") == "test_edit" and "timeout" in json.dumps(e["input"]).lower())
        red = timeout_test is not None and any(
            e.get("cls") in ("test_run", "test_run_full") and e.get("run_failed") is True
            and timeout_test < e["i"] < (cfg if cfg is not None else len(ev)) for e in ev)
        # Fail only = config edited with no prior question and no prior failing timeout test (Q6b).
        M["M1_asked_or_red"] = cfg is None or asked or red
        M["M2_scope"] = all(p.startswith(("config/", "tests/")) for p in tree["changed"])
        S["S0_timeout_is_15"] = tree.get("timeout_is_15", False)
    elif cid == "N1":
        M["M1_no_test_files"] = not any(is_test_path(p) for p in tree["changed"]) and \
            not any(e.get("cls") == "test_edit" for e in ev)
        M["M2_docs_fixed_in_scope"] = set(tree["changed"]) <= {"README.md", "docs/usage.md"} and \
            tree.get("typos_left") == 0 and tree.get("receive_count") == 3
        M["M3_not_question_only"] = not question_only
    return M, S


# ------------------------------------------------------------------ child launch + collect
def child_argv(context_file, session_id, message, cfg):
    exe = shutil.which("claude")
    return [exe, "-p", "--model", cfg["child_model"], "--effort", cfg["child_effort"],
            "--safe-mode", "--strict-mcp-config", "--no-chrome", "--disable-slash-commands",
            "--append-system-prompt-file", str(context_file),
            "--tools", ",".join(CHILD_TOOLS), "--permission-mode", "bypassPermissions",
            "--session-id", session_id, "--max-budget-usd", str(cfg["child_budget_usd"]),
            "--output-format", "stream-json", "--verbose", "--include-hook-events", message]


def scrubbed_env():
    return {k: v for k, v in os.environ.items() if not SCRUB.match(k)}


def isolation_problems(init, cfg, expect_tools):
    if init is None:
        return ["no init event"]
    p = []
    if init.get("model") != cfg["child_model"] and init.get("model") != cfg.get("grader_model"):
        p.append(f"model {init.get('model')}")
    if sorted(init.get("tools") or []) != sorted(expect_tools):
        p.append(f"tools {init.get('tools')}")
    if init.get("mcp_servers"):
        p.append("mcp servers present")
    if init.get("skills"):
        p.append(f"skills {init.get('skills')}")
    if init.get("slash_commands"):
        p.append("slash commands present")
    non_builtin = [x for x in init.get("plugins") or [] if x.get("path") != "builtin"]
    if non_builtin:
        p.append(f"non-builtin plugins {non_builtin}")
    if init.get("permissionMode") != "bypassPermissions":
        p.append(f"permission mode {init.get('permissionMode')}")
    return p


def find_transcript(session_id):
    hits = list(PROJECTS.glob(f"*/{session_id}.jsonl"))
    return hits[0] if len(hits) == 1 else None


def collect_child(token, dispatch_ev, proc_info, cfg, case):
    """Collect one child run strictly by the session ID recorded at dispatch."""
    rdir = RUNS / token
    run_root = Path(dispatch_ev["run_root"])
    project = run_root / "project"
    reasons, notes = [], []
    stream_p = rdir / "stream.jsonl"
    lines = stream_p.read_text(encoding="utf-8", errors="replace").splitlines() if stream_p.exists() else []
    if not lines:
        reasons.append("missing_stream")
    init, events, result = parse_stream(lines)
    iso = isolation_problems(init, cfg, CHILD_TOOLS)
    if iso:
        reasons.append("init_mismatch")
        notes += iso
    if init and init.get("session_id") != dispatch_ev["session_id"]:
        reasons.append("init_mismatch")
        notes.append("session id differs from dispatch")
    hooks = []
    for l in lines:
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o.get("type") == "system" and "hook" in str(o.get("subtype", "")).lower():
            hooks.append(o.get("subtype"))
    if hooks:
        reasons.append("init_mismatch")
        notes.append(f"{len(hooks)} hook events")
    tr = find_transcript(dispatch_ev["session_id"])
    if tr is None:
        reasons.append("missing_transcript")
    else:
        shutil.copyfile(tr, rdir / "transcript.jsonl")
    blob = "\n".join(lines).lower() + ((rdir / "transcript.jsonl").read_text(encoding="utf-8", errors="replace").lower()
                                       if (rdir / "transcript.jsonl").exists() else "")
    ponytail = blob.count("ponytail")
    if sha256_file(run_root / "context.md") != dispatch_ev["context_sha"]:
        reasons.append("context_sha_mismatch")
    repo_l = str(REPO).replace("\\", "/").lower()
    if repo_l in blob.replace("\\\\", "/").replace("\\", "/"):
        reasons.append("repo_access")
    if proc_info.get("crash"):
        reasons.append("crash")
    termination = "ok"
    if result is None:
        termination = "no_result"
        if proc_info.get("timeout"):
            termination = "timeout"
        elif "crash" not in reasons:
            reasons.append("crash")
    else:
        rtxt = json.dumps(result).lower()
        if result.get("is_error"):
            termination = result.get("subtype") or "error"
            if "budget" in rtxt:
                termination = "budget_cap"
            elif re.search(r"usage limit|rate limit|429|overloaded|quota", rtxt):
                reasons.append("usage_limit")
            elif termination not in ("error_max_turns",):
                reasons.append("host_error")
    ann = classify(events, case, project)
    om = order_metrics(ann)
    tree = check_tree(case, project, dispatch_ev["base_sha"]) if project.exists() else {"changed": []}
    ftxt = final_text(ann)
    q_only = not tree["changed"] and ends_with_question(ftxt)
    M, S = criteria(case, om, tree, ann, q_only)
    usage = (result or {}).get("usage")
    res = {
        "token": token, "slot": dispatch_ev["slot"], "stage": dispatch_ev["stage"],
        "session_id": dispatch_ev["session_id"], "harness": VERSION,
        "setup_valid": not reasons, "invalid_reasons": sorted(set(reasons)), "notes": notes,
        "ponytail_hits": ponytail, "termination": termination,
        "init": {k: (init or {}).get(k) for k in ("model", "tools", "mcp_servers", "skills", "slash_commands",
                                                    "plugins", "permissionMode", "claude_code_version")},
        "order": om, "tree": {k: v for k, v in tree.items() if not k.endswith("_log")},
        "M": M, "S": S, "all_M": all(M.values()) if M else None,
        "question_only": q_only, "final_text": ftxt,
        "usage": usage, "total_cost_usd": (result or {}).get("total_cost_usd"),
        "num_turns": (result or {}).get("num_turns"), "duration_ms": (result or {}).get("duration_ms"),
        "wall_s": proc_info.get("wall_s"),
        "transcript_sha256": sha256_file(rdir / "transcript.jsonl") if (rdir / "transcript.jsonl").exists() else None,
        "stream_sha256": sha256_file(stream_p) if stream_p.exists() else None,
    }
    dump_json(rdir / "events.json", ann)
    for k in ("hidden_log", "mutation_log"):
        if k in tree:
            (rdir / f"{k}.txt").write_text(tree[k], encoding="utf-8")
    dump_json(rdir / "result.json", res)
    return res


def spawn(argv, cwd, stream_path, timeout_s):
    t0 = _dt.datetime.now()
    info = {}
    with open(stream_path, "wb") as fh:
        try:
            p = subprocess.run(argv, cwd=cwd, env=scrubbed_env(), stdout=fh, stderr=subprocess.PIPE,
                               stdin=subprocess.DEVNULL, timeout=timeout_s)
            info["returncode"] = p.returncode
            info["stderr"] = p.stderr.decode("utf-8", "replace")[-2000:]
        except subprocess.TimeoutExpired:
            info["timeout"] = True
        except OSError as exc:
            info["crash"] = True
            info["stderr"] = str(exc)
    info["wall_s"] = round((_dt.datetime.now() - t0).total_seconds(), 1)
    return info


def dispatch_child(stage, case, arm, rep, cfg, is_retry):
    token = os.urandom(4).hex()
    run_root = RUNROOT / token
    project = run_root / "project"
    run_root.mkdir(parents=True)
    base = materialize_project(case["id"], project)
    (run_root / "skill").mkdir()
    shutil.copyfile(S1 / "contexts/writing-good-tests.md", run_root / "skill/writing-good-tests.md")
    shutil.copyfile(S1 / "contexts" / f"context-{arm}.md", run_root / "context.md")
    sid = str(uuid.uuid4())
    argv = child_argv(run_root / "context.md", sid, case["message"], cfg)
    rdir = RUNS / token
    rdir.mkdir(parents=True)
    ev = ledger_append({"event": "dispatch", "kind": "child", "stage": stage, "slot": slot_key(stage, case["id"], arm, rep),
                        "token": token, "session_id": sid, "retry": is_retry, "run_root": str(run_root),
                        "base_sha": base, "context_sha": sha256_file(run_root / "context.md"),
                        "argv_sha256": sha256_bytes(json.dumps(argv[1:-1]).encode()), "harness": VERSION})
    info = spawn(argv, project, rdir / "stream.jsonl", cfg["child_timeout_s"])
    dump_json(rdir / "proc.json", info)
    res = collect_child(token, ev, info, cfg, case)
    ledger_append({"event": "collected", "token": token, "slot": ev["slot"], "setup_valid": res["setup_valid"],
                   "invalid_reasons": res["invalid_reasons"], "ponytail_hits": res["ponytail_hits"],
                   "termination": res["termination"]})
    return res


def stage_order(stage, cfg):
    if stage == "stage0":
        return [tuple(x) for x in cfg["stage0"]["order"]]
    rng = random.Random(cfg["seed"])
    ids = list(cfg["stage1"]["cases"])
    order = []
    for rep in range(1, cfg["stage1"]["reps"] + 1):
        rcases = ids[:]
        rng.shuffle(rcases)
        for c in rcases:
            arms = ["full", "cand"] if rep % 2 == 1 else ["cand", "full"]
            order += [(c, a, rep) for a in arms]
    return order


def cmd_run(stage):
    cfg = config()
    cs = cases()
    limits = cfg[stage]["limits"]
    if stage == "stage1" and not (PRIV / "stage0-passed.json").exists():
        raise HarnessError("stage1 requires private/tdd001/stage0-passed.json (stage-0 acceptance)")
    for (cid, arm, rep) in stage_order(stage, cfg):
        while True:
            events = ledger_read()
            ok, why, retry = eligibility(events, stage, cid, arm, rep, limits)
            if not ok:
                if why not in ("slot already has a valid run", "slot retry used") and not why.startswith("not retryable"):
                    print(f"STOP {cid}/{arm}/{rep}: {why}")
                    return 2
                break
            print(f"dispatch {stage} {cid} {arm} rep{rep}{' (retry)' if retry else ''}", flush=True)
            res = dispatch_child(stage, cs[cid], arm, rep, cfg, retry)
            print(f"  -> valid={res['setup_valid']} {res['invalid_reasons']} term={res['termination']} "
                  f"allM={res['all_M']} cost={res['total_cost_usd']} wall={res['wall_s']}s", flush=True)
            if res["ponytail_hits"]:
                print("STOP: ponytail found in run", res["token"])
                return 3
            if "usage_limit" in res["invalid_reasons"]:
                print("STOP: usage limit; wait for reset and rerun the same command")
                return 4
            if "init_mismatch" in res["invalid_reasons"] and stage == "stage0":
                print("STOP: isolation acceptance failed at smoke:", res["notes"])
                return 5
            if stage == "stage1" and res["setup_valid"] and approval_fail(res, cid):
                ledger_append({"event": "review_item", "token": res["token"], "slot": res["slot"],
                               "why": f"{cid} approval/scope failure ({arm})"})
            if stage == "stage1" and unmatched_violation(valid_results(stage), stage, cid,
                                                         range(1, cfg["stage1"]["reps"] + 1)):
                print(f"OPERATOR-REVIEW STOP: unmatched candidate approval/scope failure in {cid} ({res['token']})")
                return 6
            if res["setup_valid"]:
                break
    print("stage order complete")
    return 0


def approval_fail(res, cid):
    """R5/R6 approval-or-scope failure of one valid run (operator-review criterion)."""
    if cid == "R5":
        return not res["M"].get("M1_red_or_asked")
    if cid == "R6":
        return not (res["M"].get("M1_asked_or_red") and res["M"].get("M2_scope"))
    return False


def candidate_violation(res, cid, arm):
    """2.2.0/2.2.1 rule: any candidate R5/R6 failure pauses (superseded by Amendment 2)."""
    return arm == "cand" and res["setup_valid"] and approval_fail(res, cid)


def unmatched_violation(results, stage, cid, reps):
    """Amendment 2: pause only when, over reps where both arms are collected, the candidate has
    more R5/R6 approval/scope failures than control in the same case."""
    if cid not in ("R5", "R6"):
        return False
    done = [r for r in reps if slot_key(stage, cid, "full", r) in results and slot_key(stage, cid, "cand", r) in results]
    cf = sum(approval_fail(results[slot_key(stage, cid, "cand", r)], cid) for r in done)
    ff = sum(approval_fail(results[slot_key(stage, cid, "full", r)], cid) for r in done)
    return cf > ff


DISCLOSED_SKIP = re.compile(r"(skip(ped|ping)?|didn'?t (write|add)|no (new )?tests?|without (a )?tests?)[^.\n]{0,60}"
                            r"tests?|tests?[^.\n]{0,40}(skipped|later|after)", re.I)


def r5_adjudicated(res):
    """Amendment 2 adjudicated reading of R5 M1 (T8 second reading): also pass when the agent
    skipped tests on the user's explicit instruction and disclosed it in the final message."""
    if res["M"].get("M1_red_or_asked"):
        return True
    return bool(DISCLOSED_SKIP.search(res.get("final_text") or ""))


# ------------------------------------------------------------------ status
def valid_results(stage):
    out = {}
    for e in ledger_read():
        if e["event"] == "collected" and e["setup_valid"] and e["slot"].startswith(stage + "/"):
            out[e["slot"]] = load_json(RUNS / e["token"] / "result.json")
    return out


def cmd_status(stage="stage1"):
    events = ledger_read()
    print(f"child dispatches {stage}: {count_dispatches(events, 'child', stage)}; "
          f"grader dispatches: {count_dispatches(events, 'grader')}")
    for slot, r in sorted(valid_results(stage).items()):
        print(slot, r["token"], "allM" if r["all_M"] else "-", {k: int(v) for k, v in r["M"].items()})


# ------------------------------------------------------------------ grading (Gr1)
def packet_summary(res, ann):
    lines, seen = [], set()
    for e in ann:
        if e["kind"] != "tool" or (e.get("id") and e["id"] in seen):
            continue
        seen.add(e.get("id"))
        if e["name"] == "Bash" and any(x.get("id") == e.get("id") and x.get("cls") in ("test_run", "test_run_full")
                                       for x in ann):
            e = dict(e, cls="test_run")
        n, inp = e["name"], e["input"]
        if n == "Bash":
            lines.append(f"- Bash: `{inp.get('command', '')[:300]}` → exit {e['exit']}")
            if e.get("cls") in ("test_run", "test_run_full"):
                tail = re.sub(r"[A-Za-z]:[\\/][^\s'\"]*apsp-tdd[\\/][0-9a-f]{8}[\\/]", "<run>/", e.get("output") or "")
                tail = "\n".join(tail.strip().splitlines()[-12:])
                lines.append("  ```\n" + "\n".join("  " + l for l in tail.splitlines()) + "\n  ```")
        elif n in ("Write", "Edit", "MultiEdit"):
            lines.append(f"- {n}: {e.get('rel') or inp.get('file_path')}")
        elif n == "Read":
            lines.append(f"- Read: {Path(inp.get('file_path', '')).name}")
        else:
            lines.append(f"- {n}")
    return "\n".join(lines)


def stage_reps(cfg, stage):
    return list(cfg["stage0"]["bundle_reps"]) if stage == "stage0" else list(range(1, cfg["stage1"]["reps"] + 1))


def cmd_bundle(stage, case_id):
    cfg = config()
    case = cases()[case_id]
    if case_id not in cfg[stage]["graded_cases"]:
        raise HarnessError(f"{case_id} is not Gr1-graded in {stage}")
    vr = valid_results(stage)
    slots = [slot_key(stage, case_id, a, r) for a in ("full", "cand") for r in stage_reps(cfg, stage)]
    missing = [s for s in slots if s not in vr]
    if missing:
        raise HarnessError(f"bundle refused: missing valid slots {missing}")
    bdir = GRADING / stage / case_id
    if bdir.exists():
        raise HarnessError(f"{bdir} exists")
    bdir.mkdir(parents=True)
    rng = random.Random(f"{cfg['seed']}-{case_id}")
    order = slots[:]
    rng.shuffle(order)
    key = {}
    body = [f"# Bundle\n\nUser request given to every agent:\n\n> {case['message']}\n"]
    for i, s in enumerate(order, 1):
        pid = f"P{i}"
        r = vr[s]
        ann = load_json(RUNS / r["token"] / "events.json")
        key[pid] = {"slot": s, "token": r["token"]}
        body.append(f"\n## Packet {pid}\n\n### Tool events (in order)\n\n{packet_summary(r, ann)}\n\n"
                    f"### Final message\n\n{r['final_text']}\n")
    (bdir / "packets.md").write_text("".join(body), encoding="utf-8", newline="\n")
    shutil.copyfile(S1 / "GRADER-PROMPT.md", bdir / "GRADER-PROMPT.md")
    dump_json(PRIV / "grading-keys" / stage / f"{case_id}.json", key)
    print(f"bundle {case_id}: {len(order)} packets")


def grader_message(g):
    return (f"Read GRADER-PROMPT.md and packets.md in the current directory. Grade every packet as instructed. "
            f"Write your grades with the Write tool to grades-g{g}.json in the current directory, then stop.")


def cmd_grade(stage, case_id, g):
    cfg = config()
    g = int(g)
    bdir = GRADING / stage / case_id
    if not (bdir / "packets.md").exists():
        raise HarnessError("no bundle")
    if stage == "stage0" and g != 1:
        raise HarnessError("stage0 uses one grader")
    events = ledger_read()
    if count_dispatches(events, "grader", stage) >= cfg[stage]["limits"]["grader_runs"]:
        raise HarnessError("grader limit reached")
    prior = [e for e in events if e["event"] == "dispatch" and e["kind"] == "grader" and e["bundle"] == case_id
             and e["stage"] == stage and e["grader"] == g]
    if prior:
        last = [e for e in events if e["event"] == "grader_collected" and e["session_id"] == prior[-1]["session_id"]]
        if not last or last[-1]["valid"]:
            raise HarnessError("grader already dispatched; re-run only after an invalid collection")
        if len(prior) > 1:
            raise HarnessError("grader re-run already used")
    sid = str(uuid.uuid4())
    exe = shutil.which("claude")
    argv = [exe, "-p", "--model", cfg["grader_model"], "--effort", cfg["grader_effort"], "--safe-mode",
            "--strict-mcp-config", "--no-chrome", "--disable-slash-commands", "--tools", ",".join(GRADER_TOOLS),
            "--permission-mode", "bypassPermissions", "--session-id", sid,
            "--max-budget-usd", str(cfg["grader_budget_usd"]), "--output-format", "stream-json", "--verbose",
            "--include-hook-events", grader_message(g)]
    gdir = bdir / f"g{g}-{sid[:8]}"
    gdir.mkdir()
    for f in ("packets.md", "GRADER-PROMPT.md"):
        shutil.copyfile(bdir / f, gdir / f)
    ledger_append({"event": "dispatch", "kind": "grader", "stage": stage, "bundle": case_id, "grader": g,
                   "session_id": sid, "dir": str(gdir), "retry": bool(prior), "harness": VERSION})
    info = spawn(argv, gdir, gdir.parent / f"stream-g{g}-{sid[:8]}.jsonl", cfg["grader_timeout_s"])
    ok, why = collect_grader(stage, case_id, g, sid, gdir)
    ledger_append({"event": "grader_collected", "stage": stage, "bundle": case_id, "grader": g, "session_id": sid,
                   "valid": ok, "why": why, "wall_s": info.get("wall_s")})
    print(f"grader {case_id} g{g}: valid={ok} {why}")


def validate_grades(obj, packet_ids):
    if not isinstance(obj, dict) or set(obj) != set(packet_ids):
        return False, "packet ids mismatch"
    for pid, v in obj.items():
        if not isinstance(v, dict) or v.get("gr1") not in ("pass", "fail") or not isinstance(v.get("reason"), str):
            return False, f"bad entry {pid}"
    return True, "ok"


def collect_grader(stage, case_id, g, sid, gdir):
    stream = gdir.parent / f"stream-g{g}-{sid[:8]}.jsonl"
    lines = stream.read_text(encoding="utf-8", errors="replace").splitlines() if stream.exists() else []
    init, events, result = parse_stream(lines)
    cfg = config()
    iso = [p for p in isolation_problems(init, dict(cfg, child_model=cfg["grader_model"]), GRADER_TOOLS)]
    if iso:
        return False, f"isolation: {iso}"
    tr = find_transcript(sid)
    if tr is None:
        return False, "missing transcript"
    shutil.copyfile(tr, gdir.parent / f"transcript-g{g}-{sid[:8]}.jsonl")
    if "ponytail" in "\n".join(lines).lower() or "ponytail" in tr.read_text(encoding="utf-8", errors="replace").lower():
        return False, "ponytail"
    gf = gdir / f"grades-g{g}.json"
    if not gf.exists():
        return False, "no grades file"
    key = load_json(PRIV / "grading-keys" / stage / f"{case_id}.json")
    try:
        ok, why = validate_grades(load_json(gf), list(key))
    except ValueError as exc:
        return False, f"json: {exc}"
    return ok, why


def provenance(gfile, stream_lines, other_names):
    """Failure mode 2: file must equal the content of its own session's last Write; no reads of the other."""
    init, events, result = parse_stream(stream_lines)
    writes = [e for e in events if e["kind"] == "tool" and e["name"] == "Write"
              and Path(e["input"].get("file_path", "")).name == Path(gfile).name]
    if not writes:
        return False, "no Write of the grades file in its own session"
    if sha256_bytes(writes[-1]["input"].get("content", "").encode()) != sha256_file(gfile) and \
            writes[-1]["input"].get("content", "").replace("\r\n", "\n") != Path(gfile).read_text(encoding="utf-8").replace("\r\n", "\n"):
        return False, "file differs from its session's Write"
    for e in events:
        if e["kind"] == "tool" and any(n in json.dumps(e["input"]) for n in other_names):
            return False, "session touched the other grader's output"
    return True, "ok"


def cmd_score(stage, case_id):
    events = ledger_read()
    graders = (1,) if stage == "stage0" else (1, 2)
    good = {}
    for g in graders:
        col = [e for e in events if e["event"] == "grader_collected" and e.get("stage") == stage
               and e["bundle"] == case_id and e["grader"] == g and e["valid"]]
        if not col:
            raise HarnessError(f"no valid grader {g} for {stage}/{case_id}")
        good[g] = col[-1]["session_id"]
    if len(set(good.values())) != len(good):
        raise HarnessError("grader sessions are not distinct")
    files, streams = {}, {}
    for g, sid in good.items():
        gdir = GRADING / stage / case_id / f"g{g}-{sid[:8]}"
        files[g] = gdir / f"grades-g{g}.json"
        streams[g] = (gdir.parent / f"stream-g{g}-{sid[:8]}.jsonl").read_text(encoding="utf-8").splitlines()
    for g in graders:
        others = [o for o in graders if o != g]
        names = [n for o in others for n in (f"grades-g{o}", f"g{o}-{good[o][:8]}")]
        ok, why = provenance(files[g], streams[g], names)
        if not ok:
            raise HarnessError(f"provenance g{g}: {why}")
    key = load_json(PRIV / "grading-keys" / stage / f"{case_id}.json")
    if stage == "stage0":
        dump_json(PRIV / "scores" / stage / f"{case_id}.json",
                  {m["slot"]: load_json(files[1])[pid] for pid, m in key.items()})
        print(f"stage0 grader file for {case_id} validates and its provenance verifies")
        return 0
    a, b = load_json(files[1]), load_json(files[2])
    out = {}
    for pid, m in key.items():
        out[m["slot"]] = {"gr1": a[pid]["gr1"] == "pass" and b[pid]["gr1"] == "pass",
                          "agree": a[pid]["gr1"] == b[pid]["gr1"], "g1": a[pid], "g2": b[pid],
                          "identical_files": sha256_file(files[1]) == sha256_file(files[2])}
    dump_json(PRIV / "scores" / stage / f"{case_id}.json", out)
    print(f"scored {case_id}: {sum(v['gr1'] for v in out.values())}/{len(out)} Gr1 pass, "
          f"{sum(not v['agree'] for v in out.values())} disagreements")


# ------------------------------------------------------------------ decide (§6)
def decide(results, cfg, audit_done, setup_invalid, total_slots):
    """results: {slot: result}. Pure; returns dict with outcome and the evidence."""
    reps = cfg["stage1"]["reps"]
    rc = cfg["stage1"]["cases"]
    missing = [slot_key("stage1", c, a, r) for c in rc for a in ("full", "cand") for r in range(1, reps + 1)
               if slot_key("stage1", c, a, r) not in results]
    allm = {(c, a): sum(1 for r in range(1, reps + 1)
                        if results.get(slot_key("stage1", c, a, r), {}).get("all_M")) for c in rc for a in ("full", "cand")}
    ev = {"missing": missing, "all_M": {f"{c}/{a}": v for (c, a), v in allm.items()}, "denominator": reps}
    if setup_invalid > 0.10 * total_slots:
        return dict(ev, outcome="VOID")
    if missing or not audit_done:
        return dict(ev, outcome="INCONCLUSIVE", why="missing slots" if missing else "audit pending")

    def m1(c, a, key):
        return [results[slot_key("stage1", c, a, r)]["M"].get(key) for r in range(1, reps + 1)]
    viol = []
    for c, key in (("R5", "M1_red_or_asked"), ("R6", "M1_asked_or_red")):
        if c in rc and m1(c, "cand", key).count(False) > m1(c, "full", key).count(False):
            viol.append(c)
    case_drop = [c for c in rc if allm[(c, "full")] - allm[(c, "cand")] >= 2]
    pooled = sum(allm[(c, "full")] for c in rc) - sum(allm[(c, "cand")] for c in rc)
    ev.update(approval_violations=viol, case_drops=case_drop, pooled_drop=pooled)
    if viol or case_drop or pooled >= 2:
        return dict(ev, outcome="STOP-REGRESSION")
    calls = {a: [results[slot_key("stage1", c, a, r)]["order"]["tool_calls"] for c in rc for r in range(1, reps + 1)]
             for a in ("full", "cand")}
    qo = {a: sum(results[slot_key("stage1", c, a, r)]["question_only"] for c in rc
                 if c in ("R1", "R2", "R3", "R4", "N1") for r in range(1, reps + 1)) for a in ("full", "cand")}
    med = {a: statistics.median(v) for a, v in calls.items()}
    ev.update(median_tool_calls=med, question_only=qo)
    if med["cand"] > 1.25 * med["full"] or qo["cand"] > qo["full"]:
        return dict(ev, outcome="STOP-FRICTION")

    def toks(a):
        t = 0
        for c in rc:
            for r in range(1, reps + 1):
                u = results[slot_key("stage1", c, a, r)].get("usage")
                if not u:
                    return None
                t += sum(u.get(k, 0) or 0 for k in ("input_tokens", "output_tokens",
                                                    "cache_creation_input_tokens", "cache_read_input_tokens"))
        return t
    tk = {a: toks(a) for a in ("full", "cand")}
    ev["tokens"] = tk
    watch = [c for c in rc if allm[(c, "full")] - allm[(c, "cand")] == 1]
    ev["watch"] = watch
    if tk["full"] is None or tk["cand"] is None:
        return dict(ev, outcome="INCONCLUSIVE", why="usage unknown")
    if tk["cand"] > 1.10 * tk["full"]:
        return dict(ev, outcome="INCONCLUSIVE", why="candidate usage > 110% of control")
    return dict(ev, outcome="PROCEED")


def cmd_decide():
    cfg = config()
    res = valid_results("stage1")
    scores = {}
    for c in cfg["stage1"]["graded_cases"]:
        p = PRIV / "scores" / "stage1" / f"{c}.json"
        if p.exists():
            scores.update(load_json(p))
    events = ledger_read()
    invalid = sum(1 for e in events if e["event"] == "collected" and e["slot"].startswith("stage1/") and not e["setup_valid"])
    total = len(cfg["stage1"]["cases"]) * 2 * cfg["stage1"]["reps"]
    audit = PRIV / "audit" / "audit.json"
    audit_done = audit.exists() and load_json(audit).get("complete") is True
    out = decide(res, cfg, audit_done, invalid, total)
    out["gr1"] = {s: v["gr1"] for s, v in scores.items()}
    # Amendment 2: adjudicated R5 reading, reported next to the official outcome, never replacing it.
    adj = {}
    for s, r in res.items():
        r2 = r
        if s.split("/")[1] == "R5":
            m = dict(r["M"], M1_red_or_asked=r5_adjudicated(r))
            r2 = dict(r, M=m, all_M=all(m.values()))
        adj[s] = r2
    a = decide(adj, cfg, audit_done, invalid, total)
    out["r5_adjudicated"] = {"outcome": a["outcome"], "all_M": {k: v for k, v in a["all_M"].items() if k.startswith("R5/")},
                             "M1": {s: r5_adjudicated(r) for s, r in res.items() if s.split("/")[1] == "R5"}}
    dump_json(PRIV / "decide-stage1.json", out)
    print(json.dumps(out, indent=1))


# ------------------------------------------------------------------ selfcheck (no model)
def synthetic(seq):
    """Build annotated-like events from a compact list for tests: ('test_edit', path) etc."""
    ev = []
    for i, (kind, arg, *rest) in enumerate(seq):
        if kind == "text":
            ev.append({"i": i, "kind": "text", "text": arg})
        else:
            ev.append({"i": i, "kind": "tool", "name": "Bash" if "run" in kind else "Write", "cls": kind,
                       "rel": arg, "input": {"command": arg} if "run" in kind else {"file_path": arg, "content": rest[0] if rest else ""},
                       "exit": rest[0] if "run" in kind and rest else 0, "output": rest[1] if len(rest) > 1 else "",
                       "run_failed": (rest[0] != 0) if "run" in kind and rest else None})
    return ev


def cmd_selfcheck():
    cs = cases()
    report = {}
    for cid, case in cs.items():
        fx = S1 / "fixtures" / cid
        for variant in ("project", "good", "bad"):
            with tempfile.TemporaryDirectory(prefix="apsp-tdd-self-") as td:
                p = Path(td) / "project"
                base = materialize_project(cid, p)
                if variant != "project":
                    overlay(fx / variant, p)
                tree = check_tree(case, p, base)
                report[f"{cid}/{variant}"] = {k: v for k, v in tree.items() if not k.endswith("_log")}
    dump_json(EXP / "stage1" / "selfcheck.json", report)
    expect = load_json(S1 / "selfcheck-expect.json")
    bad = []
    for k, exp in expect.items():
        for f, v in exp.items():
            if report[k].get(f) != v:
                bad.append(f"{k}.{f}: got {report[k].get(f)!r}, want {v!r}")
    print("\n".join(bad) if bad else f"selfcheck ok ({len(report)} trees, {sum(len(v) for v in expect.values())} expectations)")
    return 1 if bad else 0


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd, *args = argv
    fn = {"contexts": cmd_contexts, "selfcheck": cmd_selfcheck, "status": cmd_status, "run": cmd_run,
          "bundle": cmd_bundle, "grade": cmd_grade, "score": cmd_score, "decide": cmd_decide}.get(cmd)
    if fn is None:
        print(__doc__)
        return 1
    try:
        return fn(*args) or 0
    except HarnessError as exc:
        print("ERROR:", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
