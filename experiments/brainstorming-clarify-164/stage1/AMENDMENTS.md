# Amendments to stage-1 freeze 1.0.0

Recorded at the time of change. None so far.

## Amendment 1 (2026-11-07): grader budget
Operational, post-execution: up to 16 more grader attempts, absolute ceiling of 24 actual attempts. Grading inputs and decision rule unchanged. See `AMENDMENT-1-grader-budget.md`.

## Amendment 2 (2026-11-08): U1/U2 identical-file override
Scoring only, post-execution, conditional on verified separate grader executions (met). Uses the existing grade files through a separate path; the official INCONCLUSIVE result and `scores.jsonl` are kept. Corrected outcome STOP-NEGATIVE. See `AMENDMENT-2-identical-file-override.md`.
