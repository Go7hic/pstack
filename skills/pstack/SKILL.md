---
name: pstack
description: "Legacy compatibility alias for ystack. Use when an existing prompt, installation, or workflow still invokes pstack; new work should prefer ystack."
license: MIT
compatibility: Requires the complete ystack Agent Skills pack.
metadata:
  upstream: https://github.com/cursor/plugins/tree/main/pstack
  deprecated-in-favor-of: ystack
---

# pstack compatibility alias

## Portability (required)

1. Read `../ystack/SKILL.md` in full before taking any action.
2. Treat `/pstack` as `/ystack` and follow the ystack router exactly.
3. Keep this directory's `playbooks/` and `references/` as shared legacy runtime assets until a separately versioned migration removes them.
4. Prefer `/setup-ystack` and ystack-named model overrides; continue honoring legacy configuration through the adapters.

Do not present pstack as the public name of this repository. It remains here for upstream attribution and backwards compatibility.
