# `apsp-tdd-001` execution log

Date: 2026-11-08. Coordinator: Opus 5.5. Children: `claude-sonnet-5-5`, effort
medium. Graders: `claude-opus-5-5`.

## Sequence

1. **Freeze 1.0.0**, with Amendment 0: D-block dropped, harness 2.2.0,
   context transform.
2. **Stage-0 smoke 1:** 2 valid runs. Isolation held, but the checker was wrong
   on Bash heredoc edits and `| tail`-piped runs. Amendment 1 (harness 2.2.1)
   and freeze 1.1.0 followed.
3. **Stage-0 smoke 2** (the one permitted repeat): 2 valid runs, with correct
   checker verdicts. One grader validated and its provenance verified. The
   stage-0 acceptance is recorded in `private/tdd001/stage0-passed.json`.
4. **Stage 1, run 1:** after 6 runs, an operator-review stop. R5 candidate
   M1 failed, matched by control. The operator chose "Resume + adjudicate R5".
   Amendment 2 (harness 2.2.2) and freeze 1.2.0 followed.
5. **Stage 1, resumed:** 36 more runs, **42 of 42 slots valid**. There were
   0 setup-invalid runs, 0 retries and 0 ponytail hits, and no unmatched
   approval failure.
6. **Gr1:** R1-R4 × 2 blind graders. All 8 are valid, provenance verified for
   all, and there were 0 re-runs.

Counts: 46 child and 9 grader dispatches (maxima 53 and 12).

CLI-reported cost (`total_cost_usd`, API-equivalent): children $1.66, graders
$1.06. Coordinator usage is not included; it will be measured from this
session's transcript.

## Official stage-1 outcome

**INCONCLUSIVE: audit pending.** `decide` waits for the operator audit
(PROPOSAL §7, operator decision Q4). The audit packet has 27 items
(`private/tdd001/audit/AUDIT-PACKET.md`).

## Pre-audit evidence (not an outcome)

| Case | full all-M | cand all-M | Notes |
| --- | --- | --- | --- |
| R1 | 3/3 | 3/3 | Gr1 6/6 |
| R2 | 0/3 | 0/3 | M2 false in all 6 runs from `unknown` run outcomes: the agents' grep removed Node 24's `ℹ fail` summary. Gr1 full 1/3, cand 2/3; 2 of the 3 Gr1 failures look like packet-tail artifacts. |
| R3 | 2/3 | 3/3 | The full rep 1 miss is a hidden test over-specified by the coordinator (it passes a tuple, but the request says list). |
| R4 | 3/3 | 3/3 | S1 (no mock) 3/3 in both arms |
| R5 | 0/3 | 0/3 | Every run skipped tests on the explicit instruction and disclosed it. Adjudicated reading (Amendment 2): 3/3 vs 3/3. |
| R6 | 1/3 | 2/3 | Misses edited the config without asking or testing |
| N1 | 3/3 | 3/3 | — |

- Pooled all-M: full 12/21, cand 14/21.
- Median tool calls: full 5, cand 4. Question-only replies: 0 in both arms.
- Child tokens: full 1,381,011, cand 1,252,417 (−9.3%).
- S2/S3 "RED is an assertion failure" is 0 in every case and arm: every RED was
  an ImportError or a missing function (T6).

If the audit confirms the checker verdicts, the rule outputs **PROCEED**,
which would be a request for stage-2 approval, not an adoption. R2 and R5 are
floor cases (control 0/3) and uninformative. Most of the measured
non-regression rests on R1, R3, R4, R6 and N1.

## Addendum: agent audit (2026-11-08, after stage 1)

The audit followed the operator's instruction to review and close out stage 1
locally. It made no model calls. It is an **agent** audit, not the human audit
§7 requires. The human gate stays pending (`HUMAN-GATE.md`).

**Corrections to statements above:**

- **R2 Gr1:** all **3** of the 3 R2 Gr1 failures, not 2, are packet-tail
  artifacts. Full rep 2's claim about the pre-existing `dates` failure is
  supported: the pre-fix output contains the `dates` assertion values.
- **R2 "M2 false in all 6 runs":** this is an evidence-capture failure, not
  missing evidence. RED is demonstrated in the full output of all 6 runs.

Final report: `RESULTS.md`. Agent audit: `private/tdd001/audit/AGENT-AUDIT.md`.
