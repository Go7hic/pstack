---
name: pstack
description: "Portable pstack engineering system for multiple coding agents. Use for pstack or poteto rigor, non-trivial features, bug fixes, investigations, architecture, parallel exploration, adversarial review, verification, or routing across how, why, architect, arena, swarm, and interrogate."
license: MIT
compatibility: Requires an Agent Skills-compatible coding agent. Multi-agent optional.
metadata:
  upstream: https://github.com/cursor/plugins/tree/main/pstack
  format: agentskills
---

# pstack

Portable entry point for the pstack engineering system. It preserves the upstream principles and playbooks while translating delegation, model selection, verification, and runtime control through host adapters.

## Portability (required)

1. Read `references/capability-contract.md`.
2. Detect the active coding agent and read one matching file under `references/adapters/`. Use `generic.md` when no named adapter fits.
3. Express workflow steps through `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, and `model_role` rather than vendor tool names.
4. Prefer real parallel helpers when the host exposes them. Collapse to the lead agent only when spawning is missing, denied, or unsafe because write scopes overlap.
5. Resolve concrete models through `/setup-pstack` and the active adapter. Never copy model identifiers from another host.
6. Keep synthesis, final diff judgment, and verification on the lead agent.

## First moves

1. Create a todo list. The first item reads the Principles index in `poteto-mode` or `references/principles-summary.md`, then opens every leaf principle that affects a real decision.
2. Match a playbook under `playbooks/` and copy its steps into the todo list before adding task-specific work.
3. Route to sibling skills as the playbook requires: `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `tdd`, `unslop`, and the verification skills.
4. Use `verify` before declaring completion. A passing proxy is not proof when the reported problem appears on another surface.
5. State any degraded capability, such as unavailable helper spawning, model selection, transcript access, or runtime control.

## Playbooks

The entry pack includes:

- investigation;
- bug fix;
- performance issue;
- hillclimb;
- runtime and trace forensics;
- feature and refactoring;
- prototype and visual parity;
- skill authoring and eval;
- Babysit and Shipping;
- autonomous run and Orchestrate;
- full and stacked autopilot;
- session pickup and safe pause;
- multi-phase planning;
- worktree cleanup;
- opening a pull request.

## Sibling skills

**Understanding and design:** `how`, `why`, `recall`, `blast-radius`, `architect`, `arena`, `swarm`, `interrogate`, `teach`.

**Execution and adaptation:** `figure-it-out`, `reflect`, `automate-me`, `setup-pstack`, `show-me-your-work`, `tdd`, `typescript-best-practices`.

**Verification:** `create-verification-skill`, `maintain-verification-skill`.

**Quality and prose:** `unslop`, `no-comments`, `technical-writing`, `bro`.

**Mode:** `poteto-mode`, which owns the full router, principles index, autonomy boundaries, delegation contract, and playbook triggers.

**Agent rubrics:** `references/agents/poteto-agent.md` and `references/agents/comment-sicko.md`. Adapters pass these as prompts when the host has no custom helper type.

## Optional host tooling

Some upstream workflows mention cleanup, browser-control, CLI-control, automation, and skill-authoring tools that are not part of pstack itself. Use equivalent capabilities exposed by the active host. When no equivalent exists, apply the documented fallback and report the missing verification or automation surface.

The optional Benny automation sources live outside the installable skill tree. They remain host-oriented templates and are not loaded as portable Agent Skills.

## Alias and mode lifetime

When the user says `/poteto-mode` or requests Poteto style, invoke `poteto-mode` with this entry skill. Use `pstack` for adapter-first routing and `poteto-mode` for the full mode contract.

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
