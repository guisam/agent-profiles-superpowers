# Opus 5.5 TDD candidate: contract-first compaction (prepared, unvalidated)

Prepared 2026-11-08. **No model has seen this candidate.** The default for
every model remains `@apsp/test-driven-development-upstream@7.0.2`.

| File | What it is |
| --- | --- |
| [../../packages/test-driven-development-opus-5-5/](../../packages/test-driven-development-opus-5-5/) | The candidate package (0.1.0), RATIONALE (change map, inventory, evidence labels, hypotheses) and STATUS |
| [requirements.json](requirements.json) | The extracted contract: 31 requirements with verbatim upstream anchors |
| [CONTRACT.md](CONTRACT.md) | The contract by group, the ambiguities carried, whether stage-1 adjudications apply, and the gap classification |
| [CONTRACT-ONLY-DRAFT.md](CONTRACT-ONLY-DRAFT.md) | An experimental contract-only floor (2,370 bytes). Not a skill; never deliver it |
| [CHECKS.md](CHECKS.md), `CHECKS.json` | Deterministic validation results |
| [PROPOSAL.md](PROPOSAL.md) | An optional smoke evaluation: tier C ≤ 24 runs, about $2, needing separate approval |
| `tools/make_candidate.py`, `tools/check_candidate.py` | Regenerate the candidate from upstream; run the checks |
