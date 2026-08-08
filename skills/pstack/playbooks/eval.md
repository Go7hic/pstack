### Eval

**You own the experiment design. Plan, blind, run, and synthesize.** Use an eval to measure how a skill, prompt, rubric, or structural change affects agent behavior before promoting it.

The main failure mode is the observer effect. A candidate that knows the behavior being measured will perform for the test, so candidate tasks must look like organic user work.

## Blinding rules

- Do not expose words such as `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in paths, prompts, or files visible to candidates.
- Write one realistic user request that states the goal, constraints, and success condition without naming the hidden behavior being measured.
- Do not ask candidates to list which skills or principles they used. Grade actual actions and artifacts rather than self-report.
- Use ordinary project-shaped directory and branch names.
- Do not tell one candidate that other candidates exist.
- The judge sees sanitized labels, never model names or variant identities.
- When comparing variants, one judge scores all outputs in one pass on one rubric. Separate judge runs create calibration drift.

## Steps

1. **Frame the hypothesis.** State the variant or behavior under study, the baseline, and the expected observable difference. Write three to six concrete scoring criteria for the judge only.
2. **Create isolated environments.** Each candidate receives its own worktree or directory, the same project starting state, and only the skill or prompt variant assigned to that arm. Keep write scopes and runtime resources isolated.
3. **Author one organic prompt.** Use the exact same prompt and success conditions for every arm. Remove meta-language that reveals what is being measured.
4. **Run candidates through Arena.** Use `parallel` and isolated helpers as Arena's fan-out phase specifies. Resolve candidate models through the active adapter. Keep variant labels and model identities hidden from the judge.
5. **Run one blinded judge.** Use `review` with `model_role:judgment` or `model_role:critic`, preferably from a different model family than the candidate majority. Give the judge sanitized outputs and the held-back rubric.
6. **Verify behavior from available evidence, not self-report.** Prefer a first-class session trace, tool-call record, generated artifact, git history, or runtime evidence exposed by the active host. When no transcript or trace is available, grade only claims observable in the artifact and record the evidence gap. Never scan broad user-history directories to locate hidden conversations.
7. **Read every output yourself.** The lead reviews candidates end to end, compares the result with the judge, investigates disagreement, and checks that blinding was not broken.
8. **Decide.** Promote, reject, or rerun with a corrected rubric or stronger sensitivity. Do not average wildly divergent outputs into a conclusion; divergence often means the prompt, fixture, or measurement is under-specified.

## Evidence package

For each arm, retain:

- sanitized label;
- prompt and starting fixture revision;
- assigned variant revision;
- artifact or diff;
- verification result;
- available action trace or transcript reference;
- judge score per criterion;
- lead notes and final verdict.

Do not retain secrets or unrelated conversation history in the eval package.

**Reply:** hypothesis, hidden rubric, fixture and blinding controls, per-arm evidence, judge verdict, lead synthesis, confidence limits, and promote/reject/rerun recommendation.
