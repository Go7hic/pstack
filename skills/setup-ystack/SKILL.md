---
name: setup-ystack
description: "Configure which models ystack uses per role. Detects available models, migrates legacy pstack configuration when present, and writes the preferred ystack override file. Use for /setup-ystack, configure ystack models, or change ystack model choices on any coding agent."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see ystack adapters.
---

# Setup ystack

## Portability (required)

1. Read `../pstack/references/capability-contract.md`, `../pstack/references/model-override.schema.json`, and the active adapter.
2. Prefer the ystack-named override beside the active agent:
   - Cursor: `~/.cursor/rules/ystack-models.mdc` or a project `.cursor/rules/` file;
   - Codex: `~/.codex/rules/ystack-models.md`;
   - Claude Code / generic: a host-supported user rule or `~/.agents/ystack-models.md`.
3. Read legacy files as fallback when the preferred file does not exist:
   - `pstack-models.mdc` / `pstack-models.md`;
   - Codex may also honor `codex-pstack-models.md`.
4. Never invent model slugs. Write only slugs confirmed available in this session.
5. Validate with `python3 scripts/validate_model_override.py <path>` when the script is available; otherwise self-check against the schema.

## Goal

Write a ystack model override that maps `model_role` values and panel arrays to host models. Missing roles and values set to `inherit-parent` or `auto` inherit the parent session behavior.

## Steps

### 1. Detect available models

Enumerate model identifiers that the active adapter can pass to helper calls. If the host cannot expose a catalog, ask the user to supply the identifiers they actually have. `inherit-parent` and `auto` are always valid aliases.

### 2. Load current state

Read the preferred ystack file first. If absent, read the adapter's legacy pstack file and label it as migration input. Do not silently delete the legacy file.

### 3. Map and confirm

Show every role with its current model. Mark unavailable identifiers. Ask through `ask_user` whether to accept or change the mapping. Panel arrays use one helper per entry; prefer diverse model families when available.

### 4. Validate

Every real model identifier must be confirmed by the host. Reject an empty `roles` object, unknown keys, empty strings, and an unsupported schema version.

### 5. Write the preferred override

Overwrite the ystack-named file so reruns remain idempotent:

````markdown
---
description: ystack model overrides
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

Panel arrays may be shortened when the host concurrency budget is lower. Do not write the old label-line format.

### 6. Confirm migration state

Report the preferred path written, any legacy path read, and whether the old file remains. New sessions should prefer the ystack file.

### 7. Offer a verification skill once

When the project has no repeatable way to drive the real app, offer once to run `create-verification-skill`. Continue normally if declined.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | broad read-only fan-out and mechanical work |
| `feature_impl` | spec-driven implementation and refactoring |
| `bug_impl` | high-stakes fixes after evidence |
| `judgment` | architecture, synthesis, and prose |
| `critic` | adversarial and panel review |
