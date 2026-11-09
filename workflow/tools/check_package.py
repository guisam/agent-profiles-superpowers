"""Static closure check for a skill package directory (AP package.yaml schema 1). No model calls.

Reports, per package:
  - manifest: name, version, entrypoint present; LICENSE present;
  - links: every relative Markdown link and every backticked in-package path in *.md resolves
    to a file inside the package (missing ones are errors);
  - scripts: files under scripts/ and files with a shebang, with their interpreter;
  - cross-skill references: `superpowers:<skill>` names, which must be packaged separately or
    documented as unpackaged dependencies (listed, never silently dropped);
  - optionally, --compare <other package dir>: files that differ (to confirm a candidate only
    changes what its change map says).
Usage: python -I check_package.py <package dir> [<package dir> ...] [--compare <dir>] [--json]
Exit 1 if any package has errors.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
TICK = re.compile(r"`((?:\./|\.\./)?[\w.-]+(?:/[\w.-]+)*\.(?:md|sh|js|cjs|mjs|py|ts|json|yaml|yml|html|txt))`")
XSKILL = re.compile(r"\bsuperpowers:([a-z][a-z0-9-]+)")


def manifest(text):
    out = {}
    for key in ("name", "version", "entrypoint", "license"):
        m = re.search(rf"^\s*{key}:\s*\"?([^\"\n]+)\"?\s*$", text, re.M)
        out[key] = m.group(1).strip() if m else None
    return out


def check(pkg, compare=None):
    pkg = Path(pkg).resolve()
    rep = {"package": str(pkg.name), "errors": [], "warnings": []}
    mf = pkg / "package.yaml"
    if not mf.exists():
        rep["errors"].append("package.yaml missing")
        return rep
    m = manifest(mf.read_text(encoding="utf-8"))
    rep["manifest"] = m
    for k in ("name", "version", "entrypoint"):
        if not m[k]:
            rep["errors"].append(f"manifest field {k} missing")
    if m["entrypoint"] and not (pkg / m["entrypoint"]).exists():
        rep["errors"].append(f"entrypoint {m['entrypoint']} missing")
    if not (pkg / "LICENSE").exists():
        rep["errors"].append("LICENSE missing")
    files = sorted(p for p in pkg.rglob("*") if p.is_file())
    rep["files"] = {str(p.relative_to(pkg)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    links, xs = set(), set()
    for md in (p for p in files if p.suffix == ".md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for target in LINK.findall(text) + TICK.findall(text):
            if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            resolved = (md.parent / target).resolve()
            if resolved == pkg or pkg in resolved.parents:
                links.add((str(md.relative_to(pkg)).replace("\\", "/"), target, resolved.exists()))
            else:
                rep["warnings"].append(f"{md.name}: reference outside the package: {target}")
        xs |= set(XSKILL.findall(text))
    rep["links"] = [{"from": f, "to": t, "ok": ok} for f, t, ok in sorted(links)]
    missing = [l for l in rep["links"] if not l["ok"]]
    # a backticked name that is not a file may be prose (e.g. a command); only Markdown links are hard errors
    for l in missing:
        if re.search(rf"\]\({re.escape(l['to'])}", (pkg / l["from"]).read_text(encoding="utf-8", errors="replace")):
            rep["errors"].append(f"broken link {l['from']} -> {l['to']}")
        else:
            rep["warnings"].append(f"backticked path not in package (may be prose): {l['from']} -> {l['to']}")
    scripts = []
    for p in files:
        head = p.read_bytes()[:64]
        if head.startswith(b"#!") or "scripts" in p.relative_to(pkg).parts:
            interp = head.split(b"\n", 1)[0].decode("utf-8", "replace")[2:].strip() if head.startswith(b"#!") else None
            scripts.append({"path": str(p.relative_to(pkg)).replace("\\", "/"), "shebang": interp})
    rep["scripts"] = scripts
    rep["cross_skill_references"] = sorted(xs - {m["name"].split("/")[-1] if m["name"] else ""})
    if compare:
        other = Path(compare).resolve()
        of = {str(p.relative_to(other)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in other.rglob("*") if p.is_file()}
        rep["compare"] = {"against": other.name,
                          "changed": sorted(f for f in rep["files"] if f in of and of[f] != rep["files"][f]),
                          "only_here": sorted(set(rep["files"]) - set(of)),
                          "only_there": sorted(set(of) - set(rep["files"]))}
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("packages", nargs="+")
    ap.add_argument("--compare")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    reps = [check(p, a.compare) for p in a.packages]
    if a.json:
        print(json.dumps(reps, indent=1))
    else:
        for r in reps:
            m = r.get("manifest") or {}
            print(f"{m.get('name')}@{m.get('version')}: {len(r.get('files', {}))} files, "
                  f"{sum(l['ok'] for l in r.get('links', []))}/{len(r.get('links', []))} references resolve, "
                  f"{len(r.get('scripts', []))} scripts, cross-skill: {r.get('cross_skill_references')}")
            for e in r["errors"]:
                print("  ERROR", e)
            for w in r["warnings"]:
                print("  warn ", w)
            if "compare" in r:
                print("  vs", r["compare"]["against"], "changed:", r["compare"]["changed"],
                      "only here:", r["compare"]["only_here"], "only there:", r["compare"]["only_there"])
    return 1 if any(r["errors"] for r in reps) else 0


if __name__ == "__main__":
    sys.exit(main())
