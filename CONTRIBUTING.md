# Contributing

## Goals

- Keep playbook / principle **intent** aligned with upstream pstack.
- Keep vendor tool names out of skill bodies; put them only in `skills/pstack/references/adapters/`.
- Every workflow must remain correct under the `generic` adapter (no multi-agent).

## Layout

- Installable skills live under `skills/<name>/SKILL.md` (skills.sh compatible).
- Shared runtime: `skills/pstack/references/{capability-contract.md,adapters/,agents/}`.
- Playbooks: edit `skills/poteto-mode/playbooks/`, then `rsync` to `skills/pstack/playbooks/`.

## Re-port helpers

After pulling newer upstream Cursor pstack sources:

```bash
# copy upstream skills, then:
python3 scripts/port_to_portable.py
python3 scripts/port_pass2.py
rsync -a skills/poteto-mode/playbooks/ skills/pstack/playbooks/
```

Review the diff. Adapters and `setup-pstack` are hand-maintained — do not blindly overwrite them.

## skills.sh

- `description` frontmatter is the trigger surface.
- Prefer installing the whole pack so `pstack` adapters sit beside leaf skills.
