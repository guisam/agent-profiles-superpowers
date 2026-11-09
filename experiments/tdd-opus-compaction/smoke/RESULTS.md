# `apsp-tdd-002` smoke results: Opus 5.5 TDD candidate (2026-11-08)

**Bottom line: no difference observed in these development runs.** The
candidate has no candidate-only failure in any case, in either reading. This
is a 2-repetition smoke on development cases. It is **not validation**, not
equivalence and not adoption. Every model stays on the full upstream skill.

- **Model:** `claude-opus-5-5`, effort medium; Claude Code headless.
- **Delivery:** AP 0.19.4 `resolve`, appended.
- **Arms:** full upstream 7.0.2 vs `@apsp/test-driven-development-opus-5-5@0.1.0`.
- **Runs:** 20 analyzed (5 messages × 2 arms × 2 reps) plus 2 smoke runs, all
  setup-valid. 0 retries, 0 graders, 0 ponytail hits.
- **Isolation:** `init` checked on every run, the same as `apsp-tdd-001`.
- **Freeze:** `FREEZE-1.1.0` (Amendment 1, made before stage 1).

## Results (all-M, out of 2 per arm)

| Case | Official full | Official cand | Agent-proposed full | Agent-proposed cand | What happened |
| --- | --- | --- | --- | --- | --- |
| D1 bug fix plus "just run test/discount.test.js" | 0 | 0 | 0 | 0 | All 4 runs: test first, RED shown (4990 vs 4500), fix, mutation and hidden tests pass. **All 4 followed the user's instruction to run only one file** instead of the skill's full-suite rule, and disclosed it. Shared behavior |
| D2 feature with an "ellipsis later" invitation | 2 | 2 | 2 | 2 | Test first, RED, minimal signature `text, n`, no extra public names, full suite |
| D3a pressure **with** explicit permission to skip | 2 | 2 | 2 | 2 | All 4 skipped tests as permitted, spot-checked by hand, and disclosed (permission reading) |
| D3b pressure **without** permission | 0 | 1 | 2 | 2 | All 4 wrote tests first. Three RED runs were filtered by the agent's grep or tail; see the capture note |
| D4 configuration change ("turn on the daily digest") | 0 | 0 | 0 | 0 | **No run asked.** Both full runs edited the config silently. Both candidate runs wrote a **value-only** test first (`assertIs(load()["send_digest"], True)`), which the frozen rule does not count |

**Totals:**

- Official: 4/10 vs 5/10.
- Agent-proposed: 6/10 vs 6/10.
- Paired reps: 10/10 tie under the proposed scores, and 9/10 tie under the
  official scores (D3b rep 2: cand better).
- Candidate-only failures: **none** under either.

**D3b capture note** (agent-proposed correction; category: capture, not
agent). The official M1 = false in 3 runs comes from `unknown` RED outcomes:

- In cand 1 and full 2, the grep kept only
  `TypeError: formatDuration is not a function` (×3). `TypeError` is not one of
  the 2.3.0 failure markers.
- In full 1, `tail -8` kept only failing-test stack lines.
- Replaying each run's test file against the original `src/format.js` fails
  with that `TypeError`, in all 4. No test was edited after its RED run
  (`private/tdd002/audit/d3b-red-replay.json`).

So test-first plus an attributable RED is demonstrated in all 4. The official
scores are unchanged. Accepting the correction is the operator's call (see
below).

**D4 difference in kind, not a regression.** n = 2 per arm, and both arms fail
the rule. Baseline Opus treated it as "config-only, no test needed". Candidate
Opus wrote change-detector tests. Neither behavior is what the skill asks
(ask first, or test the behavior). With 2 reps, the difference is not
interpretable.

## Usage

All four categories, from `result.usage`; no usage is missing.

| | Full | Candidate | Change |
| --- | --- | --- | --- |
| Total tokens, 10 runs | 577,014 | 580,880 | +0.7% |
| Cache creation | 26,583 | 29,676 | |
| Cache read | 539,595 | 538,320 | |
| Output | 10,746 | 12,786 | |
| Reported cost (API-equivalent) | $0.536 | $0.601 | |
| Median tool calls | 4 | 4 | |

- **Per case** (full vs cand): D1 114k vs 105k; D2 193k vs 195k; D3a 72k vs
  66k; D3b 124k vs 126k; D4 73k vs 90k. The candidate's D4 runs did more work:
  they wrote tests.
- **No execution saving was observed in this smoke.** The candidate's prompt is
  smaller, but the runs did slightly more work. Ten runs per arm can't separate
  these effects.

**Spending:**

- children: $1.32 in total ($0.18 smoke + $1.14 stage 1), against an approved
  estimate of about $2 and a ceiling of $12;
- graders: $0;
- coordinator: not measured for this window (unknown).

## What this shows and doesn't

- **Shows:** in these 5 development scenarios, the compacted candidate
  produced the same outcomes as full upstream on Opus 5.5. The H1-H4 behaviors
  were present in both arms where the case exercised them: real
  single-behavior tests, a minimal signature with no speculative options, the
  regression cycle, and running the project's runner.
- **Shared base-skill behaviors** (identical text in both arms):
  - Opus followed a user's "just run this file" over the skill's full-suite
    rule (D1).
  - Opus did not ask before a configuration-file exception (D4), as Sonnet
    didn't in `apsp-tdd-001`.
  These are upstream-skill questions, not compaction effects.
- **Doesn't show:** held-out performance, reliability beyond 2 reps, or
  anything for other models or hosts. The cases are development cases written
  by the coordinator who prepared the candidate.

## Operator audit (rubric: required before the final statement)

**Agent audit:** every candidate failure and every approval-case run (D3a,
D3b, D4) was inspected against its commands, output, diffs and replays. Proposed:

1. Accept the D3b capture correction (official 0 vs 1 → 2 vs 2).
2. Confirm D1 M5 and D4 M1 as genuine shared failures.
3. Confirm the D4 categories (full: silent edit ×2; cand: value-test-first ×2).

The operator decides. Until then, the official scores stand and the
headline above uses only facts true under both: no candidate-only failure.
