# Install

Use this portable pack on every Agent Skills–compatible coding agent **except** Cursor (keep Cursor’s official pstack plugin there).

## Recommended: GitHub global install

```bash
npx skills add Go7hic/pstack -g -s '*' -y
```

Add `-a` for specific agents if you do not want every discovered agent:

```bash
npx skills add Go7hic/pstack -g \
  -a claude-code -a codex -a opencode -a factory-droid \
  -s '*' -y
```

`-g` installs into each agent’s **global** skills directory (not the current project), for example:

| Agent | Typical global skills dir |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` and/or `~/.agents/skills/` |
| Droid (Factory) | `~/.factory/skills/` |
| Generic / shared | `~/.agents/skills/` |

After install, restart or reload the agent so it rescans skills.

## Optional: skills.sh pack URL

If you already have a published skills.sh pack for this repo, you can install from that URL instead. Prefer the GitHub install above when the pack page is stale or the URL does not resolve to a valid skill archive.

```bash
# Replace with your current pack URL only after confirming it installs cleanly.
npx skills add https://skills.sh/p/<pack-id> -g -s '*' -y
```

## Optional: wire more agents from the install tree

If the CLI already installed into one global tree and you need another agent that was not selected, symlink from that install location (not from this git checkout):

```bash
# After a global install, the shared tree is usually:
SRC=~/.agents/skills
# If your install only landed under one agent, point SRC there instead, e.g.:
# SRC=~/.claude/skills

# Droid
mkdir -p ~/.factory/skills
ln -sfn "$SRC"/* ~/.factory/skills/

# OpenCode
mkdir -p ~/.config/opencode/skills
ln -sfn "$SRC"/* ~/.config/opencode/skills/

# Codex (if not installed via -a codex)
mkdir -p ~/.codex/skills
ln -sfn "$SRC"/* ~/.codex/skills/
```

Do **not** use `~/workspace/pstack/skills` as `SRC` unless you are developing this repo itself.

### Codex cutover checklist

1. Prefer `npx skills add Go7hic/pstack -g -a codex` (or symlink from `SRC` above).
2. Delete the old pack if present: `rm -rf ~/.codex/skills/codex-pstack`
3. Point model overrides at `~/.codex/rules/pstack-models.md` (see `adapters/codex-models.md`).
4. Smoke-test: `/pstack` or `/how` and confirm the agent reads `adapters/codex.md` and spawns via `multi_agent_v1` (or current Codex multi-agent tools).

## Adapter selection

| Host | Adapter |
| --- | --- |
| Cursor | official plugin — do **not** rely on this pack |
| Claude Code | `skills/pstack/references/adapters/claude-code.md` |
| Droid | `skills/pstack/references/adapters/droid.md` |
| OpenCode | `skills/pstack/references/adapters/opencode.md` |
| Codex | `skills/pstack/references/adapters/codex.md` |
| Unknown | `generic.md` (auto-uses spawn tools when present) |

## Smoke test

In each agent:

```text
/pstack   (or /poteto-mode)
fix a tiny reproducible issue in this repo, or explain how X works with /how
```

Confirm it reads the matching adapter and, for arena/how-complex, actually fans out subagents.

## Developing this repo

Local checkout only when editing the pack:

```bash
SRC=~/workspace/pstack/skills   # or your clone path
```

Day-to-day use should go through the GitHub install path above.
