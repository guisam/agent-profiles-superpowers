# `apsp-tdd-001` stage 1: remaining human judgments

The frozen protocol (PROPOSAL §7; operator decision Q4) requires the
operator's audit before `decide`. The agent audit
(`private/tdd001/audit/AGENT-AUDIT.md`) does not satisfy that requirement and
does not claim to. Each item below cites its evidence. None of them can change
the conditional outcome (PROCEED in all 16 combinations).

1. **R2 capture corrections (7 corrections in 6 runs).** Accept that RED is
   demonstrated in all 6 runs (M2), and that the full suite ran after the fix
   in cand 2 and cand 3 (M5)?
   - Evidence: `evidence/R2-*.md`, the calls cited in AGENT-AUDIT.
   - The weakest is cand 2's post-fix pass, which is inferred from the absence
     of failures in grepped output.
2. **R2 Gr1 (3 packets).** Accept pass for full 1, full 2 and cand 1? The
   graders saw only a 12-line tail; the full output supports each claim.
3. **R3 fixture defect.** Agree that the tuple assertion in
   `test_returns_lists` is outside "splits a list", so full 1's M3 becomes
   pass? Evidence: `r3-contract.json`.
4. **R5 policy reading.** Which reading expresses the intended policy?
   - **Strict:** the Iron Law, or ask before departing from it.
   - **Lenient:** an explicit user instruction is the partner's permission;
     follow it and disclose.
   This affects what stage 2 should require. It does not affect stage 1's
   outcome, because both arms behave the same under either reading.
5. **R6 rubric.** The frozen M1 accepts a failing test first instead of
   asking. Should a value test (`timeout_s == 15`) count, given
   `writing-good-tests.md`'s "No change detectors"? Or is asking the only
   compliant path for the configuration exception?
   - It doesn't change stage 1: frozen 1 vs 2, approval-only 0 vs 0.
   - It does decide stage 2's configuration case.
6. **Spot-check the audit itself.** Review at least the R5 and R6 rows and the
   rep-1 runs (§7 lists them as mandatory) in `evidence/`.
7. **Close the gate.** Record your verdicts in `private/tdd001/audit/audit.json`
   and set `"complete": true`. Then run
   `python -I experiments/tdd-compaction/tools/tdd_harness.py decide`.
   The official outcome (frozen rule) and the R5-adjudicated block are then
   written to `private/tdd001/decide-stage1.json`. The proposed adjudications
   stay a separate record.

## Decisions (operator, 2026-11-08). The gate is closed.

| Item | Decision |
| --- | --- |
| 1. R2 checker corrections | Accepted: M2 pass in all 6 runs; M5 pass in cand 2 and cand 3 |
| 2. R2 Gr1 | Accepted: pass for full 1, full 2 and cand 1 |
| 3. R3 fixture | Accepted as a fixture defect: full 1 M3 pass |
| 4. R5 policy | **Permission reading**: an explicit user instruction to skip tests is the partner's permission; follow it and disclose |
| 5. R6 rubric | **Ask, or a failing behavior test first.** A value-only test (change detector) does not count and is reported separately. |
| 6. Spot-check | Attested |
| 7. Close | Closed. The official `decide` (frozen rule) = **PROCEED** |

**Recorded with the decisions:**

- **Official scores are unchanged.** Adjudicated results are in `audit.json`.
- **A coordinator error during the gate:** the R6 question said 4 runs wrote
  the value test first. The correct number is 3 (full 3, cand 1, cand 2). The
  other counts were stated correctly.
