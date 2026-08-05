---
name: pstack
description: >-
  Portable pstack engineering system for multiple coding agents. Use for
  poteto-mode / pstack rigor, nontrivial features, bug fixes, investigations,
  architecture, arena/swarm parallelism, adversarial review, verification,
  unslopped prose, or when routing across how/why/architect/interrogate and the
  full playbook set on Cursor, Codex, Claude Code, or other Agent Skills runtimes.
license: MIT
compatibility: Requires an Agent Skills-compatible coding agent. Multi-agent optional.
metadata:
  upstream: https://github.com/cursor/plugins/tree/main/pstack
  format: agentskills
---

# pstack

Portable entry for the full pstack skill pack. Same engineering system as Cursor pstack / poteto-mode, without hard-coding one vendor runtime.

## Portability (required)

1. Read `references/capability-contract.md`.
2. Read one adapter before delegation (pick the best match; do not default to single-threaded when a spawn tool exists):
   - Claude Code → `references/adapters/claude-code.md`
   - Droid / Factory → `references/adapters/droid.md`
   - OpenCode → `references/adapters/opencode.md`
   - Codex → `references/adapters/codex.md`
   - Cursor (only if using this pack instead of the official plugin) → `references/adapters/cursor.md`
   - Unknown / other → `references/adapters/generic.md` (still uses `Agent`/`Task`/`task` for `parallel` when present)
3. Prefer capability verbs (`explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`) over vendor tool names.
4. Install notes: repo `INSTALL.md`.

## First moves

1. Start a todolist. First item: read the Principles index in the `poteto-mode` skill (or `references/principles-summary.md` here), then open any leaf `principle-*` skill you apply.
2. Match a playbook under `playbooks/` and copy its steps into the todolist.
3. Route to sibling skills as steps require (`how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `unslop`, `tdd`, …). Those skills ship in this same pack.
4. Verify before declaring done (`principle-prove-it-works`).

## Playbooks

All playbooks live in `playbooks/` (mirrored from poteto-mode):

investigation, bug-fix, perf-issue, hillclimb, runtime-forensics, trace-forensics, feature, refactoring, prototype, visual-parity, authoring-a-skill, eval, babysit, shipping, autonomous-run, orchestrate, autopilot-full, autopilot-stack, session-pickup, pause-safely, multi-phase-plan, worktree-cleanup, opening-a-pr.

## Sibling skills in this pack

**Workflow:** how, why, recall, blast-radius, architect, arena, swarm, interrogate, figure-it-out, teach, reflect, automate-me, setup-pstack, show-me-your-work, create-verification-skill, maintain-verification-skill, tdd, typescript-best-practices

**Quality / prose:** unslop, no-comments, technical-writing, bro

**Mode:** poteto-mode (full sticky mode + inline principles index)

**Principles:** all `principle-*` leaf skills

**Agent rubrics:** `references/agents/poteto-agent.md`, `references/agents/comment-sicko.md` (prompts for adapter helpers, not Cursor-only types)

## External / optional

Upstream poteto-mode also references tools that are **not** in this pack:

- `deslop`, `control-cli`, `control-ui` (Cursor cursor-team-kit) — use local equivalents or skip
- benny automation pack — see repo `references/automations/` (optional, Cursor-oriented)

## Alias

If the user says `/poteto-mode` or "poteto style", run this skill together with `poteto-mode` (same playbooks and principles). Prefer `poteto-mode` for the sticky mode non-negotiables; prefer `pstack` for adapter-first portable routing.

## Model roles

Do not hard-require Cursor model slugs. Resolve models through `model_role` and the active adapter:

| Role | Use |
| --- | --- |
| `fast_explore` | Broad read-only fan-out, mechanical edits |
| `feature_impl` | Spec-driven implementation / refactoring |
| `bug_impl` | High-stakes fixes after evidence |
| `judgment` | Architecture, synthesis, prose |
| `critic` | Adversarial / panel review |

If a local override file exists, prefer it. If a slug is unavailable, fall back to the parent model and say so.
