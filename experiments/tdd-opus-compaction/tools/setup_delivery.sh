#!/usr/bin/env bash
# apsp-tdd-002 (Opus 5.5 smoke) delivery setup. No model calls.
# Builds, under private/tdd001/ (git-ignored):
#   alias-src/t-k{1,2}/  byte copies of the two packages, renamed to opaque
#                        @apsp-trial aliases with a neutral description
#   store/               a fresh AP 0.19.4 store holding only the aliases
#   consumers/<id>/      two disposable config-v3 consumers (one per arm)
#   key.json             arm <-> alias <-> consumer mapping (never shown to children)
#   trust.trial.yaml     trial-scoped AP trust policy (operator Q5)
# Re-running refuses if private/tdd001/store exists.
set -euo pipefail
R=$(cd "$(dirname "$0")/../../.." && pwd)
P="$R/private/tdd002"
AP_PKG="@guisam/agent-profiles@0.19.4"
SRC_NODE_MODULES="$R/private/consumers/c325a2c/node_modules"   # AP 0.19.4, as in apsp-bs-002
[ -e "$P/store" ] && { echo "refusing: $P/store exists" >&2; exit 1; }
mkdir -p "$P/alias-src" "$P/store" "$P/consumers"

# Random arm -> alias assignment and opaque consumer ids.
read -r K_FULL K_CAND C_FULL C_CAND < <(python -I -c '
import secrets
ks = ["t-k1", "t-k2"]; secrets.SystemRandom().shuffle(ks)
print(ks[0], ks[1], "c" + secrets.token_hex(3), "c" + secrets.token_hex(3))' | tr -d '\r')
# (tr: Windows Python writes CRLF; the first setup run on 2026-11-08 hit this and
#  the consumer directory, package.json and key.json were corrected by hand.)

mkalias() { # $1 alias, $2 source package dir
	local d="$P/alias-src/$1"
	mkdir -p "$d"
	cp "$2/SKILL.md" "$2/writing-good-tests.md" "$2/LICENSE" "$d/"
	cat >"$d/package.yaml" <<EOF
schema_version: 1
package:
  name: "@apsp-trial/$1"
  version: "1.0.0"
  type: skill
  description: "Trial package."
  license: MIT
entrypoint: SKILL.md
behavior:
  delivery: instruction
  hosts: []
  effects: [commands]
EOF
}
mkalias "$K_FULL" "$R/packages/test-driven-development-upstream/7.0.2"
mkalias "$K_CAND" "$R/packages/test-driven-development-opus-5-5/0.1.0"

cat >"$P/trust.trial.yaml" <<'EOF'
# Trial-scoped AP machine policy for the apsp-tdd-001 disposable consumers only.
# Used via AGENT_PROFILES_TRUST; the operator's ~/.agent-profiles/trust.yaml is unchanged.
version: 1
require_approval: false
namespaces: ["@apsp-trial/*"]
effects: [commands]
EOF

AP() { (cd "$1" && shift && AGENT_PROFILES_TRUST="$P/trust.trial.yaml" ./node_modules/.bin/agent-profiles "$@"); }

for a in "$K_FULL" "$K_CAND"; do
	npx --yes "$AP_PKG" add "@apsp-trial/$a@1.0.0" --source "$P/alias-src/$a" --store "$P/store" --json >/dev/null
done

ADAPTER='Agent Profiles delivered the required test-driven-development skill below.
Its supporting file `writing-good-tests.md` is at `../skill/writing-good-tests.md`
relative to the project directory; read it from there when the skill says to.'

mkconsumer() { # $1 id, $2 assignment yaml block
	local c="$P/consumers/$1"
	mkdir -p "$c/.agent-profiles/profiles" "$c/.agent-profiles/roles"
	printf '{"name":"%s","private":true,"devDependencies":{"@guisam/agent-profiles":"0.19.4"}}\n' "$1" >"$c/package.json"
	cp -r "$SRC_NODE_MODULES" "$c/node_modules"
	printf 'Base profile.\n' >"$c/.agent-profiles/profiles/base.md"
	printf '# implementer\n\n%s\n' "$ADAPTER" >"$c/.agent-profiles/roles/implementer.md"
	cat >"$c/.agent-profiles/agents.yaml" <<EOF
version: 3
default_profile: base
default_role: implementer
models:
  claude-sonnet-5-5: {profile: base}
  claude-haiku-5-5: {profile: base}
  claude-opus-5-5: {profile: base}
families: {}
roles:
  implementer:
    file: roles/implementer.md
    skills:
      required: [test-driven-development]
      available: []
skills:
  test-driven-development:
    package: "@apsp-trial/$K_FULL"
    version: "1.0.0"
$2
EOF
	AP "$c" install --offline --store "$P/store" --json >/dev/null
}
mkconsumer "$C_FULL" "assignments: {}"
mkconsumer "$C_CAND" "assignments:
  opus-candidate:
    when: {model: claude-opus-5-5, role: implementer}
    bindings:
      skills.test-driven-development:
        package: \"@apsp-trial/$K_CAND\"
        version: \"1.0.0\""

python -I - "$P/key.json" "$K_FULL" "$K_CAND" "$C_FULL" "$C_CAND" <<'EOF'
import json, sys
p, kf, kc, cf, cc = sys.argv[1:]
json.dump({"full": {"alias": kf, "consumer": cf}, "cand": {"alias": kc, "consumer": cc}},
          open(p, "w"), indent=1)
EOF
echo "setup done: $P"
