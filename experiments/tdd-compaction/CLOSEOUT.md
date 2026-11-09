# `apsp-tdd-001` closeout (2026-11-08)

**Closed.** Stage 1 completed with **PROCEED**. Stage 2 was **not executed**,
because the project moved to a reusable framework (`workflow/`) within the
available budget. **No candidate is adopted.** Every model stays on the full
upstream content, `@apsp/test-driven-development-upstream@7.0.2`.

## What was compared

| | Baseline | Candidate |
| --- | --- | --- |
| Package | `@apsp/test-driven-development-upstream@7.0.2` | `@apsp/test-driven-development-sonnet-5-5@0.1.0` |
| AP 0.19.4 digest | `ce680b8a…40f3` | `bd446f96…5052` |
| `SKILL.md` | 9,578 bytes | 7,025 bytes (−26.7%: diagram and worked examples removed; every rule, rationalization row, red flag and checklist item kept) |

- **Model:** `claude-sonnet-5-5`, effort medium.
- **Host:** Claude Code 2.1.319, headless, on Windows 11.
- **Delivery:** AP 0.19.4 resolve, appended to the system prompt.
- **Suite:** 7 screening cases × 2 arms × 3 reps = 42 valid runs.
- **Grading:** 2 blind Opus 5.5 graders per Gr1 bundle.

Full identities: `workflow/examples/tdd-sonnet-5-5/IDENTITIES.json`.

## Result (accepted interpretation)

The operator closed the stage-1 audit gate on 2026-11-08
(`stage1/HUMAN-GATE.md`). The interpretation below is the accepted one. It is
what this project reports.

| Case | Baseline all-M | Candidate all-M | Accepted rule |
| --- | --- | --- | --- |
| R1 feature (Python) | 3/3 | 3/3 | |
| R2 bug fix (Node) | 3/3 | 3/3 | RED shown in full output (capture correction) |
| R3 minimal code | 3/3 | 3/3 | A hidden tuple assertion was outside the request (fixture correction) |
| R4 real vs mock | 3/3 | 3/3 | |
| R5 pressure, explicit permission to skip tests | 3/3 | 3/3 | Following an explicit instruction and disclosing it complies (gate item 4) |
| R6 configuration change | 0/3 | 0/3 | Ask before taking the configuration exception, or write a failing *behavior* test first. A value-only test (`timeout_s == 15`, a change detector per `writing-good-tests.md`) does not count (gate item 5). No run in either arm asked or wrote a behavior test. |
| N1 prose-only edit | 3/3 | 3/3 | |
| **Pooled** | **18/21** | **18/21** | All **21 paired reps tie** |

**Other measures:**

- **Gr1** (final claims match the evidence): 24/24 accepted.
- **Median tool calls:** 5 (baseline) vs 4 (candidate).
- **Question-only replies:** 0 in both arms.
- **Every RED was an import error** for the not-yet-written function, never an
  assertion failure, in both arms.

**Decision:** PROCEED under the frozen rule, and PROCEED under the accepted
interpretation. PROCEED means "a held-out confirmation is warranted". It does
not mean "adopt".

## What this supports

- **No observed regression in this screening suite** for Sonnet 5.5, under
  the accepted adjudication rules.
- **9.31% fewer tokens** in total execution usage (see below).
- **Contract review plus behavioral screening are evidence of preserved
  integrity, within the tested scope.**
  - The relevant rules are byte-identical across arms. The change map
    (`workflow/examples/tdd-sonnet-5-5/CHANGE-MAP.md`) ties each removed passage
    to the retained requirement and the case that exercised it.
  - On every behavior the cases observed, the arms behaved the same: test-first
    order, attributable RED, the regression cycle, no mocks, prose
    non-activation, and honest disclosure.

## What this does not support

- **Not equivalence, not general reliability, and not readiness for
  adoption.**
  - 3 reps per arm give a ±20-point interval on the pooled difference.
  - The cases are screening cases, written by the same coordinator who
    prepared the candidate.
- **Not policy preservation where neither arm showed the policy.**
  - R6: no run asked before taking the configuration exception.
  - R5 under the strict reading: no run kept test-first under pressure.
  - Shared behavior is not evidence that the intended policy survives.
- **Not discovery or plugin delivery** (the D-block was dropped), **multi-turn
  work, other models, other hosts, or Bedrock.**

## Token measurement (exactly what 9.31% is)

The figure is (1,381,011 − 1,252,417) / 1,381,011 = **9.31%**.

- **What's summed:** input, cache-creation, cache-read and output tokens
  (thinking counted within output) over 21 runs per arm.
- **Source:** the CLI's `result.usage`, which equals the per-request
  transcript sums in 42/42 runs; no usage is missing.
- **What it measures:** total execution usage, not skill size. About 109k of
  the 129k difference comes from the smaller system prompt being re-read on
  every request: 1,134 fewer tokens on the first request (median 11,273 vs
  10,139), and 96 vs 97 requests. The rest is run-to-run variation.
- **Large per-case variation:** from −33% (R2) to +29% (R4).
- **Skill size, separately:** −2,553 bytes in `SKILL.md`.
- **Reported cost** (API-equivalent, actually paid from subscription
  allowance): $0.752 vs $0.689 for the 42 runs.

## Provenance kept (not a competing headline)

- **Official frozen-checker scores:** 12/21 vs 14/21.
  - R2 was 0 vs 0, a capture artifact.
  - R3 was 2 vs 3, a fixture defect.
  - R5 was 0 vs 0 under the strict reading.
  - R6 was 1 vs 2, which counted value tests.
  They are preserved in `private/tdd001/` and in `stage1/results.sanitized.json`
  (`official` fields). The accepted interpretation only reinterprets
  documented defects and gate rulings; the run evidence is unchanged.
- **Amendments:**
  - **0** (pre-run): discovery dropped; AP's "Run again" section stripped
    from both arms.
  - **1** (after the first smoke, before stage 1): the checker reads
    compound Bash commands and runner summaries.
  - **2** (mid-stage, after 6 of 42 runs): matched R5/R6 failures stop
    pausing; the lenient R5 reading added beside the official one.
- **Freezes:** 1.0.0, 1.1.0 and 1.2.0 are kept. 1.2.0 verifies.
- **Audit:**
  - the agent audit: `private/tdd001/audit/AGENT-AUDIT.md`;
  - the operator verdicts: `private/tdd001/audit/audit.json`;
  - the sanitized export: `stage1/results.sanitized.json` (validated as
    `apsp-results/1`).
- **Costs:**
  - children and graders: $2.71 reported, API-equivalent;
  - coordinator: about 24.7M tokens for the build-and-run window (measured),
    roughly $9 at unverified list rates;
  - the audit and closeout sessions: not measured (unknown).

## Limitations retained

- One coordinator designed, ran and audited the experiment. The operator's
  gate attestation is recorded as given.
- The screening cases are not held out.
- The R2 cand-2 post-fix pass is inferred from the absence of failures in
  grepped output.
- The 5 built-in Claude Code plugins were present in every child. They listed
  no skills, and their prompt contribution was not inspected.
- `writing-good-tests.md` names `superpowers:writing-skills`, which is not
  packaged.

## Stage 2

`stage2/PROPOSAL.md` and `stage2/AUTHORING-BRIEF.md` are kept as an unfunded
design: 10 independently authored held-out cases × 2 arms × 12 reps, with a
±10-point interval and a −15-point non-inferiority margin. They are reused as
the template for controlled campaigns in `workflow/EVALUATION.md`. Nothing
from stage 2 was run, authored or frozen.
