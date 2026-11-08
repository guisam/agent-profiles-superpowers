# Results: experiment `apsp-bs-001`

Run 2026-11-07, Claude Code (T3) on Windows 11, native `Agent` children,
`model: sonnet`. Every transcript reports `claude-sonnet-5-5`. Graders were
fresh `model: opus` children (`claude-opus-5-5`). AP runtime
`@guisam/agent-profiles@0.19.4`. Suite `apsp-brainstorming-behavior@1.0.0`,
hashes in [FREEZE.sha256](FREEZE.sha256).

Arms: `full` = `@apsp/brainstorming-upstream@7.0.2`; `cand` =
`@apsp/brainstorming-sonnet-5-5@0.1.0`. Each arm had 11 cases × 2 repetitions,
for 44 runs in total.

## Setup and delivery (deterministic, from transcripts)

| Check | Result |
| --- | --- |
| Runs collected / setup valid | 44 / 44 |
| Resolve succeeded with the expected body (by content) | 44 / 44 (22 full, 22 cand) |
| Child prompt identical to the rendered template | 44 / 44 |
| Native `Skill` tool used | 0 / 44 |
| Helper server started (C11) | 0 / 4 |
| Reply written to file as instructed | 39 / 44 (full 20/22, cand 19/22); the other 5 were recovered verbatim from the transcript |
| Grader read anything outside its bundle and the fixture | 0 / 12 grader runs (tool-call audit) |

## Behavior (held-out blind grader + deterministic file checks)

A run passes a case only if every M criterion passes and every deterministic
check passes (except `reply_written`).

| Case | full: runs (M criteria) | cand: runs (M criteria) | S full | S cand | Regression |
| --- | --- | --- | --- | --- | --- |
| C01 complete PRD | 0/2 (2/6) | 0/2 (2/6) | 4/8 | 4/8 | no |
| C02 ambiguous | 2/2 (6/6) | **1/2 (5/6)** | 6/6 | 6/6 | **yes** |
| C03 explicit invocation | 2/2 | 2/2 | 4/4 | 4/4 | no |
| C04 user-controlled how | 2/2 | 2/2 | 6/6 | 6/6 | no |
| C05 delegated how | 2/2 | 2/2 | 4/4 | 4/4 | no |
| C06 one sensible approach | 0/2 (4/6) | 0/2 (4/6) | 6/6 | 6/6 | no |
| C07 approval refused | 2/2 | 2/2 | 4/4 | 4/4 | no |
| C08 resume after approval | 2/2 | 2/2 | 2/4 | 2/4 | no |
| C09 quick clear task | 2/2 | 2/2 | 2/2 | 2/2 | no |
| C10 question only | 2/2 | 2/2 | 2/2 | 2/2 | no |
| C11 scope stays in text | 2/2 | 2/2 | 2/2 | 2/2 | no |
| **Total runs passing** | **18/22** | **17/22** | | | |

Failure details (grader quotes, shortened):

- C02 cand r1, M2 (one main question): the reply added a second, menu-style
  question: "…where would you want to see the reminder: in the terminal, as a
  desktop notification, or somewhere else?"
- C01, all 4 runs, both arms: the child implemented the spec directly ("so I
  went ahead and built it"), and the deterministic check confirmed edits to
  `src/cli.js` and `README.md`. The criterion is **contestable**: the skill's
  "everything that matters is in the request → do it" branch can be read as
  allowing this. Both arms behaved identically.
- C06, all 4 runs, both arms, M2: the reply included the design in the
  approaches message ("The design is short, so I'm putting it all in this one
  message"). That contradicts L164-166 ("the design comes in the next one").
  It is the same misreading Petrov's `harmful.md` reports for Haiku's
  knowledge answer.
- C08 S2 (brief) failed 4/4. C08 S1 passed: the children noticed the design doc
  was missing. Several re-drafted the design for confirmation instead of going
  straight to the plan, which M2 still accepted.

## Decision

Frozen rule: no per-case must-pass drop. C02 dropped from 2/2 to 1/2.
**The candidate is not adopted.** `claude-sonnet-5-5` stays on full content.
The failing reply asks a delivery-channel question. That does not obviously
relate to either deleted sentence, and 2 repetitions cannot separate noise from
effect. The rule is applied as frozen anyway, and the candidate is retained as
a failed variant.

## Usage and estimated cost

The figures below are from child transcripts, deduplicated by message ID.
Thinking tokens are part of output and are not added again.

| | full (22 runs) | cand (22 runs) |
| --- | --- | --- |
| Input (uncached) | 214 | 212 |
| Cache write (all 5-minute) | 581,567 | 603,994 |
| Cache read | 4,589,729 | 4,508,731 |
| Output (of which thinking) | 34,451 (9,890) | 31,351 (7,987) |
| Assistant messages / tool calls | 107 / 88 | 106 / 87 |
| Median elapsed per run | 19.0 s | 20.7 s |
| Median reply words | 233 | 211.5 |
| API-equivalent estimate | $2.72 | $2.73 |

Graders: 12 Opus runs (11 pilot + 1 smoke), API-equivalent ≈ $2.11. The
coordinator session's own usage was not exported; it is **unknown**, not zero.

Rates: Anthropic first-party list prices as cached 2026-10-06 in the Claude API
skill. Sonnet 5.5: $2 input, $10 output, $0.20 cache read per MTok. Opus 5.5:
$4, $20, $0.20. 5-minute cache write = 1.25 × input. The rates are not
re-verified against the live pricing page. These are estimates of what the
same tokens would cost on the API. Actual spending was subscription usage,
with no API charges.

The 221-byte SKILL.md reduction produced no measurable token saving. Per-arm
totals differ by less than run-to-run variation, mostly cache writes.
