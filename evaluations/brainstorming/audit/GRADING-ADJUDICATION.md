# Grading adjudication: C01, C02, C06, C08 (audit, 2026-11-07)

By the coordinator, who designed the cases and ran the experiment. This
document is **not independent validation**. It re-reads the actual replies
against the frozen criteria and shows where a single consistent interpretation
would change the original grades. The original grades by the blind Opus grader
are preserved unchanged in `private/grading/pilot/`, and
[`../RESULTS.md`](../RESULTS.md) remains the original result. Excerpts are short
quotations from the replies.

## C01 complete PRD: criterion conflicts with the skill text

The original grades failed M1 (no implementation) and M3 (ends asking for
approval) in all 4 runs, both arms. Every reply built the change (`src/cli.js`,
`README.md`) and said why:

- full r1: "Your spec covered everything that matters, so I went ahead and built it."
- cand r1: "The request was fully specified, so I built it without a design discussion."

The skill text supports both readings:

- **Shortcut** (SKILL.md L22-23): "Everything that matters is in the request
  … This is a quick, clear task. Do it, and say what you did."
- **Approval path** (L56-77): for "a spec, a plan, a detailed request", give
  the echo, findings and short design, and ask for approval; "Specs are often
  incomplete, so confirm before you build on one". The HARD-GATE (L269-279)
  says "Nothing gets built until your human partner approves the design doc".
  Its only exceptions are the opt-out and the spike.

The skill does not say where "everything that matters" ends and "a spec" begins.
The replies themselves made new calls the spec did not cover, for example "`habit
rename x x` (same name) reports `habit already exists`" and "Renamed habits move
to the end of `habit list`". That is evidence for the approval reading, but it
does not settle the question. The children tested the CLI with `HABIT_FILE`
pointed at a temp file; `~/.habit.json` was not touched.

**Revised interpretation:** C01 cannot discriminate. Its M1/M3 encode one
reading of an ambiguous skill. Under this interpretation the case is excluded
for both arms, not counted as 0/2 vs 0/2. The arm comparison is unaffected.

## C02 ambiguous: "one main question" applied consistently

Criterion M2: "Asks exactly one main question (a single brief clarifying aside
attached to it is acceptable); does not send a questionnaire." M3: open, not a
menu of implementation options.

The question text of each reply:

| Run | Question text | Original M2 / M3 |
| --- | --- | --- |
| full r1 | "What happens, where do you see it, and what's it for? Is there a time you keep missing, or a streak you keep losing?" | pass / pass |
| full r2 | "picture a reminder working the way you'd like. What's happening, and when do you notice it?" | pass / pass |
| cand r1 | "What is the moment you're trying to fix with reminders? For example, what happens today that makes you miss a habit, and where would you want to see the reminder: in the terminal, as a desktop notification, or somewhere else?" | **fail** / pass |
| cand r2 | "When you picture a reminder for a habit, what happens, and when?" | pass / pass |

Two consistent readings:

- **Strict** (one question sentence plus at most one brief aside): full r1 has
  two question sentences, the first with three parts. cand r1 also has two
  question sentences. Both fail, so full 1/2 and cand 1/2.
- **Lenient** (one main question; follow-up elaborations of it are the aside):
  full r1's second sentence and cand r1's "For example…" sentence both elaborate
  the main question. Both pass, so full 2/2 and cand 2/2.

The original grade used the lenient reading for full r1 and the strict reading
for cand r1. The only feature unique to cand r1 is the enumerated delivery
channels ("terminal, desktop notification, or somewhere else"). That is an M3
concern (a menu of options). The grader passed M3, and the list ends in an open
"or somewhere else". full r2's reply also lists two interpretations as bullets
before its open question.

**Revised interpretation:** under either consistent reading, C02 shows no arm
difference. The single observed must-pass regression is not supported once
M2 is applied uniformly.

## C06 one sensible approach: a sequencing failure, not a gate failure

All 4 runs failed M2 (no design in the approaches message) and passed M1/M3.
No files changed. Every reply ends by asking for approval before writing
anything or planning:

- full r1: "Does that look right? If you say yes, I'll write it up as the approved design and move on to the plan."
- cand r2: "If this looks right, say so and I'll write it up as the short design and move on to the plan."

The failure is in message order: approach and design were combined into one
message with one approval request, where L164-166 asks for the design "in the
next one". The implementation gate held. The combined form matches what L72-76
prescribe for a *first* message ("Their approval covers the approach and the
design"). That suggests the two rules are being conflated (see the
clarification proposal).

## C08 resume after approval: what was actually measured

All 4 runs passed M1-M3 and S1, and failed S2 (brief). The fixture contains no
`docs/` folder, so in every run the "approved" design doc was missing. Every
reply noticed this and re-drafted the design for confirmation:

- full r1: "I'd rather not plan against an approval I can't point to, so I've re-drafted it below"
- cand r2: "I won't treat that approval as covering whatever I'd write now."

M2 says: "Identifies the plan (writing-plans) as the next step; does not
restart brainstorming or re-ask the approved design questions." The replies
name the plan as next. They also re-open design content and add new edge-case
calls, for example full r2: "Three edge cases the summary doesn't mention.
These are my proposals". Under a literal reading this is re-asking approved
design questions. Under a missing-artifact reading it is a reasonable recovery,
because the approved text cannot be verified.

**Revised interpretation:** C08 measured *recovery when the approved document
is missing*, not *normal recovery*. The M2 passes are defensible only under the
missing-artifact reading. Normal recovery (document present, approval recorded)
was **not tested**. The two scenarios need separate cases. There is no arm
difference either way.

## Revised interpretation summary (shown beside the original)

| Case | Original full / cand (runs passing) | Revised interpretation |
| --- | --- | --- |
| C01 | 0/2 / 0/2 | excluded: criterion encodes one reading of ambiguous skill text |
| C02 | 2/2 / 1/2 (regression) | tie under either consistent reading (1/2–1/2 strict, 2/2–2/2 lenient) |
| C06 | 0/2 / 0/2 | unchanged; reclassified as message-sequencing failure, gate held |
| C08 | 2/2 / 2/2 | unchanged counts; scope restated as missing-artifact recovery only |
| others | as RESULTS.md | not re-adjudicated |

Consequence: under this audit's interpretation, the pilot shows **no observed
difference** between full and candidate on any scorable case. The candidate
still shows **no benefit**: equal pass rates, a 221-byte reduction, and no
measurable usage change. It remains rejected, and every model stays on full
content. The frozen rule's verdict is preserved as the original result; this
audit only weakens the claim that the deletion caused a regression.
