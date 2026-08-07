# Contributing

## Goals

- Keep playbook and principle **intent** aligned with upstream pstack.
- Keep vendor tool names and concrete vendor model slugs out of portable skill bodies. Put runtime mechanics only in `skills/pstack/references/adapters/`.
- Every workflow must remain correct under the `generic` adapter when multi-agent tools are unavailable.
- Preserve real parallel fan-out on hosts that expose agent-spawn tools. Portability must not collapse the pack to the lowest common denominator.

## Layout and sources of truth

- Installable skills live under `skills/<name>/SKILL.md` and follow the Agent Skills layout used by skills.sh.
- Shared runtime contracts live under `skills/pstack/references/{capability-contract.md,adapters/,agents/}`.
- `skills/poteto-mode/playbooks/` is the canonical playbook directory. Mirror it to `skills/pstack/playbooks/` after edits.
- `skills/pstack/references/adapters/` is the canonical adapter directory. Mirror it to `skills/poteto-mode/references/adapters/` after edits.
- `skills/pstack/references/capability-contract.md` is canonical. Keep the copy under `skills/poteto-mode/references/` byte-identical.
- Agent rubrics and `principles-summary.md` exist only under `skills/pstack/references/`; they are not mirrored into `poteto-mode`.

Do not edit both sides of a mirror independently. The portable audit rejects drift.

## Re-port helpers

After pulling newer upstream Cursor pstack sources:

```bash
# Copy upstream skills, then run the mechanical passes.
python3 scripts/port_to_portable.py
python3 scripts/port_pass2.py

# Refresh mirrors from their canonical directories.
rsync -a --delete skills/poteto-mode/playbooks/ skills/pstack/playbooks/
rsync -a --delete skills/pstack/references/adapters/ skills/poteto-mode/references/adapters/
cp skills/pstack/references/capability-contract.md \
  skills/poteto-mode/references/capability-contract.md
```

Adapters, `setup-pstack`, and portable entry skills are hand-maintained. Do not blindly overwrite them from upstream.

## Required audit

Run this before every pull request:

```bash
python3 -m compileall -q scripts
python3 scripts/audit_portability.py
python3 scripts/audit_portability.py --strict --changed-from origin/main
```

The baseline audit checks:

- skill frontmatter and unique skill names;
- the complete playbook and adapter inventories;
- byte-identical playbook, adapter, and capability-contract mirrors;
- Cursor-only frontmatter keys;
- portability smells such as concrete Cursor model slugs, `subagent_type`, `AskQuestion`, Cursor transcript paths, and ambiguous mechanical-rewrite wording.

The non-strict repository-wide scan reports existing portability debt as warnings. The strict changed-file scan prevents a pull request from adding or preserving those patterns in files it touches.

## Semantic review after mechanical porting

Regex passes are only the first step. Review every changed skill for meaning:

1. Replace vendor calls with the narrowest capability verb. Read-only investigation uses `explore`; code changes use `implement`; independent criticism uses `review`.
2. Replace concrete model names with `model_role` and let the active adapter or override resolve a real model.
3. Keep product decisions in `ask_user`; obtain observable facts through exploration or verification.
4. Keep write scopes disjoint before using `parallel`.
5. State the fallback when the host cannot spawn helpers or drive the real runtime surface.
6. Remove claims that a mode, transcript path, MCP discovery mechanism, or background task API exists on every host.

A mechanically valid sentence can still be semantically wrong. Phrases such as “`explore` / `implement` helper” are a sign that the port has not chosen the actual capability.

## skills.sh

- The `description` frontmatter field is the trigger surface and must stay quoted for reliable parsing.
- Prefer installing the whole pack so the `pstack` entry skill, adapters, playbooks, and leaf skills remain available together.
