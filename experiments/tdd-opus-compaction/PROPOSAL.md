# Optional validation proposal: Opus 5.5 TDD candidate (DRAFT, not approved, not run)

This document makes no model calls, freezes nothing, and authorizes no
spending. Each tier below needs **separate approval**. It is deliberately much
smaller than the unfunded `apsp-tdd-001` stage-2 design.

## What to test, in priority order

| Priority | Assumption | Why it matters |
| --- | --- | --- |
| 1 | H2: minimal GREEN without the YAGNI example | A judgment gap. Even Sonnet's screening could not distinguish it (all runs added extras in both arms) |
| 2 | H3: the bug-fix regression cycle without the worked example | Execution; the most common real use |
| 3 | H1: real, single-behavior tests without examples | Knowledge/execution |
| 4 | H5: compliance under pressure is unchanged | Rebuttals are kept, so the expected risk is low, but it is consequential |
| 5 | H4: runs the project's own runner without placeholder commands | Low risk |

Every tier also observes the shared contract behaviors, scored with readings
**declared before running**:

- **Explicit permission to skip testing vs pressure without permission:** the
  permission reading for the former, the strict reading for the latter.
- **Meaningful failing tests:** the RED is attributable to the new behavior.
  Assertion vs import error is reported, not scored (T6).
- **Configuration behavior:** ask, or a failing behavior test; value-only
  tests are reported separately.
- **Verification:** the full suite after the last change, with failures named.
- **Competing instructions:** for example, "only run `test/x.test.js`" vs the
  V8 full-suite rule.

## Tiers

**Tier A: knowledge probes without the skill.** Opus answers questions about
the omitted content (examples, YAGNI, the regression cycle, test naming) with
no skill loaded. This measures knowledge only. It never justifies a cut on its
own.

- 8 single-turn prompts × 1 sample each = **8 calls**.
- Grading is deterministic where possible (key facts present). Otherwise the
  operator reads them; there is no model grader.

**Tier B: execution with concise direction.** A one-sentence instruction
("test first, watch it fail, minimal code, then run the full suite"), no skill,
on 2 small tasks: a bug fix and a feature. This shows whether Opus can execute
the procedure without the omitted guidance.

- 2 tasks × 2 reps = **4 runs**.

**Tier C: smoke comparison, full upstream vs candidate** (the smallest useful
behavioral comparison):

- **Cases:** 4 *development* cases. They are fresh fixtures, but they're
  informed by stage 1, so they don't count as held-out:
  1. **D1, bug fix (Node):** the user says "just run the cart test". This
     checks H3, V8 and competing instructions.
  2. **D2, feature with an invitation to add options "later":** checks H2.
  3. **D3, explicit permission to skip tests vs D3b, pressure without
     permission:** one case with two messages, checking T8 and H5.
  4. **D4, a configuration flag with an observable behavioral effect:** checks
     A3 and the behavior-vs-value test distinction.
- **Runs:** 5 messages (D3 has two) × 2 arms × 2 reps = **20 runs**, plus 2
  setup-smoke runs and ≤ 2 retries, for at most **24 child runs**.
- **Delivery:** AP 0.19.4 `resolve` for `claude-opus-5-5`, appended exactly as
  in stage 1. The same isolation flags. `preflight.py` and the `init` probe
  run for both arms.
- **Scoring:** deterministic checkers only, then the operator's audit of every
  candidate failure and every approval-case run. **0 grader calls.**
- **Outcome language:** "no difference observed in N development runs" or
  "candidate-only failures in X". Never "validated". A confirmation would need
  fresh held-out cases.

## Harness requirements (lessons from `apsp-tdd-001`; freeze before any run)

- **Outcome parsing:** read the runner's summary *and* per-test markers
  (`✔`/`✖`, `FAIL:`/`OK`, assertion blocks). Anything else is `unknown` and
  always audited. This is the R2 lesson.
- **Contract-linted fixtures:** each hidden assertion is mapped to a clause of
  the request, and each fixture has a good, a bad and an **alternative-valid**
  reference solution. This is the R3 lesson.
- **Complete evidence:** full test output, exit status, the final diff, and
  usage by category, with missing values recorded as missing.
- **Frozen in advance:** scoring readings (permission vs strict; behavior vs
  value tests), pause rules (only unmatched approval failures pause), retry
  rules (setup faults only) and the decision language.
- **Development cases stay development cases.** Any later confirmation uses
  newly authored held-out cases.

## Budget (estimate, API-equivalent; subscription allowance; needs approval)

**Assumptions:**

- An Opus run costs about 2-3× a Sonnet run. Stage 1 measured Sonnet at $0.034
  per run.
- The list rates are not re-verified.

| Tier | Calls | Estimate | Hard ceiling |
| --- | --- | --- | --- |
| A probes | 8 | ≈ $0.10 | $1 |
| B execution | 4 | ≈ $0.30-0.50 | $2 (`--max-budget-usd 0.50`) |
| C smoke | ≤ 24 | ≈ $1.60-2.50 | $12 (`--max-budget-usd 0.50`) |
| Coordinator (fixtures, harness fixes, audit) | n/a | a few million tokens, measured from the transcript | not enforceable; report it |
| **Total A + B + C** | **≤ 36 model calls** | **≈ $2-3** | **$15** plus coordinator |

The smallest useful step is **tier C alone**, about $2. Tiers A and B are
optional diagnostics, worth running only if tier C shows candidate-only
failures.
