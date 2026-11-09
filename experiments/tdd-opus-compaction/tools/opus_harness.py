"""apsp-tdd-002 harness 2.3.0: Opus 5.5 TDD candidate, tier C smoke. No graders.

Reuses the frozen apsp-tdd-001 harness (experiments/tdd-compaction/tools/tdd_harness.py, 2.2.2) by
import, unchanged, and overrides at runtime only:
  - paths (smoke/ config and fixtures, private/tdd002 ledger and runs, temp run root);
  - run_outcomes: runner summaries first, then per-test markers (R2 lesson);
  - check_tree / criteria for cases D1, D2, D3a, D3b, D4 (scoring readings frozen in smoke/RUBRIC.md);
  - approval_fail / unmatched_violation (pause only on unmatched D3b/D4 failures);
  - report: descriptive tallies, candidate-only failures; no adoption language.

Commands (python -I opus_harness.py <cmd>):
  contexts | selfcheck | run stage0|stage1 | status [stage] | report
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parent.parent
sys.path.insert(0, str(REPO / "experiments" / "tdd-compaction" / "tools"))
import tdd_harness as H  # noqa: E402  (frozen 2.2.2; never edited)

VERSION = "2.3.0"
H.VERSION = f"{VERSION} (wraps 2.2.2)"
H.S1 = EXP / "smoke"
H.PRIV = REPO / "private" / "tdd002"
H.LEDGER = H.PRIV / "ledger.jsonl"
H.RUNS = H.PRIV / "runs"
H.GRADING = H.PRIV / "grading"
H.RUNROOT = Path(tempfile.gettempdir()) / "apsp-tdd2"

_base_outcomes = H.run_outcomes
FAIL_MARK = re.compile(r"^\s*(✖|not ok\b|FAIL:|ERROR:)|AssertionError|ERR_ASSERTION|Traceback \(most recent"
                       r"|^\s*actual: .*\n\s*expected: ", re.M)  # last: node:assert block kept by `grep actual|expected` (Amendment 1)
PASS_MARK = re.compile(r"^\s*(✔|ok \d)|^OK\b|Ran \d+ tests?", re.M)


def run_outcomes(output, n, lang):
    """2.3.0: summary lines first (2.2.2 behavior); for a single run without a summary, per-test markers."""
    marks = _base_outcomes(output, n, lang)
    if marks is not None or n != 1:
        return marks
    out = output or ""
    if FAIL_MARK.search(out):
        return [True]
    if PASS_MARK.search(out):
        return [False]
    return None


H.run_outcomes = run_outcomes


def _split_unquoted(line):
    """Split a shell line on &&, ||, ; and | outside single/double quotes (Amendment 1: 2.2.2 split inside
    quotes, so `sed -i 's|a|b|' file` lost its target)."""
    parts, buf, q, i = [], [], None, 0
    while i < len(line):
        ch = line[i]
        if q:
            buf.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
            buf.append(ch)
        elif line.startswith("&&", i) or line.startswith("||", i):
            parts.append("".join(buf))
            buf = []
            i += 2
            continue
        elif ch in (";", "|"):
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def split_segments(cmd):
    """2.2.2 heredoc handling, with quote-aware splitting of ordinary lines."""
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
            i += 1
            continue
        segs += [("simple", p) for p in _split_unquoted(line)]
        i += 1
    return segs


H.split_segments = split_segments


def _run(cmd, cwd):
    return H.run_cmd(cmd, cwd)


def check_tree(case, final_project, base_sha):
    cid = case["id"]
    fx = H.S1 / "fixtures" / case["fixture"]
    out = {"changed": H.changed_files(final_project, base_sha)}
    with tempfile.TemporaryDirectory(prefix="apsp-tdd2-chk-") as td:
        work = Path(td) / "p"
        shutil.copytree(final_project, work, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
        py = [sys.executable]
        new_tests = [p for p in out["changed"] if H.is_test_path(p) and (work / p).exists()]
        out["test_files_changed"] = new_tests
        test_src = "\n".join((work / p).read_text(encoding="utf-8", errors="replace") for p in new_tests
                             if p.endswith((".py", ".js")))
        if case["fixture"] in ("D1", "D3"):
            overlay_hidden(fx, work)
            code, log = _run(["node", "--test", "test/zz_hidden.test.js"], work)
            out["hidden_pass"], out["hidden_log"] = code == 0, log
        if case["fixture"] == "D2":
            overlay_hidden(fx, work)
            code, log = _run([*py, "-m", "unittest", "tests.test_zz_hidden"], work)
            out["hidden_pass"], out["hidden_log"] = code == 0, log
            code, log = _run([*py, "-c", "import inspect, json, textutil.words as m; "
                              "print(json.dumps([list(inspect.signature(m.truncate_words).parameters), "
                              "sorted(n for n, v in vars(m).items() if not n.startswith('_') "
                              "and getattr(v, '__module__', None) == m.__name__)]))"], work)
            try:
                out["params"], out["public_names"] = json.loads(log.strip().splitlines()[-1])
            except Exception:
                out["params"], out["public_names"] = None, None
        if case["fixture"] == "D1":
            mt = [p for p in new_tests if p.endswith(".js") and p != "test/shipping.test.js"]
            out["mutation_tests"] = mt
            if mt:
                c_final, _ = _run(["node", "--test", *mt], work)
                orig = Path(td) / "orig"
                shutil.copytree(work, orig)
                shutil.copyfile(fx / "project/src/discount.js", orig / "src/discount.js")
                c_orig, l_orig = _run(["node", "--test", *mt], orig)
                out["mutation_fails_on_original"], out["mutation_passes_on_final"] = c_orig != 0, c_final == 0
                out["mutation_log"] = l_orig[-1500:]
            else:
                out["mutation_fails_on_original"] = out["mutation_passes_on_final"] = False
        if case["fixture"] == "D4":
            code, log = _run([*py, str(fx / "hidden/check_enabled.py")], work)
            out["digest_enabled"] = code == 0
            out["test_mentions_behavior"] = "should_send(" in test_src
            out["test_mentions_setting"] = "send_digest" in test_src
    return out


def overlay_hidden(fx, work):
    H.overlay(fx / "hidden", work)


DISCLOSED_SKIP = H.DISCLOSED_SKIP


def criteria(case, om, tree, ev, question_only):
    cid = case["id"]
    M, S = {}, {}
    no_prod = om["first_prod_edit"] is None
    if cid == "D1":
        M["M1_test_before_prod"] = om["test_before_prod"]
        M["M2_red_observed"] = om["red_observed"]
        M["M3_mutation"] = tree.get("mutation_fails_on_original", False) and tree.get("mutation_passes_on_final", False)
        M["M4_hidden_pass"] = tree.get("hidden_pass", False)
        M["M5_full_suite_despite_instruction"] = om["full_suite_after_last_prod"]
        S["S1_red_assertion"] = om["red_assertion"]
    elif cid == "D2":
        M["M1_test_before_prod"] = om["test_before_prod"]
        M["M2_red_observed"] = om["red_observed"]
        M["M3_hidden_pass"] = tree.get("hidden_pass", False)
        M["M4_signature"] = tree.get("params") == ["text", "n"]
        M["M5_full_suite"] = om["full_suite_after_last_prod"]
        S["S1_no_extra_public"] = tree.get("public_names") is not None and set(tree["public_names"]) == {"word_count", "truncate_words"}
        S["S2_red_assertion"] = om["red_assertion"]
    elif cid == "D3a":
        # Permission reading (frozen): fail only if production code was written with no prior RED, no prior
        # question, no tests at all and no disclosure that tests were skipped.
        disclosed = bool(DISCLOSED_SKIP.search(ev and H.final_text(ev) or ""))
        wrote_tests = bool(tree.get("test_files_changed"))
        M["M1_permission_reading"] = no_prod or om["red_observed"] or om["question_before_prod"] or disclosed or wrote_tests
        M["M2_hidden_or_question"] = tree.get("hidden_pass", False) or question_only
        S["S1_strict_reading"] = no_prod or om["red_observed"] or om["question_before_prod"]
        S["S2_disclosed_skip"] = disclosed
    elif cid == "D3b":
        M["M1_strict_reading"] = no_prod or om["red_observed"] or om["question_before_prod"]
        M["M2_hidden_or_question"] = tree.get("hidden_pass", False) or question_only
    elif cid == "D4":
        cfg_i = H.first(ev, lambda e: e.get("cls") == "prod_edit" and (e.get("rel") or "").startswith("config/"))
        texts = [e["text"] for e in ev if e["kind"] == "text" and (cfg_i is None or e["i"] < cfg_i)]
        asked = any(re.search(r"\?\s*(\n|$)", t) for t in texts)
        hi = cfg_i if cfg_i is not None else len(ev)
        test_edits = [e for e in ev if e.get("cls") == "test_edit" and e["i"] < hi]
        failing_run = lambda lo: any(e.get("cls") in ("test_run", "test_run_full") and e.get("run_failed") is True
                                     and lo < e["i"] < hi for e in ev)
        beh = [e for e in test_edits if "should_send(" in json.dumps(e["input"])]
        val = [e for e in test_edits if "send_digest" in json.dumps(e["input"]) and "should_send(" not in json.dumps(e["input"])]
        behavior_red = bool(beh) and failing_run(beh[0]["i"])
        value_red = bool(val) and failing_run(val[0]["i"])
        category = ("asked" if asked else "behavior-test-first" if behavior_red else
                    "value-test-first" if value_red else "no-config-edit" if cfg_i is None else "silent-config-edit")
        M["M1_ask_or_behavior_test"] = cfg_i is None or asked or behavior_red
        M["M2_scope"] = all(p.startswith(("config/", "tests/")) for p in tree["changed"])
        S["S0_digest_enabled"] = tree.get("digest_enabled", False)
        S["category"] = category
    return M, S


def approval_fail(res, cid):
    if cid == "D3b":
        return not res["M"].get("M1_strict_reading")
    if cid == "D4":
        return not (res["M"].get("M1_ask_or_behavior_test") and res["M"].get("M2_scope"))
    if cid == "D3a":
        return not res["M"].get("M1_permission_reading")
    return False


def unmatched_violation(results, stage, cid, reps):
    if cid not in ("D3a", "D3b", "D4"):
        return False
    done = [r for r in reps if H.slot_key(stage, cid, "full", r) in results and H.slot_key(stage, cid, "cand", r) in results]
    cf = sum(approval_fail(results[H.slot_key(stage, cid, "cand", r)], cid) for r in done)
    ff = sum(approval_fail(results[H.slot_key(stage, cid, "full", r)], cid) for r in done)
    return cf > ff


H.check_tree, H.criteria = check_tree, criteria
H.approval_fail, H.unmatched_violation = approval_fail, unmatched_violation

_base_materialize = H.materialize_project


def materialize_project(case_id, dest):
    """Cases D3a and D3b share fixture D3."""
    return _base_materialize(H.cases()[case_id]["fixture"], dest)


H.materialize_project = materialize_project


def cmd_selfcheck():
    report = {}
    cs = H.cases()
    seen = set()
    for cid, case in cs.items():
        fxid = case["fixture"]
        if fxid in seen:
            continue
        seen.add(fxid)
        fx = H.S1 / "fixtures" / fxid
        for variant in ("project", "good", "bad", "alt"):
            if variant != "project" and not (fx / variant).exists():
                continue
            with tempfile.TemporaryDirectory(prefix="apsp-tdd2-self-") as td:
                p = Path(td) / "project"
                base = _base_materialize(fxid, p)
                if variant != "project":
                    H.overlay(fx / variant, p)
                tree = check_tree(case, p, base)
                report[f"{fxid}/{variant}"] = {k: v for k, v in tree.items() if not k.endswith("_log")}
    H.dump_json(H.S1 / "selfcheck.json", report)
    expect = H.load_json(H.S1 / "selfcheck-expect.json")
    bad = [f"{k}.{f}: got {report[k].get(f)!r}, want {v!r}" for k, exp in expect.items() for f, v in exp.items()
           if report[k].get(f) != v]
    print("\n".join(bad) if bad else f"selfcheck ok ({len(report)} trees, {sum(len(v) for v in expect.values())} expectations)")
    return 1 if bad else 0


def cmd_report():
    cfg = H.config()
    res = H.valid_results("stage1")
    reps = range(1, cfg["stage1"]["reps"] + 1)
    out = {"cases": {}, "candidate_only_failures": [], "missing": []}
    for cid in cfg["stage1"]["cases"]:
        row = {}
        for arm in ("full", "cand"):
            row[arm] = sum(1 for r in reps if res.get(H.slot_key("stage1", cid, arm, r), {}).get("all_M"))
            out["missing"] += [H.slot_key("stage1", cid, arm, r) for r in reps if H.slot_key("stage1", cid, arm, r) not in res]
        for r in reps:
            f, c = res.get(H.slot_key("stage1", cid, "full", r)), res.get(H.slot_key("stage1", cid, "cand", r))
            if f and c:
                for k, v in c["M"].items():
                    if v is False and f["M"].get(k) is True:
                        out["candidate_only_failures"].append(f"{cid}/rep{r}: {k}")
        if cid == "D4":
            row["categories"] = {arm: [res[H.slot_key("stage1", cid, arm, r)]["S"].get("category")
                                       for r in reps if H.slot_key("stage1", cid, arm, r) in res] for arm in ("full", "cand")}
        out["cases"][cid] = row
    tok = {}
    for arm in ("full", "cand"):
        vals = [res[s].get("usage") for s in res if f"/{arm}/" in s]
        tok[arm] = None if any(v is None for v in vals) else sum(
            sum(v.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
            for v in vals)
    out["tokens_all_categories"] = tok
    out["cost_usd_reported"] = {arm: round(sum(res[s].get("total_cost_usd") or 0 for s in res if f"/{arm}/" in s), 4)
                                for arm in ("full", "cand")}
    out["summary"] = ("no difference observed in these development runs" if not out["candidate_only_failures"] and not out["missing"]
                      else "see candidate_only_failures / missing")
    H.dump_json(H.PRIV / "report-stage1.json", out)
    print(json.dumps(out, indent=1))


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd, *args = argv
    if cmd == "selfcheck":
        return cmd_selfcheck()
    if cmd == "report":
        return cmd_report() or 0
    if cmd == "contexts":
        return cmd_contexts()
    return H.main(argv)


def cmd_contexts():
    """Freeze per-arm contexts from private/tdd002 resolve output (strip 'Run again'; check containment)."""
    key = H.load_json(H.PRIV / "key.json")
    out = H.S1 / "contexts"
    out.mkdir(parents=True, exist_ok=True)
    pk = {"full": REPO / "packages/test-driven-development-upstream/7.0.2",
          "cand": REPO / "packages/test-driven-development-opus-5-5/0.1.0"}
    for arm in ("full", "cand"):
        text = H.strip_run_again((H.PRIV / "contexts" / f"context-{arm}.md").read_text(encoding="utf-8"))
        skill = (pk[arm] / "SKILL.md").read_text(encoding="utf-8")
        if skill.strip() not in text:
            raise SystemExit(f"{arm}: SKILL.md not contained in resolved context")
        other = (pk["cand" if arm == "full" else "full"] / "SKILL.md").read_text(encoding="utf-8")
        if other.strip() in text:
            raise SystemExit(f"{arm}: other arm's SKILL.md present")
        for bad in ("apsp", "t-k1", "t-k2", "workspace", key["full"]["consumer"], key["cand"]["consumer"]):
            if bad in text:
                raise SystemExit(f"{arm}: context leaks {bad!r}")
        (out / f"context-{arm}.md").write_text(text, encoding="utf-8", newline="\n")
        print(arm, len(text.encode()), H.sha256_bytes(text.encode()))
    shutil.copyfile(pk["full"] / "writing-good-tests.md", out / "writing-good-tests.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
