# Shared behavioral contract: `test-driven-development` 7.0.2 (for the Opus 5.5 candidate)

Prepared 2026-11-08 for `@apsp/test-driven-development-opus-5-5@0.1.0`. Nothing
here has been executed against a model.

- **The machine-readable contract** is [requirements.json](requirements.json):
  31 requirements, each with verbatim upstream anchors.
- **The original contract review,** with the full T1-T10 analysis, inbound
  references and Petrov evidence mapping, is
  [../tdd-compaction/CONTRACT.md](../tdd-compaction/CONTRACT.md). It still
  applies and is not repeated here.

## The contract by group

| Group | Requirements | Notes |
| --- | --- | --- |
| Activation | A1 description trigger; A2 always (features, bug fixes, refactoring, behavior changes); B1 bug found means a failing test first; A4 anti-skip reminder | A1 is byte-identical in every artifact (discovery selection) |
| Non-activation | A5 prose for humans and trivial code earn no test | **Stated only in `writing-good-tests.md`.** It is an inferred expectation for the entrypoint. Flagged, not moved into `SKILL.md` (moving it would change what the entrypoint says) |
| Ordering | O1 Iron Law; O3 RED, Verify RED, GREEN, Verify GREEN, REFACTOR; F2 repeat | In upstream, O3 is carried by headings plus the diagram. The candidate states it in one sentence |
| Actions | R1 the RED test; R2 test-quality heuristics; G1 minimal GREEN; F1 refactor only after green | |
| Failure handling | O2 code before test: delete and reimplement; V2 RED passes: fix the test; V3 RED errors: fix and re-run; V4 wrong failure: back to RED; V6 GREEN fails: fix the code; V7 other tests fail: fix now | V4 existed only as a diagram edge. It is now text |
| Verification and completion | V1 Verify RED (mandatory, run the test, fails for the right reason); V5 Verify GREEN (mandatory, run the test, all pass, pristine output); V8 the full suite plus reporting every failure by name; C1 the 8-item checklist | **The procedure is the requirement:** "run the test" is kept as an explicit action wherever the candidate removed a placeholder command |
| Approval | A3 exceptions need the partner's OK; S1 "don't know how to test" means ask; P3 no exceptions without the partner's permission | Unchanged text |
| Decision and compliance aids | P1, P2, D1 (11 rebuttals), D2 (13 red flags) | Not contract, but kept verbatim (see the inventory in RATIONALE) |
| Resources | R3 the read condition and 4 rules; X1 `writing-good-tests.md` (names `superpowers:writing-skills`, not packaged) | Byte-identical |

## Ambiguities carried, not resolved

T1-T10 from the original review are carried unchanged. The candidate does not
resolve any of them:

- T1, refactor-only work;
- T2/T3, tests that pass immediately;
- T4, fix vs report pre-existing failures;
- T5, exploration vs prototypes;
- T6, error vs failure at RED;
- T7, deleting the user's code;
- T8, "no exceptions" vs partner permission;
- T9, the description is narrower than the body;
- T10, cross-skill regression recipes.

## Do the stage-1 adjudications apply here?

The `apsp-tdd-001` operator gate settled **evaluation** questions for one
screening run. None of them is a change to the skill, and none is encoded in
this candidate.

| Stage-1 ruling | What it was | Application to this candidate |
| --- | --- | --- |
| R2 capture correction | Harness evidence parsing | None (harness lesson; see PROPOSAL) |
| R3 fixture defect | A hidden test over-specified | None (fixture lesson; see PROPOSAL) |
| R5 permission reading (gate item 4) | The operator's intended reading of T8 when the user **explicitly** permits skipping tests | **Not encoded.** The upstream text keeps both "No exceptions" and "No exceptions without your human partner's permission". Making the permission reading explicit in the skill would be a policy change. It belongs in an upstream proposal, not a compaction. A future evaluation may *score* with this reading if it is pre-declared |
| R6 rule (gate item 5): ask, or a failing behavior test; value-only tests don't count | A reading of A3 together with `writing-good-tests.md`'s "No change detectors" | **Not encoded.** Both source texts are unchanged. Scoring may use the reading if it is pre-declared |
| Q6c: a pre-existing failure is not graded | Scoping one case | None. V7 ("Fix now") and V8 ("report by name") stay as written (T4) |

## Gap classification used for this candidate

These are the categories the skill-compaction method distinguishes:

- **Knowledge gap:** the model doesn't know a fact or term. Definitions and
  examples address it.
- **Execution gap:** the model knows the rule but can't carry out the
  procedure. Procedure text and examples address it.
- **Judgment or selection gap:** the model has to choose an action (minimal vs
  speculative code, when an exception applies). Decision aids address it.
- **Attention or compliance gap:** the model knows the rule and can follow it,
  but doesn't. Rebuttals, red flags, checklists and reminders at the point of
  action address it. **More definitions do not.**

The observations from stage 1 (Sonnet, both arms) fall into these categories:

- Not asking before the configuration exception (R6): an attention/compliance
  gap.
- Skipping tests under explicit permission (R5): T8 judgment.
- Import-error REDs: T6 ambiguity.

None of these is addressed by adding explanation to this candidate. Any
salience change, such as a reminder at the configuration-edit action point,
would be a separately declared treatment, not part of a compaction.
