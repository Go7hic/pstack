---
name: architect
description: "Sketch types, signatures, caller usage, and module boundaries before implementation, then keep the sketch honest while code fills in. Use for /architect, \"architect this\", \"design this\", or non-trivial work where jumping to code could lock in the wrong shape."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Architect

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before delegation.
2. Use `explore` for grounding, `parallel` through `arena` for competing sketches, `implement` for bounded code work, `review` for independent pressure, and `verify` for the resulting contract.
3. Resolve workers through `model_role`; never require a vendor-specific model identifier or helper type.
4. Keep implementation write scopes disjoint. When helpers are unavailable, perform the same phases on the lead agent rather than skipping design work.

## Goal

Design before implementing. Start with caller usage, derive types and interfaces, compare structurally different solutions, and implement against the selected sketch. When implementation repeatedly fights the design, discard the sketch and redesign instead of adding escape hatches.

## Start

Create a todo list with one item per phase:

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap or confirm

A visible phase list prevents autonomous work from silently dropping design or verification steps.

## Phase A: Ground the problem

Build a real mental model of every existing subsystem the change touches.

Run **how** over the relevant runtime and ownership paths. Use How's critique mode when the existing structure is itself the constraint. When the change moves ownership, removes a compatibility path, or contradicts an established decision, also run **why** so historical rationale becomes evidence rather than guesswork.

Grounding must identify:

- current caller usage and public interfaces;
- data ownership and mutation boundaries;
- runtime order, retries, concurrency, and failure behavior;
- existing tests and verification surfaces;
- constraints that the new shape must preserve;
- facts that remain unknown.

Naming files is not grounding. Trace the behavior from trigger to effect.

Skip this phase only for genuinely greenfield work with no surrounding integration boundary.

## Phase B: Produce competing sketches

Run **arena** with the design-sketch task and the Phase A evidence. Use `references/runner-prompt.md` for each candidate and `references/rationale-template.md` for the output package.

Each candidate writes, in this order:

1. representative caller usage;
2. the named data shape and its organizing structure;
3. types and function signatures;
4. module and ownership boundaries;
5. invariants and error behavior;
6. migration or compatibility implications;
7. alternatives rejected and why.

Use at least two structurally different candidates. Point variations inside one architecture do not satisfy the **exhaust-the-design-space** principle.

Resolve candidate models through the configured architect panel, using `model_role:critic` for independent sketches and `model_role:judgment` for cross-judging or synthesis. Prefer diverse model families when the adapter supports selection.

Screen every candidate against `references/design-red-flags.md`. Reject or revise designs with:

- shallow pass-through modules;
- information leakage across boundaries;
- temporal decomposition where callers must know internal order;
- repeated representation conversions;
- shared mutable state introduced only to make delegation convenient;
- interfaces that expose implementation decisions rather than capabilities.

Compare viable candidates on interface depth, locality, invalid-state prevention, and reader load. Prefer the shape that hides more complexity behind a smaller coherent surface without inventing speculative abstraction.

Arena returns one synthesized design package and a record of the selected base, grafted ideas, and rejected alternatives.

## Phase C: Agree when a checkpoint is requested

Default behavior is to continue with the synthesized design. Do not add a human checkpoint for a reversible engineering decision unless the user asked for one.

Pause before implementation when the invoker explicitly requests a checkpoint or when the design creates an irreversible external contract, destructive migration, deployment, or customer-visible commitment.

When a checkpoint is active, show:

- caller usage;
- public types and signatures;
- module map;
- the key trade-off;
- what will be deleted or migrated;
- how the design will be verified.

User pushback becomes new grounding evidence. Return to Phase A and rerun the competing-sketch phase rather than patching the rejected design.

The accepted sketch may land as its own scaffold commit when doing so makes later implementation commits easier to review. Planned temporary breakage is acceptable only inside a bounded branch and with an explicit verification path.

Use **interrogate** on the sketch before implementation when the design is contested, security-sensitive, concurrency-heavy, or difficult to reverse.

## Phase D: Implement against the sketch

Use `implement` with `model_role:feature_impl` for bounded, spec-driven code work. Use `model_role:bug_impl` when the design is part of a high-stakes fix grounded in runtime evidence.

Every implementation assignment includes:

- exact file or module ownership;
- the caller usage and selected data shape;
- public signatures and invariants;
- disjoint write scope;
- success and verification criteria;
- a requirement to report deviations from the sketch.

The lead reads the diff and owns the final judgment. A helper's completion summary is not review.

Replace `not implemented` bodies with real behavior while keeping the selected interface stable. A required deviation is a design signal. Surface it and classify it:

- the sketch missed a requirement;
- the implementation is overreaching;
- an existing constraint was misunderstood;
- the interface or ownership boundary is wrong.

Do not silently add parameters, casts, optional fields, global state, or side channels to make the code fit.

Use `verify` at the public seam and on the matching runtime surface. The sketch is accepted only when callers can use it as designed and the implementation hides the promised complexity.

## Phase E: Scrap a wrong architecture

Scrap and redesign when implementation shows a repeated pattern of friction, not merely one difficult edge case. Signals include:

- the same workaround appears in unrelated call sites;
- several edge cases require the same special branch;
- types need casts, `any`, or optional fields that are always present in practice;
- callers must know internal sequencing or representation rules;
- a lock or shared store appears because ownership was never separated;
- two or more independent deviations expose the same missing concept;
- verification requires bypassing the public interface.

When the threshold is reached:

1. stop adding patches;
2. run **how** over what was learned during implementation;
3. redesign with the new constraints treated as day-one assumptions;
4. subtract the failed scaffolding before adding a replacement;
5. return to Phase B and run Arena again.

Complexity inherent in the domain is not proof of a bad architecture. Repeated complexity caused by the chosen shape is.

When the architecture holds, record the verification result and close the phase as confirmed rather than scrapped.

## Outputs

The design package starts with caller usage and derives everything else from it.

For a small change, produce one design file with usage, types, signatures, invariants, and rationale. For a larger change, add a module map, migration sequence, and verification plan. Keep the synthesis decision and rejected alternatives beside the design so future maintainers can understand why this shape won.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | broad grounding slices through How |
| `feature_impl` | bounded implementation against an accepted sketch |
| `bug_impl` | high-stakes implementation after root-cause evidence |
| `critic` | independent design candidates and adversarial pressure |
| `judgment` | cross-judging, synthesis, and final architecture decisions |

If no role override is available, inherit the parent session model.
