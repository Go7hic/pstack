# Steer with principle names

ystack ships 21 principles as individual skills. `/ystack` and `/poteto-mode` read their index at the start of multi-step work, apply the principles the task triggers, and name each applied principle with the decision it changed.

You do not need to invoke principles directly. Use their names to steer. Each name points at a complete rule the agent has already read, so one phrase can redirect work more precisely than a paragraph.

## Steering in practice

```text
use subtract before you add. delete the obsolete adapters first, then design what is left.
```

```text
apply prove it works. run the real import flow and show me the written records.
```

```text
separate before serializing shared state. give each attempt its own worktree, no locks.
```

A principle citation with no changed decision is decorative, not applied.

## The 21, briefly

### Core

- [Laziness Protocol](../../skills/principle-laziness-protocol/SKILL.md)
- [Foundational Thinking](../../skills/principle-foundational-thinking/SKILL.md)
- [Redesign from First Principles](../../skills/principle-redesign-from-first-principles/SKILL.md)
- [Subtract Before You Add](../../skills/principle-subtract-before-you-add/SKILL.md)
- [Minimize Reader Load](../../skills/principle-minimize-reader-load/SKILL.md)
- [Outcome-Oriented Execution](../../skills/principle-outcome-oriented-execution/SKILL.md)
- [Experience First](../../skills/principle-experience-first/SKILL.md)
- [Exhaust the Design Space](../../skills/principle-exhaust-the-design-space/SKILL.md)
- [Build the Lever](../../skills/principle-build-the-lever/SKILL.md)

### Architecture

- [Model the Domain](../../skills/principle-model-the-domain/SKILL.md)
- [Boundary Discipline](../../skills/principle-boundary-discipline/SKILL.md)
- [Type System Discipline](../../skills/principle-type-system-discipline/SKILL.md)
- [Make Operations Idempotent](../../skills/principle-make-operations-idempotent/SKILL.md)
- [Migrate Callers Then Delete Legacy APIs](../../skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)
- [Separate Before Serializing Shared State](../../skills/principle-separate-before-serializing-shared-state/SKILL.md)

### Verification

- [Prove It Works](../../skills/principle-prove-it-works/SKILL.md)
- [Fix Root Causes](../../skills/principle-fix-root-causes/SKILL.md)
- [Sequence Work into Verifiable Units](../../skills/principle-sequence-verifiable-units/SKILL.md)

### Delegation

- [Guard the Context Window](../../skills/principle-guard-the-context-window/SKILL.md)
- [Never Block on the Human](../../skills/principle-never-block-on-the-human/SKILL.md)

### Meta

- [Encode Lessons in Structure](../../skills/principle-encode-lessons-in-structure/SKILL.md)

Do not memorize the list. Return when you catch the agent doing something a principle name would have prevented.

Next: [Make it yours](./09-make-it-yours.md).
