# Draft AP report: text `resolve` omits the package identity of a required packaged skill

Status: **Filed 2026-11-08 as [Agent-Profiles#90](https://github.com/guisam/Agent-Profiles/issues/90) (bug).** The text below is the original draft. Status was **draft, not filed.** Target: guisam/Agent-Profiles. Found during #88.

Classification: **likely defect (inconsistency).** The same package gets an
identity line when it is *available* but none when it is *required*. AP's
guidance for reading package files (`library read <name>@<version> <path>`)
needs exactly that identity. The maintainer may still classify it as an
enhancement if the text output was never meant to support resource access.

## Environment

`@guisam/agent-profiles` 0.19.4 from npm; Windows 11, Git Bash, Node
24.20.0; config v3; isolated store and permissive trial trust policy; no
network. Source references are from the local Agent-Profiles checkout
`68b4b95`; that checkout has uncommitted changes in configuration files only.

## Reproduction

`AP=<agent-profiles executable> bash reports/repro-ap-gaps.sh <new-empty-dir>`
([script](repro-ap-gaps.sh)). It builds a fictional `@demo/tool@1.0.0` whose
SKILL.md says "Read ref/notes.md in this skill." Observed:

```text
text output lines naming @demo/: 0
json identity: @demo/tool@1.0.0
library read with that identity: note
control, same package as available skill:
Package @demo/tool@1.0.0
```

The text body appears under `## Required skill: tool` with no package, version
or digest line.

## Expected

The required-skill section names the package identity, or the exact
`library read` command prefix, so an agent can follow the skill's own relative
references. Available packaged skills already get this line:
`Package @demo/tool@1.0.0 (sha256 …). Load by binding ID: …`
(`src/diagnostics.ts`, the `skill()` helper around L352-366).

## Impact

Skills that ship supporting files reach the agent without a way to locate
them from the injected text: Superpowers brainstorming's
`builder-check-prompt.md`, `visual-companion.md` and `scripts/`. In #88 the
consumer adapter had to tell agents to rerun resolve with `--json` and read
`required[].package`. A side effect, useful for blind trials, is that the text
output does not reveal the package name. A fix that prints the identity should
be weighed against that; an opt-out flag would cover it.

## Not claimed

No security issue. JSON and MCP output already carry the identity. Behavior
of other AP versions was not checked.
