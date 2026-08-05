# Adapter: Droid (Factory)

Use inside [Factory Droid](https://docs.factory.ai/harness/subagents) when the `Task` tool can spawn subagents / custom droids.

## Detect

- `Task` tool with `subagent_type`, `run_in_background`, `resume`, `complexity`
- Skills under `~/.factory/skills/` or `.factory/skills/`
- Optional custom droids under `~/.factory/droids/` or `.factory/droids/`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `Task` with a read-only custom droid if you have one, otherwise the default research/read-oriented subagent. Explicitly forbid edits in the prompt. Prefer `complexity: light` or `medium` for exploration. |
| `implement` | `Task` with a coding subagent / general droid. Bounded file scope. Use `complexity: medium` or `heavy` for hard fixes. Disjoint write scopes across workers. |
| `review` | Separate `Task` reviewers with distinct rubrics. Prefer read-only tool policy on review droids. |
| `parallel` | Multiple `Task` calls in one turn, and/or `run_in_background: true` then collect with `TaskOutput`. Independent slices only. |
| `ask_user` | Plain chat. Only product/preference forks. |
| `verify` | Execute / browser tools on the matching surface. Narrowest meaningful check. |
| `model_role` | Prefer `complexity` routing when it maps to your settings; otherwise set an explicit model if the Task API allows it and the slug is confirmed. |

## Policy

- Lead droid owns synthesis, final patch judgment, and verification.
- Background tasks: track `task_id`, wait via `TaskOutput`, stop via `TaskStop` when abandoning work.
- `resume` only when continuing the same helper’s context beats a fresh spawn.
- Keep write scopes disjoint across parallel Tasks.
- Large multi-feature campaigns may use Factory Missions when available; still apply pstack playbook gates (verify, prove-it-works).
- If `Task` is missing, fall back to `generic.md`.

## Model override file

`~/.agents/pstack-models.md` or a Factory-side rule written by `/setup-pstack`.

## Poteto worker rubric

Optional: add a custom droid whose system prompt includes `../agents/poteto-agent.md`, then target it as `subagent_type` for playbook implementation steps.
