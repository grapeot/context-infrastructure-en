# Crontab Configuration Guide

This document describes the scheduled tasks required by the context infrastructure system.

---

## Timeline Overview

```
3:05 AM   → Situation Awareness: daily summary + camera cache refresh
4:00 AM   → Session Sync: export AI session archive
6:30 AM   → WeChat DB Parser: export daily messages as CSV (if applicable)
7:00 AM   → Daily Briefing: generate personal morning briefing → Email
8:00 AM   → AI Heartbeat Observer: scan file changes, extract observations, write to OBSERVATIONS.md
Every 2m  → Situation Awareness: snapshot collection (traffic/camera/alerts)
Every 12h → Situation Awareness: wind warning check
Weekly    → AI Heartbeat Reflector: merge/promote/clean up memory
Daily     → Crontab Monitor: health audit, send alert email on anomalies
```

---

## Core Task Descriptions

### AI Heartbeat Observer (daily)

Scans workspace file changes and extracts valuable observations into `contexts/memory/OBSERVATIONS.md`. This is the "input end" of the three-tier memory system.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/observer.py`
- **Dependency**: OpenCode Server API (`OPENCODE_API_URL`)
- **Recommended time**: Daily 8:00 AM (after daily briefing)

### AI Heartbeat Reflector (weekly)

Merges, promotes, and cleans up observations accumulated in OBSERVATIONS.md, distilling them into higher-level insights.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/reflector.py`
- **Dependency**: OpenCode Server API (`OPENCODE_API_URL`)
- **Recommended time**: Every Sunday 9:00 AM

### Crontab Monitor (daily)

Autonomously audits the health of all crontab tasks and sends alert emails on anomalies.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py`
- **Dependencies**: OpenCode Server API, Gmail (`GMAIL_USERNAME` / `GMAIL_APP_PASSWORD`)
- **Recommended time**: Daily 9:00 AM

### AI News Survey (daily/weekly)

Calls an AI agent to generate a daily or weekly AI industry report, publishable to Kit subscribers or sent as personal email.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py`
- **Dependencies**: OpenCode Server API, Gmail or Kit API
- **Recommended time**: Daily 8:00 AM (daily report) or Monday 8:00 AM (weekly report)

---

## Example Crontab Configuration

Add the following to `crontab -e`. **Replace `/path/to/your/workspace` with your actual path before using.**

```cron
# ── Timezone note ──────────────────────────────────────────────
# All times below are local time. To specify a timezone, add at the top of crontab:
# TZ=America/Los_Angeles

# AI Heartbeat Observer — daily 8:00 AM
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# AI Heartbeat Reflector — every Sunday 9:00 AM
0 9 * * 0 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1

# Crontab Monitor — daily 9:00 AM
0 9 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py >> /tmp/crontab_monitor.log 2>&1

# AI News Survey daily report — daily 8:00 AM (send personal email)
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode daily >> /tmp/ai_news_survey.log 2>&1

# AI News Survey weekly report — every Monday 8:00 AM (publish to Kit subscribers)
0 8 * * 1 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode weekly --publish-to-kit >> /tmp/ai_news_weekly.log 2>&1
```

---

## Notes

1. **Path replacement**: All `/path/to/your/workspace` must be replaced with your actual absolute path.
2. **Virtual environment**: Scripts depend on Python packages in `.venv`. Run `uv pip install -r requirements.txt` first (if a requirements file exists).
3. **Environment variables**: The cron environment does not automatically load `.env`. Either load it explicitly in the script, or inject it in crontab with `env $(cat .env | xargs)`.
4. **Timezone**: macOS cron uses the system timezone by default. On Linux servers, set `TZ=` explicitly at the top of crontab.
5. **Logs**: The examples write logs to `/tmp/`. For production, use a persistent path (e.g., a `logs/` directory).
6. **Dependency order**: The observer depends on the day's file changes. Run it after daily briefing and news survey (8:30 AM or later).
