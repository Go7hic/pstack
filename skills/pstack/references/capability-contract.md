# Capability contract

Version: `1.0.0`

Playbooks speak in these capabilities. Adapters map them to a concrete runtime. Never call a tool that the active adapter does not define.

## Capabilities

| Capability | Intent | Required? | Fallback when unavailable |
| --- | --- | --- | --- |
| `explore` | Read-only codebase search and tracing | required | Main agent uses local search/read tools |
| `implement` | Bounded code edits with disjoint write scope | required | Main agent edits directly |
| `review` | Independent critique of a design or diff | required | Main agent reviews; optionally second pass with a different rubric |
| `parallel` | Fan out independent slices at once | optional / degradable | Run slices sequentially and state the collapse |
| `ask_user` | Product or preference decision only | required | Ask in plain text; never for facts you can observe |
| `verify` | Run the narrowest meaningful check on the real surface | required | State what you could not run and why |
| `model_role` | Prefer a role-appropriate model when overrides exist | optional / degradable | Use the parent session model |

## Role hints (optional)

Adapters may map these roles to models. If unset, inherit the parent model.

| Role | Typical use |
| --- | --- |
| `fast_explore` | Broad read-only fan-out |
| `judgment` | Architecture, root cause, final synthesis, prose |
| `feature_impl` | Spec-driven implementation |
| `bug_impl` | High-stakes fix after evidence |
| `critic` | Adversarial review panel member |

## Adapter self-check

Before the first helper spawn, the lead should know for the active host:

1. which helper types exist;
2. whether true `parallel` fan-out works;
3. concurrency or queue limits;
4. whether `model_role` can select a concrete model;
5. which external connectors are available for evidence (`why`, tickets, logs);
6. whether browser/CLI/runtime control exists for `verify`;
7. what mode or skill persistence the host actually enforces.

Document host-specific answers only under `references/adapters/`.

## Read-only intent vs tool access

Read-only intent forbids writes to the repository and external mutating actions. It must not strip connected evidence tools (ticket readers, log queries, docs fetchers) that the investigation needs. Separate "may write" from "may read connected systems".

## Rules for authors

1. Playbooks must not name Cursor `Task`, Codex `spawn_agent`, Claude `Agent`, OpenCode `task`, Droid tool JSON, or vendor model slugs.
2. Write steps as: "Using `explore`, …" / "Using `implement`, …" / "Using `parallel`, …".
3. Every playbook must remain correct when spawn tools are missing (collapse via `generic`), but authors should assume modern hosts **do** support `parallel`.
4. Runtime-specific notes belong only under `references/adapters/`.
5. Bump this contract version when capability meanings or required/optional classifications change.
