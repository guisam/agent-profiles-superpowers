# `apsp-tdd-001` stage 2: confirmation proposal (DRAFT r1, not approved, not frozen)

> **Status (2026-11-08): NOT FUNDED, NOT RUN.** The project moved to the reusable
> framework in `workflow/`. This design is kept as the template for controlled
> campaigns (`workflow/EVALUATION.md`). No held-out cases were authored and nothing
> was frozen or executed. See [../CLOSEOUT.md](../CLOSEOUT.md).

Prepared 2026-11-08. **Nothing here has been run.** There have been no model
calls, no case authoring and no freeze. The candidate is unchanged.

Preconditions:

- **(a) Met (2026-11-08):** the stage-1 human gate is closed, and the official
  `decide` is PROCEED.
- **(b) Met:** HUMAN-GATE items 4 and 5 are answered and applied in §6.
- **(c) Open:** separate approval of this proposal and its budget.
- **(d) Open:** independent authorship of the held-out cases
  (`AUTHORING-BRIEF.md`).

## 1. What stage 2 should establish

The claim to test is narrow: **"no regression beyond a practical margin was
observed for `claude-sonnet-5-5` in this environment, on held-out tasks."** It
is not a test of equivalence, benefit, or other models.

Stage 1 cannot support even that claim:

- 3 repetitions give a ±20 pp interval on the pooled difference;
- 2 of 7 cases were floor or capture-affected;
- every informative case was at ceiling in both arms.

## 2. Candidate and arms

- **Candidate:** `@apsp/test-driven-development-sonnet-5-5@0.1.0` (AP
  `bd446f96…`), **unchanged**. The stage-1 audit motivates no edit:
  - every discrepancy was either shared by both arms (R5, R6 approval) or an
    artifact (R2 capture, R3 fixture);
  - the R5/R6 behavior comes from text that is byte-identical in both arms,
    so it is a base-skill question, out of scope for a compaction candidate.
  - If a future edit is proposed, it gets a new version (0.2.0). That version
    must repeat the development checks: the invariants (frontmatter, retained
    sections, references), the AP digest, a stage-0 smoke, and a stage-1
    screening on the **screening** cases only. It must never be tuned on
    held-out cases.
- **Baseline:** `@apsp/test-driven-development-upstream@7.0.2` (`ce680b8a…`).
- **Model:** `claude-sonnet-5-5`, effort medium. No substitution.

## 3. Delivery path

**R-block (required delivery): the same route as stage 1.**

- AP 0.19.4 `resolve --host claude --identity-source host-stated --model
  claude-sonnet-5-5 --role implementer` in two disposable consumers.
- Opaque aliases, with fresh aliases and a fresh key for stage 2.
- The "Run again" section is stripped, then the result is frozen as
  `context-<arm>.md` and delivered with `--append-system-prompt-file`.
- `writing-good-tests.md` sits at `../skill/` and is byte-identical across arms.

The results qualify only "AP-resolved, required, appended to the system prompt,
safe-mode headless host".

**D-block (discovery): separate and optional.** It runs only if **both** of
these hold:

- AP ships `claude-plugin-v1` in a release, or the operator approves the
  unreleased branch for trial use;
- isolation is proven with a throwaway `CLAUDE_CONFIG_DIR` and an operator
  `claude setup-token`. Stage 1 showed that `--safe-mode` plus `--plugin-dir`
  lists 17 built-in skills and not the plugin's skill.

If either fails, discovery stays **untested** and is reported that way. It is
budgeted separately (§9) and never pooled with the R-block.

## 4. Held-out cases (authored independently; the coordinator does not author them)

The coordinator designed the screening suite and has seen all stage-1
behavior, so the coordinator does not write the held-out tasks. Per
`AUTHORING-BRIEF.md`, the author is either the operator or a fresh agent that
is given only CONTRACT.md, the **baseline** `SKILL.md`,
`writing-good-tests.md` and the brief. Using a fresh agent is one more model
call and needs approval.

The author must not see:

- CASES.draft, the stage-1 fixtures, results or audit;
- RATIONALE.md;
- the candidate `SKILL.md`.

**Required coverage (10 cases):**

| Slot | Kind | Purpose |
| --- | --- | --- |
| H1 | bug fix, Python | regression test first; mutation-checked |
| H2 | bug fix, Node | as H1, with the other toolchain |
| H3a | pressure **with** explicit permission to skip tests | T8 second reading, scored per HUMAN-GATE item 4 |
| H3b | time pressure **without** permission to skip | strict reading: test-first, or ask |
| H4 | configuration exception | the change has observable behavior, so a behavior test is possible; scoring per item 5 |
| H5 | real vs mock | a real in-memory collaborator exists next to a tempting external-looking dependency |
| H6 | refactor-only | T1: no behavior change; keep the suite green before and after |
| H7 | characterization of untested code | T2: tests that pass immediately are legitimate |
| N2 | negative control: prose/config-free docs edit | no tests created |
| N3 | negative control: explanation-only question | no file changes |

There are 8 behavioral cases (H1-H7, counting H3a and H3b separately) and 2
negative controls.

**Acceptance checks before freeze** (no model calls):

- every hidden assertion is mapped to a request clause (a "contract lint");
- each fixture has a good, a bad and an **alternative-valid** reference
  solution. The alternative-valid solution must pass; this is what would have
  caught the R3 tuple defect.
- the operator (or a second reviewer) signs off the lint.

## 5. Runs, order and repetitions

- **Repetitions: 12 per arm per case.** That is 10 × 2 × 12 = **240 analyzed
  runs**, 96 per arm on the 8 behavioral cases.
- **Why 12:** at the stage-1 pass level (p ≈ 0.85):

| Reps per arm per case | 95% half-width, pooled diff | P(clear −15 pp margin \| no true difference) | P(detect a true −20 pp drop) |
| --- | --- | --- | --- |
| 3 (stage 1) | ±0.20 | 0.31 | 0.38 |
| 10 | ±0.11 | 0.76 | 0.85 |
| **12** | **±0.10** | **0.83** | **0.91** |
| 20 | ±0.08 | 0.96 | 0.99 |

- **Order:** serial, one process at a time.
  - **Case order:** each rep runs the cases in a seeded shuffle (new seed).
  - **Arm order:** counterbalanced within each case: 6 reps full-first and 6
    reps candidate-first, assigned by a seeded balanced design.
  - Each run gets a fresh process and a fresh fixture copy.
- **Single turn, no continuation.** A run that ends with a question is final.

## 6. Scoring and evidence

**Objective checkers first** (harness 2.3.0, §8).

- M criteria per case: test-first order, RED attributable to the new test, the
  mutation check (bug fixes), hidden tests, the full suite after the last
  change, scope, and approval.
- RED must be shown in two ways:
  1. a failing run between the first test edit and the first production edit;
     **and**
  2. attribution: the run's output, or an offline replay of the RED-time test
     files against the original code, implicates the new test.
- An outcome that can't be parsed stays `unknown`. It is never counted as a
  pass or a fail, and is always audited.

**Gr1 (claims match evidence), on the 8 behavioral cases:**

- **Packets:**
  - the full ordered tool events;
  - each command with its exit status and parsed outcome;
  - test output up to 200 lines per run (head 60 + tail 140, with an explicit
    elision marker and the line count);
  - diffs of the test and production files.
  - **No 12-line tails.**
- **Bundles:** 2 per case of 12 packets (6 per arm, shuffled, opaque IDs),
  giving 16 bundles.
- **Graders:** 2 blind `claude-opus-5-5` graders per bundle, 32 runs.
- **Independence** is established by execution provenance, not by different
  output bytes:
  - separate sessions;
  - each grade file equals its own session's Write;
  - neither session read the other's output.
  Identical files are allowed.
- **Disagreements:** a criterion passes only if both graders pass it. Every
  disagreement goes to the human audit, and the adjudicated result is reported
  next to the official one. Disagreement is never a reason to re-run a grader.

**Approval scoring, fixed by the operator at the stage-1 gate (2026-11-08):**

- **H3a, explicit permission to skip tests:** the **permission reading**
  (HUMAN-GATE item 4).
  - M passes if the agent follows the instruction and discloses that tests
    were skipped. Test-first or asking also passes.
  - M fails if it skips silently.
  - The strict reading is reported as a secondary, descriptive measure only.
- **H3b, pressure without permission:** strict. Test-first, or ask before
  departing from it.
- **H4, configuration exception** (HUMAN-GATE item 5):
  - M passes if the agent **asks** before taking the exception, or writes a
    **failing behavior test** first.
  - A value-only test (a change detector) fails M and is reported as its own
    category.
  - A silent configuration edit fails M.

## 7. Decision rule (frozen before any run)

Apply in order; the first rule that holds decides the outcome.

1. **VOID:** setup-invalid runs exceed 10% of the slots.
2. **INCONCLUSIVE:** any slot is missing, or the human audit is pending.
3. **REGRESSION:** any of:
   - the pooled behavioral all-M difference (cand − control) has a 95% Newcombe
     interval whose **upper bound is below 0**;
   - H3b or H4 has candidate approval failures exceeding control's by ≥ 3 of 12
     (after audit);
   - a negative control (N2/N3) has candidate failures exceeding control's by
     ≥ 3 of 12.
4. **FRICTION:** either of:
   - pooled median tool calls above 1.25 × control;
   - more question-only replies than control on non-approval cases, by ≥ 3.
5. **NON-INFERIOR (no regression beyond 15 pp observed):** the interval's
   lower bound is above −15 pp, and none of the above holds.
6. Otherwise **INCONCLUSIVE**.

**Watch items:** any case where the candidate is ≥ 4 of 12 below control.

- False-alarm rate 1-4% per case at p 0.8-0.9.
- Each one is audited and named in the report. It is not a stop on its own.

**Usage:** the candidate's total tokens above 110% of control turns
NON-INFERIOR into INCONCLUSIVE. Skill size and execution usage are reported
separately, by category, with missing usage reported as missing.

**Sensitivity:**

- the case-clustered result: the per-case paired sign of differences;
- the result excluding any case the audit marks as fixture- or capture-defective.

Reported beside the official outcome, never replacing it.

**Adoption is never automatic.** NON-INFERIOR allows only a recommendation for
human decision, limited to "no regression beyond 15 pp observed in 8 held-out
behavioral cases for Sonnet 5.5 in the stated environment".

## 8. Harness 2.3.0 (each change needs tests, a selfcheck and smoke before freeze)

1. **Outcome parsing:**
   - recognize per-test markers (`✔`/`✖` with test names, `ok`/`not ok`,
     unittest `FAIL:`/`ERROR:`/`OK`);
   - recognize assertion blocks when the runner summary was removed by the
     agent's `grep`/`tail`;
   - development check: recover R2's outcomes from the stage-1 streams.
     Stage-1 data is used for development only; its official scores never
     change.
2. **RED attribution:** an offline replay of RED-time test files, with the
   final files only where none changed after RED, as in the stage-1 audit.
3. **Full-evidence grader packets** (§6).
4. **Fixture contract lint and alternative-valid references** (§4).
5. **Pause rules fixed from the start:** only unmatched approval or scope
   failures pause (the Amendment-2 standard). Every approval-case run is
   logged for audit.
6. **Audit-packet and agent-audit tools** are promoted from stage 1:
   `audit_dump`, `audit_symmetry`, `audit_red_replay` and `audit_usage`, with
   tests.

The 2.2.2 stage-1 artifacts and freezes stay unchanged.

## 9. Failures, retries, pauses, amendments

- **Setup-invalid** (collector-computed): `init` mismatch, a context hash
  mismatch, a missing stream or transcript, a crash, a host or usage-limit
  error, or repository access.
  - Retry ≤ 1 per slot and ≤ 12 in total (5%).
  - Never retried: wrong behavior, questions, budget-cap hits, timeouts with
    model output.
- **Usage limit:** stop, record the event, wait for the reset, and resume
  from the ledger with identical settings.
- **Stops:** Ponytail or any unexpected plugin, skill or hook in `init`;
  repository access; a destructive command outside the run directory; an
  unmatched approval failure (operator review).
- **Amendments:**
  - after the first dispatch, only operational changes (pause and resume), as
    numbered amendments;
  - any scoring change after dispatch is post-hoc and reported beside the
    official result.

## 10. Budget (estimates; API-equivalent; billed against subscription allowance)

Stage-1 measured costs:

- children $0.034 per run (42 runs);
- graders $0.123 per run (8 runs);
- coordinator about 24.7M tokens for the build-and-run window (≈ $9 at
  unverified list rates).

Stage-2 tasks are larger (refactor, characterization) and the packets are
larger.

| Item | Runs (max) | Per-run estimate | Estimate | Hard ceiling |
| --- | --- | --- | --- | --- |
| Smoke (2 cases × 2 arms, new harness) | 4 + 2 retries | $0.05 | $0.30 | `--max-budget-usd 0.50` → $3 |
| R-block children | 240 + 12 retries | $0.04-0.07 | $10-18 | $0.50 cap → $126 |
| Gr1 graders | 32 + 4 re-runs (invalid output only) | $0.20-0.35 (larger packets) | $7-13 | $1.50 cap → $54 |
| Held-out authoring (fresh agent, if chosen) | 1-2 | $1-3 | $1-3 | $5 |
| Coordinator (harness 2.3.0 + tests, 10 fixtures with lint and references, dispatch, collection, audit) | n/a | measured from transcript | 30-60M tokens ≈ $12-25 | **stop and report at 60M tokens** |
| **Stage-2 R-block total** | | | **≈ $30-60** | children + graders + authoring ≤ **$188** |
| Optional D-block (2 cases × 2 × 12, after its prerequisites) | 48 + 3 | $0.04 | $2-3 + setup | $0.50 cap → $26 |

- **Time:** about 1-2 hours of serial child execution, plus grading.
- **Rates:** the dollar rates are the proposal's 2026-10-06 list rates and are
  **not re-verified**.

## 11. Approval needed before any stage-2 work beyond this document

1. ~~Close the stage-1 human gate, with HUMAN-GATE items 4 and 5 answered.~~
   Done, 2026-11-08.
2. Approve this proposal: reps, decision rule, budget.
3. Choose the held-out author: the operator, or a fresh agent (one more model
   call).
4. D-block: pursue the prerequisites, or leave discovery untested.
