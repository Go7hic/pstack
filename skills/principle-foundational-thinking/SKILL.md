---
name: principle-foundational-thinking
description: "Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Foundational Thinking

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


**Structural decisions** protect option value. **Code-level decisions** protect simplicity. Over-engineering is often a premature decision that closes doors. The right foundational data structure keeps doors open.

**Data structures first.** Get the data shape right before writing logic. The right shape makes downstream code obvious. Define core types early, trace every access pattern, and choose structures that match the dominant paths. A data-structure change late is a rewrite. Early, it is often a one-line diff.

At code level, DRY the structure, not every line. Types and data models should converge. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Test behavior and edge cases, not line counts.

**Concurrency corollary.** Before sharing state between actors, ask "what happens if another actor modifies this concurrently?" If not "nothing", isolate.

**Scaffold first.** If something helps every later phase, do it first. Ask "does every subsequent phase benefit from this existing?" CI, linting, test infrastructure, and shared types are scaffold. Sequence for option value: setup before features, tests before fixes. Keep commits small and single-purpose.

Each increment should land a coherent abstraction or deepen one that exists. Do not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding: remove dead weight first, then lay foundations.
