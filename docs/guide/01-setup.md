# Set up ystack

This page installs the pack, selects role-appropriate models, and runs a small smoke test. The exact installation and delegation tools depend on the active coding agent.

## Install on your coding agent

Install ystack globally on Claude Code, Codex, OpenCode, Droid, Cursor, or another Agent Skills host:

```bash
npx skills add Go7hic/ystack -g -s '*' -y
```

The complete pack is recommended because `/ystack` coordinates sibling skills and shared runtime assets. To install only for selected agents, add one or more `-a` flags as described in [INSTALL.md](../../INSTALL.md). Restart or reload the coding agent afterward so it rescans its skill directories.

On Cursor, choose between ystack and the official pstack plugin as your top-level router. Do not enable both mode systems simultaneously.

## Pick models by role

Run:

```text
/setup-ystack
```

[`/setup-ystack`](../../skills/setup-ystack/SKILL.md) detects the models and helper controls exposed by the current host. It maps available models to exploration, feature implementation, bug fixing, judgment, and adversarial-review roles.

The override file belongs to the active agent:

| Host | Preferred override path | Legacy fallback |
| --- | --- | --- |
| Cursor | `~/.cursor/rules/ystack-models.mdc` | `pstack-models.mdc` |
| Codex | `~/.codex/rules/ystack-models.md` | `pstack-models.md`, then `codex-pstack-models.md` |
| Claude Code or generic | `~/.agents/ystack-models.md` or a host-supported rule | `~/.agents/pstack-models.md` |

A role with no override inherits the adapter's default behavior. `inherit-parent` or `auto` tells the adapter to omit explicit child-model selection. Panel lists control reviewer or candidate count when the host supports parallel helpers.

Never copy model identifiers from another coding agent. `/setup-ystack` writes only identifiers confirmed by the current host.

## Decide whether to create project verification

At the end of setup, ystack checks whether the project has a repeatable way to exercise the real product surface. That may be a project-local `verify-*` skill, browser or simulator harness, CLI check, or another host-specific runtime driver.

When no useful harness exists, setup can route to [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md). The generated skill belongs in the active host's project-local skill directory.

A verification skill should prove one real workflow before it is accepted. Compilation and unit tests are valuable, but they do not replace checking behavior on the surface where the original problem appears.

## Run the smoke test

Choose a real but small task:

```text
/ystack add a --json flag to this command. Keep text output byte-identical and verify both paths.
```

You can also invoke `/poteto-mode`; `/pstack` remains a compatibility alias. The entry skill should:

1. read the capability contract and adapter for the current host;
2. create a todo list from the matching playbook;
3. use real parallel helpers when available;
4. fall back explicitly when helper spawning is unavailable;
5. verify the result before declaring completion.

For a read-only smoke test:

```text
/how explain how configuration reaches the command handler.
```

On a broad subsystem, confirm the adapter fans out several read-only explorers. On a narrow function, a single local pass is expected.

## Understand mode lifetime

See `skills/pstack/references/host-lifecycle.md` for the current compatibility runtime matrix.

- When the host preserves skill state, `/poteto-mode` can remain active across turns in the current conversation.
- Otherwise invoke `/ystack` or `/poteto-mode` again after a new session, context reset, or compaction.
- Never claim sticky mode on a host that cannot enforce it.

Next: [Route work through `/poteto-mode`](./02-poteto-mode.md).
