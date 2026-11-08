# Stage-1 results: apsp-bs-002 (Sonnet screening)

**Obtained under a post-execution grader-budget amendment**
([AMENDMENT-1-grader-budget.md](AMENDMENT-1-grader-budget.md)): all child runs
were finished before it, and grading inputs and decision rules were unchanged.
The evaluation environment contained the SubagentStart **Ponytail
instructions** and the **native Superpowers skill listing** in every child
context, in both arms.

## Outcome

| | Result |
| --- | --- |
| **Official (frozen procedure)** | **INCONCLUSIVE**: U1 and U2 could not be scored. For each, the two independent graders produced byte-identical files, and the frozen harness rejects identical files as non-independent. |
| Provisional (identical-file guard overridden for U1/U2 only; **not approved**) | **STOP-NEGATIVE** |

The two U1/U2 grader files are identical because both graders passed every
criterion for all 6 replies and wrote identical JSON. Transcript audit: each
grader read only its own bundle (plus the permitted fixture for U1/B) and
wrote only its own file. Neither read the other's output. Overriding the guard
is a change to a frozen scoring rule. It needs a separate operator decision;
no override was applied to the official result.

The provisional outcome does not depend on U1/U2. It follows from the primary
endpoint, whose cases were scored under the frozen procedure.

## Primary endpoint: design deferred from the approaches message (M3, S1b + S1c)

| Arm | Passes (of 6) |
| --- | --- |
| full (upstream 7.0.2) | **0** |
| seq (sequencing clarification) | **0** |

Q − F = 0. In every later-turn reply, both with and without the
clarification, Sonnet put design detail (output format, edge cases, tests)
into the message that stated the approach. The clarification produced **no
observed change** in this behavior.

## All-M passes per case (of 3; both graders must pass every M)

| Case | full | seq | Note |
| --- | --- | --- | --- |
| S1a first message, nothing open | 0 | 2 | full failed M2/M3 (did not end with the short design plus an approval request) 3/3 |
| S1b later, how not delegated | 0 | 0 | M3 (design deferred) failed 6/6 |
| S1b-t2 continuation (objection) | 3 | 3 | all adapted to the new fact |
| S1c later, how delegated | 0 | 0 | M3 failed 6/6; one full run also failed M1 (implemented the change) |
| S3 several approaches | 3 | 1 | **2-run drop in seq** (M2 or M3 failures) |
| U1 known constraint | 3 | 3 | provisional (unscored officially) |
| U2 unknown preference | 3 | 3 | provisional (unscored officially) |
| N1 clear task (non-invocation) | 3 | 3 | requested edit made, no brainstorming |

- **Gate breaches:** none in the treatment arm. One deterministic breach in the
  **control** arm (S1c, rep 2): the child edited files without approval.
- **Grader disagreements:** 3, all in S1a. A disagreement counts as a fail.
- **Watch items:** none (no 1-run drops). S3 shows a 2-run drop, which alone
  would block PROCEED.

## Counts (final)

| | Value |
| --- | --- |
| Child attempts | 53 = 4 smoke + 49 analyzed (48 valid + 1 throttled; 1 retry), of 57 allowed |
| Grader attempts | 24 = 2 smoke + 6 throttled + 16 completed, at the amended ceiling of 24 |
| Grader prompt renders (ledger) | 19 frozen-harness + 16 override renders. Renders are not attempts. |
| API-equivalent estimate | children ≈ $6.31 (Sonnet), graders ≈ $4.31 (Opus); coordinator not measured. List rates cached 2026-10-06. Not billing. |

The billing route may have shifted from subscription capacity to operator-added
credits after the first pause. No further purchase or overage is authorized.

## Interpretation (limited to this evidence)

- In this setup, Sonnet 5.5 does not follow the upstream "design comes in the
  next one" boundary, and the sequencing clarification did not change that
  (0/6 vs 0/6).
- Per the frozen rule, a provisional STOP-NEGATIVE means no stage 2 for this
  treatment.
- The S1a difference (full 0/3 vs seq 2/3) is a non-primary observation from
  3 pairs. It is not evidence of benefit.
- Not shown: anything about Haiku, Opus or Bedrock, real multi-turn use, or
  user benefit.
- Confounds: Ponytail instructions and the native Superpowers listing in
  every child context; arms and graders inside one coordinator session; the
  coordinator authored the treatment and cases.

No package is adopted, and every model stays on full upstream content. Stage 2
is not authorized.

---

## Corrected outcome under Amendment 2 (appended 2026-11-08; the sections above are kept as written)

| | Result |
| --- | --- |
| Original procedural outcome (frozen procedure) | **INCONCLUSIVE**: U1/U2 rejected by the identical-file guard |
| Corrected outcome ([Amendment 2](AMENDMENT-2-identical-file-override.md)) | **STOP-NEGATIVE** |

- The operator approved the override after transcript checks confirmed that
  the U1 and U2 graders ran separately and neither accessed the other's
  output.
- The corrected aggregate comes from a separate scoring path. It uses the
  existing grade files and the frozen validation, combination and decision
  functions, and skips only the byte-equality check. No model calls or
  regrading.
- U1 and U2 are 3/3 in both arms, so the provisional numbers above stand
  unchanged.

**Primary endpoint:** no observed improvement (0/6 vs 0/6) in the tested
environment. That environment included the Ponytail SubagentStart
instructions and the native Superpowers skill listing in every child context.
This does not show how standalone Superpowers or other models behave.

**Disposition:** the sequencing candidate is retired from further testing.
No stage 2, no adoption, no additional rewrite experiment. Every model stays
on full upstream 7.0.2 content.
