# Make it yours

`poteto-mode` captures one person's engineering style. The machinery underneath—principles, playbooks, capability routing, model roles, verification, and review—can support a smaller mode built around your own recurring conventions.

## Generate your own mode with `/automate-me`

```text
/automate-me
```

[`/automate-me`](../../skills/automate-me/SKILL.md) gathers authorized evidence from the current host, looks for repeated preferences in response style, autonomy, delegation, verification, code, prose, and delivery process, then asks which patterns are genuinely durable.

It uses the active coding agent's skill-authoring workflow, not a hard-coded vendor path. The resulting `<handle>-mode` skill goes into the project-local or user-level skill directory supported by the current host. When the host can enforce explicit-only invocation or persistent modes, the generated skill uses those controls; otherwise it documents the lifecycle fallback honestly.

Run it again when habits change:

```text
/automate-me update my mode skill with evidence since its last meaningful edit
```

Update mode preserves rules that have not been contradicted, revises stale rules, removes disproven ones, and adds sections only for genuinely new clusters.

## Capture a session's lessons with `/reflect`

After a task exposes a reusable success or failure pattern, run:

```text
/reflect that took too long. capture what should change so the next run does not repeat it.
```

[`/reflect`](../../skills/reflect/SKILL.md) builds an authorized session evidence package and sends it through three independent lenses: judgment, tooling, and divergent review. A synthesizer groups proposals into `Accepted`, `Rejected`, and `Backlog`. It waits for your approval before editing durable skills.

Approve a lesson only when it would change a future decision. One unusual session is evidence to inspect, not automatically a global rule. Prefer a script, CI check, adapter contract, or evaluation when structure can enforce the lesson better than prose.

## Author a focused skill

When the workflow is already clear:

```text
/poteto-mode write a skill for verifying database migrations in this repository
```

The [Authoring a skill playbook](../../skills/poteto-mode/playbooks/authoring-a-skill.md) routes through the active host's skill-authoring and validation workflow, checks frontmatter and references, applies portable capability language, and ships the result through the [Opening a PR playbook](../../skills/poteto-mode/playbooks/opening-a-pr.md).

Agent-facing prose has a high bar because an ambiguous sentence becomes an instruction future agents may follow. Let the authoring workflow test triggers, links, host compatibility, and fallback behavior instead of writing `SKILL.md` freehand.

A workflow that drives the real app and proves behavior is a verification skill. Use [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md) and [`/maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md). [Verify and ship](./06-verify-and-ship.md#create-a-project-verification-skill) explains when that investment earns its place.

## Write documentation to a standard

For documentation, RFCs, READMEs, pull-request descriptions, and commit messages:

```text
/technical-writing review the readme changes
```

[`/technical-writing`](../../skills/technical-writing/SKILL.md) chooses the document mode—tutorial, how-to, reference, or explanation—then checks audience, sequence, terminology, ambiguity, and sentence-level clarity. Use it to review an existing draft or name it when requesting the document.

## Test a skill change blind

A skill edit affects future sessions, so test it as an experiment:

```text
/poteto-mode run the Eval playbook on this skill change. Use the same organic task for both variants and keep the arms blind.
```

The [Eval playbook](../../skills/poteto-mode/playbooks/eval.md) controls for the observer effect. Candidate helpers receive an ordinary user-shaped task in isolated environments. They do not see experiment language, model identities, the hidden rubric, or other arms. One blinded judge scores all outputs on the same scale, and the lead verifies the behavior through artifacts, action traces, or authorized session evidence rather than candidate self-report.

Read every output before accepting the verdict. Disagreement with the judge may reveal bias, but it may also mean the rubric or fixture was under-specified.

## Keep personal rules portable

A useful personal mode distinguishes preferences from runtime mechanics:

- “Use two independent reviewers for risky architecture” is portable.
- “Call this exact vendor helper with this JSON” belongs in an adapter.
- “Keep the mode active forever” is invalid unless the host can enforce that lifecycle.
- “Never ask me questions” is unsafe; prefer “do not ask for observable facts or reversible engineering choices.”
- “Always use the strongest model” ignores cost and task shape; prefer model roles.

Run the repository portability audit when editing this pack:

```bash
python3 scripts/audit_portability.py
python3 scripts/audit_portability.py --strict --changed-from origin/main
```

**Pitfall:** do not hide a substantive skill change inside unrelated feature work. Fix the skill in its own focused pull request so it can be reviewed, evaluated, and reverted independently.

Next: [Recipes and pitfalls](./10-recipes-and-pitfalls.md).
