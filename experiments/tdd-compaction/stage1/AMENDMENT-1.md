# Amendment 1: smoke finding and checker fix (2026-11-08)

Recorded after the first stage-0 smoke run and **before** any stage-1 run.
Under PROPOSAL §5 ("On failure: fix setup, record an amendment before freeze,
and repeat smoke once. A second failure stops the experiment"), this uses the
one permitted repeat.

## What the first smoke run showed (FREEZE-1.0.0, harness 2.2.0)

There were two child runs: R1 full rep 0 and R1 cand rep 0. Both were
setup-valid, had zero ponytail hits, ended with `ok`, and cost $0.068 and $0.050
(CLI-reported). Isolation acceptance held.

Both agents edited files **only through Bash**, with Python heredoc scripts
(`python - <<'EOF' … open(p,'w').write(s) … EOF`). Each chained the edit with
a test run in the same command and piped the run through `| tail`. Harness 2.2.0
gave each tool call a single class and took the run's outcome from the exit
code. So:

- the test write chained with a RED run was classed only as a test run, and
  `| tail` made its exit code 0, although unittest printed `FAILED (errors=1)`;
- the production write chained with the green full-suite run was classed only
  as a production edit.

The checker returned M1, M2 and M4 = false for both runs. The transcripts
show test-first, a RED run (ImportError) and a green full suite in both.
Every checker returned a verdict, as §5 requires, but the verdicts were
wrong. That counts as a setup failure.

## Fix (harness 2.2.1)

- **Sub-events:** each Bash call is split into ordered sub-events. A heredoc
  (its command line plus body) is one segment; other lines split on `&&`, `||`,
  `;` and `|`. A segment produces write sub-events for the test/production
  paths it writes, then a run sub-event if it is a test run.
- **Write detection is per segment:**
  - redirect targets;
  - `sed -i` and `tee`;
  - `cp`/`mv` destinations;
  - script writes (`open(...,'w')`, `write_text`, `writeFileSync`, …) inside
    heredocs or `-c`/`-e` scripts;
  - PowerShell writers.
  Reads (`cat`, `grep`, `head`) are not writes. Every shell write stays flagged
  for audit.
- **Run outcome** comes from the runner's own summary lines, in order. For
  unittest that is `OK`/`FAILED (…)`/`NO TESTS RAN` (plus a Traceback/ERROR
  fallback); for `node --test` it is `ℹ fail N` or `# fail N`. The exit code is
  used only for a single run with a non-zero exit. Anything else is `unknown`,
  listed in `order.unknown_run_outcomes` for audit, and never counts as RED or
  as a full-suite run.
- **Full-suite detection** ignores redirections such as `2>&1` and `> out`.
- **`tool_calls`** counts distinct tool calls, not sub-events. Gr1 packets list
  each tool call once.

Tests: 45 (7 new). They include the two real smoke command sequences, with
paths masked, in `tools/smoke_streams.json`. The checker selfcheck (21 trees,
48 expectations) still passes.

Offline re-scoring of the first smoke run with 2.2.1 gives, for both runs,
M1-M4 = true, S1 = true and S2 = false (ImportError RED, T6). It is written
to `rescore-2.2.1.json` beside each run. The original `result.json` files are
unchanged.

## Procedure changes

- `run-config.json`:
  - the stage-0 order adds a repeat smoke, R1 full and cand at rep 1;
  - `bundle_reps: [1]`, so the stage-0 grader smoke uses the repeat runs;
  - the stage-0 child limit rises from 4 to 6 (2 + 2 repeat + 2 setup retries),
    the stage-0 count originally approved before the D-block was dropped.
  The new maxima are 53 child and 12 grader runs (approved: 65 and 12).
- The rep-0 runs stay in the ledger as smoke evidence. They are never analyzed.
- New freeze: `FREEZE-1.1.0.sha256`. `FREEZE-1.0.0.sha256` is kept as written.

## Observation, not a result

Both arms used Bash scripts instead of the Edit/Write tools for every file
change. This is recorded as host-behavior context. Stage 1 reports
`shell_writes` per arm.
