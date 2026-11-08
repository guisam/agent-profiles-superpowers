> **Superseded (r1, 2026-11-07).** Kept for traceability. Review found that its treatment adds mandatory approach confirmation, conflicting with the upstream delegation rule, and that its run count was inconsistent (10 + 3 scenarios imply 156 runs, not 132). See PROPOSAL.md (r2).

# Proposal: clarify the "one sensible way" sequencing rule (experiment `apsp-bs-002`)

Status: **proposed, awaiting approval.** Nothing is frozen, packaged or run.
Every model stays on `@apsp/brainstorming-upstream@7.0.2` (full content) until
this experiment, or another one, produces adopted evidence.

This is a **clarification** experiment: it adds wording. It is separate from
the failed shortening experiment `apsp-bs-001` and reuses none of its
candidate text, cases or results as evidence.

## Motivation (observed, limited)

- Petrov's dokimi data (`harmful.md`): Haiku 5.5 *with* the skill answered the
  L164-166 probe by putting the short design in the same reply.
- `apsp-bs-001` C06: Sonnet 5.5 combined the approaches and the design in one
  message in 4/4 runs in both arms, and still asked for approval before writing
  anything. See [the adjudication](../../evaluations/brainstorming/audit/GRADING-ADJUDICATION.md).
- A plausible cause is confusion between two rules that read alike:
  - **First-message exception** (L72-76): "If nothing like that is open, there's
    one sensible way: end with the short design itself … Their approval covers
    the approach and the design."
  - **Later approaches step** (L164-166): "When there's genuinely one sensible
    way, say so in that message and explain why the others don't fit; the
    design comes in the next one."

This is a hypothesis; the data shows only the behavior, not its cause.

## Treatment: one minimal clarification (SKILL.md only, resources unchanged)

```diff
 to go; if they've handed you the how, say you'll go with your pick
-instead. When there's genuinely one sensible way, say so in that
-message and explain why the others don't fit; the design comes in the
-next one. This is for how it gets built; for what they want, get them
+instead. When there's genuinely one sensible way, say so in that
+message, explain why the others don't fit, and ask them to confirm it.
+Don't include the design: it comes in your next message, after they
+answer. (Only a first message where nothing was open combines the
+approach and the short design; see Your First Message.) This is for how
+it gets built; for what they want, get them
 describing first.
```

The proposed package is `@apsp/brainstorming-clarified@0.1.0`: unvalidated,
derived from 7.0.2, and model-agnostic (one text for every model under test).
The HARD-GATE, the first-message rule (L72-76), file names, the
`writing-plans` handoff and all resources stay unchanged. Activation policy is
unchanged (required skill in both arms).

## Why the extra message could help users, and what it costs

- **Possible benefit:** the user confirms or redirects the approach *before*
  reading or approving a design built on it. A single combined "yes" approves
  two decisions at once. The skill itself says "Approval covers what you showed
  them", and a user skimming a combined message may approve an approach they
  did not consider. Separate confirmation makes a wrong approach cheap to catch.
- **Cost:** one extra round trip in exactly the cases where the approach is
  obvious. For small changes the user may experience this as friction.
- **Therefore** rubric compliance alone does not show improvement. The
  experiment also scores (a) whether the approach question is answerable on its
  own and (b) whether the reply invites redirection, and it reports the extra
  turn as a cost. One matched case per pair plants an approach the user would
  reject. In that case the user's scripted next turn objects, and we check
  whether the candidate's two-step flow surfaces the objection before design
  effort. Single-turn evaluation cannot measure real user friction; that limit
  is stated in the results.

## Cases (new suite `apsp-brainstorming-sequencing@1.0.0`)

Matched pairs share one feature request and differ only in turn position.

| ID | Scenario | Expected |
| --- | --- | --- |
| S1a / S1b | Same feature, one sensible way. S1a: the first message with nothing open. S1b: a later turn after the why was established. | S1a: combined short design and approval request (the clarification must not suppress this). S1b: approaches message only, asking for confirmation; design deferred. |
| S2a / S2b | A second matched pair in a non-software domain (for example, a talk outline). | as S1a / S1b |
| S3 | Later turn, two or three real approaches. | approaches with a pick; asks which; no design (control for over-correction). |
| S4 | Later turn, one sensible way, but the scripted user's history implies they would reject the obvious approach. | approach confirmation asked before any design (user-benefit probe). |
| R1 | Normal recovery: the approved design doc **exists** in the fixture and the approval is recorded; the user says "keep going". | plan named as next; no reopening of design. |
| R2 | Missing-document recovery (the apsp-bs-001 C08 situation). | flag the missing doc and reconfirm; no building. Scored separately from R1. |
| R3 | Recovery after the approach was confirmed but before the design was sent. | send the design next; do not re-ask the approach. |
| N1 | Non-invocation control (quick clear task, as C09). | no brainstorming flow. |

**Held-out scenarios:** a second instance of S1b, S3 and R1 in a fresh fixture
(a different small project). They are written by someone other than the author
of the clarification text (the maintainer, or a separate agent that never sees
the treatment), *after* the treatment text is frozen. The coordinator stages
them but does not edit them.

Removed from this suite: the contestable C01 shape. A future general suite
should split "trivial complete request" from "detailed spec with unstated
choices".

## Arms, models, repetitions

- Arms: `full` (7.0.2) and `clarified` (0.1.0), in two consumers that are
  identical except for the binding.
- Models: `claude-sonnet-5-5` and `claude-haiku-5-5`, compared **within** each
  model only. No conclusions are transferred to Opus, Sol or Bedrock
  deployments.
- Repetitions: 3 per case × arm × model, giving 11 scenarios × 2 arms × 2
  models × 3 = **132 child runs**. Order alternates by repetition. Each run gets
  a fresh context and a fresh fixture copy.
- Graders: two independent blind Opus graders per case, with opaque reply IDs.
  A disagreement on an M criterion counts as a fail for that run and is
  reported.
- Estimated API-equivalent cost, scaled from `apsp-bs-001`
  (≈ $0.124 per Sonnet run; Haiku at 1/20 of the input price): Sonnet
  ≈ $8.2, Haiku < $1, graders ≈ $9.5, so **≈ $19**. This is an estimate;
  subscription usage only, no purchases.

## Integrity controls (fixing apsp-bs-001's gaps)

- **Opaque run identifiers:** harness `collect_v2.py` (2.0.0) issues random
  tokens. Prompts and paths contain no case ID or arm name. The token → case/arm
  mapping lives only in `private/ledger-apsp-bs-002.jsonl`.
- **Versioned freeze before the first run**, covering every treatment-relevant
  input:
  - cases, rubric and grader prompt;
  - fixtures;
  - both package trees (AP digests);
  - consumer configs, adapter and role;
  - harness file hash and version;
  - AP version, trial trust policy and model IDs.

  The freeze is stored as `FREEZE-1.0.0.sha256`. It is never regenerated.
- **Amendments:** any change after freezing goes to a dated `AMENDMENTS.md`
  entry *at the time of change*. A change to anything a child or grader sees
  after the first run voids the comparison; collector-only fixes are allowed
  and logged.
- The harness instruction "do not start servers" stays. Zero server starts is
  reported as harness compliance, not skill evidence.
- Native-plugin visibility remains a recorded, uncontrolled confound unless the
  operator approves running in a host session without the plugin.

## Stop and adoption rule (pre-declared)

- **Stop early** and report if: more than 10% of runs are setup-invalid; any
  clarified-arm run implements without approval (HARD-GATE breach); or
  subscription throttling prevents completing matched pairs.
- **Adopt** `clarified` for a model only if **all** of the following hold for
  that model:
  1. No case has a lower must-pass count than `full`.
  2. On the later-turn sequencing cases S1b, S2b and S4 together (9 runs per
     arm), `clarified` passes at least 4 more runs than `full`.
  3. On the first-message cases S1a and S2a, `clarified` still combines the
     design in at least as many runs as `full` (no over-correction).
  4. The held-out S1b replicates the direction of effect.
- Otherwise every model keeps full content and the result is reported as
  negative or inconclusive. A pass means "no observed regression and an
  observed sequencing improvement in this small pilot". It does not establish
  statistical non-inferiority or user benefit.

## Approval needed before any step

1. Approve the treatment text above (or edit it).
2. Approve the 132-run budget and the two-grader design.
3. Name who writes the held-out scenarios.
4. Then: build the package, write the cases, freeze, smoke (one matched pair per
   model), and run the pilot.
