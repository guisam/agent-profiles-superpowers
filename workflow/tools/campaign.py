"""Campaign definition check and run schedule. Runner-agnostic; no model calls.

  python -I campaign.py check <campaign.json>   # required fields, arm pins, configuration completeness
  python -I campaign.py plan  <campaign.json>   # deterministic schedule as JSON lines: case, arm, rep, slot

Schedule ("balanced"): for each rep, cases run in a seeded shuffle; within each (case, rep) both arms
run back to back, and across reps each case runs full-first and candidate-first as evenly as
possible (exactly half each for an even rep count), with the first-arm assignment itself seeded.
Use your own runner to execute the slots (one fresh process and a fresh fixture copy per slot)
and record evidence per workflow/EVALUATION.md.
"""
import json
import random
import sys
from pathlib import Path

REQUIRED = {
    "root": ["schema", "id", "configuration", "arms", "suite", "cases", "reps_per_arm", "seed", "order", "limits"],
    "configuration": ["model", "host", "host_version", "ap_version", "delivery_route", "tools", "launch_flags"],
}


def check(c):
    errs = [f"missing {k}" for k in REQUIRED["root"] if k not in c]
    errs += [f"configuration.{k} missing" for k in REQUIRED["configuration"] if k not in c.get("configuration", {})]
    arms = c.get("arms", {})
    if len(arms) != 2:
        errs.append("exactly two arms are required (baseline and candidate)")
    for a, v in arms.items():
        if not v.get("package") or not v.get("ap_digest") or len(v.get("ap_digest", "")) != 64:
            errs.append(f"arm {a}: package and full 64-hex ap_digest required")
    if c.get("configuration", {}).get("model") in (None, "", "auto", "unknown"):
        errs.append("configuration.model must be an exact model ID (never inferred)")
    if c.get("order") != "balanced":
        errs.append("order must be 'balanced'")
    return errs


def plan(c):
    rng = random.Random(c["seed"])
    arms = sorted(c["arms"])
    reps = c["reps_per_arm"]
    first = {}
    for case in c["cases"]:
        firsts = [arms[i % 2] for i in range(reps)]
        rng.shuffle(firsts)
        first[case] = firsts
    out = []
    for rep in range(1, reps + 1):
        order = list(c["cases"])
        rng.shuffle(order)
        for case in order:
            a0 = first[case][rep - 1]
            for arm in (a0, [x for x in arms if x != a0][0]):
                out.append({"case": case, "arm": arm, "rep": rep, "slot": f"{case}/{arm}/{rep}"})
    return out


def main(argv):
    if len(argv) != 2 or argv[0] not in ("check", "plan"):
        print(__doc__)
        return 2
    c = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errs = check(c)
    if errs:
        print("\n".join(errs))
        return 1
    if argv[0] == "check":
        print(f"campaign {c['id']}: ok ({len(c['cases'])} cases x {len(c['arms'])} arms x {c['reps_per_arm']} reps "
              f"= {len(c['cases']) * 2 * c['reps_per_arm']} slots; model {c['configuration']['model']})")
        return 0
    for s in plan(c):
        print(json.dumps(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
