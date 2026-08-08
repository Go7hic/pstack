### Opening a PR

Run this at the end of an implementation playbook when the user asked for a reviewable pull request or the repository workflow clearly requires one.

1. **Protect unrelated work.** Use a clean branch or worktree based on the intended base. Do not overwrite dirty changes that belong to another task. When several helpers contribute, keep their write scopes or worktrees separate and integrate deliberately on the owning branch.
2. **Verify the final head.** Run focused tests, the broader regression gate, and the matching real-surface verification. Re-run checks after the final rebase or conflict resolution so evidence refers to the head that will be reviewed.
3. **Review the diff.** Run **interrogate** when risk or ambiguity warrants it. Apply **no-comments** to comment quality and **unslop** to prose. Perform a simplicity pass before commit; do not depend on an optional cleanup tool being installed.
4. **Shape the commits.** Use small, ordered commits that tell the implementation story. Amend when a correction belongs to the commit just created; add a new commit when the change is independently reviewable. Do not hide unrelated work in the branch.
5. **Refresh the base safely.** Rebase or merge according to the repository's documented policy. Never rewrite shared history or a published stack without the required owner checkpoint.
6. **Open the pull request through the active forge interface.** Use the connected repository tool, hosting API, or available CLI. Include:
   - user-visible outcome;
   - design choice and trade-off;
   - verification commands and results;
   - runtime evidence or known verification gap;
   - migration, rollout, or compatibility notes;
   - follow-up work explicitly out of scope.
7. **Confirm the created artifact.** Read back the pull request metadata and exact head SHA before reporting it. Do not fabricate or infer a URL.
8. **Route follow-up correctly.** Return the pull-request reference to the lead agent. Start the pstack **Babysit** playbook only when the user asks to monitor, get it green, address threads, or make it merge-ready. Opening a pull request alone does not authorize merging or long-running monitoring.

For stacked work, use the team's existing stack workflow. Keep slices small, ordered, and visible to reviewers; do not require one specific stacking product.

**Reply:** pull-request reference, base and exact head, commit sequence, verification performed, known gaps, and whether Babysit was requested.
