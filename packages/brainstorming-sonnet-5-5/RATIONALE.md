# Rationale: `@apsp/brainstorming-sonnet-5-5@0.1.0`

**Status: rejected 2026-11-07** (pilot `apsp-bs-001`: one must-pass regression, C02). Retained as a failed variant; do not select it. See `evaluations/brainstorming/RESULTS.md`.

Status: **candidate, unvalidated**. It is selected only for exact model
`claude-sonnet-5-5` in a consumer that opts in. Every other model gets
`@apsp/brainstorming-upstream@7.0.2`.

## Selection from the knowledge evidence

Petrov's dokimi data (revision `586f823`) probed 25 of 118 brainstorming atoms.
Under strict scoring (`correct_complete` only), the 25 atoms break down as:

| Haiku 5.5 | Sonnet 5.5 | Atoms |
| --- | --- | --- |
| added | added | 17 |
| added | **redundant** | **3** |
| redundant | redundant | 2 |
| still missing | still missing | 1 |
| still missing | added | 1 |
| redundant | unpaired | 1 |

The ticket asks for passages that are added for Haiku and redundant for Sonnet.
The three such atoms are:

| Atom | Span (7.0.2) | Text (paraphrase) | Sonnet without skill | Decision |
| --- | --- | --- | --- | --- |
| `a9759dad67d` | L101-105 | Otherwise state your call and reason as a proposal and move the work forward | correct_complete, self-reported confidence 0.6 | **Kept.** It governs every question/proposal choice in the skill and is part of the core conversation contract. A knowledge probe that Sonnet answers correctly does not show that Sonnet *does* it reliably. |
| `a10f53895ba` | L123-126 | Read from how they talk which how-choices they want; someone who raises the how wants options with your pick | correct_complete, confidence 0.3 | **Deleted** (2 sentences). The adjacent outcome-oriented half (L126-129) and L116-118 ("sketch each… which you'd pick") remain. Case C04 directly tests the deleted behavior. |
| `abe2ec10237` | L312 | Requirements, scope, tradeoffs, conceptual choices stay in text | correct_complete, confidence 0.7 | **Deleted** (1 sentence). The per-question test ("would they understand this better by seeing it?") and "a UI topic isn't automatically a visual question" remain. Case C11 tests it. |

The Sonnet arm was self-extracted and self-judged, and the low no-skill
confidences show these are not robust "known" facts. That is part of what the
pilot tests.

## Exact diff (SKILL.md only; all resources unchanged)

```diff
@@ -120,9 +120,7 @@
 **How it gets made.** Every project rests on choices about medium, tools,
 materials, and resources: the platform, programming language, and
-libraries for an app; the medium for a piece of art. Read from how they
-talk which of those choices they want to make. Someone who raises the how
-or asks about trade-offs wants the options with your pick. Someone who
+libraries for an app; the medium for a piece of art. Someone who
 talks about outcomes is handing you the how: make those calls and state
@@ -309,8 +307,7 @@
 Mockups, layouts, diagrams, and side-by-side designs go in the browser.
-Requirements, scope, tradeoffs, and conceptual choices stay in text. A
-question about a UI topic isn't automatically a visual question.
+A question about a UI topic isn't automatically a visual question.
```

Size: 15190 → 14969 bytes (−221, −1.5%). This is the *instruction* size
difference. It is not a token or cost saving claim.

Preserved deliberately: the HARD-GATE, approval steps 1-4, the
`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` path, the builder-check
dispatch and its file name, the `superpowers:writing-plans` handoff, the
visual-companion offer wording, the frontmatter `name`/`description` (activation
text), and all supporting files.

## Haiku 5.5: no candidate

All three passages are *added* knowledge for Haiku, so none is removable for it.
The one blue span (`harmful.md`, L164-166, "the design comes in the next one")
was misread by Haiku *with* the skill. It is a candidate for a **clarifying
rewrite**, not removal, possibly because L72-76 allow the short design in the
first message. A rewrite is a different treatment from shortening. It is
deferred and needs its own frozen case set. Haiku therefore stays on the baseline.

## Not applicable to

Opus, Sol or any other model: they are not in the knowledge data. Also not
applicable to Bedrock deployments without their own behavioral evidence.
