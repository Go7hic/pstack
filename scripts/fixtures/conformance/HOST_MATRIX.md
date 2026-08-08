# Host conformance matrix

These are smoke expectations for portable pstack. Mark results only after a live host run. In-repo CI does not execute remote agents.

| Case | Claude Code | Codex | OpenCode | Droid | Generic + spawn | Generic no spawn |
| --- | --- | --- | --- | --- | --- | --- |
| `/how` simple: no unnecessary fan-out | | | | | | |
| `/how` complex: 2–4 explorers | | | | | | |
| `/arena`: isolated candidates, cross-judge, graft, verify | | | | | | |
| `/interrogate`: independent reviewers + lead judgment | | | | | | |
| Feature: disjoint worker scope + lead diff review | | | | | | |
| Bug fix: reproduce, root cause, fix, same-surface verify | | | | | | |
| Denied model selection degrades to parent model | | | | | | |
| Denied spawn collapses to lead and is stated | | | | | | |
| No invented tool params from another host | | | | | | |

Fill cells with `pass`, `pass-degraded:<note>`, or `fail:<note>`.
