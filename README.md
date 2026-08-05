# pstack (portable)

Full portable [Agent Skills](https://agentskills.io) pack adapted from [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (poteto).

Same engineering system — principles, playbooks, how/why/architect/arena/swarm/interrogate, verification, unslop — without hard-coding one vendor runtime. Thin adapters map capabilities to Claude Code, Droid, OpenCode, Codex, and others; parallel subagents are the default on modern hosts.

## Install

See **[INSTALL.md](./INSTALL.md)** for per-agent symlinks (Claude Code, Droid, OpenCode, Codex). Keep Cursor on the official pstack plugin.

After the repo is on GitHub:

```bash
npx skills add <owner>/pstack -g
```

Until then, symlink from the repo (example for Claude Code):

```bash
mkdir -p ~/.claude/skills
ln -sfn ~/workspace/pstack/skills/* ~/.claude/skills/
```

## What’s included

| Area | Skills / assets |
| --- | --- |
| Entry | `pstack`, `poteto-mode` |
| Workflow | `how`, `why`, `recall`, `blast-radius`, `architect`, `arena`, `swarm`, `interrogate`, `figure-it-out`, `teach`, `reflect`, `automate-me`, `setup-pstack`, `show-me-your-work`, `create-verification-skill`, `maintain-verification-skill`, `tdd`, `typescript-best-practices` |
| Quality | `unslop`, `no-comments`, `technical-writing`, `bro` |
| Principles | all 21 `principle-*` leaf skills |
| Playbooks | 23 under `skills/pstack/playbooks` and `skills/poteto-mode/playbooks` |
| Runtime | `capability-contract.md` + adapters: `generic`, `claude-code`, `droid`, `opencode`, `codex`, `cursor` |
| Agent rubrics | `skills/pstack/references/agents/{poteto-agent,comment-sicko}.md` |
| Optional | `references/automations/benny` (Cursor-oriented, not a skill) |

## How portability works

1. Skills speak in capability verbs: `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`.
2. Before delegation, read the matching adapter under `pstack/references/adapters/` (`claude-code`, `droid`, `opencode`, `codex`, …).
3. Prefer real subagent fan-out (`parallel`) on modern hosts. Collapse only when spawn tools are missing or denied.
4. Model slugs are resolved via `/setup-pstack` overrides + `model_role`, not hard-required Cursor defaults.

## Not bundled (same as upstream)

Upstream poteto-mode references these but does not ship them in pstack:

- `deslop`, `control-cli`, `control-ui` (Cursor `cursor-team-kit`) — use local equivalents
- Cursor built-in `/create-skill` — use your agent’s skill authoring flow

## Credits

Adapted from pstack by Lauren Tan. See `NOTICE.md` and `LICENSE` (MIT).
