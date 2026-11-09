# Rationale: `@apsp/test-driven-development-opus-5-5@0.1.0`

**Status: UNVALIDATED candidate (2026-11-08).** It is not adopted, and no
consumer selects it. It has never been delivered to a model, and no probe,
trial or grader has run on it. Every model's operational default remains
`@apsp/test-driven-development-upstream@7.0.2`.

## Target, host and method

- **Target model:** `claude-opus-5-5`, the exact ID stated by the host in this
  session. Nothing else was assumed.
- **Intended deployment:** Claude Code (CLI 2.1.319 was observed in
  `apsp-tdd-001`), with the skill delivered by AP 0.19.4 `resolve` for that
  exact model. This is the same route as the Sonnet experiment.
- **Not covered:** interactive bootstrap delivery, Bedrock and other hosts.
  Results do not transfer across hosts.
- **Who wrote it:** the coordinator that wrote this candidate is also Opus 5.5.
  That fact establishes nothing about Opus's TDD behavior.
- **Method:** the contract-first application of AP's skill-compaction skill
  (preset 1.0.5, `SKILL.md` sha256 `989b59b9…`, unmodified):
  1. extract the full upstream contract
     ([requirements.json](../../experiments/tdd-opus-compaction/requirements.json),
     [CONTRACT.md](../../experiments/tdd-opus-compaction/CONTRACT.md));
  2. draft a contract-only floor
     ([CONTRACT-ONLY-DRAFT.md](../../experiments/tdd-opus-compaction/CONTRACT-ONLY-DRAFT.md),
     an experimental artifact);
  3. inventory the supporting guidance;
  4. assemble the candidate from the upstream text by exact edits.
- **Reproducible:**
  `python -I experiments/tdd-opus-compaction/tools/make_candidate.py` regenerates
  it from the upstream bytes. `--check` confirms the committed files match.
- **Sources of truth:**
  - The upstream contract is the source of truth.
  - The Sonnet candidate and its results are development evidence from
    another model.

## Evidence labels used

| Label | Meaning here |
| --- | --- |
| **demonstrated (cross-model)** | Observed for `claude-sonnet-5-5` in `apsp-tdd-001` stage-1 screening: 3 reps per arm, accepted interpretation. **Not Opus evidence.** |
| **knowledge-probe-only (cross-model)** | Petrov/dokimi probes of Sonnet 5.5 on Bedrock, self-judged. Knowledge, not behavior, and not Opus. |
| **unknown** | No evidence for Opus 5.5. Every capability-dependent cut below is **unknown for Opus**. |

There is **no Opus-specific TDD evidence** of any kind: Petrov's probes cover
Haiku and Sonnet only, and no Opus trial ran. AP's own host observations report
that Opus copies its exact model ID into `resolve`. That is delivery evidence
from AP, not skill-behavior evidence.

## Change map: source → contract → candidate

All requirement IDs are defined in `requirements.json`. Coverage is checked
mechanically: **31 of 31 requirements are covered** in upstream, in the Sonnet
candidate and in this candidate (`CHECKS.json`).

| Edit | Upstream passage | Requirement it serves | Candidate | Kind | Gap type it could expose | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| O1 | Red-Green-Refactor dot diagram | O3 (order), V4 (wrong failure → RED), F2 | One natural-language sentence states the order. V4 extracted by O3 below. The heading is kept for inbound references. | Editorial: the order is stated more directly than in the Sonnet candidate, which relied on headings | knowledge | n/a (meaning preserved). Order demonstrated (cross-model): R1, R3, R4 9/9 vs 9/9 |
| O2 | RED `<Good>`/`<Bad>` retry examples | R1 (real code, one behavior, clear name) | Removed. Requirements list kept verbatim at the action point. | Capability-dependent | knowledge/execution: what a real, single-behavior test looks like | Opus: **unknown**. Sonnet: knowledge-probe-only (atom `abf842ccc8e`); demonstrated (cross-model): no mocks 6/6 vs 6/6 in R1 and R4 |
| O3 | Diagram edge "wrong failure → RED" | V4 | "**Fails for another reason?** Go back to RED and correct the test." | Editorial extraction (same sentence as the Sonnet candidate) | — | Not exercised: every stage-1 RED was an import error |
| O4 | GREEN `<Good>`/`<Bad>` (options object, YAGNI) | G1 | Removed. "Write simplest code…" and "Don't add features…" kept verbatim. | Capability-dependent | **judgment**: resisting speculative generality | Opus: **unknown**. Sonnet: demonstrated (cross-model): R3 signature 6/6, but all 6 runs added an unrequested `size < 1` check (shared) |
| O5 | "Example: Bug Fix" (email) | B1, V1-V6 | Removed. Debugging Integration and every step kept. | Capability-dependent | execution: the regression cycle | Opus: **unknown**. Sonnet: demonstrated (cross-model): R2 3/3 vs 3/3 (accepted) |
| O6 | Verify RED fence `npm test path/to/test.test.ts` | V1 (run the test) | "**MANDATORY. Never skip.** Run the test." | Capability-dependent (tool guidance). **The procedure is kept as an explicit action**; only the placeholder command is removed. Its path was illustrative, not local knowledge. | execution: choosing the project's runner | Opus: **unknown**. Sonnet: demonstrated (cross-model): the project's own runner was used in 42/42 runs |
| O7 | Verify GREEN fence (same) | V5 | "**MANDATORY.** Run the test." The V8 paragraph still names `pytest`, `npm test` and `cargo test`. | As O6 | as O6 | as O6 |
| O8 | Good Tests table, "Bad" column (`test('validates email and domain and whitespace')`, `test('test1')`, "Obscures…") | R2 | A three-item list keeps every "Good" rule verbatim in meaning ("and" in name? split; name describes behavior; demonstrates desired API) | Capability-dependent (illustrations) | knowledge: recognizing vague names | Opus: **unknown**. Sonnet: R4 names 6/6 (demonstrated, cross-model) |

**Compared with the Sonnet candidate** (`@apsp/test-driven-development-sonnet-5-5@0.1.0`):

- **Same:** O2-O5.
- **Clearer:** O1, which states the cycle order in a sentence instead of
  leaving it implicit in the headings.
- **New:** O6-O8.
- **Not cut, deliberately:** nothing the Sonnet candidate kept.

## Supporting-guidance inventory (outside the core contract)

| Passage | Class | Decision | Why |
| --- | --- | --- | --- |
| Overview summary ("Write the test first…") | reminder | retained | Entry-point restatement of O1/O3. Short. |
| Core principle; letter = spirit | decision aid | retained | Gives the reason that makes the rules non-negotiable. Inbound "explains why this matters" (writing-skills). |
| "skip TDD just this once" line | reminder | retained | Anti-skip cue at the activation point. Compliance gap, not knowledge. |
| Iron Law "No exceptions" bullets | reminder plus failure handling | retained | Closes specific loopholes (reference, adapt, look). Inbound "Delete means delete". |
| Cycle diagram | procedural explanation | omitted (O1) | Fully restated in text. The one unique condition was moved into text (O3). |
| RED and GREEN `<Good>`/`<Bad>` code | examples | omitted (O2, O4) | The rule text survives. Capability-dependent, unknown for Opus. |
| Requirements list (RED) | contract at the action point | retained | Unique placement of "Real code (no mocks unless unavoidable)". |
| `npm test …` fences | tool guidance | omitted (O6, O7) | Placeholder path. The run action is kept as words. |
| Verify RED and GREEN confirm lists, recovery lines | verification and failure handling | retained | Contract (V1-V7). |
| "Other tests" paragraph | contract plus exact local rule | retained verbatim | V8 is a recent upstream rule (`a45ede8`) with exact wording. It contains the T4 tension, so it is not reworded. |
| REFACTOR bullets | procedural explanation | retained | They bound refactoring to structure-only work next to "Don't add behavior". Tiny. |
| Repeat | ordering | retained | F2. |
| Good Tests table | decision aid | rules retained; "Bad" column omitted (O8) | Unique heuristics kept. |
| `writing-good-tests.md` pointer and 4 rules | resource contract | retained verbatim | R3; the only resource pointer. |
| Common Rationalizations (11 rows) | decision aid | retained verbatim | **Compliance gap**, not a knowledge gap. Upstream `b9e75dd`: cutting similar rebuttals degraded tests-later pressure behavior. Additional definitions would not address a failure to follow a known rule. |
| Red Flags (13) | reminder plus re-entry trigger | retained verbatim | Has its own action ("Delete code. Start over"). |
| Example: Bug Fix | example | omitted (O5) | Every step it illustrates is stated elsewhere. |
| Verification Checklist | completion check | retained verbatim | A distinct action point (before marking complete). |
| When Stuck | decision aid plus approval | retained verbatim | Contains "Ask your human partner" (S1). The design rows tie into the mock policy. |
| Debugging Integration | contract | retained | B1. |
| Final Rule | approval | retained verbatim | P3. Carries T8. |

**Moved:** nothing apart from O3, which turned a diagram edge into text. No
incoming reference targets an omitted passage: checked against every upstream
v7.0.2 skill outside TDD (`CHECKS.json` → `inbound`).

## Hypotheses this candidate depends on (all untested for Opus)

| ID | Hypothesis | Gap type | Priority |
| --- | --- | --- | --- |
| H1 | Without the retry examples, Opus writes real-behavior, single-behavior, clearly named tests (O2, O8). | knowledge/execution | medium |
| H2 | Without the YAGNI example, Opus writes minimal GREEN code and adds no speculative options (O4). | judgment | **high**: the closest analogue was not distinguished even for Sonnet |
| H3 | Without the worked bug-fix example, Opus writes a failing regression test before the fix and verifies it (O5). | execution | high |
| H4 | Without placeholder commands, Opus runs the project's own runner at Verify RED and GREEN, plus the full suite (O6, O7). | execution/tool | low |
| H5 | Removing examples does not change compliance under pressure. The rebuttals, red flags and checklist are unchanged. | compliance | medium |

**Not hypotheses of this candidate.** These are shared base-skill
behaviors, identical text in both arms, and are left to separate proposals:

- R6, asking before taking the configuration exception, is an
  attention/compliance gap observed in **both** Sonnet arms.
- T6, import-error REDs, is an ambiguity in the source.
- T8, permission vs "no exceptions", is an ambiguity in the source.

## Size (UTF-8 bytes; no Opus tokenizer is available locally)

| Artifact | `SKILL.md` bytes | Words | Lines | Resource bytes (`writing-good-tests.md`) |
| --- | --- | --- | --- | --- |
| Upstream 7.0.2 | 9,578 | 1,475 | 330 | 8,268 |
| Sonnet candidate 0.1.0 | 7,025 (−26.7%) | 1,182 | 208 | 8,268 |
| **Opus candidate 0.1.0** | **6,928 (−27.7%)** | 1,170 | 201 | 8,268 |
| Contract-only draft (experimental) | 2,370 (−75.3%) | 399 | 42 | not packaged |

- **The entrypoint shrinks, the resource doesn't:** the reduction is all in
  the entrypoint. The resource is unchanged and is read on demand.
- **Instruction size is not execution cost.** Stage 1 found that total tokens
  depend on per-request prompt size *and* run behavior. No cost claim is made
  here.
- **The candidate is only 97 bytes smaller than Sonnet's.** O1 adds a sentence
  for clarity; O6-O8 remove about 220 bytes.
- **The contract-only floor is not proposed for delivery.** It drops the
  compliance aids that upstream evidence says matter.

## Hashes

| File | sha256 |
| --- | --- |
| `SKILL.md` | `4685820f8a2c44cee4d7ff9ac1b190c379dfe7fba9eea6043603e7b0bac35e14` |
| `writing-good-tests.md` | `51471c853306ff92ca8bb41dcaea05f31c0e46b03651f8f3c99754b7172f4ae1` (= upstream) |
| `LICENSE` | `a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400` (= upstream MIT) |
| AP 0.19.4 package digest (throwaway store, reproduced twice) | `ebf4efd64dc71b5d2b80944dff7e6f938c132b91f28c5cc51130ba7bf35451d7` |
