---
name: swarm
description: "Fan out independent workers, drain them, and return one evidence-backed report. Use for /swarm, \"swarm this\", parallel coverage, package-by-package checks, exploration partitions, implementation slices, races, or gauntlets."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Swarm

## Portability (required)

1. Read the `pstack` capability contract and the active host adapter before delegation.
2. Use `explore` for read-only coverage, `implement` for bounded write slices, `review` for independent criticism, and `parallel` to launch independent workers together.
3. Resolve worker models through `model_role`. Never require a vendor-specific helper type, background flag, or model identifier.
4. When the host cannot spawn helpers, execute the same slices sequentially on the lead agent and report the collapsed topology.

## Purpose

A Swarm runs several independent pieces of work and returns one consolidated result. It can:

- partition a codebase or data set into non-overlapping slices;
- run the same read-only check across many packages;
- race several implementations or investigations;
- combine coverage slices with a small race inside one slice;
- run a gauntlet of independent verification or review criteria.

Use **arena** instead when the main goal is to produce several candidates for one artifact, select a base, and graft the best ideas together. Swarm aggregates independent results; Arena synthesizes one winner.

## Start

Create a todo list with one entry per phase:

1. Frame
2. Partition
3. Fan out
4. Drain
5. Aggregate
6. Verify and report

## Phase A: Frame

State:

- the final artifact or report;
- the done predicate;
- required coverage;
- the worker result schema;
- the failure policy;
- the selection rule when any slice is a race.

Choose the Swarm shape before launching:

- **Partition.** Different workers own different slices.
- **Race.** Several workers receive the same brief; choose `first pass`, `rank all`, or `best of` before results arrive.
- **Mixed.** Partition the domain, then race only selected high-risk slices.
- **Gauntlet.** Each worker applies a different independent criterion to the same artifact without editing it.

Derive worker count from the shape and host concurrency limits. More workers are not automatically faster when coordination or setup dominates.

## Phase B: Partition safely

Every worker brief stands alone and names:

- goal and exact slice;
- allowed files, packages, records, or runtime resources;
- whether the worker is read-only or write-capable;
- data shape, invariants, and interfaces when code is involved;
- verification command or evidence contract;
- output location;
- result status: `PASS`, `ISSUES`, or `BLOCKED`;
- what must be returned to the lead.

Use `model_role:fast_explore` for broad reading and mechanical checks, `feature_impl` for clear implementation slices, `bug_impl` for evidence-backed fixes, and `critic` for independent review.

Before write fan-out, apply **separate-before-serializing-shared-state**. Give each worker a disjoint file set, branch, worktree, output directory, fixture, environment, or external resource. Do not let workers write the same target concurrently.

Run shared setup and blocking gates before fan-out. Do not make every worker repeat expensive repository setup when one verified scaffold can be reused safely.

## Phase C: Fan out

Use one `parallel` launch for all independent workers that fit the host limit.

- Read-only slices use `explore` or `review` according to the task.
- Write slices use `implement` with explicit disjoint scope.
- Use isolated worktrees or output directories when the adapter supports them.
- When the active host provides non-blocking helpers, continue only lead work that cannot conflict with worker output.
- Do not nest uncontrolled swarms. A worker may use local parallelism only when its brief and adapter explicitly allow it.

If a worker cannot start, record the dropout and either reassign the slice, run it on the lead, or report the coverage gap. Never silently reduce required coverage.

## Phase D: Drain and inspect

Collect terminal results and evidence for every required slice.

The lead checks:

- the worker actually stayed inside scope;
- evidence resolves and supports the result;
- write workers produced a reviewable diff;
- verification used the required surface;
- duplicate or contradictory findings are identified;
- blocked slices name the missing fact or capability.

Do not paste raw worker dumps into the final answer. Keep file or artifact pointers and a compact summary.

## Phase E: Aggregate

For partitioned coverage, every required slice must have a result or an explicit gap.

For a race, apply the predeclared rule:

- **First pass.** Accept the first result that satisfies the complete predicate; still stop and inspect the remaining workers safely.
- **Rank all.** Score every result against a fixed rubric.
- **Best of.** Select the strongest evidence-backed result and state why it won.

Do not change the rule after seeing which worker produced which result. When outputs diverge because the brief was under-specified, reframe and rerun rather than averaging incompatible answers.

Deduplicate issues, preserve source slices, and distinguish consensus from repeated copies of the same upstream assumption.

## Phase F: Verify and report

The lead verifies the aggregate result. A collection of worker passes does not prove the combined artifact works.

Return:

- Swarm shape and worker count;
- model roles and capability types used;
- one compact row per slice or race arm;
- evidence-backed issues;
- dropouts, blocked slices, and degraded-host behavior;
- race rule and selection when applicable;
- aggregate verification result;
- final artifact or recommended next action.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | read-only coverage and mechanical checks |
| `feature_impl` | disjoint, spec-driven implementation slices |
| `bug_impl` | evidence-backed fixes |
| `critic` | independent review and gauntlet criteria |
| `judgment` | aggregation, conflict resolution, and final selection |

If no role override is available, inherit the parent session model.
