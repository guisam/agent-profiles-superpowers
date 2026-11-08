# Draft AP report: `update` cannot move a tuple to a differently named package

Status: **Filed 2026-11-08 as two issues: enhancement [Agent-Profiles#89](https://github.com/guisam/Agent-Profiles/issues/89) and defect [Agent-Profiles#91](https://github.com/guisam/Agent-Profiles/issues/91).** The text below is the original draft. Status was **draft, not filed.** Target: guisam/Agent-Profiles. Found during #88.

Classification:

1. **Unsupported enhancement:** moving one role × model × host tuple to a
   *different package name* (for example, a model-specific variant package)
   through `update`. The documentation describes only version moves within a
   binding's default package
   (`docs/versioned-packages.md`, "Outdated and update"), so this is not a
   defect.
2. **Minor defect (input handling):** a package-qualified target is not
   rejected as malformed. It is concatenated onto the default package name and
   reported as a missing library version.

Not an issue: in configuration v3, `update` requires the target version to
have a release label from `revision record`. That is documented ("needs
revision record").

## Environment

As in [AP-GAP-1](AP-GAP-1-required-package-identity.md): AP 0.19.4,
Windows 11, Git Bash, Node 24.20.0, isolated store and trial policy.

## Reproduction

`AP=<agent-profiles executable> bash reports/repro-ap-gaps.sh <new-empty-dir>`.
Observed:

```text
-- v2 same-name version move (control):
  Selections changed: worker × model-a × claude skills.tool @demo/tool@1.0.0 → @demo/tool@1.1.0
-- v2 package-qualified target:
Agent Profiles: @demo/tool@@demo/tool-variant@1.0.0: not in the library; versions: 1.1.0, 1.0.0
-- v3 same-name move without a release label (documented precondition):
Agent Profiles: update: @demo/tool@1.1.0 has no release label; configuration v3 pins a revision. Adopt it with agent-profiles revision record first
```

## Impact

In #88 the variants were named packages
(`@apsp/brainstorming-upstream@7.0.2` vs `@apsp/brainstorming-sonnet-5-5@0.1.0`),
which config v3 bindings support. Opting one exact model into such a variant
therefore needs a hand edit of `agents.yaml` plus `install`. That bypasses
`update`'s preview, other-tuple invariance check, content diff, evidence
display and `--expect` freshness guard. A manual isolation check in #88
confirmed that the other consumer and the other tuples were unaffected. The
safety checks were done by hand, not by AP.

## Suggested direction (for discussion)

- **Enhancement:** accept a package-qualified target in config v3, e.g.
  `update skills.tool @demo/tool-variant@1.0.0`. Write it as a complete binding
  replacement and run the same preview and invariance checks.
- **Defect fix:** validate the version argument (`x.y.z`) before the library
  lookup and print a clear message for package-qualified input when
  cross-package moves are unsupported.

## Retracted during #88

An earlier note that `update` ignores `--store` was wrong: the test passed a
relative store path. With an absolute `--store`, `update` behaves correctly.
