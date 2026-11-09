# Findings

Reported 2026-11-07. Each section states its evidence class. Nothing below
claims optimal skills, guaranteed obedience or accuracy gains. Credit: the
knowledge evidence is Nikolay Petrov's, measured with Intel's dokimi, on
Jesse Vincent/obra's Superpowers (see [README](README.md#credit-and-thanks)).

## Final summary (2026-11-08): reusable workflow; TDD screening closed

- **Deliverable:** [workflow/](workflow/README.md), a plugin-free way to select,
  deliver and evaluate per-model skill variants through AP, with full upstream
  content as the default.
  - Released AP 0.19.4 is verified locally with no model calls: exact-model
    routing, fallback for unlisted, near-miss and unstated models, delivered
    text, full resource export, and rollback.
  - The gaps are stated in the [GUIDE](workflow/GUIDE.md#not-demonstrated-by-this-project-gaps-stated-plainly).
- **TDD compaction for Sonnet 5.5** (`apsp-tdd-001`, §8): stage 1 PROCEED.
  - No observed regression in the screening suite, under the accepted
    adjudication rules: 18/21 vs 18/21, all 21 paired reps tied.
  - 9.31% fewer total execution tokens.
  - Stage 2 was not funded; the candidate is **not adopted**.
- **TDD compaction for Opus 5.5** (`apsp-tdd-002`, §9): a separate candidate
  prepared contract-first. In a 2-rep smoke on 5 development cases it had **no
  candidate-only failures**: 6/10 vs 6/10 with every pair tied (4 vs 5 under
  the frozen checker).
- **What this shows about AP:** one skill, three model-specific deliveries
  from one configuration. `claude-sonnet-5-5` and `claude-opus-5-5` each
  receive their own compacted variant; every other model (including near-miss
  IDs such as `claude-opus-5` and unstated models) receives full upstream. No
  plugin is installed, and each model received exactly the text intended for
  it.
- **No variant of any skill is adopted.** Every model stays on full upstream
  7.0.2.

## Summary at the close of the first slice (2026-11-08)

Two different candidates failed for different reasons. Neither is adopted,
and every model stays on full upstream 7.0.2 content.

| | Shortening (`apsp-bs-001`, §4) | Sequencing clarification (`apsp-bs-002`, §7) |
| --- | --- | --- |
| Change | Delete 221 bytes judged redundant for Sonnet | Reword L164-166 to defer design to the next message |
| Question | Can Sonnet do as well with less text? | Does clearer wording fix the C06 sequencing failure? |
| Result | No benefit; C02 regression withdrawn in audit | No observed improvement on the primary endpoint (0/6 vs 0/6); S3 dropped by 2 runs |
| Outcome | Rejected (lack of benefit) | Original: INCONCLUSIVE; corrected: STOP-NEGATIVE; retired |

Scope: Sonnet 5.5 via a subscription-backed Claude Code host, with the Ponytail
SubagentStart instructions and the native Superpowers skill listing visible to
children. These are small pilots. They do not establish non-inferiority, an
optimum, or behavior for standalone Superpowers, Haiku, Opus, Sol or Bedrock.

## Audit corrections (2026-11-07, coordinator's own audit, not independent)

The sections below are the original findings. A later audit qualifies them; see
[evaluations/brainstorming/audit/](evaluations/brainstorming/audit/):

- Arm labels (`.full.`/`.cand.`) and case IDs were visible in every child
  prompt and path (44/44). The trials were not blind to the model.
- The C02 "regression" disappears under either consistent reading of "one main
  question". The candidate stays rejected for **lack of benefit**, not for
  demonstrated harm.
- C01 cannot discriminate (the skill text is ambiguous). C08 tested only
  recovery with a missing design doc. C06 is a message-sequencing failure;
  the approval gate held in 4/4 runs.
- C11's zero server starts reflects the harness instruction, not skill
  behavior.
- Two frozen files (PROTOCOL.md, collect.py) changed after the freeze. Both
  changes are fully reconstructed, and neither touched what children or graders
  saw. See [FREEZE-STATUS](evaluations/brainstorming/audit/FREEZE-STATUS.md).
- `beta` and the candidate-routing example are archived trial configurations.
  Use the baseline (`selectors/alpha.agents.yaml`).

## 1. Knowledge evidence (Petrov / dokimi, not this project)

Source: [dataset `586f823`](https://github.com/napetrov/obra-superpowers/tree/586f82373fa984f941bbaaee4d3118f7c8a30f14).
Bedrock Haiku 5.5 and Sonnet 5.5; the judge was Sonnet 5.5, which also judged
its own arm.

- Brainstorming: 25 of 118 atoms were probed. Strict outcomes: 17 added for both
  models, 3 added for Haiku but redundant for Sonnet, 2 redundant for both, and
  none degraded.
- The blue span L164-166 is wrong both with and without the skill for Haiku.
- This is knowledge ("can the model state the rule"), not behavior.

## 2. Source and packaging (this project; verified locally)

- Baseline v7.0.2 `22f0b46` is very likely the study's checkout. All 478 atom
  spans fit 7.0.2; 5 do not fit 7.0.1. The only quoted span matches exactly.
  This is inferred, not proven: the data commit has no parent.
- The complete brainstorming tree (SKILL.md, 2 references, 5 scripts) plus the
  upstream LICENSE was imported byte-exact from git blobs. Hashes are in
  [PROVENANCE.md](PROVENANCE.md).
- Helpers pass `node --check` and `bash -n` on Windows/Git Bash. They were
  never executed.
- The dataset has no license, so it is linked and summarized, not copied.

## 3. Delivery (AP 0.19.4, two disposable consumers, verified)

- Exact-model routing works.
  - beta: `claude-sonnet-5-5` → candidate.
  - beta: Haiku, Opus and an unknown model → full baseline.
  - alpha: every model → baseline.
  - All 44 trial children received the intended body, checked by content.
- Isolation works. Changing alpha's pin (edit + install) changed alpha's
  Sonnet routing only. beta's `agents.yaml` and lock bytes and its routing were
  unchanged. Restoring alpha's two files reproduced the original hashes and
  routing.
- Trust policy: the operator's machine policy (`require_approval: true`,
  `commands` effect not allowed) correctly withheld both packages and said so.
  By operator decision, the trials used a trial-scoped `AGENT_PROFILES_TRUST`
  policy for the disposable consumers only. `~/.agent-profiles/trust.yaml` was
  not modified.
- Native Superpowers plugin confound: it is globally enabled in the host, and
  no child called the `Skill` tool (0/44). Hidden system-prompt skill listings
  were still visible to children; this is not controlled.

## 4. Behavior (this project; small paired pilot)

The full table is in [evaluations/brainstorming/RESULTS.md](evaluations/brainstorming/RESULTS.md).

- *[Audit, 2026-11-07: the C02 regression below was withdrawn. The rejection
  stands, for lack of benefit. See Audit corrections above.]*
- **Candidate rejected.** Sonnet full passed 18/22 case-runs; the candidate
  passed 17/22. One must-pass regression: C02 ambiguous request, a second
  menu-style question in 1 of 2 runs. On the two cases aimed at the deleted
  text (C04 user-controlled how, C11 scope stays in text), both arms passed 4/4.
  The pilot shows **no benefit** from the deletion and one observed regression.
  The 2-repetition design cannot attribute that regression to the deletion.
- **Shared weakness, both arms, 4/4 runs: C06 one sensible approach.** Sonnet
  puts the design into the approaches message, contradicting L164-166. This
  matches the Haiku misreading in Petrov's `harmful.md`. It supports a
  *clarifying rewrite* of L164-166 (as a separate, declared treatment) rather
  than any removal.
- **Contestable case C01 (complete PRD):** both arms built the change
  immediately in 4/4 runs. The skill text allows two readings ("everything that
  matters is in the request → do it" vs. "a spec… confirm before you build").
  The case needs revision in a later suite version; its result does not
  differentiate the arms.
- Harness compliance: 5/44 children returned the message instead of writing the
  reply file. Those replies were recovered verbatim and recorded separately from
  quality.

## 5. Cost (estimates, not billing)

API-equivalent estimates at Anthropic list rates cached 2026-10-06: full arm
$2.72 and candidate arm $2.73 (22 runs each), graders $2.11. Coordinator usage
is unknown. Actual spending was subscription usage only. Instruction size fell
221 bytes; no token saving was observable.

## 6. Generic AP gaps (filed 2026-11-08)

Both are reproduced with [reports/repro-ap-gaps.sh](reports/repro-ap-gaps.sh)
on AP 0.19.4:

1. [AP-GAP-1](reports/AP-GAP-1-required-package-identity.md), defect, filed as
   [Agent-Profiles#90](https://github.com/guisam/Agent-Profiles/issues/90):
   text `resolve` omits the package identity of a *required* packaged skill but
   prints it for *available* ones. Agents therefore cannot locate the skill's
   supporting files without `--json`.
2. [AP-GAP-2](reports/AP-GAP-2-update-cross-package.md), filed separately as
   enhancement [#89](https://github.com/guisam/Agent-Profiles/issues/89) and
   input-handling defect [#91](https://github.com/guisam/Agent-Profiles/issues/91): `update` cannot target a
   differently named package, and a package-qualified target produces a
   misleading "not in the library" error. The v3 release-label precondition is
   documented behavior.

A relative `--store` path behaved differently than the same relative
`AGENT_PROFILES_STORE` in one test. With absolute paths both behave correctly.
This is not reported as a defect; the cause was not isolated.

## 7. Sequencing clarification of L164-166 (apsp-bs-002 stage 1, 2026-11-08)

Behavioral; Sonnet 5.5; 8 screening cases × 2 arms × 3 repetitions; two blind
Opus graders. Report:
[stage1/RESULTS.md](experiments/brainstorming-clarify-164/stage1/RESULTS.md).

- **Primary endpoint: no observed improvement.** In 0/6 later-turn
  approaches messages per arm did Sonnet defer the design, with or without
  the clarification. This answers the §4 C06 suggestion negatively for this
  wording.
- **Outcome:** INCONCLUSIVE by the original procedure, because the
  identical-file guard rejected U1/U2. STOP-NEGATIVE after a documented
  override: [Amendment 2](experiments/brainstorming-clarify-164/stage1/AMENDMENT-2-identical-file-override.md),
  where transcripts confirmed the graders ran separately. The S3 all-M score
  dropped by 2 runs (3 → 1) in the treatment arm.
- Grading was completed under a post-execution grader-budget amendment
  ([Amendment 1](experiments/brainstorming-clarify-164/stage1/AMENDMENT-1-grader-budget.md)).
- **Environment:** every child context included the Ponytail SubagentStart
  instructions and the native Superpowers skill listing. The result applies
  to that environment and to Sonnet 5.5 only. It says nothing about standalone
  Superpowers, Haiku, Opus or other hosts.
- **Disposition:** `@apsp/brainstorming-sequencing@0.1.0` is retired, not
  adopted, and goes to no stage 2. Every model stays on full upstream content.
- **Harness lesson (fix recorded, not implemented):** byte-identical grade
  files do not show that graders were dependent, and different bytes do not
  show they were independent. A future harness should verify grader
  execution provenance instead.
- Cost, API-equivalent and not billing: children ≈ $6.31, graders ≈ $4.31.

## 8. TDD compaction for Sonnet 5.5 (`apsp-tdd-001`, closed 2026-11-08)

Full record: [CLOSEOUT](experiments/tdd-compaction/CLOSEOUT.md) and
[stage-1 results](experiments/tdd-compaction/stage1/RESULTS.md). Each item
below is labeled with its evidence class.

- **Source and packaging (verified):**
  - The baseline is byte-exact upstream v7.0.2 (blobs `46838cc9`,
    `d3c4482f`, `abf03903`).
  - The candidate changes `SKILL.md` only (−2,553 bytes): the diagram and
    worked examples are removed, and one condition is extracted. Every rule,
    rationalization row, red flag and checklist item is kept.
  - `check_package.py --compare` confirms that only `SKILL.md` and
    `package.yaml` differ.
- **Knowledge (Petrov/dokimi):** used as leads for candidate generation only.
  The change map labels each capability-dependent cut.
- **Delivery (verified, AP 0.19.4, no model calls):** see the final summary
  above. During the trial, every child's transcript showed its own arm's text.
  Isolation was checked from `init` on all 46 child and 9 grader runs.
- **Behavior (screening):**
  - 7 cases × 2 arms × 3 reps, 42 valid runs.
  - Accepted interpretation (operator gate): 18/21 vs 18/21, all paired reps
    tied; Gr1 24/24.
  - Official frozen scores (12 vs 14) are kept for provenance. The difference
    comes from documented capture and fixture defects, and from gate rulings
    on R5 and R6.
  - **Shared gaps** (identical text in both arms):
    - no run asked before the configuration-file exception (R6);
    - under explicit permission, every run skipped tests and disclosed it (R5,
      compliant under the accepted permission reading).
  - **Not established:** equivalence, held-out performance, discovery
    delivery, other models or hosts.
- **Cost:**
  - total execution tokens −9.31%: all four categories, mostly the smaller
    prompt re-read each request;
  - reported cost $0.752 vs $0.689 (API-equivalent; the actual use was
    subscription allowance);
  - experiment total: children and graders $2.71; the coordinator's
    build-and-run window about 24.7M tokens. The audit and closeout sessions
    were not measured.

## 9. TDD compaction for Opus 5.5 (`apsp-tdd-002`, smoke, 2026-11-08)

Full record: [smoke results](experiments/tdd-opus-compaction/smoke/RESULTS.md),
[candidate rationale](packages/test-driven-development-opus-5-5/RATIONALE.md).

- **Candidate:** `@apsp/test-driven-development-opus-5-5@0.1.0`, built
  contract-first from upstream (not from the Sonnet candidate).
  - `SKILL.md` goes from 9,578 to 6,928 bytes (−27.7%).
  - 31/31 upstream requirements are mechanically covered. Every rule, rebuttal,
    red flag and checklist item is kept, and the resources are unchanged.
  - The worked examples, the diagram and the placeholder commands are
    removed. The cycle order and "run the test" are stated explicitly.
- **Delivery (verified):** AP 0.19.4 routed the candidate only to
  `claude-opus-5-5`; Sonnet, Haiku, `claude-opus-5` and unknown IDs got
  full upstream. Isolation was checked on every run.
- **Behavior (smoke, development cases, 2 reps per arm, no graders):**
  - No candidate-only failures.
  - D2 (feature, "options later") and D3a (explicit permission to skip
    tests): 2/2 in both arms.
  - D3b (time pressure without permission): all 4 runs wrote failing tests
    first; 3 of those REDs were hidden by the agents' own output filtering
    (capture correction pending the operator audit).
  - **Shared behaviors**, on identical text in both arms:
    - D1: Opus followed a user's "just run this test file" over the skill's
      full-suite rule, and said so.
    - D4: no run asked before changing a configuration file. Sonnet behaved
      the same in `apsp-tdd-001`.
    These are upstream-skill questions, not compaction effects.
- **Usage:**
  - Totals: 581k vs 577k tokens (+0.7%); reported cost $0.60 vs $0.54.
  - Almost all of the difference is D4 (90k vs 73k). Both candidate runs wrote
    a test before changing the config, and both baseline runs edited it
    directly.
  - Those were value-only tests, which the skill's own "no change detectors"
    guidance doesn't count. So the extra work did not produce more correct
    outcomes.
  - Across the other cases the candidate used slightly fewer tokens.
  - At 10 runs per arm none of this is a cost finding.
- **Cost:** children $1.32 (2 smoke + 20 runs), against a $12 ceiling.
- **Not established:** held-out performance, reliability beyond 2 reps, other
  hosts. **Not adopted.**

## Not done / limits

- Haiku 5.5: no candidate (unchanged baseline), so no pair was run.
- `apsp-tdd-001` stage 2 (held-out confirmation) was designed but not funded.
  Discovery delivery was not tested: the AP plugin adapter is unreleased, and
  `--safe-mode` with `--plugin-dir` did not list the skill.
- `apsp-sd-001` was prepared but never run, and was not re-reviewed after
  Ponytail was removed.
- Opus, Sol: not covered by knowledge evidence and not tested.
- The evaluation is single-turn; scripted history replaces a live user. Multi-turn
  gate behavior, builder-check dispatch and visual-companion use were not
  exercised.
- `apsp-bs-001`: one grader per case. `apsp-bs-002`: two blind graders per
  case. Grader judgment is model judgment either way.
- Petrov's results were from Bedrock; these trials used subscription Claude
  Code. The deployments differ.
- Every child context in both experiments included the Ponytail
  SubagentStart instructions and the native Superpowers skill listing. Neither
  was controlled.
- One coordinator designed the treatments and cases, ran both arms and
  graders, and audited the results. There was no independent review.
- `writing-plans` (the next stage after brainstorming) is not packaged. The
  helper scripts were syntax-checked only; their runtime behavior was never
  qualified.
- Both apsp-bs-002 amendments came after execution: Amendment 1 (grader
  budget) and Amendment 2 (identical-file override). The original
  procedural outcome is kept alongside the corrected one.
