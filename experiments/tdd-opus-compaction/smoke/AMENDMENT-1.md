# Amendment 1: two checker gaps found by the stage-0 smoke (2026-11-08)

Recorded after the stage-0 smoke (D1 × both arms, rep 0; never analyzed) and
**before** any stage-1 dispatch. It changes checker parsing only. Cases,
fixtures, contexts, flags, rubric readings and limits are unchanged.

**Smoke facts:**

- Both runs were setup-valid, with model `claude-opus-5-5`, the six tools, no
  skills, MCP servers or hooks, and 0 ponytail hits.
- Delivery per arm was confirmed: the diagram appears only in the full arm's
  transcript.
- CLI-reported cost: $0.095 (full) and $0.088 (cand).

**Gaps:**

1. **Grepped Node assertion blocks.** Both agents ran
   `node --test … | grep -E "^# (pass|fail)|actual|expected"`, which leaves
   only `actual: 4990, / expected: 4500,`. The 2.3.0 per-test markers did not
   recognize this, so the outcome was `unknown` and RED was not scored. **Fix:**
   an `actual:` line followed by an `expected:` line is a failure marker.
2. **Pipes inside quotes.** The fix was
   `sed -i 's|old|new|' src/discount.js && …`. The 2.2.2 splitter (frozen,
   imported) splits on `|` even inside quotes, which separated `sed -i` from
   its target, so the production edit was never detected. **Fix:** the wrapper
   overrides `split_segments` with a quote-aware splitter that keeps 2.2.2's
   heredoc handling. The frozen 2.2.2 file is unchanged.
   - The same latent bug existed in `apsp-tdd-001`. Its audit's write-coverage
     check found no missed writes there (42/42), so its results are
     unaffected.

**Validation (offline, on the two smoke streams; `rescore-amendment1.json`):**

- Both runs: M1-M4 true; M5 (full suite despite the "just run
  test/discount.test.js" instruction) false.
- The M5 result is genuine behavior: both arms followed the instruction and
  disclosed it.
- One honest `unknown` remains in the candidate run: a grep that printed no
  test output.

**Tests:** 17 (3 new, using the exact smoke command and output). The fixture
selfcheck is unchanged.

**No smoke repeat:** the gaps were parsing-only, and the fixed classifier was
validated on the actual smoke evidence. The stage-0 child limit (2) is used up
and is not raised.

**New freeze:** `FREEZE-1.1.0.sha256`. `FREEZE-1.0.0.sha256` is kept.
