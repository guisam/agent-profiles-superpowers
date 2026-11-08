# Trial protocol: brainstorming, claude-sonnet-5-5, full vs candidate

Frozen 2026-11-07 together with `cases.json` and `RUBRIC.md`, before any trial.
`FREEZE.sha256` records their hashes. A later edit to these files is a new
suite version and invalidates comparison with earlier results.

## Treatment

| Arm | Consumer | Sonnet selects | Everything else |
| --- | --- | --- | --- |
| `full` | `alpha` | `@apsp/brainstorming-upstream@7.0.2` | identical |
| `cand` | `beta` | `@apsp/brainstorming-sonnet-5-5@0.1.0` | identical |

Both consumers have byte-identical profile, role, adapter and AP runtime
(`@guisam/agent-profiles@0.19.4`) and share one disposable store. The only
difference is beta's `sonnet-candidate` assignment. The resolve output names the
selected package and its description; that label is visible to the model in both
arms. This is a known, unremoved difference.

Activation policy is the same in both arms: `brainstorming` is a required skill
of the `brainstormer` role, so its body is always delivered. Non-invocation cases
(C09, C10) test whether the model applies it when it should not. Changing that
policy would be a separate, declared treatment.

Not compared here: Haiku 5.5 (its initial candidate is the unchanged baseline, so
there is no pair to run), Opus/other models (not measured by the knowledge study),
native-plugin delivery (later, separate comparison).

Trust policy (operator decision, 2026-11-07): the machine policy
(`require_approval: true`, `commands` not allowed) withholds both packages. Both
arms therefore run resolve with `AGENT_PROFILES_TRUST=private/trust.trial.yaml`:
namespaces `@apsp/*`, effects `[commands]`, no approval. This applies only to the
two disposable consumers and their throwaway store. `~/.agent-profiles/trust.yaml`
is unchanged.

Pre-run amendment (before any trial, same suite version): AP's text resolve
output names no package. So (a) the adapter now gets the package for
`library read` from `--json`, and (b) the collector identifies the delivered
variant by the two deleted sentences, not by package name. A side effect: the
arm label is not visible in the model's context unless the child runs the
`--json` lookup.

Post-smoke amendments (collector only; the child prompt, adapter, cases and
rubric did not change, so the smoke pair counts as C04 r1):
(a) when a child returns its message instead of writing `reply.md`, the
collector copies the transcript's final text verbatim to `reply.recovered.md`
and records `reply_written=false` as a harness-compliance deviation, separate
from quality; (b) `prompt_exact` checks that the transcript's first user message
equals the rendered prompt; (c) `bundle`/`score` build blind grader bundles
(case `targets` stripped, shuffled opaque IDs, arm key kept apart).

## Fixed within each pair

Host Claude Code via the coordinator's native `Agent` tool, `model: sonnet`
(exact ID taken from the transcript, never assumed), same prompt template, same
tools and permissions, default effort, fresh context per run, fresh fixture copy
per run. The coordinator does not edit replies.

Known confound: the host session has a native Superpowers plugin enabled
globally, and no global plugin change is authorized. Children are told to use
only the AP-delivered text. Any `Skill` tool call in a child transcript marks
that run `invalid-setup`. It is retained, excluded from quality, and rerun once.

## IDs and order

`experiment = apsp-bs-001`. Run ID: `<experiment>.<case>.<arm>.r<rep>`.
IDs are written to `runs.jsonl` before dispatch. After return, the coordinator
appends the host-returned `agentId` and the transcript path. T3 thread or task
IDs and provider session IDs are not exposed for native `Agent` children; they
are recorded as `unknown`, never invented. The transcript `sessionId` field is
the parent Claude Code session, not a provider ID.

Order alternates: in repetition 1, odd cases run `full` first; in repetition 2,
even cases run `full` first. Runs execute one at a time.

## Phases

1. Smoke: C04 × {full, cand} × r1. It checks setup, resolve, export and grading
   end to end. Smoke runs count as pilot repetition 1 for C04 only if no setup
   change follows.
2. Pilot: all 11 cases × 2 arms × 2 repetitions (44 runs, including the smoke runs).

## Logging and export

Per run, at completion, `tools/collect.py` copies the child transcript JSONL to
`private/runs/<run-id>/transcript.jsonl` and records sha256. It extracts:
model IDs, per-message usage deduplicated by message ID (input, cache-write,
cache-read, output; thinking tokens are part of output and are not added again),
tool calls by name, turns, elapsed time from first to last timestamp, resolve
success and selected package, Skill tool use, and fixture changes. Fields the
transcript lacks are `null` (unknown), not zero.

The coordinator's own usage for dispatch and reporting, and the grader calls, are
recorded separately as overhead. They are not attributed to either arm.

Raw transcripts stay in `private/` (ignored). Public results contain only
aggregates, grades with short quoted spans, and hashes.

## Grading

Deterministic checks first. Then one held-out grader per case, a fresh `Agent`
with `model: opus`. It never sees arm labels and gets replies under shuffled
opaque IDs, with only RUBRIC.md, the case and the fixture. It did not
see the knowledge dataset or the candidate rationale. The grader and the
evaluated models are different. Its judgment is still model judgment, not ground truth.

## Decision rule

The candidate is adopted for `claude-sonnet-5-5` only if, in every case, its
must-pass count is not lower than the full arm's (pass count per case across
repetitions; any M failure counts) and no `invalid-setup` remains unresolved.
Otherwise the full content stays and the negative result is reported. Two
repetitions per case cannot establish non-inferiority; adoption means "no
observed must-pass regression in this pilot" and nothing stronger.
