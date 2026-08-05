# Adapter: Codex

Use inside [OpenAI Codex](https://chatgpt.com/codex) (CLI / IDE) when multi-agent tools are available. This is the portable replacement for the old `codex-pstack` pack — install this repo’s skills under `~/.codex/skills/` and delete `codex-pstack`.

## Detect

- Multi-agent tools such as `multi_agent_v1.spawn_agent` (names may evolve; follow current tool metadata)
- Skills under `~/.codex/skills/` or project Codex skill paths
- Optional model override at `~/.codex/rules/pstack-models.md`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | `spawn_agent` with `agent_type: explorer`. Explicitly prohibit edits. Prefer local `rg`/reads first for tiny questions; fan out 2–4 explorers for broad subsystems. |
| `implement` | `spawn_agent` with `agent_type: worker` (or `default` when worker is unavailable). Bounded, disjoint file scopes. Prepend the poteto worker rubric from `../agents/poteto-agent.md` when the playbook wants full-style implementation. |
| `review` | Separate agents (`explorer` or `default`) with distinct rubrics. Prohibit edits in the prompt. Diverse `model` / `reasoning_effort` when the panel needs independent judgment. |
| `parallel` | Spawn **multiple** agents in one turn for independent slices. Continue non-overlapping lead work while they run. Do not wait serially unless scopes collide. |
| `ask_user` | Plain chat. Only product/preference forks that no experiment can settle. |
| `verify` | Local shell. Narrowest meaningful check first, then broaden. |
| `model_role` | Set `model` (+ `reasoning_effort` when supported) only from confirmed Codex slugs / the override file. Never copy Cursor model slugs. |

## Cursor → Codex translation

| Cursor / portable concept | Codex |
| --- | --- |
| `Task` / `Agent` / `task` | `multi_agent_v1.spawn_agent` (or current equivalent) |
| explore helper | `agent_type: explorer` |
| implement helper | `agent_type: worker` or `default` |
| `run_in_background: true` | spawn and continue local non-overlapping work |
| `readonly: true` | `explorer` + explicit no-edit rule |
| poteto-agent type | `worker`/`default` + `../agents/poteto-agent.md` prompt |
| Comment Sicko | `review` helper + `../agents/comment-sicko.md` rubric |
| Cursor model slug | Codex `model` + optional `reasoning_effort` from override file |

## Policy

- Prefer real parallel fan-out for how-complex, arena, swarm, interrogate, and playbook delegates.
- Critical-path synthesis stays on the lead agent. You own the final answer, patch, and verification.
- Keep worker write scopes disjoint. Tell workers not to revert or overwrite others’ edits.
- Close / stop completed agents when you no longer need them.
- If multi-agent tools are missing or spawn is denied, fall back to `generic.md` and say so.

## Model roles (defaults)

Resolve via `/setup-pstack` → `~/.codex/rules/pstack-models.md`. See `codex-models.md` for override shape and legacy path notes.

| Role | Typical use |
| --- | --- |
| `fast_explore` | how explorers, swarm workers, mechanical edits |
| `feature_impl` | feature / refactoring workers |
| `bug_impl` | bug-fix / perf / hillclimb |
| `judgment` | synthesis, prose, hardest design calls |
| `critic` | arena / architect / interrogate / how-critics panels |

Omit `model` when the override says `inherit-parent` / `auto`, or when a single parent model is enough.

## Poteto worker rubric

For playbook code delegates, spawn `worker`/`default` and include the instructions from `../agents/poteto-agent.md` in the agent prompt so style and principles load even without a Cursor `poteto-agent` type.
