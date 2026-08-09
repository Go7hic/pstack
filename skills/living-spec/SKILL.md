---
name: living-spec
description: "Maintain a lightweight, current product-truth layer for pstack projects. Use for /living-spec inspect, draft, or converge; when a feature changes durable user-visible or business behavior; when work spans sessions or pull requests; or when current product docs, change briefs, or ADRs must stay aligned with verified implementation."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Living spec

Keep the repository's current product behavior understandable without requiring a full specification framework for every task.

This skill is intentionally small. It distinguishes:

- **current truth** — what the product now promises;
- **change context** — what one in-progress change is trying to alter;
- **decision rationale** — why one durable technical choice won;
- **execution evidence** — how the work was performed and verified.

Do not combine those into one ever-growing document.

## Portability (required)

1. Read the [pstack capability contract](../pstack/references/capability-contract.md), [workflow-quality defaults](../pstack/references/workflow-quality.md), and the active host adapter before delegation.
2. Use `explore` to discover existing documentation and behavior, `implement` for bounded documentation edits, `review` for independent convergence checks, `ask_user` only for product intent that evidence cannot settle, and `verify` for observable behavior.
3. Keep paths repository-relative. Do not depend on one vendor's session, transcript, or rules directory.
4. Small documentation decisions stay on the lead agent. Use helpers only when independent investigation or review will reduce a real blind spot.
5. Existing canonical systems win. If the repository already uses OpenSpec, another spec framework, established ADRs, or a product documentation hierarchy, update that system instead of creating a competing source of truth.

## Default layout

Use the repository's established layout when one exists. Otherwise prefer:

```text
docs/
├── product/      # current verified product behavior
├── changes/      # temporary briefs for larger in-progress changes
└── decisions/    # durable ADRs

.audit/            # optional execution evidence from show-me-your-work
```

These paths are defaults, not requirements.

## Persistence decision

At the beginning of a feature, classify the change with these questions:

1. Does it create or modify durable user-visible, operator-visible, API, security, billing, permission, data-retention, or business behavior?
2. Will it likely span multiple sessions, pull requests, repositories, owners, or independently shipped units?
3. Will a future maintainer need to know why a non-obvious choice was made?

Choose the smallest persistence level that earns its cost:

| Result | Action |
| --- | --- |
| No durable behavior change | No product document. Record `not required` with a reason. |
| Durable behavior, one bounded change | Update one current-truth product document during `converge`. |
| Durable behavior plus multi-session or multi-PR work | Create one temporary change brief, then converge into current truth. |
| Durable, non-obvious, hard-to-reverse decision with real alternatives | Add an ADR in addition to the relevant current-truth update. |

Do not create an ADR for naming, local refactoring, routine library use, or an easily reversible implementation detail.

## Operation: inspect

Use before design or implementation.

1. Read the user request, originating ticket/spec/acceptance list, and relevant repository instructions.
2. Discover existing product docs, specifications, ADR conventions, change briefs, and external authority documents.
3. Use `explore` to compare intended behavior with current code, tests, and the real runtime surface when available.
4. Classify any mismatch:
   - **implementation bug** — documented or requested behavior is not delivered;
   - **stale documentation** — verified behavior changed intentionally but current truth was not updated;
   - **unresolved product decision** — evidence cannot determine what should happen;
   - **implementation detail only** — no product-truth update is needed.
5. Return a documentation plan:
   - persistence level;
   - canonical files to read or update;
   - whether a change brief is warranted;
   - whether an ADR may be warranted;
   - explicit `not required` reason when no persistence is needed.

`inspect` is read-only unless the user explicitly asks to create the brief immediately.

## Operation: draft

Use only when `inspect` found that the change benefits from a persistent brief.

1. Create one file using the [change brief template](references/change-brief-template.md).
2. Keep it concise: intent, scope, non-goals, acceptance, constraints, current design choice, verification plan, and product docs expected to change.
3. Prefer checkable behavior over implementation narration.
4. Link authoritative security, design-system, API, or operational docs rather than copying them.
5. Set status to `draft` or `in-progress`. The brief is not current product truth.
6. When implementation reveals a real design change, update the brief rather than allowing chat history to become the only record.

Do not split a solo-project change into proposal/spec/design/tasks files unless the repository already follows that convention.

## Operation: converge

Use only after the implementation has been verified on the meaningful real surface.

1. Re-read:
   - the original intent and acceptance criteria;
   - the final implementation diff;
   - tests and runtime evidence;
   - any change brief and decision trail;
   - current product docs and ADRs.
2. Update current truth using the [product document template](references/product-doc-template.md), adapted to the repository's existing style.
3. Describe the final verified behavior:
   - normal paths;
   - failure and boundary scenarios;
   - product constraints and non-goals that remain relevant;
   - stable technical constraints only when maintainers must preserve them;
   - repeatable verification surfaces.
4. Remove or rewrite stale current-behavior statements. Never append a new rule beside a contradictory old rule.
5. Do not rewrite desired intent to match a broken implementation. When verified behavior misses the accepted requirement, report a convergence gap and route back to implementation or an explicit product decision.
6. Create an ADR from the [ADR template](references/adr-template.md) only when the decision is durable, non-obvious, difficult to reverse, and had meaningful alternatives.
7. Resolve the temporary change brief:
   - archive it when its decision history remains valuable;
   - otherwise delete it after current truth converges; Git retains the history;
   - never leave an `in-progress` brief after the change is complete.
8. Run a convergence review:
   - for ordinary work, the lead compares docs, acceptance, diff, and verification;
   - for high-risk or broad changes, use one read-only `review` helper with `model_role:critic`;
   - classify the result as `pass`, `gap`, or `not applicable`.

## Canonicality rules

- One domain has one current-truth home.
- Current product docs describe **now**, not the chronology of implementation.
- Change briefs describe **this in-progress change**, not the whole product.
- ADRs describe **why a durable decision was made**, not product requirements.
- `.audit/` and `show-me-your-work` describe **execution evidence**, not current behavior.
- Git history preserves previous versions; do not retain obsolete rules in current docs merely for history.
- External authority documents stay authoritative. Link them and record only the change-specific constraint.

## Output contract

Always report:

```text
Documentation:
- persistence: none | product-doc | change-brief | ADR
- current truth: <paths or not required>
- change brief: <path and status, or none>
- decisions: <ADR paths or none>
- convergence: pass | gap | not applicable
- evidence: <verification pointers>
```

When there is a gap, name whether code, docs, or product intent must change next.
