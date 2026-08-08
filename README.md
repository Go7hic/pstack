# pstack (portable)

A portable [Agent Skills](https://agentskills.io) distribution of [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (poteto).

It preserves the same engineering system—principles, playbooks, `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, verification, and prose cleanup—without hard-coding one vendor runtime. Thin adapters map capability verbs to Claude Code, Codex, Droid, OpenCode, Cursor, and unknown Agent Skills hosts. Modern hosts keep real parallel subagents; single-agent runtimes degrade explicitly and safely.

## Install

Use this portable pack on Agent Skills-compatible coding agents other than Cursor. Cursor users should keep the official pstack plugin.

```bash
npx skills add https://skills.sh/p/3EVEFJjSrRBr1mI4 -g -s '*' -y
```

See [INSTALL.md](./INSTALL.md) for per-agent selection, model override paths, migration notes, and smoke tests. After global installation, skills usually land under an agent-specific directory such as `~/.claude/skills/`, `~/.codex/skills/`, or the shared `~/.agents/skills/` tree.

## What is included

| Area | Skills and assets |
| --- | --- |
| Entry | `pstack`, `poteto-mode` |
| Workflow | `how`, `why`, `recall`, `blast-radius`, `architect`, `arena`, `swarm`, `interrogate`, `figure-it-out`, `teach`, `reflect`, `automate-me`, `setup-pstack`, `show-me-your-work`, `create-verification-skill`, `maintain-verification-skill`, `tdd`, `typescript-best-practices` |
| Quality | `unslop`, `no-comments`, `technical-writing`, `bro` |
| Principles | all 21 `principle-*` leaf skills |
| Playbooks | 23 mirrored under `skills/poteto-mode/playbooks/` and `skills/pstack/playbooks/` |
| Runtime | `capability-contract.md` plus `generic`, `claude-code`, `codex`, `droid`, `opencode`, and `cursor` adapters |
| Agent rubrics | `skills/pstack/references/agents/{poteto-agent,comment-sicko}.md` |
| Optional | `references/automations/benny`, a Cursor-oriented source pack that is not installed as Agent Skills |

## How portability works

1. Skills express intent with the capability verbs `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, and `model_role`.
2. Before delegation, the lead reads the matching adapter under `skills/pstack/references/adapters/`.
3. The adapter maps those verbs to the host's actual tools, helper types, model controls, and fallback behavior.
4. Parallel fan-out remains the default when the host exposes agent-spawn tools. The workflow collapses to the lead agent only when spawning is missing or denied.
5. `/setup-pstack` resolves role-appropriate models through a host-specific override file. Portable skills must not require Cursor model slugs.
6. The lead agent always owns synthesis, the final patch judgment, and verification on the narrowest meaningful real surface.

The portable layer is an instruction protocol, not an emulator. It preserves workflow intent across hosts, but it cannot manufacture features a host does not expose. A runtime without subagents, model selection, browser control, or persistent modes will use the documented fallback and state the limitation.

## Session and mode behavior

`/poteto-mode` is sticky when the active host supports persistent skill or mode state. On hosts without that lifecycle, treat it as active for the current conversation and invoke it again after a fresh session or a context reset. The engineering rules and playbooks remain portable even when the host cannot provide a native mode flag.

## Maintenance and audits

The repository contains a structural and portability audit:

```bash
python3 scripts/audit_portability.py
python3 scripts/audit_portability.py --strict --changed-from origin/main
```

GitHub Actions runs the structural audit on `main` and on pull requests. It also rejects new vendor leakage in changed files, including concrete Cursor model slugs, Cursor-only tool fields, transcript paths, and drift between mirrored playbooks or adapters.

See [CONTRIBUTING.md](./CONTRIBUTING.md) before syncing a newer upstream revision. Mechanical regex porting is followed by a semantic review; capability verbs must describe the actual job rather than merely replacing vendor vocabulary.

## Not bundled

Upstream poteto-mode references tools that are not part of pstack itself:

- `deslop`, `control-cli`, and `control-ui` from Cursor's `cursor-team-kit`; use equivalent cleanup and runtime-control tools available on the active host.
- Cursor's built-in skill-authoring flow; use the active agent's corresponding authoring or validation workflow.

## Credits

Adapted from pstack by Lauren Tan. See [NOTICE.md](./NOTICE.md) and [LICENSE](./LICENSE) for attribution and MIT licensing.
