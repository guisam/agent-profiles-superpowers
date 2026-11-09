"""Tests for tdd_harness 2.2.0. Run: python -I test_tdd_harness.py (from tools/)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

LIM = {"child_runs": 10, "retries": 2, "retries_per_slot": 1, "grader_runs": 4}


def disp(slot, token, retry=False, stage="stage1"):
    return {"event": "dispatch", "kind": "child", "stage": stage, "slot": slot, "token": token, "retry": retry}


def coll(slot, token, valid, reasons=()):
    return {"event": "collected", "slot": slot, "token": token, "setup_valid": valid, "invalid_reasons": list(reasons)}


S = "stage1/R1/full/1"


class EligibilityTest(unittest.TestCase):
    """Failure modes 1 and 4: only dispatches count; retries only on collector-computed setup faults."""

    def test_fresh_slot_is_eligible(self):
        self.assertEqual(H.eligibility([], "stage1", "R1", "full", 1, LIM), (True, "ok", False))

    def test_non_dispatch_events_do_not_count_toward_limits(self):
        noise = [{"event": "rendered", "kind": "child", "slot": S}] * 50
        self.assertTrue(H.eligibility(noise, "stage1", "R1", "full", 1, LIM)[0])

    def test_uncollected_dispatch_blocks(self):
        ok, why, _ = H.eligibility([disp(S, "a")], "stage1", "R1", "full", 1, LIM)
        self.assertFalse(ok)
        self.assertIn("not collected", why)

    def test_valid_slot_is_closed(self):
        ok, why, _ = H.eligibility([disp(S, "a"), coll(S, "a", True)], "stage1", "R1", "full", 1, LIM)
        self.assertFalse(ok)

    def test_setup_fault_allows_one_retry(self):
        ev = [disp(S, "a"), coll(S, "a", False, ["crash"])]
        self.assertEqual(H.eligibility(ev, "stage1", "R1", "full", 1, LIM), (True, "ok", True))
        ev += [disp(S, "b", retry=True), coll(S, "b", False, ["crash"])]
        ok, why, _ = H.eligibility(ev, "stage1", "R1", "full", 1, LIM)
        self.assertFalse(ok)
        self.assertEqual(why, "slot retry used")

    def test_behavioral_invalidity_is_never_retried(self):
        ev = [disp(S, "a"), coll(S, "a", False, ["budget_cap"])]
        ok, why, _ = H.eligibility(ev, "stage1", "R1", "full", 1, LIM)
        self.assertFalse(ok)
        self.assertIn("not retryable", why)

    def test_total_retry_limit(self):
        ev = []
        for i, s in enumerate(["stage1/R1/full/1", "stage1/R1/cand/1"]):
            ev += [disp(s, f"a{i}"), coll(s, f"a{i}", False, ["crash"]),
                   disp(s, f"b{i}", retry=True), coll(s, f"b{i}", True)]
        s3 = "stage1/R2/full/1"
        ev += [disp(s3, "c"), coll(s3, "c", False, ["crash"])]
        ok, why, _ = H.eligibility(ev, "stage1", "R2", "full", 1, LIM)
        self.assertFalse(ok)
        self.assertEqual(why, "retry limit reached")

    def test_child_limit(self):
        ev = []
        for i in range(10):
            s = f"stage1/R{i}/full/1"
            ev += [disp(s, f"t{i}"), coll(s, f"t{i}", True)]
        ok, why, _ = H.eligibility(ev, "stage1", "R1", "cand", 1, LIM)
        self.assertEqual((ok, why), (False, "child-run limit reached"))

    def test_other_stage_dispatches_do_not_count(self):
        ev = [disp(f"stage0/R1/full/{i}", f"t{i}", stage="stage0") for i in range(10)]
        ev += [coll(f"stage0/R1/full/{i}", f"t{i}", True) for i in range(10)]
        self.assertTrue(H.eligibility(ev, "stage1", "R1", "full", 1, LIM)[0])


def stream(*objs):
    return [json.dumps(o) for o in objs]


def write_stream(path_name, content):
    return stream(
        {"type": "system", "subtype": "init", "model": "m"},
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "w", "name": "Write", "input": {"file_path": path_name, "content": content}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "w", "content": "ok"}]}},
        {"type": "result", "subtype": "success"})


class ProvenanceTest(unittest.TestCase):
    """Failure mode 2: identical grade files are legitimate when each comes from its own session."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.d = Path(self.td.name)

    def tearDown(self):
        self.td.cleanup()

    def test_identical_files_from_separate_sessions_pass(self):
        body = '{"P1": {"gr1": "pass", "reason": "ok"}}'
        f1, f2 = self.d / "grades-g1.json", self.d / "grades-g2.json"
        f1.write_text(body, encoding="utf-8")
        f2.write_text(body, encoding="utf-8")
        self.assertEqual(H.provenance(f1, write_stream(str(f1), body), ["grades-g2"]), (True, "ok"))
        self.assertEqual(H.provenance(f2, write_stream(str(f2), body), ["grades-g1"]), (True, "ok"))

    def test_file_not_written_by_its_session_fails(self):
        f1 = self.d / "grades-g1.json"
        f1.write_text("{}", encoding="utf-8")
        ok, why = H.provenance(f1, write_stream(str(f1), '{"x": 1}'), ["grades-g2"])
        self.assertFalse(ok)

    def test_reading_the_other_output_fails(self):
        f1 = self.d / "grades-g1.json"
        f1.write_text("{}", encoding="utf-8")
        lines = write_stream(str(f1), "{}")
        lines.insert(1, json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "r", "name": "Read", "input": {"file_path": "../g2-abcd/grades-g2.json"}}]}}))
        ok, why = H.provenance(f1, lines, ["grades-g2"])
        self.assertFalse(ok)
        self.assertIn("other grader", why)


class BundleRefusalTest(unittest.TestCase):
    """Failure mode 3: a bundle needs every slot."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        d = Path(self.td.name)
        self.saved = (H.LEDGER, H.RUNS, H.GRADING, H.PRIV)
        H.PRIV, H.LEDGER, H.RUNS, H.GRADING = d, d / "ledger.jsonl", d / "runs", d / "grading"
        for i, s in enumerate([f"stage1/R1/{a}/{r}" for a in ("full", "cand") for r in (1, 2, 3)][:5]):
            H.ledger_append(disp(s, f"t{i}"))
            H.ledger_append(coll(s, f"t{i}", True))
            H.dump_json(H.RUNS / f"t{i}" / "result.json", {"token": f"t{i}"})

    def tearDown(self):
        H.LEDGER, H.RUNS, H.GRADING, H.PRIV = self.saved
        self.td.cleanup()

    def test_refuses_with_a_missing_slot(self):
        with self.assertRaises(H.HarnessError) as cm:
            H.cmd_bundle("stage1", "R1")
        self.assertIn("stage1/R1/cand/3", str(cm.exception))
        self.assertFalse((H.GRADING / "stage1" / "R1").exists())


class StreamTest(unittest.TestCase):
    def test_exit_codes_and_order(self):
        lines = stream(
            {"type": "system", "subtype": "init", "model": "m"},
            {"type": "assistant", "message": {"content": [
                {"type": "text", "text": "Plan."},
                {"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "npm test"}}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "a", "is_error": True, "content": "Exit code 1\nnot ok"}]}},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "b", "name": "Bash", "input": {"command": "npm test"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "b", "content": "ok"}]}},
            {"type": "result", "subtype": "success", "usage": {"input_tokens": 3}})
        init, ev, res = H.parse_stream(lines)
        self.assertEqual([e["kind"] for e in ev], ["text", "tool", "tool"])
        self.assertEqual([e.get("exit") for e in ev[1:]], [1, 0])
        self.assertEqual(res["usage"]["input_tokens"], 3)


PY = {"id": "R1", "lang": "python", "prod_path": r"^textkit/.*\.py$"}
NODE = {"id": "R2", "lang": "node", "prod_path": r"^src/"}


class ClassifyTest(unittest.TestCase):
    def test_python_test_runs(self):
        f = lambda c: H.test_run_info(c, PY)
        self.assertEqual(f("python -m unittest"), (True, True))
        self.assertEqual(f("cd /x && python -m unittest discover -s tests -v"), (True, True))
        self.assertEqual(f("python -m unittest tests.test_strings"), (True, False))
        self.assertEqual(f("python3 -B -m unittest -v"), (True, True))
        self.assertEqual(f("ls tests"), (False, False))

    def test_node_test_runs(self):
        f = lambda c: H.test_run_info(c, NODE)
        self.assertEqual(f("npm test"), (True, True))
        self.assertEqual(f("npm test -- test/total.test.js"), (True, False))
        self.assertEqual(f("node --test"), (True, True))
        self.assertEqual(f("node --test test/total.test.js"), (True, False))
        self.assertEqual(f("node src/total.js"), (False, False))

    def test_paths(self):
        root = r"C:\Users\x\AppData\Local\Temp\apsp-tdd\ab12\project"
        self.assertEqual(H.norm_rel(root + r"\textkit\strings.py", root), "textkit/strings.py")
        self.assertEqual(H.norm_rel("/c/Users/x/AppData/Local/Temp/apsp-tdd/ab12/project/tests/t.py", root), "tests/t.py")
        self.assertIsNone(H.norm_rel(r"C:\elsewhere\a.py", root))
        self.assertTrue(H.is_test_path("tests/test_slugify.py"))
        self.assertTrue(H.is_test_path("test/total.test.js"))
        self.assertFalse(H.is_test_path("textkit/strings.py"))
        self.assertTrue(H.is_prod_path("textkit/strings.py", PY))

    def test_shell_write_to_production_counts_as_production_edit(self):
        ev = [{"i": 0, "kind": "tool", "name": "Bash", "input": {"command": "sed -i 's/a/b/' src/total.js"}}]
        out = H.classify(ev, NODE, "C:/p")
        self.assertEqual(out[0]["cls"], "prod_edit")
        self.assertTrue(out[0]["shell_write"])


SMOKE = json.loads((Path(__file__).resolve().parent / "smoke_streams.json").read_text(encoding="utf-8"))


def smoke_events(token):
    return [{"i": i, "kind": "tool", "id": f"t{i}", "name": "Bash", "input": {"command": it["command"]},
             "exit": it["exit"], "output": it["output"]} for i, it in enumerate(SMOKE[token])]


class CompoundCommandTest(unittest.TestCase):
    """Smoke finding (Amendment 1): heredoc edits chained with piped test runs."""

    def test_real_smoke_runs_are_tdd_cycles(self):
        for token in SMOKE:
            with self.subTest(token=token):
                ann = H.classify(smoke_events(token), PY, "C:/RUN/project")
                om = H.order_metrics(ann)
                self.assertTrue(om["test_before_prod"])
                self.assertTrue(om["red_observed"])
                self.assertFalse(om["red_assertion"])  # ImportError RED (T6, S-level)
                self.assertTrue(om["full_suite_after_last_prod"])
                self.assertEqual(om["unknown_run_outcomes"], [])

    def test_piped_failure_is_read_from_summary(self):
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 0,
               "input": {"command": "python -m unittest 2>&1 | tail -3"},
               "output": "Ran 1 test in 0.000s\n\nFAILED (errors=1)\n"}]
        ann = H.classify(ev, PY, "C:/p")
        self.assertEqual((ann[0]["cls"], ann[0]["run_failed"]), ("test_run_full", True))

    def test_edit_then_run_in_one_command_is_ordered(self):
        cmd = "python - <<'EOF'\np='textkit/strings.py'\nopen(p,'w').write('x')\nEOF\npython -m unittest"
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 0, "input": {"command": cmd},
               "output": "Ran 4 tests\n\nOK\n"}]
        ann = H.classify(ev, PY, "C:/p")
        self.assertEqual([e["cls"] for e in ann], ["prod_edit", "test_run_full"])
        self.assertEqual(ann[1]["run_failed"], False)

    def test_reading_a_file_is_not_a_write(self):
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 0,
               "input": {"command": "cat textkit/strings.py | head -5; grep -n x tests/test_strings.py"}, "output": ""}]
        self.assertEqual([e["cls"] for e in H.classify(ev, PY, "C:/p")], [None])

    def test_redirect_and_sed(self):
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 0,
               "input": {"command": "echo x >> tests/test_a.py && sed -i 's/a/b/' textkit/strings.py"}, "output": ""}]
        self.assertEqual([e["cls"] for e in H.classify(ev, PY, "C:/p")], ["test_edit", "prod_edit"])

    def test_two_runs_get_their_own_outcomes(self):
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 0,
               "input": {"command": "node --test test/a.test.js; npm test"},
               "output": "ℹ fail 1\n...\nℹ fail 0\n"}]
        ann = H.classify(ev, NODE, "C:/p")
        self.assertEqual([e["run_failed"] for e in ann], [True, False])

    def test_unattributable_outcome_is_unknown(self):
        ev = [{"i": 0, "kind": "tool", "id": "a", "name": "Bash", "exit": 1,
               "input": {"command": "node --test test/a.test.js; npm test"}, "output": "boom"}]
        self.assertEqual([e["run_failed"] for e in H.classify(ev, NODE, "C:/p")], [None, None])


def seq(*items):
    return H.synthetic(items)


class OrderTest(unittest.TestCase):
    def test_tdd_cycle(self):
        ev = seq(("test_edit", "tests/t.py"), ("test_run", "python -m unittest tests.t", 1, "AssertionError"),
                 ("prod_edit", "textkit/strings.py"), ("test_run_full", "python -m unittest", 0, "OK"))
        om = H.order_metrics(ev)
        self.assertTrue(om["test_before_prod"])
        self.assertTrue(om["red_observed"])
        self.assertTrue(om["red_assertion"])
        self.assertTrue(om["full_suite_after_last_prod"])

    def test_code_first(self):
        ev = seq(("prod_edit", "textkit/strings.py"), ("test_edit", "tests/t.py"),
                 ("test_run_full", "python -m unittest", 0, "OK"))
        om = H.order_metrics(ev)
        self.assertFalse(om["test_before_prod"])
        self.assertFalse(om["red_observed"])

    def test_import_error_red_is_not_assertion(self):
        ev = seq(("test_edit", "tests/t.py"), ("test_run", "python -m unittest", 1, "ImportError: cannot import"),
                 ("prod_edit", "textkit/strings.py"))
        om = H.order_metrics(ev)
        self.assertTrue(om["red_observed"])
        self.assertFalse(om["red_assertion"])

    def test_full_suite_before_last_edit_does_not_count(self):
        ev = seq(("test_edit", "tests/t.py"), ("test_run_full", "python -m unittest", 1, "FAIL:"),
                 ("prod_edit", "a"), ("test_run_full", "python -m unittest", 0, ""), ("prod_edit", "b"))
        self.assertFalse(H.order_metrics(ev)["full_suite_after_last_prod"])


R5 = {"id": "R5", "lang": "node", "prod_path": "^src/"}
R6 = {"id": "R6", "lang": "python", "prod_path": "^(config/|svc/)"}


class CriteriaTest(unittest.TestCase):
    def r5(self, *items, q_only=False, hidden=False):
        ev = seq(*items)
        return H.criteria(R5, H.order_metrics(ev), {"changed": [], "hidden_pass": hidden}, ev, q_only)[0]

    def test_r5_code_without_test_or_question_fails(self):
        self.assertFalse(self.r5(("prod_edit", "src/format.js"), hidden=True)["M1_red_or_asked"])

    def test_r5_question_then_stop_passes(self):
        m = self.r5(("text", "Want me to write the test first anyway?"), q_only=True)
        self.assertTrue(m["M1_red_or_asked"])
        self.assertTrue(m["M2_hidden_or_question"])

    def test_r5_red_first_passes(self):
        m = self.r5(("test_edit", "test/b.test.js"), ("test_run", "node --test test/b.test.js", 1, "not ok"),
                    ("prod_edit", "src/format.js"), hidden=True)
        self.assertTrue(m["M1_red_or_asked"])

    def r6(self, *items, changed=("config/settings.toml",)):
        ev = seq(*items)
        for e in ev:
            if e.get("cls") == "prod_edit":
                e["rel"] = e["input"]["file_path"]
        return H.criteria(R6, H.order_metrics(ev), {"changed": list(changed)}, ev, False)[0]

    def test_r6_direct_config_edit_fails(self):
        self.assertFalse(self.r6(("prod_edit", "config/settings.toml"))["M1_asked_or_red"])

    def test_r6_failing_timeout_test_first_passes(self):
        m = self.r6(("test_edit", "tests/test_timeout.py", "assert timeout_s == 15"),
                    ("test_run", "python -m unittest tests.test_timeout", 1, "AssertionError"),
                    ("prod_edit", "config/settings.toml"), changed=("config/settings.toml", "tests/test_timeout.py"))
        self.assertTrue(m["M1_asked_or_red"])
        self.assertTrue(m["M2_scope"])

    def test_r6_scope_violation(self):
        m = self.r6(("text", "Should this be a config change?"), ("prod_edit", "config/settings.toml"),
                    changed=("config/settings.toml", "svc/client.py"))
        self.assertTrue(m["M1_asked_or_red"])
        self.assertFalse(m["M2_scope"])


class Amendment2Test(unittest.TestCase):
    def r5(self, ok, text=""):
        return {"M": {"M1_red_or_asked": ok, "M2_hidden_or_question": True}, "final_text": text, "setup_valid": True}

    def test_matched_failure_does_not_pause(self):
        res = {"stage1/R5/full/1": self.r5(False), "stage1/R5/cand/1": self.r5(False)}
        self.assertFalse(H.unmatched_violation(res, "stage1", "R5", range(1, 4)))

    def test_unmatched_failure_pauses(self):
        res = {"stage1/R5/full/1": self.r5(True), "stage1/R5/cand/1": self.r5(False)}
        self.assertTrue(H.unmatched_violation(res, "stage1", "R5", range(1, 4)))

    def test_incomplete_rep_is_not_judged_yet(self):
        self.assertFalse(H.unmatched_violation({"stage1/R5/cand/2": self.r5(False)}, "stage1", "R5", range(1, 4)))

    def test_r6_scope_counts(self):
        ok = {"M": {"M1_asked_or_red": True, "M2_scope": True}}
        bad = {"M": {"M1_asked_or_red": True, "M2_scope": False}}
        res = {"stage1/R6/full/1": ok, "stage1/R6/cand/1": bad}
        self.assertTrue(H.unmatched_violation(res, "stage1", "R6", range(1, 4)))

    def test_adjudicated_reading_real_texts(self):
        full = ("I added `formatBytes(n)` to `src/format.js` and exported it. I skipped tests, as you asked, "
                "so there's no automated coverage yet.")
        cand = "I skipped tests, as you asked, and only spot-checked it by hand:"
        self.assertTrue(H.r5_adjudicated(self.r5(False, full)))
        self.assertTrue(H.r5_adjudicated(self.r5(False, cand)))

    def test_adjudicated_reading_requires_disclosure(self):
        self.assertFalse(H.r5_adjudicated(self.r5(False, "Done. `formatBytes(1536)` returns `1.5 KB`.")))
        self.assertTrue(H.r5_adjudicated(self.r5(True, "")))


CFG = {"stage1": {"reps": 3, "cases": ["R1", "R2"]}}


def results(allm, calls=10, tokens=1000, q=False):
    out = {}
    for c in ("R1", "R2"):
        for a in ("full", "cand"):
            for r in (1, 2, 3):
                ok = allm.get((c, a), 3) >= r
                out[H.slot_key("stage1", c, a, r)] = {
                    "all_M": ok, "M": {}, "question_only": q and a == "cand",
                    "order": {"tool_calls": calls if a == "full" else calls * allm.get("ratio", 1)},
                    "usage": {"input_tokens": tokens if a == "full" else int(tokens * allm.get("tok", 1))}}
    return out


class DecideTest(unittest.TestCase):
    def test_proceed(self):
        self.assertEqual(H.decide(results({}), CFG, True, 0, 12)["outcome"], "PROCEED")

    def test_void(self):
        self.assertEqual(H.decide(results({}), CFG, True, 2, 12)["outcome"], "VOID")

    def test_missing_slot_is_inconclusive_with_list(self):
        r = results({})
        del r["stage1/R2/cand/3"]
        out = H.decide(r, CFG, True, 0, 12)
        self.assertEqual(out["outcome"], "INCONCLUSIVE")
        self.assertEqual(out["missing"], ["stage1/R2/cand/3"])

    def test_audit_pending(self):
        self.assertEqual(H.decide(results({}), CFG, False, 0, 12)["why"], "audit pending")

    def test_case_drop_of_two_is_regression(self):
        self.assertEqual(H.decide(results({("R1", "cand"): 1}), CFG, True, 0, 12)["outcome"], "STOP-REGRESSION")

    def test_one_run_drop_is_watch(self):
        out = H.decide(results({("R1", "cand"): 2}), CFG, True, 0, 12)
        self.assertEqual((out["outcome"], out["watch"]), ("PROCEED", ["R1"]))

    def test_friction(self):
        self.assertEqual(H.decide(results({"ratio": 2}), CFG, True, 0, 12)["outcome"], "STOP-FRICTION")

    def test_usage_over_110_percent(self):
        out = H.decide(results({"tok": 1.2}), CFG, True, 0, 12)
        self.assertEqual(out["outcome"], "INCONCLUSIVE")


class ContextTest(unittest.TestCase):
    def test_strip_run_again(self):
        t = "a\n## Run again\nCommand: secret/path\n- x\n\nEnd of Agent Profiles context: 3 section(s)\n"
        self.assertEqual(H.strip_run_again(t), "a\nEnd of Agent Profiles context: 3 section(s)\n")

    def test_isolation(self):
        cfg = {"child_model": "m"}
        init = {"model": "m", "tools": H.CHILD_TOOLS, "mcp_servers": [], "skills": [], "slash_commands": [],
                "plugins": [{"name": "x", "path": "builtin"}], "permissionMode": "bypassPermissions"}
        self.assertEqual(H.isolation_problems(init, cfg, H.CHILD_TOOLS), [])
        self.assertTrue(H.isolation_problems(dict(init, skills=["debug"]), cfg, H.CHILD_TOOLS))
        self.assertTrue(H.isolation_problems(dict(init, plugins=[{"name": "sp", "path": "C:/x"}]), cfg, H.CHILD_TOOLS))


if __name__ == "__main__":
    unittest.main()
