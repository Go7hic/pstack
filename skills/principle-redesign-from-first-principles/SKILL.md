---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Redesign From First Principles

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before any helper delegation.
2. Prefer capability verbs (`explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`) over vendor tool names.
3. Resolve models through `model_role`. Never require a vendor-specific model identifier.
4. When helper spawning is unavailable, run the work on the lead agent and state that fan-out was collapsed.

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start. The result should look like what we would have built if we'd known on day one.

- Read all affected files and understand the current design holistically
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the redesign holistically, then deliver it incrementally

This is the method for preserving option value when integrating changes into an existing design.
