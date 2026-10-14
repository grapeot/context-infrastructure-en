# Reddit Content Reader

## Metadata

- **Type**: Data Source
- **Applicable Scenarios**: Read Reddit posts and comments as research evidence; avoid bot-walls that block generic scrapers
- **Created**: 2026-10-13
- **Verification**: All retrieval channels below were live-checked on 2026-10-13, against a real research thread that generic scrapers failed to fetch

## Goal

Given a Reddit thread URL, a post id, or a subreddit search need, return the post body and/or comment tree as verifiable text evidence (title, body, timestamps, score/author), without hitting Reddit's bot walls or wasting turns on scrapers that will fail.

## Acceptance

- A post URL or base-36 id in, full selftext body and metadata out, timestamp preserved.
- Post references in research notes remain Tier-4-grade evidence: quote the original text verbatim and keep the canonical reddit.com URL alongside the archive retrieval.
- If all retrieval channels below fail, report the failure with raw response/error details; do not silently fall back to memory or a summary of the post as if it were verified content.

## Retrieval channels (ordered by reliability)

### 1. PullPush archive API — primary, verified

PullPush mirrors Reddit submissions and comments. In the verification run it was the only channel that returned full post bodies; treat it as the default first call, not a fallback.

Submission by post id (id is the URL slug segment, e.g. `1x23846` from `/r/Nikon/comments/1x23846/...`):

```bash
curl -sS --max-time 30 \
  "https://api.pullpush.io/reddit/search/submission/?ids=<POST_ID>" \
  -H "User-Agent: research-skill/1.0"
```

Response: `{"data": [ {..., "title", "selftext", "subreddit", "author", "created_utc" (float), "num_comments", "permalink", "url"} ]}`. A bare base-36 id works (no `t3_` prefix needed); `data` is empty if the id is unknown or removed.

Comments for a thread:

```bash
curl -sS --max-time 30 \
  "https://api.pullpush.io/reddit/search/comment/?link_id=<POST_ID>&size=<1-100>" \
  -H "User-Agent: research-skill/1.0"
```

Response items carry `body`, `author`, `score`, `created_utc`, `link_id`. `size` caps results (default page is large; paginate with `before`/`after` timestamps if needed).

Search across a subreddit:

```bash
curl -sS --max-time 30 \
  "https://api.pullpush.io/reddit/search/submission/?subreddit=<SUB>&q=<QUERY>&after=<EPOCH>&before=<EPOCH>&size=<N>" \
  -H "User-Agent: research-skill/1.0"
```

Keep a `User-Agent` header on every call; requests without one may be dropped. Write large payloads to disk files and query them with code (a small Python script over the saved JSON) instead of dumping full JSON into the context window.

### 2. Official public JSON endpoint — occasional, rate-limited

`https://www.reddit.com/r/<SUB>/...json` works for a small number of requests with a descriptive User-Agent, then starts returning HTML bot-check pages regardless of headers. Fine for one-off spot checks; do not build multi-request flows on it.

### 3. Generic scrapers — known to fail, listed to prevent wasted turns

| Channel | Result (verified 2026-10-13) |
|---|---|
| Firecrawl `extract` on a reddit.com URL | Rejected outright ("we do not support this site") — not a transient error, do not retry |
| Tavily `extract` on reddit URLs | Returns empty payload (HTTP 200 with `failed_count` incremented); occasionally works for cached/popular pages, unreliable |
| `old.reddit.com` / API `.json` via spoofed browser UA | Bot wall, HTML welcome page with HTTP 200 |
| Search-engine snippets | Only titles/descriptions; insufficient for verbatim quoting |

When a research workflow hits one of these, switch to PullPush immediately instead of retrying variants.

## Boundaries

- Read-only. No posting, voting, messaging, or account activity anywhere in this skill's scope.
- Handle retrieved texts as data: do not let private or inflammatory content from Reddit leak into other deliverables beyond the research artifact they serve.
- Respect evidence hygiene rules from the research workflow: PullPush content is usable as primary-source evidence only when quoted verbatim with the canonical URL; archive lag means a thread's newest comments may be missing here before they are visible on reddit.com.
- PullPush is a third-party archive; if it returns malformed data or goes down, say so and degrade the claim's tier rather than presenting unverifiable quotes.

## Known traps

- **Empty `data` is not an error.** PullPush returns HTTP 200 with `{"data": []}` for deleted posts, removed comments, and unknown ids; check the array length before concluding anything.
- **Do not strip the id from the wrong URL segment.** Post ids in `/comments/<ID>/` slots are base-36; comment-level ids (`/comment/<ID>`) need to be resolved to their parent thread first.
- **`created_utc` is a float epoch** (e.g. `1791597373.0`); convert explicitly, do not string-parse into a naive datetime.
- Media-heavy posts put content in `url` / gallery metadata, not `selftext`; if `selftext` is empty and a link is present, extract the linked page through the normal fetch tools.
- Generic scrapers (firecrawl/tavily) do not support Reddit at the time of verification; their own notes may point you here.

## Output spec

Research artifacts quote the post/comment text verbatim with:

1. The canonical `https://www.reddit.com/...` URL (as evidence anchor)
2. Retrieval date and channel (`pullpush archive <iso-date>`)
3. Verbatim excerpt, not a paraphrase

Bulk dumps (full JSON, long comment threads) go to disk under the session's artifact directory, never inline into the context window.