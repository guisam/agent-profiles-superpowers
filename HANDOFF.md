# Agent Profiles + Superpowers companion

Start with the task and acceptance criteria in:
https://github.com/guisam/Agent-Profiles/issues/88

This folder is the separate companion project. Keep skill packages, model-specific variants and evaluations here; keep generic AP changes in Agent-Profiles.

Local references:
- ../Agent-Profiles — AP implementation and public examples/superpowers
- ../superpowers — upstream reference checkout; do not modify it casually
- ../workflow-skills/experiments/superpowers — initial trial, findings and model-tailoring preparation

Read issue #88 before implementation. Begin with provenance and licensing, one baseline skill and one candidate. Preserve supporting scripts/templates and distinguish knowledge evidence from behavioral results.

Nothing has been installed, imported, signed or published here. No remote repository has been created. Use existing subscription-backed sessions; no new paid purchases. Keep private session records and development configuration out of public packages.

---

## Status after first slice (2026-11-07, Claude, implementer role)

Scope: issue #88, brainstorming only. Everything is local; nothing is committed
(this folder is not a git repository), pushed, published, signed or filed.

Done (verified):
- Skeleton, credit, license audit and provenance: `README.md`, `PROVENANCE.md`.
- Source mapping: new baseline v7.0.2 `22f0b46`, very likely the study's checkout
  (inference; evidence in PROVENANCE).
- Packages: `@apsp/brainstorming-upstream@7.0.2` (immutable baseline,
  `5f4f5b6f…`) and `@apsp/brainstorming-sonnet-5-5@0.1.0` (`759b3a0c…`,
  **rejected**). Haiku has no candidate.
- Frozen suite, protocol and collector: `evaluations/brainstorming/`
  (`FREEZE.sha256`; the pre-run and post-smoke collector amendments are recorded
  in PROTOCOL.md; cases and rubric are unchanged since freeze).
- Pilot `apsp-bs-001`: 44 Sonnet runs plus 12 Opus grader runs. Results in
  `evaluations/brainstorming/RESULTS.md`; findings in `FINDINGS.md`.
- Two-consumer routing, fallback and isolation were demonstrated with AP 0.19.4
  (FINDINGS §3).

Private, ignored (`private/`): consumers, store, trial trust policy, run copies,
raw transcripts (sha256 in each `result.json`), grader bundles, keys and
grades, `routing-*.md`, `isolation-*.md`. *[Corrected by the audit below: the
`runs.jsonl` ledger at `evaluations/brainstorming/runs.jsonl` holds host agent
IDs and was **not** ignored when this was first written. `.gitignore` now
excludes it.]*

Commands (from this folder):
- `python -I evaluations/brainstorming/tools/collect.py selftest`
- `prepare <case> <arm> <rep>` / `prompt <run>` / `collect <run> <agentId>` /
  `bundle <case> <tag>` / `score <tag> <case> <grades.json>`
- Resolve as a child does: see `collect.py prompt <run>` (uses
  `AGENT_PROFILES_TRUST=private/trust.trial.yaml`).

Unresolved questions (need the maintainer):
1. Owner and visibility for a remote repository; whether to `git init` and commit.
2. Whether to ask Petrov for dataset redistribution terms.
3. Whether to file the AP gaps in FINDINGS §6 as Agent-Profiles issues.
4. Whether `runs.jsonl` and the per-case grades can be published in sanitized form.

Recommended next step: a separate, declared treatment rewriting L164-166 for
clarity ("one sensible way → design in the next message"). It needs a new suite
version, with C01 revised, more repetitions, and Haiku and Sonnet pairs. Every
model stays on full content until then.

---

## Status after cleanup and evidence audit (2026-11-07, Claude, implementer role)

Scope: local, reversible cleanup and audit. No model trials ran. Nothing was
committed, pushed, filed, signed or published, and the global plugin and trust
policy are unchanged. The baseline and rejected candidate packages are
unchanged: their AP digests reproduce, and `private/PRESERVED-2026-11-07.sha256`
lists 470 preserved artifacts.

Changes:
- **Privacy:** `.gitignore` now excludes `evaluations/*/runs.jsonl` and
  `__pycache__/`. A scan found host agent IDs only in that ledger; the public
  files contain no session ID and no user paths. Ignore rules were verified with
  `git check-ignore` in a scratch repository.
- **Freeze:** the original `FREEZE.sha256` is kept and not regenerated.
  [audit/FREEZE-STATUS.md](evaluations/brainstorming/audit/FREEZE-STATUS.md)
  reconstructs both frozen files byte-for-byte (hashes match) and separates
  content-established facts from timestamp chronology (supporting only;
  wording qualified in audit revision 2) and from claims that rest on the
  coordinator's account. The
  first, pre-amendment freeze was overwritten and is unrecoverable.
- **Harness v2:** `tools/collect_v2.py` (2.0.0) plus `tools/test_collect_v2.py`
  (11 tests). It adds opaque run tokens, strict grade validation, unknown-aware
  usage, and delivery checking by package body. v1 `collect.py` is unchanged
  (`298eaee4…`); no artifact was recollected. Read-only checks show v1's latent
  defects altered no recorded number or grade.
- **Audit:** [GRADING-ADJUDICATION.md](evaluations/brainstorming/audit/GRADING-ADJUDICATION.md)
  and [CORRECTIONS.md](evaluations/brainstorming/audit/CORRECTIONS.md), kept
  separate from RESULTS.md, which is unchanged.
- **Docs:** README and selectors label `beta` as an archived trial
  configuration and recommend the baseline. FINDINGS has an audit-corrections
  section and links to the gap reports.
- **Proposal:** [experiments/brainstorming-clarify-164/PROPOSAL.md](experiments/brainstorming-clarify-164/PROPOSAL.md)
  (`apsp-bs-002`, not frozen, not run).
- **AP gap drafts:** `reports/AP-GAP-1…`, `reports/AP-GAP-2…`, with
  `reports/repro-ap-gaps.sh`, verified on AP 0.19.4. Not filed; AP core is
  untouched.

Conclusions that changed:
- The C02 regression is not supported under a consistent reading. The candidate
  stays rejected for lack of benefit.
- The trials were not label-blind: run IDs with arm and case names were in
  every prompt.
- C01 is non-discriminating, C08 covered only missing-document recovery, and
  C06 is a sequencing failure with the gate intact.
- C11's zero server starts reflects the harness instruction.

Remaining limitations:
- The audit is by the same coordinator who designed and ran the experiment; it
  is not independent validation.
- Native-plugin visibility in children was not controlled.
- The overwritten first freeze cannot be verified.
- Intermediate collector versions during the pilot are evidenced only by
  re-collection timestamps.

*[Superseded by proposal r2 below: r1's 132-run / $19 figure was inconsistent,
and its treatment added mandatory confirmation.]* Every model stays on full
content.

Checks: `python -I evaluations/brainstorming/tools/collect.py selftest` and
`cd evaluations/brainstorming/tools && python -E -s test_collect_v2.py`.

---

## Status after proposal revision r2 (2026-11-07, Claude, implementer role)

Scope: preparation only. No model calls, no new runs. Nothing was committed,
filed, published or sent externally, and AP core is untouched. The original
evidence and packages are unchanged: `private/PRESERVED-2026-11-07.sha256`
verifies 470/470.

Changes:
- **experiments/brainstorming-clarify-164/** (`apsp-bs-002`, draft, not
  frozen):
  - `PROPOSAL.md` r2; r1 kept as `PROPOSAL-r1-superseded.md`.
  - `TREATMENT.md`: a sequencing-only edit of L164-166 that preserves
    delegation and adds no confirmation. The policy treatments P1 and P2 are
    listed separately and not proposed.
  - `cases.draft.json`: 8 screening cases + 3 validation recovery cases.
  - `RUBRIC.draft.md`: approval violations defined per scenario; N1 excluded
    from the stop rule.
  - `INVENTORY.md`: exact counts and the budget.
  - `fixtures/` (`habit`, `habit-sync`, `habit-approved`).
- **audit/FREEZE-STATUS.md** revision 2 separates content-established facts
  from timestamp chronology. Content facts:
  - reconstructed hashes;
  - prompt identity;
  - all 44 results written by the final collector (verified: `reply_source`
    and `prompt_exact` in 44/44, absent from the frozen collector).
- **audit/CORRECTIONS.md** item 10: coordinator usage was measurable. It was
  ≈ $8.8 API-equivalent over the approximate trial window, larger than either
  arm. Item 7 is qualified.

Awaiting review:
- Stage 1 Sonnet screening: 48 analyzed + 4 smoke + ≤ 5 retries child runs,
  and 16 + 2 + ≤ 2 grader runs. Estimate ≈ $21 API-equivalent (≈ $12-$28),
  subscription usage only.
- Stage 2 runs only after a PROCEED and a separate approval.
- Before freeze: harness v2.1 (per-case fixtures, continuation turns, per-case
  gates, two-grader bundles, with tests).
- Held-out H1-H4 authorship is assigned after the treatment is frozen.

---

## Status: apsp-bs-002 stage 1 halted before grading (2026-11-07)

- **Built and tested:** harness 2.1.0 (`collect_v2.py`, 23 tests passing) with
  per-case fixtures, continuations built from the same arm and repetition's
  actual reply (`prompt_exact` 49/49 on valid runs), scenario gates,
  two-grader scoring and the frozen decision rule. The treatment package is
  `@apsp/brainstorming-sequencing@0.1.0`.
- **Freeze:** stage-1 freeze 1.0.0 (54 files) verifies. No amendments were
  made. The smoke runs needed no change.
- **Children:** 48/48 analyzed slots are valid, so the matched pairs are
  complete. 53/57 child calls and 1/5 retries were used. One run was throttled
  and retried.
- **Grading:** blocked. 6 grader calls hit the Opus 5-hour limit, leaving 12
  of the 20 grader calls, while two-grader scoring needs 16. Stage-1 outcome:
  **INCONCLUSIVE (unscored)**. No behavioral conclusion is drawn.
- **Recorded observations, not results:**
  - one control-arm design-gate violation (S1c full, rep 2);
  - the Ponytail SubagentStart hook was injected into every child in both
    experiments (confound);
  - the billing route may have changed after the first pause (operator added
    credits).
  See `experiments/brainstorming-clarify-164/stage1/EXECUTION-LOG.md`.
- **Evidence:** `private/PRESERVED-bs002-stage1.sha256`.
- **Operator decision needed:** either (a) a documented amendment raising the
  grader limit to at least 24, so the 16 required calls fit after the 8
  already used, with no change to anything children or graders see; or
  (b) close stage 1 as INCONCLUSIVE. Grade only after the Opus limit resets.
  Stage 2 remains unauthorized, and every model stays on full content.

---

## apsp-bs-002 stage 1 graded under Amendment 1 (2026-11-07)

- **Grading:** 16 additional grader attempts, all completed; 24 of 24 actual
  attempts used. The frozen freeze is unchanged (54/54), and the pre-grading evidence manifest verifies for every file
  except the append-only ledger: its earlier content is exactly the first 132
  lines of the current 191, so later events were only appended.
- **Official outcome:** INCONCLUSIVE. U1 and U2 grader files are
  byte-identical (unanimous all-pass), and the frozen guard rejects that. The
  transcript audit shows independent grading.
- **Provisional outcome:** STOP-NEGATIVE, if the guard is overridden; this is
  not approved. The primary endpoint is scored officially: 0/6 (full) vs 0/6
  (seq). The sequencing clarification produced no observed change.
- **Report:** `experiments/brainstorming-clarify-164/stage1/RESULTS.md`.
  Evidence: `private/PRESERVED-bs002-stage1-graded.sha256`.
- **Operator decision needed:** approve or reject a guard override for U1/U2.
  Either way, the treatment is not adopted. Stage 2 is unauthorized, and every
  model stays on full content.

---

## apsp-bs-002 closed: corrected STOP-NEGATIVE under Amendment 2 (2026-11-08)

- **Override (operator-approved, conditional, condition met):** U1/U2 were
  scored despite byte-identical grade files.
  `private/bs002_amend2_score.py verify` confirmed four separate grader
  executions with no access to each other's output.
  `bs002_amend2_score.py run` scored U1/U2 from the existing files, using the
  frozen validate/combine/decide and skipping only the byte-equality check.
  It made no model calls.
- **Outcomes:** original procedural INCONCLUSIVE (kept); corrected
  **STOP-NEGATIVE**.
  - Primary endpoint 0/6 vs 0/6: no observed improvement in the tested
    environment, which included the Ponytail instructions and the native
    Superpowers listing. This is not generalized to standalone Superpowers
    or other models.
  - S3 dropped by 2 runs.
- **Preserved:**
  - freeze 54/54;
  - official `s1/scores.jsonl` unchanged (`b8df6494…`);
  - the graded-evidence manifest verifies for every file except the
    append-only ledger.
  The corrected aggregate is in `private/grading-v2/apsp-bs-002/s1-amend2/`.
- **Disposition:** the sequencing candidate is retired: no stage 2, no
  adoption, no further rewrite experiment. Every model stays on full upstream
  7.0.2 content.
- **Future harness fix (not implemented):** replace the byte-equality guard
  with a grader execution and provenance check
  (`stage1/AMENDMENT-2-identical-file-override.md`).
- **Draft for review, not posted:** `reports/issue-88-update.draft.md`.
- **Still open for the maintainer:** the four questions above
  (remote/commit, Petrov terms, filing AP gaps, publishing sanitized ledgers).
  Also, whether to post the issue update.

---

## First slice wrapped up (2026-11-08)

- **Outcome:** no variant is adopted, and every model is on full upstream
  7.0.2 (`selectors/alpha.agents.yaml`).
  - Shortening (`apsp-bs-001`) was rejected for lack of benefit.
  - The sequencing clarification (`apsp-bs-002`) is retired: original
    INCONCLUSIVE, corrected STOP-NEGATIVE.
  - Status notes: `packages/*/STATUS.md`.
- **Checks run 2026-11-08 (no model calls):**
  - bs-002 freeze 54/54.
  - bs-001 freeze: the 2 known mismatches, and both reconstructions still
    reproduce the frozen hashes.
  - Preserved manifests: 470/470; 501 and 519 match except the append-only
    ledger, which is an exact prefix.
  - `collect.py selftest`, and 23/23 `test_collect_v2` tests.
  - Amendment-2 provenance verify; package digests via AP 0.19.4 add (all 3
    match).
  - `repro-ap-gaps.sh` on AP 0.19.4.
- **AP gaps filed:** Agent-Profiles #90 (bug, resolve text identity), #91
  (bug, misleading update error), #89 (enhancement, cross-package update).
- **Issue #88:** the progress update was posted, with the text in
  `reports/issue-88-update-2026-11-08.md`. The issue stays open.
- **Acceptance gaps:**
  - dependency closure (`writing-plans` not packaged);
  - helper runtime qualification (syntax checks only);
  - apsp-bs-001 freeze integrity (reconstructed, first freeze lost);
  - post-execution amendments in apsp-bs-002;
  - publication readiness (no remote).
- **Git:** a local repository with one reviewed commit. No remote, no push.
  `private/`, raw transcripts, ledgers, `graft/` and fixture `node_modules`
  are ignored.
- **Decisions for the maintainer:**
  - remote owner/visibility and push;
  - Petrov dataset terms;
  - publishing sanitized ledgers and grades;
  - whether the partial criteria go to follow-up issues.

---

## apsp-sd-001 prepared: systematic-debugging compaction for Sonnet 5.5 (2026-11-08)

Scope: preparation only. No model trials, no adoption, no selection change,
no publication, and AP core and global configuration are untouched. Earlier
experiments and their artifacts are unchanged. Nothing is committed.

- **Target:** `systematic-debugging` for `claude-sonnet-5-5` on subscription
  Claude Code. It has the strongest Sonnet knowledge signal of Petrov's three
  nominations (strict 0.88), most of the explanation of familiar mechanics,
  and an objectively testable contract. The evidence is knowledge-probe-only
  from Bedrock and self-judged; nothing transfers it to this deployment.
- **Packages:**
  - baseline `@apsp/systematic-debugging-upstream@7.0.2` (`f758787e…`,
    byte-exact from upstream blobs);
  - candidate `@apsp/systematic-debugging-sonnet-5-5@0.1.0` (`ed798698…`,
    **unvalidated**). `SKILL.md` goes 9530 → 8124 bytes (−14.8%). The
    frontmatter, Phase 4 onward and all resources are byte-identical. The only
    capability-dependent cut is the Phase 1.4 worked shell example; its
    secret-handling condition is extracted into text.
- **Docs:**
  - `experiments/systematic-debugging-compaction/` holds CONTRACT (contract,
    contradictions C1-C6, content-mapped evidence), CASES.draft (7 screening
    cases) and PROPOSAL (evaluator choice, host isolation audit, delivery
    route, staged counts, acceptance criteria, harness 2.2 fixes, budget,
    blocking questions);
  - change map: `packages/systematic-debugging-sonnet-5-5/RATIONALE.md`.
- **Host audit findings:**
  - account-synced Superpowers **6.4.2** (a different SD text);
  - `engineering:debug`, Ponytail and graft hooks;
  - T3/Claude environment variables would reach children.
  Agent-tool subagents cannot be isolated. The proposal uses `claude -p
  --safe-mode …` with an environment scrub, to be verified at smoke.
- **Harness 2.1.0 defects relevant here (not fixed):**
  - `grader_prompt` ledgers an attempt on render;
  - `prepare` counts undispatched runs and blocks their retry;
  - `score` rejects identical grade files;
  - `bundle_runs` silently bundles fewer packets.
- **Next:** operator review of PROPOSAL §10 questions 1-6, then pre-freeze
  work (§11), then stage 0 smoke. Every model stays on full upstream content.
- **Checks run (no model calls):**
  - blob hash match for all 7 baseline files;
  - candidate invariants (frontmatter and retained sections byte-identical, no
    unhyphenated keyword, no `$1` tokens, all references kept);
  - AP 0.19.4 `add` of both packages to a throwaway store.
- **2026-11-08, after preparation:** at the operator's request, Ponytail 4.13.0
  was uninstalled at user scope (`claude plugin uninstall ponytail@ponytail`).
  It had still been enabled globally; only some other projects had local
  `false` overrides. The backup of the three plugin config files is in
  session scratch only. The coordinator session that prepared `apsp-sd-001`
  still had Ponytail's SessionStart text in context; children launched later
  will not.

---

## START HERE in a fresh session: Ponytail-free re-runs (2026-11-08)

Ponytail contaminated every prior child run, through a `SubagentStart` hook
(97/97 transcripts) and its skill listing. It was uninstalled at user scope,
and its cached hook scripts and state files were moved to the old session's
scratchpad. The old session still held Ponytail in memory, so a canary from
it still saw the Ponytail skill listing (the hook injection was gone). Hence
this fresh session.

Operator instruction: **if Ponytail appears anywhere in an experiment,
stop immediately and tell the operator.**

1. **Canary first.** Launch one Agent-tool subagent (model `sonnet`, prompt
   "Reply with exactly the word: canary. Do not use any tools."). Read its
   transcript under
   `~/.claude/projects/c--workspace-agent-profiles-superpowers/*/subagents/agent-<id>.jsonl`.
   Fail if any `attachment` record (hook results, hook context,
   `skill_listing`) contains "ponytail", case-insensitive. On failure, stop
   and report.
2. **Reassess** the `apsp-sd-001` candidate and proposal. They were written
   with Ponytail's instructions in the coordinator's context. Review
   `packages/systematic-debugging-sonnet-5-5/RATIONALE.md` and
   `experiments/systematic-debugging-compaction/` without that bias.
3. **Re-run the tainted experiments** as new, separately named replications
   (`apsp-bs-001` and `apsp-bs-002` stage 1). Use the same frozen cases,
   rubric and method. *[Revised 2026-11-08, operator: the synced Superpowers
   6.4.2 plugin stays off (`superpowers@synced: false`). Original skill text
   comes only from AP baseline packages built from `c:\workspace\superpowers`
   (v7.0.2, `22f0b46`); if a full-original variant is needed, add an AP
   profile, never a plugin install. So the replications differ from the
   originals by two removed confounds, Ponytail and the 6.4.2 listing; record
   both as declared deviations.]* Never overwrite the
   originals' runs, ledgers or results: use new experiment IDs, ledgers and
   run directories.
4. **Keep scanning.** Check every child and grader transcript for "ponytail"
   during collection, and stop on the first hit.

---

## apsp-tdd-001 prepared: test-driven-development compaction for Sonnet 5.5 (2026-11-08)

Fresh session, started per the operator's instruction for a new bounded
compaction experiment. Scope: preparation only. No model calls, trials,
adoption, selection change, publication, AP-core or global-config change.
Earlier experiments are untouched, including the uncommitted `apsp-sd-001`
files. The HANDOFF "START HERE" items above (canary, `apsp-sd-001`
reassessment, Ponytail-free re-runs) were **not** done in this session. This
coordinator context had no Ponytail text.

- **Target:** `test-driven-development` × `claude-sonnet-5-5`.
  - Sonnet strict 0.80 / lenient 0.96 (Petrov, Bedrock, self-judged).
  - All 4 strict-added atoms are in retained text.
  - The removable bulk is examples and a diagram.
  - The contract is objectively checkable.
- **Packages:**
  - baseline `@apsp/test-driven-development-upstream@7.0.2` (`ce680b8a…`);
  - candidate `@apsp/test-driven-development-sonnet-5-5@0.1.0` (`bd446f96…`,
    **unvalidated**). `SKILL.md` goes 9578 → 7025 bytes (−26.7%).
  - The edits are deletions only: the dot diagram, the RED/GREEN code examples
    and "Example: Bug Fix".
  - One line is extracted from the diagram: "Fails for another reason? Go back
    to RED".
  - Every rule, rationalization row, red flag, checklist item, the frontmatter
    and `writing-good-tests.md` are unchanged.
- **Docs:**
  - `experiments/tdd-compaction/`: CONTRACT (contract, inbound references,
    contradictions T1-T10, evidence map), CASES.draft (R1-R6, N1 required;
    D1-D2 discovery), PROPOSAL.
  - Change map: `packages/test-driven-development-sonnet-5-5/RATIONALE.md`.
- **Key host finding:** the account-synced Superpowers plugin has a TDD
  `SKILL.md` **byte-identical to the baseline**. Unisolated candidate runs would
  be contaminated. The proposal requires `init`-verified isolation and stops
  otherwise.
- **Evaluator:**
  - `collect_v2.py` → bounded 2.2.0, with the four failure-mode fixes verified
    against the code.
  - superpowers-evals/quorum + AP plugin arms was inspected but is not runnable
    here: no Gauntlet, Docker down, no Sonnet 5.5 credential, campaign comparisons
    need the appliance.
- **Plan:**
  - stage 0: 4 child runs + 1 grader run;
  - stage 1: 42 R + 12 D analyzed (max 65 child / 12 grader);
  - estimate ≈ $50 API-equivalent; subscription only.
- **Next:** operator answers PROPOSAL §10 Q1-Q6, then pre-freeze work (§11).
  Every model stays on full upstream content.
- **Checks run (no model calls):**
  - `git hash-object` matches for all 3 upstream files;
  - candidate invariants (deletions-only + 1 insertion; frontmatter identical;
    link, headings and key contract strings present; no `$` tokens);
  - AP 0.19.4 `add` of both packages, twice for the candidate (same digest).
- **Not committed.**

---

## Canary and plugin state (2026-11-08, fresh session)

- The `engineering` plugin is no longer installed. Its files are in
  `~/.claude/plugins/.trash/` and are not loaded.
- A canary Sonnet Agent-tool subagent replied "canary". Its transcript has no
  "ponytail", no "engineering" and no Superpowers skills in the skill listing;
  every "superpowers" hit is the repo path. graft hooks and the `trail` skill
  still reach children in both arms.
- Operator decision: do not install or enable Superpowers. Test originals via
  the AP `*-upstream` packages built from `c:\workspace\superpowers`, or with
  additional AP profiles that use the full original source. See revised
  START HERE item 3.

---

## apsp-tdd-001: approved, frozen, smoke passed, stage 1 running (2026-11-08)

- **Operator decisions:** PROPOSAL §10.1. Stage 0 and stage 1 are approved;
  `bypassPermissions`; the D-block is dropped if its isolation fails; the
  operator audits after grading; the trust policy is reaffirmed; R5 and R6
  readings are confirmed; R2's `dates` failure is not graded at all.
- **Amendment 0** (pre-freeze, `stage1/AMENDMENT-0.md`):
  - the D-block is dropped: `--plugin-dir` under `--safe-mode` lists 17
    built-in skills and not the plugin's skill, and `claude-plugin-v1` is not
    in AP 0.19.4;
  - harness 2.2.0 is a new module, `tools/tdd_harness.py`;
  - AP's "Run again" section is stripped from both arms' contexts.
- **Amendment 1** (smoke finding, `stage1/AMENDMENT-1.md`): the children edit
  only through Bash heredoc scripts chained with `| tail`-piped test runs.
  Checker 2.2.1 splits commands into ordered sub-events and reads outcomes
  from runner summaries. One permitted smoke repeat was used.
- **Freezes:** `stage1/FREEZE-1.0.0.sha256` (kept) and `FREEZE-1.1.0.sha256`
  (current, 95 files).
- **Stage 0 passed** (`private/tdd001/stage0-passed.json`):
  - isolation, delivery per arm and the grader check all verified;
  - AP proof bytes: 9578 → 7025 for the skill;
  - cost about $0.05 per child and $0.07 per grader;
  - the cap-hit behavior of `--max-budget-usd` is unobserved.
- **Private state:** `private/tdd001/`
  - ledger: `ledger.jsonl`;
  - runs: `runs/<token>/`;
  - arm key: `key.json`;
  - consumers, store and trust.
- **Stage 1:** `python -I experiments/tdd-compaction/tools/tdd_harness.py run
  stage1`, then for R1-R4: `bundle stage1 <C>`, `grade stage1 <C> 1`,
  `grade stage1 <C> 2`, `score stage1 <C>`. Then the operator audit packet.
  `decide` waits for `private/tdd001/audit/audit.json` with
  `{"complete": true}`.
- Tests: `cd experiments/tdd-compaction/tools && python -I test_tdd_harness.py`
  (45); `python -I tools/tdd_harness.py selfcheck` (48 expectations).

### apsp-tdd-001 stage 1 complete; awaiting operator audit (2026-11-08)

- 42/42 slots are valid; 8/8 graders valid. Amendment 2 was operator-approved
  after an R5 matched-failure stop. Current freeze: `stage1/FREEZE-1.2.0.sha256`;
  harness 2.2.2, 51 tests.
- **Official outcome:** INCONCLUSIVE (audit pending). If the audit confirms the
  verdicts, `decide` would output PROCEED (request stage-2 approval). See
  `stage1/EXECUTION-LOG.md`.
- **Next (operator):** review `private/tdd001/audit/AUDIT-PACKET.md` (27
  items) and fill in `private/tdd001/audit/audit.json`, setting
  `"complete": true`. Then run `python -I
  experiments/tdd-compaction/tools/tdd_harness.py decide`.
- **Known measurement issues** (for the audit):
  - R2 run outcomes are unknown because the agents' grep removed Node 24's
    `ℹ fail` summary;
  - the R3 hidden test passing a tuple is over-specified;
  - the Gr1 packets' 12-line output tail caused at least 2 false Gr1 failures.
  Fix these in any stage-2 harness before freezing it.
- Stage 2 is not approved. Every model stays on full upstream 7.0.2. Nothing is
  committed.

### apsp-tdd-001 stage 1: agent audit done; human gate pending (2026-11-08)

- **Scope:** local audit and preparation only. No model calls, no commit, no
  stage-2 start. Frozen inputs, official scores, grader files, transcripts and
  the ledger are unchanged, and `FREEZE-1.2.0` verifies. `audit.json` is
  untouched (`complete: false`).
- **Agent audit** of all 42 runs (`private/tdd001/audit/AGENT-AUDIT.md`,
  `agent-adjudication.json`, `evidence/`): 12 proposed corrections in 7 runs.
  - R2: RED is demonstrated in all 6 runs; M2 and M5 = false were capture
    failures; the 3 Gr1 failures are tail artifacts.
  - R3: full 1 fails only an unsupported tuple assertion (fixture defect).
  - R5 and R6: the verdicts stand, with their interpretation documented.
- **Outcome:** official INCONCLUSIVE (audit pending). Conditional PROCEED in all
  16 combinations of the open judgments.
- **Report:** `experiments/tdd-compaction/stage1/RESULTS.md`. The 9.31% token
  figure is verified as total execution usage across all four categories.
  Most of it comes from 1,134 fewer prompt tokens per request.
- **Next (operator):** `stage1/HUMAN-GATE.md` (7 items). Then
  `stage2/PROPOSAL.md` (draft r1: 10 held-out cases × 2 arms × 12 reps,
  ≈ $30-60 API-equivalent, ceiling $188 excluding coordinator) and
  `stage2/AUTHORING-BRIEF.md` (an independent author is required).

### apsp-tdd-001 stage-1 human gate closed: official PROCEED (2026-11-08)

- **Gate decisions** (`stage1/HUMAN-GATE.md`): the R2 and R3 corrections are
  accepted; R5 intended policy = permission reading; R6 = ask, or a behavior
  test first (value tests don't count).
- **Official `decide`:** PROCEED (`private/tdd001/decide-stage1.json`).
  Operator-adjudicated: also PROCEED (19 vs 20 of 21, or 18 vs 18 under the
  item-5 R6 rule).
- **Next:** approve or revise `stage2/PROPOSAL.md` (updated for items 4 and 5),
  and choose the held-out author. Stage 2 is not started. No model has been
  switched, and nothing is committed.

---

## Wrap-up: reusable workflow delivered; apsp-tdd-001 closed (2026-11-08)

**Operator decision:** stage 2 is not funded. There are no further model
trials, graders or paid case authoring. Full upstream content stays the
default. **No candidate is adopted.**

**The deliverable is `workflow/`** (start at `workflow/README.md`):

- `GUIDE.md`: the maintainer guide, with TDD Sonnet 5.5 as the worked example;
- `EVALUATION.md`: isolation, campaign, evidence, scoring, results format;
- `BETA.md` and `templates/beta-feedback.md`: the opt-in beta, its rollback,
  and controlled vs everyday evidence;
- `examples/tdd-sonnet-5-5/`: `IDENTITIES.json`, `CHANGE-MAP.md`, the AP config
  v3 consumer, `agents.rollback.yaml`, `trust.example.yaml`, `routing.json`,
  `campaign.example.json`, and `delivery-report.json` (`ok: true`);
- tools (stdlib, no model calls): `verify_delivery.py`, `check_package.py`,
  `preflight.py`, `campaign.py` and `results_format.py`, with
  `test_workflow_tools.py` (18 tests);
- `schemas/results.schema.json` (`apsp-results/1`).

**The experiment closeout:**

- `experiments/tdd-compaction/CLOSEOUT.md` and `README.md`.
- `stage1/RESULTS.md` now leads with the accepted interpretation:
  18/21 vs 18/21, all paired reps tied, under the R6 rule "ask, or a behavior
  test".
- `stage1/results.sanitized.json` is valid against the schema.
- `stage2/PROPOSAL.md` is marked NOT FUNDED.
- `packages/test-driven-development-sonnet-5-5/CLOSEOUT-STATUS.md` supersedes
  `STATUS.md`. Frozen files were left unedited, so FREEZE-1.2.0 still
  verifies.

**Verified locally on AP 0.19.4:**

- pins and digests;
- exact-model routing, with fallback for Haiku and Opus 5.5, the near-miss
  `claude-sonnet-5`, unlisted and unstated models;
- the exact delivered text;
- full resource export (`stamp` + `materialize filesystem-v1`) and
  `library read`;
- rollback.

**Gaps (documented, not implied):**

- the AP `CLAUDE.md` bootstrap route was not evaluated;
- AP does not detect the model;
- the `claude-plugin-v1` discovery adapter is unreleased;
- `writing-plans` and `writing-skills` are not packaged;
- AP issues #89, #90 and #91.

**Drafts for review (not posted or sent):**

- `reports/issue-88-update-2026-11-08-closeout.draft.md`;
- `reports/maintainer-summary.draft.md`.

**Open decisions:**

- the remote owner and visibility, and whether to commit and push;
- whether to offer the workflow to obra;
- Petrov's dataset terms;
- publishing sanitized results;
- closing #88, with follow-ups.

**Not pursued:** `apsp-sd-001` (prepared, never run, not re-reviewed).

### Published (2026-11-08)

- At the operator's direction, this companion is published as the public repo
  `guisam/agent-profiles-superpowers` (MIT for the project's own content;
  `private/` excluded).
- The skill-compaction preset is in Agent-Profiles PR #92 (0.19.7).
- The issue #88 update is posted from
  `reports/issue-88-update-2026-11-08-closeout.draft.md`, revised for
  publication.
- PR #92 merged into Agent-Profiles `main` (`8953285`) after all CI checks passed
  on macOS, Ubuntu and Windows. Wiki updated (0.19.7 entry and a companion link).
  No npm release or tag.
- The #88 update is posted:
  https://github.com/guisam/Agent-Profiles/issues/88#issuecomment-6730991902
  (text in `reports/issue-88-update-2026-11-08-closeout.md`). The issue stays
  open.
- Still open: whether to offer the workflow to obra
  (`reports/maintainer-summary.draft.md`, not sent); Petrov's dataset terms;
  closing #88 with follow-ups.
