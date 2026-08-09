---
name: setup-pstack
description: "Legacy compatibility alias for setup-ystack. Use when an existing prompt still invokes /setup-pstack; new work should prefer /setup-ystack."
license: MIT
compatibility: Requires the complete ystack Agent Skills pack.
metadata:
  deprecated-in-favor-of: setup-ystack
---

# setup-pstack compatibility alias

## Portability (required)

1. Read `../setup-ystack/SKILL.md` in full.
2. Treat `/setup-pstack` as `/setup-ystack`.
3. When a legacy `pstack-models.*` file exists, use it as migration input and write the preferred `ystack-models.*` path.
4. Do not delete legacy configuration unless the user explicitly asks.

Report both the new path and any legacy path that was read.
