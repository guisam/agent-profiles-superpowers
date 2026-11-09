# Behavioral contract: `systematic-debugging` v7.0.2

Experiment `apsp-sd-001`. Prepared 2026-11-08. Nothing here has been executed.

Source: obra/superpowers v7.0.2 `22f0b463e7a5e579904dd6211a520321035526f7`,
`skills/systematic-debugging/SKILL.md` blob `62fc752a` (9530 bytes). The same
blob is present at v7.0.0 (`bb92a77`), v7.0.1 (`2ce8aa1`) and v7.0.2, so the
study's 2026-11-04 checkout almost certainly measured these exact bytes. That
is stronger than the brainstorming mapping, whose file changed in 7.0.2.

Line numbers below are 7.0.2 lines, given for reading convenience only. Edits
are applied and reviewed by content.

## Activation and non-activation

| Element | Source | Kind |
| --- | --- | --- |
| Selection metadata: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes" | frontmatter | Discovery trigger. **Unchanged in the candidate.** |
| Use for ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues | When to Use | Body-level trigger (matters when the skill is always delivered) |
| Especially under time pressure, when one quick fix seems obvious, after multiple or failed fixes, when the issue isn't fully understood | When to Use | Trigger reinforcement |
| Don't skip when the issue seems simple, you're in a hurry, or a manager wants it fixed now | When to Use | Anti-skip trigger |
| Red flags and partner phrases ("Stop guessing", "Ultra-think this", ...) mean STOP and return to Phase 1 | Red Flags, partner signals | Re-entry triggers |

**Gap (flagged, not resolved):** the skill states no non-activation conditions.
Non-activation (feature work, conceptual questions) is inferred from the
description only. Evaluation treats it as an inferred expectation, not a
stated rule.

## Required outcomes, decisions and ordering

1. **Iron Law:** no fixes without root-cause investigation first. Phase 1 must
   be complete before proposing fixes.
2. **Phase order:** complete each phase before the next (1 root cause,
   2 pattern, 3 hypothesis, 4 implementation).
3. Phase 1 decisions:
   - read errors, warnings and stack traces completely;
   - reproduce; **if not reproducible, gather more data, don't guess**;
   - check recent changes;
   - **when multiple components:** instrument each boundary *before proposing
     fixes*, run once, then analyze, then investigate the failing component;
   - **when deep in the call stack:** trace backward and fix at the source.
     The full technique is in `root-cause-tracing.md`.
   - Success criterion: understand WHAT and WHY. *(Stated only in the Quick
     Reference table in the source.)*
4. Phase 2: find working examples; read a reference implementation completely
   before applying a pattern; list every difference; understand dependencies.
5. Phase 3: one written, specific hypothesis; smallest change, one variable;
   **worked → Phase 4; didn't → new hypothesis, no fixes on top**; when you
   don't know, say so, don't pretend, ask for help, research more.
6. Phase 4, in order:
   1. a failing test case is **required before fixing**: automated if
      possible, a one-off script if there is no framework, using
      `superpowers:test-driven-development`;
   2. a single fix addressing the root cause: one change, no "while I'm here"
      improvements, no bundled refactoring;
   3. verify the test passes, no other tests broke, and the issue is
      resolved, using `superpowers:verification-before-completion` before
      claiming success;
   4. if the fix fails: STOP and count. < 3 → back to Phase 1. ≥ 3 → step 5.
      No fix #4 without architectural discussion.
   5. after 3+ failures: question the architecture and **discuss with your
      human partner before attempting more fixes**.
7. "No root cause" exit: only after completing the process. Document what was
   investigated, implement handling (retry, timeout, error message), add
   monitoring/logging. "95% of 'no root cause' cases are incomplete
   investigation."

## Permissions and approval

- The only approval boundary is Phase 4 step 5: discuss with the human partner
  before more fixes after 3+ failures. Phase 3 step 4 directs asking for help
  when you don't understand.
- The skill grants no edit, command or publication permission and withholds
  none beyond that. Host permissions govern.

## Exact interfaces and host-sensitive text

| Item | Why it is exact |
| --- | --- |
| `name`/`description` frontmatter | Discovery selection. Byte-identical in the candidate. |
| `superpowers:test-driven-development`, `superpowers:verification-before-completion` | Cross-skill names. Not packaged here (see dependency closure). |
| `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md` "in this directory" | Resource pointers. These are the only links to the last two files. |
| "see Phase 4.5" (Red Flags) and "(step 5 below)" | Internal numeric references. Phase/step numbering must not change. |
| "Ultra-think this" (hyphenated) | Deliberate: without the hyphen, the word trips Claude Code's extended-thinking keyword scanner on every session that loads the skill (upstream #1283, commit `90e1721`/#1558). No edit may remove the hyphen. |
| No `$1`/`$ARGUMENTS`-style tokens | Claude Code substitutes them in skill bodies invoked with arguments (upstream #2311/#2361). The source has none outside the removed example's `$IDENTITY`/`$APP`. |
| Secret-safe diagnostic example | v7.0.1 fixed the example so it reports only whether `IDENTITY` is set; the old lines printed the value (#2375/#2380). This is a condition hidden in an example. |

## Verification and failure handling

- Verify fix: test passes, no other tests broken, issue resolved; verification
  skill before claiming success.
- Failed fix: count, loop to Phase 1, or escalate at 3.
- Not reproducible: gather data. No root cause: the documented exit with
  handling plus monitoring.

## Dependency closure

- In-tree: `root-cause-tracing.md` (→ `find-polluter.sh`), `defense-in-depth.md`,
  `condition-based-waiting.md` (→ `condition-based-waiting-example.ts`). No
  resource cites a SKILL.md passage, so cuts cannot break inbound links.
- `find-polluter.sh` has an upstream test suite outside the skill folder
  (`tests/systematic-debugging/test-find-polluter.sh`). It is not packaged, and
  the script is not executed here.
- Cross-skill: TDD and verification-before-completion are referenced by name and
  **not packaged**. In a trial they are equally unavailable to both arms.
- Inbound, by skill name only: `using-superpowers` ("Fix this bug →
  systematic-debugging first") and `executing-plans` ("Code wrong?
  systematic-debugging"). No inbound reference targets a passage.

## Contradictions and tensions (flagged; NOT resolved by the candidate)

| ID | Passages | Issue |
| --- | --- | --- |
| C1 | Phase 4.4 "If < 3: Return to Phase 1" vs. rationalization row "'One more fix attempt' (after 2+ failures) → … don't fix again" and Red Flag "'One more fix attempt' (when already tried 2+)" | Off-by-one: after two failed fixes, step 4 permits a third after re-analysis; the table says don't fix again. |
| C2 | Phase 3.2 "Make the SMALLEST possible change to test hypothesis" vs. Phase 4.1 failing test "MUST have before fixing" | If the hypothesis change is the fix, the test is written after it. The skill doesn't say whether to revert first. |
| C3 | SD Iron Law and Phase 4.1 (no exceptions) vs. TDD's exceptions (throwaway prototypes, generated code, configuration files: ask your human partner) | Cross-skill: a config-only bug requires a failing test case under SD but is an ask-first exception under TDD. |
| C4 | "No root cause" handling "(retry, timeout, …)" vs. `condition-based-waiting.md` "Replace arbitrary timeouts with condition polling" | Scope tension: external flakiness vs. test timing. |
| C5 | Phase 1.4 instrumentation (code changes) "BEFORE proposing fixes" vs. "BEFORE attempting ANY fix" | Instrumentation edits are not classified as fixes, and their removal is unspecified. |
| C6 | Body "ANY technical issue" vs. description "bug, test failure, or unexpected behavior" | The body is somewhat broader than the selection metadata. |

Evaluation consequences: graders must not penalize either reading of C1, C2 or
C5. Case A4 uses three failures, which avoids C1. Ordering checks that C2
affects are graded as *should*, not *must*.

## Knowledge evidence mapped by content (Petrov / dokimi, dataset `586f823`)

Bedrock `us.anthropic.claude-haiku-5-5` and `us.anthropic.claude-sonnet-5-5`.
The judge is Sonnet 5.5, so the Sonnet arm is self-extracted and self-judged.
**25 of 90** extracted atoms were probed (triage tier, ±0.2 CI at n=25), and
53 of 283 lines carry a probed atom. Strict = `correct_complete` only.

| Probed content (7.0.2 location by content) | Sonnet strict / lenient | Haiku strict / lenient | Candidate |
| --- | --- | --- | --- |
| Symptom fixes are failure (L10) | redundant / redundant | added / redundant | kept verbatim |
| **Boundary instrumentation rule (L76-80; dataset span "L16" is a code-fence line)** | redundant / redundant | added / redundant | kept, reworded as prose |
| When to Use list (L24-30) | redundant / redundant | redundant / redundant | kept verbatim |
| Don't skip when in a hurry (L39-41) | redundant / redundant | redundant / redundant | kept verbatim |
| Phase 1 before any fix (L48-50) | redundant / redundant | added / redundant | kept verbatim |
| Not reproducible → gather data (L62) | redundant / redundant | redundant / redundant | kept, reworded |
| **Signing example, keychain layer (L97-100; dataset span "L88" is a code-fence line)** | **added / added** (no-skill: abstained) | added / added | **deleted** (example-specific detail; secret condition extracted) |
| Quick version of tracing (L114-118) | redundant / redundant | redundant / redundant | kept, reworded as one sentence |
| Read reference COMPLETELY (L128-131) | redundant / redundant | added / added | kept, reworded |
| Hypothesis written, specific (L149-150) | redundant / redundant | redundant / redundant | kept, reworded |
| Worked → Phase 4, else new hypothesis (L157-159) | added / redundant | added / redundant | kept, reworded |
| Phase 4 steps 1-2 (L172-181) | redundant / redundant | redundant / redundant | verbatim |
| verification-before-completion (L189) | redundant / redundant | added / redundant | verbatim |
| Architecture patterns, refactor vs. continue (L200-208) | redundant / redundant | redundant / redundant | verbatim |
| Red flags "Here are the main problems…" (L224-225) | added / redundant | added / redundant | verbatim |
| 3+ failures → see Phase 4.5 (L231); "One more fix" row (L255) | redundant / redundant | added / redundant | verbatim |
| "Stop guessing" signal (L238), rationalization rows (L248, L251) | redundant / redundant | redundant / redundant | verbatim |
| Quick Reference Phase 4 row (L264) | redundant / redundant | redundant / redundant | table deleted (duplicate) |
| No-root-cause handling (L268-272); defense-in-depth pointer (L279-282) | redundant / redundant | redundant / redundant | verbatim |

Reading:

- Every probed atom in the text the candidate rewrites is strict-redundant
  for Sonnet. The exception is the example, which tests recall of example
  content and is uninformative about capability.
- Phase 1 items 1 and 3, Phase 2 items 1, 3 and 4, and Phase 3 items 2 and 4
  were **not probed**. Rewording them is editorial only (no meaning removed);
  no capability claim is made for them.
- All of this is **knowledge-probe-only** evidence from a different deployment
  (Bedrock, not subscription Claude Code), and it is self-judged. It nominates
  places to look. It does not establish that removal is safe.
