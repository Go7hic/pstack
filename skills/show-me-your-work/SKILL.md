---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: one TSV row per decision with reason, evidence, and result. Local by default; commit it when a reviewer needs the trail to trust the outcome. Use for /show-me-your-work, autonomous runs, multi-phase work, or work reviewed after the user steps away."
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters.
---

# Show me your work

## Portability (required)

1. Read the `pstack` capability contract and the active host adapter before delegation.
2. Store the decision trail in the repository or current work directory, not in a vendor-specific session path.
3. Audit the trail against action evidence the current host exposes: repository state, tool-call records, authorized session resources, verification artifacts, or a lead-written timeline.
4. Use a read-only `review` helper with `model_role:critic` for fresh-eyes review when helpers are available. Otherwise run a second explicit review pass on the lead agent and state the limitation.
5. Never search unrelated conversation history to find evidence.

## Purpose

For work a human reviews after the fact, a decision trail lets them reconstruct what was chosen, why, and on what evidence without rerunning the task or reading an entire conversation.

Keep one canonical log for the run. Other skills reference this skill instead of inventing their own audit format.

## Format

Use one TSV file with one row per decision or checkpoint. TSV renders well in repository interfaces and spreadsheets, and it can be appended safely from shell scripts.

Start from `references/decision-log-template.tsv`. Columns:

- **ts.** ISO 8601 timestamp.
- **phase.** Phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** Plain-language reason. Name a principle only when it changed the decision.
- **evidence.** A compact pointer: commit, pull request, `file:line`, test output, trace, screenshot, query, or artifact path.
- **result.** Observable outcome such as `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, or `open`.

Example:

```text
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	measured the migration before starting	needed the real size before choosing a run shape	commit 3a9f1c2	five blockers found
2026-05-24T09:40:00Z	harness	captured the old UI before changing it	needed a stable visual baseline	baseline/	120 screenshots saved
2026-05-24T11:15:00Z	widget	moved styles without changing behavior	kept the diff narrow and reversible	commit 7c21e0a	pixel-diff 0; tests pass
2026-05-24T12:30:00Z	widget	reverted a helper's patch	its screenshots were blank and did not prove the claim	worktree reset	reverted
```

## Logging rows

Use `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` when available. It timestamps rows, writes the header on first use, removes tabs and newlines from cells, and neutralizes spreadsheet-formula prefixes.

If appending manually, apply the same safety rules. Treat generated and user-provided cell text as untrusted data.

Log:

- a design fork and selected alternative;
- a phase completion and verification result;
- a failed hypothesis, revert, or pivot;
- an accepted or dismissed review finding;
- a blocker and escalation;
- one row per iteration in an optimization or autonomous loop.

Do not log every command. A row should help a reviewer understand a decision or verify a checkpoint.

Apply **unslop** to log text. Use plain operational language rather than AI-style narration or principle jargon.

## Location and retention

By default, keep the log as an uncommitted working artifact:

- `decisions.tsv` for one run;
- `.audit/<task-slug>.tsv` when several runs coexist.

Commit the log only when the work is large, risky, long-running, or difficult enough that reviewers need the trail to trust the result. Do not commit secrets, private transcript content, credentials, or unrelated user context.

The log is append-only. A superseded decision receives a new row; never rewrite history to make the run look cleaner.

## Audit the trail

Before handoff, compare the log with the best authorized action evidence available:

1. repository commits, diffs, branches, and pull requests;
2. test, trace, screenshot, benchmark, or runtime artifacts;
3. tool-call or session resources exposed for the current task;
4. a bounded transcript or handoff explicitly supplied by the user;
5. the lead agent's reduced timeline when no first-class trace exists.

Check:

- every row maps to a real action or decision;
- every evidence pointer resolves and supports the claim;
- important forks, reversions, and failed approaches are present;
- incomplete or inconclusive results are labeled honestly;
- no row exposes private information or unrelated history;
- low-value padding is removed.

Fix the log when it disagrees with reality. Do not rewrite the story to defend the log.

## Fresh-eyes review

After the self-audit, use one read-only `review` helper through `model_role:critic`, preferably from a different model family than the main implementation model.

The reviewer receives the log, relevant diff or artifacts, original success condition, and authorized action evidence. It looks for:

- decisions with weak or missing evidence;
- verification claimed on the wrong surface;
- scope creep or premature architecture;
- symptom fixes presented as root-cause fixes;
- gaps that a casual reviewer would miss;
- rows whose result does not match the cited artifact.

The reviewer does not redo the task and does not edit files.

Every final report for a run with a decision trail includes an **Attention** section. Identify the review method or model role, then list specific rows or moments that deserve scrutiny. “No flags” is valid when the review found none.

## Reviewing the log

Read top to bottom and follow evidence pointers. A committed TSV should render as a table; in a terminal, use a TSV-aware viewer or:

```bash
column -s$'\t' -t decisions.tsv
```

A row whose evidence does not resolve or whose result is unverified is a gap, not a success.

## Composition

Other skills route decision logging here by name. Do not duplicate the column definitions in every playbook.

**Reply:** log path, retention decision, row count, self-audit result, fresh-eyes review, Attention items, and unresolved evidence gaps.
