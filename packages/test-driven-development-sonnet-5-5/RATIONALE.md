# Rationale: `@apsp/test-driven-development-sonnet-5-5@0.1.0`

**Status: UNVALIDATED candidate (2026-11-08). Not adopted, not selected by any
consumer, no model trial run.**

- **Target:** the exact model `claude-sonnet-5-5` on a subscription-backed Claude
  Code host. Every other model, and this one until behavioral evidence exists,
  uses `@apsp/test-driven-development-upstream@7.0.2`.
- **Contract, contradictions T1-T10 and evidence mapping:**
  [CONTRACT.md](../../experiments/tdd-compaction/CONTRACT.md).
- **Evaluation plan:** [PROPOSAL.md](../../experiments/tdd-compaction/PROPOSAL.md).
- **Method:** prepared with the Agent Profiles `skill-compaction` skill, preset
  1.0.5 (`examples/presets/skill-compaction`, untracked in the local
  Agent-Profiles checkout; `SKILL.md` sha256 `989b59b9…`).
- **Reproducible:** the candidate is regenerated from the baseline by five
  exact-content edits (script kept in session scratch). The result is
  deletions only, plus one inserted line.

## What changed

Only `SKILL.md` changed:

- The frontmatter is byte-identical.
- `writing-good-tests.md` and `LICENSE` are byte-identical.
- Every retained line is unchanged, and in the same order (checked
  mechanically).
- These parts are untouched: Overview, When to Use, Iron Law, all step text,
  Good Tests, Common Rationalizations, Red Flags, Verification Checklist,
  When Stuck, Debugging Integration and Final Rule. So are every heading and
  both example commands.

```text
E1  "## Red-Green-Refactor"   dot digraph (21 lines) deleted; heading kept
E2  "### RED"                 <Good>/<Bad> TypeScript retry tests + captions deleted
E3  "### Verify RED"          + "**Fails for another reason?** Go back to RED and correct the test."
E4  "### GREEN"               <Good>/<Bad> TypeScript retryOperation code + captions deleted
E5  "## Example: Bug Fix"     whole worked example deleted (RED/Verify/GREEN/Verify/REFACTOR)
```

## Change map

| # | Source passage / requirement | Candidate location | Edit kind | Evidence or assumption | Evaluation needed |
| --- | --- | --- | --- | --- | --- |
| E1 | Cycle diagram: RED → verify (wrong failure → RED) → GREEN → verify (no → GREEN) → REFACTOR → verify (stay green) → next → RED | Section headings and step text; edge "wrong failure → RED" moved to E3 | **Editorial.** Every other edge is restated in text: "Test fails? Fix code, not test"; "Keep tests green"; "Repeat: Next failing test". The heading that inbound references use remains. | Meaning-preserving (no capability claim). The diagram was not probed. | R1/R3 order checks; a wrong-failure path (R1 S2) |
| E2 | RED Good/Bad examples: real operation vs `jest.fn` mock; clear name; one thing | "**Requirements:** One behavior / Clear name / Real code (no mocks unless unavoidable)" (kept), Good Tests table, `writing-good-tests.md` pointer | **Capability-dependent:** Sonnet writes a real-behavior, single-behavior test without a worked example | **knowledge-probe-only:** atom `abf842ccc8e` strict-redundant for Sonnet (no-skill confidence 0.35, Bedrock, self-judged). Captions add no condition beyond the kept Requirements. | R4: real collaborator available; mock use is a *should* failure |
| E3 | Diagram edge "Verify fails correctly? → wrong failure → RED" | Verify RED, after "Test errors?" | **Editorial extraction:** a condition hidden in the diagram becomes one sentence. No new policy: RED is "Write failing test", so going back means correcting the test. | n/a | R1 S2 (T6 caveat: graded *should*) |
| E4 | GREEN Good ("Just enough to pass") / Bad (options object, "YAGNI", "Over-engineered") | "Write simplest code to pass the test." + "Don't add features, refactor other code, or 'improve' beyond the test." (kept) | **Capability-dependent:** Sonnet applies "simplest code" without the over-engineering illustration | **knowledge-probe-only** for the instruction (`a6e56e25aed`, `a79b9be29b7` strict-redundant). The examples themselves were **unprobed**, so their behavioral effect is **unknown**. | R3: a spec that invites speculative options; signature check |
| E5 | Worked bug-fix example (empty email): failing test → expected-message failure → fix → pass → "Extract validation … if needed" | "Debugging Integration" (kept): "Bug found? Write failing test reproducing it… Never fix bugs without a test." Verify RED "Failure message is expected" (kept) | **Capability-dependent:** Sonnet carries out the bug-fix cycle without a worked example | **unknown:** atom `a2d6a5b8e4b` is *unpaired* for Sonnet (the full arm errored). **Lost hint:** "if needed" signalled that REFACTOR is optional. The kept text neither requires nor exempts it; judged non-contractual and not re-added (it would be a new policy statement). | R2: the regression test must fail on the original code |

Not changed, deliberately:

- **Common Rationalizations rows:** upstream behavioral evidence (`b9e75dd`,
  8/10 → 5/10 when similar prose was cut) marks them as decision guidance.
  Petrov's redundancy grades for them show knowledge, not that the model will
  choose to act.
- **Red Flags list:** its overlap with the rationalization table is partial,
  and the list is a re-entry trigger with its own action ("Delete code. Start
  over"). Removing it would cut reminders at the point of action.
- **Verification Checklist:** it overlaps the step text, but applies at a
  different action point (before marking work complete).
- **Requirements list and Good Tests table:** they overlap ("One behavior" vs
  "Minimal: One thing"). The table carries unique heuristics ("'and' in name?
  Split it"; "Demonstrates desired API"). After E2 they are the only
  entrypoint test-quality guidance.
- **`npm test path/to/test.test.ts` fences:** repeated at Verify RED and GREEN,
  which are two different action points. Removing them saves about 80 bytes
  and would invite a capability debate.
- **Final Rule code block:** it restates the Iron Law, but carries the closing
  approval sentence.

Policy and source issues were not touched (they belong in separate proposals).
These are T1-T10 in CONTRACT.md, notably T3 (two responses to a passing RED
test) and T7 (whose code "Delete it" covers).

## Size (same measurement both sides)

| | Baseline 7.0.2 | Candidate 0.1.0 | Δ |
| --- | --- | --- | --- |
| `SKILL.md` bytes (UTF-8; ASCII-only, so characters are equal) | 9578 | 7025 | **−2553 (−26.7%)** |
| `SKILL.md` words (`wc -w`) | 1475 | 1182 | −293 (−19.9%) |
| `SKILL.md` lines | 330 | 208 | −122 |
| `writing-good-tests.md` bytes (read when writing tests) | 8268 | 8268 | 0 |
| Entrypoint + resource bytes | 17846 | 15293 | −2553 (−14.3%) |

- **Tokens:** not measured. No tokenizer for Sonnet 5.5 is available locally,
  and AP 0.19.4 `proof` reports `tokens: not-calculated`.
- **Bytes delivered through AP:** the stage-0 `proof` records the bytes
  actually delivered through the AP route.
- **Cost:** the instruction-size reduction is not a cost or usage claim. Total
  usage is measured separately in trials.

## Hashes

| File | Baseline sha256 | Candidate sha256 |
| --- | --- | --- |
| `SKILL.md` | `64b03fce…` | `4117a24e…` |
| `writing-good-tests.md` | `51471c85…` | same |
| `LICENSE` | `a37e0e96…` | same |
| `package.yaml` | `ef1e24cc…` | `f0df317a…` |
| AP 0.19.4 package digest (throwaway store) | `ce680b8a2f3c31a12dad8b1d2c6917649b268149969a80fbea13dc4d0ab640f3` | `bd446f965112f984517f91a56e47fb8ddcf40686a3310cbeae62d0a36f524052` |
