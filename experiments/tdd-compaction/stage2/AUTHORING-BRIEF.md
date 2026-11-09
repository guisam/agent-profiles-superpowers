# Held-out case authoring brief (`apsp-tdd-001` stage 2)

This is for the independent author: the operator, or a fresh agent. The
stage-1 coordinator must not write these cases.

## You may read

- `experiments/tdd-compaction/CONTRACT.md`;
- the **baseline** skill:
  `packages/test-driven-development-upstream/7.0.2/SKILL.md` and
  `writing-good-tests.md`;
- this brief.

## You must not read

- `CASES.draft.md`;
- anything under `experiments/tdd-compaction/stage1/`, `private/` or `tools/`;
- `packages/test-driven-development-sonnet-5-5/`, including `RATIONALE.md`
  and the candidate `SKILL.md`.

## Deliverable

Write one file, `stage2/cases.heldout.md`. It holds 10 cases, one per slot.
Each case gives:

1. **Slot ID** and a one-line purpose.
2. **The single user message**, exactly as it will be sent. It must never
   mention TDD, tests-first, skills or Superpowers. H3a is the one exception:
   it must explicitly permit skipping tests.
3. **The project:** language (Python 3 stdlib `unittest`, or Node 24
   `node --test`), files and their contents (or a precise description), and
   the existing tests. The existing suite passes unless the slot requires
   otherwise.
4. **The hidden checks.** Each assertion is mapped to the clause of the user
   message it checks. Assert nothing the message does not require.
5. **Reference solutions:**
   - **good** (passes everything);
   - **bad** (fails at least one M check);
   - **alternative-valid** (a different correct implementation that must pass).
6. **What counts as asking** (H3b, H4) and what counts as scope (all slots).

## Slots

| Slot | Requirement |
| --- | --- |
| H1 | Bug fix, Python. A real defect whose regression test fails on the original code. |
| H2 | Bug fix, Node, as H1. Use no pre-existing failing tests. |
| H3a | Time pressure, and the user explicitly says to skip tests for now. |
| H3b | Time pressure **without** any permission to skip tests. |
| H4 | A configuration change with an observable behavioral effect (for example, a flag that enables a code path), so that a behavior test is possible without asserting the configured value. |
| H5 | A feature where a real, cheap in-memory collaborator exists, next to an external-looking dependency that is tempting to mock. |
| H6 | A refactor only: no behavior change requested. The suite should stay green throughout. |
| H7 | Add tests for existing untested code (characterization). Tests that pass immediately are legitimate here. |
| N2 | A documentation-only fix, in prose. No code or tests should be created. |
| N3 | An explanation-only question about existing code. No file changes. |

## Constraints

- Use only the project's own toolchain. No installs, no network.
- **Do not reuse** these domains or functions:
  - string slugs, cart totals or quantities, list chunking, task due dates,
    byte formatting, HTTP timeouts, spelling typos (used in screening);
  - email validation, retry wrappers, form submission (the skill's own
    examples).
- Keep tasks small: about 2-15 tool calls for a competent agent.
- Every hidden assertion must be derivable from the user message alone. If
  a reasonable alternative implementation could fail an assertion, delete the
  assertion.
