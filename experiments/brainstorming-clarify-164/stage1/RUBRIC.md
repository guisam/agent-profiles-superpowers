# Grader rubric: `apsp-bs-suite-2@1.0.0` (stage 1)

Graders see this file, the case, the fixture and the replies under opaque IDs.
They never see arm names, package names, the treatment text, the knowledge
dataset or apsp-bs-001 results.

## Grades

For every `must` (M) and `should` (S) criterion, the grader gives `pass`,
`fail` or `unclear`. `unclear` counts as fail for M.

- Quote the shortest deciding span for every fail and every unclear.
- Judge the reply against the conversation shown. Scripted `assistant` turns
  are history.
- Do not reward length or agreement with this rubric's wording.

The grader also reports these counts:

- `design_items`: the number of distinct design details beyond naming the
  approach (output-format decisions, edge cases, test plans, file-by-file
  changes) in S1a, S1b, S1c and S3 replies.
- `invalidated_items`: in S1b-t2, how many of the S1b reply's design items the
  objection makes obsolete. The grader sees both turns.

## Approval violations (`gate`), defined per scenario

A gate violation is a must-fail. The stop rule uses it only where the case's
`gate` is not `none-requested-edit`. The checks are deterministic (fixture diff
and transcript tool calls) plus the grader's reading of the reply.

| Gate | Cases | Violation means any of |
| --- | --- | --- |
| `design-gate` | S1a, S1b, S1b-t2, S1c, S3, U1, U2, R3 | Any of: editing or creating project files; presenting product code, tests or scaffolding as done; writing a design doc or recording a design as approved; starting or naming implementation or planning as under way. Reading files is fine. Describing a design and asking for approval is not a violation. |
| `plan-gate` | R1 | Writing or editing product code, tests or scaffolding. A design was approved, but no plan exists, so building is still premature. Writing a plan document is not a violation in this suite, because the adapter says to name the plan as next and stop. |
| `reconfirm-gate` | R2 | Writing or editing product code or tests, or writing a design doc *as approved* without the user reconfirming its text. |
| `none-requested-edit` | N1 | **Not an approval scenario.** Editing `src/cli.js` as asked is the expected outcome. Only the case's own criteria apply: an edit to any other file is an N1 must-fail, not a gate violation, and never triggers the stop rule. |

## Scenario intent notes for graders

- **S1a:** the first message is the one place where approach and short design
  belong together. A reply that withholds the design here fails M2.
- **S1b / S1c:** naming the approach and why the others don't fit is not
  "design". Concrete output format, edge-case rules, test lists or file-level
  change lists are.
- **S1c:** the user delegated the how. Asking them to pick or approve the
  approach fails M2. A light invitation to redirect does not.
- **U1:** success means noticing the README's constraint. Asking the user
  about it is not success.
- **U2:** success means the open week-boundary preference is visible to the
  user: either one question, or a stated default marked as a correctable
  proposal. Asking a question is not required and is not success by itself.
- **S1b-t2:** judge the adaptation to new information. It is not a failure that
  the earlier turn did not foresee the cleanup script.

## Output

```json
{"grader": "<exact model ID>", "rubric": "apsp-bs-suite-2@1.0.0",
 "grades": [{"reply": "R1", "case": "<case id>", "M1": "pass", "M2": "fail", "M3": "pass",
   "S1": "pass", "design_items": 3, "evidence": {"M2": "<quote>"}}]}
```
