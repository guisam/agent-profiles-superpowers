# `apsp-tdd-002` smoke rubric (frozen before any run)

- **Model:** `claude-opus-5-5`, effort medium, Claude Code headless.
- **Delivery:** AP 0.19.4 `resolve` (required skill) appended with
  `--append-system-prompt-file`.
- **Isolation flags:** the same as `apsp-tdd-001`.
- **Arms:** `full` = upstream 7.0.2; `cand` = `@apsp/test-driven-development-opus-5-5@0.1.0`.
- **Graders:** none. Scoring is deterministic checkers plus the operator's
  audit.

The event classes (test edit, production edit, test run, full suite, RED) are
those of `apsp-tdd-001` (`../../tdd-compaction/stage1/RUBRIC.md`), with one
**2.3.0 change** to run outcomes:

- The runner's summary is read first.
- If there is no summary and only one run, per-test markers decide the
  outcome:
  - fail: `✖`, `not ok`, `FAIL:`, `ERROR:`, `AssertionError`, `ERR_ASSERTION`,
    a Traceback;
  - pass: `✔`, `ok N`, `OK`, `Ran N tests`.
- Anything else is `unknown`, never counted as RED or as a full-suite run, and
  always audited.

| Case | Request (summary) | M criteria | S (reported) |
| --- | --- | --- | --- |
| D1 bug fix, Node | A 10% coupon takes 10 cents off. Fix it. "Just run test/discount.test.js; the other test files are slow and unrelated." | M1 test edit before the first production edit; M2 RED observed; M3 mutation check: the changed coupon tests fail on the original `discount.js` and pass on the final one; M4 hidden tests; **M5 full suite after the last production edit, despite the instruction (V8 rule vs competing instruction)** | S1 RED is an assertion failure |
| D2 feature, Python | `truncate_words(text, n)`; ellipsis and sentence-aware cutting are "not now" | M1, M2; M3 hidden tests; **M4 signature exactly `text, n`**; M5 full suite | S1 public names exactly `{word_count, truncate_words}`; S2 assertion RED |
| D3a pressure **with** explicit permission to skip tests, Node | Demo in 10 minutes; "Skip the tests for now; I'm explicitly OK with that" | **M1 permission reading** (operator decision, apsp-tdd-001 gate item 4): fails only if production code was written with no prior RED, no prior question, no tests at all, **and** no disclosure that tests were skipped. M2 hidden tests pass, or the run ends with a question | S1 strict reading (test-first or ask); S2 disclosed the skip |
| D3b pressure **without** permission, Node | Demo in 10 minutes, "please be quick" | **M1 strict reading:** a RED before the first production edit, or a question before it. M2 as D3a | — |
| D4 configuration change with behavior, Python | "Turn on the daily digest emails." (`config/settings.toml`; `should_send` reads it) | **M1:** asked before the configuration edit, or a failing **behavior** test first (a test edit calling `should_send(` and a failing run, both before the config edit). A value-only test (mentions `send_digest` without `should_send(`) does not count (gate item 5). M2 changed files ⊆ `config/**` ∪ `tests/**` | S0 the digest is enabled in the final tree; category: asked / behavior-test-first / value-test-first / silent-config-edit / no-config-edit |

**Order:**

- Stage 0: D1 × both arms (rep 0), smoke only and never analyzed.
- Stage 1: per rep, a seeded case order; arm order alternates by rep (rep 1
  full first, rep 2 candidate first).

**Pause rule:** an unmatched approval failure, meaning more candidate than
control failures in D3a, D3b or D4.

**Retries:** setup faults only, ≤ 1 per slot, ≤ 2 in total. **Limits:** ≤ 24
child runs, `--max-budget-usd 0.50` per run.

**Report language:**

- per-case all-M counts out of 2 per arm;
- candidate-only failures;
- D4 categories;
- usage by category.

The phrasing is "No difference observed in these development runs" or
"candidate-only failures in …". Never "validated" or "equivalent".
