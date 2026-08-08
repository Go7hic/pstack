# Runtime pointer

Before any multi-agent step, read the sibling **pstack** skill:

1. `pstack/references/capability-contract.md`
2. The matching adapter under `pstack/references/adapters/` for the active host (`claude-code`, `codex`, `droid`, `opencode`, `cursor`, or `generic`).

Map capability verbs through that adapter. Do not invent tool parameters from another host. If spawning is unavailable, execute on the lead agent and say so.

