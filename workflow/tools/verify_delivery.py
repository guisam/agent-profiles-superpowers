"""Verify AP selection and plugin-free delivery for a model-specific variant. No model calls.

Uses only released AP commands (default: `npx --yes @guisam/agent-profiles@0.19.4`; override
with AP_CMD, e.g. AP_CMD="node /path/to/node_modules/@guisam/agent-profiles/bin/agent-profiles.js").
Everything happens in a fresh temporary directory: throwaway store, disposable consumer, a
trial-scoped trust policy. The home store, home trust policy and ~/.claude are never touched.

Checks, against an identities file (IDENTITIES.json):
  1. package bytes on disk equal the pinned sha256 values; AP `add` digests equal the pins;
  2. routing: each listed model resolves to the expected package (candidate only for the
     opted-in model; every other model, an unlisted model and an unstated model get the baseline);
  3. delivered text: the plain `resolve` output contains the selected package's SKILL.md exactly,
     and never the other package's SKILL.md;
  4. resources: `stamp` + `materialize --adapter filesystem-v1` exports the full selected package
     tree (every file, byte-identical), and `library read` returns each resource;
  5. rollback: replacing agents.yaml with the rollback config + `install` returns the opted-in
     model to the baseline.
Writes a JSON report (default: <tmp>/delivery-report.json; --out to choose).

Usage: python -I verify_delivery.py <example dir> [--repo <repo root>] [--out report.json] [--keep]
"""
import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_AP = "npx --yes @guisam/agent-profiles@0.19.4"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class Ctx:
    def __init__(self, ap_cmd, trust):
        self.ap = shlex.split(ap_cmd, posix=os.name != "nt") if isinstance(ap_cmd, str) else ap_cmd
        exe = shutil.which(self.ap[0])
        if exe:
            self.ap[0] = exe
        self.env = dict(os.environ, AGENT_PROFILES_TRUST=str(trust))
        self.log = []

    def run(self, args, cwd, ok=True):
        p = subprocess.run(self.ap + args, cwd=cwd, env=self.env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        self.log.append({"args": args, "rc": p.returncode})
        if ok and p.returncode != 0:
            raise RuntimeError(f"AP {' '.join(args)} failed ({p.returncode}): {p.stderr.strip()[-800:] or p.stdout[-800:]}")
        return p


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("example")
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--out")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    ex, repo = Path(a.example).resolve(), Path(a.repo).resolve()
    ids = json.loads((ex / "IDENTITIES.json").read_text(encoding="utf-8"))
    routing = json.loads((ex / "routing.json").read_text(encoding="utf-8"))
    tmp = Path(tempfile.mkdtemp(prefix="apsp-delivery-"))
    report = {"tool": "verify_delivery",
              "ap_cmd": "AP_CMD override (path not recorded)" if os.environ.get("AP_CMD") else DEFAULT_AP,
              "checks": {}, "ok": False}
    checks = report["checks"]
    try:
        store, consumer, out_root = tmp / "store", tmp / "consumer", tmp / "exports"
        store.mkdir(), out_root.mkdir()
        shutil.copytree(ex / "consumer", consumer)
        shutil.copyfile(ex / "trust.example.yaml", tmp / "trust.yaml")
        c = Ctx(os.environ.get("AP_CMD", DEFAULT_AP), tmp / "trust.yaml")
        v = c.run(["--version"], tmp, ok=False)
        report["ap_version_output"] = (v.stdout or v.stderr).strip()[:80]

        # 1. bytes and digests
        pins = {}
        for ident, meta in ids["packages"].items():
            src = repo / meta["path"]
            bad = {f: m["sha256"] for f, m in meta["files"].items() if sha(src / f) != m["sha256"]}
            extra = sorted(p.name for p in src.iterdir() if p.is_file() and p.name not in meta["files"])
            out = json.loads(c.run(["add", ident, "--source", str(src), "--store", str(store), "--json"], tmp).stdout)
            digest = out.get("sha256") or out.get("digest") or (out.get("package") or {}).get("sha256")
            pins[ident] = digest
            checks[f"package {ident}"] = {"file_hash_mismatches": bad, "unpinned_files": extra,
                                          "ap_digest": digest, "digest_matches_pin": digest == meta["ap_0_19_4_digest"]}
        c.run(["install", "--offline", "--store", str(store), "--json"], consumer)

        skill_text = {ident: (repo / meta["path"] / "SKILL.md").read_text(encoding="utf-8")
                      for ident, meta in ids["packages"].items()}

        def selected(model_args):
            out = json.loads(c.run(["resolve", "--store", str(store), "--host", "claude", "--identity-source",
                                    "host-stated", "--role", routing["role"], "--json", *model_args], consumer).stdout)
            req = [r for r in out.get("required", []) if r.get("id") == routing["skill"]]
            digest = ((req[0].get("backing") or {}).get("sha256")) if req else None
            # AP 0.19.4 resolve --json identifies the package by digest; map it through the pins.
            by_digest = {m["ap_0_19_4_digest"]: i for i, m in ids["packages"].items()}
            return by_digest.get(digest, f"unpinned:{digest}"), digest

        def plain(model_args):
            return c.run(["resolve", "--store", str(store), "--host", "claude", "--identity-source", "host-stated",
                          "--role", routing["role"], *model_args], consumer).stdout

        # 2 + 3. routing and delivered text
        rt = {}
        for case in routing["cases"]:
            margs = ["--model", case["model"]] if case["model"] else []
            ident, digest = selected(margs)
            text = plain(margs)
            others = [i for i in skill_text if i != case["expect"]]
            rt[case["model"] or "<unstated>"] = {
                "expected": case["expect"], "selected": ident, "selected_digest": digest,
                "routing_ok": ident == case["expect"],
                "skill_text_exact": skill_text[case["expect"]].strip() in text,
                "other_arm_text_absent": all(skill_text[o].strip() not in text for o in others)}
        checks["routing_and_text"] = rt

        # 4. resources via stamp + filesystem-v1 export, and library read
        res = {}
        for case in routing["cases"]:
            if not case["model"] or case["model"] in res:
                continue
            st = json.loads(c.run(["stamp", "--store", str(store), "--host", "claude", "--identity-source", "user",
                                   "--model", case["model"], "--role", routing["role"], "--json"], consumer).stdout)
            dest = out_root / case["model"]
            c.run(["materialize", st["digest"], "--store", str(store), "--adapter", "filesystem-v1",
                   "--output-root", str(out_root), "--destination", str(dest), "--protect-root", str(repo),
                   "--json"], consumer)
            meta = ids["packages"][case["expect"]]
            pkg_dirs = list((dest / "content" / "packages" / "sha256").glob("*"))
            tree = {}
            for d in pkg_dirs:
                for f, m in meta["files"].items():
                    hits = list(d.rglob(f))
                    if hits:
                        tree[f] = sha(hits[0]) == m["sha256"]
            reads = {}
            name, ver = case["expect"].rsplit("@", 1)
            for f, m in meta["files"].items():
                if f in ("SKILL.md", "package.yaml"):
                    continue
                r = c.run(["library", "read", case["expect"], f, "--store", str(store)], consumer, ok=False)
                reads[f] = r.returncode == 0 and hashlib.sha256(r.stdout.encode("utf-8")).hexdigest() == m["sha256"]
            res[case["model"]] = {"stamp": st["digest"], "export_package_dirs": len(pkg_dirs),
                                  "export_files_match": tree, "export_complete": set(tree) >= set(meta["files"]) - {"package.yaml"}
                                  and all(tree.values()), "library_read_matches": reads}
        checks["resources"] = res

        # 5. rollback
        shutil.copyfile(ex / "agents.rollback.yaml", consumer / ".agent-profiles" / "agents.yaml")
        c.run(["install", "--offline", "--store", str(store), "--json"], consumer)
        rb = {}
        for case in routing["cases"]:
            margs = ["--model", case["model"]] if case["model"] else []
            ident, _ = selected(margs)
            rb[case["model"] or "<unstated>"] = {"selected": ident, "ok": ident == routing["baseline"]}
        checks["rollback"] = rb

        report["ok"] = (all(not v["file_hash_mismatches"] and v["digest_matches_pin"]
                            for k, v in checks.items() if k.startswith("package "))
                        and all(v["routing_ok"] and v["skill_text_exact"] and v["other_arm_text_absent"] for v in rt.values())
                        and all(v["export_complete"] and all(v["library_read_matches"].values()) for v in res.values())
                        and all(v["ok"] for v in rb.values()))
        report["ap_calls"] = len(c.log)
    except Exception as exc:  # report, never hide
        report["error"] = str(exc)
    finally:
        out = Path(a.out) if a.out else tmp / "delivery-report.json"
        out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=1, sort_keys=True))
        if not a.keep and not a.out:
            pass  # keep tmp so the report remains readable; it is disposable
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
