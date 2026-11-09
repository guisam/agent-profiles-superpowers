"""Deterministic checks for the Opus 5.5 TDD candidate. No model calls.
Writes experiments/tdd-opus-compaction/CHECKS.json and prints a summary.
Usage: python -I check_candidate.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EXP = REPO / "experiments/tdd-opus-compaction"
PKG = {
    "upstream": REPO / "packages/test-driven-development-upstream/7.0.2",
    "sonnet": REPO / "packages/test-driven-development-sonnet-5-5/0.1.0",
    "opus": REPO / "packages/test-driven-development-opus-5-5/0.1.0",
}
# Terms other upstream skills rely on (git grep of obra/superpowers v7.0.2, outside this skill).
INBOUND = ["## Red-Green-Refactor", "### RED - Write Failing Test", "### Verify RED - Watch It Fail",
           "### GREEN - Minimal Code", "### Verify GREEN - Watch It Pass", "### REFACTOR - Clean Up",
           "### Repeat", "- Delete means delete", "| \"Keep as reference, write tests first\" |",
           "\"Keep as reference\" or \"adapt existing code\"", "## The Iron Law"]
FORBIDDEN = [r"\$ARGUMENTS", r"\$[0-9]", r"(?i)ultrathink"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def section(text, heading):
    lines = text.splitlines()
    i = lines.index(heading)
    out = []
    for l in lines[i + 1:]:
        if l.startswith("## "):
            break
        out.append(l)
    return [l for l in out if l.strip()]


def frontmatter(text):
    return text.split("---", 2)[1]


def coverage(req, text, resource_text):
    missing = []
    for a in req.get("anchors", []):
        alt = (req.get("alt") or {}).get(a)
        if a in text or (alt and alt in text):
            continue
        missing.append(a)
    for a in req.get("resource_anchors", []):
        if a not in resource_text:
            missing.append(f"(resource) {a}")
    return missing


def subsequence_check(cand, up):
    """Every non-blank candidate line that also exists in upstream appears in the same relative order;
    lines absent from upstream are reported as insertions."""
    ul = up.splitlines()
    pos, inserted, out_of_order = 0, [], []
    uset = set(ul)
    for l in cand.splitlines():
        if not l.strip():
            continue
        if l not in uset:
            inserted.append(l)
            continue
        try:
            pos = ul.index(l, pos) + 1
        except ValueError:
            out_of_order.append(l)
    return inserted, out_of_order


def main():
    reqs = json.loads((EXP / "requirements.json").read_text(encoding="utf-8"))["requirements"]
    texts = {k: (p / "SKILL.md").read_text(encoding="utf-8") for k, p in PKG.items()}
    res = {k: (p / "writing-good-tests.md").read_text(encoding="utf-8") for k, p in PKG.items()}
    draft = (EXP / "CONTRACT-ONLY-DRAFT.md").read_text(encoding="utf-8")
    up = texts["upstream"]
    report = {"coverage": {}, "sections": {}, "subsequence": {}, "frontmatter_identical": {},
              "forbidden_tokens": {}, "resources": {}, "inbound": {}, "contract_only_draft": {}, "sizes": {}}

    for name, text in texts.items():
        cov = {}
        for r in reqs:
            miss = coverage(r, text, res[name])
            for h in r.get("sections", []):
                miss += [f"[{h}] {l}" for l in section(up, h) if l not in text]
            cov[r["id"]] = miss
        report["coverage"][name] = {"covered": sum(not v for v in cov.values()), "total": len(reqs),
                                    "missing": {k: v for k, v in cov.items() if v}}
        report["frontmatter_identical"][name] = frontmatter(text) == frontmatter(up)
        report["forbidden_tokens"][name] = [p for p in FORBIDDEN if re.search(p, text)]
        report["inbound"][name] = [t for t in INBOUND if t not in text]
        report["resources"][name] = {
            "writing-good-tests.md": sha(res[name].encode()) == sha(res["upstream"].encode()),
            "LICENSE": sha((PKG[name] / "LICENSE").read_bytes()) == sha((PKG["upstream"] / "LICENSE").read_bytes()),
            "link_present": "[writing-good-tests.md](writing-good-tests.md)" in text,
            "names_writing_skills": "superpowers:writing-skills" in res[name]}
        if name != "upstream":
            ins, ooo = subsequence_check(text, up)
            report["subsequence"][name] = {"inserted_lines": ins, "out_of_order": ooo}

    contract_ids = [r["id"] for r in reqs if r["kind"] in ("contract", "contract-inferred")]
    tags = set(re.findall(r"\[([A-Z][0-9])\]", draft))
    # A1 lives in frontmatter (cannot carry a tag): covered when the description is verbatim.
    if frontmatter(draft) == frontmatter(up):
        tags.add("A1")
    report["contract_only_draft"] = {"contract_ids": len(contract_ids),
                                     "missing_ids": [i for i in contract_ids if i not in tags],
                                     "omitted_non_contract": [r["id"] for r in reqs if r["id"] not in tags]}

    def size(t):
        return {"bytes": len(t.encode("utf-8")), "words": len(t.split()), "lines": len(t.splitlines())}
    for name, text in texts.items():
        report["sizes"][name] = dict(size(text), resource_bytes=len(res[name].encode("utf-8")),
                                     sha256=sha(text.encode("utf-8")))
    body = draft.split("-->", 1)[1].lstrip("\n")
    fm = "---" + draft.split("---", 2)[1] + "---\n\n"
    report["sizes"]["contract_only_draft"] = dict(size(fm + body), resource_bytes=None,
                                                  note="frontmatter + body, excluding the HTML comment banner")

    (EXP / "CHECKS.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    ok = True
    for name in texts:
        c = report["coverage"][name]
        flag = c["covered"] == c["total"]
        ok &= flag
        print(f"{name:9} coverage {c['covered']}/{c['total']} frontmatter={report['frontmatter_identical'][name]} "
              f"forbidden={report['forbidden_tokens'][name]} inbound_missing={report['inbound'][name]} "
              f"resources={all(report['resources'][name].values())}")
        if not flag:
            print("   missing:", json.dumps(c["missing"], ensure_ascii=False)[:600])
        ok &= report["frontmatter_identical"][name] and not report["forbidden_tokens"][name] and not report["inbound"][name]
    for name, s in report["subsequence"].items():
        print(f"{name:9} inserted lines: {s['inserted_lines']} out_of_order: {s['out_of_order']}")
        ok &= not s["out_of_order"]
    d = report["contract_only_draft"]
    print(f"contract-only draft: contract IDs missing {d['missing_ids']}; omitted non-contract {d['omitted_non_contract']}")
    ok &= not d["missing_ids"]
    for name, s in report["sizes"].items():
        print(f"size {name:20} {s['bytes']:6} bytes {s['words']:5} words {s['lines']:4} lines  resource {s['resource_bytes']}")
    print("ALL CHECKS PASS" if ok else "CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
