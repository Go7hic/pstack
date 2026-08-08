---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement, ownership, or layering questions such as \"where should this live\" and \"which package owns this\". Explains subsystem architecture and runtime flow; optionally critiques the design. Use why for historical motivation."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# How

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before delegation.
2. Use `explore` for read-only tracing, `parallel` for independent exploration slices, and `review` for architectural criticism.
3. Do not use a write-capable helper for this skill. Every helper is instructed not to edit files.
4. Resolve models through `model_role`; never require a vendor-specific model identifier.
5. When helper spawning is unavailable, run the same steps on the lead agent and state that fan-out was collapsed.

## Purpose

Answer questions about how a subsystem works at the level of a senior engineer onboarding into it. Build a useful mental model rather than an annotated source dump.

There are two modes:

1. **Explain** is the default. Trace the system and present one coherent explanation.
2. **Critique** explains the system first, then asks independent reviewers to identify architectural risks.

## Explain mode

### 1. Interpret the question

Identify the target, the requested depth, and the likely entry point. When the wording is ambiguous, state the best current interpretation and proceed; let the user redirect rather than blocking on a fact the repository can answer.

Classify the investigation:

- **Simple.** One function, module, or narrow data path that fits in one exploration pass.
- **Complex.** A subsystem spanning multiple files, services, packages, runtime surfaces, or ownership boundaries.

Lean simple when uncertain. Fan out only when independent exploration angles will reduce blind spots or protect the lead context window.

### 2a. Explore a complex subsystem

Split the question into two to four independent angles. Typical slices include:

- data model and state ownership;
- request, event, or command path;
- configuration and dependency wiring;
- persistence, queues, or external services;
- runtime effects, metrics, and failure handling;
- tests and public extension points.

Use `parallel` with one read-only `explore` helper per slice. Use `model_role:fast_explore` unless a slice requires architectural judgment.

Each helper reads `references/explorer-prompt.md` and returns:

- components and symbols found;
- the traced flow from trigger to effect;
- file pointers for every important step;
- assumptions confirmed by code;
- surprising behavior, hidden coupling, or gaps;
- anything it could not verify.

Explorers read actual implementations and follow callers, callees, types, and data transformations. File names alone are not evidence.

### 2b. Explore a simple target

Use one read-only `explore` pass with `model_role:judgment`, or perform the pass directly on the lead agent when spawning would add no value.

Read `references/explainer-prompt.md`. Trace the full path before writing the explanation. Do not stop at the first matching symbol.

### 3. Synthesize complex findings

After all complex exploration slices finish, synthesize on the lead agent or with one read-only `explore` helper using `model_role:judgment`.

The synthesizer receives file pointers and structured findings rather than large source dumps. It reconciles overlaps, resolves contradictions by reading the code, and distinguishes confirmed behavior from inference.

Use `references/explainer-prompt.md` for the communication contract. The lead owns the final explanation and should verify any load-bearing claim that came only from a helper summary.

### 4. Present the explanation

Use the sections that fit the question:

**Overview.** What the subsystem is, what it does, and where its boundary sits.

**Key concepts.** The small set of types, services, state containers, or protocols needed to understand the rest.

**How it works.** A step-by-step runtime or data-flow narrative from input to output. Reference specific files and symbols, but avoid code dumps unless a short excerpt is necessary to explain an invariant.

**Where things live.** A compact map of the directories and files a maintainer should open first.

**Gotchas.** Non-obvious behavior, misleading names, hidden state, ordering constraints, compatibility paths, or facts that remain unverified.

When the question concerns live behavior that source alone cannot settle, read `references/runtime.md` and use `verify` on the narrowest meaningful runtime surface.

## Critique mode

Critique mode starts only after Explain mode has produced a grounded architecture model.

### 1. Frame the review

State what the architecture is trying to accomplish, the constraints already confirmed, and the scope of the critique. Reviewers judge the design against that intent rather than against personal style.

### 2. Run independent critics

Use `parallel` with two or more read-only `review` helpers. Resolve each through `model_role:critic`; prefer diverse model families when the active adapter supports model selection.

Every critic receives:

1. the explanation from Explain mode;
2. the relevant file and symbol pointers;
3. `references/critic-prompt.md`;
4. `references/critique-rubric.md`.

The same evidence and rubric go to every reviewer. Independent model priors provide diversity; invented personas do not.

### 3. Apply lead judgment

The lead reads the relevant code and classifies findings:

- **Act on.** A correctness, operability, or maintainability problem worth fixing now.
- **Consider.** A real trade-off whose benefit may not justify current cost.
- **Noted.** Valid context with low immediate impact.
- **Dismissed.** Incorrect, already mitigated, unsupported, or merely stylistic.

Deduplicate equivalent findings and identify agreement across reviewers. Consensus is stronger evidence, not proof. A lone finding can still be correct; a unanimous panel can still share a bad assumption.

Present the explanation first and the critique second so the architecture model remains useful on its own.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | broad read-only tracing and independent subsystem slices |
| `judgment` | synthesis, runtime interpretation, and final explanation |
| `critic` | independent architectural review |

If no role override is available, inherit the parent session model.
