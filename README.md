# agent-profiles-superpowers

Experimental companion to [Agent Profiles](https://github.com/guisam/Agent-Profiles)
(AP). It holds versioned packages of [Superpowers](https://github.com/obra/superpowers)
skills, model-specific candidate variants, frozen behavioral evaluations and
findings. Tracking issue: [Agent-Profiles#88](https://github.com/guisam/Agent-Profiles/issues/88).

**Status (2026-11-08): wrapped up as a reusable workflow and published here.**
There is no package release and nothing is signed. **No variant is adopted:**
every model uses the full upstream 7.0.2 content by default. Raw transcripts,
ledgers and host identifiers stay private; the shared results are the
sanitized exports. This project's own content is licensed under MIT
([LICENSE](LICENSE)). The adapted skill packages keep the upstream Superpowers
MIT license.

**Start here: [workflow/](workflow/README.md).** It is a plugin-free workflow
for maintainers to propose, deliver (through AP, exact-model opt-in with full
upstream fallback) and evaluate per-model skill variants. It includes an
isolation preflight, a campaign planner, a sanitized results format and an
opt-in beta process. The worked example is the TDD Sonnet 5.5 candidate
([GUIDE](workflow/GUIDE.md)).

| Experiment | Treatment | Outcome |
| --- | --- | --- |
| `apsp-bs-001` | **Shortening**: delete 221 bytes judged redundant for Sonnet | Candidate rejected for **lack of benefit**. The original "one must-pass regression" (C02) was withdrawn in audit. |
| `apsp-bs-002` stage 1 | **Sequencing clarification** of L164-166 | Original procedure: INCONCLUSIVE. Corrected after a documented override: **STOP-NEGATIVE** (0/6 vs 0/6 on the primary endpoint). Candidate **retired**. |
| `apsp-sd-001` (2026-11-08) | **Compaction** of systematic-debugging Phase 1-3 for Sonnet 5.5 (−1406 bytes, −14.8%) | **Prepared, never run; not pursued.** It was prepared while Ponytail text was in the coordinator's context, and was not re-reviewed. Kept as an unvalidated candidate: [PROPOSAL](experiments/systematic-debugging-compaction/PROPOSAL.md). |
| `apsp-tdd-001` (2026-11-08) | **Compaction** of test-driven-development for Sonnet 5.5 (−2553 bytes, −26.7% of `SKILL.md`; diagram and worked examples only, every rule and reminder kept) | **Closed. Stage 1 PROCEED:** no observed regression in the screening suite (accepted: 18/21 vs 18/21, all 21 paired reps tied), and 9.31% fewer total execution tokens. **Stage 2 not funded or run; not adopted.** [CLOSEOUT](experiments/tdd-compaction/CLOSEOUT.md) |

The two brainstorming experiments ran with Ponytail SubagentStart
instructions and the native Superpowers skill listing visible to children.
`apsp-tdd-001` ran isolated: no plugins, skills, hooks or MCP servers beyond
5 built-ins, with `init` checked on every run. None of the results transfer to
standalone Superpowers, other models or other deployments. See
[FINDINGS.md](FINDINGS.md).

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
packages/systematic-debugging-upstream/7.0.2/    immutable baseline (upstream v7.0.2, byte-exact + package.yaml + LICENSE)
packages/systematic-debugging-sonnet-5-5/0.1.0/  unvalidated compaction candidate for claude-sonnet-5-5 (RATIONALE.md = change map)
experiments/systematic-debugging-compaction/     apsp-sd-001: contract, draft cases, trial proposal (not frozen, not run)
packages/test-driven-development-upstream/7.0.2/       immutable baseline (upstream v7.0.2, byte-exact + package.yaml + LICENSE)
packages/test-driven-development-sonnet-5-5/0.1.0/     compaction candidate for claude-sonnet-5-5: screened, not adopted (CLOSEOUT-STATUS.md)
experiments/tdd-compaction/                      apsp-tdd-001: closed (CLOSEOUT.md); stage-1 freeze, results, sanitized export, audit tools; unfunded stage-2 design
workflow/                                  reusable workflow: GUIDE, EVALUATION, BETA, example AP config, tools, results schema
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
python -I workflow/tools/verify_delivery.py workflow/examples/tdd-sonnet-5-5   # TDD routing, delivery, resources, rollback
(cd workflow/tools && python -I test_workflow_tools.py)
```

Expected digests are in [PROVENANCE.md](PROVENANCE.md#packages). Locking a
consumer is subject to your machine's AP trust policy. These packages declare
the `commands` effect, because the skill instructs running helper scripts.
