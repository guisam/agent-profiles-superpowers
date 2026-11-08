# agent-profiles-superpowers

Experimental companion to [Agent Profiles](https://github.com/guisam/Agent-Profiles)
(AP). It holds versioned packages of [Superpowers](https://github.com/obra/superpowers)
skills, model-specific candidate variants, frozen behavioral evaluations and
findings. Tracking issue: [Agent-Profiles#88](https://github.com/guisam/Agent-Profiles/issues/88).

**Status (2026-11-08): first slice complete, local only.** There is no remote,
no release, and nothing is published or signed. Brainstorming only, Sonnet 5.5
only. **No variant is adopted:** every model uses the full upstream 7.0.2
content.

| Experiment | Treatment | Outcome |
| --- | --- | --- |
| `apsp-bs-001` | **Shortening**: delete 221 bytes judged redundant for Sonnet | Candidate rejected for **lack of benefit**. The original "one must-pass regression" (C02) was withdrawn in audit. |
| `apsp-bs-002` stage 1 | **Sequencing clarification** of L164-166 | Original procedure: INCONCLUSIVE. Corrected after a documented override: **STOP-NEGATIVE** (0/6 vs 0/6 on the primary endpoint). Candidate **retired**. |

Both ran with Ponytail SubagentStart instructions and the native Superpowers
skill listing visible to children. The results do not transfer to standalone
Superpowers, other models or other deployments. See [FINDINGS.md](FINDINGS.md).

## Credit and thanks

- **Nikolay Petrov ([@napetrov](https://github.com/napetrov))** published the
  fact-level knowledge map that nominated every candidate change here: probes,
  answers, source spans, reproduction commands and clear caveats.
  [obra/superpowers#2665](https://github.com/obra/superpowers/issues/2665),
  [dataset revision `586f823`](https://github.com/napetrov/obra-superpowers/tree/586f82373fa984f941bbaaee4d3118f7c8a30f14).
  Thank you. The knowledge measurements are his, made with
  **[Intel's dokimi](https://github.com/intel/dokimi)**. They are not results of
  this project.
- **Jesse Vincent / obra** wrote **Superpowers**, MIT licensed. Every package
  here keeps the upstream `LICENSE`.
- The later behavioral results are this project's. They are attributed
  separately in [FINDINGS.md](FINDINGS.md).

None of these people or organizations reviewed or endorsed this work.
Thanks do not grant redistribution rights. The dataset has no license, so it
is linked and summarized, not copied ([PROVENANCE.md](PROVENANCE.md#license-audit)).

## Ownership boundary

| Here (content, own release cycle) | In Agent-Profiles (engine) |
| --- | --- |
| Skill packages, baselines, candidates, rationale | Package format, store, lock, selection, stamps, evidence/promotion interfaces |
| Frozen cases, rubric, trial protocol, results | Generic fixes and gaps found here (raised as separate issues) |
| Findings about specific skills and models | Integration instructions and a link to this case study |

This is like a shared ESLint config versus ESLint itself, with one difference:
LLM instructions are not deterministic enforcement.

## Layout

```text
packages/brainstorming-upstream/7.0.2/     immutable baseline (upstream v7.0.2, byte-exact + package.yaml + LICENSE)
packages/brainstorming-sonnet-5-5/0.1.0/   candidate for claude-sonnet-5-5 (rejected; retained as failed variant)
packages/brainstorming-sonnet-5-5/RATIONALE.md   exact diff and why (STATUS.md: current status)
packages/brainstorming-sequencing/0.1.0/  sequencing treatment for apsp-bs-002 (retired; STATUS.md)
selectors/                                 trial consumer configs (alpha = baseline, recommended; beta = archived trial)
evaluations/brainstorming/                 apsp-bs-001: frozen cases, rubric, protocol, fixture, collector v1, FREEZE.sha256, RESULTS
evaluations/brainstorming/audit/           post-hoc audit: freeze status, grading adjudication, corrections
evaluations/brainstorming/tools/collect_v2.py   harness 2.1.0 (+ tests), used by apsp-bs-002
experiments/brainstorming-clarify-164/     apsp-bs-002: proposal, treatment, stage-1 freeze, amendments, RESULTS (closed)
reports/                                   AP gap reports (filed as Agent-Profiles #89, #90, #91), repro script
PROVENANCE.md                              sources, license audit, source mapping, hashes, closure, platform checks
FINDINGS.md                                knowledge vs delivery vs behavior vs cost, kept separate
private/                                   ignored: consumers, store, raw transcripts, local dataset copies
```

There is no npm package. Packages are plain directories in AP's
`package.yaml` schema 1, imported with `agent-profiles add`.

## Selection model

A consumer declares one binding, `skills.brainstorming`. **Recommended for
current use:** the baseline for every model, with no assignments
([selectors/alpha.agents.yaml](selectors/alpha.agents.yaml)):

```yaml
skills:
  brainstorming: {package: "@apsp/brainstorming-upstream", version: "7.0.2"}
assignments: {}
```

**Archived trial configuration, do not use:** experiment `apsp-bs-001` opted one
exact model into a candidate with a config v3 assignment
([selectors/beta.agents.yaml](selectors/beta.agents.yaml)). That candidate was
rejected. The snippet shows the routing mechanism only:

```yaml
assignments:
  sonnet-candidate:   # archived: routes to a rejected candidate
    when: {model: claude-sonnet-5-5, role: brainstormer}
    bindings:
      skills.brainstorming: {package: "@apsp/brainstorming-sonnet-5-5", version: "0.1.0"}
```

In that configuration every other model, including unknown ones, fell back to the
full upstream content.

## Reproduce (local, no model calls)

Prerequisites: Node 24, Git Bash on Windows, the upstream checkout at
`../superpowers`. The commands use a throwaway store and leave your home store
alone.

```sh
STORE=$(mktemp -d)
npx --yes @guisam/agent-profiles@0.19.4 add @apsp/brainstorming-upstream@7.0.2 --source "$PWD/packages/brainstorming-upstream/7.0.2" --store "$STORE" --json
npx --yes @guisam/agent-profiles@0.19.4 add @apsp/brainstorming-sonnet-5-5@0.1.0 --source "$PWD/packages/brainstorming-sonnet-5-5/0.1.0" --store "$STORE" --json
python -I evaluations/brainstorming/tools/collect.py selftest
```

Expected digests are in [PROVENANCE.md](PROVENANCE.md#packages). Locking a
consumer is subject to your machine's AP trust policy. These packages declare
the `commands` effect, because the skill instructs running helper scripts.
