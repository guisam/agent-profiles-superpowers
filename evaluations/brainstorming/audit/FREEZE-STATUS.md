# Freeze status of `apsp-bs-001` (audit, 2026-11-07; revision 2)

Written after the experiment. This is the coordinator's own audit, not
independent review. The original `../FREEZE.sha256` is preserved unchanged and
is **not** regenerated. Two of its entries no longer match.

Revision 2 separates what file contents establish from what timestamps only
suggest. Revision 1 stated some timing inferences too strongly.

## Current check

`sha256sum -c ../FREEZE.sha256` from `evaluations/brainstorming/`:

| File | Frozen hash | Current hash | Status |
| --- | --- | --- | --- |
| cases.json, RUBRIC.md, fixture/* (6), selectors/* (4) | as recorded | same | match |
| PROTOCOL.md | `ac9b4351…` | `9d587f67…` | **mismatch** |
| tools/collect.py | `b80dff08…` | `298eaee4…` | **mismatch** |

## Established by content (hash reconstruction)

These facts follow from bytes and hashes. They do not depend on any clock.

1. **PROTOCOL.md.** Deleting exactly one paragraph, the one starting
   "Post-smoke amendments", from the current file reproduces the frozen hash
   `ac9b4351…`. So the frozen protocol is known byte-for-byte, and that
   paragraph is the only difference.
2. **collect.py.** Reversing three identified edits on the current file
   reproduces the frozen hash `b80dff08…` exactly. The reconstruction is
   [collect.frozen-reconstructed.py.txt](collect.frozen-reconstructed.py.txt);
   the diff is [collect.freeze-to-final.diff](collect.freeze-to-final.diff).
   The edits:
   - (a) transcript-final-text reply recovery and `reply_source`;
   - (b) the `prompt_exact` check;
   - (c) `bundle` and `score`.

   None touches `prompt()`, delivery detection, usage extraction or the
   deterministic file checks.
3. **Prompt identity.** Because `prompt()` is identical in the frozen and final
   collector, and all 44 transcripts' first user message equals the rendered
   prompt (`prompt_exact` 44/44), every child received the frozen prompt
   template.
4. **Recorded results.** Every stored `result.json` contains the fields
   `reply_source` and `checks.prompt_exact`. Only the final collector writes
   both, so every stored result was written by the final `collect.py`
   (`298eaee4…`).
5. **Grades.** All 12 original grade files pass the stricter v2 validator, and
   `scores.jsonl` contains no `"missing"` values.

## Supporting chronology (timestamps; weaker evidence)

The sources are file mtimes (local −08:00, shown here in UTC) and the `at`
fields in `runs.jsonl`. mtimes are filesystem metadata: they record a file's
last modification and can be changed by later copies or edits. Ledger
timestamps come from the collector's own clock. Neither is tamper-evident,
and neither records intermediate versions. Read the items below as consistent
with the coordinator's account, not as proof.

- **Freeze written before runs:** the `FREEZE.sha256` mtime is 20:16:07Z. The
  first `planned` ledger event is 20:16:13Z and the first `collected` is
  20:16:53Z. This suggests the freeze was written before any run.
- **Post-smoke paragraph written last:** the PROTOCOL.md mtime is 20:46:00Z,
  after the last `collected` event (20:42:07Z). This suggests the post-smoke
  paragraph was *written* after all runs, although its heading names the time
  of the collector changes. The mtime shows only the last modification.
- **Collector edits during the pilot:** the collect.py mtime is 20:21:15Z.
  Re-collection events are C04 r1 at 20:17:54Z and C04 r1 + C01 r1 at
  20:21:16-17Z. This fits edits made during the pilot, with the four earliest
  runs re-collected under the final version. The other 40 runs' first
  `collected` events come after 20:21:15Z.

## Rests on the coordinator's account only

- An earlier `FREEZE.sha256` existed before the "pre-run amendment" (trust env
  in the prompt, content-based variant detection, adapter `--json` lookup). It
  was overwritten when the suite was re-frozen before the smoke run. It is not
  preserved and cannot be verified.
- The order of amendments: (a) and (c) between the smoke runs and C01 r1, then
  (b) after C01 r1.

## Assessment

The content evidence establishes that the treatment-relevant inputs a child or
grader saw were unchanged through the 44 runs: cases, rubric, fixture,
selectors, adapter and prompt template. It also establishes exactly how the
protocol and collector differ from the freeze. *When* those differences were
introduced is supported only by timestamps. Future freezes must cover the
harness and prompt template. Amendments must be logged in a dated file at the
time of change; see the apsp-bs-002 proposal.
