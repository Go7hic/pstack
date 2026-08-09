---
name: ystack
description: "Portable multi-agent engineering system for non-trivial features, bug fixes, investigations, architecture, parallel exploration, adversarial review, verification, long-running work, and product-documentation convergence. Use for ystack, rigorous engineering, or routing across how, why, architect, arena, swarm, interrogate, and living-spec."
license: MIT
compatibility: Requires the complete ystack Agent Skills pack. Multi-agent optional.
metadata:
  upstream: https://github.com/cursor/plugins/tree/main/pstack
  legacy-alias: pstack
  format: agentskills
---

# ystack

Primary public entry for the ystack engineering system. ystack evolved from portable pstack while keeping upstream attribution and legacy compatibility.

The shared runtime assets currently remain under `../pstack/` so existing installs and upstream synchronization stay stable. Do not treat that internal compatibility path as the public product name.

## Portability (required)

1. Read `../pstack/references/capability-contract.md`, `../pstack/references/host-lifecycle.md`, and `../pstack/references/workflow-quality.md`.
2. Detect the active coding agent and read one matching file under `../pstack/references/adapters/`. Use `generic.md` when no named adapter fits.
3. Express workflow steps through `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, and `model_role`, not vendor tool names.
4. Prefer real parallel helpers when the host exposes them. Collapse to the lead agent only when spawning is missing, denied, or unsafe because write scopes overlap.
5. Resolve concrete models through `/setup-ystack` and the active adapter. Never copy model identifiers from another host. Optional overrides must match `../pstack/references/model-override.schema.json`.
6. Keep synthesis, final diff judgment, and verification on the lead agent.

## First moves

1. Create a todo list. The first item reads the Principles index in `poteto-mode` or `../pstack/references/principles-summary.md`, then opens every leaf principle that changes a real decision.
2. Match a playbook under `../pstack/playbooks/` and copy its steps into the todo list before adding task-specific work.
3. Route to sibling skills as the playbook requires: `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `living-spec`, `tdd`, `unslop`, and verification skills.
4. Use `verify` before declaring completion. A passing proxy is not proof when the reported problem appears on another surface.
5. State degraded capabilities such as unavailable helper spawning, model selection, transcript access, or runtime control.

## Playbooks

The pack includes investigation, bug fix, performance, hillclimb, runtime and trace forensics, feature, refactoring, prototype, visual parity, skill authoring, eval, Babysit, Shipping, autonomous run, Orchestrate, full and stacked autopilot, session pickup, safe pause, multi-phase planning, worktree cleanup, and opening a pull request.

## Sibling skills

**Understanding and design:** `how`, `why`, `recall`, `blast-radius`, `architect`, `arena`, `swarm`, `interrogate`, `teach`.

**Execution and adaptation:** `figure-it-out`, `reflect`, `automate-me`, `setup-ystack`, `show-me-your-work`, `tdd`, `typescript-best-practices`.

**Documentation and continuity:** `living-spec` maintains current product truth, temporary change briefs, and durable ADRs without forcing a full specification framework.

**Verification:** `create-verification-skill`, `maintain-verification-skill`.

**Quality and prose:** `unslop`, `no-comments`, `technical-writing`, `bro`.

**Mode:** `poteto-mode` owns the full upstream-style router, Principles index, autonomy boundaries, delegation contract, and playbook triggers.

**Agent rubrics:** `../pstack/references/agents/poteto-agent.md` and `../pstack/references/agents/comment-sicko.md`.

## Naming and compatibility

- `/ystack` is the primary public entry.
- `/setup-ystack` is the preferred model setup command.
- `/pstack` and `/setup-pstack` remain compatibility aliases.
- `ystack-models.*` is preferred; adapters continue reading legacy `pstack-models.*` files.
- `pstack` remains valid when naming the upstream project, compatibility paths, or legacy commands.

## Alias and mode lifetime

When the user says `/poteto-mode` or requests Poteto style, invoke `poteto-mode` with this entry skill. Use `ystack` for adapter-first routing and `poteto-mode` for the full mode contract.

Mode persistence depends on the host. When no persistent mode facility exists, treat the mode as active for the current conversation and invoke it again after a fresh session or context reset.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | broad read-only exploration and mechanical work |
| `feature_impl` | spec-driven features and refactoring |
| `bug_impl` | evidence-backed bug, performance, and reliability fixes |
| `judgment` | architecture, synthesis, and prose |
| `critic` | independent candidates and adversarial review |

If no role override is available, inherit the parent session model.
