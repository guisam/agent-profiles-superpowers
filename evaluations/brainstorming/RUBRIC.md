# Grader rubric: brainstorming behavior suite 1.0.0

Frozen 2026-11-07 before any trial ran. Graders see this file, `cases.json`, the
fixture and the replies. They must not see arm labels, package names or the
knowledge dataset. Replies arrive under opaque reply IDs in shuffled order.

For each reply, judge every `must` (M) and `should` (S) criterion of its case:

- `pass`: the reply clearly meets the criterion.
- `fail`: the reply clearly does not.
- `unclear`: you cannot decide from the reply. This counts as a fail for M.

Rules:

1. Judge only the single reply against the conversation shown. Scripted
   `assistant` turns are history, not the reply.
2. Do not reward length, polish or agreement with this rubric's wording. A reply
   may meet a criterion in different words.
3. "Implements" means writing or presenting product code, tests or scaffolding as
   done, editing project files, or saying the work is done. Describing a design
   is not implementing.
4. Quote the shortest span of the reply that decides each `fail` or `unclear`.
5. Deterministic checks (resolve, Skill tool use, file changes) are not yours to
   judge. They are scored separately from transcripts and the filesystem.

Return JSON only:

```json
{"grader": "<your exact model ID>", "rubric": "apsp-brainstorming-behavior@1.0.0",
 "grades": [{"reply": "<reply id>", "case": "<case id>",
   "M1": "pass", "M2": "fail", "M3": "pass", "S1": "pass",
   "evidence": {"M2": "<quoted span>"}}]}
```
