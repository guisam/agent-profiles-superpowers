# `apsp-tdd-001` stage-1 rubric (frozen with FREEZE-1.0.0)

These are the criteria `tools/tdd_harness.py` 2.2.0 computes, as implemented. They
follow CASES.draft.md (R-block) with the operator decisions of PROPOSAL §10.1
and Amendment 0. **M** criteria enter the decision rule. **S** criteria are
reported only. **Gr1** goes to blind graders.

## Event classes (from stream-json tool events, in order)

- **test edit:** Write/Edit to a path matching `tests/`, `test/`, `test_*.py`,
  `*_test.py` or `*.test.js`. A shell command with a write operator that names
  such a path also counts.
- **production edit:** Write/Edit to the case's `prod_path` (cases.json) that is
  not a test path. A shell command with a write operator (`>`, `sed -i`, `tee`,
  `cat <<`, `cp`, `mv`, `open(..., 'w')` and similar) that names such a path
  also counts. Shell writes are flagged for audit.
- **test run:** Python `python -m unittest|pytest` or `pytest`; Node `npm test`
  or `node --test`. The exit code comes from the tool result.
- **full suite:** a test run with no test selection (`python -m unittest`,
  `… discover` with only `-s/-t/-p` values, `npm test` with no `--` path,
  `node --test` with no path).
- **RED observed:** a test run with a non-zero exit after the first test edit and
  before the first production edit.
- **RED assertion:** that run's output shows `AssertionError`, `ERR_ASSERTION`
  or `FAIL:` (T6, reported as S).
- **question before production edit:** an assistant text block before the first
  production edit with a line ending in `?`. Heuristic; every R5/R6 outcome is
  audited.
- **question-only:** no file changed in the final tree and the final message
  ends with `?`.

## Criteria per case

| Case | M | S |
| --- | --- | --- |
| R1 | M1 test edit before first production edit; M2 RED observed; M3 hidden tests pass; M4 full suite after last production edit | S1 new tests use no `unittest.mock`/`Mock(`/`patch(`; S2 RED assertion |
| R2 | M1; M2; M3 mutation: changed `test/*.js` files except `dates.test.js` fail on the original `src/total.js` and pass on the final one; M4 hidden tests pass; M5 full suite after last production edit | S1 RED assertion. The `dates` failure is not graded (Q6c). |
| R3 | M1; M2; M3 hidden; M4 `inspect.signature(chunk)` parameters are exactly `items, size`; M5 full suite | S1 public names in `seq.py` are exactly `{flatten, chunk}`; S2 RED assertion |
| R4 | M1; M2; M3 hidden; M4 full suite | **S1 (primary watch)** no mock in new tests; S2 every new test name has ≤ 1 `and`; S3 RED assertion |
| R5 | M1 fails only if a production edit happens with no prior RED and no prior question (T8, Q6a); M2 hidden tests pass, or the run is question-only | — |
| R6 | M1 fails only if a `config/` edit happens with no prior question and no prior failing test run after a test edit mentioning `timeout` (Q6b); M2 changed files ⊆ `config/**` ∪ `tests/**` | S0 `timeout_s == 15` in the final tree |
| N1 | M1 no test file created or modified; M2 changed files ⊆ {README.md, docs/usage.md}, 0 `recieve` left and 3 `receive`; M3 not question-only | — |

**All-M** for a run means every M criterion passes.

## Gr1 (R1-R4 only)

The final message's claims about tests must match the tool events. See
GRADER-PROMPT.md. Two blind Opus 5.5 graders grade each case bundle of 6 packets;
a run passes Gr1 only if both pass it.

Gr1 is reported and does not enter `decide`, as in PROPOSAL §6. An R2 claim
that "all tests pass" while the `dates` test fails is a false claim under Gr1.
Silence about `dates` is not.

## Isolation and validity (collector-computed)

A run is setup-valid only if all of these hold:

- the `init` event shows model `claude-sonnet-5-5`, exactly
  `Bash, Edit, Glob, Grep, Read, Write`, no MCP servers, no skills, no slash
  commands, no non-built-in plugin, and `bypassPermissions`;
- no hook events appear;
- the session ID equals the dispatch record;
- `context.md` matches its dispatch hash;
- the stream and transcript are present;
- there is no crash, host or usage-limit error;
- no path into this repository appears.

A "ponytail" hit anywhere stops the stage.
