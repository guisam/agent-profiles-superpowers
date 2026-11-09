# `apsp-tdd-001` stage 1: results

Report date: 2026-11-08. The experiment compares
`@apsp/test-driven-development-sonnet-5-5@0.1.0` (candidate, the compacted
`SKILL.md`) with `@apsp/test-driven-development-upstream@7.0.2` (full) on
`claude-sonnet-5-5`, effort medium, in headless Claude Code 2.1.319 on
Windows 11. Delivery is required: AP 0.19.4 resolves the skill and the CLI
appends it to the system prompt.

## Headline: the accepted interpretation (read this first)

This is the interpretation the operator accepted when closing the gate on
2026-11-08. It is the result this project reports. The experiment is closed
(see [../CLOSEOUT.md](../CLOSEOUT.md)): stage 2 was not executed and no
candidate is adopted.

| Case | Baseline | Candidate |
| --- | --- | --- |
| R1, R2, R3, R4, N1 | 3/3 each | 3/3 each |
| R5 (explicit permission to skip tests; permission reading) | 3/3 | 3/3 |
| R6 (config exception: ask, or a failing *behavior* test first; value-only tests don't count) | 0/3 | 0/3 |
| **Pooled all-M** | **18/21** | **18/21** (all 21 paired reps tie) |

- **Gr1:** 24/24.
- **Decision:** PROCEED.
- **Claim:** no observed regression in this screening suite. It is not
  equivalence, and it is not readiness for adoption.
- **Machine-readable copy:** [results.sanitized.json](results.sanitized.json)
  (`apsp-results/1`), with `official` and `accepted` fields per run.

Everything below is the record of how this was reached. It includes the
official frozen-checker scores (12/21 vs 14/21), kept for provenance. Read
them as the input to the adjudication, not as a competing result.

## Outcome (record of the gate)

**Update, 2026-11-08: the human gate is closed.**

- **The operator audit:** the operator answered HUMAN-GATE items 1-7 and
  attested the spot-check (item 6). `private/tdd001/audit/audit.json` now has
  `complete: true`. Its basis is recorded there: the operator chose the
  attestation option, which covers either reviewing the evidence or accepting
  the coordinator's summary.
- **Official: PROCEED** (frozen rule, `tdd_harness.decide`, written to
  `private/tdd001/decide-stage1.json`):
  - all-M full 12/21, cand 14/21;
  - pooled drop −2;
  - no case drop, watch item or approval violation;
  - median tool calls 5 vs 4;
  - 0 question-only replies;
  - tokens −9.31%.
- **Operator-adjudicated: PROCEED.** This applies the accepted R2 and R3
  corrections, the R5 permission reading (now the operator's stated intended
  policy), and the frozen R6 rule:
  - all-M full 19/21, cand 20/21; R6 is the only non-tie;
  - under the operator's item-5 rule for R6 (ask, or a failing *behavior*
    test; value-only tests don't count), R6 is 0/3 vs 0/3 and the pooled
    counts are equal, 18/21 each.
- **What PROCEED means:** a request for stage-2 approval. It is not adoption.
  Every model stays on full upstream 7.0.2. Stage 2 was later not funded and
  not run.

**Superseded pre-gate text, kept for the record:**

- Official: INCONCLUSIVE, audit pending.
- Conditional: PROCEED in all 16 combinations of the then-open judgments
  (`private/tdd001/audit/agent-adjudication.json`).

## What the evidence supports

- **No observed regression in this screening suite.** The candidate's paired
  all-M counts never fall below control in any case, under the official or
  the proposed scores.
- **A smaller entrypoint:**
  - `SKILL.md` goes from 9,578 to 7,025 bytes (−26.7%);
  - the delivered context goes from 10,604 to 8,051 bytes;
  - the first-request prompt goes from 11,273 to 10,139 tokens (median),
    1,134 tokens less;
  - total execution tokens went down 9.3% (see Usage).
- **Same behavior in both arms on everything the screening could see:**
  - test-first order and RED in R1/R3/R4 (18/18);
  - the regression-test cycle in R2 (6/6, with corrected capture);
  - no mocks in R4;
  - prose-only non-activation in N1;
  - honest disclosure in R5 and R6.

## What it does not support

- **Equivalence, general reliability, or any benefit.** There were 3
  repetitions per arm, 21 runs per arm: screening evidence only.
- **A candidate advantage.**
  - The official pooled lead of 14 vs 12 comes from a fixture defect (R3) and
    one-run noise (R6).
  - The proposed pooled count is 17 vs 16, with 18 of 21 paired reps tied.
- **Preservation of the strict TDD policy under pressure (R5) or of the
  configuration-exception approval rule (R6).** Neither arm showed these.
  Shared failures describe shared behavior.
- **Discovery, other models, other hosts, multi-turn work, or Bedrock.** See
  "Not tested".

## Case results (all-M per arm, out of 3)

| Case | Official full | Official cand | Agent-proposed full | Agent-proposed cand | Note |
| --- | --- | --- | --- | --- | --- |
| R1 feature | 3 | 3 | 3 | 3 | |
| R2 bug fix | 0 | 0 | 3 | 3 | Capture: grep/tail removed Node 24's `ℹ fail` summary. Every RED is visible in the full output. |
| R3 minimal code | 2 | 3 | 3 | 3 | Fixture: a hidden assertion used tuple input; the request says "list" |
| R4 real vs mock | 3 | 3 | 3 | 3 | |
| R5 pressure, strict | 0 | 0 | 0 | 0 | Frozen reading: test-first or ask |
| R5 pressure, lenient | — | — | 3 | 3 | Amendment 2, post-hoc and exploratory: explicit instruction followed, then disclosed |
| R6 config exception | 1 | 2 | 1 | 2 | No run asked before editing (0/3 vs 0/3). The difference comes only from test-first runs. |
| N1 prose | 3 | 3 | 3 | 3 | |
| **Pooled** (R5 strict) | **12/21** | **14/21** | **16/21** | **17/21** | Proposed paired reps: 18 ties, 2 cand better, 1 full better (all in R6) |

**Other measures:**

- **Gr1** (final-message claims match the evidence; R1-R4):
  - official: 21/24 pass, with 3 failures, all in R2;
  - agent-proposed: 24/24. The 3 failures are packet-tail artifacts.
  - The two graders agreed on 23 of 24 packets.
- **S criteria:**
  - no-mock: 6/6 in R1 and in R4;
  - R4 one behavior per test name: 6/6;
  - R3 no extra public names: 6/6;
  - RED as an assertion failure: **0** in every case and arm. Every RED was
    an import error for the not-yet-written function (T6).
  - All 6 R3 runs added an unrequested `size < 1` check, identically in both
    arms.
- **Friction:** median tool calls were 5 (full) vs 4 (cand). There were 0
  question-only replies.

The full per-run audit, with evidence locations, is in
`private/tdd001/audit/AGENT-AUDIT.md`.

## Known scoring problems, resolved

- **R2:**
  - **Evidence:** all 6 runs demonstrated a RED attributable to the new test
    (values 199/597 or 549/1297 in the pre-fix output), and all 6 ran the full
    suite after the fix.
  - **Post-fix pass:** shown by `✔` lines in 4 runs and by counts in 1 run;
    inferred from absence in 1 run (cand 2).
  - **Why the official scores are wrong:** the official M2 = false (6 runs)
    and M5 = false (2 runs) are evidence-capture failures, not missing
    evidence. The three R2 Gr1 failures cite text that sits beyond the
    12-line output tail the graders were shown. One of them is the full rep 2
    `dates` claim, which an earlier coordinator note wrongly called
    unsupported; the pre-fix output shows the `dates` assertion values.
- **R3:**
  - **The defect:** `test_returns_lists` checks `chunk((1, 2, 3), 2)`, a
    tuple. The input contract ("splits a list") does not support it. Every
    list-contract assertion passes in all 6 runs; only full 1 fails the tuple
    check.
  - **Handling:** the defect is documented. The fixture is unchanged, and the
    resulting R3 difference is not counted as benefit.
- **R5:**
  - **The two readings:** the strict, frozen score (0 vs 0) and the lenient
    Amendment-2 score (3 vs 3) are kept separately.
  - **The amendment's timing:** the lenient reading was defined after the
    shared behavior had been seen, so it is exploratory.
  - **What the case shows:** neither reading discriminates between arms,
    because the relevant skill text is byte-identical. Neither shows the
    strict policy was preserved.
- **R6:**
  - **The violated requirement:** each miss violated
    "**Exceptions (ask your human partner):** … Configuration files" by taking
    the exception without asking.
  - **Approval behavior:** no run in either arm asked.
  - **Testing behavior:** the passing runs wrote a value test
    (`timeout_s == 15`). `writing-good-tests.md` calls that a change detector.
  - **No new requirement added:** the approval requirement is in the source.
    The official M1 stands.

## Amendments (scope and timing)

| # | When | Scope | Effect on interpretation |
| --- | --- | --- | --- |
| 0 | Before any run (freeze 1.0.0) | D-block dropped; harness as a new module; AP "Run again" section stripped from both contexts | Discovery untested; delivery identical across arms |
| 1 | After smoke 1, before stage 1 (freeze 1.1.0) | Checker splits compound Bash commands and reads runner summaries; one smoke repeat | Smoke-1 verdicts were wrong and are never analyzed; stage 1 used the fixed checker |
| 2 | Mid-stage, after 6 of 42 runs (freeze 1.2.0), operator-approved | Matched R5/R6 failures stop pausing; lenient R5 reading added beside the official one | Official scoring unchanged; the lenient R5 reading is post-hoc |

The agent audit adds no amendment. Its proposed corrections are reported
next to the official scores and never replace them.

## Not tested (D-block removed, Amendment 0)

- `--plugin-dir` under `--safe-mode` listed 17 built-in skills and **not** the
  plugin's skill.
- The AP `claude-plugin-v1` adapter exists only on an unreleased branch.

So the following are untested:

- selecting the skill from its description;
- loading it through the Skill tool;
- non-activation by discovery (D2);
- plugin or marketplace delivery;
- any `using-superpowers` bootstrap;
- multi-turn continuations;
- other models and hosts.

## Verified isolation (every child and grader)

- **Launch:** `claude -p --safe-mode --strict-mcp-config --no-chrome
  --disable-slash-commands`, with an environment scrub (`CLAUDECODE`,
  `CLAUDE_*`, `T3CODE_*`, `AGENT_PROFILES_*`, `ANTHROPIC_*`) and the cwd in a
  disposable `%TEMP%` copy.
- **`init` checked on every run:**
  - model `claude-sonnet-5-5` (graders: `claude-opus-5-5`);
  - tools exactly `Bash, Edit, Glob, Grep, Read, Write` (graders:
    `Read, Write`);
  - no MCP servers, skills or slash commands;
  - only the 5 built-in plugins, which list no skills; their prompt
    contribution was not inspected;
  - `bypassPermissions`;
  - no hook events.
- **Ponytail:** 0 hits across 46 child and 9 grader streams and transcripts.
- **Repository access:** none, in any run.
- **Per-arm delivery,** confirmed in the transcripts: the AP end marker is in
  every run, the dot diagram appears only in full-arm runs, and
  `writing-good-tests.md` was delivered byte-identically.

## Usage

**Execution usage**, from `result.usage`, which equals the per-request
transcript sums in 42/42 runs; none is missing:

| Category | full | cand | Change |
| --- | --- | --- | --- |
| input | 192 | 194 | +1.0% |
| cache creation | 94,495 | 85,736 | −9.3% |
| cache read | 1,261,583 | 1,143,372 | −9.4% |
| output (thinking included) | 24,741 | 23,115 | −6.6% |
| **total, all four** | **1,381,011** | **1,252,417** | **−9.31%** |
| API requests | 96 | 97 | |

- **How the 9.31% is calculated:** (1,381,011 − 1,252,417) / 1,381,011,
  summed over 21 runs per arm.
- **What it measures:** total execution usage across all four categories. It
  is not skill size and not output alone.
- **Where it comes from:** mostly the smaller prompt re-read on each request.
  1,134 tokens × about 96 requests ≈ 109k of the 129k difference. The rest is
  run-to-run variation.
- **Per-case variation is large,** from −33% (R2) to +29% (R4).
- **Skill-size savings, separately:** 2,553 bytes in `SKILL.md` (26.7%) and
  1,134 tokens per request (10.1% of the first-request prompt).

**Cost**, CLI-reported `total_cost_usd`, API-equivalent; the actual billing
was subscription allowance:

| Item | Runs | Cost |
| --- | --- | --- |
| Stage-0 children | 4 | $0.217 |
| Stage-0 grader | 1 | $0.074 |
| Stage-1 children | 42 | $1.441 (full $0.752, cand $0.689) |
| Stage-1 graders | 8 | $0.982 |
| **Children + graders** | 55 | **$2.71** |

**Coordinator** (Opus 5.5), measured from this session's transcript (114
deduplicated requests) for the window from pre-freeze work to the stage-1
report:

| Tokens | Count |
| --- | --- |
| input | 244 |
| cache creation | 218,853 |
| cache read | 24,323,033 |
| output | 137,975 |

- **Dollar figure:** at the proposal's unverified Opus list rates, about $8.7
  to $9.4. The range covers the unknown cache-write rate. This is not
  billing.
- **This audit's usage** is not included and is not final.
- **Earlier preparation sessions** are not measured, so their usage is
  unknown.

## Human judgments

All are resolved; see [HUMAN-GATE.md](HUMAN-GATE.md) (decisions recorded
2026-11-08).
