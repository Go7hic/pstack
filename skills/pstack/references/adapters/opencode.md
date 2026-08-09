# Adapter: OpenCode

Use inside OpenCode when the task tool can spawn subagents.

## Detect

- task tool for subagent invocation
- built-in read-only and write-capable subagents
- skills under `~/.config/opencode/skills/`, `~/.agents/skills/`, or another configured root

## Capability map

| Capability | How |
| --- | --- |
| `explore` | Use a read-only explorer; use an external-docs scout for dependency research. |
| `implement` | Use a write-capable general agent with disjoint file scope. |
| `review` | Use a read-oriented reviewer with an explicit rubric and edit denial. |
| `parallel` | Issue multiple independent task calls in one turn when the runtime schedules them concurrently. |
| `ask_user` | Use the question tool when available, otherwise plain chat. |
| `verify` | Bash and browser tools on the matching surface. |
| `model_role` | Use confirmed per-agent model configuration or inherit. |

## Policy

- The primary lead owns synthesis, final patch judgment, and verification.
- Do not enable unbounded recursive task permission globally.
- Keep worker write scopes disjoint.
- Hidden custom agents are acceptable for Poteto-style workers.
- Fall back to `generic.md` when task is unavailable or denied.

## Model override file

Prefer `~/.agents/ystack-models.md` and/or OpenCode-native agent model fields. `/setup-ystack` writes the portable override and may mirror roles into host config when the user requests it. Honor `~/.agents/pstack-models.md` as a legacy fallback.

## Poteto worker rubric

An optional OpenCode agent may include `../agents/poteto-agent.md` and be selected for implementation steps.
