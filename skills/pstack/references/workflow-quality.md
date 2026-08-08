# Workflow quality defaults

## Lightweight mode

If the task is a single local edit, a one-file explanation, or otherwise fits one pass, do not fan out. Lean simple when uncertain. Fan-out exists to reduce blind spots, not to decorate small work.

## Spec compliance

When an originating spec, ticket, or acceptance list exists, review against it as a first-class axis beside engineering quality. A clean diff that misses the named acceptance criteria is not done.

## External side effects

Pause before irreversible or externally visible actions unless the operator already granted them for this run:

- force-push to shared branches;
- production deploys;
- deletions of user data or shared resources;
- customer-facing messages;
- merging or closing someone else's PR without an explicit Shipping/Autopilot grant.

Reversible chat/ticket/doc updates may proceed, but log them in the decision trail for autonomous runs.

## Cost and concurrency budgets

Default budgets unless the operator raises them:

- How complex exploration: 2–4 helpers;
- Interrogate panel: 3–4 reviewers;
- Arena candidates: 2–4 runners plus one cross-judge;
- Autopilot / Orchestrate in-flight writers: keep the drainable window (about ten) rather than unbounded spawn.

When the host denies spawn or model selection, collapse immediately and state the degraded path instead of inventing another host's tool parameters.
