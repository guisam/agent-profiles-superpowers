# Workflow: model-specific skill variants through Agent Profiles

This is a reusable, plugin-free workflow to propose, distribute and evaluate
per-model variants of Superpowers skills. Full upstream content stays the
default. **Start with [GUIDE.md](GUIDE.md).**

| Need | Entry point |
| --- | --- |
| Understand the workflow and the TDD worked example | [GUIDE.md](GUIDE.md) |
| Run a bounded baseline/candidate comparison | [EVALUATION.md](EVALUATION.md) |
| Run an opt-in beta with volunteers | [BETA.md](BETA.md), [templates/beta-feedback.md](templates/beta-feedback.md) |
| Copy a working AP configuration (exact-model opt-in, fallback, rollback) | [examples/tdd-sonnet-5-5/](examples/tdd-sonnet-5-5/) |

## Tools

Python 3 standard library only; no model calls.

| Tool | What it does |
| --- | --- |
| `tools/verify_delivery.py <example dir>` | Checks pins, exact-model routing and fallback, delivered text, the full resource export (`stamp` + `materialize filesystem-v1`, `library read`) and rollback, against released AP (default `npx @guisam/agent-profiles@0.19.4`; override with `AP_CMD`) |
| `tools/check_package.py <pkg> [--compare <baseline>]` | Package closure: manifest, `LICENSE`, references, scripts, cross-skill dependencies, changed files |
| `tools/preflight.py …` | Isolation preflight per arm: global instructions, hooks, duplicate installations, other-arm content, environment leaks, and an optional `init` probe |
| `tools/campaign.py check\|plan <campaign.json>` | Validates a campaign definition and prints a deterministic, balanced slot schedule |
| `tools/results_format.py validate <file>` | Validates `apsp-results/1` (structure plus privacy scan) |
| `tools/test_workflow_tools.py` | Tests for the tools above (18) |

The schema is in `schemas/results.schema.json`.

The experiment-specific reference implementations are in
`experiments/tdd-compaction/tools/`:

- the harness, with a Claude Code launcher and checkers;
- the audit tools;
- the sanitized exporter.

## Status

- Released AP 0.19.4 is verified locally for the configuration, routing,
  fallback, delivery, resource export and rollback.
- No variant is adopted. The TDD Sonnet 5.5 candidate is an opt-in beta only,
  with screening evidence ([CLOSEOUT](../experiments/tdd-compaction/CLOSEOUT.md)).
- Gaps are listed in [GUIDE.md](GUIDE.md#not-demonstrated-by-this-project-gaps-stated-plainly).
