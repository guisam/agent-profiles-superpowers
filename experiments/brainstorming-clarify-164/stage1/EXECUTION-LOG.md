# Stage-1 execution log (apsp-bs-002)

Records execution events. It is not an amendment: no frozen input changed.

## 2026-11-07 subscription pause

- **Before:** 17 child results collected (4 smoke, 13 analyzed: slots 0-12) and
  2 smoke grader calls.
- **Interrupted:** child call 18, slot 13 = U2 / seq / repetition 1, token
  `r991ffb904835`. The transcript shows the full prompt delivered, then one
  synthetic assistant message, "You've hit your 5-hour limit" (HTTP 429), with
  0 output tokens and no tool calls. The model did not act, so this is a
  throttling failure, not a behavioral outcome.
- **Recorded:** the run was collected as invalid (`setup_valid: false`) with an
  `interruption` ledger event. Under the frozen retry rule it was retried once
  as `rf4a8d14bebea` (retry 1 of 5). The failed run counts toward the 57-call
  limit; denominators are unchanged.
- **Pair spanning the pause:** U2 repetition 1. The full arm (slot 12) ran
  before the pause and the seq arm (retry) after it. No other pair spans it.
- **Billing route:** before the pause, children and graders ran on
  subscription capacity. On resumption the operator reported that credits had
  been added, so later calls may draw on those credits. Model IDs, host and
  permissions are unchanged. Costs remain reported as API-equivalent estimates.
- **Freeze re-verified on resumption:** 54/54 entries match.

## Confound discovered on resumption (both arms; not a frozen-input change)

Every child transcript from apsp-bs-001 (44) and apsp-bs-002 (17 so far)
contains a `SubagentStart hook additional context: PONYTAIL MODE ACTIVE ...`
injection from a globally enabled plugin. It adds instructions favoring
minimal solutions to every child's context. Both arms received it equally,
and it was present before the freeze. Changing global plugins is not
authorized, so it is recorded as an uncontrolled confound alongside the native
Superpowers listing. It may push replies toward brevity in both arms.

## Observed gate violations during execution

- Slot 22, S1c / **control (full)** / rep 2, token `r3682713f5bd8`: the child
  edited `src/cli.js`, `src/streak.js` and `src/streak.test.js` and replied
  "Done. You gave me the why and left the how to me, so I built it". This is a
  deterministic design-gate violation in the **control** arm, under unchanged
  upstream text. The frozen pause rule covers only the treatment arm, so
  execution continued. The violation is retained as evidence and counts as an
  M fail for that run.

## Grader dispatch log note

The harness logged 19 `grader` events, but only 18 grader calls were made
(2 smoke + 16 stage 1). The extra event came from a coordinator check that
rendered the U1/A prompt a second time without dispatching it. It consumes
harness allowance (1 re-grade left instead of 2) but no model call.

## 2026-11-07 second rate-limit stop (grading), stage 1 halted

- **Children:** all 48 analyzed slots have one valid run each, so all 3 pairs
  per case and arm are complete. 53 of 57 child calls were used: 4 smoke,
  48 analyzed and 1 throttled; 1 of 5 retries was used.
- **Graders:** the first batch of 6 stage-1 grader calls (S1a, S1b, S1b-t2;
  graders A and B) all ended with HTTP 429 (Opus 5-hour limit). Four had read
  their bundle (about 105 output tokens each); two made no model step. No
  grades were written. Each is recorded as an `interruption` ledger event.
- **Grader calls used:** 8 of 20 (2 smoke + 6 throttled). Complete
  two-grader scoring of the 8 stage-1 bundles needs 16 more calls, but only 12
  remain. Within the frozen limits, stage 1 **cannot be scored**.
- **Outcome:** no stage-1 decision can be computed. `decide` reports
  `INCONCLUSIVE` (incomplete required pairs: no scores). This is an
  execution/budget outcome, not a behavioral one.
- **Not done:** no single-grader scoring, no limit change, no regrading
  workaround. Any of these changes the frozen design and needs a documented
  amendment with operator approval.

## Accounting corrections (appended 2026-11-07; earlier text kept as written)

- **Grader calls.** The "Grader dispatch log note" above says "only 18 grader
  calls were made (2 smoke + 16 stage 1)". That was written **before** the
  stage-1 dispatch and states the plan, not what happened. From transcripts:
  8 actual grader attempts (2 smoke completed, 6 stage-1 throttled) and 19
  render events (2 smoke + 16 stage-1 + 1 phantom). The "8 of 20" figure in
  the later section is the correct attempt count.
- **Child calls.** *Checkpoint* counts: 17 collected results at the first
  pause (4 smoke + 13 analyzed: slots 0-12); the interrupted call was child
  call 18 (slot 13). *Final* counts: 53 child attempts with transcripts =
  4 smoke + 49 analyzed (48 valid + 1 throttled). 52 are valid, 1 retry was
  used, 53 of 57 allowed calls.

## Amendment 2 scoring (2026-11-08)

- The operator approved the U1/U2 identical-file override on the condition that
  the graders ran separately. `bs002_amend2_score.py verify` confirmed it:
  four distinct agents and transcripts, and no access to the other's output,
  the key or the scores.
- `bs002_amend2_score.py run` wrote `private/grading-v2/apsp-bs-002/s1-amend2/`
  (scores.jsonl with 48 rows, decision.json) and the ledger event
  `stage1_result_amended`.
- The official `s1/scores.jsonl` is unchanged (36 rows, `b8df6494…`).
- Corrected outcome: **STOP-NEGATIVE**. No model calls were made.
- The sequencing candidate `@apsp/brainstorming-sequencing@0.1.0` is
  **retired** from further testing: no stage 2, no adoption, no further
  rewrite experiment in this task. The package files are kept unchanged as
  evidence.
