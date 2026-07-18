# Workflow Watchdog — Background Task Inspection

## Applicable Scenarios

After dispatching long-running workflows, background agents, or batch sub-agent tasks. These subprocesses occasionally get stuck in a loop or retry, producing no output for a long time. Do not wait in place.

## What to Do

After dispatching a task, set a reasonable inspection wake-up, default about 30 minutes (1800s). Use `ScheduleWakeup` in the Claude Code harness; in other harnesses use the corresponding timing mechanism (e.g., Process Launcher delayed execution).

On wake-up, check the task status and handle two cases:

1. **Genuinely busy**: new output appears, the agent keeps producing. Leave it alone; wait or set another wake-up.
2. **Stuck in a loop**: no progress for a long time, the same step retries repeatedly. Kill it (use `TaskStop` in Claude Code), and proceed with the partial results, or switch methods and redo.

The "genuinely busy vs stuck" judgment is yours to make; do not ask the user. This aligns with the self-execution contract: inspection and kill are technical orchestration decisions to be carried through to the end.

## Source

Generalized from a session where a dispatched subprocess got stuck and the AI waited in place, wasting the entire interval. The lesson: make "set an inspection after dispatching" the default action, not a remediation after things go wrong.