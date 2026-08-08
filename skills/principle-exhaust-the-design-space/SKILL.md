---
name: principle-exhaust-the-design-space
description: "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Exhaust the Design Space

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before any helper delegation.
2. Prefer capability verbs (`explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`) over vendor tool names.
3. Resolve models through `model_role`. Never require a vendor-specific model identifier.
4. When helper spawning is unavailable, run the work on the lead agent and state that fan-out was collapsed.

When a novel interaction or architectural decision has no established precedent, explore several concrete alternatives before implementation. Building the wrong thing costs more than exploring three options.

**The rule.** When the right answer is not obvious, build 2-3 competing prototypes or sketches. Compare them side by side. Only then commit. Design it twice is this rule by another name. A second flavor of the first shape does not count.

**When it applies:**
- Novel UI interactions (no prior art in the codebase)
- Architectural choices with multiple viable approaches
- Product design decisions where user experience depends on feel, not logic

**When it doesn't:**
- Mechanical implementation where the pattern is established
- Bug fixes or refactors with a clear target state
- Changes where constraints dictate a single viable approach
