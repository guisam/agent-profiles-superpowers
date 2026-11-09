# Change map: TDD 7.0.2 → `@apsp/test-driven-development-sonnet-5-5@0.1.0`

This map links each edit to the requirement it must preserve and to the
evidence that it did. It extends the original map in
[`packages/test-driven-development-sonnet-5-5/RATIONALE.md`](../../../packages/test-driven-development-sonnet-5-5/RATIONALE.md)
(frozen; written before any run) with the stage-1 behavioral evidence. The
contract and its contradictions T1-T10 are in
[`experiments/tdd-compaction/CONTRACT.md`](../../../experiments/tdd-compaction/CONTRACT.md).

**How the change was made:**

- The edits are deletions, plus one extracted sentence.
- The frontmatter (selection), `writing-good-tests.md` and `LICENSE` are
  byte-identical. Every retained line is unchanged and in order.
- `check_package.py --compare` confirms that only `SKILL.md` and
  `package.yaml` differ.

## Edits

| # | Removed / changed | Requirement that must survive (still in the candidate) | Edit kind and pre-run evidence | Stage-1 behavioral evidence (accepted; both arms) |
| --- | --- | --- | --- | --- |
| E1 | Red-green-refactor dot diagram (21 lines) | Order: failing test → watch it fail → minimal code → watch it pass → refactor while green → repeat (step text; the heading is kept for inbound references) | Editorial: every edge is restated in text | R1, R3, R4: test edit before code, RED observed, full suite after the last change. 9/9 vs 9/9. |
| E2 | RED Good/Bad TypeScript examples | "One behavior / Clear name / Real code (no mocks unless unavoidable)", the Good Tests table and the `writing-good-tests.md` pointer | Capability-dependent; knowledge-probe-only (Petrov atom `abf842ccc8e`, Bedrock, self-judged) | R4 no-mock 3/3 vs 3/3, one behavior per name 3/3 vs 3/3; R1 no-mock 3/3 vs 3/3. `writing-good-tests.md` read in every run. |
| E3 | (added) "Fails for another reason? Go back to RED and correct the test." | The diagram edge "wrong failure → RED" | Editorial extraction | **Not exercised.** Every RED was an import error for a missing function, in both arms (S "assertion RED" 0 vs 0). The wrong-failure path stays untested. |
| E4 | GREEN Good/Bad (`retryOperation`, options object, YAGNI) | "Write simplest code to pass the test" and "Don't add features … beyond the test" | Capability-dependent; the instruction is knowledge-probe-only, the examples were unprobed | R3 signature exactly `items, size` 3/3 vs 3/3; no padding or overlap options 3/3 vs 3/3. **Shared gap:** all 6 runs added an unrequested `size < 1` check, so the arms are not distinguished on small extras. |
| E5 | Worked bug-fix example | "Bug found? Write failing test reproducing it … Never fix bugs without a test"; "Failure message is expected" | Capability-dependent; unknown (atom `a2d6a5b8e4b` unpaired for Sonnet) | R2: regression test first, RED shown, mutation check (fails on the original, passes on the fix), hidden tests, full suite. 3/3 vs 3/3 (accepted, after a capture correction). |

## Requirements not touched by any edit, but tested

These requirements are byte-identical in both arms. A shared result here
describes the base skill's behavior on Sonnet 5.5, not the compaction.

| Requirement | Case | Result (accepted) |
| --- | --- | --- |
| Final Rule: "No exceptions without your human partner's permission" (permission reading, gate item 4) | R5 | 3/3 vs 3/3: every run followed the explicit "skip tests" instruction and disclosed it |
| "Exceptions (ask your human partner): … Configuration files" plus "No change detectors" (gate item 5) | R6 | 0/3 vs 0/3: no run asked; some wrote a value-only test, the rest edited silently and disclosed it afterwards |
| Prose-only work does not need tests (resource rule) | N1 | 3/3 vs 3/3 |

## Evaluation still needed before any promotion

- **E3:** a case where the first failure is the wrong failure.
- **E4:** a case that separates "simplest code" from defensive extras.
- **E5 and E1:** held-out bug-fix and multi-cycle cases (refactor and
  characterization are untested).
- **Discovery:** selection from the description through native skill
  listing. This is untested, because the frontmatter is identical but plugin
  delivery was not available.
- **The R6 behavior:** it is a base-skill issue. If the maintainer wants
  "ask before config exceptions" to hold, that is a separate upstream proposal,
  not a compaction edit.
