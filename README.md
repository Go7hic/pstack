# ystack

**ystack** is a portable multi-agent engineering skill stack for Agent Skills-compatible coding agents. It began as a portable adaptation of [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (poteto), then grew host adapters, portability audits, long-running playbooks, model-role configuration, and `living-spec` product-documentation convergence.

It preserves the upstream engineering system—principles, playbooks, `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, verification, and prose cleanup—without hard-coding one vendor runtime. Thin adapters map capability verbs to Claude Code, Codex, Droid, OpenCode, Cursor, and unknown Agent Skills hosts. Modern hosts keep real parallel subagents; single-agent runtimes degrade explicitly and safely.

## Install

Install the complete pack globally. The `ystack` entry coordinates sibling skills and shared compatibility assets, so keep `-s '*'`:

```bash
npx skills add Go7hic/ystack -g -s '*' -y
```

See [INSTALL.md](./INSTALL.md) for per-agent selection, model override paths, migration notes, and smoke tests. After installation, restart or reload the coding agent so it rescans skills.

Cursor users may use ystack through its Cursor adapter or keep Cursor's official pstack plugin. Do not enable both as competing top-level routers in the same session.

## Public entry points

- `/ystack` — primary adapter-first router.
- `/poteto-mode` — full upstream-style mode contract.
- `/setup-ystack` — configure role and panel models.
- `/pstack` and `/setup-pstack` — legacy compatibility aliases.

## What is included

| Area | Skills and assets |
| --- | --- |
| Entry | `ystack`, `poteto-mode`; legacy alias `pstack` |
| Workflow | `how`, `why`, `recall`, `blast-radius`, `architect`, `arena`, `swarm`, `interrogate`, `figure-it-out`, `teach`, `reflect`, `automate-me`, `setup-ystack`, `show-me-your-work`, `living-spec`, `create-verification-skill`, `maintain-verification-skill`, `tdd`, `typescript-best-practices` |
| Quality | `unslop`, `no-comments`, `technical-writing`, `bro` |
| Principles | all 21 `principle-*` leaf skills |
| Playbooks | 23 mirrored under `skills/poteto-mode/playbooks/` and the legacy runtime tree `skills/pstack/playbooks/` |
| Runtime | capability contract plus `generic`, `claude-code`, `codex`, `droid`, `opencode`, and `cursor` adapters |
| Agent rubrics | Poteto worker and Comment Sicko review rubrics |
| Optional | `references/automations/benny`, a Cursor-oriented source pack that is not installed as Agent Skills |

## How portability works

1. Skills express intent with the capability verbs `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, and `model_role`.
2. Before delegation, the lead reads the matching host adapter from the shared runtime tree.
3. The adapter maps those verbs to the host's actual tools, helper types, model controls, and fallback behavior.
4. Parallel fan-out remains the default when the host exposes agent-spawn tools. The workflow collapses to the lead agent only when spawning is missing or denied.
5. `/setup-ystack` resolves role-appropriate models through a host-specific override file. Portable skills must not require another host's model slugs.
6. The lead agent always owns synthesis, final patch judgment, and verification on the narrowest meaningful real surface.

The portable layer is an instruction protocol, not an emulator. It preserves workflow intent across hosts, but it cannot manufacture features a host does not expose. A runtime without subagents, model selection, browser control, or persistent modes uses the documented fallback and states the limitation.

## Naming and compatibility

`ystack` is the public project and repository name. The internal `skills/pstack/` namespace remains temporarily because it is both the upstream lineage name and the compatibility home used by existing installations. New documentation and commands should prefer `ystack`.

Model overrides prefer:

- Cursor: `ystack-models.mdc`
- Codex: `ystack-models.md`
- shared Agent Skills hosts: `ystack-models.md`

Adapters continue to honor legacy `pstack-models.*` files so existing users can migrate without losing configuration.

## Living product documentation

`living-spec` is an optional, solo-friendly documentation layer for projects that use ystack without a full specification framework. It keeps three concerns separate:

- `docs/product/` describes the product's current, verified behavior;
- `docs/changes/` holds a temporary brief only for changes that span sessions, pull requests, or several modules;
- `docs/decisions/` records durable, non-obvious technical decisions with meaningful alternatives.

The skill does not require documentation for internal refactors or trivial edits. It first inspects the repository for an existing canonical system such as OpenSpec, ADRs, or product docs, and reuses that system instead of creating a competing source of truth. Feature work converges documentation only after real-surface verification.

## Session and mode behavior

`/poteto-mode` is sticky when the active host supports persistent skill or mode state. On hosts without that lifecycle, treat it as active for the current conversation and invoke `/ystack` or `/poteto-mode` again after a fresh session or context reset.

## Maintenance and audits

The repository contains structural, branding, and portability audits:

```bash
python3 scripts/check_branding.py
python3 scripts/audit_portability.py --strict
python3 scripts/sync_mirrors.py --check
python3 scripts/check_markdown_links.py
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) and [UPSTREAM_MANIFEST.json](./UPSTREAM_MANIFEST.json) before syncing a newer upstream revision. Mechanical regex porting is followed by semantic review; capability verbs must describe the actual job rather than merely replacing vendor vocabulary.

## Credits

ystack is adapted from Cursor pstack by Lauren Tan. See [NOTICE.md](./NOTICE.md) and [LICENSE](./LICENSE) for attribution and MIT licensing.
