# Deterministic validation: Opus 5.5 TDD candidate (2026-11-08)

All checks are local, with no model calls. Re-run them with:

```sh
python -I experiments/tdd-opus-compaction/tools/make_candidate.py --check
python -I experiments/tdd-opus-compaction/tools/check_candidate.py      # writes CHECKS.json
python -I workflow/tools/check_package.py packages/test-driven-development-opus-5-5/0.1.0 \
  --compare packages/test-driven-development-upstream/7.0.2
```

| Check | Result |
| --- | --- |
| Generator reproduces the candidate from upstream bytes | pass |
| Requirement coverage (31, verbatim anchors or declared restatements; 4 whole sections) | upstream 31/31, Sonnet 31/31, **Opus 31/31** |
| Lines retained from upstream appear in upstream order | pass (0 out of order) |
| Inserted lines | exactly the planned O1, O3, O6, O7 and O8 text (8 lines) |
| Frontmatter (`name`, `description`) byte-identical | pass |
| Forbidden host tokens (`$ARGUMENTS`, `$0-9`, `ultrathink`) | none |
| Inbound references used by other upstream skills (headings, "Delete means delete", "Keep as reference" rows, Iron Law) | all present |
| `writing-good-tests.md` and `LICENSE` byte-identical to upstream; link present | pass |
| Package closure (`check_package.py`) | 4 files, 1/1 references resolve, no scripts; cross-skill `writing-skills` (unpackaged, documented) |
| Files that differ from upstream and from the Sonnet candidate | `SKILL.md`, `package.yaml` only |
| AP 0.19.4 `add` digest, two throwaway stores | `ebf4efd64dc71b5d2b80944dff7e6f938c132b91f28c5cc51130ba7bf35451d7` both times |
| Contract-only draft carries every contract requirement ID | pass. It omits A4, P1, P2, D1, D2 and X1 by design: aids and resource, not contract |
| `apsp-tdd-001` freeze 1.2.0 still verifies (earlier evidence untouched) | pass |

## Sizes (UTF-8 bytes)

| Artifact | `SKILL.md` | Resource |
| --- | --- | --- |
| Upstream 7.0.2 | 9,578 | 8,268 |
| Sonnet candidate | 7,025 | 8,268 |
| Opus candidate | 6,928 | 8,268 |
| Contract-only draft | 2,370 | — |

**What these checks do not show:**

- They do not show that Opus behaves the same with the candidate. That needs
  the optional evaluation in [PROPOSAL.md](PROPOSAL.md).
- Covered requirements mean the *text* is present, not that it is *followed*.
