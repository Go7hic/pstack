# Install

Use this portable pack on every Agent Skills–compatible coding agent **except** Cursor (keep Cursor’s official pstack plugin there).

## One source, many agents

```bash
SRC=~/workspace/pstack/skills

# Claude Code (+ OpenCode Claude-compatible path)
mkdir -p ~/.claude/skills
ln -sfn "$SRC"/* ~/.claude/skills/

# Droid (Factory)
mkdir -p ~/.factory/skills
ln -sfn "$SRC"/* ~/.factory/skills/

# OpenCode / generic Agent Skills
mkdir -p ~/.agents/skills
ln -sfn "$SRC"/* ~/.agents/skills/
mkdir -p ~/.config/opencode/skills
ln -sfn "$SRC"/* ~/.config/opencode/skills/

# Codex (replaces ~/.codex/skills/codex-pstack)
mkdir -p ~/.codex/skills
ln -sfn "$SRC"/* ~/.codex/skills/
# Remove the old single-skill pack so it does not shadow this one:
rm -rf ~/.codex/skills/codex-pstack
# Optional: migrate model overrides
# mv ~/.codex/rules/codex-pstack-models.md ~/.codex/rules/pstack-models.md
```

### Codex cutover checklist

1. Symlink this pack into `~/.codex/skills/` (above).
2. Delete `~/.codex/skills/codex-pstack` so descriptions do not compete.
3. Point model overrides at `~/.codex/rules/pstack-models.md` (see `adapters/codex-models.md`).
4. Smoke-test: `/pstack` or `/how` and confirm the agent reads `adapters/codex.md` and spawns via `multi_agent_v1` (or current Codex multi-agent tools).

After linking, restart or reload the agent so it rescans skills.

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
