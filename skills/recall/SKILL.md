---
name: recall
description: "Reconstruct recent working context from authorized conversation history, live repository state, and the shared engineering record, then return a tight current-state brief. Use for \"recall my work on X\", \"catch me up\", \"what have I been working on\", or \"where did I leave off\"."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Recall

## Portability (required)

1. Read the `pstack` capability contract and the active host adapter before delegation.
2. Obtain conversation history only through resources the host exposes for the current user and authorized scope. Never assume one transcript directory or schema.
3. Use `parallel` with read-only `explore` helpers for independent history slices and shared-record sources.
4. Resolve history mining through `model_role:fast_explore` and final synthesis through `model_role:judgment`.
5. When history or helper access is unavailable, use the visible conversation, repository state, and a stated evidence gap rather than inventing memory.

## Purpose

Before work starts or resumes, rebuild the user's recent context and hand back a concise capsule of where things stand and what should happen next.

Recall combines two records:

- **Personal working history.** Goals, decisions, corrections, branches, pull requests, and unfinished threads from authorized prior conversations.
- **Shared engineering record.** Source control, tickets, documents, team discussion, incidents, errors, and current production or repository state. Use **why** to search this record.

A feature with a long bug tail cannot be reconstructed from personal conversations alone. Conversely, tickets and commits may omit the user's intent. The brief reconciles both.

## Process

### 1. Classify the request

Route one specific handoff or transcript to the **Session pickup** playbook. Route “turn my habits into a skill” to **automate-me**. Recall is for rebuilding context across several recent threads before choosing the next move.

When the user already provides a complete state capsule with branch, paths, decisions, and current goal, use it and skip unnecessary history mining.

### 2. Lock the scope

State:

- topic or named target;
- time window, defaulting to the last seven days when “recent” is unspecified;
- active workspace or repository;
- whether the user wants personal activity only or a full shared-record sweep.

Do not silently reinterpret “all” as a smaller window. Do not read another workspace's history without authorization.

### 3. Mine authorized working history

Use the best current-host source, in order:

1. a first-class conversation-history or session-search capability;
2. a user-provided export, handoff, transcript reference, or saved context resource;
3. the visible current conversation;
4. a stated gap when none is available.

For a broad corpus, use `parallel` with bounded `explore` helpers, one time or topic slice per helper. Helpers read only the scoped material and return one block per relevant thread:

- user's goal;
- decisions and corrections;
- work completed;
- open questions and blockers;
- branches, pull requests, tickets, files, or artifacts;
- evidence pointer supplied by the host.

Order sources by real timestamps exposed by the host. Skip the current conversation, helper-only noise, and unrelated sessions. For one or two threads, search directly instead of fanning out.

### 4. Sweep the shared record

When the topic names a feature, file, subsystem, project, or bug, run **why** with a current-state question:

> What is the current state, what has already been tried, what failed or was reverted, and what are users or operators still reporting?

Run its available source investigators in parallel with history mining. Preserve positive findings, null results, contradictions, and unavailable-source gaps.

Skip this step only for pure personal activity recall with no named technical target, such as “what did I work on this week?”

### 5. Verify live state

History is not current truth. Check every surfaced branch, pull request, ticket, release, or artifact through live repository and connected-system tools.

Confirm:

- merged, open, closed, or reverted status;
- exact branch and head revision;
- dirty or uncommitted work;
- current CI and review state when relevant;
- whether a claimed fix still exists in the current code;
- whether an old blocker has already been resolved.

When the answer depends on what an earlier agent actually did, use an authorized full action trace when available. Do not infer tool usage from a summary.

### 6. Write the brief

Stay on the named topic. An adjacent thread appears only when it blocks the next move.

## Output contract

- **Capsule.** At most five bullets describing the work and overall state.
- **Threads.** One line each with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`.
- **Problems.** At most five recurring symptoms, failed approaches, reverted fixes, or unresolved risks.
- **Evidence gaps.** History or shared sources that were unavailable or searched without useful results.
- **Next move.** One concrete highest-value action.

Apply **unslop** to the brief. Cite working-history findings through the evidence identifiers the host provides and shared-record findings through their native source references. Remove private context before any public output.

**Reply:** the brief in the contract above.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | scoped conversation-history and shared-record mining |
| `judgment` | reconciliation, current-state synthesis, and next-action selection |

If no role override is available, inherit the parent session model.
