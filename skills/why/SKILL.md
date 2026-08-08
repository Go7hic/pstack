---
name: why
description: "Use for \"why does X work this way\", \"why did we choose Y\", design rationale, regressions, postmortems, historical constraints, or data-backed thresholds. Searches available source control, tickets, documents, chat, observability, error tracking, and analytics evidence in parallel, then separates direct evidence from inference. Use how for current runtime behavior."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Why

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before delegation.
2. Discover evidence through the tools, connectors, resources, and local repository access actually available in the current host. Do not assume a specific MCP registry, filesystem path, or vendor tool name.
3. Use `parallel` with read-only `explore` helpers for independent evidence categories. Use the lead agent or a read-only `review` helper for synthesis.
4. Resolve investigators through `model_role:fast_explore` and synthesis through `model_role:judgment`. Never require a vendor-specific model identifier.
5. When a category or helper capability is unavailable, record the gap and continue. Do not invent access or silently replace missing historical evidence with code-shape speculation.

## Purpose

Investigate the motivation and intent behind code or a product decision:

- why a design has its current shape;
- why one alternative was selected over another;
- which incidents or edge cases motivated defensive code;
- which customer, business, compliance, or operational constraint forced a choice;
- where a threshold or constant came from;
- whether the original rationale still applies.

**How** explains current behavior. **Why** explains the forces and decisions that produced it. Code is an anchor and a source of shipped facts, but rarely a complete source of intent.

## Operating posture

Work like an evidence-driven investigator:

- **Evidence before narrative.** Gather sources before choosing a story.
- **Cite every claim about intent.** Link it to a commit, pull request, ticket, document, chat message, incident, dashboard, error event, or query result.
- **Separate fact from inference.** Uncited intent is a hypothesis and must be labeled.
- **Surface contradictions.** Show disagreeing sources instead of quietly selecting one.
- **Treat null results as evidence.** A searched tracker or document system returning nothing says something about how the decision was recorded.
- **Name access gaps.** A source that was unavailable is different from a source that was searched and empty.
- **Calibrate confidence.** Direct design text supports stronger language than timing correlation or code-shape inference.
- **Resist rationalization.** A design that makes sense today may have shipped for a different reason or no documented reason at all.

Read `references/epistemics.md` before synthesis. Its confidence language is part of the deliverable.

## Step 1: Define the target and question

Identify the concrete target:

- files and line ranges;
- symbols, APIs, feature flags, constants, or data structures;
- the behavior or decision under investigation;
- the time range when the code or decision appeared;
- the specific “why” question.

When the referent is ambiguous, state the best interpretation from the current conversation and repository context, then proceed. Ask the user only when two interpretations would lead to materially different product questions and neither can be resolved by observation.

## Step 2: Establish a code anchor

Build a compact anchor before fanning out:

- relevant file and symbol pointers;
- blame or last-touch commits where available;
- recent history through renames;
- linked pull requests, issues, or change identifiers;
- tests and comments that encode motivating cases;
- ship dates, releases, or flag transitions that help bound searches.

Use the source-control tools exposed by the current environment: local Git, a repository connector, a hosting CLI, or equivalent APIs. Do not require one hosting provider.

The anchor is seed context, not the answer. Pass it to investigators so they search the historical record rather than rediscovering the same code.

## Step 3: Build the evidence coverage map

Enumerate available tools and resources through the active host and adapter. Map each one to at most one primary evidence category. A connector may expose several tools, but each investigator should own one evidence system so query vocabulary and result interpretation remain focused.

The seven categories are:

1. **Source control and review history.** Commits, pull requests, code review, code comments, tests, and linked change metadata. Best for implementation-time rationale and alternatives debated during review.
2. **Issue or ticket tracking.** Problems, projects, customer requests, deadlines, labels, and scope changes. Best for product, business, compliance, and planning forcing functions.
3. **Long-form documents.** Specifications, RFCs, ADRs, postmortems, design notes, meeting notes, and strategy documents. Best for explicit alternatives and finalized reasoning.
4. **Real-time team communication.** Chat threads, incident rooms, and informal decisions. Best for time-sensitive deliberation that never reached a formal document.
5. **Infrastructure observability.** Metrics, logs, traces, dashboards, monitors, and incidents. Best for runtime conditions, capacity limits, and thresholds that forced code changes.
6. **Error or exception tracking.** Error groups, events, stack traces, affected releases, and regressions. Best for defensive code, retry logic, guards, and corrective fixes.
7. **Product analytics and data warehouses.** Usage, experiments, feature exposure, billing, migrations, and distributions. Best for user-behavior evidence, launch decisions, scale assumptions, and data-derived constants.

Record for every category:

- the tool or source selected;
- whether it was searched;
- search terms and time range;
- positive findings;
- null result;
- unavailable access;
- a written reason for any deliberate skip.

The default is broad coverage across every available category. Do not skip merely because a source seems unlikely to contain the answer.

## Step 4: Run parallel investigators

Use one `parallel` fan-out with one read-only `explore` helper per available evidence category. When helpers are unavailable, run the category searches sequentially and keep the result sets separate until synthesis.

Each investigator receives:

1. the user's question;
2. the code anchor;
3. `references/investigator-prompt.md`;
4. the appropriate source guide under `references/sources/` or an adaptation based on `references/source-playbook.md`;
5. the incident-postmortem guide when the target looks defensive or operational;
6. a requirement to return citations, null results, query coverage, confidence, contradictions, and gaps.

Use `model_role:fast_explore` for category investigators. The helper may need authenticated connector access, so the adapter should choose an execution mode that preserves those tools while the prompt prohibits writes.

An investigator does not write repository files, modify tickets, post messages, or change external systems.

### Valid reasons to skip a category

A category may be skipped only when:

- no matching source or connector is available in the current environment; or
- the category is provably irrelevant to the target, such as runtime error tracking for a purely build-time artifact with no deployed path.

“Probably empty” is not a valid reason. Search it and report the null result.

For a very small target whose pull request explicitly and completely answers the question, the lead may avoid full fan-out only after checking which other available sources could contradict or qualify that rationale. State why broader searches would be redundant.

## Step 5: Synthesize with calibrated confidence

Synthesize on the lead agent or with one read-only `review` helper using `model_role:judgment`.

The synthesizer receives:

- the user's question;
- the code anchor;
- every investigator result, including empty and unavailable categories;
- `references/epistemics.md`;
- `references/synthesizer-prompt.md`.

Before presenting, spot-check load-bearing citations against the original source. Do not strengthen the synthesizer's confidence language during editing.

Distinguish:

- **Direct evidence.** A source explicitly states the rationale, constraint, alternative, or outcome.
- **Reasonable inference.** Several facts support a conclusion that no source states directly.
- **Competing hypotheses.** More than one explanation fits the record.
- **Unknown.** The available evidence cannot answer the question.

## Output format

**The question.** A concise restatement of what is being explained.

**Code or decision in question.** File, symbol, change, and time anchors.

**What the record says.** Direct evidence with source-specific citations. Include contradictions rather than averaging them away.

**What we can reasonably infer.** Each inference names the evidence chain and uses calibrated language such as “appears to,” “likely,” or “suggests.”

**Competing hypotheses.** For each plausible explanation, list evidence for and against it. Skip when the record clearly supports one explanation.

**What remains unknown.** Specific unanswered questions, unavailable sources, and searched sources that returned no relevant result.

**Sources consulted.** One line per category with the source, queries or scope, and result status: found, null, unavailable, or deliberately skipped with justification.

**Current relevance.** When evidence supports it, state whether the original rationale still appears active, has been superseded, or needs a new decision. Label this as inference unless a current source explicitly confirms it.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | independent evidence-category searches |
| `judgment` | confidence-calibrated synthesis and final presentation |

If no role override is available, inherit the parent session model.
