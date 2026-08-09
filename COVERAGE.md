# Coverage

ystack aims for full upstream pstack capability coverage, ported to Agent Skills plus host adapters and extended with portable-only workflows.

## Skills (48)

The pack includes the upstream-derived skill set, the public `ystack` entry and `setup-ystack`, the `living-spec` addition, and legacy `pstack` / `setup-pstack` compatibility aliases.

## Playbooks (23)

Mirrored in `skills/poteto-mode/playbooks/` and `skills/pstack/playbooks/` during the compatibility window.

## Intentionally adapted (not 1:1 Cursor runtime)

| Upstream | ystack treatment |
| --- | --- |
| `Task` / `subagent_type` | capability verbs + per-host adapters |
| Claude Code `Agent`/`Task` | `adapters/claude-code.md` |
| Droid `Task` + custom droids | `adapters/droid.md` |
| OpenCode `task` | `adapters/opencode.md` |
| Codex multi-agent | `adapters/codex.md` |
| `poteto-agent` / Comment Sicko types | portable rubric markdown |
| Cursor model slugs | `model_role` + `/setup-ystack` override file |
| `AskQuestion` | `ask_user` |
| `/loop` | host long-running mechanism when available, otherwise explicit continuation |
| `watch-pr` scripts | optional; Babysit falls back to the active forge interface |
| upstream poteto-mode scripts | omitted when they depend on Cursor-only runtime behavior |
| Benny automations | kept as non-installable source templates under `references/automations/benny/` |

## Portable-only additions

- `ystack` — primary public entry.
- `setup-ystack` — preferred model configuration entry.
- `living-spec` — lightweight current-product-truth convergence for solo projects.
- portability, mirror, model-schema, link, and branding audits.

## Compatibility

- `/pstack` routes to `/ystack`.
- `/setup-pstack` routes to `/setup-ystack`.
- legacy `pstack-models.*` files remain readable after ystack-named overrides become preferred.
- upstream names remain in credits, lineage metadata, and compatibility paths.

## External

`deslop`, `control-cli`, and `control-ui` from `cursor-team-kit` are not bundled; use equivalent host capabilities.
