# Understand the code before changing it

Editing code you do not understand is how subtle regressions ship. ystack gives you four ways in. `/how` explains what the code does now. `/why` digs up the reasons it is shaped that way. `/teach` blends both into one explanation. `/recall` rebuilds your own recent context on a topic.

![A detective studies a machine blueprint with a magnifying glass while robots fetch case files; the evidence board behind her links clues under /how and /why.](./images/understanding.jpg)

## Trace behavior with `/how`

```text
/how do we dedupe notifications? is there an n+1 when we look up subscribers?
```

Ask the question you actually have. [`/how`](../../skills/how/SKILL.md) reads the code and answers at the level of a senior engineer onboarding you onto the subsystem, with the runtime flow, key types, and non-obvious parts. For a big subsystem it fans out two to four read-only explorers first. For a narrow question it just reads and explains.

`/how` can also push back on the design. Ask for Critique mode when you suspect the structure itself:

```text
/how explain the sync service, then critique its ownership boundaries
```

The explanation comes first, so the critique stays grounded in how the thing really works.

## Dig up history with `/why`

```text
/why was the retry limit set to five? does the reason still hold?
```

[`/why`](../../skills/why/SKILL.md) starts from source control, then queries whatever evidence categories your connected tools expose, such as the issue tracker, long-form docs, team chat, observability, error tracking, and analytics. The report cites evidence, separates direct facts from inference, and reports null results too.

The two compose naturally. `do why first then how` is a good prompt when you suspect history explains the structure.

## Actually understand it with `/teach`

```text
/teach me how this PR changes retries. convince me it fixes the cause and not the symptom.
```

[`/teach`](../../skills/teach/SKILL.md) is for when a summary is not enough. It runs `/how` and `/why`, then weaves the findings into an explanation you can challenge.

## Rebuild your own context with `/recall`

```text
/recall catch me up on the export work from last week
```

[`/recall`](../../skills/recall/SKILL.md) mines authorized recent context plus the shared project record and returns a brief on where things stand and what comes next.

## Take over prior work with Session pickup

When another agent or an earlier session left a branch mid-flight:

```text
/ystack take over this branch. read the decision log, figure out what is done, and continue from there. do not redo finished work.
```

The [Session pickup playbook](../../skills/poteto-mode/playbooks/session-pickup.md) reconstructs branch state and decisions, names the resume point, and verifies inherited claims against the original goal.

**Pitfall:** do not skip these skills because "the agent will read the code anyway." `/how` first is cheaper than the second bug.

Next: [Design the change](./04-design.md).
