# Per-model skill variants without a plugin: a summary for skill maintainers

A short overview for maintainers of [Superpowers](https://github.com/obra/superpowers) and similar skill
sets. The full walkthrough is the [maintainer guide](workflow/GUIDE.md).

## The idea

Some Superpowers skills carry teaching that a strong model may not need, such
as worked code examples and diagrams that restate the steps. Every model still
needs the decision guidance: triggers, order, exceptions, approval boundaries
and verification.

This workflow lets a maintainer offer a **per-model variant** as an
**opt-in**:

- it is selected by the exact model ID;
- the full upstream skill stays the default for everyone else;
- it is delivered by Agent Profiles, so users never install a plugin;
- it is evaluated in a bounded, paired way before anyone calls it better, or
  even equivalent.

## What we tried

**The candidate:** a compacted `test-driven-development` for Sonnet 5.5,
made with Agent Profiles' contract-preserving
[skill-compaction preset](https://github.com/guisam/Agent-Profiles/tree/main/examples/presets/skill-compaction).
The [change map](workflow/examples/tdd-sonnet-5-5/CHANGE-MAP.md) ties each
edit to the requirement it preserves.

- The diagram and three worked examples were removed, taking `SKILL.md` from
  9.6 KB to 7.0 KB.
- Every rule, rationalization row, red flag and checklist item was kept, as
  were the resources.

**The evaluation:** 7 screening tasks × 2 arms × 3 runs, with isolation
checked on every run. The tasks were a feature, a bug fix, minimal code, real
vs mock, pressure to skip tests, a configuration change, and a prose-only
edit.

**What we found:**

- No observed regression in that screening suite: 18/21 vs 18/21, with every
  paired run tied under the accepted rules.
- 9% fewer total tokens per task. That comes mostly from the smaller prompt
  being re-read on every request.
- On identical text, **neither** variant asked before treating a
  configuration-file edit as an exception, as the skill says to.

**What we did not establish:** equivalence, held-out performance, or discovery
through a plugin. The candidate is **not adopted**. The held-out confirmation
was designed but not run. Full record:
[closeout](experiments/tdd-compaction/CLOSEOUT.md) and
[stage-1 results](experiments/tdd-compaction/stage1/RESULTS.md).

## Then a second model: Opus 5.5

We built a separate Opus 5.5 candidate, contract-first from the upstream text.

- **Size:** `SKILL.md` goes from 9.6 KB to 6.9 KB.
- **Contract:** every one of the 31 requirements we extracted is still
  present.
- **Smoke test:** 5 small development tasks × 2 versions × 2 runs, isolated,
  for about $1.30 in model usage.

**What we found:**

- **No failures unique to the candidate,** and every pair of runs had the same
  outcome under the accepted scoring.
- **The same two behaviors as Sonnet, in both versions:**
  - Opus followed a user's "just run this test file" over the skill's
    full-suite rule, and said so.
  - It didn't ask before changing a configuration file.
- **Tokens were essentially equal** (+0.7% for the candidate). Most of that
  came from one task, where the candidate wrote a quick test before flipping a
  config value and the baseline didn't. Those were value-only tests, so they
  didn't count as more correct work.

This is development evidence from 2 runs per case, not validation.

## What this shows about Agent Profiles

One configuration now serves one skill three ways:

- `claude-sonnet-5-5` gets its compacted variant.
- `claude-opus-5-5` gets a different compacted variant.
- **Every other model** gets the full upstream skill. That includes Haiku, a
  near-miss ID like `claude-opus-5`, and agents that don't state their model.

No plugin is installed. We verified before each run which text each model
received, and that switching back is a one-block edit. A plugin has to ship one
version for everyone; per-model tuning needs something that picks the version
for each agent, and that's what Agent Profiles does.

## What a maintainer would do

1. **Keep the upstream skill as an immutable baseline package,** made from the
   exact git bytes.
2. **Publish a candidate as a separate, versioned package** for one exact
   model. Include a change map: edit → preserved requirement → evidence.
   Knowledge-probe results, such as Petrov's, are leads, not deletion
   instructions.
3. **Publish a one-block AP config** for users who want to opt in, and the
   rollback config ([example](workflow/examples/tdd-sonnet-5-5/)).
4. **Collect evidence in two separate ways** ([beta process](workflow/BETA.md),
   [evaluation method](workflow/EVALUATION.md)):
   - frozen, paired campaigns that volunteers can run with their own
     credentials, reported as one sanitized file per configuration and never
     pooled;
   - everyday feedback through a reviewed template, with no automatic uploads.
5. **Promote only after a held-out campaign** and a human decision, scoped to
   that model, host and route.

## Honest limits of the tooling today

- Agent Profiles 0.19.4 routes by the model ID the host states. It does not
  detect the model.
- Delivery into a host's native skill discovery needs an AP adapter that is
  not released yet.
- Interactive delivery through AP's instruction-file bootstrap exists, but was
  not evaluated here.

## Credits

- **Superpowers:** Jesse Vincent / obra (MIT).
- **Knowledge probes:** Nikolay Petrov, with Intel's dokimi
  ([obra/superpowers#2665](https://github.com/obra/superpowers/issues/2665)).
- **[Agent Profiles](https://github.com/guisam/Agent-Profiles) and the skill-compaction preset:** Apache-2.0.

Nobody named here reviewed or endorsed this work.
