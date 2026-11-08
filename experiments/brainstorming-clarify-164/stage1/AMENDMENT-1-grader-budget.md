# Amendment 1: grader budget (operational, post-execution) — apsp-bs-002 stage 1

Authorized by the operator on 2026-11-07 (after all child runs were finished
and before any stage-1 grade existed). Recorded before any further model
call. It does **not** regenerate or edit `FREEZE-1.0.0.sha256` or any file it
lists.

## What changes

The grader-attempt budget only. Up to 16 additional grader attempts are
allowed, with an **absolute ceiling of 24 actual grader attempts**. Earlier
smoke and failed attempts count toward the ceiling.

Unchanged: the grader model (`claude-opus-5-5` via Agent `model: opus`),
`RUBRIC.md`, `GRADER-PROMPT.md`, the 8 stage-1 bundles and their reply IDs and
keys, the two-grader rule (an M criterion passes only if both pass), and the
stage-1 decision rule (`collect_v2.decide`). There are no new child runs, no
single-grader fallback, no selective regrading and no retries prompted by
grades.

## Reconciled accounting before this amendment (from transcripts)

| Kind | Count |
| --- | --- |
| Grader prompt renders (harness `grader` ledger events) | 19 = 2 smoke + 16 stage-1 + 1 phantom re-render (U1/A, never dispatched) |
| Actual grader attempts (transcripts) | 8 = 2 smoke (completed) + 6 stage-1 (all throttled, HTTP 429; 4 made a model step of about 105 output tokens, 2 made none) |
| Completed stage-1 grades | 0 |
| Remaining attempts under the ceiling | 24 − 8 = 16, exactly the number needed for 8 bundles × 2 graders. **There is no slack.** |

The harness's `limits.grader_runs: 20` counts render events, not attempts.
After this amendment it is bypassed by a separate, documented driver
(`private/bs002_grade_override.py`). The driver re-renders prompts through
the frozen `collect_v2.grader_prompt` and its frozen template. In memory only,
it raises the render limit; it enforces the attempt ceiling of 24 from
explicit `grader_attempt` ledger events. The frozen `run-config.json` and
`collect_v2.py` are not modified.

## Execution rules

- Start only after the reported Opus reset (17:10 PT); it is 17:44 PT at
  recording.
- Dispatch one grader first. If it is throttled, stop immediately.
- After that, stop launching new attempts as soon as any attempt is throttled
  or returns an invalid grade file. With zero slack, either outcome means
  grading cannot complete within the ceiling. Report that and stop.
- Every attempt (transcript, grade file, outcome) is preserved and recorded as
  a `grader_attempt` ledger event.

## Reporting

Any stage-1 outcome is reported as obtained **under a post-execution
grader-budget amendment**. The evaluation environment contained the
SubagentStart Ponytail instructions and the native Superpowers skill listing
in every child context (see `EXECUTION-LOG.md`).

Spending: the last explicit authorization stands, meaning existing capacity
only and no purchases or automatic overages. The fact that credits were added
is not read as permission for further purchases.
