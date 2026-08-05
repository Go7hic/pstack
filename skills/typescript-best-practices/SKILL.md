---
name: typescript-best-practices
description: TypeScript best practices. Use when reading or editing any .ts or .tsx file.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# TypeScript best practices

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


Apply the **type-system-discipline** principle skill first; this skill grounds it in TypeScript syntax.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they can't be mixed up. Validate once at creation. |
| Constructive modeling | Build the shape so the illegal value can't be constructed. `[T, ...T[]]` for non-empty, `[T, T][]` for even length, `start` plus `duration` for a range. Not a runtime guard, not a wish for refinement types. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. `any` disables type checking everywhere it touches. |
| No `as` casts | Every `as` is a runtime crash waiting. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Boundary validation | Validate where data crosses in; trust types inside. See the **boundary-discipline** principle skill. |
| Schema-derived types | Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Don't mock what you can run. Prefer the framework's real test primitives with leak/disposable checks, and verify UI in a running build. Mock only what you can't run locally. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples: `references/patterns.md`.
