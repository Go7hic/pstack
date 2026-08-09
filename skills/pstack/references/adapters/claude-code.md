# Adapter: Claude Code

Use inside [Claude Code](https://code.claude.com) when the `Agent` tool is available. Older builds may expose it as `Task`; treat both as the same capability.

## Detect

- Tools named `Agent` or `Task` for spawning subagents
- Skills loaded from `~/.claude/skills/` or `.claude/skills/`
- Built-in subagent types such as `Explore`, `Plan`, `general-purpose`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `Agent` / `Task` with `subagent_type: Explore` or an equivalent read-only agent. |
| `implement` | `Agent` / `Task` with `subagent_type: general-purpose` or a custom worker. Pass disjoint file scopes. |
| `review` | Separate calls with distinct rubrics/models. Deny edits in the prompt. |
| `parallel` | Emit multiple `Agent` / `Task` calls in one assistant turn for independent slices. Use background execution only when supported. |
| `ask_user` | Plain chat or the host's question UI. Do not ask for observable facts. |
| `verify` | Bash and browser tools on the matching surface. |
| `model_role` | Pass `model` only when an override names a confirmed slug; otherwise inherit. |

## Policy

- The lead owns synthesis, final patch judgment, and verification.
- Do not trust helper completion summaries without reading the diff or artifacts.
- Keep worker write scopes disjoint.
- Prefer shallow fan-out from the lead.
- Fall back to `generic.md` when spawning is unavailable.

## Model override file

Prefer `~/.agents/ystack-models.md` or a Claude user rule written by `/setup-ystack`. If absent, honor `~/.agents/pstack-models.md` as a legacy fallback. `/setup-pstack` is an alias for the new setup skill.

## Poteto worker rubric

When a playbook wants a full-style worker, spawn `general-purpose` or a configured custom agent and prepend `../agents/poteto-agent.md`.
