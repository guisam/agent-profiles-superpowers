# Beta feedback (opt-in, reviewed by you before sharing)

Fill this in yourself, read it through, and paste it into the maintainer's
issue tracker. Nothing is collected or uploaded automatically.

**Do not include:**

- prompts or chat text;
- source code or diffs;
- file paths or repository names;
- transcripts or tool output;
- account, organization or session identifiers;
- credentials.

Paraphrase instead.

## Configuration (copy from `agent-profiles resolve --json` and your host)

- Exact model ID, as your host reports it. Write "unknown" if your host doesn't
  say. Don't guess from behavior.
- Host and version:
- AP version:
- Skill package and version, with its AP digest (first 12 characters are
  enough):
- Delivery route (for example, AP bootstrap in CLAUDE.md, appended context,
  or a plugin export):
- Anything else active that could interact: other skill sets, hooks, global
  instructions. Name them generically.

## What happened

- Kind of task, paraphrased (for example, "small bug fix in a Node service
  with existing tests"):
- What you expected the skill to make the agent do:
- What it did instead (behavior, not wording):
- Category: missed test-first / wrong exception handling / skipped
  verification / over-asked / under-asked / other:
- How often, roughly: once / sometimes / every time:
- Did you try the same task on the full upstream package? Same / different /
  not tried.

## Suggested scenario (optional)

A one-paragraph task description the maintainer could turn into a frozen
evaluation case. It must contain no proprietary details.

## Consent

- [ ] I reviewed everything above, and it contains no private material.
