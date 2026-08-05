# Runtime pointer

Before any multi-agent step, read the sibling **pstack** skill:

1. `pstack/references/capability-contract.md`
2. Matching adapter under `pstack/references/adapters/`:
   - `claude-code.md` — Claude Code (`Agent` / `Task`)
   - `droid.md` — Factory Droid (`Task`)
   - `opencode.md` — OpenCode (`task` → explore/general/…)
   - `codex.md` (+ `codex-models.md`) — OpenAI Codex / replaces codex-pstack
   - `cursor.md` — Cursor (prefer official pstack plugin there)
   - `generic.md` — unknown host (still parallelize if a spawn tool exists)

If the `pstack` skill is missing, use whatever `Agent`/`Task`/`task` tool the host exposes with disjoint scopes; otherwise execute locally.
