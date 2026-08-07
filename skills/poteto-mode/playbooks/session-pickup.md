### Session pickup

**You own the resume point. Read the prior trail and do not redo completed work.** Use for “take over this,” “resume,” “continue from this handoff,” a prior session reference, or a pushed branch that another agent started.

A pickup inherits work already paid for: repository exploration, reproductions, decisions, commits, and verification. Re-deriving everything wastes context and can erase the value of the prior agent's independent perspective.

1. **Locate authorized evidence.** Prefer, in order:
   - a handoff document or decision trail supplied by the user;
   - repository state, branch history, pull-request metadata, and committed artifacts;
   - a first-class current-session or shared-session resource exposed by the active host;
   - a transcript path or URL explicitly provided for this task;
   - a compact user or lead-agent digest.

   Never scan broad user-history directories to guess which conversation is relevant. Do not read unrelated sessions.

2. **Build a reduced timeline.** Extract the original goal, constraints, decisions, failed paths, verification evidence, open concerns, and the last known action. Use `explore` on a long authorized trail and keep only the reduced timeline in the lead context.

3. **Reconstruct operational state.** Inspect the exact branch, base, worktree, commits, diff, untracked artifacts, open pull requests, CI state, and todo or decision-log files. Trust repository evidence over conversational memory when they disagree.

4. **Separate done from pending.** Map completed outcomes to commits or artifacts and identify the first unfinished unit. Do not rerun an expensive reproduction or redesign solely for reassurance. Recheck only when the prior evidence is missing, stale, contradictory, or tied to a different head.

5. **State the resume point.** Explain what is inherited, what remains, which assumptions still require verification, and which playbook owns the next action.

6. **Route remaining work.** Continue through the matching playbook: implementation, Bug fix, Babysit, Shipping, Pause safely, or another appropriate flow. Session pickup ends once ownership and state are reconstructed.

7. **Verify inherited completion claims.** Before declaring the overall goal complete, use `verify` against the original success condition on the current artifact. A prior summary is evidence of work, not proof of the final state.

When no usable trail or repository evidence exists, say what is missing and reconstruct only the minimum facts required to proceed. Do not pretend a lost session was recovered.

**Reply:** evidence sources used, where the previous work stopped, inherited completed work, anything deliberately rechecked and why, the exact resume point, routed playbook, and final outcome.
