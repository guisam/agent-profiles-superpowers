# Evaluating a variant: isolation, campaign, evidence, scoring, results

This is the bounded comparison method behind [GUIDE.md](GUIDE.md). It has
three separable layers, so maintainers can swap in their own runner and
credentials:

| Layer | Owns | What this repo provides |
| --- | --- | --- |
| **Selection and delivery** (AP) | Which package a model gets, and the exact text and resources delivered | `consumer/.agent-profiles/agents.yaml` examples; `tools/verify_delivery.py` |
| **Execution** (your runner) | Launching the model with fixed settings, one fresh process and fixture copy per slot | `tools/campaign.py plan` (the schedule); `tools/preflight.py` (isolation); a reference Claude Code launcher in `experiments/tdd-compaction/tools/tdd_harness.py` |
| **Evaluation** | Evidence capture, deterministic checks, blind grading, the decision | the checkers, harness and audit tools in `experiments/tdd-compaction/tools/`; `schemas/results.schema.json`; `tools/results_format.py` |

## 1. Freeze before running

Fix all of the following, then hash every file into a `FREEZE-x.y.z.sha256`
manifest:

- the cases (one user message each);
- the fixtures, with hidden checks;
- the rubric;
- reps per arm;
- the order seed;
- limits (runs, retries, per-run budget caps);
- pause rules;
- the decision rule.

After the first dispatch, only numbered amendments are allowed. Any scoring
change made after the fact is reported **beside** the official result, never
in its place.

Fixture rules learned from `apsp-tdd-001`:

- **Map every hidden assertion to a clause of the request.** Give each fixture
  a good, a bad, and an **alternative-valid** reference solution that must
  pass. An alternative-valid solution would have caught the R3 tuple defect.
- **Avoid pre-existing failures that make "the suite passes" impossible,**
  unless that is the point of the case.
- **Pre-declare how contradictory source rules are scored,** for example the
  "no exceptions" vs "ask your partner" readings. The pre-run contract review
  should list these contradictions.

## 2. Isolation preflight (every arm, before any run)

Run `tools/preflight.py` on a prepared run directory:

```sh
python -I workflow/tools/preflight.py --run-dir RUN/project --context RUN/context.md \
  --arm-skill packages/<arm>/SKILL.md --other-skill packages/<other arm>/SKILL.md \
  --skill-name test-driven-development --forbid "$PWD" \
  --probe --model claude-sonnet-5-5 \
  --claude-flag=--safe-mode --claude-flag=--strict-mcp-config --claude-flag=--no-chrome \
  --claude-flag=--disable-slash-commands --claude-flag=--permission-mode --claude-flag=bypassPermissions
```

It checks:

- **Global instructions:** `CLAUDE.md` and `AGENTS.md` in the user config, or
  above the run directory.
- **Hooks:** in user or project settings.
- **Duplicate skill installations:** user skills, plugin caches and synced
  plugins, project `.claude/skills`, and `~/.agents/skills`. A duplicate is
  matched by frontmatter name, or by content hash of either arm.
- **Arm access:**
  - the delivered context contains this arm's `SKILL.md` exactly, and not the
    other arm's;
  - no file in the run directory contains the other arm's text;
  - the run directory is outside the repository that holds both arms.
- **Environment variables** that would leak host session state. The launcher
  must scrub them.
- **The `init` probe:** it launches the exact child command and stops it at the
  `init` event, before any assistant output. It then checks the model, tools,
  MCP servers, listed skills, slash commands, non-built-in plugins, hook
  events, and deny-listed terms (default: `ponytail`).

**Static findings must be neutralized by launch flags *and* confirmed by the
probe.** For example, the graft hooks on this machine are present but
disabled by `--safe-mode`, and the probe confirms that no hook events occur.

**Other hosts:** pass your host's session description with `--init-json`, or
run the static checks only and record that limitation.

**What the preflight does not cover:**

- the content of built-in host plugins (5 on Claude Code 2.1.319, listing no
  skills);
- provider-side behavior;
- anything the host loads after `init`.

Re-check `init` on every run, not just once.

## 3. Campaign

`tools/campaign.py check|plan <campaign.json>` validates a campaign
definition and prints the slot schedule. See
`examples/tdd-sonnet-5-5/campaign.example.json`.

- **One campaign is one configuration:** exact model ID, host and version, AP
  version, both arms' digests, delivery route, launch flags, effort and tools.
  Changing any of these makes a different campaign.
- **Order is balanced:**
  - seeded case order per rep;
  - arms run back to back within a case-rep;
  - each case runs full-first and candidate-first equally (for an even rep
    count).
- **One fresh process and one fresh fixture copy per slot.** Single turn; a
  run that ends with a question is final.

**Repetitions.** Three per arm is screening. At a pass rate near 0.85, the
95% interval on the pooled difference is:

| Behavioral cases | Reps per arm | Interval |
| --- | --- | --- |
| 7 | 3 | about ±20 points |
| 8 | 12 | about ±10 points |

The held-out design in `experiments/tdd-compaction/stage2/PROPOSAL.md` (12
reps, −15-point non-inferiority margin) is the template for a confirmation
campaign.

**Retries and pauses:**

- **Retry** only for collector-computed setup faults (`init` mismatch, missing
  stream or transcript, crash, host or usage-limit error, repository access).
  At most once per slot, with a total cap.
- **Never retry** wrong behavior, questions, budget-cap hits, or timeouts that
  ended with model output.
- **Pause** on: a deny-listed term or an unexpected skill, plugin or hook; any
  repository access; an *unmatched* approval failure (the candidate fails more
  than control in the same case).

## 4. Evidence to collect per run

Collect all of the following, hashed and kept private:

- the stream (`stream-json`), including the `init` event;
- the full transcript;
- the final tree diff;
- the hidden-test output;
- usage by category: input, cache creation, cache read, output. Missing usage
  is recorded as missing, never zero;
- the reported cost;
- wall time.

**Lessons from `apsp-tdd-001`:**

- **Agents pipe test output through `grep` and `tail`.** Read the outcome from
  the runner's own summary and per-test markers. If neither is present, record
  `unknown`, which is never counted as a pass or a fail and is always audited.
- **Agents edit files through shell heredocs.** Classify writes per command
  segment, and audit shell writes.
- **Give graders full test output** (head and tail, with an explicit elision
  marker) plus exit status. A 12-line tail produced 3 false Gr1 failures.
- **RED must be attributable to the new test.** Use the run output, or an
  offline replay of the test files against the original code
  (`audit_red_replay.py`).

## 5. Scoring

1. **Deterministic checkers first.** These cover test-first order, an
   attributable RED, the mutation check (bug fixes), hidden tests, the full
   suite after the last change, scope, and approval.
2. **Blind graders only where nothing deterministic exists**, for example
   whether claims in the final message match the evidence.
   - Use two graders per bundle, with opaque packet IDs and shuffled arms.
   - Establish independence from execution provenance: separate sessions; each
     grade file equals its own session's Write; neither session read the
     other's output. Never use byte inequality as the test.
   - A criterion passes only if both graders pass it. Every disagreement goes
     to the human audit.
3. **Human audit before the decision.** Cover at least every candidate
   failure, every approval-case outcome, every grader disagreement, every
   `unknown`, and every rep-1 run.
   - Proposed corrections are recorded with the original score, the evidence
     location, the reason, and the cause: agent, capture, rubric or fixture.
   - Apply the same standard to both arms, and check passes as well as
     failures.
   - The tools are `audit_dump.py`, `audit_symmetry.py`,
     `audit_red_replay.py`, `audit_adjudicate.py` and `audit_usage.py`, in
     `experiments/tdd-compaction/tools/`.
4. **The decision.** Apply the frozen rule to the official scores, and report
   the accepted (adjudicated) interpretation as the headline once the gate
   closes.
   - Report instruction size, task success, constraint compliance, friction
     (tool calls, question-only replies) and total usage separately.
   - A smaller file is never success on its own.

## 6. Results format

Shared results use `schemas/results.schema.json` (`apsp-results/1`):

- one file per configuration;
- for each run: `official` and `accepted` criteria, Gr1, tool calls, usage
  by category, and reported cost;
- the campaign's amendments and freeze hash;
- the configuration block;
- the arm identities, including the delivered-context hash.

`tools/results_format.py validate <file>` enforces the structure. It refuses
files that contain:

- file paths;
- UUIDs (session or account IDs);
- email addresses;
- credentials;
- long free text, which suggests a transcript or final message.

Worked example:
[`experiments/tdd-compaction/stage1/results.sanitized.json`](../experiments/tdd-compaction/stage1/results.sanitized.json),
produced by `experiments/tdd-compaction/tools/export_sanitized.py`.

**Never pool results across configurations.** A headline number belongs to
exactly one model × host version × AP version × arm digests × delivery route
× flags × effort.
