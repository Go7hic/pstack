### Worktree and simulator cleanup

**You own the disk and the safety gate.** Prune merged or abandoned git worktrees and stale iOS simulators to reclaim space. Deletion is irreversible, so every step guards against deleting something in use or holding uncommitted work.

1. Snapshot and audit. Record `df -h /`, then run `scripts/worktree-audit.sh` when present (principle-build-the-lever). It reads paths from `git worktree list`, never hand-typed, since a hand-typed path can miss host-managed worktree roots (principle-encode-lessons-in-structure). It classifies each worktree by size, age, merge state, uncommitted work, PR state, and the newest session that touched it, then suggests a bucket. Session scanning is slow, so run it non-blocking when the adapter supports it.
2. The bucket is advice, not permission. Active or pinned sessions are the real artifact (principle-prove-it-works). Get that set from the user or the host UI and cross-check every candidate. The lever has marked `safe` a worktree the user still needs, so the active set wins.
3. Verify usage before deleting. For every doubtful row, use `parallel` with read-only `explore` helpers to inspect session evidence and report whether the session is active and which worktrees it touches (principle-guard-the-context-window). An active session can own sibling arena or repro worktrees even when those names never appear in the sidebar.
4. Pause on irreversible loss. `wip:N` is N tracked uncommitted edits. Show the diff and get a decision first, since removing a clean worktree is recoverable from its branch but uncommitted work is gone. `scratch:N` is untracked throwaway, safe to drop, but name the files. Per Autonomy, clean and merged and not-in-use proceeds; `wip` and in-use pause.
5. Prune the confirmed set. Per path, `git worktree remove --force <path>`; if the dir survives on ignored build artifacts, `rm -rf` it, then `git worktree prune`. Branch refs survive, so no commits are lost. Confirm with `df -h /` and re-list.
6. Simulators and other reclaimers. Simulators are usually the next-biggest win. `xcrun simctl --set testing delete all` (XCTestDevices clones), `xcrun simctl delete unavailable`, and `xcrun simctl runtime list` then `runtime delete <id>` for old runtimes. More when needed: Xcode `DerivedData` and `iOS DeviceSupport`; host-local IDE state caches only when the user names them; package caches (pnpm, uv, brew, yarn). Clear only caches the user has not said to keep.

This is the one playbook that deletes user state with no code review to catch a slip, so the gates above are the review.

**Reply:** `df -h /` before and after with space reclaimed, the worktrees pruned, and a one-line reason for each held back (in-use by which chat, or uncommitted work).
