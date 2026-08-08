# Host lifecycle matrix

Mode and session persistence are host properties. Portable skills must not claim a stronger guarantee than the active adapter documents.

| Host | Current turn | Current conversation | After compaction / summarize | New session |
| --- | --- | --- | --- | --- |
| Claude Code | Active skill instructions apply | Usually sticky within the conversation when the skill remains selected | Re-invoke `/pstack` or `/poteto-mode` if the mode contract is no longer visible | Re-invoke; do not assume sticky mode |
| Codex | Active skill instructions apply | Sticky only while the skill remains in context / selected | Re-invoke after major context loss | Re-invoke; load overrides from `~/.codex/rules/` if configured |
| OpenCode | Active skill instructions apply | Sticky within the open session when skills stay loaded | Re-invoke if compacted away | Re-invoke |
| Droid / Factory | Active skill instructions apply | Sticky while the droid/session keeps the skill | Re-invoke after reset | Re-invoke |
| Cursor (official plugin preferred) | Plugin/mode facilities may persist | May be sticky via Cursor mode/skill state | Follow Cursor mode lifecycle; this portable pack is not the primary path | Prefer official plugin |
| Generic with spawn | Active skill instructions apply | Conversation-scoped only | Re-invoke | Re-invoke |
| Generic without spawn | Same as generic with spawn, but helpers collapse to the lead | Conversation-scoped only | Re-invoke | Re-invoke |

## Recovery without hidden memory

Session pickup must prefer, in order:

1. user-supplied handoff or decision trail;
2. repository state, branches, PRs, commits;
3. host-exposed current-session resources;
4. an explicit transcript path or URL for this task;
5. a compact lead digest.

Never scan broad history directories to guess the active conversation. Never claim sticky mode on a host that cannot enforce it.
