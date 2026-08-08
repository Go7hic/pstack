# Codex model notes

Companion to `adapters/codex.md`. Validate every slug against **current** Codex tool metadata before use; this file is illustrative.

## Override file

Prefer:

```text
~/.codex/rules/pstack-models.md
```

Legacy name from the old pack (still honored if present):

```text
~/.codex/rules/codex-pstack-models.md
```

`/setup-pstack` writes the new path using the portable JSON fence from `../model-override.schema.json`:

````markdown
---
description: pstack model overrides
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

Use `inherit-parent` or `auto` to omit `model` on that role. Optional effort can be encoded in the slug string only when Codex requires a combined token; otherwise keep effort in adapter-specific notes beside the override.

## Role → intent

| Role | Intent |
| --- | --- |
| `feature_impl` | everyday implementation / refactoring |
| `bug_impl` | high-stakes reasoning after evidence |
| `judgment` | synthesis, architecture, unslop-sensitive replies |
| `fast_explore` | fast read-only or mechanical fan-out |
| `critic` | adversarial / panel diversity |
| panel arrays | one helper per entry; prefer diverse families |

## Effort

When the API separates reasoning effort from the model slug, set it from host-supported fields. Do not invent effort values the tool rejects.
