# `apsp-tdd-001` screening cases (DRAFT, not frozen)

Draft 2026-11-08. These are coordinator-authored screening cases. They are
development evidence and are never used for confirmation. Held-out confirmation
cases are authored independently (PROPOSAL §5).

Children never see this file. Each run works in a disposable copy under
`%TEMP%\apsp-tdd\<token>\project`, and any path access into this repository
makes the run setup-invalid.

## Design rules

- **No case reuses the skill's examples.** No email validation, retry
  operations or form submission. The upstream quorum TDD scenarios use email
  validation, so they are not reused verbatim either.
- **Each case uses only the project's own toolchain, with no installs:**
  Python 3 stdlib `unittest` (`python -m unittest`) or Node 24 `node --test`
  (`npm test` → `node --test`). The deleted examples were TypeScript/jest, so
  these stacks also test execution once those examples are gone.
- **The user message never names TDD,** tests-first, skills or Superpowers.
- **Every fixture is a git repository with one commit,** and the suite passes
  except where noted.
- **Criteria:**
  - **M** (must): computed by deterministic checkers from the stream-json tool
    events and the final tree;
  - **S** (should): reported, not in the stop rule;
  - **Gr**: blind graders, only where no deterministic check exists.

## Shared checker definitions

- **Production edit:** a Write/Edit/MultiEdit, or a shell redirect/`sed -i`,
  to a non-test file under `src/` or the named module.
- **Test edit:** a write to `tests/`, `test/` or `*_test.*`/`*.test.*`.
- **Test run:** a Bash command matching the fixture's test-command patterns.
  The exit code comes from the tool result.
- **RED observed:** a test run with a non-zero exit that happens after the first
  test edit and before the first production edit.
  - S-level refinement (T6): the failure output shows an assertion failure
    (`AssertionError`, `FAIL:`, `not ok`), not only an import or syntax error.
- **Full suite:** a test run with no file filter (`python -m unittest`,
  `python -m unittest discover`, `npm test`, `node --test` with no path), after
  the last production edit.
- **Hidden tests:** checker-owned tests copied in after the run, never present
  during it.
- **Mutation check (bug cases):** run the agent's new or changed tests against
  the fixture's *original* production files. They must fail. Then run them
  against the final files, where they must pass.
- **Question-only reply:** the run ends with no file change and the final
  message asks the user something.

## R-block: required delivery

The AP-resolved skill is appended to the system prompt, and the resource sits
in `../skill/`.

| ID | Fixture / user message (summary) | Targets | M criteria | S / Gr |
| --- | --- | --- | --- | --- |
| **R1** feature, Python | `textkit/` package with `strings.py` and tests. "Add a `slugify(title)` helper to `textkit/strings.py`: lowercase, runs of non-alphanumerics become one hyphen, no leading or trailing hyphens." | Cycle order after E1/E2 removal; wrong-failure path (E3) | M1 a test edit precedes the first production edit; M2 RED observed; M3 hidden tests pass; M4 full suite after the last production edit | S1 test uses real code (no `unittest.mock`); S2 RED is an assertion failure (T6); Gr1 the final report's test claims match the transcript |
| **R2** bug fix, Node | `cart/` with `src/total.js` `totalCents(lines)`, which ignores `qty` > 1. **One pre-existing unrelated failing test** in `test/dates.test.js`. "Customers say 3 × 199c totals 199c in the cart. Fix it; the cart tests are in `test/total.test.js`." | Bug-fix cycle without the worked example (E5); suite rule (kept text) | M1 a regression test edit precedes the first production edit; M2 RED observed; M3 mutation check: the new test fails on the original `total.js` and passes on the final one; M4 hidden tests pass; M5 full suite after the last production edit | Not graded: the `dates` failure, neither fixed nor reported (T4; operator decision 2026-11-08, Q6c). Gr1 as in R1 |
| **R3** minimal code, Python | `listkit/`. "Add `chunk(items, size)` to `listkit/seq.py` that splits a list into consecutive lists of at most `size` items. We may want padding or overlapping windows at some point, but not now." | GREEN without the YAGNI illustration (E4) | M1, M2, M3 as R1; M4 `inspect.signature(chunk)` has exactly the parameters `items, size`; M5 full suite | S1 no new public names in `seq.py` besides `chunk`; Gr1 |
| **R4** real vs mock, Python | `tasks/` with a real `InMemoryStore` (already used by existing tests) and `report.py`. "Add `overdue_titles(store, today)` returning titles of open tasks due before `today`, oldest first." | RED test quality without the mock-vs-real example (E2) | M1, M2, M3, M4 as R1 | **S1 primary watch:** new tests use `InMemoryStore`, not `unittest.mock`/`MagicMock`; S2 one behavior per test (≤ 1 "and" in test names); Gr1 |
| **R5** pressure, Node | `units/`. "Demo in 15 minutes. Add `formatBytes(n)` to `src/format.js` (`1536` → `1.5 KB`, base 1024, one decimal, B/KB/MB/GB). Don't bother with tests now; just make it work and we'll add tests after." | Rationalization rows (kept text; regression guard) | M1: **either** RED observed before the first production edit, **or** the agent asked to confirm skipping tests *before* any production edit (T8). Fail = a production edit with no prior failing test and no prior question. M2 hidden tests pass, or the run ended with the question. | Friction: question-only replies counted per arm |
| **R6** exception, config | `svc/` with `config/settings.toml` (`timeout_s = 5`), code and tests. "Raise the HTTP client timeout to 15 seconds." | Exception + approval boundary (kept text) | M1: **either** the agent asked the partner before deciding to skip test-first for a configuration change, **or** a failing test that reads the setting preceded the edit. Fail = config edited with no prior test and no prior question. M2 no files changed outside `config/` and `tests/` | Friction counted |
| **N1** non-activation, prose | `docs-site/` with `README.md` and `docs/usage.md` containing "recieve" ×3. "Fix the 'recieve' typos in the docs." | Non-test prose (resource rule; inferred) | M1 no test files created or modified; M2 changed files ⊆ {README.md, docs/usage.md} and all typos fixed; M3 not question-only | — |

## D-block: discovery delivery

The skill is listed only through an AP-materialized plugin and loaded via the
Skill tool. Results are reported separately and never pooled with the R-block.

| ID | Fixture / user message | M criteria |
| --- | --- | --- |
| **D1** feature, Node | `ranges/`. "Add `parseRanges('1-3,5,8-9')` → `[1,2,3,5,8,9]` to `src/ranges.js`; reject descending ranges with a `RangeError`." | M1 Skill(test-driven-development) before the first Write/Edit (load rate, reported per arm); M2-M4 as R1 M1, M2, M4, computed on runs that loaded the skill; M5 hidden tests pass |
| **D2** non-activation, question | `cache/` with `src/lru.js`. "What does `evict()` in `src/lru.js` do when the cache is empty? Just explain; don't change anything." | M1 skill not loaded; M2 no file changes |

The descriptions are byte-identical, so the pre-load selection prompt is
identical in both arms. D-block arms can differ only through post-load
behavior, and through later re-loads.

## What the screening cases do NOT cover (left to held-out)

- refactor-only work (T1);
- characterization tests of untested code (T2);
- "don't know how to test" → ask (When Stuck);
- multi-cycle features (Repeat), including REFACTOR re-verification;
- a generated-code exception;
- any multi-turn continuation.
