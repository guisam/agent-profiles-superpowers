# Model-specific Superpowers skills through Agent Profiles: a maintainer guide

This guide is for a skill maintainer, such as the author of Superpowers, who
wants to propose, distribute and evaluate per-model variants of a skill
**without installing a Superpowers plugin** and **without changing the default
for anyone**. The worked example is `test-driven-development` for
`claude-sonnet-5-5`.

## The problem

One skill text serves every model. A strong model may not need the teaching
of mechanics it already knows, such as worked code examples or a diagram that
restates the steps. It still needs the decision guidance: when to act, what
order to follow, the exceptions, the approval boundaries and the verification
requirements. Cutting the wrong part silently changes policy.

The workflow here lets a maintainer:

1. pick a variant per **exact** model;
2. deliver it through Agent Profiles (AP), with full upstream content as the
   fallback;
3. prove what each model received;
4. compare variant and baseline in a bounded, paired way;
5. collect volunteer evidence without sharing private material.

## What the worked example established, and what it didn't

`apsp-tdd-001` stage 1 is closed. See
[CLOSEOUT](../experiments/tdd-compaction/CLOSEOUT.md).

**The setup:**

- **Candidate:** a compacted `SKILL.md`, 7,025 bytes against 9,578. The cycle
  diagram and three worked examples were removed; every rule, rationalization
  row, red flag and checklist item was kept.
- **Model:** Sonnet 5.5 on headless Claude Code.
- **Suite:** 7 screening cases × 2 arms × 3 reps.

**Findings:**

- **No observed regression in this screening suite,** under the accepted
  adjudication rules: 18/21 vs 18/21, with all 21 paired reps tied.
- **9.31% fewer tokens** in total execution usage (input, cache creation, cache
  read and output, over 21 runs per arm). This is mostly the smaller system
  prompt re-read on every request: 1,134 fewer tokens on the first request.
  Skill size, separately: −2,553 bytes.
- **Integrity evidence, within the tested scope:**
  - the contract review shows every requirement is retained verbatim;
  - the behavioral screening showed both arms behaving the same on test-first
    order, attributable RED, the regression cycle, avoiding mocks, prose
    non-activation and disclosure.
- **Shared gaps:**
  - **R6:** neither arm asked before taking the configuration-file exception
    that the skill says to ask about.
  - **Strict reading of R5:** neither arm kept test-first under explicit
    pressure.
  These describe the base skill on this model, not the compaction. They are
  not evidence that the policy survives.

**Not established:**

- equivalence;
- reliability on other tasks, models or hosts;
- discovery or plugin delivery;
- readiness for adoption.

The held-out confirmation (stage 2) was designed but not funded. The candidate
is **not adopted**; it is an opt-in beta at most.

## Two sources of variants

### A. A historical skill version with evidence

If an older upstream version is known to have worked well with a particular
model, AP can select it for that model:

1. **Package the exact historical bytes from git**, not from a copy:
   - `git -C superpowers cat-file blob <tag>:skills/<skill>/SKILL.md`;
   - the same for every resource;
   - then `git hash-object` against the blob IDs.
   Name it `@ns/<skill>-upstream@<tag>`, and record the commit and blob IDs in
   an `IDENTITIES.json`.
2. **Check compatibility.** Historical availability is **not** evidence of
   suitability.
   - `check_package.py` confirms the references and scripts are present.
   - Every `superpowers:<other-skill>` name must exist in the set the user
     actually has, or be documented as unavailable.
   - Scripts must run on today's platforms.
   - A version older than its sibling skills can cite renamed skills or
     changed formats.
3. **Require evidence for the exact target model:** a paired comparison
   against the current baseline, in the target environment. A version's
   history ("it shipped when model X was current") is a lead, not evidence.
4. **Bind it with a single assignment,** exactly as for a candidate.

In this project the TDD `SKILL.md` is byte-identical from v6.4.1 to v7.0.2
(blob `46838cc9`), so there is no distinct historical TDD version to select.
The mechanism is the same for any skill whose text did change.

### B. A carefully compacted candidate

Use AP's **skill-compaction** skill: AP preset
`examples/presets/skill-compaction` 1.0.5, Apache-2.0, `SKILL.md` sha256
`989b59b9…`. Its rules, applied in this example:

- **Inventory the contract first:** triggers, required states, order,
  exceptions, approval boundaries and verification. Flag contradictions (TDD
  has ten, T1-T10 in
  [CONTRACT.md](../experiments/tdd-compaction/CONTRACT.md)). Don't resolve
  them inside a compaction.
- **The main compression target is execution explanation,** such as worked
  examples and restating diagrams. Keep decision guidance, local knowledge,
  constraints and checks.
- **Label each edit:**
  - **Editorial:** meaning preserved; no capability evidence needed.
  - **Capability-dependent:** "the model can do this without the example".
    These need evidence, or an explicit assumption in an unvalidated candidate.
- **Make the source's intent explicit and testable.** For example, "Fails for
  another reason? Go back to RED" was a condition hidden in the diagram, so it
  became a sentence.
- **Produce a change map:** edit → preserved requirement → evidence →
  evaluation needed ([example](examples/tdd-sonnet-5-5/CHANGE-MAP.md)).

**Petrov's knowledge probes** ([obra/superpowers#2665](https://github.com/obra/superpowers/issues/2665),
measured with Intel's dokimi) are **candidate-generation leads**:

- a passage the model "already knows" is a place to look;
- it is not a deletion instruction;
- knowing a rule does not mean choosing to follow it;
- unprobed text is not proven redundant.

The TDD candidate kept every rationalization row, despite redundancy grades,
because upstream's behavioral evidence shows they matter.

## How AP delivers the selected version (no plugin)

The consumer config binds the skill to the baseline, plus one assignment for
one exact model and role:

```yaml
skills:
  test-driven-development: {package: "@apsp/test-driven-development-upstream", version: "7.0.2"}
assignments:
  sonnet-5-5-candidate:
    when: {model: claude-sonnet-5-5, role: implementer}
    bindings:
      skills.test-driven-development: {package: "@apsp/test-driven-development-sonnet-5-5", version: "0.1.0"}
```

Full files: [examples/tdd-sonnet-5-5/](examples/tdd-sonnet-5-5/). Rollback is
the same config with `assignments: {}`.

### Capabilities verified on AP 0.19.4, the released npm version

Verified locally, with no model calls, by `tools/verify_delivery.py`; the
report is [delivery-report.json](examples/tdd-sonnet-5-5/delivery-report.json):

- **Pinned bytes.** Package bytes match the pinned sha256 values. AP digests
  reproduce: `ce680b8a…` for the baseline, `bd446f96…` for the candidate.
- **Exact-model routing.** `claude-sonnet-5-5` gets the candidate. Haiku 5.5,
  Opus 5.5, the near-miss `claude-sonnet-5`, an unlisted ID and an unstated
  model all get the baseline.
- **Delivered text.** `resolve` output contains the selected `SKILL.md`
  exactly, and never the other arm's.
- **Resources.** `stamp` plus `materialize --adapter filesystem-v1` exports
  the selected package's full tree, byte-identical. `library read` returns each
  resource.
- **Rollback.** Removing the assignment and running `install` returns every
  model to the baseline.
- **Pin isolation** between two consumers, from the first slice
  ([FINDINGS §3](../FINDINGS.md)).

### Demonstrated with models in `apsp-tdd-001`

A launcher appended AP's resolved context to Claude Code's system prompt
(`--append-system-prompt-file`). The per-arm text was confirmed in every
transcript, with the isolation checks of [EVALUATION.md](EVALUATION.md) §2.

### Not demonstrated by this project: gaps, stated plainly

- **Interactive delivery through AP's bootstrap** (a `CLAUDE.md` managed block
  in which the agent runs `resolve` with the model ID the host states). AP
  documents this mode and its own host observations. This project did not
  evaluate it. AP guarantees what `resolve` prints for a stated identity;
  copying the right ID and running the command are agent behavior.
- **Exact-model identification** comes from the host's statement, or the
  launcher's `--model`. AP does not detect or verify which model is running.
  No native host integration ships yet.
- **Native skill discovery** (selecting the skill from its description through
  a plugin export) is untested. The `claude-plugin-v1` adapter exists only on
  an unreleased AP branch. Under `--safe-mode`, `--plugin-dir` did not list the
  plugin's skill.
- **Placing exported resources into a host's skill folder** is host-specific;
  this repo does not automate it.
- **AP issues filed from this work:** #89 (cross-package `update`), #90
  (required-skill package identity in plain `resolve`), #91 (misleading
  `update` error).
- **Cross-skill dependencies** (`writing-skills`, `writing-plans`) are not
  packaged here.

## Running a bounded comparison

See [EVALUATION.md](EVALUATION.md). In short:

1. **Freeze** the cases, fixtures with hidden checks, rubric, reps, seed,
   limits and decision rule.
2. **Preflight both arms** (`tools/preflight.py`). It checks global
   instructions, hooks, duplicate skill installations, other-arm content, the
   environment, and the `init` probe.
3. **Plan** with `tools/campaign.py plan` and run with your own runner. The
   reference Claude Code harness is `experiments/tdd-compaction/tools/tdd_harness.py`.
4. **Score:** deterministic checks first; then two blind graders with
   provenance-based independence; then a human audit before the decision.
   Report official and accepted scores separately, with the accepted
   interpretation as the headline once the gate closes.
5. **Export** one `apsp-results/1` file per configuration
   (`tools/results_format.py validate`).

**Budget reality from the example:**

- children $1.66 and graders $1.06 (API-equivalent, reported by the CLI) for
  46 child and 9 grader runs;
- the coordinator's build-and-run overhead was larger, about 24.7M tokens.

Plan coordinator effort explicitly.

## Beta feedback

See [BETA.md](BETA.md):

- the opt-in;
- rollback;
- controlled campaign submissions (one configuration per report, never
  pooled);
- everyday feedback with the [template](templates/beta-feedback.md).

There are no automatic uploads. Volunteers review everything they share.

## Before promoting a variant

These are the requirements; the full text is in [BETA.md](BETA.md#promotion-what-adopted-would-require):

1. a contract review;
2. screening with no observed regression;
3. a held-out campaign with a stated margin and no unmatched approval failure;
4. a recorded human decision, scoped to model, host and route.

Until then the variant is opt-in only, and full upstream content stays the
default.

## Credits and boundaries

- **Superpowers** is by Jesse Vincent (obra), MIT. Every package keeps the
  upstream `LICENSE`.
- **Knowledge probes:** Nikolay Petrov (@napetrov), measured with Intel's
  **dokimi**. The dataset has no license, so it is linked and summarized, never
  copied ([PROVENANCE.md](../PROVENANCE.md)).
- **Agent Profiles and the skill-compaction preset** are Apache-2.0.
- The behavioral results are this project's own. None of the people or
  organizations above reviewed or endorsed this work.
