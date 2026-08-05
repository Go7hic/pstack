# Adapter: OpenCode

Use inside [OpenCode](https://opencode.ai/docs/agents/) when the `task` tool can spawn subagents.

## Detect

- `task` tool for subagent invocation
- Built-in subagents: `general` (parallel multi-step / can edit), `explore` (fast read-only), `scout` (external docs / deps, read-only)
- Skills under `~/.config/opencode/skills/`, `~/.agents/skills/`, or `~/.claude/skills/`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `task` → subagent `explore` (read-only). Use `scout` when the slice is upstream docs/deps rather than the local tree. |
| `implement` | `task` → subagent `general` (or a custom write-capable subagent). Disjoint file scopes across workers. |
| `review` | `task` → read-oriented subagent / custom reviewer with `edit: deny`. Distinct rubrics per reviewer. |
| `parallel` | Issue **multiple** `task` calls for independent slices in one turn when the runtime schedules them concurrently. If the host serializes `task`, still issue the batch as separate tasks and note sequential execution; do not invent a fake parallel API. |
| `ask_user` | Prefer OpenCode `question` tool when available; else plain chat. Facts you can observe → do not ask. |
| `verify` | `bash` / browser tools. Narrowest meaningful check. |
| `model_role` | Set per-subagent `model` in agent config or task override when confirmed available (`provider/model-id`). Otherwise inherit. |

## Policy

- Lead (primary Build/Plan) owns synthesis, final patch judgment, and verification.
- Do not enable unbounded recursive `permission.task` on every subagent globally — prefer task permission on the primary only, or specific subagent patterns.
- Keep worker write scopes disjoint.
- Hidden custom subagents are fine for programmatic poteto-style workers.
- If `task` is denied or missing, fall back to `generic.md`.

## Model override file

`~/.agents/pstack-models.md` and/or OpenCode agent model fields. `/setup-pstack` should write the portable override and optionally mirror role models into `opencode.json` agent entries when the user wants sticky per-agent models.

## Poteto worker rubric

Create an optional OpenCode subagent (markdown under `~/.config/opencode/agents/`) whose prompt includes `../agents/poteto-agent.md`, then `task` that agent for playbook implementation steps.
