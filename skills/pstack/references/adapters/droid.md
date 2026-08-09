# Adapter: Droid (Factory)

Use inside Factory Droid when the Task tool can spawn subagents or custom droids.

## Detect

- Task tool with helper, background, resume, and complexity controls
- Skills under `~/.factory/skills/` or `.factory/skills/`
- Optional custom droids under `~/.factory/droids/` or `.factory/droids/`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | Use a read-oriented helper and explicitly forbid edits. |
| `implement` | Use a coding helper with bounded file scope and appropriate complexity. |
| `review` | Separate reviewers with distinct rubrics and read-only policy. |
| `parallel` | Issue multiple independent Tasks and collect through the host's task-output mechanism. |
| `ask_user` | Plain chat for product or preference forks only. |
| `verify` | Execute or browser tools on the matching surface. |
| `model_role` | Prefer supported complexity routing or a confirmed explicit model. |

## Policy

- The lead droid owns synthesis, final patch judgment, and verification.
- Track background task identifiers and stop abandoned work.
- Resume only when preserving the same helper context is valuable.
- Keep parallel write scopes disjoint.
- Missions may coordinate broad campaigns, but ystack verification gates still apply.
- Fall back to `generic.md` when Task is unavailable.

## Model override file

Prefer `~/.agents/ystack-models.md` or a Factory-side rule written by `/setup-ystack`. Honor `~/.agents/pstack-models.md` as a legacy fallback.

## Poteto worker rubric

A custom droid may include `../agents/poteto-agent.md` and be used for playbook implementation steps.
