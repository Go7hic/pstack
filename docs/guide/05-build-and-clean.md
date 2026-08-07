# Build the change and clean the diff

The build playbooks share one discipline: state what you observed and let the playbook demand the missing evidence. This page shows what to put in the prompt for common build tasks, then the cleanup habits that keep diffs reviewable.

## Prompt each build playbook with what you know

A bug prompt states the symptom and asks for a reproduction first:

```text
/poteto-mode this command emits two records after a retry. reproduce first, then fix and verify.
```

A feature prompt states the behavior and what must not change:

```text
/poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

A refactoring prompt pins behavior before structure moves:

```text
/poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it is unchanged after.
```

A performance prompt states the measurement rather than a vague impression:

```text
/poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, and show before and after.
```

These route to the [Bug fix](../../skills/poteto-mode/playbooks/bug-fix.md), [Feature](../../skills/poteto-mode/playbooks/feature.md), [Refactoring](../../skills/poteto-mode/playbooks/refactoring.md), and [Perf issue](../../skills/poteto-mode/playbooks/perf-issue.md) playbooks. The playbook adds the steps you did not type: reproduce before fixing, name the data shape before implementing, pin behavior before restructuring, and profile before optimizing.

For sustained improvement of one number, use the [Hillclimb playbook](../../skills/poteto-mode/playbooks/hillclimb.md). Give it the metric, target, and stop condition. It freezes the measurement harness, tries one hypothesis at a time, keeps measured wins, and reverts everything else.

## Write a failing test first when it is the right seam

When a bug has a cheap local test path, invoke:

```text
/tdd implement
```

In context, that is enough. [`/tdd`](../../skills/tdd/SKILL.md) writes the smallest test that fails for the intended reason, implements the fix, and reruns the test. When a test would require broad harness setup or brittle mocks, use the closest executable real-surface check instead. Do not force a unit test when a real command or browser reproduction is stronger evidence.

## Let language-specific discipline load when needed

[`typescript-best-practices`](../../skills/typescript-best-practices/SKILL.md) translates the type-system principles into concrete TypeScript rules: discriminated unions, `unknown` at boundaries, exhaustive variants, and schema-derived types. It can be invoked directly or selected automatically by a host that supports implicit skill routing.

## Clean before you commit

The [Opening a PR playbook](../../skills/poteto-mode/playbooks/opening-a-pr.md) requires a simplicity pass before commit and applies [`/unslop`](../../skills/unslop/SKILL.md) to pull-request descriptions and commit bodies.

Use a host-provided code-cleanup tool when one is available. The required outcome is portable even when the tool name is not:

- remove narrating comments;
- remove unsupported defensive guards;
- delete dead compatibility paths;
- remove speculative abstractions;
- revert unrelated edits;
- reduce wrappers and layers that add no capability;
- keep the smallest diff that proves the outcome.

For prose, `/unslop` accepts a target and any extra rules:

```text
/unslop the readme changes, no em dashes
```

Terse follow-ups such as `unslop that and tighten it` are fine when the target is clear from context.

## Review comments with `/no-comments`

Comments need a separate pass from an agent that did not write them:

```text
/no-comments the diff
```

[`/no-comments`](../../skills/no-comments/SKILL.md) uses the [Comment Sicko rubric](../../skills/pstack/references/agents/comment-sicko.md). The keep list is narrow: required license headers, public-API documentation, links that explain an external constraint, or rationale the code cannot encode.

A comment that narrates obvious steps should disappear. A comment that reveals surprising code should usually trigger a design or naming fix. When a comment claims a durable constraint, encode it as a type, test, lint, schema, or runtime check where possible.

The division of labor is:

- the simplicity pass removes code and structural padding;
- `/unslop` cleans human- and agent-facing prose;
- `/no-comments` applies independent judgment to comments and their underlying causes.

**Pitfall:** cleanup is not optional polish. Narrating comments, defensive dead weight, and unrelated edits make a diff harder to trust and create more surface for the next bug. Clean before review, not after reviewers identify the padding.

Next: [Verify and ship](./06-verify-and-ship.md).
