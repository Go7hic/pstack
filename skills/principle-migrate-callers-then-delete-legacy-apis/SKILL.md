---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Migrate Callers Then Delete Legacy APIs

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


When we decide a new API is the right design, migrate callers and remove the old API in the same refactor wave instead of preserving compatibility layers.

**Rule:**
- Do not keep legacy API paths alive only because internal callers still exist
- Inventory callers, migrate them, and delete the old API immediately
- Treat temporary adapters as exceptional and time-boxed, not default architecture
- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative

Keeping both old and new APIs creates dual-path complexity, slows cleanup, and makes the codebase feel append-only.
