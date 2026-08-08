---
name: bro
description: "Restate the last message in plain human language, with no jargon."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before any helper delegation.
2. Prefer capability verbs (`explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`) over vendor tool names.
3. Resolve models through `model_role`. Never require a vendor-specific model identifier.
4. When helper spawning is unavailable, run the work on the lead agent and state that fan-out was collapsed.

Restate your last message. Stop using jargon and speak coherently. State it more simply and concisely, like one human talking to another.
