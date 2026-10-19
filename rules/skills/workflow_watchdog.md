# Workflow Watchdog — Background Task Inspection

## Applicable Scenarios

Use for ordinary CLIs, long batch jobs, or other tasks without native automatic completion notifications, only when the host permits supervision and the caller has actual inspection and stop permissions. These subprocesses can get stuck in loops or retries and need bounded supervision.

**Native `task(background=true)` subagents with automatic completion notifications are excluded from scheduled inspection.** Follow [Parallel Subagent Workflow](./workflow_parallel_subagents.md) and wait for automatic completion; do not bypass this contract with scheduled wake-ups, polling, `sleep` progress checks, or scheduled log reads. Before dispatch, arrange stage budgets, a total deadline, logs, failure stop conditions, and partial-artifact preservation inside the child task or through an explicitly supported platform event channel.

## What to Do

For tasks eligible for supervision above, define the stage and artifact, total deadline, no-progress budget, and log locations before dispatch. About 30 minutes (1800s) may be a reference inspection interval for long batch jobs, but does not replace task deadlines or justify long silent waits during interactive stages. Use only mechanisms actually available and authorized in the current host, such as `ScheduleWakeup` when supported, or delayed supervision under an installed Process Launcher skill; do not invent tools.

At authorized checkpoints, verify progress for the same task and attempt rather than process liveness alone. A launch receipt is not completion evidence; acceptance also requires checking actual results and artifacts. Handle two cases:

1. **Genuinely busy**: Verifiable stage progress or new artifacts exist. Continue within the total deadline, keeping any further checks bounded. Log growth alone is not useful progress.
2. **Stuck, explicitly failed, or timed out**: Preserve the failed stage, logs, exit code when available, diff, and partial artifacts first. Within the granted permissions, stop only processes owned by this invocation. Use existing results to narrow the next step; do not repeat the same broad task without new evidence.

Within this scope, judge progress and recover autonomously under existing permissions and the contract in `rules/SOUL.md`; this does not authorize stopping unrelated processes or expanding scope. For native automatically notifying subagents, recovery still uses child-internal budgets and supported platform events, without adding host-side polling.

## Source

Generalized from a session where a dispatched subprocess got stuck and the AI waited in place, wasting the entire interval. The lesson is to define supervision and recovery boundaries before dispatch: schedule bounded inspection only when host supervision is permitted, without overriding the no-poll contract for native automatic completion notifications.
