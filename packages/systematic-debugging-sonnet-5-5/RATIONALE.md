# Rationale: `@apsp/systematic-debugging-sonnet-5-5@0.1.0`

**Status: UNVALIDATED candidate (2026-11-08). Not adopted, not selected by
any consumer, no model trial run.** The target is exact model `claude-sonnet-5-5`
on a subscription-backed Claude Code host. Every other model, and this one
until behavioral evidence exists, uses `@apsp/systematic-debugging-upstream@7.0.2`.

- Contract inventory and the contradictions (C1-C6), which are flagged and
  left as they are: [CONTRACT.md](../../experiments/systematic-debugging-compaction/CONTRACT.md).
- Evaluation plan: [PROPOSAL.md](../../experiments/systematic-debugging-compaction/PROPOSAL.md).
- Prepared with the Agent Profiles `skill-compaction` skill (preset 1.0.5,
  `examples/presets/skill-compaction` in the local Agent-Profiles checkout).

## What changed

Only `SKILL.md` changed. The frontmatter is byte-identical, so selection
metadata is the same. All five resources and `LICENSE` are byte-identical to
the baseline. These sections are byte-identical, checked by content
comparison: Overview, Iron Law, When to Use, the Four Phases intro, Phase 4
(all five steps), Red Flags, partner signals, Common Rationalizations,
"No Root Cause" and Supporting Techniques.

The rewrite is confined to Phase 1-3 and the Quick Reference table:

```text
Phase 1 items 1-3          bullet/question lists → one directive sentence each
Phase 1 item 4             pseudo-code block → one paragraph; bash example + "This reveals" deleted;
                           secret-handling condition extracted from the example
Phase 1 item 5             "Quick version" bullets → one sentence; pointer kept
(new) Phase 1 end          "Phase 1 is complete when you understand WHAT is happening and WHY."
Phase 2 items 1-4          bullets → directives
Phase 3                    "Scientific method:" label dropped; bullets → directives
Quick Reference table      deleted
```

`diff packages/systematic-debugging-upstream/7.0.2/SKILL.md packages/systematic-debugging-sonnet-5-5/0.1.0/SKILL.md`
reproduces the exact change.

## Change map

Evidence labels follow the compaction skill: **demonstrated** (behavioral, this
model and environment), **knowledge-probe-only**, **unknown**. Nothing is
demonstrated. "KP" means Petrov/dokimi on Bedrock `us.anthropic.claude-sonnet-5-5`,
self-judged, which is a different deployment from the target.

| Source passage / requirement | Candidate location | Edit kind | Evidence or assumption | Evaluation needed |
| --- | --- | --- | --- | --- |
| P1.1 read errors: 4 bullets incl. "They often contain the exact solution" | P1.1 sentence | Editorial: rationale dropped; all three directives kept (don't skip errors or warnings, read stack traces completely, note lines/paths/codes) | Not probed. Meaning-preserving | Buried-error behavior is covered indirectly by A2/A3 (error-reading precedes fix) |
| P1.2 reproduce: 3 questions + "not reproducible → gather more data, don't guess" | P1.2 sentence | Editorial: questions restated as a directive; the rule is kept with its arrow | KP: rule strict-redundant (both models) | A3 (intermittent failure) |
| P1.3 check recent changes: question + 3 bullets | P1.3 sentence | Editorial | Not probed | A2, A4 (git history is the evidence) |
| P1.4 instrumentation pseudo-code: 4 boundary checks; run once → analyze → investigate | P1.4 paragraph | Editorial: all 4 checks and the 3-step sequence kept, WHEN/BEFORE triggers verbatim | KP: rule strict-redundant (both) | A2 |
| P1.4 bash signing example (4 layers) + "This reveals: which layer fails" | deleted | **Capability-dependent**: assumes the model writes boundary instrumentation from the rule alone | **unknown** for execution. The example atom is "added" for both models, but it probes recall of example details (macOS keychain commands), which says nothing about capability | A2: multi-component failure with no worked example in context |
| Hidden condition in that example: report only whether a secret is set (fixed upstream #2375/#2380) | P1.4 "For secrets and credentials, log only whether they are set, never their values." | **Extraction**: an implicit condition made explicit. **Review point:** confirm this is an extraction, not a policy expansion. The source demonstrates it but doesn't state it as a rule | n/a (contract preservation) | A2 safety check: secret value never printed |
| P1.5 "Quick version": 4 bullets | P1.5 one sentence + pointer | Editorial: same four steps ("originates", "callers", "until you find", "fix at source") | KP: strict-redundant (both) | A1 (bug deep in call stack) |
| Quick Reference table (4 rows) | deleted; Phase 1 success criterion moved to the end of Phase 1 | Editorial: rows duplicate phase text. The only unique content, "Understand WHAT and WHY", is relocated | KP: Phase 4 row strict-redundant (both) | A1/A2 premature-fix checks |
| P2.1-2.4 bullets/questions | P2 directives | Editorial: COMPLETELY/every line/don't skim, "every difference, however small", "don't assume 'that can't matter'" all kept | KP: "read COMPLETELY" strict-redundant for Sonnet, added for Haiku. Others not probed | Covered indirectly by A1/A5. No dedicated case |
| P3 "Scientific method:" label | dropped | Editorial: a framing label with no step behind it; the steps that follow are kept | n/a | none beyond P3 cases |
| P3.1-3.4 bullets | P3 directives | Editorial: "I think X is the root cause because Y", written, specific; smallest change / one variable / no multiple fixes; worked → P4, else NEW hypothesis, DON'T add fixes on top; say "I don't understand X", don't pretend, ask for help, research more | KP: P3.1 redundant; P3.3 strict **added** / lenient redundant for Sonnet, so its wording is kept nearly verbatim | A5 (unrelated temptations, single change) |
| Format: checklists → prose in P1-P3 | throughout P1-P3 | **Format change** (not a meaning change). It may affect how reliably steps are followed | **unknown** | All screening cases. Format is confounded with wording; the trial cannot separate them |

## Kept deliberately (not compressed)

- **Pressure and reminder content:** "letter … spirit", Iron Law, When to Use
  (including "Don't skip when"), Red Flags, partner signals and the
  rationalization table. Petrov's data shows Sonnet *knows* most of it. That
  does not show the text is inert. Upstream measured a behavioral drop when a
  similar rebuttal section in TDD was compressed (8/10 → 5/10 under
  tests-after pressure, v6.4.2 release notes). These are reminders to act,
  which the compaction skill preserves.
- **Phase 4 verbatim:** its order, approval boundary, counts and skill names
  are the core contract, and probing showed nothing to gain.
- "No Root Cause" and Supporting Techniques: the only pointers to two of the
  resources, plus the exit condition.

## Contradictions

C1-C6 in CONTRACT.md are unchanged, deliberately. Fixing them would be a policy
treatment and needs its own declared experiment.

## Size (same measurement for both files)

UTF-8 bytes, `wc -c`. No Anthropic tokenizer is available offline, so tokens
are not reported.

| Measure | Baseline 7.0.2 | Candidate 0.1.0 | Change |
| --- | --- | --- | --- |
| `SKILL.md` file | 9530 | 8124 | −1406 (−14.8%) |
| `SKILL.md` body after frontmatter (what a required delivery injects) | 9388 | 7982 | −1406 (−15.0%) |
| Deferred resources (5 files, read only on demand) | 19527 | 19527 | 0 |
| Whole tree incl. `LICENSE`, `package.yaml` | n/a | n/a | −1406 on SKILL.md; the `package.yaml` descriptions differ |

This is the entrypoint reduction only. It is **not** a usage or cost claim.
Total task usage depends on turns and caching, and on whether the model now
reads `root-cause-tracing.md` more often. AP `proof` through the trial route
is measured at smoke (PROPOSAL §5).

## Identity and hashes

| | AP digest (sha256, AP 0.19.4 `add`) | `SKILL.md` sha256 |
| --- | --- | --- |
| `@apsp/systematic-debugging-upstream@7.0.2` | `f758787e9160ad1e1030825904a80d2dfdfdd57a5e0d60d163ecb4c697ca0005` | `51c6435d…` (= upstream blob `62fc752a`) |
| `@apsp/systematic-debugging-sonnet-5-5@0.1.0` | `ed798698e88a2b762104faa2871f60628cbcabb242543f9eca17a9c079091a18` | `d0ccf6df…` |

The candidate's own version line (0.x = unvalidated) is independent of upstream.
Its upstream base is recorded in `package.yaml` and here.
