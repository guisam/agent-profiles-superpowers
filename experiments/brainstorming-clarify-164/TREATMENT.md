# Treatment for `apsp-bs-002`: sequencing clarification only (draft r2, not frozen)

## What changes

There is one edit to SKILL.md L164-166 of upstream v7.0.2 (`22f0b46`). All
other bytes and all resources stay unchanged. The edit was verified against the
baseline: the old text occurs exactly once, and the result is 15190 → 15331
bytes, sha256 `f942f2f0…` (draft; the frozen package digest will be recorded at
freeze).

```diff
 each trades off. Recommend one and say why, then ask which way they want
 to go; if they've handed you the how, say you'll go with your pick
 instead. When there's genuinely one sensible way, say so in that
-message and explain why the others don't fit; the design comes in the
-next one. This is for how it gets built; for what they want, get them
+message and explain why the others don't fit; the design comes in your
+next message, not this one. Only your first message, when nothing was
+open, puts the approach and the short design together (see Your First
+Message). This is for how it gets built; for what they want, get them
 describing first.
```

Proposed package: `@apsp/brainstorming-sequencing@0.1.0`. It is unvalidated,
derived from 7.0.2, and uses the same text for every model under test.

## Why this is the smallest change

- It only removes an ambiguity. "The next one" becomes "your next message, not
  this one", and the first-message exception (L72-76) is named where the
  conflicting reading arises. Observed behavior suggests that conflict: the
  apsp-bs-001 C06 replies combined approach and design, and Haiku's dokimi
  answer did the same.
- **It adds no approval requirement.** The preceding delegation rule (L163-164,
  "if they've handed you the how, say you'll go with your pick instead") and
  the proposal rule (L101-105) stay byte-identical. The added text contains no
  "confirm", "approve" or "permission" (checked). When the user has delegated
  the how, the approaches message still states the agent's pick as its call.
  It does not ask the user to choose or confirm.
- The message boundary it clarifies already exists in the written upstream
  text ("the design comes in the next one"); the treatment adds no new written
  requirement. **In practice, however, enforcing it may add interaction
  overhead compared with observed baseline behavior.** In apsp-bs-001 C06,
  Sonnet combined approach and design in 4/4 runs. If the treatment works, users
  in that situation get one more exchange before seeing a design. The
  experiment measures that cost (turns, design work invalidated by S1b-t2)
  instead of assuming it is zero.

## Approval-policy treatments: separate, not proposed now

These change *what needs the user's assent*, not message order. Each would
need its own experiment and frozen cases.

| ID | Policy change | Why not now |
| --- | --- | --- |
| P1 | Require explicit confirmation of the single approach before the design (r1's wording) | Conflicts with the delegation rule and the "state your call as a proposal" rule. It adds a question even where the user handed over the how. |
| P2 | When the how is delegated and there is one sensible way, allow approach and design in one message | Removes the existing boundary for delegated cases, so it trades fewer turns against less chance to redirect. It is a real candidate if screening shows the boundary costs users more than it saves, but it changes upstream semantics. |

The scenarios below include a delegated case (S1c). It checks that the
sequencing treatment does not drift into P1-style confirmation.
