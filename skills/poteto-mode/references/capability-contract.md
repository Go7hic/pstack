# Capability contract

Playbooks speak in these capabilities. Adapters map them to a concrete runtime. Never call a tool that the active adapter does not define.

## Capabilities

| Capability | Intent | Fallback when unavailable |
| --- | --- | --- |
| `explore` | Read-only codebase search and tracing | Main agent uses local search/read tools |
| `implement` | Bounded code edits with disjoint write scope | Main agent edits directly |
| `review` | Independent critique of a design or diff | Main agent reviews; optionally second pass with a different rubric |
| `parallel` | Fan out independent slices at once | Run slices sequentially |
| `ask_user` | Product or preference decision only | Ask in plain text; never for facts you can observe |
| `verify` | Run the narrowest meaningful check on the real surface | State what you could not run and why |
| `model_role` | Prefer a role-appropriate model when overrides exist | Use the parent session model |

## Role hints (optional)

Adapters may map these roles to models. If unset, inherit the parent model.

| Role | Typical use |
| --- | --- |
| `fast_explore` | Broad read-only fan-out |
| `judgment` | Architecture, root cause, final synthesis, prose |
| `feature_impl` | Spec-driven implementation |
| `bug_impl` | High-stakes fix after evidence |
| `critic` | Adversarial review panel member |

## Rules for authors

1. Playbooks must not name Cursor `Task`, Codex `spawn_agent`, Claude `Agent`, OpenCode `task`, Droid tool JSON, or vendor model slugs.
2. Write steps as: "Using `explore`, …" / "Using `implement`, …" / "Using `parallel`, …".
3. Every playbook must remain correct when spawn tools are missing (collapse via `generic`), but authors should assume modern hosts **do** support `parallel`.
4. Runtime-specific notes belong only under `references/adapters/`.
