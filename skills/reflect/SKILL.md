---
name: reflect
description: "Review a completed or difficult working session from three independent lenses, identify durable lessons, and route accepted lessons into concrete skill or tooling changes. Use when the user says reflect or when a repeatable workflow should be captured."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Reflect

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before delegation.
2. Use `parallel` with read-only `review` helpers for the independent lenses. Use `review` or the lead agent for synthesis.
3. Obtain session evidence through capabilities the active host actually exposes. Never assume a particular transcript filesystem, project-history directory, or JSONL schema.
4. Resolve models through `model_role`; never require a vendor-specific model identifier.
5. When transcript export or helper spawning is unavailable, use a bounded session digest and run the lenses sequentially on the lead agent. State the degraded path.

## Purpose

Mine a session for lessons that should improve future work. A lesson is durable when it applies beyond the exact task and can be encoded in a skill, adapter, script, lint, metadata rule, test, or operating convention.

Reflect when:

- the user says `reflect` or `/reflect`;
- a complex task landed and the successful recipe is worth preserving;
- the agent hit dead ends before finding a reusable path;
- the user corrected the working method rather than only the final answer;
- a workflow repeated enough to justify automation;
- an existing skill failed to trigger, routed poorly, or contained stale runtime assumptions.

Skip reflection for trivial conversations, one-off facts, or work already handled correctly by an existing skill. Do not turn every preference into global policy.

## Process

### 1. Build the session evidence package

Use the best source the active host exposes, in this order:

1. a first-class current-conversation or transcript resource;
2. a runtime-provided session export or transcript path explicitly associated with the current conversation;
3. the visible conversation context plus tool results;
4. a compact digest written by the lead agent.

Never search broad user-history or project-history directories to guess which conversation is active. Do not read unrelated sessions.

The evidence package contains:

- the user's original goal;
- important constraints and corrections;
- the approach taken and major decisions;
- failed paths and why they failed;
- verification evidence;
- the resulting diff, artifact, or answer;
- unresolved concerns;
- existing skills that were invoked, skipped, or misrouted.

Prefer a file or runtime resource pointer when helpers can read it. Otherwise pass a compact digest. Do not inline a massive transcript into every helper prompt.

### 2. Run three independent reviews

Use one `parallel` fan-out with three read-only `review` helpers. The prompts explicitly forbid file edits and external writes.

| Lens | Model role | Prompt template | Question |
| --- | --- | --- | --- |
| Judgment | `judgment` | `references/judgment-reviewer.md` | Which decisions, trade-offs, and corrections generalize? |
| Tooling | `feature_impl` or `bug_impl` | `references/tooling-reviewer.md` | What should become a script, check, adapter rule, or workflow change? |
| Divergent | `critic` | `references/divergent-reviewer.md` | What did the other lenses overlook, and which apparent lesson is actually noise? |

Each reviewer receives the same evidence package and the relevant prompt template. Each returns:

- proposed lesson;
- supporting session evidence;
- scope and counterexamples;
- recommended enforcement mechanism;
- target skill, adapter, script, or backlog item;
- confidence and risk of overgeneralization.

When `parallel` is unavailable, run the three lenses sequentially and keep their notes separate until synthesis.

### 3. Synthesize

Synthesize on the lead agent or with one read-only `review` helper using `model_role:judgment` and `references/synthesizer.md`.

Return three groups:

- **Accepted.** Durable, supported, correctly scoped, and routed to a concrete change.
- **Rejected.** Unsupported, already encoded, too specific, contradictory, or likely to create bad global behavior.
- **Backlog.** Valuable, but better implemented as tooling, evaluation, metadata, or a broader design change rather than an immediate skill edit.

The synthesizer must deduplicate equivalent lessons, surface disagreements, and preserve counterexamples. A repeated sentence is not automatically a rule; a rule earns its place by preventing a demonstrated failure.

### 4. Prefer structural enforcement

Review every Accepted item before proposing edits.

Move an item to Backlog when it would be enforced more reliably by:

- a lint or static check;
- a CI workflow;
- metadata or frontmatter;
- a runtime guard;
- an adapter capability rule;
- an automated migration or generator;
- an evaluation fixture.

Follow the **encode-lessons-in-structure** principle. Do not keep adding prose when a machine-checkable constraint is available.

### 5. Obtain approval for durable changes

Present the full Accepted, Rejected, and Backlog result before editing skills. Wait for explicit user approval of the subset to apply.

This checkpoint is mandatory because skill changes affect future sessions and possibly multiple coding agents. It does not apply to a read-only reflection report.

Do not create tickets, modify shared trackers, or change external systems unless the user has authorized that workflow and the active adapter exposes the required tools. Otherwise include a ready-to-file backlog description in the report.

### 6. Apply approved changes

For each approved item:

- **Small correction.** The lead edits an existing skill, adapter, or maintenance document directly.
- **Substantive skill change.** Use the active coding agent's skill-authoring workflow, including its validation or evaluation loop.
- **Trigger problem.** Tune the skill description and test that the intended request selects it without causing unrelated activation.
- **New skill.** Create one only when no existing skill owns the reusable discipline.
- **Structural rule.** Implement the script, lint, CI check, metadata flag, or adapter change instead of adding another instruction paragraph.

Run any available Skill validator on touched skills. For portable pstack changes, also run:

```bash
python3 scripts/audit_portability.py
python3 scripts/audit_portability.py --strict --changed-from origin/main
```

When a mirrored playbook, adapter, or capability contract changes, refresh the mirror and verify byte equality before declaring completion.

### 7. Report

Return a compact record:

- **Applied.** Path and one-line change for every accepted edit.
- **Structural changes.** Scripts, checks, metadata, or evaluations added.
- **Backlog.** Ready-to-file items and why they were deferred.
- **Rejected.** One line per dropped lesson with the synthesizer's reason.
- **Verification.** Validators, audits, and behavior checks that passed.
- **Evidence source.** Transcript resource, exported session, visible context, or lead-written digest.

## Model roles

| Role | Use |
| --- | --- |
| `judgment` | session interpretation and synthesis |
| `feature_impl` | workflow and tooling improvement analysis |
| `bug_impl` | failure-path and debugging-process analysis |
| `critic` | divergent review and overgeneralization pressure |

If no role override is available, inherit the parent session model.
