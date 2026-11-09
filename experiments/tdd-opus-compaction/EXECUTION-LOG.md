# `apsp-tdd-002` execution log (Opus 5.5 TDD candidate, tier C smoke)

- **2026-11-08, operator:** approved starting the experiment, plus auto-resume
  after usage-limit pauses. The scope is tier C only: ≤ 24 child runs, no
  graders, estimate about $2, ceiling $12. Tiers A and B are not approved.
- **Auto-resume:** an hourly T3 scheduled task, bound to this
  thread. It reads `run-state.json`, and deletes itself when `complete` is
  true.
- **Build** (no model calls):
  - fixtures D1-D4 (D3 serves D3a and D3b), with good, bad and
    alternative-valid references; selfcheck 16 trees / 35 expectations pass;
  - harness 2.3.0 wraps the frozen 2.2.2 harness (14 tests);
  - delivery in `private/tdd002`: blind aliases; the candidate is assigned to
    `claude-opus-5-5` only; routing verified (Sonnet, Haiku, the near-miss
    `claude-opus-5` and unknown IDs get the baseline);
  - contexts frozen: full 10,602 bytes, cand 7,952 bytes (Δ 2,650 = `SKILL.md`
    Δ);
  - preflight with `init` probe passes for both arms.
- **Stage-0 smoke:** 2 valid runs. Amendment 1 fixed two parsing gaps
  (grepped Node assertion blocks; pipes inside quotes); the fixes were
  validated offline on the smoke streams. Freeze 1.1.0 written; stage 0
  accepted.
- **Stage 1:** 20/20 setup-valid; 0 retries; 0 ponytail; 0 graders.
  - Official: 4/10 vs 5/10.
  - Agent-proposed (D3b capture correction): 6/10 vs 6/10.
  - **No candidate-only failures** under either.
  - Tokens: 577k vs 581k.
  - Children's cost: $1.32 in total.
- **The auto-resume task was deleted** (runs complete).
- **The operator audit of 3 items is pending** (`smoke/RESULTS.md`).
