# Contributing

## Goals

- Keep playbook and principle **intent** aligned with upstream pstack.
- Keep vendor tool names and concrete vendor model slugs out of portable skill bodies. Put runtime mechanics only in `skills/pstack/references/adapters/`.
- Every workflow must remain correct under the `generic` adapter when multi-agent tools are unavailable.
- Preserve real parallel fan-out on hosts that expose agent-spawn tools. Portability must not collapse the pack to the lowest common denominator.

## Layout and sources of truth

- Installable skills live under `skills/<name>/SKILL.md` and follow the Agent Skills layout used by skills.sh.
- Shared runtime contracts live under `skills/pstack/references/{capability-contract.md,adapters/,agents/,host-lifecycle.md,model-override.schema.json}`.
- `skills/poteto-mode/playbooks/` is the canonical playbook directory.
- `skills/pstack/references/adapters/` is the canonical adapter directory.
- `skills/pstack/references/capability-contract.md` is canonical.
- Agent rubrics, `principles-summary.md`, `host-lifecycle.md`, and the model-override schema exist only under `skills/pstack/references/`.

Do not edit both sides of a mirror independently. The portable audit rejects drift.

## Re-port helpers

After pulling newer upstream Cursor pstack sources:

```bash
# Verify mirrors without rewriting (CI uses this).
python3 scripts/sync_mirrors.py --check

# Refresh mirrors after local playbook/adapter/agent edits.
python3 scripts/sync_mirrors.py
```

`UPSTREAM_MANIFEST.json` is the source of truth for hand-maintained `SKILL.md` names. Import still syncs `poteto-mode` playbooks/references while protecting those SKILL files and local adapters/agents.

## Required audit

Run this before every pull request:

```bash
python3 -m compileall -q scripts
python3 scripts/sync_mirrors.py --check
python3 scripts/audit_portability.py --strict
python3 scripts/check_markdown_links.py
python3 scripts/validate_model_override.py scripts/fixtures/model-override/valid.md
python3 scripts/port_to_portable.py --check-idempotent
```

The baseline audit checks:

- skill frontmatter and unique skill names;
- the complete playbook and adapter inventories;
- byte-identical playbook, adapter, and capability-contract mirrors;
- Cursor-only frontmatter keys;
- portability smells (vendor fields, Cursor paths/control surfaces, thin mechanical blocks, rewrite artifacts);
- regression fixtures under `scripts/fixtures/portability/` for every portability pattern.

Repository-wide non-strict audit should stay at `0 error(s), 0 warning(s)` unless a finding is intentionally introduced and tracked. The strict changed-file scan rejects regressions in files a PR touches.

## Semantic review after mechanical porting

Regex passes are only the first step. Review every changed skill for meaning:

1. Replace vendor calls with the narrowest capability verb. Read-only investigation uses `explore`; code changes use `implement`; independent criticism uses `review`.
2. Replace concrete model names with `model_role` and let the active adapter or override resolve a real model.
3. Keep product decisions in `ask_user`; obtain observable facts through exploration or verification.
4. Keep write scopes disjoint before using `parallel`.
5. State the fallback when the host cannot spawn helpers or drive the real runtime surface.
6. Remove claims that a mode, transcript path, MCP discovery mechanism, or background task API exists on every host.

A mechanically valid sentence can still be semantically wrong. Phrases such as “`explore` / `implement` helper” are a sign that the port has not chosen the actual capability.

## Host conformance

Live host results belong in `scripts/fixtures/conformance/HOST_MATRIX.md`. CI does not run remote agents; fill the matrix after smoke tests on each supported host.

## skills.sh

- The `description` frontmatter field is the trigger surface and must stay quoted for reliable parsing.
- Prefer installing the whole pack so the `pstack` entry skill, adapters, playbooks, and leaf skills remain available together.
