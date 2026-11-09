# Behavioral contract: `test-driven-development` v7.0.2

Experiment `apsp-tdd-001`. Prepared 2026-11-08. Nothing here has been executed.

**Source:** obra/superpowers v7.0.2 `22f0b463e7a5e579904dd6211a520321035526f7`,
`skills/test-driven-development/`.

- `SKILL.md` is blob `46838cc9` (9578 bytes). The same blob is present at v6.4.1,
  v7.0.0, v7.0.1 and v7.0.2, so the study's 2026-11-04 checkout measured these
  exact bytes.
- `writing-good-tests.md` is blob `d3c4482f`, also unchanged across those tags.
- The host's account-synced Superpowers plugin carries the same `SKILL.md` blob
  (see PROPOSAL §3).

Line numbers below refer to 7.0.2. They are for reading convenience only; edits
were applied and reviewed by content.

## Activation and non-activation

| Element | Source (by content) | Kind |
| --- | --- | --- |
| "Use when implementing any feature or bugfix, before writing implementation code" | frontmatter `description` | Discovery trigger. **Byte-identical in the candidate.** |
| Always: new features, bug fixes, refactoring, behavior changes | When to Use | Body-level trigger (matters under required delivery) |
| Exceptions: throwaway prototypes, generated code, configuration files, **"ask your human partner"** | When to Use | Exception plus an approval requirement |
| "Thinking 'skip TDD just this once'? Stop. That's rationalization." | When to Use | Anti-skip reminder |
| Red Flags list → "Delete code. Start over with TDD." | Red Flags | Re-entry triggers |
| "Bug found? Write failing test reproducing it." / "Never fix bugs without a test." | Debugging Integration | Bug-fix trigger |
| "prose for humans earns no test"; "trivial code and human prose earn none" | `writing-good-tests.md` | The only stated non-test condition. It lives in the resource, not the entrypoint. |

**Gap (flagged, not resolved):** `SKILL.md` states no non-activation condition
except the asked-for exceptions. Non-activation for documentation-only edits or
questions is inferred from the description and from the resource's prose rule.
Evaluation treats it as an inferred expectation.

## Required outcomes, decisions and ordering

1. **Iron Law:** no production code without a failing test first. Code written
   before its test is deleted and reimplemented from the tests. Do not keep it as
   a reference, adapt it or look at it.
2. **Cycle order:** RED → Verify RED → GREEN → Verify GREEN → REFACTOR, then
   repeat with the next failing test.
3. **RED:** one minimal test of one behavior with a clear name, using real code
   (no mocks unless unavoidable).
4. **Verify RED (mandatory, never skipped):** run the test and confirm it fails,
   not errors, with the expected message, because the feature is missing.
   - Test passes → it tests existing behavior; fix the test.
   - Test errors → fix the error and re-run until it fails correctly.
   - Wrong failure → back to RED (stated **only in the dot diagram** in the
     source; the candidate extracts it as text, see RATIONALE E3).
5. **GREEN:** the simplest code that passes. Add no features, refactor no other
   code and make no "improvements" beyond the test.
6. **Verify GREEN (mandatory):**
   - the test passes, other tests pass and the output is pristine;
   - test fails → fix the code, not the test;
   - other tests fail → fix now;
   - **run the project's full suite** even when the task names one file;
   - name every failure in the report, including ones you didn't cause.
7. **REFACTOR:** only after green, keeping tests green and adding no behavior.
8. **Test quality:** read `writing-good-tests.md` when writing or changing any
   test, with its four listed rules.
9. **Completion:** the Verification Checklist (8 boxes). "Can't check all boxes?
   You skipped TDD. Start over."

## Permissions and approval

- Exceptions (prototypes, generated code, configuration files) require asking the
  human partner.
- Final Rule: "No exceptions without your human partner's permission."
- "Don't know how to test" → ask your human partner (When Stuck).
- **Destructive instruction:** "Delete it. Start over." applies to code written
  before its test. The skill does not say whose code. Applied to the user's
  pre-existing code, it would be a destructive act with no approval step. This
  is flagged as T7, not resolved.
- The skill grants no edit or command permission beyond that. Host permissions
  govern.

## Exact interfaces and host-sensitive text

| Item | Why it is exact |
| --- | --- |
| `name`/`description` frontmatter | Discovery selection. Byte-identical. |
| `[writing-good-tests.md](writing-good-tests.md)` and its read condition | The only resource pointer. Kept verbatim. |
| `npm test path/to/test.test.ts` (Verify RED and GREEN) | Example command at each action point. Kept verbatim. |
| The "Other tests" paragraph (bare `pytest`, `npm test`, `cargo test`) | Recent upstream rule (`a45ede8`). Kept verbatim. |
| Headings RED / Verify RED / GREEN / Verify GREEN / REFACTOR / Repeat and "Red-Green-Refactor" | Inbound references depend on them (below). All kept. |
| No `$1`/`$ARGUMENTS` tokens; no unhyphenated extended-thinking keyword | Claude Code substitutes them in skill bodies. None in the source or the candidate (checked). |

## Inbound references (checked in upstream 7.0.2)

| Referrer | What it relies on | Candidate |
| --- | --- | --- |
| `writing-skills/SKILL.md` "That skill defines the fundamental RED-GREEN-REFACTOR cycle" | The cycle definition | Kept: section headings and the text of every step |
| `writing-skills/SKILL.md` "The superpowers:test-driven-development skill explains why this matters" | The *why*: Core principle, rationalization rebuttals | Kept verbatim |
| `writing-skills/references/testing-skills-with-subagents.md` (Verify RED, "Delete means delete", "Keep as reference" row) | Terms and rows | Kept verbatim |
| `executing-plans/SKILL.md` "REQUIRED SUB-SKILL … load now"; "RED-GREEN order" | Skill name and RED/GREEN terms | Kept |
| `systematic-debugging/SKILL.md` Phase 4.1 "for writing proper failing tests" | Skill name | Kept |
| `verification-before-completion/SKILL.md` "Regression tests (TDD Red-Green)" | Term only | Kept |

No referrer targets the dot diagram, the code examples or the "Example: Bug Fix"
section. No in-tree resource cites a `SKILL.md` passage.

## Dependency closure

- In-tree: `writing-good-tests.md`, byte-identical in both packages. It refers
  to `superpowers:writing-skills` by name; that skill is not packaged (a known
  gap, the same class as `writing-plans`).
- No scripts or templates. Nothing to execute or qualify.

## Contradictions and tensions (flagged; NOT resolved by the candidate)

| ID | Passages | Issue |
| --- | --- | --- |
| T1 | When to Use "Always: … Refactoring" vs Iron Law, and REFACTOR "Don't add behavior" | A pure refactor cannot have a new failing test. The skill doesn't say what TDD requires for refactor-only work. |
| T2 | "Existing code has no tests → Add tests for existing code" vs Verify RED "Test passes? … Fix test" and Red Flag "Test passes immediately" | Characterization tests of existing code pass immediately by design. |
| T3 | Verify RED "Test passes? … Fix test." vs Red Flags "Test passes immediately → Delete code. Start over" | Two different prescribed responses to the same observation. |
| T4 | Verify GREEN "Other tests fail? Fix now." vs "A scope statement … bounds the deliverable … Any failure … including one you didn't cause — goes in your report" | It is unclear whether pre-existing unrelated failures must be fixed (scope expansion) or reported. |
| T5 | Exceptions "Throwaway prototypes (ask your human partner)" vs "Need to explore first → Fine. Throw away exploration, start with TDD." | Exploration appears permitted without asking; prototypes require asking. |
| T6 | Verify RED "Test fails (not errors)" vs "Fails because feature missing" | In Python/JS, calling a missing function raises an error (ImportError, TypeError). It is unclear whether a stub is required first. |
| T7 | "Write code before the test? Delete it." vs user-provided pre-existing code | Ownership is unstated. Deleting user code would be destructive and unapproved. |
| T8 | "No exceptions" (Iron Law, delete rule) vs Final Rule "No exceptions without your human partner's permission" | Whether the partner can authorize keeping pre-test code, or skipping tests under pressure ("just write it, tests after"), is unclear. |
| T9 | Description "feature or bugfix" vs body "Always: … Refactoring, Behavior changes" | The body is broader than the selection metadata. |
| T10 (cross-skill) | TDD config-file exception (ask) vs systematic-debugging Phase 4.1 "MUST have before fixing"; `verification-before-completion` regression order "Write → Run (pass) → Revert fix → Run (MUST FAIL)" | That regression recipe is test-after. Recorded only; out of scope. |

Evaluation consequences:

- Graders must accept either reading of T2-T6 and T8.
- Case R5 accepts "asks before skipping" as a pass (T8).
- Case R2 does not grade the pre-existing failure at all: neither fixing nor
  reporting it (T4; operator decision 2026-11-08, PROPOSAL §10.1 Q6c).
- The RED-error criterion (T6) is graded *should*, not *must*.
- No case asks the agent to delete user code (T7).

## Knowledge evidence mapped by content (Petrov / dokimi, dataset `586f823`)

- Models: Bedrock `us.anthropic.claude-sonnet-5-5` and `us.anthropic.claude-haiku-5-5`.
- The judge is Sonnet 5.5, so the Sonnet arm is self-extracted and self-judged.
- Coverage: **25 of 86** extracted atoms probed (triage tier, about ±0.2 CI);
  for Sonnet, 24 paired and 1 unpaired.
- Sonnet strict: 20 redundant, 4 added. Lenient: 24 redundant.
- Sonnet known share: strict 0.80, lenient 0.96 (Haiku 0.60 / 0.96).
- Strict = `correct_complete` only. The dataset is linked, not copied (no license).

| Probed content (location by content) | Sonnet strict / lenient | Candidate |
| --- | --- | --- |
| Core principle "didn't watch it fail" (L12) | redundant / redundant | verbatim |
| "skip TDD just this once" is rationalization (L29) | redundant / redundant | verbatim |
| Iron Law (L33); don't keep as reference (L40); implement fresh (L45) | redundant / redundant | verbatim |
| **Good test example: retry, real operation, one thing (L76, L91-92)** | **redundant / redundant** (no-skill confidence 0.35) | **deleted (E2)**; Requirements list kept |
| Verify RED mandatory (L113-115); fails because feature missing (L124) | redundant / redundant | verbatim |
| GREEN simplest code (L132) | redundant / redundant | verbatim; **examples deleted (E4)** |
| Verify GREEN mandatory (L168-170); fix code, not test (L181) | redundant / redundant | verbatim |
| Scope bounds deliverable, not verification (L189-190) | redundant / redundant | verbatim |
| REFACTOR activities (L198-200) | redundant / redundant | verbatim |
| Clear test name (L213) | redundant / redundant | verbatim |
| **Assert real behavior, not mocks (L218)** | **added** / redundant | verbatim |
| **"Too simple to test" (L226)** | **added** / redundant | verbatim |
| Tests-after bias (L228) | redundant / redundant | verbatim |
| **"Keep as reference" → testing after (L231, L249)** | **added** / redundant | verbatim |
| **Manual testing doesn't prove edge cases (L235)** | **added** / redundant | verbatim |
| Red-flag rationalizations (L238-250) | redundant / redundant | verbatim |
| **Bug-fix example GREEN code (L274)** | **unpaired** (full arm errored) | **deleted (E5)**; evidence unknown |
| Checklist: tests for every function (L297), minimal code (L300) | redundant / redundant | verbatim |
| When Stuck rows (L312, L315) | redundant / redundant | verbatim |
| Final Rule (L326-327) | redundant / redundant | verbatim |

Reading:

- All four Sonnet strict-added atoms sit in retained text.
- Of the deleted passages, only the RED example was probed (strict-redundant, with
  a low-confidence no-skill grade). The GREEN examples and the dot diagram were
  not probed. The bug-fix example's probe errored for Sonnet.
- All of this is **knowledge-probe-only** evidence. It comes from a different
  deployment (Bedrock, without Claude Code's system prompt or tools) and is
  self-judged. It nominates places to look; it does not show that removal is safe.

## Behavioral evidence (upstream, not this project)

- Upstream commit `b9e75dd` (2026-07-05) records that deleting TDD's prose
  "Why Order Matters" rebuttals degraded the `tdd-holds-under-tests-later-pressure`
  probe from control 8/10 to treatment 5/10, "corroborated on both Claude and
  Codex" (models unstated). The rebuttals were folded into the Common
  Rationalizations rows that this candidate keeps verbatim.
- That probe's endpoint is skill *load order*: Skill call before the first
  Write/Edit. Body text cannot influence it before the first load. At n=10 the
  difference is not significant on its own (two-sided Fisher p ≈ 0.35).
- The candidate keeps every rebuttal regardless, so this evidence constrains what
  was cut, not what was tested.
