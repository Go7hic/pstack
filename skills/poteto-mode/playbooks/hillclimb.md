### Hillclimb

**You own the metric and the experiment's integrity. Supervise and review; delegate bounded attempts.** Use this playbook for sustained improvement of one measurable outcome against a target. A one-off performance defect belongs to Perf issue; Hillclimb is an evidence-driven search loop.

Core discipline: one hypothesis, one change, one measurement, then keep or revert. Never stack unmeasured edits, and never claim a win from source inspection. The data decides.

1. **Ground the workload and architecture.** Run **how** over the target. Name the workload dimensions that can change the result, such as data size, history, state, concurrency, cache warmth, device class, or network conditions. Select a realistic case that reproduces the user's complaint. If it does not reproduce, fix the reproduction before optimizing.

   Define one metric, the direction that counts as better, and a stop predicate. A robust predicate combines a target improvement with a minimum number of attempts so a lucky early sample cannot end the run. Use the user's numbers when provided; otherwise use `ask_user` for the product or cost trade-off after presenting a recommendation.

2. **Build and freeze the measurement harness.** Apply **build-the-lever**. One repeatable `verify` command must emit the metric and the regression-gate result. Prove sensitivity with contrasting realistic workloads. Sample enough to clear noise; prefer a distribution or median over a single run.

   Record:

   - environment and dependencies;
   - workload fixture and warm-up policy;
   - exact command;
   - sample count and aggregation;
   - baseline metric and variability;
   - correctness or regression gate.

   Once attempts begin, changing the ruler invalidates earlier comparisons. Start a new series instead of silently editing the harness.

3. **Open a decision trail.** Use **show-me-your-work**. Keep one row per attempt with:

   ```text
   id, hypothesis, mechanism, change, before, after, delta, tests, verdict, note
   ```

   Store the trail outside files that will be reverted with rejected attempts. Read it before each new hypothesis so the search accumulates rather than circling.

4. **Ground each hypothesis in a mechanism.** A useful hypothesis predicts why a specific change should move the metric. “Defer X off startup because it blocks first paint” is testable. “Try memoization” is not.

   Generate hypotheses from the architecture and measurement evidence. Prefer deletion and critical-path removal before low-level tuning.

5. **Run one attempt per iteration.**

   - Use `implement` with `model_role:bug_impl` and a tight write scope. The lead reviews the diff.
   - When several hypotheses are truly independent, use `parallel` with separate worktrees or isolated write targets as provided by the active adapter. Never let multiple helpers write the same branch or files.
   - Measure before and after with the frozen harness.
   - Run the regression gate and verify the matching real surface.
   - Accept the attempt only when the movement exceeds noise and behavior remains correct.
   - Otherwise revert the attempt completely. A change that “might help” does not ride along.
   - Create one focused commit per accepted improvement, staging only the intended files.
   - Log kept and rejected attempts alike.

   Every iteration ends in a check before the next begins. Apply **sequence-verifiable-units**.

6. **Push past the first plateau.** After several rejected attempts, do not repeat the same category with cosmetic variations. Re-read traces and source, pivot mechanisms, combine compatible near-misses in a new measured attempt, or test a more structural alternative through **architect**.

   Correctness and simplicity outrank the number. Revert a numerical win that harms behavior. Prefer a simpler implementation when it holds the same metric.

7. **Stop honestly.** Stop when the predicate is met, or when remaining hypotheses are genuinely marginal relative to their complexity, cost, or risk. Do not relax the predicate to declare victory. Do not stop while cheap evidence-backed hypotheses remain.

   When the host supports autonomous continuation, the loop may run unattended under an explicit user contract. Preserve the decision trail and the same stop predicate across context resets. When the host cannot persist long-running state, use the Pause safely and Session pickup playbooks rather than relying on hidden memory.

8. **Prepare the pull request.** Run **Opening a PR** with accepted commits ordered so the metric improvement reads from root to tip. Include the harness command, baseline, final result, sample method, regression gate, accepted attempts, rejected categories, and remaining risks.

**Reply:** metric and target, baseline to final with percentage delta, sample/noise method, attempts run with kept versus reverted counts, each accepted fix on one line, decision-trail path, regression result, and the next hypothesis you would test if more improvement were required.
