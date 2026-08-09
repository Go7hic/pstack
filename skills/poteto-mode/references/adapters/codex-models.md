# Codex model notes

Companion to `codex.md`. Validate every model identifier against current Codex tool metadata before use; examples here are structural, not a live catalog.

## Override files

Preferred:

```text
~/.codex/rules/ystack-models.md
```

Legacy fallbacks, in order:

```text
~/.codex/rules/pstack-models.md
~/.codex/rules/codex-pstack-models.md
```

`/setup-ystack` reads a legacy file when needed and writes the preferred ystack path using the JSON fence from `../model-override.schema.json`:

````markdown
---
description: ystack model overrides
alwaysApply: true
---

```json
{
  "schema_version": 1,
  "roles": {
    "fast_explore": "<slug>",
    "feature_impl": "<slug>",
    "bug_impl": "<slug>",
    "judgment": "<slug>",
    "critic": "<slug>"
  },
  "arena_runners": ["<slug>", "<slug>"],
  "arena_cross_judge_pool": ["<slug>"],
  "interrogate_reviewers": ["<slug>", "<slug>", "<slug>"],
  "architect_runners": ["<slug>", "<slug>"]
}
```
````

Use `inherit-parent` or `auto` to omit an explicit child model. Keep reasoning effort in adapter-supported fields unless the runtime explicitly encodes it in the model identifier.

## Role intent

| Role | Intent |
| --- | --- |
| `feature_impl` | everyday implementation and refactoring |
| `bug_impl` | high-stakes reasoning after evidence |
| `judgment` | synthesis, architecture, and prose |
| `fast_explore` | fast read-only or mechanical fan-out |
| `critic` | adversarial and panel diversity |
| panel arrays | one helper per entry; prefer diverse families |
