# Status: `@apsp/brainstorming-sonnet-5-5@0.1.0`

**Rejected, not adopted. Retained as a failed variant; do not select it.**
Current as of 2026-11-08. `RATIONALE.md` is preserved as written on 2026-11-07,
so its status line predates the audit.

- Treatment: **shortening**. 221 bytes (about 1.5%) were deleted for
  `claude-sonnet-5-5`, based on Petrov's knowledge evidence.
- Pilot `apsp-bs-001` (Sonnet 5.5, 11 cases × 2 repetitions per arm):
  - no benefit over full content;
  - no meaningful saving was established.
- Audit correction: the "one must-pass regression" (C02) depends on applying
  "one main question" inconsistently. Under either consistent reading the arms
  tie. So the reason for rejection is **lack of benefit**, not demonstrated
  harm. See `evaluations/brainstorming/audit/GRADING-ADJUDICATION.md`.
- Package bytes are unchanged (AP digest `759b3a0c…`). No further testing is
  planned.
- Recommended configuration: `selectors/alpha.agents.yaml`, which puts every
  model on `@apsp/brainstorming-upstream@7.0.2`.
