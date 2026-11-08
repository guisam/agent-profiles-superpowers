#!/usr/bin/env bash
# Minimal local reproduction of the two draft AP gap reports. No network, no model calls.
# Usage: AP=/path/to/agent-profiles bash repro-ap-gaps.sh <new-empty-directory>
# Verified 2026-11-07 with @guisam/agent-profiles 0.19.4 (Windows 11, Git Bash, Node 24.20.0).
set -euo pipefail
AP=${AP:?set AP to the agent-profiles executable}
W=${1:?give a new empty directory}
mkdir "$W" && cd "$W"
abs() { if command -v cygpath >/dev/null; then cygpath -wa "$1"; else realpath "$1"; fi; }
printf 'version: 1\nrequire_approval: false\n' > policy.yaml   # isolate from any machine trust policy
export AGENT_PROFILES_TRUST="$(abs policy.yaml)"
mkdir store; ST="$(abs store)"
mk() { # mk <name> <version>
  mkdir -p "pk/$1/$2/ref"
  printf 'schema_version: 1\npackage:\n  name: "@demo/%s"\n  version: "%s"\n  type: skill\n  description: demo\nentrypoint: SKILL.md\nbehavior:\n  delivery: instruction\n  hosts: []\n  effects: []\n' "$1" "$2" > "pk/$1/$2/package.yaml"
  printf -- '---\ndescription: demo skill %s\n---\nRead ref/notes.md in this skill.\n' "$2" > "pk/$1/$2/SKILL.md"
  echo note > "pk/$1/$2/ref/notes.md"
  "$AP" add "@demo/$1@$2" --source "$(abs "pk/$1/$2")" --store "$ST" --json >/dev/null
}
mk tool 1.0.0; mk tool 1.1.0; mk tool-variant 1.0.0
project() { # project <dir> <config version> <required> <available>
  mkdir -p "$1/.agent-profiles/profiles" "$1/.agent-profiles/roles"
  echo "# P" > "$1/.agent-profiles/profiles/base.md"; echo "# R" > "$1/.agent-profiles/roles/worker.md"
  cat > "$1/.agent-profiles/agents.yaml" <<EOF
version: $2
default_profile: base
default_role: worker
models:
  model-a: {profile: base}
families: {}
roles:
  worker:
    file: roles/worker.md
    skills: {required: [$3], available: [$4]}
skills:
  tool: {package: "@demo/tool", version: "1.0.0"}
assignments: {}
EOF
  "$AP" install --root "$1" --store "$ST" --offline --json >/dev/null
}
R=(--store "$ST" --host claude --model model-a --identity-source user --role worker)

echo "### Gap 1: required packaged skill, text output"
project req 3 tool ""
echo "text output lines naming @demo/: $("$AP" resolve --root req "${R[@]}" | grep -c '@demo/' || true)"
echo "json identity: $("$AP" resolve --root req "${R[@]}" --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const p=JSON.parse(s).required[0].package;console.log(p.name+"@"+p.version)})')"
echo "library read with that identity: $("$AP" library read @demo/tool@1.0.0 ref/notes.md --store "$ST")"
echo "control, same package as available skill:"
project avail 3 "" tool
"$AP" resolve --root avail "${R[@]}" | grep -o 'Package @demo/tool@1.0.0' | head -1

echo "### Gap 2: update across package names"
project v2 2 tool ""
echo "-- v2 same-name version move (control):"
"$AP" update skills.tool 1.1.0 --root v2 --store "$ST" --model model-a --role worker --host claude 2>&1 | grep -m1 'Selections changed' || true
echo "-- v2 package-qualified target:"
"$AP" update skills.tool @demo/tool-variant@1.0.0 --root v2 --store "$ST" --model model-a --role worker --host claude 2>&1 | head -1 || true
echo "-- v3 same-name move without a release label (documented precondition):"
"$AP" update skills.tool 1.1.0 --root req --store "$ST" --model model-a --role worker --host claude 2>&1 | head -1 || true
