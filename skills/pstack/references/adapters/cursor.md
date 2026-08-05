# Adapter: Cursor

Use inside Cursor Agent when Task / subagent tools are available.

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `Task` with a read-only explorer prompt. Prefer `subagent_type: explore` or `generalPurpose` with an explicit no-edit rule. |
| `implement` | `Task` with `generalPurpose` (or a project poteto-style worker if configured). Disjoint file scopes across workers. |
| `review` | Separate `Task` reviewers with distinct rubrics/models when diversity helps. |
| `parallel` | Multiple `Task` calls in one assistant message. `run_in_background: true` when the parent continues non-overlapping work. |
| `ask_user` | Prefer a structured question UI if present; otherwise ask in chat. Facts you can observe → do not ask. |
| `verify` | Shell / browser / IDE tools on the matching surface. |
| `model_role` | Optional Task `model` override from user setup. If unset, omit `model` and inherit. |

## Policy

- Lead agent owns synthesis, the final patch judgment, and verification.
- Do not treat subagent "done" summaries as ground truth; read the diff.
- If Task is unavailable, fall back to `generic.md` immediately.

## Do not import from upstream Cursor pstack

- Hard-coded Cursor-only model slug tables as required defaults
- `poteto-agent` as a mandatory subagent type (use it only if the user's Cursor install provides it)
- Plugin frontmatter (`mode:`, `icon:`, `disable-model-invocation`) as portable skill requirements
