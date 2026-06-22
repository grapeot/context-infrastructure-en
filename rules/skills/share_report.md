# Skill: Share Report to Web

Convert Markdown reports to bilingual (Chinese + English) HTML and publish to yage.ai/share, returning accessible URLs. An English translation is auto-generated for every publish.

## When to Use

Trigger phrases: "share this", "publish this", "give me a public link", or any request to share a Markdown article for others to read.

## Prerequisites

- pandoc: `/opt/homebrew/bin/pandoc`
- SSH passwordless login to `yage`
- Project directory: `adhoc_jobs/yage_share/` (contains `manifest.json`, `gen_index.py`, `site/`, `md_archived/`)
- Image archive directory: `adhoc_jobs/yage_share/md_archived/assets/<slug>/`. All relative images referenced in Markdown must be archived here alongside the Markdown, so future site-level rebuilds do not depend on the original draft directory or remote servers.
- Templates inside the yage_share project (tracked by `adhoc_jobs/yage_share/` nested git repo):
  - `adhoc_jobs/yage_share/templates/share_report.css` — main stylesheet (includes `.site-nav`, `.brand-footer` styles)
  - `adhoc_jobs/yage_share/templates/share_report_ga4.html` — GA4 loader (dynamic script injection version, **must read** key constraints)
  - `adhoc_jobs/yage_share/templates/share_report_nav.html` / `adhoc_jobs/yage_share/templates/share_report_nav_en.html` — Chinese/English nav bar (with Superlinear Academy brand link)
  - `adhoc_jobs/yage_share/templates/share_report_progress.html` — reading progress bar (2px fixed top, injected into all articles)
  - `adhoc_jobs/yage_share/templates/share_report_cta.html` — Chinese Kit subscription CTA (Chinese version only)
  - `adhoc_jobs/yage_share/templates/share_report_brand_footer.html` / `adhoc_jobs/yage_share/templates/share_report_brand_footer_en.html` — article-end brand signature bar ("100% AI-generated · Superlinear Academy" + community signup CTA, Chinese/English versions)
  - `adhoc_jobs/yage_share/templates/share_report_disqus.html` — Disqus comment embed (dynamic script injection)
- Post-processing scripts (under `adhoc_jobs/yage_share/`):
  - `inject_seo.py` — inject SEO meta + canonical link
  - `inject_tags.py` — inject tag badges
  - `inject_publish_time.py` — inject publish time below title from manifest `date`
  - `inject_lang_switch.py` — inject Chinese/English language switch + hreflang
  - `inject_theme_toggle.py` — inject article page theme restore script + theme toggle button
  - `gen_rss.py` — generate RSS 2.0 feeds from manifest (`feed.xml` Chinese, `feed-en.xml` English, latest 50 indexed articles each)

## "Full Publish Pipeline" Definition

When the user says "run the full publish flow", "publish to all channels", or "complete the full publishing pipeline", execute all three channels simultaneously:

1. **yage_share**: Bilingual publish (Chinese + English), `indexed: true` (both languages enter their respective homepages and RSS). Articles with images also upload standalone image files to `imgs/<slug>/`.
2. **Circle**: Post to Deep News (space 2535452), Chinese version only. If there are images, use standalone image URLs in the body.
3. **Twitter/X**: Post a Typefully long post with Twitter UTM tracked URL. If there are images, use standalone image URLs (Twitter/X auto-expands to card). Schedule 1-2 minutes ahead. Article distribution is not constrained by the 280-character tweet limit by default; do not compress information to fit a regular tweet length. Only when the user explicitly requests "regular tweet", "under 280 characters", or "short tweet" should you rewrite to fit X's length limit.

The three channels are independent and can run in parallel (after yage_share's `publish_report.py` completes, image upload, Circle publish, and Twitter schedule can all start simultaneously). See respective skill files: `rules/skills/circle_post.md`, `rules/skills/typefully_twitter.md`.

## Two Independent Switches: publish vs include in index

`publish` = upload HTML to `yage.ai/share/<slug>.html`; anyone with the link can access it. `include in index` = list the article on the `/share/` homepage public listing. These are two separate switches. **Default: publish only.** Only when the user explicitly says "add it to the index", "list it publicly", or "include it on the homepage" should you set `indexed: true` and refresh the index. When the user says "run the full publish flow", "publish to all channels", or "complete the full publishing pipeline", `indexed` is also `true` because the article is simultaneously posted to Circle and Twitter/X; not listing it on the homepage would break distribution coherence.

`adhoc_jobs/yage_share/manifest.json` is the local source of truth. **Do not upload it to the server by default.**

## Publish Workflow

### 1. Translate English Version

Read the Chinese MD, translate to English MD. Keep technical terms in original English, preserve the original paragraph structure, and translate title and description as well. Naming: insert `-en` before the date in the Chinese slug, e.g. `attention-residuals-intuition-20260318` → `attention-residuals-intuition-en-20260318`.

Run subsequent steps once for each language version.

### 2. Check Original Source Links

If the article depends on external facts, data, or quotes, confirm before publishing that the original source links are already in the final MD body (or appendix), not only in scratchpad / search manifest / stdout. The English version should also retain clickable links.

### 3. Run publish_report.py (replaces old manual steps 3-8)

Starting from step 3, all mechanical steps are handled by `publish_report.py` in one pass: H1 dedup → pandoc conversion → manifest update → MD archive → 5 inject scripts → conditional index/RSS → integrity check → upload → curl verification → git commit.

```bash
cd adhoc_jobs/yage_share

# Chinese version (unindexed, temporary)
./.venv/bin/python publish_report.py \
  --md <zh-md-path> \
  --slug <slug> \
  --title "Article Title" \
  --description "Article description (1-2 sentences)" \
  --tags "Tag1" "Tag2" \
  --temporary

# Bilingual version (public indexed, both languages enter respective homepages/RSS)
./.venv/bin/python publish_report.py \
  --md <zh-md-path> \
  --en-md <en-md-path> \
  --slug <slug> \
  --title "Chinese Title" \
  --en-title "English Title" \
  --description "Chinese description" \
  --en-description "English description" \
  --tags "Chinese Tag 1" \
  --en-tags "English Tag 1" \
  --indexed

# --index-en is deprecated; English indexed status always follows Chinese

# Dry run to preview the plan
./.venv/bin/python publish_report.py ... --dry-run

# Build only, no upload (local debugging)
./.venv/bin/python publish_report.py ... --skip-upload
```

Parameter reference:

| Parameter | Required | Description |
|------|------|------|
| `--md` | Yes | Chinese Markdown path (relative to workspace root) |
| `--slug` | Yes | URL slug, lowercase English + hyphens, date suffix (e.g. `article-20260511`) |
| `--title` | Yes | Chinese article title |
| `--description` | Yes | Chinese article description (1-2 sentences) |
| `--tags` | Yes | 1-3 Chinese tags, from `docs/tag_taxonomy.md` |
| `--en-md` | No | English Markdown path (if provided, publish bilingual) |
| `--en-title` | No | English title (required when `--en-md` is provided) |
| `--en-description` | No | English description (same as above) |
| `--en-tags` | No | English tags (same as above) |
| `--date` | No | Publish date YYYY-MM-DD (default: today) |
| `--author` | No | Author name (default: configured site author) |
| `--indexed` | No | Include in site index/RSS (default: false) |
| `--index-en` | No | Deprecated; English `indexed` status always follows Chinese |
| `--temporary` | No | Mark as temporary article (default: false, auto-skips Kit CTA) |
| `--skip-kit-cta` | No | Skip Kit CTA injection even for Chinese version |
| `--dry-run` | No | Validate parameters, print plan, do not execute |
| `--skip-upload` | No | Build only, no upload (local debugging) |

The script is designed to be idempotent and safe to re-run. When a slug already exists, it updates the manifest entry in-place (replaces at original position) rather than inserting a duplicate. On re-run, the git commit verb auto-switches from `add` to `update`.

What the script does not do automatically (requires AI judgment): translate the English version, select tags, write descriptions, generate slugs. These parameters are prepared by the AI before calling the script.

Chinese version (with Kit CTA + brand signature bar):

```bash
pandoc /tmp/<slug>_no_h1.md \
  -o adhoc_jobs/yage_share/site/<slug>.html \
  --standalone --embed-resources \
  --metadata title="<Report Title>" \
  --css adhoc_jobs/yage_share/templates/share_report.css \
  --include-in-header=adhoc_jobs/yage_share/templates/share_report_ga4.html \
  --include-before-body=adhoc_jobs/yage_share/templates/share_report_progress.html \
  --include-before-body=adhoc_jobs/yage_share/templates/share_report_nav.html \
  --include-after-body=adhoc_jobs/yage_share/templates/share_report_cta.html \
  --include-after-body=adhoc_jobs/yage_share/templates/share_report_brand_footer.html \
  --include-after-body=adhoc_jobs/yage_share/templates/share_report_disqus.html
```

English version (uses English nav and English brand signature bar, **does not inject** Kit CTA since the Kit form is Chinese):

```bash
pandoc /tmp/<slug-en>_no_h1.md \
  -o adhoc_jobs/yage_share/site/<slug-en>.html \
  --standalone --embed-resources \
  --metadata title="<English Title>" \
  --css adhoc_jobs/yage_share/templates/share_report.css \
  --include-in-header=adhoc_jobs/yage_share/templates/share_report_ga4.html \
  --include-before-body=adhoc_jobs/yage_share/templates/share_report_progress.html \
  --include-before-body=adhoc_jobs/yage_share/templates/share_report_nav_en.html \
  --include-after-body=adhoc_jobs/yage_share/templates/share_report_brand_footer_en.html \
  --include-after-body=adhoc_jobs/yage_share/templates/share_report_disqus.html
```

**Note the order of the two post-body components**: Kit CTA is Chinese-only and must come before the brand signature bar. The brand signature bar appears before Disqus, so readers see the "100% AI-generated" contrast + community entry immediately after the body, then the comment section.

**Note: the pandoc command does not include `--include-in-header=/tmp/<slug>_seo.html`**. SEO meta (including canonical link) goes through step 4's `inject_seo.py` post-processing, not through pandoc. See the "Key Constraints" section below for the reason.

Articles with local images: place images in the same directory as the MD source file, reference them with relative paths in MD (e.g. `![](chart.png)`). `publish_report.py` auto-adds `--resource-path` pointing to the MD's directory based on the `--md` path; pandoc's `--embed-resources` converts images to base64 embedded in the HTML. Relative images are also copied to `md_archived/assets/<slug>/...`. After publishing, verify with `grep -c 'data:image' site/<slug>.html` that the count is > 0.

Batch rebuilds depend on the image archive at `md_archived/assets/<slug>/...`. Do not archive only the Markdown and drop the images; otherwise, when `republish_indexed.py` does site-level rebuilds (CSS / SEO / nav), pandoc will degrade relative image paths to bare relative paths, and the live site may try to access `/share/<filename>` instead of the uploaded `/share/imgs/<slug>/<filename>`, causing broken images.

**Circle posting note**: Relative image paths in MD (`![](chart.png)`) are fine as base64 inline in yage.ai HTML, but when submitting to Circle, `circle_post.py convert` puts relative paths verbatim into TipTap JSON, which Circle cannot load, resulting in "media was deleted" after publishing. Therefore: upload standalone image files to the server (step below), get absolute URLs, then replace relative paths in the Circle-destined MD with `https://yage.ai/share/imgs/<slug>/<filename>.png` before convert → publish.

Images also need to be uploaded as standalone files to the server for Twitter/Circle and other channels to directly reference the URL:

```bash
SLUG="<slug>"
ssh yage "mkdir -p /var/www/yage/share/imgs/$SLUG"
rsync -av <image files> yage:/var/www/yage/share/imgs/$SLUG/
ssh yage "chmod 644 /var/www/yage/share/imgs/$SLUG/*"
curl -s -o /dev/null -w "%{http_code}" "https://yage.ai/share/imgs/$SLUG/<img>.png"  # Confirm 200
```

Standalone image URL format: `https://yage.ai/share/imgs/<slug>/<filename>.png`. When reporting to the user after publish, include each image's standalone URL.

### 4. Update manifest.json + Archive MD (must run before inject)

**All three inject scripts (step 5) read the article list from manifest.json. If the manifest does not yet contain this entry, inject will skip the new article. This step must complete before running step 5.**

Insert two entries (Chinese + English) at the top of the `articles` array in `adhoc_jobs/yage_share/manifest.json`. Required fields: `slug`, `title`, `date`, `description`, `author` (grapeot), `lang` (zh/en), `indexed` (default false), `tags` (1-3, from `docs/tag_taxonomy.md`). Optional: `is_temporary` (default false), `md_path`. The English version's `is_temporary` and `indexed` both follow the Chinese version. Public indexed articles must have both languages publicly listed; Chinese indexed with English unindexed is a manifest error.

**Tag language rule**: Chinese articles use Chinese display names for `tags`; English articles use English display names. Bilingual paired articles share the same set of semantic tags, but the display text switches with `lang`. Do not copy Chinese tags directly into English articles.

```bash
cp <final Chinese MD path> adhoc_jobs/yage_share/md_archived/<slug>.md
cp <final English MD path> adhoc_jobs/yage_share/md_archived/<slug-en>.md
```

Archive the final published version, not intermediate drafts. `md_archived/` is the source for subsequent Circle publishing, batch republish, and other scenarios — required. When there are relative images, `publish_report.py` syncs image archiving to `md_archived/assets/<slug>/...`; manual publishing must also copy the same directory structure.

### 5. Post-Processing: Inject SEO / tags / language switch / theme toggle

```bash
cd adhoc_jobs/yage_share
python3 inject_seo.py        # Inject description / og / canonical / robots from manifest
./.venv/bin/python inject_tags.py   # Inject tag badges from manifest
./.venv/bin/python inject_publish_time.py  # Inject publish time below title from manifest
python3 inject_lang_switch.py              # Inject Chinese/English switch links + hreflang
python3 inject_theme_toggle.py             # Inject article page theme restore script + toggle button
```

All five scripts are idempotent; they iterate over all articles in the manifest and auto-process new ones. **If the output shows no `INJECTED <slug>` and is all `ALREADY HAS SEO`, the manifest is missing that entry or the slug doesn't match — go back to step 4.**

### 6. Conditional Index + RSS Update

Only run when `indexed: true`:

```bash
cd adhoc_jobs/yage_share && python3 gen_index.py && python3 gen_rss.py
```

`gen_index.py` reads `manifest.json` by default (relative path) and outputs to `site/index.html`. Must `cd adhoc_jobs/yage_share` or explicitly pass `--manifest` / `--output`. It generates `index.html`, not uploading the manifest itself.

### 7. Upload

```bash
# Single article upload
rsync adhoc_jobs/yage_share/site/<slug>.html yage:/var/www/yage/share/
rsync adhoc_jobs/yage_share/site/<slug-en>.html yage:/var/www/yage/share/
ssh yage "chmod 644 /var/www/yage/share/<slug>.html /var/www/yage/share/<slug-en>.html"

# If index was updated
rsync adhoc_jobs/yage_share/site/index.html yage:/var/www/yage/share/
rsync adhoc_jobs/yage_share/site/feed.xml yage:/var/www/yage/share/
rsync adhoc_jobs/yage_share/site/feed-en.xml yage:/var/www/yage/share/
ssh yage "chmod 644 /var/www/yage/share/index.html /var/www/yage/share/feed.xml /var/www/yage/share/feed-en.xml"
```

**Do not use `rsync site/ remote:` for full-directory upload**. The local `site/` contains both indexed and unindexed files; full-directory upload would accidentally expose or overwrite unindexed private content. Batch uploads must use `--files-from=<whitelist>` or use `republish_indexed.py` directly (see below).

Any `rsync` with `--delete` **must first `--dry-run`** and manually confirm the deletion list.

### 8. Verify + git commit

```bash
curl -s -o /dev/null -w "%{http_code}" https://yage.ai/share/<slug>.html       # 200
curl -s -o /dev/null -w "%{http_code}" https://yage.ai/share/<slug-en>.html    # 200
curl -s -o /dev/null -w "%{http_code}" https://yage.ai/share/                  # 200 (if indexed)

cd adhoc_jobs/yage_share && git add manifest.json && git commit -m "add: <slug> (zh+en)"
```

## Final Report Format

When reporting back to the user, must include:

1. **Indexed status**: Explicitly state `indexed: true` or `indexed: false` (true means the article is publicly listed on the homepage and RSS; false means only people with the link can access it)
2. **Direct URL**: `https://yage.ai/share/<slug>.html`
3. **WeChat UTM URL**: `https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>`

For bilingual publishes, also provide both URL types for the English version. **Missing any item means the workflow is incomplete.**

**All URLs must be output in Markdown link format** (`[display text](url)`), not plain text URLs or bare `url` links. Plain text URLs are not clickable in terminals and some clients, forcing the user to manually copy-paste. Markdown link format ensures clickability in all environments.

**WeChat UTM URL special note**: The WeChat URL is the sole channel for sharing in WeChat mobile, formatted as `[https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>](https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>)`. In the final report, this URL must be a clickable Markdown link, not a bare URL or wrapped in a code block.

Recommended final report snippet:

```markdown
**WeChat Share Link**
[https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>](https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>)
```

Do not write:

```markdown
WeChat: https://yage.ai/share/<slug>.html?utm_source=wechat&utm_medium=share&utm_campaign=<slug>
```

The latter is not clickable in some clients, and the user cannot directly open it from the assistant's reply.

## Batch Republish

To uniformly apply a site-level change (CSS upgrade, GA4 fix, SEO field adjustment, etc.) to all indexed articles, use `adhoc_jobs/yage_share/republish_indexed.py`:

```bash
python3 republish_indexed.py              # dry-run, see upload list
python3 republish_indexed.py --confirm    # real upload
python3 republish_indexed.py --lang zh    # restrict language
```

This script only reads `indexed: true` entries and uses `--files-from=<whitelist>` for rsync, never touching unindexed files. See `adhoc_jobs/yage_share/AGENTS.md` for details.

Image safety: `republish_indexed.py` prioritizes resolving relative images from `md_archived/assets/<slug>/...`. If a historical article has no local image archive but the remote standard location `/share/imgs/<slug>/<filename>` still exists, the script first syncs images back to the local archive, then uses local files to embed in HTML. This remote sync is a one-time bootstrap and should not become a long-term dependency; new articles must archive images at publish time.

## Slug Naming + URL

Lowercase English, words joined with `-`, ending with `YYYYMMDD`. Example: `iran-war-survey-20260302`. Final URL: `https://yage.ai/share/<slug>.html`.

## Key Constraints

**GA4 loader must use dynamic script injection**. `adhoc_jobs/yage_share/templates/share_report_ga4.html` is currently a dynamic injection version (`document.createElement('script')` mounts src at runtime), bypassing pandoc `--embed-resources` fetch behavior for external `<script src>`. If reverted to static `<script src="https://googletagmanager.com/...">` form, pandoc will base64-inline the entire ~415KB gtag.js into every HTML, ballooning files from ~33KB to ~460KB. Any new external script resources (Plausible, Segment, etc.) must follow the same dynamic injection pattern. Post-verification: `grep -c 'Copyright 2012 Google' site/<slug>.html` should be 0.

**SEO meta goes through inject_seo.py post-processing, not pandoc's `--include-in-header`**. pandoc's `--embed-resources` sees `<link rel="canonical" href="https://...">` as an external resource to fetch, base64-inlining the remote HTML into the generated HTML, triggering exponential file bloat. If the old workflow injected SEO via pandoc's `--include-in-header=/tmp/<slug>_seo.html`, it must be changed to post-pandoc `python3 inject_seo.py`. Post-verification: `grep -c 'data:text/html' site/<slug>.html` should be 0; normal article HTML total size should be 30-80KB (articles with images can be larger).

**Any `rsync --delete` must first dry-run**. Production safety rule.

**Claude Code / Cloud Code typo check**. For articles involving Claude Code, grep the filename, slug, manifest, and SEO before publishing for accidental Cloud Code misspellings. Publicly published errors persist long-term.

**Naming consistency**. Source MD filename, date suffix, slug, manifest `date`, and final URL must all match. When an article has been renamed or its date updated, fix the source first, then generate HTML.

**Publish time only in manifest.** The body Markdown must not manually write "publish time", "publish date", "research date", "Published on", or other opening date lines. The publish pipeline uses `inject_publish_time.py` to inject the time from the manifest's `date` field below the title. Before and after publishing, check that the final HTML has exactly one `article-publish-time` and no duplicate date explanation at the body start.

**Brand elements and article page theme CSS are centralized in `adhoc_jobs/yage_share/templates/share_report.css`**. Nav, brand footer, and theme toggle `<style>` blocks must **not** be inlined back into HTML partial files. pandoc `--embed-resources` handles CSS selector conflicts as specificity priority; generic selectors (`.site-nav a`) can override class selectors (`.site-nav-back`). A unified external CSS file keeps the style hierarchy clear. Batch site-level changes (CTA copy, logo, brand color, theme toggle) use `republish_indexed.py`, which re-runs the full pandoc + inject pipeline.

**Article page theme sync is a dual-track design**. The index page manages `localStorage.theme` on its own; article pages rely on `inject_theme_toggle.py` to restore this value in the head and write it to `<html data-theme>`. `share_report.css` must support both explicit `data-theme` and system `prefers-color-scheme`. Changing only CSS or only the script will re-split the index/article theme fork.

**The share directory is publicly accessible**. Do not upload sensitive content. To delete published content: `ssh yage "rm /var/www/yage/share/<slug>.html"`.

**Do not execute the full pipeline in one shot**. Preprocessing + pandoc + inject + gen_index + rsync + curl should not be crammed into a single ultra-long command. A more stable order: generate local HTML → post-process inject → refresh index → upload → verify links.

## Twitter/X UTM Attribution

When syncing a share report to Twitter, use the tracked URL:

```
https://yage.ai/share/<slug>.html?utm_source=twitter&utm_medium=thread&utm_campaign=<slug>
```

UTM belongs only to the distribution layer and does not enter canonical / og:url / manifest / page source main address. The tracked URL goes only in the last tweet. See `rules/skills/typefully_twitter.md` for the detailed posting workflow.

## Before Tweeting: R/T/N Form Determination (Required Before Writing Copy)

Before writing Twitter copy, determine which tweet form this article should use. Do not write by feel. R/T/N is a functional classification of tweets, based on topic×form resonance data from 269 historical tweets annotated on 2026-06-10 (analysis at `adhoc_jobs/website_growth/docs/rtn_analysis_0610.md`, background objective function at `adhoc_jobs/website_growth/docs/project_context.md`). This rule set is private, used only in this workspace; do not write it into any public skill.

Three forms:

- **R (Reach)**: Pure opinion/judgment post without external links, aimed at expanding influence and gaining followers. Write a specific, counterintuitive, first-person judgment as the hook, expand the argument in the body, do not include the article link. Follower growth is heavily concentrated in this type, and the common thread is "what a person with judgment is thinking", not information relay.
- **T (Traffic)**: Includes a yage.ai article link, aimed at driving readers to the long-form article on the site. Write a clear traffic hook (what specific question this article answers / what specific numbers it gives), put the tracked URL in the last tweet.
- **N (Newsletter)**: Includes a subscription CTA. Under current strategy, subscription CTAs are rarely done in tweets (newsletter growth relies on article page CTAs), so default to not choosing N unless there is a clear reason.

Check this table by article topic to determine the form (left-high = good for R opinion posts, right-high = good for T traffic posts):

| Article Topic | Preferred Form | Basis |
|---|---|---|
| Engineering judgment / practice | **R** (strong) | R follower gain 16.4/post highest; with link, clicks only 108/post. Readers will follow for engineering opinions but won't click into long articles |
| Reasoning / infra | **Both R and T strong** | R follower gain 16.8/post, T clicks 578/post — both among the highest. The only topic worth doing both forms |
| Model release / news timeliness | **R** | R median exposure 5,891 highest; on release day readers want instant judgment, traffic post clicks only 189/post. Article traffic can go the next day |
| Safety / compliance / legal | **T** | T clicks 428/post, median exposure 3,853 high; R follower gain only 0.3/post. Readers will click in for specific security events but won't follow for the topic |
| Agent engineering / architecture | **T slightly preferred** | T clicks 498/post; R follower gain 5.9/post moderate |
| Industry / product observation | **R slightly preferred** | R median exposure 2,608, follower gain 6.9/post |
| AI workflow / management | Either works | Largest volume but moderate per-post efficiency; occasional breakout T posts can outperform the baseline |

Determination steps: classify the article topic → check the table for form → write copy per that form's requirements. If an article suits both reach and traffic, you can first post an R opinion post to harvest exposure, then post the T traffic post a day or two later.

Note the form choice and rationale in one line of the publish report (e.g. "Per R/T/N, this article falls under 'engineering judgment' topic, using R opinion post, no link"), to facilitate future retrospective accumulation of this rule set's hit rate. This is the "zero-labeling" implementation: the AI auto-classifies when generating copy, no manual labeling needed.

## Post to Twitter (Optional)

After determining the form and writing approach per the previous section, use `adhoc_jobs/typefully_twitter_skill/.venv/bin/typefully-twitter` to create or schedule a Typefully draft. Tweets with URLs should not be published instantly; create a draft first or schedule for a slightly later time. See `rules/skills/typefully_twitter.md` for details.

Default to Typefully long post. When `post count` returns `long_post: true` and `status: OK`, proceed to schedule; do not additionally apply the 280-character regular tweet limit. Only when the user explicitly requests a short tweet should you use regular tweet length as a hard constraint.

Chinese-audience accounts default to posting in Chinese.

## Scheduled Publish

### Trigger Phrases

"schedule publish", "publish in 3 hours", "publish tomorrow morning", "delayed publish", "run the full flow in X hours".

### Goal

Package the full publish pipeline (translation + images + yage_share + Circle + Twitter) into a self-contained OpenCode prompt, scheduled for execution at a specified time via Process Launcher's `delay_seconds` or `run_at`. The user does not need to manually operate at publish time, and the agent does not need to keep the session alive waiting.

### Acceptance Criteria

After scheduling, all of the following must hold:

1. Process Launcher's `/scheduled` endpoint shows this job, status `pending`, `run_at` matching the user's requested time
2. OpenCode `submit --dry-run` was run before scheduling to verify OpenCode server connectivity
3. The prompt file is written to `tmp/` and is self-contained: includes article path, slug, title, description, tags, image paths, channel selection, and all necessary information — the OpenCode agent receiving this prompt should need to ask zero questions to complete the full publish pipeline
4. The prompt explicitly requires the OpenCode agent to write the publish result to a specified location (e.g. `tmp/<slug>_publish_result.md`) after completion

### Available Resources

- **Process Launcher**: `http://localhost:7997`, provides `POST /run` with `delay_seconds` and `run_at` parameters, persisted to SQLite, launcher restores `pending` jobs on restart. See `rules/skills/process_launcher.md`
- **OpenCode Skill**: `adhoc_jobs/opencode_skill/.venv/bin/python -m opencode_skill submit`, accepts `--prompt-file`. See `rules/skills/opencode_job_submission.md`
- **Publish Pipeline**: The full publish chain defined in the preceding sections of this file

### Operation Workflow

Scheduled publishing has two steps: prepare the prompt file, then submit the delayed job. The two steps have a dependency (the job needs the prompt file to exist), but the specific execution within each step is decided by the agent based on the actual situation.

**Step 1: Prepare a self-contained prompt file.** Write all information needed for publishing into a Markdown file at `tmp/<slug>_publish_prompt.md`. This file is the sole input for the OpenCode agent executing the publish task and must contain:

- Chinese MD path and English MD path (if already translated)
- slug, title (Chinese + English), description (Chinese + English), tags (Chinese + English)
- Whether indexed
- Image file paths (if there are images)
- Channel selection: yage_share is mandatory, Circle and Twitter per user request
- Explicitly require the OpenCode agent to first read `rules/skills/share_report.md` to understand the publish workflow, then execute
- Explicitly require writing the publish result (URLs, success status) to `tmp/<slug>_publish_result.md` after completion

After writing the prompt file, run the checklist: can the OpenCode agent, given this file, complete the full publish pipeline without asking any questions? If any parameter requires the agent to guess, add it.

**Step 2: Schedule via Process Launcher.** Before scheduling, run OpenCode dry-run to verify connectivity:

```bash
cd /Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill
.venv/bin/python -m opencode_skill submit --prompt-file prompt.md --title "Dry-run test" --dry-run --json
```

After dry-run succeeds (returns `OK`), submit the delayed job via Process Launcher. The job's command is calling OpenCode submit, with `delay_seconds` or `run_at` matching the user's requested time:

```bash
# Using delay_seconds (e.g. 6 hours = 21600 seconds)
curl -X POST http://localhost:7997/run \
  -H 'Content-Type: application/json' \
  -d '{
    "command": ["/Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill/.venv/bin/python",
                "-m", "opencode_skill", "submit",
                "--prompt-file", "/Users/grapeot/co/knowledge_working/tmp/<slug>_publish_prompt.md",
                "--title", "Publish: <slug>",
                "--send-timeout", "300"],
    "cwd": "/Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill",
    "label": "publish-<slug>",
    "delay_seconds": 21600,
    "timeout": 1800
  }'

# Or using run_at (absolute time, with misfire_policy)
curl -X POST http://localhost:7997/run \
  -H 'Content-Type: application/json' \
  -d '{
    "command": ["/Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill/.venv/bin/python",
                "-m", "opencode_skill", "submit",
                "--prompt-file", "/Users/grapeot/co/knowledge_working/tmp/<slug>_publish_prompt.md",
                "--title", "Publish: <slug>",
                "--send-timeout", "300"],
    "cwd": "/Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill",
    "label": "publish-<slug>",
    "run_at": "2026-06-13T04:00:00-07:00",
    "misfire_policy": "run_immediately",
    "timeout": 1800
  }'
```

Parameters easy to miss:

- **`cwd`**: `opencode_skill submit` depends on `.env` in the current directory to load credentials and endpoint configuration. Without `cwd`, the launcher's default working directory may be wrong, causing submit to pick up the wrong base URL or agent name.
- **`--send-timeout 300`**: After submitting the prompt, OpenCode needs a few seconds for handshake; the default send timeout may be too short. 300 seconds covers handshake and initial response without false timeout errors.
- **`timeout: 1800`**: The full publish pipeline (pandoc + rsync + Circle API + Typefully) may take 5-10 minutes; set a 30-minute hard timeout to prevent zombie processes.

After scheduling, verify the job was created:

```bash
curl -sf http://localhost:7997/scheduled | python -m json.tool | grep -A5 "publish-<slug>"
```

### Post-Scheduling Report to User

After scheduling completes, report the following to the user:

1. Job ID and label
2. Expected execution time (`run_at`)
3. Prompt file path
4. Reminder: Process Launcher must be running at execution time (if the machine reboots or the launcher is shut down, the job will be handled per `misfire_policy` when the launcher restarts)
5. Publish result will be written to `tmp/<slug>_publish_result.md`; the user can check it after the execution time

### Known Pitfalls

**Process Launcher not running.** Before scheduling, check if the launcher is online: `curl -sf http://localhost:7997/health`. If non-200 or connection refused, start the launcher in a terminal or tmux (`cd adhoc_jobs/background_job_manager && ./scripts/start.sh`). The launcher needs to be started from a GUI terminal to get TCC permissions; see `rules/skills/process_launcher.md` notes.

**OpenCode server not running.** If dry-run fails, check if the OpenCode server is online (`curl -sf http://localhost:4096/health`); if not, start it (`knowledge_working/start_opencode.sh`).

**Prompt not self-contained enough.** If the prompt file misses key parameters like slug, tags, or indexed status, the OpenCode agent will stall or make wrong assumptions during execution. When writing the prompt, cross-check against the `publish_report.py` parameter table in the preceding sections. A more aggressive approach is to write all publish commands (pandoc args, rsync paths, Circle space ID, Typefully commands) directly into the prompt, so the agent doesn't need to read share_report.md or other skill files — even if the agent misinterprets a skill when reading it, execution won't be affected.

**Delay spans machine sleep.** If the scheduled time is late at night and the machine may sleep, using `run_at` + `misfire_policy: run_immediately` is safer than `delay_seconds`. The launcher will immediately catch up on missed `pending` jobs after restart.

**OpenCode submit agent selection.** Publish tasks need to read files, run commands, and call multiple skills — use the `general` agent. Explicitly specify the agent type in the prompt file, or set it via environment variable `OPENCODE_AGENT=general` in the submit command.

**Missing `cwd` causes submit to load wrong config.** `opencode_skill submit` reads `OPENCODE_BASE_URL`, credentials, and agent config from `.env` in the current working directory. When Process Launcher's `POST /run` doesn't pass `cwd`, the working directory may not be the `opencode_skill` project root, causing submit to pick up the wrong endpoint or agent name — manifesting as HTTP 200 but no assistant response. Always explicitly pass `"cwd": "/Users/grapeot/co/knowledge_working/adhoc_jobs/opencode_skill"` when scheduling.

**zsh `?` glob trap.** In zsh, writing `curl http://localhost:7997/processes?running_only=true` directly gets treated as a glob pattern matching filenames, erroring with `no matches found`. When verifying launcher status, wrap the entire URL in single quotes: `curl -sf 'http://localhost:7997/processes?running_only=true'`.

**`run_at` timezone format.** Process Launcher accepts ISO 8601 with timezone offset, e.g. `2026-06-12T15:42:33-07:00`. On macOS, `date -v+3H '+%Y-%m-%dT%H:%M:%S%z'` produces `20260612T124233-0700` (missing colons); manually insert colons to get `2026-06-12T12:42:33-07:00`, or use `date -u -v+3H '+%Y-%m-%dT%H:%M:%SZ'` with UTC to avoid timezone format issues.
