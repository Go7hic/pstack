# Install ystack

ystack supports Agent Skills-compatible coding agents, including Claude Code, Codex, OpenCode, Droid, generic Agent Skills hosts, and Cursor through the included adapter.

If Cursor's official pstack plugin is already enabled, do not also activate ystack as a competing top-level router in the same session. Choose one router, or keep ystack on your non-Cursor agents.

## Recommended: global install

Install the complete pack because `/ystack` coordinates sibling skills and the shared compatibility runtime tree:

```bash
npx skills add Go7hic/ystack -g -s '*' -y
```

Add `-a` for specific agents when you do not want every discovered agent:

```bash
npx skills add Go7hic/ystack -g \
  -a claude-code -a codex -a opencode -a factory-droid \
  -s '*' -y
```

`-g` installs into each agent's global skills directory, for example:

| Agent | Typical global skills dir |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` and/or `~/.agents/skills/` |
| Droid (Factory) | `~/.factory/skills/` |
| Generic / shared | `~/.agents/skills/` |

After installation, restart or reload the agent so it rescans skills.

## Public commands and compatibility

Prefer:

```text
/ystack
/setup-ystack
```

The legacy commands remain available:

```text
/pstack
/setup-pstack
```

They route to the ystack workflow so existing prompts and installations continue to work.

## Model override migration

`/setup-ystack` writes the preferred ystack-named override file for the active host:

| Host | Preferred path | Legacy fallback |
| --- | --- | --- |
| Cursor | `~/.cursor/rules/ystack-models.mdc` | `~/.cursor/rules/pstack-models.mdc` |
| Codex | `~/.codex/rules/ystack-models.md` | `~/.codex/rules/pstack-models.md`, then `codex-pstack-models.md` |
| Claude Code / generic | `~/.agents/ystack-models.md` or a host rule | `~/.agents/pstack-models.md` |
| Droid / OpenCode | preferred shared file or host-native agent config | legacy shared file |

Existing legacy files are read as fallback. Re-running `/setup-ystack` writes the new path; it does not silently delete the old file.

## Optional: wire more agents from one install tree

If the CLI already installed into one global tree and you need another agent that was not selected, symlink from that install location, not from this git checkout:

```bash
SRC=~/.agents/skills
# If installation landed under one agent only, point SRC there instead.

mkdir -p ~/.factory/skills
ln -sfn "$SRC"/* ~/.factory/skills/

mkdir -p ~/.config/opencode/skills
ln -sfn "$SRC"/* ~/.config/opencode/skills/

mkdir -p ~/.codex/skills
ln -sfn "$SRC"/* ~/.codex/skills/
```

Do not use `~/workspace/ystack/skills` as `SRC` unless you are developing this repository itself.

### Codex cutover checklist

1. Install with `npx skills add Go7hic/ystack -g -a codex -s '*' -y`.
2. Delete the obsolete standalone pack if present: `rm -rf ~/.codex/skills/codex-pstack`.
3. Run `/setup-ystack` and prefer `~/.codex/rules/ystack-models.md`.
4. Smoke-test `/ystack` or `/how` and confirm the Codex adapter uses current multi-agent tools.

## Adapter selection

The runtime assets currently live under the legacy compatibility namespace while the public project name is ystack:

| Host | Adapter |
| --- | --- |
| Cursor | `skills/pstack/references/adapters/cursor.md` |
| Claude Code | `skills/pstack/references/adapters/claude-code.md` |
| Droid | `skills/pstack/references/adapters/droid.md` |
| OpenCode | `skills/pstack/references/adapters/opencode.md` |
| Codex | `skills/pstack/references/adapters/codex.md` |
| Unknown | `generic.md` |

## Smoke test

In each agent:

```text
/ystack add a --json flag to this command. Keep text output byte-identical and verify both paths.
```

You can also invoke `/poteto-mode`. Confirm that the entry skill:

1. reads the capability contract and matching adapter;
2. creates a todo list from the matched playbook;
3. uses real parallel helpers when the host exposes them;
4. falls back explicitly when spawning is unavailable;
5. verifies the result before declaring completion.

## Developing this repository

Use a local checkout only when editing ystack:

```bash
SRC=~/workspace/ystack/skills   # or your clone path
```

Day-to-day use should go through the GitHub installation path above.
