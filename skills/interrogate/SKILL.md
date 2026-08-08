---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Interrogate

## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before delegation.
2. Use `parallel` with read-only `review` helpers for the reviewer panel. Keep synthesis and final categorization on the lead agent.
3. Resolve reviewer models through `model_role` or the host override file. Never require a vendor-specific model identifier.
4. Do not auto-apply reviewer suggestions. The deliverable is a synthesized verdict.
5. When helper spawning or model selection is unavailable, run the same rubric sequentially on the lead agent, keep notes separate until synthesis, and state the degraded path.

## Purpose

Spawn independent reviewers to adversarially review code changes. Each reviewer gets the same prompt and rubric. The adversarial signal comes from model diversity, not assigned personas. Models differ in blind spots, priors, and reasoning patterns. Agreement across models is high-confidence signal; lone-model findings are worth reading but lower confidence.

## Step 1: Decide scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff <base>...HEAD` for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents plus any surrounding context the reviewers need. Prefer path pointers over dumping large files into every prompt when helpers can read the workspace.

## Step 2: State the intent

Before spawning reviewers, state the intent explicitly. What is this code trying to accomplish? Derive this from:

- the user's message;
- commit messages;
- PR description if one exists;
- the code itself.

Write one clear paragraph. Reviewers challenge whether the work achieves the intent well, not whether the intent itself is correct. If the intent is ambiguous in a way that would change the review, use `ask_user` once; otherwise state the best current reading and proceed.

## Step 3: Spawn reviewers

Use `parallel` to launch the reviewer panel in one turn when the host supports it. Prefer the `interrogate reviewers` list from the local pstack model override file when present, one reviewer per entry. Otherwise use this default panel:

| Reviewer | Model role |
| --- | --- |
| A | `judgment` |
| B | `bug_impl` |
| C | `fast_explore` |
| D | `critic` (different family when possible) |

Every helper is a read-only `review` worker. Instruct each helper not to edit files or post external comments.

If a configured model cannot be resolved by the active adapter, pick the closest available equivalent (prefer the strongest reasoning tier in the same family), continue the review, and note the substitution. Open a separate follow-up to fix the override file. Values such as `inherit-parent` or `auto` mean omit an explicit model and inherit the parent session.

Read `references/reviewer-prompt.md` and fill the template with:

1. the stated intent;
2. the diff or file contents / path pointers;
3. the review rubric from `references/rubric.md`;
4. the code-quality lens from `references/code-quality-review.md`.

The same filled template goes to all reviewers. Each reviewer returns structured findings as described in the prompt template.

## Step 4: Synthesize

As results come back, build a unified picture:

1. Parse all findings from the reviewers.
2. Identify consensus. Findings raised by 2+ reviewers independently are highest signal.
3. Identify lone-model findings. Still worth reading, but weight accordingly.
4. Deduplicate. Different models may describe the same issue differently. Merge these and note which reviewers raised it.
5. Note disagreements. If one reviewer flags something and another explicitly says the opposite, keep that tension in the verdict.

## Step 5: Lead judgment

The lead is a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework. Reviewers only see a slice of the codebase. The lead has the full context: goal, constraints, timeline, and tradeoffs already considered. Use that context aggressively.

Categorize every finding:

- **Act on.** Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider.** Legitimate points, but it is unclear they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted.** Technically valid but not actionable now. Context-dependent, premature, or low-impact.
- **Dismissed.** Wrong, nitpicky, or missing context. Brief explanation why.

For each finding include:

- which reviewer(s) raised it;
- the category;
- a one-line rationale for the categorization.

## Output format

### Intent

> [The stated intent paragraph from Step 2]

### Reviewers

- Reviewer [label]: [model role or resolved model], [N findings]

### Act On

Findings that should be addressed. For each: description, which reviewers raised it, why it matters.

### Consider

Findings worth thinking about. For each: description, which reviewers raised it, tradeoff involved.

### Noted

Valid but low-priority. Brief list.

### Dismissed

Rejected findings with brief rationale so the user can override the lead judgment.

### Agreement Map

Where reviewers agreed, where they diverged, and what the pattern implies.

## Model roles

| Role | Use |
| --- | --- |
| `fast_explore` | breadth and mechanical inconsistency hunting |
| `bug_impl` | correctness and failure-mode pressure |
| `judgment` | architecture and maintainability judgment |
| `critic` | adversarial / panel diversity |

If no role override is available, inherit the parent session model and say so.
