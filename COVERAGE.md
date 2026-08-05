# Coverage

This pack aims for **full upstream pstack capability coverage**, ported to Agent Skills + adapters.

## Skills (45)

All upstream skills under `skills/` plus the portable hub `pstack`.

## Playbooks (23)

Mirrored in `skills/poteto-mode/playbooks/` and `skills/pstack/playbooks/`.

## Intentionally adapted (not 1:1 Cursor runtime)

| Upstream | Portable treatment |
| --- | --- |
| `Task` / `subagent_type` | capability verbs + per-host adapters (parallel by default on modern agents) |
| Claude Code `Agent`/`Task` | `adapters/claude-code.md` (`Explore`, `general-purpose`, multi-spawn one turn) |
| Droid `Task` + custom droids | `adapters/droid.md` (`run_in_background` / `TaskOutput`) |
| OpenCode `task` | `adapters/opencode.md` (`explore` / `general` / `scout`) |
| Codex multi-agent | `adapters/codex.md` |
| `poteto-agent` / Comment Sicko types | rubric markdown under `pstack/references/agents/` |
| Cursor model slugs | `model_role` + setup-pstack override file |
| `AskQuestion` | `ask_user` |
| `/loop` | long-run/loop if available, else continue |
| `watch-pr` scripts | optional; babysit falls back to `gh` |
| poteto-mode `scripts/` (orch, watch-pr) | omitted from pack copy (Cursor tooling); playbooks note fallbacks |
| benny automations | kept under `references/automations/benny/skill-templates/` as `INSTRUCTIONS.md` (not discoverable by `npx skills add`) |

## External (never in upstream pstack either)

`deslop`, `control-cli`, `control-ui` from `cursor-team-kit`.
