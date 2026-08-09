# The ystack guide

ystack works best when you stop micromanaging the agent. You describe what you want and how you'll know it is done. `/ystack` picks the playbook, runs the other skills as the steps need them, and shows you the evidence. `/poteto-mode` remains available when you want the full upstream-style mode contract.

Here's what you'll learn:

1. [Set up ystack](./01-setup.md). Install the pack and pick your models.
2. [Route work through `/poteto-mode`](./02-poteto-mode.md). Give it a goal and watch it pick a playbook.
3. [Understand the code](./03-understand.md). `/how`, `/why`, `/teach`, and `/recall` before you edit anything.
4. [Design the change](./04-design.md). `/architect`, `/arena`, `/swarm`, and `/interrogate` before code locks in a shape.
5. [Build and clean the change](./05-build-and-clean.md). The build playbooks, `/tdd`, `/unslop`, and `/no-comments`.
6. [Verify and ship](./06-verify-and-ship.md). Prove behavior on the real app, then open a focused PR and drive it to merged.
7. [Run work while you sleep](./07-overnight.md). An overnight contract, a decision log you can audit, and the playbooks that scale past one agent.
8. [Steer with principle names](./08-principles.md). The 21 names that redirect an agent mid-task.
9. [Make it yours](./09-make-it-yours.md). Your own mode, plus how to test a skill change.
10. [Recipes and pitfalls](./10-recipes-and-pitfalls.md). Prompts to copy and mistakes to skip.

Read the pages in order the first time. After that, each page stands alone.

## If you only remember one thing

Give the agent a goal and a way to check it, in your own words:

```text
/ystack the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

You do not need to name a playbook or list skills. "repro first" and a checkable outcome are all the routing signal ystack needs. It matches the Bug fix playbook, copies the steps into a todo list, and calls the right skills as each step fires.

Next: [Set up ystack](./01-setup.md).
