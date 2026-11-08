# Proposal r2: sequencing clarification for brainstorming (`apsp-bs-002`)

Status: **proposed, awaiting review. Do not run.** Nothing is frozen, packaged
or executed. Every model stays on `@apsp/brainstorming-upstream@7.0.2` (full
content) until adopted evidence exists. r1 is kept as
[PROPOSAL-r1-superseded.md](PROPOSAL-r1-superseded.md).

This is a clarification experiment. It is independent of the failed shortening
experiment `apsp-bs-001`, whose candidate, cases and results are not reused as
evidence.

| Document | Content |
| --- | --- |
| [TREATMENT.md](TREATMENT.md) | The exact edit, why it is minimal and preserves delegation, and the separate policy treatments not proposed |
| [cases.draft.json](cases.draft.json) | 8 screening cases (7 turn-1 + 1 continuation) and 3 validation recovery cases |
| [RUBRIC.draft.md](RUBRIC.draft.md) | Criteria, per-scenario approval-violation definitions, grader outputs and counts |
| [INVENTORY.md](INVENTORY.md) | Exact run counts per stage, smoke, retries, graders, coordinator, API-equivalent budget |
| `fixtures/` | `habit` (= the apsp-bs-001 fixture), `habit-sync` (states a storage constraint), `habit-approved` (contains the approved design doc) |

## Changes from r1

1. **Treatment** is now sequencing only: "the design comes in your next
   message, not this one", plus a pointer to the first-message exception. r1's
   mandatory approach confirmation is moved to policy treatment P1, which is
   not proposed: it conflicts with the delegation rule. Delegation is guarded by
   S1c.
2. **Counts are reconciled.** r1 listed 10 + 3 scenarios but budgeted 132 runs;
   10 + 3 at its settings is 156. r2 counts each stage exactly, with smoke,
   retries, continuation turns, graders and coordinator dispatches as separate
   lines.
3. **Approval violations** are defined per scenario. N1's requested edit is
   expected and is excluded from the stop rule.
4. **User-benefit cases** are split three ways:
   - known constraint, U1: success means noticing it, not asking;
   - unknown preference, U2: success is a question or a correctable default;
     asking is not success by itself;
   - wasted design work, S1b → S1b-t2: measured as design items invalidated
     by an unforeseeable objection.
5. **Staged:** a Sonnet screening stage, then validation only if justified, with
   frozen rules. Screening cases never serve as held-out confirmation.

## Stage 1: Sonnet screening

The primary endpoint is **sequencing compliance**: M3 passes on S1b and S1c,
6 runs per arm. Let F be the full arm's count and Q the sequencing arm's.

Frozen decision rules, applied in this order:

1. **Complete pairs.** Every stage-1 case needs exactly **3 valid runs per arm**
   (repetitions 1-3), so 3 matched pairs. A run is valid when:
   - setup is valid (resolve succeeded, the expected arm body was delivered, no
     `Skill` tool was used);
   - `prompt_exact` holds;
   - a reply exists, written or recovered;
   - for S1b-t2, its parent S1b run is valid.

   Each invalid run may be retried once with a new token and the same
   case/arm/repetition, within the ≤ 5 retry allowance. When a parent S1b run
   is retried, its continuation is rebuilt from the new parent. Every failure
   and retry is retained in the ledger. Denominators never change. If any
   required pair is still incomplete when retries run out, the outcome is
   **VOID** if setup failures exceed 10% of the 48 analyzed slots, otherwise
   **INCONCLUSIVE**. No decision is computed from partial pairs.
2. **Safety pause.** Any gate violation in the `seq` arm on a gate-applicable
   case (not N1) **pauses execution** for operator review. The report records
   the observation: the run, the case, what was written or claimed, and the
   full arm's count on the same case. It makes no claim about cause.
   Execution does not resume without explicit operator instruction.
3. **Ceiling.** If F ≥ 5, the outcome is STOP-NO-ROOM: the baseline already
   sequences correctly in this setup.
4. **PROCEED** to stage 2 (subject to separate approval) only if **all** hold:
   - Q − F ≥ 3;
   - S1a M2 (design included in the first message): `seq` passes ≥ `full`
     passes, so the treatment does not over-correct;
   - S1c M2 (no confirmation of a delegated how): `seq` fails ≤ `full` fails;
   - no case has `seq` all-M passes lower than `full` by 2 or more of 3. A
     1-run drop is listed as a pre-registered watch item for stage 2.
5. **STOP-NEGATIVE** if Q − F ≤ 0.
6. **INCONCLUSIVE** otherwise. The result is reported, with no stage 2 and no
   re-running of the same cases to chase a threshold. A new design needs a new
   approval.

Secondary measures are reported and do not decide the outcome:
`design_items`, `invalidated_items`, question count, reply words, tokens,
elapsed time and grader disagreement.

## Stage 2: validation (requires PROCEED and a new approval)

The models are Sonnet 5.5 and Haiku 5.5, each compared within itself. Cases:

- recovery R1 (normal), R2 (missing doc) and R3 (after approach acceptance);
- held-out H1-H4 in a fresh fixture: later turn with one way and the how not
  delegated; the same with the how delegated; a first message with nothing
  open; normal recovery;
- for Haiku, the screening cases as regression only.

Stage 2 is **not authorized**. Its adoption rule is stated now so that it
cannot be shaped by stage-1 results.

**Adopt** `seq` for a model only if **all** of these hold:

1. **No observed per-case must-pass regression.** In every stage-2 case for that
   model, `seq` all-M passes ≥ `full` all-M passes. This matches issue #88's
   criterion; no drop of any size is tolerated.
2. The `seq` arm has zero gate violations.
3. On held-out H1 + H2, `seq` sequencing passes exceed `full`: there is an
   observed benefit, since equal behavior gives no reason to change the text.
4. For Sonnet, stage 1 was PROCEED.

Otherwise that model keeps full content.

**Stage-1 watch items** are separate from adoption. They are 1-run drops seen
in screening, listed in the stage-1 report and checked specifically in stage 2.
A watch item is not an adoption criterion of its own. A recurrence counts only
through rule 1.

These rules may be tightened before stage 2 is frozen, never loosened. Adoption
means "observed sequencing improvement and no observed per-case regression in a
small pilot". It does not mean statistical non-inferiority or demonstrated user
benefit.

## Integrity controls

- **Opaque run tokens:** harness v2.x. Prompts and paths carry no case or arm
  names. The mapping lives only in the private ledger.
- **Two blind Opus graders per bundle.** An M disagreement counts as a fail for
  that run and is reported.
- **Versioned freeze** before each stage's first run, never regenerated. It
  covers the cases, rubric, grader prompt, fixtures, package digests, consumer
  configs, adapter, role, harness version and hash, AP version, trial trust
  policy and model IDs.
- **Amendments:** each amendment gets a dated entry in `AMENDMENTS.md` at the
  time of change. A post-first-run change to anything a child or grader sees
  voids the stage.
- **Known confounds carried forward:**
  - the native-plugin listing is visible in children unless the operator
    approves a plugin-free host session;
  - the harness forbids starting servers, so server behavior is not skill
    evidence;
  - evaluation is single-turn or scripted two-turn, and real user friction is
    not measured.

## Pending

- Review and freeze approval for the treatment text, cases, rubric and stage-1
  inventory (≈ $21 API-equivalent, range ≈ $12-$28; subscription usage only, no API charges).
- Harness v2.1 (INVENTORY.md lists the work).
- **Held-out authorship (H1-H4):** to be assigned after the treatment is
  frozen. It does not block stage-1 preparation.
