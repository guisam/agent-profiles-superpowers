# `apsp-tdd-001`: test-driven-development compaction for Sonnet 5.5 (PROPOSAL, draft r1)

Status 2026-11-08: **preparation only, awaiting review.** No model trial has run.
Nothing is frozen, adopted, selected, published or filed. AP core, global
configuration and live selections are unchanged.

Earlier experiments are historical evidence only and are left unchanged:
`apsp-bs-001`, `apsp-bs-002` and the uncommitted `apsp-sd-001` preparation.
They inform harness design. They are never fresh confirmation for anything here.

| Artifact | Path |
| --- | --- |
| Immutable baseline | `packages/test-driven-development-upstream/7.0.2/` (AP `ce680b8a…`) |
| Unvalidated candidate | `packages/test-driven-development-sonnet-5-5/0.1.0/` (AP `bd446f96…`) |
| Change map, size | `packages/test-driven-development-sonnet-5-5/RATIONALE.md` |
| Contract, contradictions T1-T10, evidence mapping | `CONTRACT.md` |
| Screening cases | `CASES.draft.md` |

**Coordinator context disclosure:**

- This session received the Superpowers `using-superpowers` SessionStart text
  and graft hook text.
- No Ponytail text was present.
- The coordinator is Opus 5.5, not the target model.

## 1. Target selection

**Skill: `test-driven-development`. Model: `claude-sonnet-5-5` (Sonnet 5.5),
subscription Claude Code 2.1.319 on Windows 11.**

| | **test-driven-development** | systematic-debugging | receiving-code-review |
| --- | --- | --- | --- |
| Sonnet known, strict (lenient) | 0.80 (0.96), n=24 | 0.88 (0.96), n=25 | 0.68 (0.96), n=25 |
| Sonnet strict-added atoms | 4, all in text this candidate keeps | 3 | 8 |
| Removable execution explanation | **High:** 3 worked code examples and a diagram that restates the steps (≈ 27% of `SKILL.md`) | Moderate (prior attempt: −14.8%) | Low: mostly phrasing and stance rules |
| Testable contract | **Objective:** tool-event order (test → failing run → production edit), mutation check, signature check, full-suite run | Objective | Partly (phrasing) |
| Dependencies | 1 resource (unchanged), no scripts | 5 resources, 2 cross-skill names | none |
| Already prepared here | no | yes (`apsp-sd-001`, prepared with Ponytail in the coordinator's context; preserved, not reused) | no |

Why TDD:

- The removable bulk is *examples and a diagram* (execution explanation), not
  reminders.
- Every Sonnet strict-added atom sits in retained text.
- Its contract is the most mechanically checkable of the three.
- A fresh target also gives evidence independent of the tainted `apsp-sd-001`
  preparation.

The earlier objection to TDD (`apsp-sd-001` §1) was re-examined:

- **"Its bulk is rebuttal text, which upstream showed matters."** True. This
  candidate keeps every rebuttal, red flag and checklist item verbatim. The
  reduction comes from elsewhere.
- **"Ponytail opposes it."** Ponytail was uninstalled at user scope on
  2026-11-08.

Brainstorming was not reconsidered.

Why this exact model:

- Petrov's data covers only Haiku 5.5 and Sonnet 5.5 on Bedrock. Sonnet has the
  higher strict-known share.
- **No substitution:**
  - Quorum's `sonnet5` credential is `claude-sonnet-5`, a different model, and
    is not used.
  - Opus and Haiku get no candidate.
- **Evidence transfer is qualified.** The probes ran on Bedrock
  `us.anthropic.claude-sonnet-5-5` with no Claude Code system prompt or tools,
  and were self-judged. That is knowledge-probe-only evidence from another
  deployment. Only this trial would test it in subscription Claude Code.

## 2. Evaluator choice (integrations inspected 2026-11-08)

| Option | Finding | Verdict |
| --- | --- | --- |
| **This repo's harness `collect_v2.py` 2.1.0** (+23 tests) | Opaque tokens, per-case fixtures, delivery check by body, two-grader scoring, enforced limits, append-only ledger. It collects from Agent-tool subagent transcripts, which cannot be isolated (§3), and has the four defects in §8. | **Selected, with a bounded 2.2.0 revision** (§8). The same revision also serves `apsp-sd-001`; it is not a general runner. |
| `superpowers-evals` / quorum, branch with AP per-model plugin arms (`238287f6`, 2026-10-30) | The best fit in principle: a throwaway `$HOME` per run, native Skill discovery through an AP-materialized `claude-plugin-v1`, and existing TDD scenarios (triggering, tests-later pressure, user-pref non-activation), plus a Gauntlet driver for multi-turn. **Not runnable here without new setup:** Gauntlet is not installed; the Docker daemon is not running; there is no credential for `claude-sonnet-5-5` (`sonnet5` = `claude-sonnet-5`, API key); the Windows Claude path requires `ANTHROPIC_API_KEY` on a VM; and finite campaign comparisons require the maintainer's Linux appliance. Its TDD scenarios grade only *load order* (§CONTRACT, behavioral evidence), and reuse the email example. | Not selected for this stage. The **AP `materialize --adapter claude-plugin-v1` route it proved** is reused for the D-block (§4). Option for confirmation if the operator provisions it (Q7). |
| AP `migrate plan/results/report` | Records paired evidence offline; does not execute. | Optional record of results (Q8). |
| AP preset `skill-compaction/evals` (`cases.json`) | Evaluates the compaction *skill*, not a compacted skill. | Not applicable. |
| Upstream `tests/claude-code/*`, `tests/explicit-skill-requests` | Native plugin delivery, explicit invocation, no paired arms. | Not applicable. The `claude -p` launch pattern is reused. |

## 3. Host audit and isolation (read-only; global configuration not changed)

| Source | What a child would receive | Relevance |
| --- | --- | --- |
| Account-synced plugin (claude.ai sync) `~/.claude/plugins/synced/…/skills/test-driven-development/SKILL.md` | A native `superpowers:test-driven-development` whose **blob is `46838cc9`, byte-identical to the baseline**, plus `using-superpowers` and the other synced skills | **Critical:** a candidate-arm child could load the full text via the Skill tool. It must be absent from every analyzed run. |
| Account-synced `engineering:*` skills (`testing-strategy`, `debug`, …) | Competing testing guidance | Competitor |
| `~/.claude/settings.json` hooks | SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd (graft) | Competing instructions |
| `enabledPlugins` | `cc-plugin-you-should-know@builtin` (a built-in, which `--safe-mode` keeps enabled) | Unknown content; recorded in `init` |
| `~/.claude/skills/` | `trail` ("Use for ANY task"), `find-skills`, `documentation-writer` | Noise |
| `~/.claude/CLAUDE.md` | absent | none |
| Ponytail | uninstalled 2026-11-08; every transcript is scanned for "ponytail" anyway (HANDOFF rule: stop and report on a hit) | Guard |
| This session's environment | `CLAUDECODE`, `CLAUDE_AGENT_SDK_VERSION`, `CLAUDE_CODE_{CHILD_SESSION,ENTRYPOINT,EXECPATH,MESSAGING_SOCKET,MESSAGING_TOKEN,SESSION_ATTENDED,SESSION_ID}`, `CLAUDE_EFFORT`, `CLAUDE_PID`, `T3CODE_CLI_PATH`, `T3CODE_THREAD_ID` | Would leak into a child process; scrubbed |

Child launch: one process per run, with cwd set to the run's project copy.
`<scrubbed env>` unsets every variable in the last row of the table above.

```sh
env <scrubbed env> claude -p --model claude-sonnet-5-5 --effort medium \
  --safe-mode --strict-mcp-config --no-chrome \
  [R-block] --disable-slash-commands --append-system-prompt-file <run>/context.md
  [D-block] --plugin-dir <run>/plugin \
  --tools "Bash,Read,Edit,Write,Glob,Grep" [D-block adds: Skill] \
  --permission-mode bypassPermissions --session-id <uuid> \
  --max-budget-usd 1.25 --output-format stream-json --verbose --include-hook-events \
  "<case user message>"
```

**Isolation acceptance**, checked on every run's `init` event and fatal at smoke:

- model `claude-sonnet-5-5`;
- exactly the listed tools;
- no MCP servers;
- no hook events;
- R-block: no skills or slash commands at all;
- D-block: exactly one non-built-in skill, the AP plugin's `test-driven-development`;
- no "ponytail" anywhere in the run.

What remains unknown (from `claude --help` text only):

- `--safe-mode` disables "installed plugins", but documents "built-in … plugins"
  as kept. Whether **account-synced** plugins survive is unknown.
- Whether `--plugin-dir` works under `--safe-mode` is unknown.
- `--append-system-prompt-file` appears only in `--bare`'s help.
- `--max-budget-usd` under subscription auth is unverified.
- `--bare` is unusable, because it requires `ANTHROPIC_API_KEY`.

**If isolation fails:**

- If synced plugins survive in the R-block (even with `--disable-slash-commands`),
  stop. Report the observed `init`.
- If the D-block cannot list the AP plugin alone, the D-block is **not run**.
  Discovery is then reported as unqualified. The alternative is a throwaway
  `CLAUDE_CONFIG_DIR` with a `claude setup-token` OAuth token, the quorum
  pattern, which needs the operator (Q3).

`bypassPermissions` runs model-chosen commands on this Windows host without a
sandbox. The disposable `%TEMP%\apsp-tdd\<token>\` copies and the six-tool list
are identical across arms. **This needs operator approval** (Q2).

## 4. Delivery route and arms (AP selects; both arms use the same route)

**Consumers:**

- Two disposable AP 0.19.4 config-v3 consumers under `private/consumers/tdd-*`,
  each with one role (`implementer`).
- `tdd-full` binds the baseline.
- `tdd-cand` binds the baseline by default, plus the assignment
  `{model: claude-sonnet-5-5, role: implementer}` → candidate.
- `resolve` verifies routing: Sonnet 5.5 → candidate; Haiku, Opus and an
  unknown model → baseline.

**Blinding:**

- The private trial store republishes both packages under opaque aliases
  (`@apsp-trial/t-k1`, `t-k2`). Their bytes are identical to the canonical
  packages, checked by file hash.
- Aliases carry a neutral description. The key stays in `private/`.
- No path, prompt, tool output or file name visible to a child carries an arm or
  case label.

**R-block, required delivery.**

- Each arm's context comes from `resolve --host claude --identity-source
  host-stated --model claude-sonnet-5-5 --role implementer` with the
  trial-scoped trust policy.
- It is frozen once as `context-<arm>.md` with its sha256. The arm's `SKILL.md`
  body must be contained in it.
- Every run of an arm receives the identical file.
- `../skill/writing-good-tests.md` is byte-identical in both arms. The adapter
  text, identical and frozen, says that supporting files are in `../skill/` and
  that other `superpowers:*` skills are unavailable.

**D-block, discovery delivery.**

- AP `stamp` + `materialize --adapter claude-plugin-v1`, exactly as in the
  superpowers-evals build script, produces one plugin per arm. Each holds only
  `test-driven-development`.
- The plugin name is `superpowers`, so the address stays
  `superpowers:test-driven-development`, but only if smoke proves the synced
  plugin is absent. Otherwise the D-block does not run.
- Manifests are identical except for the skill body (checked).
- There is no `using-superpowers` bootstrap in either arm.

**Qualification:**

- R-block results qualify only "AP-resolved, required, appended to the Claude
  Code system prompt, safe-mode headless host".
- D-block results qualify only "AP-materialized claude-plugin-v1 with this skill
  alone, no Superpowers bootstrap, safe-mode headless host".
- Neither qualifies native Superpowers delivery, the AP CLAUDE.md bootstrap, MCP,
  other models or Bedrock.

**Size through the route:** stage 0 records AP `proof` bytes for both consumers
and the delivered plugin `SKILL.md` bytes.

## 5. Staged plan (exact counts; serial dispatch, one process at a time)

### Stage 0: setup smoke (never analyzed)

- **Child runs: 4.** R1 × 2 arms and D1 × 2 arms, rep 0. **Setup retries ≤ 2.**
- **Grader runs: 1** (an R1 smoke bundle with 2 packets), plus ≤ 1 re-run for
  invalid output only.
- **Pass requires all of:**
  - isolation acceptance (§3);
  - context and plugin sha match;
  - stream and transcript collected;
  - every R1 checker returns a verdict;
  - the grader file validates and its provenance verifies;
  - `proof` recorded;
  - the `--max-budget-usd` behavior observed.
- **On failure:** fix setup, record an amendment *before* freeze, and repeat smoke
  once. A second failure stops the experiment.
- If only the D-block fails isolation, stage 1 runs the R-block alone, and the
  D-block is reported unqualified.

### Stage 1: screening

- **R-block:** 7 cases (R1-R6, N1) × 2 arms × **3 reps = 42**.
- **D-block:** 2 cases (D1, D2) × 2 arms × **3 reps = 12**. Reported separately.
- **Order:**
  - rep 1 → 3, cases in a seeded, frozen shuffled order;
  - arm order alternates within each (case, rep): odd reps full first, even
    reps candidate first;
  - a fresh process and a fresh fixture copy per run.
- **No continuations:** every case is one user message, with no `--resume`. A
  run that ends with a question is final behavior and is graded as such.
- **Retries:**
  - **≤ 5 total, ≤ 1 per slot.**
  - Retry only for collector-computed setup invalidity: `init` mismatch, a
    context/plugin sha mismatch, missing stream or transcript, a crash or
    host/usage-limit error at any point, or a path access into this repository.
  - Never retried: budget-cap hits, wrong behavior, questions, refusals or
    timeouts that end with model output.
- **Rate limits:**
  - On a usage-limit or 429 signal, stop dispatching and record the event.
  - Wait for the reset; never buy capacity.
  - Resume from the ledger with identical frozen settings.
  - The interrupted run uses its slot's single retry. If none is left, the slot
    stays missing.
- **Graders:**
  - Gr1 (report claims vs transcript) is graded on R1-R4: 4 bundles × 2 blind
    graders = **8**.
  - Plus ≤ 2 re-runs, for invalid output only, never for disagreement.
- **Stage 0+1 maxima:**
  - **child runs:** 4 + 2 + 54 + 5 = **65**;
  - **grader runs:** 2 + 10 = **12**.

### Stage 2: confirmation (only after stage 1 = PROCEED and separate approval)

- **H-block, held-out, required delivery:** 4 new cases × 2 arms × 3 reps =
  **24**.
  - Authored after the candidate freeze by the operator, or by a fresh agent
    given only CONTRACT.md, the baseline `SKILL.md` and the case format. Neither
    may see CASES.draft.md, stage-1 results or RATIONALE.md.
  - Must cover the CASES.draft "not covered" list (at least refactor-only,
    characterization and multi-cycle) and every stage-1 watch item.
- **D-block, held-out:** 2 new cases × 2 × 3 = **12** (only if D-isolation
  passed).
- **Retries ≤ 4. Graders:** 4 × 2 = 8 + ≤ 2.
- **Maxima:** 40 child runs, 10 grader runs.

### Stop conditions (any stage)

- **Operator-review stop:**
  - a candidate-arm approval violation (R5 M1, R6 M1) or out-of-scope file
    change;
  - any destructive command outside the run directory;
  - any child access to evaluator files;
  - any "ponytail" hit.
- **Hard stop:**
  - any child, grader or retry limit reached;
  - budget-cap hits on more than 25% of a stage's runs, which means the
    settings are wrong;
  - unmet isolation acceptance.
- **No mid-stage change.** Any change is a numbered amendment. A post-execution
  amendment keeps the original procedural outcome next to any corrected one.

## 6. Acceptance criteria (frozen before any run)

Report these separately and never combine them into one score:

- (a) instruction size (deterministic; RATIONALE);
- (b) task success: the M criteria;
- (c) constraint compliance: test-first order, RED observed, full suite,
  approval and scope criteria;
- (d) user-facing friction: question-only replies, tool calls, turns,
  wall-clock time;
- (e) total usage: input, cache-creation, cache-read and output tokens, plus the
  CLI-reported cost, for child, grader and coordinator.

**A smaller file alone is not success.**

**Stage-1 outcome, per block, computed by `decide` and then human audit.**
Precedence runs from the first rule below to the last.

1. **VOID** if setup-invalid runs exceed 10% of slots.
2. **INCONCLUSIVE** if any slot lacks exactly one valid run, or if audits are
   pending.
   - Denominators are fixed at 3 per case per arm.
   - Missing slots are listed, never dropped.
3. **STOP-REGRESSION** on any of:
   - a candidate-arm approval violation (R5/R6 M1) not matched by a control
     violation in the same case, after audit;
   - any case where the candidate's all-M count is ≥ 2 below control;
   - a pooled R-block all-M total ≥ 2 below control.
4. **STOP-FRICTION** on either of:
   - pooled median tool calls per run above 1.25 × control;
   - more question-only replies than control in R1-R4, N1 or D1.
5. **PROCEED** to request stage-2 approval if none of the above hold.
   - Every case with a 1-run all-M drop becomes a **watch item**.
   - So does any S1 drop in R4 (the mock watch), or any decline in RED observed.

**Usage:**

- Pooled child tokens are reported per arm, with the range.
- If the candidate's total exceeds control by more than 10%, PROCEED becomes
  INCONCLUSIVE: a smaller entrypoint that causes more exploration is not a
  saving.

**Floor and ceiling:**

- A case where control scores 0/3 all-M is uninformative.
- 3/3 in both arms is recorded as "no regression observed", not as a benefit.

**Adoption recommendation, after stage 2 (still not an adoption):**

- all of the above hold on the H-block;
- no candidate-only approval violation at any stage;
- the D-block is reported, or discovery is explicitly listed as unqualified;
- a human decision.

The claim would be limited to "no regression observed in N tested cases for
Sonnet 5.5 in the stated environment".

## 7. Grading and human audit

**Objective first.** Checkers are hidden from children and run before any grader
is dispatched. Their results go into `result.json`. They compute:

- tool-event order;
- test-run exit codes and failure kinds;
- the mutation check and hidden tests (on a copy of the final tree);
- the signature check;
- the changed-file set;
- question detection (heuristic: final text ends with "?" and no files changed;
  every hit is human-audited).

**Graders (Gr1 only).**

- Two independent blind `claude-opus-5-5` graders per bundle.
- Same isolated launch, `--tools "Read,Write"`, cwd = the bundle directory.
- Each packet holds the case message, the final reply and a tool-event summary
  with commands and exit codes. Arm labels, tokens and objective verdicts are
  excluded.
- A criterion passes only if both graders pass it.

**Human audit (the operator), mandatory before `decide`:**

- every candidate-arm M failure;
- every R5/R6 M1 outcome in both arms;
- every question-detector hit;
- every grader disagreement;
- every checker error;
- all rep-1 runs (18).

Original and adjudicated grades are stored separately. The official outcome
uses the original rule, with any adjudicated outcome reported next to it.
Audit time is recorded.

## 8. Harness review: the four known failure modes

The 2.1.0 behaviors below were verified by reading the code on 2026-11-08. The
2.2.0 changes are **not implemented**; they need review, then tests, before
freeze.

| Failure mode | 2.1.0 behavior (by code) | 2.2.0 change |
| --- | --- | --- |
| Prompt renders counted as model attempts | `grader_prompt()` appends a `grader` ledger event when it renders the prompt, and the grader limit counts those events. `prepare()` appends `planned` and counts it toward `child_runs` even if never dispatched. An undispatched slot can never be retried (`result is None` → `LimitError`). | Pure render. A separate `dispatch` event is written immediately before the process spawns (session ID, argv hash). Limits count dispatches only; undispatched plans are voidable. |
| Legitimate identical grades read as copying | `score()` raises if the two grade files are byte-identical (the bs-002 INCONCLUSIVE). | Remove the byte check. Provenance check: each file must hash-match the Write in its own recorded grader session, the sessions must differ, and neither transcript may read the other's output. Identical bytes are allowed. |
| Incomplete pairs silently changing denominators | `decide()` already reports missing slots. But `bundle_runs()` bundles only valid runs, with no count check. | `bundle` refuses unless all 6 slots are valid. Every report prints fixed denominators and the missing list. |
| Retries chasing favorable results | A retry needs a collected invalid run, one per slot. But `collect(token, agent_id)` takes whichever agent ID the coordinator supplies. | Collect is bound to the session ID recorded at dispatch. Retry eligibility comes only from collector-computed setup fields (§5). One valid run per slot; the ledger stays append-only. |

Other bounded 2.2.0 additions, each with a test:

- the `claude -p` launcher with the frozen flags and environment scrub;
- stream-json collection;
- `init` isolation checks and the ponytail scan;
- per-case checker hooks (Python/Node, run on copies);
- extended `result.json` (tool order, test runs, questions, termination reason,
  usage, `total_cost_usd`);
- the §6 `decide`.

The 23 existing tests must still pass. The brainstorming artifacts stay on 2.1.0.

## 9. Budget (estimates; not billing; actual use is subscription allowance)

**Rates:**

- Sonnet 5.5 at $2 / $10 / $0.20 (cache read) per MTok, and Opus 5.5 at $4 /
  $20 / $0.20.
- These are the list rates cached 2026-10-06 and used in the earlier proposals.
  **Not re-verified for this proposal.**

| Item | Runs (max) | Per-run estimate | Estimate | Hard ceiling |
| --- | --- | --- | --- | --- |
| Stage 0+1 children (Sonnet 5.5) | 65 | ≈ $0.45 (assumed $0.20-1.00; multi-step coding runs) | ≈ $29 | $81 (65 × `--max-budget-usd 1.25`, if honored) |
| Stage 0+1 graders (Opus 5.5) | 12 | ≈ $0.40 | ≈ $5 | $12 (cap $1.00 each) |
| Coordinator (Opus): harness 2.2 + tests, 9 fixtures + checkers + reference solutions, consumers/aliases/plugins, dispatch, collection, audit support | n/a | measured from its own transcript for the window | ≈ $15-25 | none enforceable; reported |
| **Stage 0+1 total** | | | **≈ $50 (range ≈ $35-100)** | children + graders ≤ $93 |
| Stage 2 (if approved) | 40 child, 10 grader | same | ≈ $18 + $4 + coordinator ≈ $10 | $50 + $10 |

Usage is summed across children, retries, graders and coordinator from the
stream `result` events and transcripts. Thinking is counted within output.
Missing usage is unknown, never zero. Elapsed time, turns, tool calls and
throttling are recorded.

## 10. Questions that block execution

1. **Spend:** approve stage 0, then stage 1, separately (≈ $50 API-equivalent
   estimate; subscription allowance only).
2. **Permission mode:** approve `bypassPermissions` with six tools (seven in the
   D-block) in `%TEMP%` copies, with no sandbox on Windows. The alternative is
   an allowlist, which adds equal denial friction to both arms.
3. **Isolation fallback:** if synced plugins or `--plugin-dir` behave badly under
   `--safe-mode`, choose one:
   - (a) drop the D-block;
   - (b) mint a `claude setup-token` for a throwaway `CLAUDE_CONFIG_DIR` (the
     secret is supplied by the operator);
   - (c) run R only.
   For the R-block, a synced-plugin leak means stop.
4. **Human auditor:** who audits, and when. Stage-1 `decide` is blocked until
   the audit is done.
5. **Trial trust policy:** reaffirm the trial-scoped `AGENT_PROFILES_TRUST`
   (`commands` effect) for the disposable consumers. The home policy stays
   unchanged.
6. **Contract readings:** confirm the grading interpretations of T8 (R5:
   "asks before skipping" passes), the R6 exception rule and T4 (R2: report
   the unrelated failure, fixing it not graded). If they are judged wrong,
   revise the cases before freeze. Do not change the candidate.
7. *(Non-blocking)* Whether quorum should be provisioned for stage 2 discovery
   (Gauntlet install, Docker or Linux runtime, a `claude-sonnet-5-5` OAuth
   credential, the Gauntlet-Agent's extra model usage).
8. *(Non-blocking)* Whether to record results via AP `migrate plan/results`.
9. *(Non-blocking)* Ordering with `apsp-sd-001`. Both await review and share the
   harness 2.2.0 work; run one stage 0 at a time.

### 10.1 Operator decisions (2026-11-08)

| Q | Decision |
| --- | --- |
| Q1 Spend | Stage 0 **and** stage 1 approved, with the ≈ $50 estimate (range $35-100) on subscription allowance. Stage 1 starts only if stage 0 meets its acceptance checks (§5); otherwise stop and report. Stage 2 is not approved. |
| Q2 Permissions | `bypassPermissions` approved, with the six-tool list (seven in the D-block) in disposable `%TEMP%` copies. |
| Q3 Isolation fallback | (a) If isolation fails only for the D-block, drop the D-block and report discovery as unqualified. An R-block leak still means stop. |
| Q4 Human audit | The operator audits after stage-1 grading, from an audit packet the coordinator prepares (transcripts, grades, checker output). `decide` waits for the audit. |
| Q5 Trust | The trial-scoped `AGENT_PROFILES_TRUST` (`commands`) policy in `private/` is reaffirmed. The home policy is unchanged. |
| Q6a R5 | Confirmed: asking before any production edit passes (T8). |
| Q6b R6 | Confirmed: asking first, or a failing test that reads the setting, passes. |
| Q6c R2 | **Changed:** the pre-existing `dates` failure is not graded at all, neither fixing nor reporting it. R2's M6 is removed in CASES.draft and CONTRACT. The fixture keeps the failing test. |

Non-blocking questions Q7-Q9: no decision recorded.

## 11. Pre-freeze work (after approval, before any model call)

1. Implement harness 2.2.0 and its tests (§8).
2. Build the 9 fixtures, with deterministic setup and hidden checkers. Validate
   each checker against hand-written good and bad reference solutions, with no
   model.
3. Create consumers, aliases, contexts, D-block plugins and `proof`.
4. Write RUBRIC.md (Gr1), GRADER-PROMPT.md and run-config.json (limits, seed,
   decision rule). Freeze with `FREEZE-1.0.0.sha256`.
5. Run stage 0 smoke.
