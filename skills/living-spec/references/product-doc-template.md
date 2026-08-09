# <Domain>

## Purpose

One paragraph describing the user, operator, or business outcome this domain owns.

## Current behavior

- Describe behavior that is true in the verified product now.
- Use stable language that survives implementation refactors.
- Split unrelated behavior into separate bullets or subsections.

## Failure and boundary scenarios

- Describe important rejected, unavailable, expired, partial, or recovery paths.
- Include security, permission, billing, data-loss, and compatibility boundaries when relevant.

## Product constraints

- State durable in-scope and out-of-scope behavior.
- Do not list temporary implementation tasks.

## Technical constraints

Include only constraints future maintainers must preserve, such as an external protocol, storage ownership rule, migration invariant, or public compatibility contract.

## Verification surfaces

- Name repeatable UI, CLI, API, test, trace, or operational checks that prove the behavior.
- Prefer concrete paths or commands when stable.

## Related decisions

- Link relevant ADRs.
- Link external authoritative documents rather than copying them.
