# Adapter: Codex

Use inside OpenAI Codex CLI or IDE when multi-agent tools are available. This pack replaces the obsolete standalone `codex-pstack` pack; install ystack under the normal Codex skills tree and remove the old standalone pack.

## Detect

- Current Codex multi-agent spawn tools
- Skills under `~/.codex/skills/` or project Codex skill paths
- Preferred model override at `~/.codex/rules/ystack-models.md`
- Legacy fallback at `~/.codex/rules/pstack-models.md` or `codex-pstack-models.md`

## Capability map

| Capability | How |
| --- | --- |
| `explore` | Spawn an explorer agent and explicitly prohibit edits. Use local reads first for tiny questions. |
| `implement` | Spawn a worker or default agent with bounded, disjoint file scope. Include the Poteto worker rubric when requested. |
| `review` | Separate read-only agents with distinct rubrics and, when useful, diverse models or reasoning effort. |
| `parallel` | Spawn multiple independent agents in one turn and continue non-overlapping lead work. |
| `ask_user` | Plain chat for product or preference decisions only. |
| `verify` | Local shell and available runtime tools, narrowest meaningful check first. |
| `model_role` | Set model and optional reasoning effort only from confirmed Codex identifiers or the override file. |

## Cursor to Codex translation

| Portable concept | Codex |
| --- | --- |
| helper spawn | current Codex multi-agent spawn tool |
| explore helper | explorer agent |
| implement helper | worker or default agent |
| background work | spawn and continue non-overlapping lead work |
| read-only intent | explorer plus explicit no-edit rule |
| Poteto worker | worker/default plus `../agents/poteto-agent.md` |
| Comment Sicko | review helper plus `../agents/comment-sicko.md` |
| model role | confirmed Codex model plus optional reasoning effort |

## Policy

- Prefer real parallel fan-out for broad How, Arena, Swarm, Interrogate, and independent playbook delegates.
- Critical-path synthesis stays on the lead.
- Keep worker write scopes disjoint.
- Close completed agents when they are no longer needed.
- Fall back to `generic.md` when multi-agent tools are unavailable or denied.

## Model roles

Resolve through `/setup-ystack` and `~/.codex/rules/ystack-models.md`. If absent, read legacy pstack paths. See `codex-models.md` for the override shape.

| Role | Typical use |
| --- | --- |
| `fast_explore` | broad reading and mechanical work |
| `feature_impl` | feature and refactoring workers |
| `bug_impl` | bug, performance, and hillclimb work |
| `judgment` | synthesis, prose, and hard design calls |
| `critic` | Arena, Architect, Interrogate, and How critique panels |

Omit an explicit child model when the override says `inherit-parent` or `auto`.

## Poteto worker rubric

For code delegates, include `../agents/poteto-agent.md` in the worker prompt so the full engineering discipline loads without a vendor-specific helper type.
