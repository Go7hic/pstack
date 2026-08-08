### Perf issue

**You own the measurement story. Plan, review, and verify the numbers.** Tie every fix to a measurement; do not substitute source inspection for measurement.

1. Capture a baseline trace or metric with `verify` on the matching real surface. Record the workload, environment, command, artifact path, sampling method, and noise range so the post-fix result is comparable.
2. Run **how** to ground hypotheses. Do not claim a performance ceiling without measuring it.

   Most fixes come from eight strategy families. Use them as hypothesis generators, not a checklist. A family earns an attempt only when evidence shows the signal it names.

   - **Elimination.** The cheapest work is work that does not run. Before optimizing a hot path, ask whether the work is consumed, enabled, or still required. A trace shows what is expensive; the How pass determines whether it is deletable.
   - **Divide and conquer.** The dominant cost scales with input size. Split, shard, chunk, or prune the search space; run independent pieces in parallel only when shared state has been removed.
   - **Caching.** Identical inputs repeat an expensive computation or fetch. Name cache keys, invalidation, memory cost, and staleness before accepting the change.
   - **Indirection.** A cheaper intermediate removes expensive work from the critical path: an index instead of a scan, a queue instead of synchronous execution, or a handle that permits a cheaper implementation. An extra layer that does not remove work is pure cost.
   - **Batching.** Many small operations each pay a fixed RPC, query, syscall, serialization, or draw-call overhead. Coalesce them and measure both latency and resource usage.
   - **Redundancy.** Tail latency is dominated by one slow instance or attempt. Hedging or replication can trade extra load for lower latency only when the system has headroom and cancellation is correct.
   - **Lazy evaluation.** Work is performed for results that are never used or not needed yet. Defer it until the first real demand.
   - **Scheduling.** Necessary work occurs while a user or critical task is waiting. Move it before the hot moment, after it, or into an idle window, then measure the interactive path rather than only total work.

3. Plan the smallest evidence-backed fix. If it crosses a meaningful interface boundary, run **architect** first. Use `implement` with `model_role:bug_impl` and a bounded write scope; the lead reviews the diff. Capture a post-fix artifact using the same frozen workload and measurement method.

   Apply the **sequence-verifiable-units** principle. Verify or revert each attempt before introducing another variable.

4. Parse and compare the artifacts. Use structured conversion or a small analysis script when needed. Report baseline, post-fix value, absolute and percentage delta, sample count, and whether the movement clears noise. “Inconclusive” or a different surface is not a pass.
5. Run the regression gate and verify the user-visible path. A faster trace that changes behavior is a rejected attempt.
6. Cite the measurement command and artifacts in the pull request.
7. Run the **Opening a PR** playbook.

For sustained, iterative work against a target metric rather than a one-off diagnosis and fix, use the Hillclimb playbook.

**Reply:** workload and environment, baseline, post-fix result, delta, confidence/noise note, verification result, and artifact paths.
