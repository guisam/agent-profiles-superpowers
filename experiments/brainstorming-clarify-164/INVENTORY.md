# Run inventory and budget: `apsp-bs-002` (draft r2, nothing executed)

Arms: `full` (`@apsp/brainstorming-upstream@7.0.2`) and `seq`
(`@apsp/brainstorming-sequencing@0.1.0`). Repetitions: 3 per case × arm.

## Stage 1: Sonnet screening (`claude-sonnet-5-5` only)

| Item | Count | Rule |
| --- | --- | --- |
| Turn-1 scenarios | 7 | S1a, S1b, S1c, S3, U1, U2, N1 |
| Continuation scenarios | 1 | S1b-t2. Each run continues that arm and repetition's own S1b reply. |
| Turn-1 child runs | 42 | 7 × 2 arms × 3 |
| Continuation child runs | 6 | 1 × 2 × 3, dispatched only after the matching S1b run is collected |
| **Analyzed child runs** | **48** | |
| Smoke child runs | 4 | S1b and S1b-t2 × 2 arms. Retained; never analyzed or counted. |
| Retry allowance | ≤ 5 | One rerun per invalid run (new token, same case/arm/rep). Retrying a parent S1b also rebuilds its S1b-t2 continuation, which costs one extra call out of the 5. All failures stay in the ledger. If the 5 retries cannot complete every required pair (3 valid runs per arm and case), the outcome is VOID or INCONCLUSIVE (PROPOSAL rule 1). Denominators never change. |
| **Child runs, maximum** | **57** | |
| Grader bundles | 8 | One per case: 7 + S1b-t2; 6 replies each |
| Grader runs | 16 | 2 independent blind graders per bundle |
| Smoke grader runs | 2 | 1 grader each for the S1b and S1b-t2 smoke bundles |
| Grader re-runs | ≤ 2 | Only for files the v2 validator rejects |
| **Grader runs, maximum** | **20** | |
| Coordinator dispatches | ≤ 77 | 57 child + 20 grader |

## Stage 2: validation (NOT AUTHORIZED; only after a stage-1 PROCEED **and** a separate approval)

| Item | Count | Rule |
| --- | --- | --- |
| Sonnet scenarios | 7 | R1, R2, R3 + held-out H1-H4. The screening cases already ran for Sonnet and are not repeated. |
| Haiku scenarios | 14 + 1 continuation | the 7 screening turn-1 cases, R1-R3, H1-H4, plus S1b-t2 |
| Sonnet child runs | 42 | 7 × 2 × 3 |
| Haiku child runs | 90 | 14 × 2 × 3 + 6 continuation |
| **Analyzed child runs** | **132** | |
| Haiku smoke runs | 4 | as stage 1 |
| Retry allowance | ≤ 14 | about 10% of 132 |
| **Child runs, maximum** | **150** | |
| Grader runs | 44 | (7 Sonnet + 15 Haiku bundles) × 2 graders |
| Smoke graders / re-runs | 2 / ≤ 3 | |
| **Grader runs, maximum** | **49** | |
| Coordinator dispatches | ≤ 199 | |

Held-out H1-H4 use a fresh fixture. They are authored **after** the treatment
is frozen, by someone other than its author. They are the only confirmation
evidence; screening cases never count as held-out.

## Budget: API-equivalent estimates, not spending

All runs use existing subscription sessions. Nothing is billed per token. The
dollar figures are what the same tokens would cost at Anthropic list prices
(cached 2026-10-06 in the Claude API skill; not re-verified):

| Model | Input | Output | Cache read (per MTok) |
| --- | --- | --- | --- |
| Sonnet 5.5 | $2 | $10 | $0.20 |
| Opus 5.5 | $4 | $20 | $0.20 |
| Haiku 5.5 | $0.10 | $0.50 | $0.01 (**assumed**; no rate cached) |

Cache writes are priced at 1.25× input for 5-minute writes and 2× for 1-hour
writes. Subscription consumption shows up as usage-limit headroom, which this
plan cannot convert to dollars.

Unit bases observed in apsp-bs-001:

| Unit | Basis |
| --- | --- |
| Sonnet child run | mean $0.124, min $0.104, max $0.192 (44 runs) |
| Opus grader run | $0.176 per 4-reply bundle; assume $0.21 for 6 replies, $0.25 upper |
| Haiku child run | no observation. Sonnet token profile at Haiku rates: mean $0.006, max $0.010 (assumption) |
| Coordinator per dispatch | **measured** ≈ $8.8 of Opus usage over the apsp-bs-001 window (108 messages, 20:13-20:52Z) ÷ 56 dispatches ≈ $0.157. The window boundaries are approximate and include non-trial analysis. A fresh, lean coordinator session would cost less; assume $0.05 as the lower bound. |

| Stage | Children | Graders | Coordinator | **Total (expected / range)** |
| --- | --- | --- | --- | --- |
| 1 | $6.4 (52 incl. smoke × 0.124; max 57 × 0.192 = $10.9) | $3.8 (18 × 0.21; max 20 × 0.25 = $5.0) | $11.0 (70 × 0.157; low 70 × 0.05 = $3.5, max 77 × 0.157 = $12.1) | **≈ $21** (≈ $12-$28) |
| 2 | Sonnet $5.2 + Haiku $0.6 (max with all 14 retries on Sonnet ≈ $11.7) | $9.7 (46 × 0.21; max 49 × 0.25 = $12.3) | $28.6 (182 × 0.157; low $9.1, max 199 × 0.157 = $31.2) | **≈ $44** (≈ $22-$55) |

Expected-case dispatches: stage 1 = 52 children (48 analyzed + 4 smoke) + 18
graders = 70; stage 2 = 136 children + 46 graders = 182. Maximums use the full
retry and re-grade allowances. The low bound uses observed minimum unit costs
and a lean coordinator.

The coordinator is the largest cost line. Running each stage from a fresh,
minimal coordinator session is the main lever. Token counts are captured from
transcripts per run and per grader. Missing fields stay unknown (harness v2).

## Harness work required before freeze (not done in r2)

`collect_v2.py` 2.0.0 assumes one fixture per suite and single-turn runs. A
v2.1 must add:

- a per-case `fixture`;
- continuation prompts built from a named prior run's verbatim reply plus the
  scripted user turn;
- per-case `gate` handling, so N1's requested edit is not a gate violation;
- two-grader bundles with a disagreement report.

Each addition needs tests in `test_collect_v2.py`. v2.1 becomes part of the
freeze.
