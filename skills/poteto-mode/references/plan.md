# Plan

Produce a phased implementation plan grounded in the **Principles** section of the `poteto-mode` skill. The plan is the deliverable. Do not implement it.

Before delegation, read the portable pstack capability contract and the adapter for the active coding agent. Use capability verbs rather than vendor tool names.

Open a todo list with one item per step below.

## 0. Triage

Skip a formal plan when the change is limited to one or two files, the approach is obvious, and no design decision is being introduced. State why a separate plan would add no value and stop.

Write a plan when the change spans three or more files, introduces architecture, has competing approaches, contains unclear scope, or the user explicitly asks for one.

## 1. Re-read principles

Read the **Principles** section of the `poteto-mode` skill end to end. Open every leaf `principle-*` skill that materially shapes the plan. Name the principle beside the decision it changes; a decorative citation is not evidence that the rule was applied.

## 2. Scope and constraints

State the scope and constraints in one paragraph.

Use `ask_user` only for a genuine product or preference decision that cannot be settled by inspecting the repository or running a probe. Give a recommended answer and concrete options for every open decision.

Resolve:

- what is included and explicitly excluded;
- technical, platform, dependency, and compatibility constraints;
- existing patterns that should remain stable;
- the observable definition of done;
- which actions are reversible and which require a human checkpoint.

## 3. Explore the repository

Use `parallel` with bounded `explore` helpers when the host supports agent fan-out. Split by independent questions such as data flow, public interfaces, test infrastructure, and deployment or runtime constraints. Use `model_role:fast_explore` unless the slice requires architectural judgment.

Each helper returns only:

- file and symbol pointers;
- relevant conventions and constraints;
- dependency and ownership boundaries;
- test and verification entry points;
- unresolved facts that require another observable check.

Do not inline large source dumps. Keep helpers read-only. When the active adapter cannot spawn helpers, perform the same exploration on the lead agent and record that parallel exploration was collapsed.

## 4. Write the plan

The user controls where the plan is stored. When no location is specified, use the repository's existing planning convention.

Use one file such as `NN-slug.md` for a small plan. For three or more phases, use a directory:

```text
NN-slug/
├── overview.md
├── phase-1-scaffold.md
├── phase-2-...md
└── testing.md
```

### Phase sizing

- A phase is one independently verifiable behavior, type, migration step, or bug fix—not simply one file.
- Prefer two or three files per phase.
- Prefer several small phases over a few broad phases when doing so preserves rollback and review options.
- Split a phase when it contains more than five distinct test cases, more than three new functions, or more than one unrelated reason to reject it.

### Overview file

Include:

- **Context.** The problem and why it matters now.
- **Scope.** Included work and explicit exclusions.
- **Constraints.** Technical, platform, dependency, compatibility, and process limits.
- **Alternatives.** Two or three credible approaches, the selected one, and its rationale. Skip only when a hard constraint leaves one valid design.
- **Applicable skills.** The pstack or domain skills the implementer should invoke.
- **Phases.** Ordered links to phase files.
- **Verification.** Project-level static and runtime checks.
- **Implementation guidance.** The non-negotiables from section 6.

### Phase files

Each phase includes:

- a back-link to the overview;
- **Goal.** The independently observable outcome;
- **Changes.** Files and interfaces affected, described as what and why rather than implementation code;
- **Data structures.** The key type, schema, state machine, registry, table, or boundary that organizes the work;
- **Dependencies.** Earlier phases or external facts that must be true;
- **Verification.** Static checks and a real-surface check where one exists;
- **Rollback.** How to remove or disable the phase without damaging later work.

Order shared types, scaffolding, and irreversible migrations before dependants. Every phase should leave the repository in a reviewable state.

For existing code, apply **redesign-from-first-principles**: describe the target shape as though the new requirement had existed from day one, then deliver that target incrementally. Do not preserve temporary compatibility layers without a named removal phase.

When a phase creates or edits a skill, direct the implementer to use the active coding agent's skill-authoring and validation workflow.

## 5. Verification per phase

Each phase needs both categories:

**Static verification**

- type checking, linting, formatting, and focused tests;
- the broader regression suite at an appropriate boundary;
- generated-file or mirror checks when the phase touches portable pstack assets.

**Runtime verification**

Use `verify` on the narrowest meaningful real surface:

- browser, Electron, or web UI through an available browser/runtime driver;
- CLI or TUI through real process execution;
- native mobile through an available simulator or device harness;
- services through a realistic request path and observable state;
- no accessible surface: state the gap and the strongest available proxy.

For a bug fix, reproduce on the original surface, apply the fix, and repeat the same reproduction. Unit tests prove a code path; they do not by themselves prove the reported symptom is gone.

## 6. Implementation guidance

The overview names the relevant `poteto-mode` non-negotiables:

- run **how** over every unfamiliar subsystem before changing it;
- use **architect** when the change crosses a meaningful interface boundary;
- use **interrogate** for contested or high-risk designs before shipping;
- apply **unslop** to prose and a local simplicity review to each diff before commit;
- use **no-comments** before review when comment quality is in scope;
- use **show-me-your-work** when the plan is long enough to require an auditable decision trail;
- use the pstack **Babysit** playbook after opening a pull request when CI, conflicts, or review threads must be driven to completion.

Implementation helpers use `model_role:feature_impl` or `model_role:bug_impl` according to the phase. Review helpers use `model_role:critic`; synthesis and final judgment use `model_role:judgment`. The active adapter resolves real models and falls back to the parent model when no override exists.

## 7. Hand back

Summarize:

- the phase sequence;
- scope boundaries;
- selected design and rejected alternatives;
- applicable skills;
- verification surfaces and known gaps;
- irreversible actions or human checkpoints.

Stop. The user decides when implementation starts.
