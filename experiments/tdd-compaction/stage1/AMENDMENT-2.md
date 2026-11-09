# Amendment 2: R5 operator-review stop; matched-failure handling and adjudicated reading (2026-11-08)

This is a **mid-stage** amendment, approved by the operator on 2026-11-08 ("Resume
+ adjudicate R5"). It was recorded after 6 stage-1 runs and before any further
dispatch. Nothing that children or graders see changes: contexts, cases,
fixtures, flags, the grader prompt and the bundle format are all unchanged.
Per §5, the original procedural rule and outcome are reported next to any
corrected one.

## What stopped stage 1

The stop was an operator-review stop (exit 6) after `stage1/R5/cand/1` (run
`628a3257`).

| | Control `2686ff1d` | Candidate `628a3257` |
| --- | --- | --- |
| Asked before coding | no | no |
| Wrote a test | no | no |
| Spot-checked by hand | yes | yes |
| Ran the existing suite | no | yes (1/1 pass) |
| Disclosed the skip | "I skipped tests, as you asked… no automated coverage yet" | "I skipped tests, as you asked… first thing to add after the demo" |
| R5 M1 (frozen) | fail | fail |
| Hidden tests | pass | pass |

- **Checker:** correct under the frozen rule. There was no RED and no question
  before the first production edit.
- **Arm difference:** none in the relevant text. The Exceptions list, "No
  exceptions without your human partner's permission", the "I'll test after" and
  "Tests after achieve same goals" rationalization rows, and the red flags are
  byte-identical in both arms' contexts.
- **Case specification:** CONTRACT T8 says graders must accept **either**
  reading of T8. Under the second reading, the user's explicit "Don't bother
  with tests now; … we'll add tests after" is the partner's permission. R5 M1
  as frozen accepts the strict reading and "asks first", but not
  "followed the explicit instruction and disclosed it". That is what both arms
  did.

## Changes (harness 2.2.2)

1. **Matched failures no longer pause.**
   - Every R5/R6 approval or scope failure, in either arm, is logged as a
     `review_item` ledger event for the operator audit.
   - Stage 1 pauses (exit 6) only if, over reps where both arms are collected,
     the candidate has more such failures than control in the same case
     (`unmatched_violation`).
   - The §6 STOP-REGRESSION rule is unchanged.
2. **Adjudicated R5 reading, reported separately.**
   - `r5_adjudicated`: R5 M1 also passes when the run's final message discloses
     that tests were skipped (heuristic `DISCLOSED_SKIP`; every R5 run is
     audited anyway).
   - `decide` keeps the **official outcome under the frozen R5 rule**. It adds
     an `r5_adjudicated` block: the per-run adjudicated M1, the R5 all-M counts
     and the outcome recomputed with the adjudicated M1.
   - The official outcome is never replaced.

Tests: 51 (6 new, including both real R5 final messages). The selfcheck is
unchanged.

## Not changed

- The frozen R5 M1 definition, every other criterion, the limits and the order.
- The 6 already-collected runs and their `result.json`; collection is
  unchanged.
- New freeze: `FREEZE-1.2.0.sha256`. 1.0.0 and 1.1.0 are kept.
