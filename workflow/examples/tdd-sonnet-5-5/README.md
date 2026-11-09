# Example: TDD for `claude-sonnet-5-5` (opt-in beta, not adopted)

| File | Purpose |
| --- | --- |
| `IDENTITIES.json` | Upstream commit and blob IDs, per-file sha256, AP 0.19.4 digests for both packages |
| `CHANGE-MAP.md` | Each edit → preserved requirement → pre-run evidence → stage-1 behavioral evidence |
| `consumer/.agent-profiles/` | AP config v3: baseline default plus one exact-model, one-role assignment |
| `agents.rollback.yaml` | The same config with no assignment (rollback) |
| `trust.example.yaml` | Trial-scoped AP trust policy, passed with `AGENT_PROFILES_TRUST` |
| `routing.json` | Expected package per model, used by `verify_delivery.py` |
| `campaign.example.json` | The stage-1 configuration as a campaign definition |
| `delivery-report.json` | Output of `verify_delivery.py` on AP 0.19.4 (`ok: true`) |

## Try it (no model calls)

From the repository root:

```sh
python -I workflow/tools/verify_delivery.py workflow/examples/tdd-sonnet-5-5   # uses npx @guisam/agent-profiles@0.19.4
python -I workflow/tools/check_package.py packages/test-driven-development-sonnet-5-5/0.1.0 \
  --compare packages/test-driven-development-upstream/7.0.2
python -I workflow/tools/campaign.py check workflow/examples/tdd-sonnet-5-5/campaign.example.json
```

## Use it in a real project (opt-in)

1. Import both package directories into your store:
   ```sh
   agent-profiles add @apsp/test-driven-development-upstream@7.0.2 --source packages/test-driven-development-upstream/7.0.2
   agent-profiles add @apsp/test-driven-development-sonnet-5-5@0.1.0 --source packages/test-driven-development-sonnet-5-5/0.1.0
   ```
2. Add the `skills` binding and the single `assignments` block from
   `consumer/.agent-profiles/agents.yaml` to your config, then run
   `agent-profiles install`.
3. Confirm the routing with `resolve --json`. `required[].backing.sha256`
   should be `bd446f96…` for `claude-sonnet-5-5` and `ce680b8a…` for every
   other model.
4. **Rollback:** remove the assignment (see `agents.rollback.yaml`), run
   `install`, and resolve again.
