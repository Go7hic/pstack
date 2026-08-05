# Codex model notes

Companion to `adapters/codex.md`. Validate every slug against **current** Codex tool metadata before use; this file is illustrative.

## Override file

Prefer:

```text
~/.codex/rules/pstack-models.md
```

Legacy name from the old pack (still honored if present):

```text
~/.codex/rules/codex-pstack-models.md
```

`/setup-pstack` should write the new path. Shape:

```text
feature, refactoring: <slug>/<effort>
bug-fix, perf-issue, hillclimb: <slug>/<effort>
judgment and prose: <slug>/<effort>
how explorer: <slug>/<effort>
how explainer: <slug>/<effort>
how critics: <slug>/<effort>, <slug>/<effort>, <slug>/<effort>
arena runners: ...
architect runners: ...
interrogate reviewers: ...
swarm workers: ...
```

Use `inherit-parent` or `auto` to omit `model` on that role.

## Role → intent

| Role / label | Intent |
| --- | --- |
| feature, refactoring | everyday implementation |
| bug-fix, perf-issue, hillclimb | high-stakes reasoning after evidence |
| judgment and prose | synthesis, architecture, unslop-sensitive replies |
| how explorer / swarm workers | fast read-only or mechanical fan-out |
| how explainer / why synthesizer | final explanation quality |
| *critics / runners / reviewers panels | diverse families when available |

## Effort

When the API separates reasoning effort from the model slug, set it from the override (`high`, `max`, `ultra`, …). Do not invent effort values the tool rejects.
