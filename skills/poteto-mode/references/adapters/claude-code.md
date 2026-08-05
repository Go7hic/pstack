# Adapter: Claude Code

Use inside [Claude Code](https://code.claude.com) when the `Agent` tool is available (older builds may still expose it as `Task` — treat them as the same capability).

## Detect

- Tools named `Agent` or `Task` for spawning subagents
- Skills loaded from `~/.claude/skills/` or `.claude/skills/`
- Built-in subagent types such as `Explore`, `Plan`, `general-purpose`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `Agent` / `Task` with `subagent_type: Explore` (or equivalent explore agent). Prefer thoroughness `medium` unless the slice is tiny (`quick`) or broad (`very thorough`). Read-only; do not edit. |
| `implement` | `Agent` / `Task` with `subagent_type: general-purpose` (or a custom worker). Pass disjoint file scopes. Optionally `isolation: "worktree"` when the runtime supports it and writes would collide. |
| `review` | Separate `Agent` calls with distinct rubrics/models. Prefer read-only tools / deny edits in the prompt. |
| `parallel` | Emit **multiple** `Agent`/`Task` calls in **one** assistant turn. Independent slices only. Use `run_in_background: true` when available and the parent continues non-overlapping work; collect with the runtime’s task-output mechanism if needed. |
| `ask_user` | Plain chat (or Claude’s question UI if present). Facts you can observe → do not ask. |
| `verify` | Bash / browser tools on the matching surface. Prefer the narrowest meaningful command. |
| `model_role` | Pass `model` on the Agent call when the override file names a confirmed slug. Otherwise omit and inherit. Explore often inherits/caps — do not fight the runtime. |

## Policy

- Lead agent owns synthesis, final patch judgment, and verification.
- Do not trust subagent “done” summaries; read the diff / returned paths.
- Keep worker write scopes disjoint. Tell workers not to revert others’ edits.
- Respect spawn / concurrent subagent limits; if spawn fails, finish remaining work locally or sequentially.
- Nested subagents: prefer shallow fan-out from the lead. Do not build deep trees unless the playbook requires it.
- If `Agent`/`Task` is missing, fall back to `generic.md`.

## Model override file

Prefer `~/.agents/pstack-models.md` or a Claude user rule. `/setup-pstack` should write beside the active agent.

## Poteto worker rubric

When a playbook wants a full-style worker, spawn `general-purpose` (or a custom droid/agent you configured) and prepend instructions from `../agents/poteto-agent.md`.
