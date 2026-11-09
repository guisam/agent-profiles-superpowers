# Opt-in maintainer beta

This is how a skill maintainer can publish versioned candidate variants and
let volunteers contribute evaluation capacity, without a Superpowers plugin
and without changing anyone's default.

## Principles

- **Full upstream content is the default.** A variant reaches a model only
  through an explicit, local opt-in by the person who runs the agent.
- **Exact identity or nothing.** A variant is bound to one exact model ID,
  and optionally one role.
  - A model whose ID is unlisted, near-miss (`claude-sonnet-5` is not
    `claude-sonnet-5-5`) or unstated gets the baseline.
  - Never infer the model from its behavior.
  - `verify_delivery.py` checks this fallback.
- **Two kinds of evidence, never mixed:**
  - **Controlled campaigns:** frozen tasks, a frozen rubric, paired arms, and
    one configuration per report. These can support or block promotion.
  - **Everyday beta feedback:** real use, and the failures and new scenarios
    it surfaces. This feeds new frozen cases. It never counts as a pass rate.
- **Private by default.** Volunteers share only what they have reviewed. There
  is no automatic upload or telemetry, and nothing is sent anywhere.

## For the maintainer: publishing a candidate

1. **Package it.**
   - Keep the baseline as an immutable package of the exact upstream bytes
     (`@ns/<skill>-upstream@<upstream version>`).
   - Publish the candidate as a separate package with its own version
     (`@ns/<skill>-<model>@0.x.y`) and a description that says
     "unvalidated candidate for <exact model ID>".
   - Ship the full resource tree and `LICENSE`.
   - Run `workflow/tools/check_package.py <candidate> --compare <baseline>`.
2. **Publish identities.**
   - Publish an `IDENTITIES.json`: upstream commit and blob IDs, per-file
     sha256, and AP digests.
   - Publish a change map that links every edit to a preserved requirement.
   - Publish a campaign file.
   - Volunteers check bytes against these before running anything.
3. **Publish a consumer snippet,** a single assignment (see
   `examples/tdd-sonnet-5-5/consumer/.agent-profiles/agents.yaml`). Also
   publish the rollback config, plus a note on what is unvalidated.
4. **Run a controlled campaign** before calling a variant anything other than
   "beta". See "Promotion" below.

AP distribution is a local store fed by `agent-profiles add <id>@<version>
--source <dir>`. AP 0.19.4 has no remote registry. Volunteers fetch the
package directory (for example, from a tagged release of this repository)
and import it locally. The trust policy is theirs to set.

## For a volunteer: opting in

1. **Fetch** the tagged package directories and check their sha256 against
   `IDENTITIES.json`.
2. **Import** into your store with `agent-profiles add …` (once per package).
   Then add the maintainer's single assignment block to your project's
   `.agent-profiles/agents.yaml` and run `agent-profiles install`.
3. **Confirm the routing** before use:
   ```sh
   agent-profiles resolve --host claude --identity-source host-stated --model <your exact model ID> --json
   ```
   The `required[].backing.sha256` field must equal the candidate's AP digest
   for your model, and the baseline's for any other model.
4. **Use your agent normally.** The candidate applies only when your host
   states the exact model ID that the assignment names.

### Rollback (any time)

Delete the assignment block, or copy in `agents.rollback.yaml`, then run
`agent-profiles install`. Resolve again and confirm you get the baseline
digest. In a session that already loaded the candidate, start a new session,
or re-run `resolve` after compaction, as the AP bootstrap asks.

## Contributing evaluation capacity

### Controlled campaign runs (counted)

**Before running:**

- Run exactly the maintainer's frozen campaign (`campaign.json`, cases,
  fixtures, rubric, freeze hash), with your own runner and credentials.
- Run `preflight.py` for both arms before the first slot.
- Keep raw evidence on your machine.

**What to submit:**

- Export **one** `apsp-results/1` file for your configuration, and run
  `results_format.py validate` on it.
- Read the file. It holds identities, booleans and counts only.
- Submit it by hand.

**What the report must identify:**

- the exact model ID;
- the host and version;
- the AP version;
- both arms' AP digests and delivered-context hashes;
- the delivery route;
- the launch flags;
- the effort and tools;
- the OS.

The maintainer aggregates per configuration key only. Results from different
keys are listed side by side, never summed into a headline.

### Everyday beta feedback (not counted)

Use [templates/beta-feedback.md](templates/beta-feedback.md):

- the configuration identities;
- a paraphrased task kind;
- expected vs observed behavior;
- whether the baseline behaves differently.

The template lists what must not be included. The volunteer reviews it and
pastes it manually.

The maintainer turns repeated or serious reports into new frozen cases for
the *next* campaign. Feedback never edits a candidate that is mid-campaign,
and is never used to tune a candidate against held-out cases.

## Promotion (what "adopted" would require)

A variant may become a recommended selection for one exact model only with
all of the following:

1. **A passing contract review.** There is a change map, and no requirement is
   weakened, expanded or silently changed.
2. **Development screening with no observed regression.**
3. **A held-out controlled campaign** with independently authored cases and
   enough repetitions for a stated margin. For example, the 12 reps and
   −15-point margin in `experiments/tdd-compaction/stage2/PROPOSAL.md`. It must
   show no regression beyond that margin, and no unmatched approval or
   negative-control failure.
4. **A human decision,** recorded with its scope: model, host, delivery route,
   and the tested cases.

Even then, the baseline stays the default for every other model. Rollback
stays one config edit away.

The TDD candidate has passed (1) and (2) only, so it remains an opt-in beta.
