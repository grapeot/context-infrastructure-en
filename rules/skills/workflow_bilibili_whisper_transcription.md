# Video Download and Speech Recognition Workflow

## Metadata
- Type: Workflow
- Applicable Scenarios: Bilibili/YouTube video batch download + Whisper speech recognition
- Created: 2025-02-12
- Last Updated: 2026-03-11
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
3. **Multi-process transcription** → Run Whisper in parallel, 4-8 processes, choose model size based on hardware

## Key Decisions

| Decision Point | Choice | Reason |
|----------------|--------|--------|
| Download concurrency | Single-threaded | Avoid triggering Bilibili anti-scraping mechanisms |
| Transcription concurrency | Multi-process (4-8) | CPU-intensive; fully utilize multi-core |
| Model selection | Based on needs | See table below |
| Output format | Final retention: plain text transcript | More stable for subsequent retrieval; intermediate artifacts recyclable |

## Whisper Model Selection

| Model | Parameters | Speed (CPU) | Accuracy | Recommended Scenario |
|-------|-----------|-------------|----------|----------------------|
| tiny | 39M | 1-2 min / 10 min | Lower | Quick preview |
| base | 74M | 2-5 min / 10 min | Medium | Balanced choice |
| small | 244M | 5-10 min / 10 min | Higher | Daily use |
| medium | 769M | 10-20 min / 10 min | High | High-quality needs |
| large-v3 | 1550M | 20-60 min / 10 min | Highest | Maximum quality requirements |

**Performance reference**: 12 videos (3.5 hours) + large-v3 + 7 processes ≈ 20 minutes

## LLM Post-Processing

Whisper raw output typically requires post-processing:

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

**Transcription phase:** Multi-process (4-8) + specify language parameter + skip already-processed files + choose model based on hardware

**Persistence phase:** Complete download and transcription in `tmp/`; after organizing plain text transcript, move into `adhoc_jobs/videos_transcribe/transcripts/`

**Cleanup phase:** After transcript is persisted, delete or trash audio, timestamped subtitles, and sidecar files; retain only the final transcript

**Quality optimization:** Use large-v3 for critical content; use base/small for quick preview; manual proofreading when necessary

**Error handling:** Implement retry mechanism; verify file integrity; handle exceptions to avoid script interruption
