"""Sanitized results format (apsp-results/1): validator and privacy scan. Stdlib only.

  python -I results_format.py validate <results.json>   # schema + privacy checks; exit 1 on failure

The validator enforces the required structure of workflow/schemas/results.schema.json and
refuses files that look like they contain private material (paths, session IDs, emails,
credentials, transcripts, long free text). It is deliberately strict; it is not a general
JSON Schema engine.
"""
import json
import re
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "results.schema.json"
PRIVATE = [
    (re.compile(r"[A-Za-z]:\\\\|[A-Za-z]:/|/Users/|/home/|AppData"), "filesystem path"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"), "UUID (session or account ID)"),
    (re.compile(r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b"), "email address"),
    (re.compile(r"sk-ant-|ANTHROPIC_API_KEY|Bearer\s+\S{10,}|ghp_[A-Za-z0-9]{10,}"), "credential"),
]
MAX_STRING = 600  # longer free text suggests a transcript excerpt or final message


def require(obj, keys, where, errs):
    for k in keys:
        if k not in obj:
            errs.append(f"{where}: missing '{k}'")


def validate(doc):
    errs = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    require(doc, schema["required"], "root", errs)
    if doc.get("schema") != "apsp-results/1":
        errs.append("root: schema must be 'apsp-results/1'")
    props = schema["properties"]
    for sect in ("campaign", "configuration"):
        if isinstance(doc.get(sect), dict):
            require(doc[sect], props[sect]["required"], sect, errs)
    if doc.get("campaign", {}).get("suite_kind") not in ("screening", "held-out"):
        errs.append("campaign.suite_kind must be 'screening' or 'held-out'")
    arm_req = props["arms"]["additionalProperties"]["required"]
    for arm, ident in (doc.get("arms") or {}).items():
        require(ident, arm_req, f"arms.{arm}", errs)
    run_req = props["runs"]["items"]["required"]
    for i, r in enumerate(doc.get("runs") or []):
        require(r, run_req, f"runs[{i}]", errs)
        if r.get("arm") not in (doc.get("arms") or {}):
            errs.append(f"runs[{i}]: arm '{r.get('arm')}' not declared in arms")
        u = r.get("usage")
        if isinstance(u, dict) and any(v is None for v in u.values()):
            pass  # explicit unknowns are allowed; zero is never substituted
    require(doc.get("decision") or {}, ["official", "accepted"], "decision", errs)
    require(doc.get("privacy") or {}, ["excluded"], "privacy", errs)
    # privacy scan over every string
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for j, v in enumerate(x):
                walk(v, f"{path}[{j}]")
        elif isinstance(x, str):
            for rx, what in PRIVATE:
                if rx.search(x):
                    errs.append(f"privacy: {what} in {path}")
            if len(x) > MAX_STRING:
                errs.append(f"privacy: long free text ({len(x)} chars) in {path}")
    walk(doc, "root")
    return errs


def main(argv):
    if len(argv) != 2 or argv[0] != "validate":
        print(__doc__)
        return 2
    doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errs = validate(doc)
    print("\n".join(errs) if errs else f"valid apsp-results/1: {len(doc['runs'])} runs, arms {sorted(doc['arms'])}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
