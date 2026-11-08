# Corrections to `apsp-bs-001` claims (audit, 2026-11-07)

These correct or qualify statements in RESULTS.md, FINDINGS.md, PROTOCOL.md
and the first handoff. The original files keep their text, except where noted
in HANDOFF.md.

1. **Treatment and case labels were visible to the models.** All 44 child
   prompts contain the run ID, for example `apsp-bs-001.C04-user-controlled-how.cand.r1`.
   The ID appears in the opening line, in the project and reply paths, and in
   the required return line. Verified: 44/44 prompts contain `.full.` or
   `.cand.`, and 44/44 contain the case ID.
   - Both arms were equally exposed.
   - Case IDs such as `one-sensible-approach`, `scope-question-stays-text` and
     `approval-refused` hint at the behavior under test, which may raise pass
     rates in both arms.
   - Arm names may have primed behavior differently.

   PROTOCOL.md's statement that the arm label "is not visible in the model's
   context unless the child runs the `--json` lookup" was true only of the
   resolve output, not of the prompt. Harness v2 uses opaque run tokens.
2. **C11 "0/4 server starts" is not skill evidence.** The harness prompt
   instructed every child: "Do not start servers or run the skill's scripts."
   Zero starts shows compliance with the harness, not that the skill kept the
   scope question in text. That is judged separately by C11 M2 from the reply.
3. **Native-plugin caveat retained.** Superpowers is enabled globally in the
   host session. Children did not call the `Skill` tool (0/44), but the plugin's
   skill listing was visible in their context. That is uncontrolled exposure to
   the native skill's name and description. It cannot be ruled out that this
   affected both arms.
4. **C06 is a message-sequencing failure.** Replies combined approach and
   design and asked for approval before any writing or planning (M1/M3 4/4, no
   file changes). It is not an approval-gate failure. See
   [GRADING-ADJUDICATION.md](GRADING-ADJUDICATION.md#c06-one-sensible-approach-a-sequencing-failure-not-a-gate-failure).
5. **The C02 "regression" depends on inconsistent application of M2.** It
   disappears under either consistent reading. See the adjudication. The
   candidate stays rejected for lack of benefit.
6. **C01 and C08 scope.** C01 cannot discriminate because the skill text is
   ambiguous. C08 tested only missing-document recovery; normal recovery is
   untested.
7. **Freeze.** Two frozen files changed after the freeze. Hash reconstruction
   establishes exactly what changed. File mtimes *suggest* that the protocol
   paragraph describing the changes was written after all runs; this is
   supporting chronology, not proof. See [FREEZE-STATUS.md](FREEZE-STATUS.md).
8. **Privacy.** The first handoff listed `evaluations/brainstorming/runs.jsonl`
   among ignored private files. That was wrong: it was not excluded until this
   audit added it to `.gitignore`. Nothing was committed or published in the
   meantime; the folder is not a repository.
9. **Trial configurations.** `selectors/beta.agents.yaml` and the
   candidate-routing snippet formerly in README.md are archived trial
   configurations. They route `claude-sonnet-5-5` to a rejected candidate.
   Current use: `selectors/alpha.agents.yaml` (the baseline for every model).
10. **Coordinator cost was measurable, not unknown.** RESULTS.md and FINDINGS.md
    call the coordinator's usage unknown. The parent session transcript records
    per-message usage. Over the trial window (20:13-20:52Z, approximate, and
    including some non-trial analysis) it shows 108 Opus messages: 216 input,
    194,000 cache-write (1-hour), 27,236,674 cache-read and 89,762 output tokens.
    That is ≈ $8.8 API-equivalent at the cached list rates, more than either
    arm's ≈ $2.7. The figure is an estimate over an approximate window;
    subscription usage only.
