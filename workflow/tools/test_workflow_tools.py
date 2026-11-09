"""Tests for the workflow tools (stdlib only; no model calls, no AP calls).
Run: python -I test_workflow_tools.py   (from workflow/tools/)"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import campaign  # noqa: E402
import check_package  # noqa: E402
import preflight  # noqa: E402
import results_format  # noqa: E402

REPO = HERE.parents[1]


def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class CheckPackageTest(unittest.TestCase):
    def pkg(self, d, link="ref.md"):
        write(d / "package.yaml", 'schema_version: 1\npackage:\n  name: "@x/s"\n  version: "1.0.0"\n'
                                  "  type: skill\n  license: MIT\nentrypoint: SKILL.md\n")
        write(d / "LICENSE", "MIT")
        write(d / "SKILL.md", f"---\nname: s\n---\nRead [the ref]({link}). See superpowers:other-skill.\n")
        write(d / "ref.md", "ref")

    def test_real_tdd_packages_close(self):
        for p in ("packages/test-driven-development-upstream/7.0.2", "packages/test-driven-development-sonnet-5-5/0.1.0"):
            r = check_package.check(REPO / p)
            self.assertEqual(r["errors"], [])
            self.assertEqual(r["cross_skill_references"], ["writing-skills"])

    def test_candidate_changes_only_skill_and_manifest(self):
        r = check_package.check(REPO / "packages/test-driven-development-sonnet-5-5/0.1.0",
                                REPO / "packages/test-driven-development-upstream/7.0.2")
        self.assertEqual(r["compare"]["changed"], ["SKILL.md", "package.yaml"])
        self.assertEqual(r["compare"]["only_here"] + r["compare"]["only_there"], [])

    def test_broken_link_is_an_error(self):
        with tempfile.TemporaryDirectory() as t:
            self.pkg(Path(t), link="missing.md")
            r = check_package.check(t)
            self.assertTrue(any("broken link" in e for e in r["errors"]))
            self.assertEqual(r["cross_skill_references"], ["other-skill"])

    def test_good_package_passes(self):
        with tempfile.TemporaryDirectory() as t:
            self.pkg(Path(t))
            self.assertEqual(check_package.check(t)["errors"], [])


class PreflightTest(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        d = Path(self.t.name)
        self.cfg, self.run = d / "claude", d / "runs" / "r1" / "project"
        self.run.mkdir(parents=True)
        self.arm, self.other = d / "arm" / "SKILL.md", d / "other" / "SKILL.md"
        write(self.arm, "---\nname: tdd\n---\nARM TEXT unique alpha\n")
        write(self.other, "---\nname: tdd\n---\nOTHER TEXT unique beta\n")
        write(self.run.parent / "context.md", "header\n" + self.arm.read_text(encoding="utf-8"))
        self.env = mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.cfg)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.t.cleanup()

    def args(self, *extra):
        return preflight.argparse.Namespace(
            run_dir=str(self.run), context=str(self.run.parent / "context.md"), arm_skill=str(self.arm),
            other_skill=str(self.other), skill_name="tdd", forbid=None, claude_flag=list(extra),
            probe=False, init_json=None, model=None, tools="Bash", expect_tools=None, deny=None, out=None)

    def run_static(self, *extra):
        a = self.args(*extra)
        return preflight.static_checks(a, self.arm.read_text(encoding="utf-8"), self.other.read_text(encoding="utf-8"))

    def test_clean(self):
        c = self.run_static()
        for k in ("arm", "dupes", "env"):
            self.assertTrue(c[k]["ok"], k)
        # Ancestor settings outside the temp tree (e.g. a real ~/.claude reached by walking up from a temp
        # directory under the home folder) are reported on purpose; nothing inside the temp tree is.
        inside = [f for f in c["hooks"]["files_with_hooks"] + c["global"]["files"] if self.t.name in f]
        self.assertEqual(inside, [])

    def test_duplicate_install_by_name_and_hooks_and_global(self):
        write(self.cfg / "plugins" / "cache" / "sp" / "skills" / "tdd" / "SKILL.md", "---\nname: tdd\n---\nanything\n")
        write(self.cfg / "settings.json", json.dumps({"hooks": {"SessionStart": []}}))
        write(self.cfg / "CLAUDE.md", "global rules")
        c = self.run_static()
        self.assertFalse(c["dupes"]["ok"])
        self.assertFalse(c["hooks"]["ok"])
        self.assertFalse(c["global"]["ok"])
        c2 = self.run_static("--safe-mode")
        self.assertTrue(c2["dupes"]["neutralized_by_flags"])

    def test_other_arm_content_in_run_dir(self):
        write(self.run / "notes" / "copy.md", self.other.read_text(encoding="utf-8"))
        c = self.run_static()
        self.assertFalse(c["arm"]["ok"])
        self.assertEqual(len(c["arm"]["other_arm_files_in_run_dir"]), 1)

    def test_context_with_other_arm_fails(self):
        write(self.run.parent / "context.md", self.other.read_text(encoding="utf-8"))
        c = self.run_static()
        self.assertFalse(c["arm"]["context_contains_arm_skill"])
        self.assertFalse(c["arm"]["context_free_of_other_arm"])

    def test_forbidden_root(self):
        a = self.args()
        a.forbid = [str(Path(self.t.name) / "runs")]
        c = preflight.static_checks(a, self.arm.read_text(encoding="utf-8"), self.other.read_text(encoding="utf-8"))
        self.assertFalse(c["arm"]["ok"])

    def test_init_evaluation(self):
        a = self.args()
        a.model, a.tools = "m", "Bash,Read"
        good = {"model": "m", "tools": ["Read", "Bash"], "mcp_servers": [], "skills": [], "slash_commands": [],
                "plugins": [{"name": "b", "path": "builtin"}]}
        self.assertTrue(preflight.evaluate_init(good, [good], a)["ok"])
        bad = dict(good, skills=["debug"], plugins=[{"name": "ponytail", "path": "C:/x"}])
        r = preflight.evaluate_init(bad, [bad], a)
        self.assertFalse(r["ok"])
        self.assertEqual(len(r["problems"]), 3)  # skills, non-builtin plugin, deny-listed term


class ResultsFormatTest(unittest.TestCase):
    def doc(self):
        return json.loads((REPO / "experiments/tdd-compaction/stage1/results.sanitized.json").read_text(encoding="utf-8"))

    def test_stage1_export_is_valid(self):
        self.assertEqual(results_format.validate(self.doc()), [])

    def test_private_material_is_refused(self):
        for bad in ("C:/Users/someone/project", "deadbeef-1234-5678-9abc-def012345678", "me@example.com",
                    "sk-ant-abc", "x" * 700):
            d = self.doc()
            d["runs"][0]["termination"] = bad
            self.assertTrue(results_format.validate(d), bad)

    def test_package_versions_are_not_emails(self):
        d = self.doc()
        self.assertIn("@7.0.2", d["arms"]["full"]["package"])
        self.assertEqual(results_format.validate(d), [])

    def test_undeclared_arm_refused(self):
        d = self.doc()
        d["runs"][0]["arm"] = "other"
        self.assertTrue(results_format.validate(d))


class CampaignTest(unittest.TestCase):
    def c(self, **kw):
        c = json.loads((REPO / "workflow/examples/tdd-sonnet-5-5/campaign.example.json").read_text(encoding="utf-8"))
        c.update(kw)
        return c

    def test_example_checks(self):
        self.assertEqual(campaign.check(self.c()), [])

    def test_model_must_be_exact(self):
        c = self.c()
        c["configuration"]["model"] = "auto"
        self.assertTrue(campaign.check(c))

    def test_plan_is_deterministic_and_complete(self):
        p1, p2 = campaign.plan(self.c()), campaign.plan(self.c())
        self.assertEqual(p1, p2)
        self.assertEqual(len({s["slot"] for s in p1}), 42)

    def test_even_reps_are_balanced(self):
        p = campaign.plan(self.c(reps_per_arm=12))
        for case in self.c()["cases"]:
            firsts = [p[i]["arm"] for i in range(0, len(p), 2) if p[i]["case"] == case]
            self.assertEqual(firsts.count("full"), 6)
            self.assertEqual(firsts.count("cand"), 6)


if __name__ == "__main__":
    unittest.main()
