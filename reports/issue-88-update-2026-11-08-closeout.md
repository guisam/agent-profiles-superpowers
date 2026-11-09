## Closeout: reusable workflow for model-specific skills, plus the TDD screening result (2026-11-08)

**Summary:**

- The companion is wrapped up as a **reusable, plugin-free workflow** for
  proposing, delivering and evaluating per-model skill variants through AP.
- **No variant is adopted.** Full upstream Superpowers 7.0.2 remains the
  default for every model.
- **Published:** https://github.com/guisam/agent-profiles-superpowers (MIT for
  the project's own content; the packages keep upstream Superpowers MIT). Raw
  transcripts, ledgers and host identifiers stay private; shared results are
  the sanitized `apsp-results/1` exports.
- **The skill-compaction preset** used to prepare the candidate is merged into
  Agent Profiles as `examples/presets/skill-compaction` (preset 1.0.5,
  AP 0.19.7, #92). No npm release or tag was made.

### What is ready to use ([`workflow/`](https://github.com/guisam/agent-profiles-superpowers/tree/main/workflow))

- **Guide:** a maintainer guide, with TDD for `claude-sonnet-5-5` as the
  worked example.
- **Example AP config v3:** the baseline binding, one exact-model, one-role
  assignment, a rollback config, and a trial-scoped trust policy.
- **Pinned identities:** upstream commit and blob IDs, per-file sha256, AP
  digests. Plus a change map that links each edit to the requirement it
  preserves and to its evidence.
- **Tools** (Python stdlib, no model calls):
  - `verify_delivery.py`: AP pins, routing, delivered text, resource export,
    rollback;
  - `check_package.py`: references, scripts, cross-skill dependencies;
  - `preflight.py`: isolation, covering global instructions, hooks, duplicate
    installations, other-arm content and environment leaks, plus an `init`
    probe;
  - `campaign.py`: a balanced, seeded schedule;
  - `results_format.py`: the sanitized `apsp-results/1` format, with a privacy
    scan.
  - 18 tests.
- **An opt-in beta process:**
  - controlled campaigns (one configuration per report, never pooled) are kept
    separate from everyday feedback (a reviewed template; no automatic
    uploads);
  - explicit rollback;
  - unknown models fall back to full content.

### Verified on AP 0.19.4 (the released npm version), locally, no model calls

- **Pins:** both packages' bytes match their pins, and the AP digests reproduce
  (`ce680b8a…` baseline, `bd446f96…` candidate).
- **Routing:** `claude-sonnet-5-5` gets the candidate. Haiku 5.5, Opus 5.5,
  the near-miss `claude-sonnet-5`, an unlisted ID and an unstated model all get
  the baseline.
- **Delivered text:** `resolve` delivers the exact selected `SKILL.md`, never
  the other one.
- **Resources:** `stamp` plus `materialize --adapter filesystem-v1` exports
  the full package tree byte-identically, and `library read` returns each
  resource.
- **Rollback:** removing the assignment and running `install` returns every
  model to the baseline.

### Not demonstrated: gaps

- **Interactive delivery through AP's `CLAUDE.md` bootstrap** was not
  evaluated by this project. AP's own host observations rate Sonnet routing
  through the bootstrap as "limited".
- **AP does not detect the model.** It relies on the host-stated, or
  launcher-given, model ID. No native host integration ships.
- **Native discovery:** the `claude-plugin-v1` adapter is only on an
  unreleased branch, and `--safe-mode` with `--plugin-dir` did not list the
  plugin's skill. Discovery is untested.
- **Cross-skill dependencies** (`writing-skills`, `writing-plans`) are not
  packaged.
- #89, #90 and #91 still stand.

### TDD compaction for Sonnet 5.5 (`apsp-tdd-001`), closed

**What was compared:**

- **Candidate:** `SKILL.md` goes from 9,578 to 7,025 bytes. The cycle diagram
  and three worked examples are removed. Every rule, rationalization row, red
  flag and checklist item is kept; the resources are byte-identical.
- **Setup:** Sonnet 5.5, Claude Code 2.1.319 headless, AP-resolved context
  appended to the system prompt.
- **Isolation:** checked on every run. There were no plugins, skills, hooks or
  MCP servers beyond 5 built-ins, and 0 Ponytail hits.
- **Suite:** 7 screening cases × 2 arms × 3 reps = 42 valid runs, with 2 blind
  Opus graders for the claims-vs-evidence check.

**Result:** stage 1 = **PROCEED**. Under the accepted adjudication rules (the
operator gate), **18/21 vs 18/21, with all 21 paired reps tied**, and Gr1
24/24. The accepted rules are:

- **R2:** a capture correction. RED was demonstrated in the full output; the
  agents' grep had hidden Node 24's summary line.
- **R3:** a fixture correction. A hidden assertion used tuple input, but the
  request said "list".
- **R5:** following an explicit "skip tests" instruction and disclosing it
  complies.
- **R6:** compliant means asking before taking the configuration-file
  exception, or writing a failing *behavior* test first. A value-only test
  doesn't count. **No run in either arm did either.**

The official frozen-checker scores (12/21 vs 14/21) are kept for provenance.

**Tokens:** 9.31% fewer in total execution usage (input + cache creation +
cache read + output, 21 runs per arm). This is mostly the smaller system prompt
re-read on every request (1,134 fewer tokens on the first request). Skill size
is −2,553 bytes.

**What this supports:**

- no observed regression in this screening suite;
- contract review plus behavioral screening as evidence of preserved integrity
  within the tested scope.

**What it does not show:**

- equivalence;
- held-out performance;
- discovery delivery;
- other models or hosts;
- readiness for adoption.

**Shared behavior on identical text** (the R6 approval gap; R5 under the
strict reading) describes the base skill on this model. It is not evidence the
policy survives.

**Stage 2:** a held-out confirmation (10 independent cases × 12 reps,
−15-point margin) was designed and **not funded**. It is kept as the campaign
template.

**Cost** (API-equivalent, actually used against the subscription allowance):

- children and graders: $2.71;
- coordinator build-and-run overhead: about 24.7M tokens (measured);
- the audit and closeout sessions: not measured.

**No further model calls** were made for the closeout.

### Acceptance criteria changes since the last update

- **Publication readiness:** ✅ published (sanitized; raw evidence private).
- **Frozen cases and rubric, plus logging checks before runs:**
  - `apsp-tdd-001` was frozen before runs. Amendments 0 and 1 came before
    stage 1; Amendment 2 came mid-stage, was operator-approved and is
    documented.
  - The current freeze verifies.
  - Coordinator usage was measured for the build-and-run window.
- **Findings separate knowledge, delivery, behavior and cost:** FINDINGS §8
  added.

### Key links

- Guide: [workflow/GUIDE.md](https://github.com/guisam/agent-profiles-superpowers/blob/main/workflow/GUIDE.md)
- Evaluation method: [workflow/EVALUATION.md](https://github.com/guisam/agent-profiles-superpowers/blob/main/workflow/EVALUATION.md)
- Beta process: [workflow/BETA.md](https://github.com/guisam/agent-profiles-superpowers/blob/main/workflow/BETA.md)
- TDD closeout: [experiments/tdd-compaction/CLOSEOUT.md](https://github.com/guisam/agent-profiles-superpowers/blob/main/experiments/tdd-compaction/CLOSEOUT.md)
- Findings: [FINDINGS.md](https://github.com/guisam/agent-profiles-superpowers/blob/main/FINDINGS.md)

### Still open

1. Whether to offer the workflow to obra/Superpowers. A maintainer summary is
   drafted in the companion (`reports/maintainer-summary.draft.md`); nothing
   has been sent.
2. Petrov's dataset terms. It is still linked only, not copied.
3. Whether to close this issue, with `writing-plans`/`writing-skills`
   packaging, discovery delivery and the native host route moved to follow-ups.
