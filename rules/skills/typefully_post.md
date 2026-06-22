# Skill: Typefully Post CLI

Create drafts, schedule publishing, and immediately publish tweets and threads via the Typefully v2 API.

## When to Use

Trigger when the user says:
- Post a tweet
- Post to Twitter / Post to X
- Post this to Twitter
- Schedule a tweet
- Sync to Twitter after share report publish

## Prerequisites

- Root `.env` contains:
  - `TYPEFULLY_API_KEY`: Typefully API key
  - `TYPEFULLY_SOCIAL_SET_ID`: Social set ID for the target account
- Python venv activated
- Dependencies installed: `pip install -r tools/requirements.txt`

Generate the Typefully API key in Settings → API. The social set ID comes from your own Typefully account configuration.

## Five Publishing Rules

1. **Default to single tweet, not thread**: Only use a thread when the content naturally needs to be split into 2-4 tweets, or when the user explicitly requests a thread.
2. **Prefer scheduling for tweets with URLs**: This workflow defaults to scheduling URL-bearing tweets 1-2 minutes ahead, not immediate `now`. This is more stable and allows a final check of copy and links.
3. **URLs with UTM**: Links should use tracked URLs, e.g. `https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post`.
4. **Validate length with weighted count**: Run `count` before publishing; do not estimate 280 characters by eye. URLs count as 23, CJK characters typically count as 2.
5. **Explicitly enable long post**: Use `--long-post` when exceeding standard tweet length. Long post and thread are two different formats; do not mix them.

## Usage

All commands run from the repo root.

### Single Tweet

```bash
python tools/typefully_post.py draft --text "Hello from the API!"
python tools/typefully_post.py post --text "Going live now!" --publish-at now
python tools/typefully_post.py post --text "Tomorrow morning" --publish-at "2026-04-20T16:00:00Z"
python tools/typefully_post.py count --text "Draft tweet with URL https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
```

### Long Post

```bash
python tools/typefully_post.py post --text "$(cat long_post.md)" --publish-at "2026-04-20T16:00:00Z" --long-post
```

### Thread

Thread file format: separate each tweet with `---`.

```bash
python tools/typefully_post.py post --thread-file my_thread.md
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
printf "First tweet\n---\nSecond tweet" | python tools/typefully_post.py post --thread-stdin
```

### Draft Management

```bash
python tools/typefully_post.py list --status published --limit 10
python tools/typefully_post.py list --status draft
python tools/typefully_post.py get 12345
python tools/typefully_post.py publish 12345
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
python tools/typefully_post.py schedule 12345 --next-free-slot
python tools/typefully_post.py delete 12345
python tools/typefully_post.py draft --text "tweet content" --draft-title "Launch post"
```

## Pre-Publish Check

Run weighted count with the local CLI first:

```bash
python tools/typefully_post.py count --text "Your copy https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
python tools/typefully_post.py count --thread-file my_thread.md
```

Output shows each tweet's `weighted_length/280`, marking over-limit ones as `TOO_LONG`.

## Writing Habits

- Observation first: Start with an observation, number, or choice that shifts the reader's judgment, then give the conclusion
- One tweet carries one main judgment; treat the link as extended reading
- Default to one URL only. Single tweet: at the end. Thread: in the last tweet
- Engineer-leaning tone. Write judgments and observations, not summaries

## Optional Workflow

If you already have your own sharing workflow, you can chain this skill after it:

1. First publish the article or report, get the public URL
2. Add UTM parameters to the URL
3. Write tweet copy, run `count` first
4. Finally use `post` or `draft + schedule` to send

## Notes

- `--publish-at` supports `now`, `next-free-slot`, or ISO time
- `post --thread-file` is good for creating thread drafts first; if you need precise timing control, `draft` then `schedule` is more direct
- `TYPEFULLY_API_KEY` and `TYPEFULLY_SOCIAL_SET_ID` should both be provided by the user; do not write them into the repo
