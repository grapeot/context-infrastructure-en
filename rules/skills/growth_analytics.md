---
title: Growth Analytics Toolkit
category: API Guide
tags: [analytics, ga4, kit, gsc, typefully, growth, metrics]
created: 2026-03-14
updated: 2026-03-29
---

# Skill: Growth Analytics (GA4 / Kit / GSC / Typefully / short_url)

Five data entrypoints for querying website traffic (GA4), email subscriptions (Kit), search engine performance (GSC), Twitter publishing and engagement (Typefully), and short-link clicks with conversion paths (short_url).

## Pre-Analysis Required Reading

Before doing yage.ai growth analysis or making growth recommendations, read `adhoc_jobs/website_growth/docs/project_context.md`. The project's objective function is curiosity bandwidth and sharing, not traffic or monetization; the recommendation priority framework follows that document.

## When to Use

Trigger when the user says:
- "Check recent traffic", "How's the website doing"
- "How many new subscribers", "What's the open rate"
- "How's search ranking", "GSC data", "Keyword performance"
- "Twitter engagement data", "How many impressions"
- "Short link clicks", "short_url data"
- "Run a growth analysis", "Pull growth data"
- Any query involving yage.ai website, Newsletter, search engine metrics, or social media metrics

## Prerequisites

- Root `.env` contains:
  - `KIT_API_KEY` — Kit (ConvertKit) API v4 key
  - `TYPEFULLY_API_KEY` — Typefully v2 API key (for publishing queries)
  - `GA4_CREDENTIALS_PATH` — absolute path to GA4/GSC service account JSON file (shared by both tools)
- `tools/ga4_metrics.py` and `tools/gsc_metrics.py` share authentication: both read the service account JSON from `GA4_CREDENTIALS_PATH`, but use different API scopes (GA4 uses Analytics Data API, GSC uses Webmasters API)
- `tools/ga4_metrics.py` merges and loads `--env-file`, `GA4_ENV_FILE`, upward `.env` from the current working directory, and upward `.env` from the script directory in order; missing keys are filled from higher layers, so hitting a local `.env` first no longer causes `GA4_CREDENTIALS_PATH` to be lost
- If `GA4_CREDENTIALS_PATH` is not set in the environment, GA4/GSC CLI also auto-discovers `gen-lang-client-*.json` from the current and parent directories as fallback (compatible with `adhoc_jobs/website_growth/`)
- Typefully browser-level credentials (optional, only needed for engagement metrics):
  - `TYPEFULLY_AUTHORIZATION`, `TYPEFULLY_ACCOUNT`, `TYPEFULLY_SESSION`
- `short_url.db` is at `ai_builder_courses/short_url/data/short_url.db`; pull the latest copy from `yage` via `ai_builder_courses/circle_context/scripts/sync_remote_circle_context.sh`
- Python venv activated (`source .venv/bin/activate`)

## Tool 1: Kit Subscription Data

The Kit commands have migrated from the legacy `tools/kit_metrics.py` script to the `kit-skill analytics` CLI. New workflows should use the CLI; the legacy script is retained only for backward compatibility.

```bash
cd <kit_skill_dir>
op run --env-file=.env -- .venv/bin/kit-skill analytics account --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics growth --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics growth --start-date 2026-02-28 --end-date 2026-03-14 --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics email-stats --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics subscriber-count
op run --env-file=.env -- .venv/bin/kit-skill analytics broadcasts --limit 10 --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics broadcast-stats 23288438 --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics snapshot --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics snapshot --output /tmp/kit_snapshot.json
op run --env-file=.env -- .venv/bin/kit-skill analytics sequences --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics sequence 2789126 --format json
op run --env-file=.env -- .venv/bin/kit-skill analytics sequence 2789126 --include-subscribers --format json
```

### Kit Key Metrics

- **growth_stats**: New, unsubscribed, net change, total over the period
- **email_stats**: 90-day aggregate sent, opened, clicked
- **broadcast stats**: Per-broadcast open_rate, click_rate, unsubscribes
- **subscribers**: Active/inactive/unsubscribed subscriber list and counts; `subscriber-count` is the account-wide active count, not equal to a specific newsletter tag's send audience; list commands mask emails by default, add `--show-emails` only for private-output scenarios
- **sequences / sequence**: Welcome sequence and other automation active status, email count, subscribers entering the sequence. `Welcome Sequence` id is `2789126` (sends daily at 13:00 Pacific, 3 emails). `subscriber_count` is a flow metric (subscribers exit after completing all 3 emails); with organic subscription of 2-3/day, the steady-state in-sequence count is 8-15. Judge health by whether it stays in that band; do not expect it to grow with cumulative subscriptions. Batch-imported lists do not trigger form automations or enter sequences; this is expected behavior.
- **sequence e2e verification**: Inside `<kit_skill_dir>`, run `KIT_ENABLE_LIVE_TESTS=1 .venv/bin/python -m pytest -m live_integration tests/test_analytics.py` (skipped by default; creates a probe subscriber that goes through the real sequence, clean up the probe after)

## Tool 2: GA4 Website Traffic

```bash
python tools/ga4_metrics.py daily --days 7        # Daily traffic trend
python tools/ga4_metrics.py weekly --days 90       # Weekly aggregation
python tools/ga4_metrics.py top-pages --limit 20   # Top pages
python tools/ga4_metrics.py sources                # Traffic source breakdown
python tools/ga4_metrics.py channels               # Channel grouping
python tools/ga4_metrics.py campaigns --days 14    # UTM campaign attribution (Twitter effectiveness tracking)
python tools/ga4_metrics.py snapshot --output /tmp/ga4_snapshot.json  # Full snapshot
```

### GA4 Key Metrics

- **daily/weekly**: activeUsers, newUsers, sessions, screenPageViews, averageSessionDuration, bounceRate
- **top-pages**: pagePath, pageTitle, screenPageViews, activeUsers
- **sources**: Traffic distribution by sessionSource, sessionMedium dimensions
- **channels**: sessionDefaultChannelGroup (Direct, Organic Search, Referral, Social, etc.)
- **campaigns**: sessionCampaignName — used to verify whether UTM-tagged Twitter threads actually drove traffic

### GA4 Property

- yage.ai (Computing Life): `393442232`
- Guide Me City / travel_guide (guideme.city): `535900600`
- Measurement / gtag ID: yage.ai and guideme.city each bind to different `G-` measurement IDs (injected into their respective site gtag snippets), but both properties are under the same Google Analytics account, sharing the same service account authentication
- Service Account JSON location: specified by `GA4_CREDENTIALS_PATH` in `.env`

## Tool 3: GSC Search Engine Data (Google Search Console)

```bash
python tools/gsc_metrics.py overview --days 30          # Overview: total clicks, impressions, CTR, avg position
python tools/gsc_metrics.py top-queries --days 30 --limit 20  # Top search queries
python tools/gsc_metrics.py top-pages --days 30 --limit 20    # Top landing pages
python tools/gsc_metrics.py daily --days 30                 # Daily trend
```

### GSC Key Metrics

- **overview**: Total clicks, total impressions, average CTR, average position
- **top-queries**: clicks, impressions, ctr, position by query dimension (descending by clicks)
- **top-pages**: clicks, impressions, ctr, position by page dimension (descending by clicks)
- **daily**: clicks, impressions, ctr, position by date dimension (ascending by date)

### GSC Property

- Default Site URL: `sc-domain:grapeot.me` (domain-level property)
- `sc-domain:yage.ai` is also available; query directly via `GSC_SITE_URL` environment variable or `--site sc-domain:yage.ai`
- Default query days: 30
- Authentication shares the same service account as GA4 (`GA4_CREDENTIALS_PATH`), but uses an independent scope (`webmasters.readonly`)

### GSC Notes

- GSC data has a 2-3 day delay; content published today won't appear immediately
- GSC's 25,000 row/request limit means very large datasets need pagination (the tool has built-in pagination)
- Default query target remains `sc-domain:grapeot.me`; use `--site sc-domain:yage.ai` or set `GSC_SITE_URL` when querying yage.ai

## Tool 4: Typefully Twitter Data

### Unified Typefully/X CLI

New workflows use `adhoc_jobs/typefully_twitter_skill/`:

```bash
cd adhoc_jobs/typefully_twitter_skill
.venv/bin/typefully-twitter doctor config --format json
.venv/bin/typefully-twitter post list --status published --limit 10 --format json
.venv/bin/typefully-twitter metrics snapshot --start-date 2026-03-01 --end-date 2026-03-14 --format json
.venv/bin/typefully-twitter x fetch --days 7 --format json
```

See `rules/skills/typefully_twitter.md` for details. Typefully publishing, Typefully account-level metrics, and X per-post analytics are three independent credential sets; `doctor config` reports available capabilities separately.

## Tool 5: Short URL & Conversion Analytics (short_url.db)

For tracking short-link clicks, conversion attribution, and Circle community tag sync.

### Database Location and Sync
- **Location**: `ai_builder_courses/short_url/data/short_url.db`
- **Sync**: The source database is at `yage:/home/grapeot/short_url/data/short_url.db`. The local copy is pulled together via `ai_builder_courses/circle_context/scripts/sync_remote_circle_context.sh`; it is not auto-synced in real time.

### Core Schema
- `short_links`: Stores short link configuration (`short_code`, `long_url`, `circle_tag_name`, etc.).
- `access_logs`: Stores click logs (`short_code`, `ip_address`, `user_agent`, `accessed_at`).
- `circle_tag_cache`: Stores Circle tag metadata (`tag_id`, `tag_name`, `member_count`).

### Key Interpretation Rule: SSO vs. Acquisition
**SSO is an authentication path, not an acquisition tag.**
- Analysis should use a two-dimensional view: **authentication path** (SSO, Email, etc.) vs. **acquisition tag** (Affiliate, Landing Page, etc.).
- Users who log in via SSO may also carry affiliate or landing-page tags; the two are not mutually exclusive.
- Do not misread the residual `sso` bucket in reports as all SSO users. Existing Circle reports typically classify by tag first, then list remaining SSO separately.

### Join Logic
1. **short_url -> Circle**: Align via `circle_tag_name`. Suitable for tag-level trend comparison, not user-level attribution.
2. **Circle -> Stripe**: Join via `email`. Circle member emails match Stripe payment records.
3. **short_url -> Stripe**: No direct join. Must go through the indirect chain `circle_tag_name -> Circle member -> email -> Stripe`, and explicitly state the measurement-scope limitations.

### Query Examples (sqlite3)

```bash
# View click trend for a specific short link
sqlite3 ai_builder_courses/short_url/data/short_url.db \
  "SELECT date(accessed_at), count(*) FROM access_logs WHERE short_code = 'your_code' GROUP BY 1;"

# View short-link clicks for a specific tag
sqlite3 ai_builder_courses/short_url/data/short_url.db \
  "SELECT short_code, circle_tag_name, count(*) AS clicks FROM short_links LEFT JOIN access_logs USING(short_code) WHERE circle_tag_name = 'Affiliate_AceMode' GROUP BY short_code, circle_tag_name;"

# View all short links with Circle tags
sqlite3 ai_builder_courses/short_url/data/short_url.db \
  "SELECT short_code, circle_tag_name, long_url FROM short_links WHERE circle_tag_name IS NOT NULL;"
```

## Typical Usage

### Quick Growth Overview

```bash
# One command for Kit full snapshot (kit-skill analytics CLI)
cd <kit_skill_dir> && op run --env-file=.env -- .venv/bin/kit-skill analytics snapshot --format json

# One command for GA4 full snapshot
python tools/ga4_metrics.py snapshot

# One command for GSC full snapshot
python tools/gsc_metrics.py overview --days 30
```

### SEO Diagnosis: GSC + GA4 Cross-Reference

```bash
# GSC: What search terms bring users in
python tools/gsc_metrics.py top-queries --days 30 --limit 20

# GA4: How the landing pages for those terms perform
python tools/ga4_metrics.py top-pages --limit 20

# GSC: Which pages have impressions but low CTR (need title/description optimization)
python tools/gsc_metrics.py top-pages --days 30 --limit 50
```

### Verify Twitter Promotion Effectiveness

```bash
# Check GA4 UTM campaign data to see if Twitter threads drove traffic
python tools/ga4_metrics.py campaigns --days 14
```

### Conversion Attribution: Short URL + Circle + Stripe

```bash
# 1. Check short-link clicks
sqlite3 ai_builder_courses/short_url/data/short_url.db "SELECT count(*) FROM access_logs WHERE short_code = 'xyz';"

# 2. Check Circle tag members (with Circle snapshot or circle_analytics)
# 3. Check Stripe payment records (with Stripe Skill)
# Core: In Circle, separate auth path from acquisition tag; short_url aligns with Circle via circle_tag_name, Circle aligns with Stripe via email.
```

### Cross-Analysis

Pull Kit, GA4, GSC, short_url simultaneously, then cross-reference with Circle / Stripe:

```bash
cd <kit_skill_dir> && op run --env-file=.env -- .venv/bin/kit-skill analytics growth --start-date 2026-03-01 --end-date 2026-03-14 --format json
python tools/ga4_metrics.py weekly --days 30
python tools/gsc_metrics.py daily --days 30
sqlite3 ai_builder_courses/short_url/data/short_url.db "SELECT date(accessed_at), count(*) FROM access_logs GROUP BY 1 ORDER BY 1 DESC LIMIT 30;"
```

## Data Storage

To persist historical data, use `--output` to save JSON. Growth analysis project historical data and reports are in `adhoc_jobs/website_growth/`.

## Notes

- Kit API rate limit: 120 requests / 60 seconds
- GA4 Data API has quota limits; the snapshot command runs multiple reports in one call, avoid calling too frequently
- GSC Data API has a 25,000 row/request limit; the tool has built-in pagination; data has a 2-3 day delay
- Typefully engagement API is a private API and may change at any time
- `short_url.db` is a local sync copy, not a real-time database. Confirm the last sync time before analysis.
- `short_url` clicks and Circle registrations have no user-level join. It is suitable for multi-layer signal comparison on the same tag, not for precise end-to-end conversion rates.
- All tools default to JSON output to stdout; format with `| python3 -m json.tool`
