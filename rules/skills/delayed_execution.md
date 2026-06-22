# Skill: Delayed Execution

For executing tasks after a delay. This starter skill only keeps a lightweight fallback; if the task needs persistence, restart recovery, log querying, cancellation, or AI agent job submission, install the public repos listed in `docs/SKILL_ECOSYSTEM.md`.

## When to Use

- Need to run a simple command after a delay
- The current workspace has not yet installed a more complete process manager
- Task loss risk is acceptable

## Recommended Path

Prefer installing and using the dedicated capabilities from the ecosystem:

- `process-launcher`: durable one-shot schedule, process logs, cancellation, restart recovery
- `opencode_skill`: OpenCode `submit` / `submit --dry-run` / batch submission

For delayed tasks requiring AI judgment, the correct combination is: first use `opencode_skill submit --dry-run` to pre-check the submission chain, then use `process-launcher` to trigger the real `opencode_skill submit` at the future time. Do not maintain private OpenCode endpoints, models, agents, or local paths in this starter skill.

## Lightweight Fallback: sleep + nohup

Only suitable for low-risk, short-duration, losable command-line tasks.

```bash
# Syntax: nohup bash -c 'sleep <seconds> && <command>' > /tmp/delayed_task.log 2>&1 &
nohup bash -c 'sleep 3600 && /path/to/script.sh' > /tmp/delayed_task.log 2>&1 &
disown
```

## Time Conversion

| Duration | Seconds |
|------|------|
| 1 minute | 60 |
| 5 minutes | 300 |
| 10 minutes | 600 |
| 30 minutes | 1800 |
| 1 hour | 3600 |
| 2 hours | 7200 |
| 24 hours | 86400 |

## Inspect and Cancel

```bash
# Check if task is running
ps aux | grep "sleep" | grep -v grep

# View logs
tail -f /tmp/delayed_task.log

# Cancel task
kill <PID>
```

## Safety Rules

- Prefer `process-launcher` unless the task is genuinely low-risk and losable.
- Before delayed execution, run the target command's dry-run / check / preview mode; if no pre-check capability exists, explicitly state the risk.
- All fallback tasks must redirect logs.
- Do not write real API keys, private endpoints, contacts, model preferences, or local machine paths into this public starter skill.
