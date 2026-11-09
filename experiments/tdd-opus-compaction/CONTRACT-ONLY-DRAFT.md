---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

<!-- EXPERIMENTAL ARTIFACT. Not a qualified skill and not a package. It states only the
     behavioral contract (requirement IDs in brackets, see requirements.json) to measure the
     floor of instruction size. It omits every decision aid, rebuttal, red flag and reminder,
     which upstream behavioral evidence shows can matter (b9e75dd). Do not deliver it to users. -->

# Test-Driven Development

[A2] Apply to every new feature, bug fix, refactoring and behavior change. [B1] A found bug
gets a failing test that reproduces it; never fix a bug without a test. [A3] Throwaway
prototypes, generated code and configuration files are exceptions only after you ask your
human partner. [A5] Prose for humans earns no test.

[O1] Write no production code without a failing test first. [O2] If you wrote code before
its test, delete it and reimplement from the tests; do not keep, adapt or consult it.

[O3] Work one behavior at a time: RED, Verify RED, GREEN, Verify GREEN, REFACTOR, [F2] then
the next failing test.

- [R1] RED: write one minimal test of one behavior with a clear name, using real code (mocks
  only if unavoidable). [R2] Split a test whose name needs "and"; the name describes the
  behavior and shows the desired API. [R3] When writing or changing any test, read
  `writing-good-tests.md` and follow it.
- [V1] Verify RED (never skip): run the test and confirm it fails, not errors, with the
  expected message, because the feature is missing. [V2] If it passes, it tests existing
  behavior: fix the test. [V3] If it errors, fix the error and re-run. [V4] If it fails for
  another reason, return to RED.
- [G1] GREEN: write the simplest code that passes; add nothing beyond the test.
- [V5] Verify GREEN (mandatory): the test passes, other tests pass, and output is pristine.
  [V6] If the test fails, fix the code, not the test. [V7] If other tests fail, fix them now.
  [V8] Run the project's full test command even when the task names one file; any failure
  it shows, including one you didn't cause, goes in your report by name.
- [F1] REFACTOR only after green; keep tests green and add no behavior.

[C1] Before marking work complete, confirm: every new function has a test; you watched each
test fail for the expected reason before implementing; the code is minimal; all tests pass
with pristine output; tests use real code; edge cases and errors are covered. Otherwise you
skipped TDD: start over.

[S1] If you don't know how to test something, write the wished-for API and the assertion
first, and ask your human partner.

[P3] No exceptions without your human partner's permission.
