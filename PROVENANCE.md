# Provenance, licensing and source mapping

Recorded 2026-11-07. This file covers everything this companion copies or
derives. Hash commands are under "Verify".

## Sources

| Source | Revision | License | How it is used here |
| --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) (Jesse Vincent) | v7.0.2, `22f0b463e7a5e579904dd6211a520321035526f7` (tree `8fddc972…`, `skills/brainstorming` tree `ebd5b1af…`) | MIT, Copyright (c) 2025 Jesse Vincent | Skill files copied byte-exact from git blobs; `LICENSE` copied into every package |
| [napetrov/obra-superpowers](https://github.com/napetrov/obra-superpowers/tree/586f82373fa984f941bbaaee4d3118f7c8a30f14) knowledge-map data (Nikolay Petrov) | `586f82373fa984f941bbaaee4d3118f7c8a30f14` | **None stated** for the data (see audit) | Linked and summarized only. Atom IDs, line spans and short quoted fragments are cited. No bulk data or charts are copied into public files. |
| [Intel dokimi](https://github.com/intel/dokimi) | not pinned by the dataset | see that repository | Measurement tool used by Petrov; not run here |
| [Agent Profiles](https://github.com/guisam/Agent-Profiles) | npm `@guisam/agent-profiles@0.19.4`; example/findings from `origin/main` `66ed1e6` (PR #87) | MIT | Package format, selection, store; nothing copied |

### License audit

- Superpowers: MIT. The license requires keeping the notice with copies and
  substantial portions. Every package tree here contains the upstream `LICENSE`
  byte-exact (sha256 `a37e0e96…`). Candidate packages are adaptations. The MIT
  notice still applies to them.
- Dataset: commit `586f823` is an orphan commit (no parents). It adds only
  `README.md`, `facts.jsonl`, `skills.csv`, `harmful.md` and 5 PNG charts. It
  contains no license file. GitHub reports the *fork* as MIT. That detection
  comes from the fork's default branch, which carries Superpowers' own license.
  It does not establish a license for Petrov's data. Treat the data as all rights
  reserved: link to it, cite it with attribution, and do not republish
  `facts.jsonl`, `skills.csv` or the charts. Local copies used for analysis live
  in the ignored `private/` tree or the earlier trial's ignored evidence folder.
- Asking Petrov for redistribution terms is an open question. No upstream message
  is authorized by the ticket.

## Source mapping (dataset → baseline)

The study README says "2026-11-04 checkout" and names no commit. The exact
revision cannot be recovered by ancestry: the data commit has no parent.
Content evidence:

1. On obra/superpowers, the only commit in 2026-11-03..2026-11-05 is
   `22f0b46` (v7.0.2, 2026-11-03T22:17Z). The same holds for
   `skills/brainstorming`.
2. All 478 atoms' line spans lie within the corresponding `SKILL.md` at
   `22f0b46`. At v7.0.1 (`2ce8aa1`), 5 atoms point past the end of file
   (brainstorming 2, executing-plans 1, subagent-driven-development 2).
3. The only quoted span in `harmful.md` (`brainstorming/SKILL.md:164-166`, "When
   there's genuinely one sensible way…") matches 7.0.2 lines 164-166 exactly. At
   7.0.1 those lines are about spikes.
4. The three spans selected for the candidate (102-104, 123-125, 312) were read
   at 7.0.2. Each matches its atom text in content.

Conclusion: **new baseline, labeled v7.0.2 `22f0b46`, highly likely identical to
the study's checkout for `brainstorming`**. This is inference. It is not proven
for other skills or for uncommitted local state in Petrov's checkout. Evidence
transfer limits:

- Only 25 of 118 extracted brainstorming atoms were probed. Unprobed text has no
  knowledge evidence either way, and it is not evidence of redundancy.
- Only `SKILL.md` was measured. `builder-check-prompt.md`, `visual-companion.md`
  and `scripts/` have no knowledge evidence.
- Models were Bedrock `us.anthropic.claude-haiku-5-5` and
  `us.anthropic.claude-sonnet-5-5`. The behavioral trials here use subscription
  Claude Code sessions (`claude-sonnet-5-5`). Same model family name, different
  deployment, system prompt and tools.
- The Sonnet arm was self-extracted and self-judged.
- Changes are applied by exact content match, never by line number.

## Packages

AP package names and versions identify *this companion's* variants. They carry
upstream versions only where content is unmodified upstream:

| Package | Meaning | AP tree digest (sha256) |
| --- | --- | --- |
| `@apsp/brainstorming-upstream@7.0.2` | Immutable baseline: upstream v7.0.2 skill tree byte-exact, plus `package.yaml` and upstream `LICENSE`. Version mirrors upstream. Full-content fallback for every model without adopted evidence. Never edited; a new upstream release gets a new version. | `5f4f5b6ffc1a61b7caca25642a775bc4e6cb7b195fb1932589d0b51fc174433c` |
| `@apsp/brainstorming-sonnet-5-5@0.1.0` | Candidate for exact model `claude-sonnet-5-5` only. Its own version line (0.x = unvalidated) is independent of upstream. Derived from 7.0.2. | `759b3a0c5d3c8951fc603bed86a87e12bc15681d7e172c4f24ab289f86e3a3f7` |

AP accepts only exact `x.y.z` versions with no prerelease or build tags
([contract](https://github.com/guisam/Agent-Profiles/blob/main/docs/development/issue-20-contract.md)),
so the upstream base of a candidate is recorded in its manifest description and
here, not in its version. Haiku 5.5 has no candidate. Its initial candidate is the
unchanged baseline (see `packages/brainstorming-sonnet-5-5/RATIONALE.md`).

### Files and transformations

Per-file sha256. Upstream files were written from `git cat-file blob` at
`22f0b46`. Each was then rechecked with `git hash-object` against the upstream
blob ID. This avoids Windows checkout line-ending conversion: the
upstream working tree here has CRLF in some files; the blobs are LF.

| Path | Upstream | Baseline 7.0.2 | Candidate 0.1.0 |
| --- | --- | --- | --- |
| `SKILL.md` | blob `9eb0edc7` | `2c9ca71f…` = upstream | `a4628536…` **2 deletions** |
| `builder-check-prompt.md` | blob `136e9c1d` | `36d51a47…` | same |
| `visual-companion.md` | blob `8dca065b` | `6ffcb038…` | same |
| `scripts/frame-template.html` | blob `f540bb8a` | `6a8a4e58…` | same |
| `scripts/helper.js` | blob `e11d2648` | `43c6d699…` | same |
| `scripts/server.cjs` | blob `fdc79612` | `763abf96…` | same |
| `scripts/start-server.sh` (mode 755 upstream) | blob `f6d538a4` | `314dd68d…` | same |
| `scripts/stop-server.sh` (mode 755 upstream) | blob `7cacfe94` | `0b5ccbbd…` | same |
| `LICENSE` (repo root upstream) | blob `abf03903` | `a37e0e96…` | same |
| `package.yaml` | added | `b4bf1081…` | `dc2ebada…` |

The AP package digest hashes bytes and paths, not file modes. Executable bits
are not carried by AP identity.

### Dependency closure and cross-skill references

- Relative links inside the tree are preserved: `builder-check-prompt.md`,
  `visual-companion.md` ("in this directory"), and `visual-companion.md` →
  `scripts/start-server.sh`, `stop-server.sh`, `frame-template.html`, `helper.js`.
  `server.cjs` serves `frame-template.html`/`helper.js` from its own directory.
- Cross-skill: `superpowers:writing-plans` (SKILL.md L32, L282) is the next stage
  after approval. It is **not packaged in this slice**. The consumer adapter maps
  it to "say that the plan is the next step and stop". A full workflow consumer
  must add a `writing-plans` package. This is a known gap, and nothing is
  silently dropped.
- Builder check dispatches a fresh subagent with `builder-check-prompt.md`. This
  is a host capability (subagent tool). The skill text provides a fallback.
- Runtime: helpers need `bash` and `node` (stdlib only: `crypto`, `http`, `fs`,
  `path`, `os`, `child_process`). Windows needs Git Bash; `start-server.sh`
  detects MSYS/MINGW/CYGWIN and runs in the foreground.

### Helper platform checks (Windows 11, Git Bash 5.2.37, Node 24.20.0)

| Check | Result |
| --- | --- |
| `node --check server.cjs`, `node --check helper.js` | passed |
| `bash -n start-server.sh`, `bash -n stop-server.sh` | passed |
| Executing the server or scripts | **not done**. Preserving a script does not authorize running it; trial children are told not to start servers. |

## Credit

See [README.md](README.md#credit-and-thanks). Attribution is not endorsement:
neither Petrov, Intel, nor Jesse Vincent/obra reviewed or endorsed this work.

## Verify

```sh
# from this folder; expects the upstream checkout at ../superpowers
for p in SKILL.md builder-check-prompt.md visual-companion.md scripts/*; do
  [ "$(git hash-object packages/brainstorming-upstream/7.0.2/$p)" = \
    "$(git -C ../superpowers rev-parse 22f0b46:skills/brainstorming/$p)" ] || echo "MISMATCH $p"; done
(cd packages/brainstorming-upstream/7.0.2 && find . -type f | sort | xargs sha256sum)
npx --no agent-profiles add @apsp/brainstorming-upstream@7.0.2 --source packages/brainstorming-upstream/7.0.2 --store <throwaway-store> --json
```

## systematic-debugging (added 2026-11-08, experiment `apsp-sd-001`)

Source: obra/superpowers v7.0.2 `22f0b46`, `skills/systematic-debugging/`
(MIT). `SKILL.md` blob `62fc752a` is identical at v7.0.0, v7.0.1 and v7.0.2,
so the study's 2026-11-04 checkout almost certainly measured these bytes. Two
dataset atoms carry spans that point at code-fence lines (`L16`, `L88`); they
were mapped by content to L76-80 and L97-100 (see
`experiments/systematic-debugging-compaction/CONTRACT.md`).

Files were written from `git cat-file blob` and rechecked with `git hash-object`
against the upstream blob IDs (all match):

| Path | Upstream blob | Baseline 7.0.2 sha256 | Candidate 0.1.0 |
| --- | --- | --- | --- |
| `SKILL.md` | `62fc752a` | `51c6435d…` | `d0ccf6df…` (Phase 1-3 compacted, Quick Reference removed; see RATIONALE) |
| `condition-based-waiting-example.ts` | `703a06b6` | `40ae5ebe…` | same |
| `condition-based-waiting.md` | `70994f77` | `e89fec84…` | same |
| `defense-in-depth.md` | `e2483354` | `1e175fb8…` | same |
| `find-polluter.sh` (mode 755 upstream) | `985f5d08` | `dd7b8f13…` | same |
| `root-cause-tracing.md` | `0e72e8f9` | `75b933b6…` | same |
| `LICENSE` (repo root upstream) | `abf03903` | `a37e0e96…` | same |
| `package.yaml` | added | `876c6683…` | `f23a6165…` |

AP 0.19.4 digests: `@apsp/systematic-debugging-upstream@7.0.2`
`f758787e9160ad1e1030825904a80d2dfdfdd57a5e0d60d163ecb4c697ca0005`;
`@apsp/systematic-debugging-sonnet-5-5@0.1.0`
`ed798698e88a2b762104faa2871f60628cbcabb242543f9eca17a9c079091a18`
(throwaway store; the home store is untouched).

Dependency closure: the in-tree resources are complete. `find-polluter.sh` has
an upstream test (`tests/systematic-debugging/test-find-polluter.sh`); it is not
packaged and the script was not executed. The cross-skill names
`superpowers:test-driven-development` and
`superpowers:verification-before-completion` are **not packaged** (known gap,
same class as `writing-plans`).

Host note: this machine's account-synced Superpowers plugin is **6.4.2**, whose
`systematic-debugging/SKILL.md` differs from 7.0.2 (blob `095d194a`: the
pre-#2375 example that prints the secret) and still installs the pressure-test
prompts next to the skill.

## test-driven-development (added 2026-11-08, experiment `apsp-tdd-001`)

Source: obra/superpowers v7.0.2 `22f0b46`, `skills/test-driven-development/`
(MIT). `SKILL.md` blob `46838cc9` and `writing-good-tests.md` blob `d3c4482f`
are identical at v6.4.1, v7.0.0, v7.0.1 and v7.0.2, so the study's 2026-11-04
checkout measured these bytes. All 25 probed atoms' spans were mapped by
content (see `experiments/tdd-compaction/CONTRACT.md`).

Files were written from `git cat-file blob` and rechecked with `git hash-object`
against the upstream blob IDs (all match):

| Path | Upstream blob | Baseline 7.0.2 sha256 | Candidate 0.1.0 |
| --- | --- | --- | --- |
| `SKILL.md` | `46838cc9` | `64b03fce…` | `4117a24e…` (diagram and worked examples removed; see RATIONALE) |
| `writing-good-tests.md` | `d3c4482f` | `51471c85…` | same |
| `LICENSE` (repo root upstream) | `abf03903` | `a37e0e96…` | same |
| `package.yaml` | added | `ef1e24cc…` | `f0df317a…` |

AP 0.19.4 digests (throwaway store; the home store is untouched):
`@apsp/test-driven-development-upstream@7.0.2`
`ce680b8a2f3c31a12dad8b1d2c6917649b268149969a80fbea13dc4d0ab640f3`;
`@apsp/test-driven-development-sonnet-5-5@0.1.0`
`bd446f965112f984517f91a56e47fb8ddcf40686a3310cbeae62d0a36f524052`
(reproduced on a second `add`).

Dependency closure: complete in-tree (one reference file, no scripts).
`writing-good-tests.md` names `superpowers:writing-skills`, which is **not
packaged** (known gap, same class as `writing-plans`).

Host note: the account-synced Superpowers plugin on this machine carries a
byte-identical TDD `SKILL.md` (blob `46838cc9`). Any trial must prove that it
is absent from children (PROPOSAL §3).

### Workflow identities and method (added 2026-11-08, closeout)

- Machine-readable pins for both TDD packages are in
  `workflow/examples/tdd-sonnet-5-5/IDENTITIES.json`: the upstream commit,
  the blob IDs, full per-file sha256 values and the AP 0.19.4 digests. They
  are rechecked by `workflow/tools/verify_delivery.py`.
- The candidate was prepared with the AP `skill-compaction` preset 1.0.5
  (Apache-2.0). Its `SKILL.md` sha256 is
  `989b59b983c3d3ad047711e002269042ec788a49d8348e73d97392eeec68dc7d`. At the
  time, the preset was untracked in the local Agent-Profiles checkout. It is
  referenced, not copied.
- Redistribution boundaries are unchanged:
  - upstream MIT `LICENSE` in every package;
  - Petrov's dataset linked and summarized only (no license);
  - nothing published.
