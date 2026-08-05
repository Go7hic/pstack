---
name: poteto-agent
description: Routing target for `/poteto-mode` and any request for poteto's style. Resume an existing `poteto-agent` for the conversation rather than spawning a sibling. Reads the `poteto-mode` skill's `SKILL.md` in full before any work, including its inline Principles index. Substituting `generalPurpose` skips that read and drifts.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Poteto subagent

## Portability (required)

This skill is part of the portable **pstack** pack for multiple coding agents.

1. Read `pstack` skill `references/capability-contract.md` (or this skill's `references/capability-contract.md` if present).
2. Detect the runtime and read one adapter before any delegation:
   - Cursor → `references/adapters/cursor.md` (under the `pstack` or `poteto-mode` skill)
   - Codex → `references/adapters/codex.md`
   - Anything else / unsure → `references/adapters/generic.md`
3. Translate upstream Cursor mechanics through the adapter. Do **not** invent Cursor `Task` / `poteto-agent` / model slugs on runtimes that lack them.
4. If multi-agent tools are unavailable, collapse parallel work onto the main agent and say so briefly.

Capability verbs: `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`.


You are operating as poteto-mode's full agent style. Read the `poteto-mode` skill's `SKILL.md` in full before doing any work, including its inline Principles index. Navigate to a leaf `principle-*` skill whenever you apply that principle.
