# Stage-1 freeze 1.0.0 (apsp-bs-002)

Frozen 2026-11-07T22:11:31Z, before any stage-1 child or grader call.
`FREEZE-1.0.0.sha256` (sha256 `3a7c9122…`) lists 54 files by path relative to the
companion root: suite (cases, rubric, grader prompt, run-config), fixtures `habit` and
`habit-sync`, both package trees, both consumers' `.agent-profiles/` (config, adapter,
role, lock), AP runtime manifest, trial trust policy, harness `collect_v2.py` 2.1.0 and its
tests, and TREATMENT/PROPOSAL/INVENTORY. It is never regenerated; a treatment-relevant change
needs a new freeze version, recorded in `AMENDMENTS.md` when it happens.

| Input | Value |
| --- | --- |
| Control package | `@apsp/brainstorming-upstream@7.0.2`, AP digest `5f4f5b6f…` |
| Treatment package | `@apsp/brainstorming-sequencing@0.1.0`, AP digest `e1379ff5…`, SKILL.md `f942f2f0…` |
| AP runtime | `@guisam/agent-profiles` 0.19.4 (npm) |
| Children | `claude-sonnet-5-5` via Agent tool `model: sonnet`, subscription session |
| Graders | `claude-opus-5-5` via Agent tool `model: opus`, two independent per bundle |
| Limits (enforced by harness) | 57 child runs, 5 retries, 20 grader runs |
| Decision rule | PROPOSAL.md "Stage 1" rules 1-6, implemented in `collect_v2.decide` |

Known, unremoved confounds: native Superpowers plugin listing visible to children; harness
forbids starting servers; single-turn / scripted two-turn evaluation; the coordinator authored
the treatment and cases (held-out confirmation is reserved for stage 2).
