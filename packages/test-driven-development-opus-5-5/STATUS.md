# Status: `@apsp/test-driven-development-opus-5-5@0.1.0`

**Unvalidated candidate. Not adopted; no consumer selects it.** Current as of
2026-11-08.

- **Target:** `claude-opus-5-5` on Claude Code, with AP-resolved required
  delivery.
- **Treatment:** contract-first compaction of `SKILL.md` (−2,650 bytes,
  −27.7%). Edits O1-O8 are in [RATIONALE.md](RATIONALE.md). The frontmatter,
  every rule, rebuttal, red flag and checklist item, and the resources are
  unchanged.
- **Evidence:** none for Opus. The Sonnet 5.5 screening (`apsp-tdd-001`) is
  cross-model development evidence only.
- **Deterministic checks:** 31/31 requirements covered; insertions are exactly
  the planned edits, in order; frontmatter and resources identical; inbound
  references intact; AP digest reproducible
  ([CHECKS.md](../../experiments/tdd-opus-compaction/CHECKS.md)).
- **Next, optional and needing separate approval:** a smoke evaluation
  ([PROPOSAL.md](../../experiments/tdd-opus-compaction/PROPOSAL.md)).
- **Recommended configuration:** every model on
  `@apsp/test-driven-development-upstream@7.0.2`.
