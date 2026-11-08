# Superpowers brainstorming adapter (experimental)

Repository and host instructions govern permissions, delegation and approval
gates. This adapter changes delivery only.

Agent Profiles delivered the required brainstorming skill from a versioned
package. Its supporting files (`builder-check-prompt.md`, `visual-companion.md`,
`scripts/`) belong to that package. When the skill tells you to read one, read
it with `npx --no agent-profiles library read <package>@<version> <path>` plus
the same `--store`. Get `<package>` and `<version>` from `required[].package`
in the output of the same resolve command with `--json` added. A missing
resource is a setup problem; report it.

Use only the skill text delivered here. Do not load Superpowers through a host
skill tool or plugin. `superpowers:writing-plans` is the next stage and is not
delivered in this trial: where the skill says to invoke it, say that the plan is
the next step and stop.
