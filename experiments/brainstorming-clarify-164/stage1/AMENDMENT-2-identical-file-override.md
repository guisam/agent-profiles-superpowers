# Amendment 2: identical-file override for U1/U2 (scoring, post-execution): apsp-bs-002 stage 1

The operator authorized this on 2026-11-08, after grading was complete and
the official result (INCONCLUSIVE) had been recorded. It does **not**
regenerate or edit `FREEZE-1.0.0.sha256` or any file it lists. It does not
change the official result, `scores.jsonl` or any grade file either.

## Why

The frozen `collect_v2.score` rejects a case when its two grade files are
byte-identical, as a sign that the graders were not independent. Byte
equality cannot establish that, in either direction:

- Two independent graders that both pass every criterion on every reply
  produce the same canonical JSON. This happened for U1 and U2: 6/6 replies,
  every M and S criterion `pass`, no evidence spans.
- Two non-independent graders can produce different bytes, for example by
  copying the content and reformatting it.

Independence is a fact about how the graders were executed, not about what
they wrote.

## Condition (checked before scoring; met)

`private/bs002_amend2_score.py verify` checks each of U1 and U2 for:

| Check | U1 | U2 |
| --- | --- | --- |
| Two completed `grader_attempt` events, different agent IDs | yes (IDs in the private ledger) | yes |
| Exactly one transcript per agent, no mixed agent IDs | yes | yes |
| No tool call references the other grader's output, the key or `scores.jsonl` | yes (A: 2 calls, B: 4) | yes (2 and 2) |
| Each grader wrote its own output | yes | yes |
| Grade file sha256 unchanged since its attempt was recorded | yes | yes |

The tool calls were:
- each grader read its own `bundle.md`;
- U1/B also listed and read the permitted `fixtures/habit-sync` (one earlier
  `cat` of a nonexistent path failed);
- each grader wrote its own `grades-<A|B>.json`.

The checker was also exercised against injected violations: a reference to
the other output, a read of `scores.jsonl`, and an empty call list. It
rejected all three.

## What changes

The aggregate is corrected through a separate, reviewable path,
`private/bs002_amend2_score.py run`, which runs once:

1. It copies the official `s1/scores.jsonl` (36 rows, sha256 `b8df6494…`,
   unchanged afterward) to `private/grading-v2/apsp-bs-002/s1-amend2/`.
2. It scores U1 and U2 with the frozen `validate_grades` and `combine`, from
   the existing grade files. The only step skipped is the byte-equality line
   of `score`.
3. It runs the frozen `decide` on the amended scores file (48 rows, sha256
   `0f054b8f…`). This redirects `grading_dir` in memory.
4. It writes `s1-amend2/decision.json` and a `stage1_result_amended` ledger
   event.

Unchanged:
- grade files, replies, keys, rubric, criteria and model;
- the two-grader rule;
- every other validation (reply IDs, case, criteria, values, completeness);
- deterministic gates;
- the decision rule.

No model calls, regrading or new grades.

## Result

**Corrected outcome: STOP-NEGATIVE.** F = 0 and Q = 0 on the primary
endpoint. The S3 all-M score dropped by 2 runs (3 → 1). U1 and U2 are 3/3 in
both arms. There were no treatment-arm gate breaches, no missing pairs, and
3 disagreements, all in S1a. The official procedural outcome stays
**INCONCLUSIVE**. Both are reported.

## Future harness fix (recorded only; not implemented)

Replace the byte-equality guard in `score` with a provenance check that:
- confirms the two grades came from two distinct, completed grader executions
  (agent ID, transcript and hash recorded at attempt time);
- confirms neither execution accessed the other's output, the key or the
  scores.

Identical content should then be accepted. This is the check in
`bs002_amend2_score.verify`. The harness gains no other new framework.
