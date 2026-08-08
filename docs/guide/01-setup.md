# Set up portable pstack

This page installs the pack, selects role-appropriate models, and runs a small smoke test. The exact installation and delegation tools depend on the active coding agent.

## Install on your coding agent

### Cursor

Use the official Cursor pstack plugin rather than this portable distribution:

```text
/add-plugin pstack
```

The official plugin has native mode metadata and Cursor-specific integrations that the portable pack deliberately does not duplicate.

### Claude Code, Codex, OpenCode, Droid, and other Agent Skills hosts

Install the portable pack globally:

```bash
npx skills add https://skills.sh/p/3EVEFJjSrRBr1mI4 -g -s '*' -y
```

To install only for selected agents, add one or more `-a` flags as described in [INSTALL.md](../../INSTALL.md). Restart or reload the coding agent after installation so it rescans its skill directories.

## Pick models by role

Run:

```text
/setup-pstack
```

[`/setup-pstack`](../../skills/setup-pstack/SKILL.md) detects the models and helper controls exposed by the current host. It then maps available models to roles such as exploration, feature implementation, bug fixing, judgment, and adversarial review.

The override file belongs to the active agent, not to a universal Cursor path:

| Host | Typical override path |
| --- | --- |
| Cursor | `~/.cursor/rules/pstack-models.mdc` |
| Codex | `~/.codex/rules/pstack-models.md` |
| Claude Code or a generic Agent Skills host | `~/.agents/pstack-models.md` or a host-supported user rule |

A role with no override inherits the adapter's default behavior. A value of `inherit-parent` or `auto` tells the adapter to omit an explicit child-model selection and use the parent session model. Panel roles accept a list; the list length controls the number of reviewers or candidates when the host supports parallel helpers.

Never copy model identifiers from another coding agent. `/setup-pstack` writes only model identifiers confirmed by the current host.

## Decide whether to create project verification

At the end of setup, pstack checks whether the project has a repeatable way to exercise the real product surface. That may be a project-local `verify-*` skill, a browser or simulator harness, a CLI check, or another host-specific runtime driver.

When no useful harness exists, setup can route to [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md). The generated skill belongs in the active host's project-local skill directory. Do not assume `.cursor/skills/` outside Cursor.

A verification skill should prove one real workflow before it is accepted. Compilation and unit tests are valuable, but they do not replace checking the behavior on the surface where the original problem appears.

## Run the smoke test

Choose a real but small task:

```text
/pstack add a --json flag to this command. Keep text output byte-identical and verify both paths.
```

You can also invoke `/poteto-mode`. The entry skill should:

1. read the capability contract and the adapter for the current host;
2. create a todo list from the matching playbook;
3. use real parallel helpers when the host exposes them;
4. fall back explicitly to the lead agent when helper spawning is unavailable;
5. verify the result before declaring completion.

For a read-only smoke test, try:

```text
/how explain how configuration reaches the command handler.
```

On a broad subsystem, confirm the adapter fans out several read-only explorers. On a narrow function, a single local pass is expected.

## Understand mode lifetime

Cursor's official plugin can provide native sticky-mode behavior. Other coding agents vary:

- When the host preserves skill state, `/poteto-mode` can remain active across turns in the current conversation.
- When the host does not provide persistent mode state, invoke `/pstack` or `/poteto-mode` again after a new session, context reset, or compaction.
- The playbooks and engineering principles remain the same; only the lifecycle mechanism changes.

Next: [Route work through `/poteto-mode`](./02-poteto-mode.md).
