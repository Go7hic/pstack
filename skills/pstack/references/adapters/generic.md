# Adapter: generic

Default when the runtime is unknown, **or** as the fallback when a named adapter’s spawn tool is missing.

Modern coding agents usually expose a subagent/Task/Agent/`task` tool. Prefer a named adapter when you can identify the host. If you only see a generic spawn tool, use the **detect-and-parallel** rules below instead of collapsing immediately.

## Detect-and-parallel

If any of these exist, treat `parallel` as available:

- Tool named `Agent`, `Task`, or `task` that spawns a helper session
- Documented subagent types (explore / general / worker / etc.)

Then:

1. Map `explore` → read-only helper (forbid edits in the prompt if no explore type exists)
2. Map `implement` → write-capable helper with a bounded file list
3. Map `review` → read-only helper with an explicit rubric
4. Map `parallel` → **multiple spawn calls in one turn** for independent slices; disjoint write scopes
5. If spawn fails or is denied mid-run, finish remaining slices on the main agent and say so

Only when **no** spawn tool exists should you fully collapse to single-threaded local work.

## Capability map (no spawn tool)

| Capability | How |
| --- | --- |
| `explore` | Main agent: search, read files, trace call chains |
| `implement` | Main agent edits. Keep diffs small and scoped |
| `review` | Main agent reviews with an explicit rubric; optional second pass |
| `parallel` | Sequential. Note: `collapsed parallel explore into local pass` |
| `ask_user` | Plain-language question. Product/preference only |
| `verify` | Narrowest local command |
| `model_role` | Ignore / stay on current model |

## Policy

- Never invent Cursor-, Codex-, Claude-, Droid-, or OpenCode-specific JSON when those tools are absent.
- Prefer naming which adapter you selected when you start multi-step work.
