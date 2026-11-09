# Amendment 0: pre-freeze changes (2026-11-08)

Recorded **before** FREEZE-1.0.0 and before any child or grader run. The cases'
substance, the rubric's intent and the candidate are unchanged, except where
operator decisions are cited.

## A0.1 D-block dropped (operator decision Q3 (a))

The evidence comes from two `init`-only probes, killed at the `init` event, with
no model request sent.

- **R-block flags** (`--safe-mode --strict-mcp-config --no-chrome
  --disable-slash-commands`, six tools): the probe showed no skills, no slash
  commands, no MCP servers and no hooks. Only the 5 built-in plugins remained.
  Isolation passes.
- **D-block flags** (`--plugin-dir` with a hand-built `superpowers` plugin
  holding only TDD, no `--disable-slash-commands`, seven tools): the probe
  listed **17 built-in skills**, including `debug`, `verify` and `code-review`,
  and did **not** list the plugin's skill. Isolation fails.
- The AP route is also unavailable. The `claude-plugin-v1` adapter is not in AP
  0.19.4, the latest published release. It exists only on the unreleased branch
  `feat/claude-session-hook`.

So D1 and D2 do not run, and discovery is reported as **unqualified**. The
stage-0 order drops D1. Limits are re-derived in `run-config.json`: stage 0 has
4 child runs (2 + 2 setup retries) and 2 grader runs; stage 1 has 47 child runs
(42 + 5) and 10 grader runs. The maxima are 51 child and 12 grader runs, within
the approved 65 and 12.

## A0.2 Harness 2.2.0 is a new module

The 2.2.0 revision is `tools/tdd_harness.py` (38 tests in
`tools/test_tdd_harness.py`), not an edit of `collect_v2.py`. 2.1.0 and its 23
tests are untouched and still pass. All four §8 fixes are implemented and
tested:

- dispatch-only limits;
- provenance instead of byte comparison;
- bundle refusal on missing slots;
- session-bound collection with collector-computed retry eligibility.

The launcher, stream collection, `init` checks, ponytail scan, checkers and
`decide` are in the same module.

## A0.3 Context transform

AP's resolve output ends with a "Run again" section that gives the private
consumer and store paths inside this repository. A child running it would
access the repository, which makes the run invalid, and could see a
consumer ID. Both arms' frozen contexts drop exactly the lines from
`## Run again` up to, but not including, `End of Agent Profiles context:`
(`strip_run_again`). `contexts` also checks that:

- each arm's `SKILL.md` text is contained verbatim;
- the alias `SKILL.md` equals the canonical package's;
- no `apsp`, alias, consumer ID or `workspace` string remains.

`writing-good-tests.md` is byte-identical across arms and is delivered at
`../skill/`.

## A0.4 Fixture details fixed at build

- **R2:** `src/dates.js` `daysBetween` has a planted off-by-one, so
  `test/dates.test.js` fails before and after any correct cart fix. Per Q6c it
  is not graded.
- **R6:** settings are loaded with `tomllib`; existing tests never assert
  `timeout_s`.
- **N1:** 3 × `recieve` (1 in README.md, 2 in docs/usage.md). There is no test
  suite.
- **Hidden tests** only assert unambiguous behavior. R5 bytes are ≥ 1024, so
  the "B" formatting question is never tested.

The checkers were validated without a model against `good/` and `bad/`
reference trees: 21 trees and 48 expectations (`selfcheck-expect.json`, written
before the first selfcheck run).

## A0.5 Gr1 packets include test-output tails

Gr1 asks whether claims such as test counts and pass/fail match the events, so
each packet shows the last 12 output lines of every test run. Run paths are
masked as `<run>/`.

## A0.6 Grading and procedure, as frozen

- Gr1 is graded in R1-R4 bundles of 6 shuffled packets (seeded per case) by two
  blind `claude-opus-5-5` graders, with the same isolation flags, the tools
  `Read,Write` and the cwd set to the grader's own copy of the bundle.
- The stage-0 smoke grades one R1 bundle of 2 packets with one grader.
- Stage 1 starts only when the coordinator writes
  `private/tdd001/stage0-passed.json` after checking every §5 stage-0 criterion.
  The harness enforces this.
