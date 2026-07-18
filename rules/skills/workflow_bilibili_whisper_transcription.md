# Video Download and Speech Recognition Workflow (Qwen ASR Priority)

## Metadata
- Type: Workflow
- Applicable Scenarios: Bilibili/YouTube video batch download + local speech recognition (default Qwen ASR 1.7B)
- Created: 2025-02-12
- Last Updated: 2026-04-04
- Original project archived (no longer retained in workspace)

## Path Conventions

- Temporary downloads and intermediate artifacts: `tmp/<task_name>/`
- Final long-term-retained transcripts: `adhoc_jobs/videos_transcribe/transcripts/`
- Final default retention: **plain text transcript without timestamps only**; recommended filename: `YYYYMMDD_platform_videoid_short_slug.md`
- Audio, `.srt`, `.vtt`, `.tsv`, `.json` and other intermediate artifacts cleaned up to trash after transcript is persisted

## Core Flow

**Three-stage workflow:**

1. **Get list** → Use yt-dlp to extract video IDs (note Bilibili API limits; may return 352 errors)
2. **Single-threaded download** → Download audio one by one, 2-3 second interval between each, to avoid triggering anti-scraping
3. **Local transcription** → Default runs MLX Qwen ASR 1.7B; only fall back to Whisper for compatibility or regression reasons

## Key Decisions

| Decision Point | Choice | Reason |
|----------------|--------|--------|
| Download concurrency | Single-threaded | Avoid triggering Bilibili anti-scraping mechanisms |
| Transcription concurrency | Multi-process (4-8) | CPU-intensive; fully utilize multi-core |
| Model selection | Default Qwen ASR 1.7B | Timestamps are not the main deliverable by default; full text matters more |
| Output format | Final retention: plain text transcript | More stable for subsequent retrieval; intermediate artifacts recyclable |

## Default Choice: Qwen ASR 1.7B

Current recommended default model: `Qwen/Qwen3-ASR-1.7B`

Reasons:

1. Runs locally on Apple Silicon via `mlx-qwen3-asr`
2. Friendlier for Chinese scenarios
3. On real samples, produces fewer long repeated hallucinations than Whisper
4. Most video transcription scenarios do not need word-level timestamps; keeping the full text better fits subsequent retrieval and summarization

Recommended invocation:

```bash
python <videos_transcribe_dir>/transcribe.py \
  --input input.mp4 \
  --output transcripts/output.md \
  --model Qwen/Qwen3-ASR-1.7B \
  --language auto
```

By default keep only the full text; add this only when segmented text is explicitly needed:

```bash
--include-segments
```

## Whisper as Fallback

| Model | Parameters | Speed (CPU) | Accuracy | Recommended Scenario |
|-------|-----------|-------------|----------|----------------------|
| tiny | 39M | 1-2 min / 10 min | Lower | Quick preview |
| base | 74M | 2-5 min / 10 min | Medium | Balanced choice |
| small | 244M | 5-10 min / 10 min | Higher | Daily use |
| medium | 769M | 10-20 min / 10 min | High | High-quality needs |
| large-v3 | 1550M | 20-60 min / 10 min | Highest | Maximum quality requirements |

Whisper is still a valid fallback, especially when:

- Reusing an old workflow
- Needing consistency with historical results
- Explicitly wanting Whisper-style timestamped output

## Qwen ASR Usage Tips

1. **Timestamps usually not needed**: most knowledge-organization, video-summary, full-text-search scenarios care only about the final text, not the timeline.
2. **Keep the full text first, then decide whether to keep segments**: full text is the main deliverable; segmented text is an optional sidecar.
3. **1.7B is the current default not because it is absolutely most accurate, but because it is a more stable default starting point**.
4. **If the goal is very low latency or batch throughput, consider 0.6B**; if the goal is one-shot high-quality full text, try 1.7B first.
5. **Watch for Whisper's repetition hallucination in long silence / low-information segments**; Qwen ASR is more conservative on such samples, often outputting nothing or less.

## LLM Post-Processing

Whisper/Qwen raw output typically requires post-processing:

1. **Convert to Simplified Chinese** — recognition may be Traditional Chinese
2. **Add punctuation** — Add commas, periods, question marks based on semantics
3. **Reasonable paragraphing** — Divide into paragraphs by topic; add subheadings
4. **Correct terminology** — Domain-specific term recognition errors (e.g., "木质布"→"木质部", "筛管细胞")
5. **Optimize readability** — Adjust word order; supplement missing content

## Lessons Learned

| Problem | Symptom | Solution |
|---------|---------|----------|
| **352 Error** | Request blocked by Bilibili | Add User-Agent/Referer headers; increase delay; or manually obtain IDs |
| **404 Error** | Video deleted or ID incorrect | Verify ID validity; skip invalid videos; record failed IDs |
| **Out of Memory** | Memory overflow during multi-process transcription | Reduce parallel process count (4-6); use smaller model; process in batches |
| **Incomplete Download** | .m4a file unplayable | Check file size; re-download; add integrity verification |
| **Transcription Too Slow** | large-v3 single video 20-60 min | Choose appropriate model size; use GPU acceleration; chunk long videos |

## Best Practices

**Download phase:** Single-threaded + 2-3 second delay + User-Agent headers + audio-only download + record failed IDs

**Transcription phase:** Default Qwen ASR 1.7B + `language=auto` + keep full text by default; enable `--include-segments` only when segments are needed

**Persistence phase:** Complete download and transcription in `tmp/`; after organizing plain text transcript, move into `adhoc_jobs/videos_transcribe/transcripts/`

**Cleanup phase:** After transcript is persisted, delete or trash audio, timestamped subtitles, and sidecar files; retain only the final transcript

**Quality optimization:** Try Qwen ASR 1.7B first; switch to Whisper fallback to align with historical Whisper results; manual proofreading when necessary

**Error handling:** Implement retry mechanism; verify file integrity; handle exceptions to avoid script interruption
