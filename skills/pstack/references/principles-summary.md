# Principles

Apply these as decision rules. Name a principle only when it changed a choice.

## Core

- **Laziness protocol.** Prefer deletion, the smallest useful change, and fewer abstractions.
- **Foundational thinking.** Name the data shape, ownership, and shared state before code.
- **Redesign from first principles.** When a requirement breaks the core shape, redesign instead of bolting on exceptions.
- **Subtract before adding.** Remove dead paths or confusing layers before adding new ones.
- **Minimize reader load.** Collapse one-caller wrappers, shrink mutable scope, make the path traceable.
- **Outcome-oriented execution.** Converge on the intended architecture; do not preserve throwaway compatibility states.
- **Experience first.** Choose the product outcome users feel, not the easiest implementation.
- **Exhaust the design space.** When a novel decision has no precedent, sketch 2–3 alternatives before committing.
- **Build the lever.** Prefer a script, repro, eval, or harness that proves or accelerates the work.

## Architecture

- **Model the domain.** Encode the domain in a structure (state machine, typed model, table/registry, reducer, boundary) instead of scattered conditionals.
- **Boundary discipline.** Validate at system boundaries, trust internal types, keep business logic pure.
- **Type system discipline.** Make illegal states unrepresentable; parse external data at the edge.
- **Make operations idempotent.** Design commands and loops to converge under retries and crashes.
- **Migrate callers then delete legacy APIs.** Avoid long-lived parallel old/new paths.
- **Separate before serializing shared state.** Remove unnecessary sharing before adding locks or queues.

## Verification

- **Prove it works.** Verify against the real artifact or a faithful local equivalent.
- **Fix root causes.** Reproduce, trace, and confirm the surviving mechanism before patching.
- **Sequence work into verifiable units.** Each phase ends with a concrete check; verify before the next.

## Delegation

- **Guard the context window.** Route bulk exploration and independent review to helpers when the adapter supports it; keep summaries on the main thread.
- **Never block on the human** for reversible work. Observe, prototype, or proceed when the answer can be discovered.

## Meta

- **Encode lessons in structure.** Turn repeated instructions into a lint, test, script, config, or skill update.

## Prose

- Short declarative sentences. One thought per sentence.
- No filler, boilerplate, or invented certainty.
- Impact before implementation trivia.
- Do not fabricate citations, links, or transcript references.
