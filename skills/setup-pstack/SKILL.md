---
name: setup-pstack
description: "Configure which models pstack uses per role. Detects available models and writes an always-applied override file. Use for /setup-pstack, configure pstack models, or changing pstack model choices on any coding agent."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Setup pstack

## Portability (required)

1. Read the sibling `pstack` skill `references/capability-contract.md`, `references/model-override.schema.json`, and the active adapter.
2. Write the override beside the active agent — do not assume one vendor path:
   - Cursor: `~/.cursor/rules/pstack-models.mdc` (or project `.cursor/rules/`)
   - Codex: `~/.codex/rules/pstack-models.md`
   - Claude Code / generic: project or user rules file named in the adapter, or `~/.agents/pstack-models.md`
3. Never invent model slugs. Only write slugs confirmed available in this session.
4. After writing, validate with `python3 scripts/validate_model_override.py <path>` when that script is available in the checkout; otherwise self-check against the schema fields below.

## Goal

Write a **pstack model override file** that maps `model_role` values to host models. Skills read the JSON fence and fall back to parent-session defaults when a role is absent or set to `inherit-parent` / `auto`.

## Steps

### 1. Detect available models

Enumerate model slugs you can pass to adapter helpers in this session. If you cannot detect any, ask the user to paste the slugs they have. Never write an unconfirmed real slug. Aliases `inherit-parent` and `auto` are always valid.

### 2. Load current state

If a pstack model override file already exists for this runtime, read its JSON fence. Otherwise start from the role table below.

### 3. Map and confirm

Show every role with its current model. Mark unavailable slugs. Ask via `ask_user` whether to accept or change. Panel arrays use one helper per entry. Prefer diverse families for panels when available.

### 4. Validate

Every real slug must be in the detected set. `inherit-parent` / `auto` always pass. Reject an empty `roles` object.

### 5. Write the override

Overwrite the whole file so re-runs stay idempotent. Use this exact shape (replace placeholders with confirmed slugs):

````markdown
---
description: pstack model overrides
alwaysApply: true
---

```json
{
  "schema_version": 1,
  "roles": {
    "fast_explore": "<fast_explore>",
    "feature_impl": "<feature_impl>",
    "bug_impl": "<bug_impl>",
    "judgment": "<judgment>",
    "critic": "<critic>"
  },
  "arena_runners": ["<critic>", "<critic>", "<judgment>"],
  "arena_cross_judge_pool": ["<judgment>", "<critic>"],
  "interrogate_reviewers": ["<judgment>", "<bug_impl>", "<fast_explore>", "<critic>"],
  "architect_runners": ["<judgment>", "<critic>", "<critic>"]
}
```
````

Notes:

- `inherit-parent` or `auto` means omit an explicit child model for that role.
- Panel arrays may be shortened when the host concurrency budget is lower.
- Do not write the old label-line format (`feature, refactoring: ...`).

### 6. Confirm

Tell the user where the file was written and that new sessions pick it up. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

If the project has no way to drive the real app for proof, offer once to run `create-verification-skill`. On no, move on.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | Broad read-only fan-out, mechanical edits |
| `feature_impl` | Spec-driven implementation / refactoring |
| `bug_impl` | High-stakes fixes after evidence |
| `judgment` | Architecture, synthesis, prose |
| `critic` | Adversarial / panel review |
