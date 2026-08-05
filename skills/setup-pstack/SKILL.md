---
name: setup-pstack
description: "Configure which models pstack uses per role. Detects available models and writes an always-applied override file. Use for /setup-pstack, configure pstack models, or changing pstack model choices on any coding agent."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Setup pstack

## Portability (required)

1. Read the sibling `pstack` skill `references/capability-contract.md` and the active adapter.
2. Write the override beside the active agent — do not assume one vendor path:
   - Cursor: `~/.cursor/rules/pstack-models.mdc` (or project `.cursor/rules/`)
   - Codex: `~/.codex/rules/pstack-models.md`
   - Claude Code / generic: project or user rules file named in the adapter, or `~/.agents/pstack-models.md`
3. Never invent model slugs. Only write slugs confirmed available in this session.

## Goal

Write a **pstack model override file** that maps roles to models. Skills read it and fall back to `model_role` defaults when a line is absent.

## Steps

### 1. Detect available models

Enumerate model slugs you can pass to adapter helpers in this session. If you cannot detect any, ask the user to paste the slugs they have. Never write an unconfirmed real slug. Aliases `inherit-parent` and `auto` are always valid.

### 2. Load current state

If a pstack model override file already exists for this runtime, read it. Otherwise start from the role table below.

### 3. Map and confirm

Show every role with its current model. Mark unavailable slugs. Ask via `ask_user` whether to accept or change. For panel roles the value is a list (one helper per entry). `arena cross-judge pool` is a list from which Arena picks one. Prefer diverse families for panels when available.

### 4. Validate

Every real slug must be in the detected set. `inherit-parent` / `auto` always pass.

### 5. Write the override

Overwrite the whole file so re-runs stay idempotent. Example shape (values are placeholders — replace with confirmed slugs):

```text
# pstack model configuration. One line per role.
# inherit-parent / auto => omit model on that role (use parent chat model).
feature, refactoring: <feature_impl>
bug-fix, perf-issue, hillclimb: <bug_impl>
judgment and prose: <judgment>
hardest tasks: <judgment>
how explorer: <fast_explore>
how explainer: <judgment>
how critics: <critic>, <critic>, <critic>
why investigators: <fast_explore>
why synthesizer: <judgment>
reflect tooling: <feature_impl>
reflect judgment, divergent, synthesizer: <judgment>
arena runners: <critic>, <critic>, <critic>
arena cross-judge pool: <judgment>, <critic>, <critic>
swarm workers: <fast_explore>
architect runners: <judgment>, <critic>, <critic>
interrogate reviewers: <judgment>, <critic>, <critic>
```

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
