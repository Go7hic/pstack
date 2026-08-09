# Contributing

## Goals

- Keep ystack's public API and documentation consistent.
- Keep playbook and principle intent aligned with upstream pstack where the fork has not intentionally diverged.
- Keep vendor tool names and concrete vendor model slugs out of portable skill bodies. Put runtime mechanics only in the shared adapter tree.
- Every workflow must remain correct under the `generic` adapter when multi-agent tools are unavailable.
- Preserve real parallel fan-out on hosts that expose agent-spawn tools.

## Naming boundary

- `ystack` is the public project, repository, install target, and primary entry skill.
- `pstack` identifies the upstream lineage and remains a compatibility alias.
- New user-facing docs and examples should use `/ystack`, `/setup-ystack`, `Go7hic/ystack`, and `ystack-models.*`.
- Do not remove legacy names without a separate migration plan and release note.

## Layout and sources of truth

- Installable skills live under `skills/<name>/SKILL.md`.
- `skills/ystack/SKILL.md` is the public entry.
- Shared runtime contracts currently remain under `skills/pstack/references/` for compatibility.
- `skills/poteto-mode/playbooks/` is the canonical playbook directory.
- `skills/pstack/references/adapters/` is the canonical adapter directory during the compatibility window.
- Agent rubrics, lifecycle guidance, and model schema are mirrored into poteto-mode as required by its relative references.

Do not edit both sides of a mirror independently. The audit rejects drift.

## Re-port helpers

After pulling newer upstream Cursor pstack sources:

```bash
python3 scripts/sync_mirrors.py --check
python3 scripts/sync_mirrors.py
```

`UPSTREAM_MANIFEST.json` is the source of truth for hand-maintained skills. Upstream imports must not overwrite ystack entries, compatibility aliases, local adapters, or portable-only workflows.

## Required audit

Run before every pull request:

```bash
python3 -m compileall -q scripts
python3 scripts/check_branding.py
python3 scripts/sync_mirrors.py --check
python3 scripts/audit_portability.py --strict
python3 scripts/check_markdown_links.py
python3 scripts/validate_model_override.py scripts/fixtures/model-override/valid.md
python3 scripts/port_to_portable.py --check-idempotent
```

## Semantic review after mechanical porting

1. Use the narrowest capability verb: `explore`, `implement`, `review`, `parallel`, `ask_user`, or `verify`.
2. Replace concrete model names with `model_role` and let the adapter resolve them.
3. Keep product decisions in `ask_user`; obtain observable facts through exploration or verification.
4. Keep write scopes disjoint before using `parallel`.
5. State fallbacks when the host cannot spawn helpers or drive the real runtime surface.
6. Preserve the public ystack naming boundary while retaining explicit upstream attribution.

## Host conformance

Live host results belong in `scripts/fixtures/conformance/HOST_MATRIX.md`. CI does not run remote agents; fill the matrix after smoke tests.

## skills.sh

- The `description` frontmatter field is the trigger surface and must stay quoted.
- Install the whole pack so the `ystack` entry, sibling skills, adapters, playbooks, and compatibility assets remain available together.
