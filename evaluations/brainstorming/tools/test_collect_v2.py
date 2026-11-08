"""Tests for collect_v2 (harness 2.1). Run: python -E -s test_collect_v2.py (from tools/)."""
import copy, json, shutil, tempfile, unittest
from pathlib import Path
import collect_v2 as c

CRIT = {"must": ["M1: gate", "M2: b", "M3: c"], "should": ["S1: d"]}


def case(cid, fixture="fx", gate="design-gate", **kw):
    return {"id": cid, "stage": "screening", "fixture": fixture, "gate": gate,
            "conversation": [{"role": "user", "text": f"question for {cid}"}], **CRIT, **kw}


class Env(unittest.TestCase):
    """A throwaway suite, private dir and transcript dir; module globals point at them."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.saved = (c.PRIVATE, c.SUITE, c.TRANSCRIPTS)
        c.PRIVATE, c.SUITE, c.TRANSCRIPTS = self.tmp / "private", self.tmp / "suite", self.tmp / "tx"
        for p in (c.PRIVATE, c.SUITE / "fx", c.SUITE / "fy", c.TRANSCRIPTS / "s" / "subagents"):
            p.mkdir(parents=True)
        (c.SUITE / "fx" / "a.txt").write_text("x")
        (c.SUITE / "fy" / "b.txt").write_text("y")
        (c.SUITE / "RUBRIC.md").write_text("rubric")
        (c.SUITE / "GRADER-PROMPT.md").write_text("grade {bundle} using {fixture} into {out}")
        self.arms = {}
        for arm, body in (("full", "BODY FULL text"), ("seq", "BODY SEQ text")):
            pk = self.tmp / "pk" / arm
            pk.mkdir(parents=True)
            (pk / "SKILL.md").write_text(f"---\nname: x\n---\n{body}\n")
            self.arms[arm] = {"consumer": f"/c/{arm}", "package": str(pk)}
        self.write_cases([
            case("P1"), case("P2", continues="P1", scripted_user_turn="NEW FACT"),
            case("D1"), case("O1", fixture="fy"),
            case("N1", gate="none-requested-edit", expect_changed={"a.txt": "edited"})])
        self.write_cfg()

    def tearDown(self):
        c.PRIVATE, c.SUITE, c.TRANSCRIPTS = self.saved
        shutil.rmtree(self.tmp)

    def write_cases(self, cs):
        (c.SUITE / "cases.json").write_text(json.dumps({"cases": cs}))

    def write_cfg(self, **limits):
        conf = {"experiment": "t-exp", "arms": self.arms, "control": "full", "treatment": "seq",
                "store": "/store", "trust": "/trust.yaml",
                "limits": {"child_runs": 57, "retries": 5, "grader_runs": 20, **limits},
                "decision": {"primary": [["P1", "M3"], ["D1", "M3"]], "overcorrection": ["O1", "M2"],
                             "delegation": ["D1", "M2"], "ceiling": 5, "margin": 3, "void_failure_share": 0.10}}
        (c.SUITE / "run-config.json").write_text(json.dumps(conf))

    def run_child(self, cid, arm, rep, reply, parent=None, body=None, skill=False, edit=None):
        """prepare -> fake transcript (exact prompt, resolve output, final text) -> collect."""
        t = c.prepare(cid, arm, rep, parent)
        body = body or ("BODY FULL text" if arm == "full" else "BODY SEQ text")
        rows = [{"type": "user", "message": {"content": c.prompt(t)}},
                {"type": "assistant", "message": {"id": "m1", "model": "claude-sonnet-5-5",
                 "usage": {"input_tokens": 1, "cache_creation_input_tokens": 2, "cache_read_input_tokens": 3,
                           "output_tokens": 4, "output_tokens_details": {"thinking_tokens": 1}},
                 "content": [{"type": "tool_use", "id": "u1", "name": "Bash",
                              "input": {"command": "npx --no agent-profiles resolve"}}]
                 + ([{"type": "tool_use", "id": "u2", "name": "Skill", "input": {}}] if skill else [])}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "u1",
                 "content": f"{body}\nEnd of Agent Profiles context: 3"}]}},
                {"type": "assistant", "message": {"id": "m2", "model": "claude-sonnet-5-5",
                 "usage": {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 5,
                           "output_tokens": 6, "output_tokens_details": {"thinking_tokens": 0}},
                 "content": [{"type": "text", "text": reply}]}}]
        agent = "a" + t[1:]
        (c.TRANSCRIPTS / "s" / "subagents" / f"agent-{agent}.jsonl").write_text(
            "\n".join(json.dumps(r) for r in rows))
        if edit:
            (c.runs_dir() / t / "project" / edit[0]).write_text(edit[1])
        return t, c.collect(t, agent)


class Fixtures(Env):
    def test_per_case_fixture(self):
        t = c.prepare("O1", "full", 1)
        self.assertTrue((c.runs_dir() / t / "project" / "b.txt").exists())
        self.assertFalse((c.runs_dir() / t / "project" / "a.txt").exists())

    def test_tokens_are_opaque(self):
        t = c.prepare("P1", "seq", 2)
        p = c.prompt(t)
        for leak in ("P1", "seq", "full", "r2"):
            self.assertNotIn(leak + "/", p)
        self.assertNotIn(".seq.", p)


class Continuations(Env):
    def test_uses_own_arm_and_rep_reply(self):
        tf, _ = self.run_child("P1", "full", 1, "FULL-R1 reply")
        ts, _ = self.run_child("P1", "seq", 1, "SEQ-R1 reply")
        tf2, _ = self.run_child("P1", "full", 2, "FULL-R2 reply")
        cont = c.prepare("P2", "seq", 1, ts)
        p = c.prompt(cont)
        self.assertIn("SEQ-R1 reply", p)
        self.assertNotIn("FULL-R1 reply", p)
        self.assertNotIn("FULL-R2 reply", p)
        self.assertEqual([h["role"] for h in c.history(cont)], ["user", "assistant", "user"])
        self.assertEqual(c.history(cont)[2]["text"], "NEW FACT")
        self.assertEqual(c.planned(cont)["parent"], ts)

    def test_rejects_wrong_parent(self):
        tf, _ = self.run_child("P1", "full", 1, "r")
        with self.assertRaisesRegex(ValueError, "need P1/seq/r1"):
            c.prepare("P2", "seq", 1, tf)  # other arm
        with self.assertRaisesRegex(ValueError, "need P1/full/r2"):
            c.prepare("P2", "full", 2, tf)  # other repetition
        with self.assertRaisesRegex(ValueError, "give the parent"):
            c.prepare("P2", "full", 1)
        with self.assertRaisesRegex(ValueError, "not a continuation"):
            c.prepare("D1", "full", 1, tf)

    def test_rejects_invalid_parent(self):
        bad, res = self.run_child("P1", "full", 1, "r", body="WRONG BODY")
        self.assertFalse(res["setup_valid"])
        with self.assertRaisesRegex(ValueError, "not a valid run"):
            c.prepare("P2", "full", 1, bad)

    def test_bundle_shows_each_replys_history(self):
        for arm in ("full", "seq"):
            parent, _ = self.run_child("P1", arm, 0, f"PARENT-{arm}")
            self.run_child("P2", arm, 0, f"CHILD-{arm}", parent=parent)
        path, n = c.bundle("P2", "smoke", (0,))
        text = path.read_text()
        self.assertEqual(n, 2)
        for arm in ("full", "seq"):
            block = text[text.index(f"CHILD-{arm}") - 400:text.index(f"CHILD-{arm}")]
            self.assertIn(f"PARENT-{arm}", block)
        self.assertNotIn('"stage"', text)


class Gates(Env):
    def test_gated_case_flags_file_change(self):
        _, res = self.run_child("D1", "seq", 1, "r", edit=("a.txt", "changed"))
        self.assertEqual((res["gate_violation"], res["changed_files"]), (True, ["a.txt"]))

    def test_requested_edit_is_not_a_violation(self):
        _, ok = self.run_child("N1", "seq", 1, "done", edit=("a.txt", "edited"))
        self.assertEqual((ok["gate_violation"], ok["expected_edit_ok"]), (False, True))
        _, missing = self.run_child("N1", "seq", 2, "done")
        self.assertEqual((missing["gate_violation"], missing["expected_edit_ok"]), (False, False))

    def test_skill_tool_invalidates(self):
        t, res = self.run_child("D1", "full", 1, "r", skill=True)
        self.assertFalse(res["setup_valid"])
        self.assertFalse(c.valid(t))


class Limits(Env):
    def test_retry_only_after_collected_invalid(self):
        t1 = c.prepare("D1", "full", 1)
        with self.assertRaisesRegex(c.LimitError, "retry only once"):
            c.prepare("D1", "full", 1)  # not collected yet
        good, _ = self.run_child("D1", "seq", 1, "ok")
        with self.assertRaisesRegex(c.LimitError, "retry only once"):
            c.prepare("D1", "seq", 1)  # valid already
        bad, _ = self.run_child("O1", "full", 1, "r", body="WRONG")
        retry = c.prepare("O1", "full", 1)
        self.assertEqual(c.planned(retry)["retry_of"], bad)

    def test_retry_and_child_limits(self):
        self.write_cfg(retries=1, child_runs=2)
        bad, _ = self.run_child("D1", "full", 1, "r", body="WRONG")
        bad2, _ = self.run_child("D1", "full", 1, "r", body="WRONG")  # first retry allowed
        with self.assertRaisesRegex(c.LimitError, "child run limit"):
            c.prepare("O1", "full", 1)
        self.write_cfg(retries=1, child_runs=10)
        bad3, _ = self.run_child("O1", "full", 1, "r", body="WRONG")
        with self.assertRaisesRegex(c.LimitError, "retry limit"):
            c.prepare("O1", "full", 1)

    def test_grader_limit_and_rerun_only_if_invalid(self):
        self.write_cfg(grader_runs=2)
        t, _ = self.run_child("D1", "full", 0, "r")
        c.bundle("D1", "smoke", (0,))
        self.assertIn("grades-A.json", c.grader_prompt("smoke", "D1", "A"))
        out = c.grading_dir("smoke") / "D1.grades-A.json"
        out.write_text("{not json")  # invalid output: one re-run allowed, the bad file is kept
        c.grader_prompt("smoke", "D1", "A")
        self.assertEqual(len(list(c.grading_dir("smoke").glob("D1.grades-A.rejected-*.json"))), 1)
        out.write_text(json.dumps({"grader": "g", "grades": [
            {"reply": "R1", "case": "D1", "M1": "pass", "M2": "pass", "M3": "pass", "S1": "pass"}]}))
        with self.assertRaisesRegex(c.LimitError, "output is valid"):
            c.grader_prompt("smoke", "D1", "A")
        with self.assertRaisesRegex(c.LimitError, "grader limit"):
            c.grader_prompt("smoke", "D1", "B")


KEY = {"R1": "rAAA", "R2": "rBBB"}
CASE = {"id": "C99", **CRIT}
GOOD = {"grader": "g", "grades": [
    {"reply": "R1", "case": "C99", "M1": "pass", "M2": "fail", "M3": "pass", "S1": "unclear", "evidence": {"M2": "x"}},
    {"reply": "R2", "case": "C99", "M1": "pass", "M2": "pass", "M3": "pass", "S1": "pass", "design_items": 2}]}


def mutated(fn):
    g = copy.deepcopy(GOOD)
    fn(g)
    return g


class Scoring(unittest.TestCase):
    def rejects(self, grades, key=KEY, msg=""):
        with self.assertRaisesRegex(c.GradeError, msg):
            c.validate_grades(key, grades, CASE)

    def test_valid_and_metrics(self):
        rows = c.validate_grades(KEY, GOOD, CASE)
        self.assertEqual([r["run"] for r in rows], ["rAAA", "rBBB"])
        self.assertEqual(rows[1]["metrics"], {"design_items": 2})

    def test_rejections(self):
        self.rejects(GOOD, key={"R1": "rAAA", "R2": "rAAA"}, msg="same run")
        self.rejects(mutated(lambda g: g["grades"].append(dict(g["grades"][0]))), msg="duplicate")
        self.rejects(mutated(lambda g: g["grades"].pop()), msg="no grades for")
        self.rejects(mutated(lambda g: g["grades"][1].pop("S1")), msg="missing criteria")
        self.rejects(mutated(lambda g: g["grades"][0].update(M4="pass")), msg="unexpected")
        self.rejects(mutated(lambda g: g["grades"][0].update(M1="yes")), msg="invalid grade")
        self.rejects(mutated(lambda g: g["grades"][0].update(reply="R9")), msg="unknown reply")
        self.rejects(mutated(lambda g: g["grades"][0].update(case="C01")), msg="is not")

    def test_two_graders_disagreement_fails(self):
        b = mutated(lambda g: g["grades"][1].update(M3="fail", grader="h"))
        rows = c.combine(c.validate_grades(KEY, GOOD, CASE), c.validate_grades(KEY, b, CASE), CASE)
        r2 = [r for r in rows if r["run"] == "rBBB"][0]
        self.assertEqual((r2["M3"], r2["disagree"]), ("fail", ["M3"]))
        r1 = [r for r in rows if r["run"] == "rAAA"][0]
        self.assertEqual((r1["M1"], r1["M2"], r1["S1"]), ("pass", "fail", "fail"))


class Usage(unittest.TestCase):
    def test_missing_fields_stay_unknown(self):
        t = c.usage_totals([{"input_tokens": 1, "output_tokens": 5, "output_tokens_details": {"thinking_tokens": 2}},
                            {"input_tokens": 2, "output_tokens": 7}])
        self.assertEqual((t["input_tokens"], t["output_tokens"]), (3, 12))
        self.assertIsNone(t["cache_read_input_tokens"])
        self.assertIsNone(t["thinking_tokens_within_output"])
        self.assertIsNone(c.usage_totals([]))


class Decision(Env):
    """Fabricate a complete stage-1 grid, then vary it."""

    def grid(self, primary_pass, skip=None, breach=False, oc=None, delegation_fail=None):
        rows = []
        for cid in ("P1", "D1", "O1", "N1"):
            for arm in ("full", "seq"):
                for rep in c.REPS:
                    if skip == (cid, arm, rep):
                        continue
                    edit = ("a.txt", "edited") if cid == "N1" else None
                    t, _ = self.run_child(cid, arm, rep, "reply", edit=edit)
                    g = {k: "pass" for k in ("M1", "M2", "M3", "S1")}
                    if cid in ("P1", "D1"):
                        g["M3"] = "pass" if rep <= primary_pass[arm][cid] else "fail"
                    if breach and arm == "seq" and cid == "D1" and rep == 1:
                        g["M1"] = "fail"
                    if oc and cid == "O1" and rep <= oc.get(arm, 0):
                        g["M2"] = "fail"
                    if delegation_fail and cid == "D1" and rep <= delegation_fail.get(arm, 0):
                        g["M2"] = "fail"
                    rows.append({"run": t, "case": cid, **g, "disagree": []})
        (c.grading_dir("s1")).mkdir(parents=True, exist_ok=True)
        (c.grading_dir("s1") / "scores.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
        # P2 (continuation) is not a screening case here
        cs = json.loads((c.SUITE / "cases.json").read_text())["cases"]
        for x in cs:
            if x["id"] == "P2":
                x["stage"] = "validation"
        self.write_cases(cs)
        return c.decide("s1")

    def test_proceed(self):
        d = self.grid({"full": {"P1": 0, "D1": 1}, "seq": {"P1": 2, "D1": 2}})  # F=1, Q=4
        self.assertEqual((d["outcome"], d["F"], d["Q"]), ("PROCEED", 1, 4))

    def test_incomplete_pairs_never_decide(self):
        d = self.grid({"full": {"P1": 0, "D1": 0}, "seq": {"P1": 3, "D1": 3}}, skip=("O1", "seq", 2))
        self.assertEqual(d["outcome"], "INCONCLUSIVE")
        self.assertEqual(d["missing_pairs"], ["O1/seq/r2"])

    def test_breach_pauses_without_attribution(self):
        d = self.grid({"full": {"P1": 0, "D1": 0}, "seq": {"P1": 3, "D1": 3}}, breach=True)
        self.assertEqual(d["outcome"], "PAUSED")
        self.assertEqual(len(d["treatment_gate_breaches"]), 1)

    def test_ceiling(self):
        self.assertEqual(self.grid({"full": {"P1": 3, "D1": 2}, "seq": {"P1": 3, "D1": 3}})["outcome"], "STOP-NO-ROOM")

    def test_negative(self):
        self.assertEqual(self.grid({"full": {"P1": 1, "D1": 1}, "seq": {"P1": 1, "D1": 1}})["outcome"], "STOP-NEGATIVE")

    def test_overcorrection_blocks(self):
        d = self.grid({"full": {"P1": 0, "D1": 0}, "seq": {"P1": 3, "D1": 3}}, oc={"seq": 1})
        self.assertEqual(d["outcome"], "INCONCLUSIVE")
        self.assertEqual(d["watch_items"], ["O1"])

    def test_delegation_confirmation_blocks(self):
        d = self.grid({"full": {"P1": 0, "D1": 0}, "seq": {"P1": 3, "D1": 3}}, delegation_fail={"seq": 2})
        self.assertNotEqual(d["outcome"], "PROCEED")


if __name__ == "__main__":
    unittest.main()
