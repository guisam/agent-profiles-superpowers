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
