## Progress update: first slice complete (brainstorming, Sonnet 5.5) — 2026-11-08

**No variant is adopted.** The recommended configuration keeps every model on full upstream Superpowers 7.0.2 brainstorming content. Two different candidates were tested and both failed, for different reasons. The companion project exists **only on the maintainer's machine**: no remote, release, signing or publication. The local commit described below is not publicly accessible.

### Results

| Experiment | Treatment | Outcome |
| --- | --- | --- |
| `apsp-bs-001` | **Shortening**: delete 221 bytes judged redundant for Sonnet | Rejected for lack of benefit. The earlier C02 "regression" was withdrawn in audit (reported in the previous update). |
| `apsp-bs-002` stage 1 | **Sequencing clarification** of L164-166 (design in the next message, not the approaches message) | Original procedural outcome **INCONCLUSIVE**; corrected outcome **STOP-NEGATIVE**. Candidate retired. |

`apsp-bs-002` stage 1 used Sonnet 5.5, 8 cases × 2 arms × 3 repetitions (48 analyzed child runs, all matched pairs complete) and two blind Opus graders per case.

- **Primary endpoint:** the design was deferred out of the approaches message in **0/6** runs with full upstream text and **0/6** with the clarification. No observed improvement.
- **S3 (several approaches):** all-must-pass dropped from 3/3 to 1/3 with the clarification. That alone blocks progression.
- **Gate breaches:** none in the treatment arm. One control-arm design-gate breach (a full-text run edited files without approval).
- **Procedural record:**
  - The stage-1 freeze (54 files) still verifies.
  - Two amendments, both after execution:
    - **Amendment 1** raised the grader-attempt budget (24 attempts, all used). Children, grading inputs and decision rules were unchanged.
    - **Amendment 2** overrode the identical-file check for two cases (U1/U2), whose two graders both passed every criterion and therefore wrote byte-identical files. Transcripts confirmed four separate grader executions with no access to each other's output. The aggregate was recomputed through a separate scoring path, with no regrading or new model calls. The original **INCONCLUSIVE** result and scores are preserved next to the corrected **STOP-NEGATIVE**.
  - Lesson: byte equality says nothing about grader independence. A future harness should verify execution provenance instead (recorded, not implemented).
- **Disposition:** no stage 2, no adoption, no further rewrite experiment in this slice.
- **Estimated cost** (API-equivalent at cached list rates; not billing): children ≈ $6.31, graders ≈ $4.31, coordinator not measured. Usage was subscription capacity, plus credits the operator added during a pause.

### Tested environment and limits

- Sonnet 5.5 on a subscription-backed Claude Code host only.
- Every child context in both experiments included the **Ponytail SubagentStart instructions** and the **native Superpowers skill listing**.
- The results say nothing about standalone Superpowers, Haiku, Opus, Sol, Bedrock or other hosts.
- Small pilots: no statistical non-inferiority, no optimum, no user-benefit claim.
- Scripted single-turn and continuation cases, not live multi-turn use.
- One coordinator designed, ran and audited both experiments. There was no independent review.

### Generic AP gaps (filed separately)

- #90: bug. Plain-text `resolve` omits the package identity for *required* packaged skills but prints it for *available* ones.
- #91: bug. `update` with a package-qualified target gives a misleading "not in the library" error.
- #89: enhancement. `update` cannot move a tuple to a differently named variant package.

The config v3 release-label requirement is documented behavior and was not reported as a defect. All three reproduce on 0.19.4, the current npm release; AP core is unchanged.

### Acceptance criteria

| Criterion | Status | Evidence / gap |
| --- | --- | --- |
| Separate companion skeleton, AP/core boundary | ✅ Complete | Local companion README ownership table; AP core unchanged |
| Petrov/dokimi/Superpowers credit, license audit, provenance | ✅ Complete | README credit, PROVENANCE license audit. Dataset linked, not copied (no license) |
| Exact source mapping or new-baseline limits | ✅ Complete, with limit | v7.0.2 `22f0b46`; equivalence to the study checkout is inferred, not proven |
| Complete resources, dependency closure, helper-platform checks | 🟡 **Partial** | Full tree and LICENSE byte-exact from git blobs, with hashes. **`writing-plans` dependency documented but not packaged.** Helpers passed `node --check` / `bash -n` only; **runtime qualification deferred** (never executed) |
| Immutable baseline, minimal candidates with diff rationale | ✅ Complete | Baseline digest `5f4f5b6f…`; Sonnet candidate with exact diff; Haiku intentionally unchanged; sequencing treatment documented |
| Frozen cases/rubric and logging/export checks before runs | 🟡 **Partial** | `apsp-bs-002` frozen before runs and intact; amendments 1-2 were post-execution and documented. `apsp-bs-001`: two frozen files changed after the freeze (reconstructed byte-exact), the first freeze was overwritten, and arm labels were visible. Coordinator usage only partly measured |
| Repeated paired evidence or honest blockers | ✅ Complete for Sonnet 5.5 | bs-001 2 reps, bs-002 3 reps. Haiku: no candidate. Opus/Sol/Bedrock: not tested (stated) |
| No must-pass regression for adopted; failed retained | ✅ Complete | Nothing adopted; both candidates retained with status notes |
| Model/role routing and fallback across two consumers | ✅ Complete | AP 0.19.4: exact-model routing, unknown-model fallback, pin isolation |
| Findings separate knowledge, delivery, behavior, cost | ✅ Complete | FINDINGS sections 1-7 |
| No optimal/obedience/accuracy-gain claims | ✅ Complete | Stated limits throughout |
| Final handoff: commands, artifacts, open questions, next step | ✅ Complete (local) | HANDOFF.md in the local commit |

**Publication readiness: not ready.** Everything is in one local commit. Raw transcripts, ledgers, host identifiers, consumers and the trial trust policy are excluded by ignore rules and are not committed. Publishing needs the decisions below.

### Decisions still needed from the maintainer

1. Owner and visibility of a companion remote, and whether to push the local commit.
2. Whether to ask Petrov about redistribution terms for the dataset (no license today).
3. Whether sanitized ledgers and per-case grades may be published.
4. Whether the partial criteria (packaging `writing-plans`, qualifying helper runtime) belong in this issue or a follow-up.

### Recommendation

Keep this issue open until decisions 1 and 4 are made. If the two partial items move to follow-ups, the brainstorming slice is otherwise ready to close as a documented negative result. A negative experimental result is a valid outcome for this slice, not a project failure.
