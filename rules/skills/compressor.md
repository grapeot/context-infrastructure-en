# Apple Compressor Skill

## Metadata

- Type: API Guide
- Use when: submitting, monitoring, pausing, resuming, or cancelling video transcoding jobs via Apple Compressor CLI on this machine
- Last updated: 2026-06-12

## Goal

Reliably submit transcoding batches through Apple Compressor's command-line entrypoint, and verify with confirmable checks that the job entered the Compressor queue, output files started writing, and the batch completed.

This skill primarily serves local video workflows, especially auto-submitting custom Dolby presets after DaVinci Resolve finishes exporting.

## Trigger Phrases

- `Compressor`
- `Apple Compressor`
- `compressor preset`
- `Dolby preset`
- `8k60pDolby`
- `2k60pDolby`
- `batch transcode`
- `transcode after Resolve finishes exporting`

## Local Resources

Compressor app:

```bash
/Applications/Compressor.app
```

CLI entrypoint:

```bash
/Applications/Compressor.app/Contents/MacOS/Compressor
```

Local custom settings directory:

```text
/Users/grapeot/Library/Group Containers/PTN9T2S29T.com.apple.videoProApps/Library/Application Support/Compressor/Settings/
```

Confirmed custom presets:

```text
2k60pDolby.compressorsetting
8k60pDolby.compressorsetting
8kTV.compressorsetting
h265_SDR.compressorsetting
```

`2k60pDolby` is also Compressor's current default custom setting, recorded in `.DefaultSettingInfo`.

## Boundaries

Compressor does not expose a stable AppleScript dictionary; `sdef /Applications/Compressor.app` will fail. Do not attempt AppleScript object-model control of Compressor by default.

Prefer the CLI. GUI automation is a last resort — it is more fragile than CLI, sensitive to window state, permission prompts, and UI label changes.

Do not submit a source file while Resolve or another process is still writing it. Confirm completion with `lsof` and file size stability first.

## Submitting Jobs

Basic command structure. `-locationpath` must be a complete output file path including filename, not just a directory.

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" \
  -batchname "Example Dolby transcodes" \
  -priority medium \
  -jobpath "file:///Users/grapeot/Downloads/input.mov" \
  -settingpath "/Users/grapeot/Library/Group Containers/PTN9T2S29T.com.apple.videoProApps/Library/Application Support/Compressor/Settings/8k60pDolby.compressorsetting" \
  -locationpath "/Users/grapeot/Downloads/input-8k60pDolby.mov" \
  -jobpath "file:///Users/grapeot/Downloads/input.mov" \
  -settingpath "/Users/grapeot/Library/Group Containers/PTN9T2S29T.com.apple.videoProApps/Library/Application Support/Compressor/Settings/2k60pDolby.compressorsetting" \
  -locationpath "/Users/grapeot/Downloads/input-2k60pDolby.mov" \
  -outputformat json
```

On success, Compressor returns a batch id and job id(s):

```json
{
  "batch": {
    "batchID": "86F264AF-60C1-445C-B870-597CB6814AB2",
    "jobs": [
      {"jobID": "34EE03A7-7D31-4768-A50D-458495B4ABC4"}
    ]
  }
}
```

One `jobID` can still contain multiple targets. Do not assume the second preset was not submitted just because the response shows only one job. Verify targets through job storage files or output files.

## Monitoring Jobs

Monitor a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" \
  -monitor \
  -format json \
  -batchid "BATCH_ID" \
  -once
```

`-format json` must come after `-monitor`. `-monitor -batchid ... -once -format json` fails with `Invalid parameter: -format` on this machine.

Typical response includes `status`, `percentComplete`, `timeRemaining`, `batchid`, and `jobid`. For continuous monitoring, remove `-once` and add `-query <seconds>` and `-timeout <seconds>`.

Check whether output files are actually being written:

```bash
lsof "/Users/grapeot/Downloads/input-8k60pDolby.mov"
ls -lT "/Users/grapeot/Downloads/input-8k60pDolby.mov" "/Users/grapeot/Downloads/input-2k60pDolby.mov"
```

Check Compressor job storage for source file paths and target names:

```bash
grep -R "input\|input-8k60pDolby\|input-2k60pDolby" \
  "/Users/grapeot/Library/Group Containers/PTN9T2S29T.com.apple.videoProApps/Library/Application Support/Compressor/Storage"
```

In OpenCode, prefer the `grep` tool for scoped directory searches; do not run global searches across the entire home or workspace.

## Waiting for Source File Completion

While Resolve is exporting, the source `.mov` may already exist and keep growing. Before submitting, satisfy at least these two conditions:

1. `lsof /path/to/source.mov` shows no Resolve or other writer process.
2. File size remains stable over a short window, e.g. 60 seconds.

One-shot check:

```bash
lsof "/Users/grapeot/Downloads/input.mov"
stat -f '%z %m %Sm' "/Users/grapeot/Downloads/input.mov"
sleep 60
stat -f '%z %m %Sm' "/Users/grapeot/Downloads/input.mov"
```

If the user asks to check periodically and auto-submit when ready, do not use bare `sleep` / `nohup` as a long-running background task. Read `rules/skills/process_launcher.md` first and use Process Launcher to start a watcher, writing logs to `tmp/<session_slug>/` or `tmp/compressor_watch/`.

## Acceptance Criteria

A Compressor operation is successful only when all of the following hold:

1. Source file is confirmed no longer being written, and file size is stable.
2. Compressor CLI returns a `batchID`, or `-monitor` can find the corresponding `batchid`.
3. Compressor job storage shows the source file path and target output names, or output files exist on disk and are being written by the `Transcode` process.
4. For multi-preset jobs, all target output names are confirmed in job storage or on the filesystem; do not rely solely on the job count in the batch response.
5. Final `-monitor` shows batch completion, or both output files are no longer being written and their sizes are stable.

## Known Pitfalls

`-locationpath` given as a directory only will fail. The error is `Parameter error: Destination is a directory; Expected complete output file path with file name.` Provide a full output file path, e.g. `/Users/grapeot/Downloads/input-8k60pDolby.mov`.

Omitting `-locationpath` can result in Compressor exiting with code 0 but producing no verifiable output or job cache entry containing the new source file. Always pass an explicit output path for every target in production jobs.

`-monitor` argument order matters. `-format json` at the end fails with `Invalid parameter: -format`; place it immediately after `-monitor`.

`fileURL is NOT a directory` may appear on stderr even for successful submissions. Do not treat this log line alone as a failure indicator. Judge by `batchID`, `-monitor`, job storage, and output files.

Compressor returning one job id does not mean only one target was submitted. Multiple `-jobpath/-settingpath/-locationpath` combinations can merge into a single job containing multiple targets internally.

## Common Control Commands

Pause a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -pause -batchid "BATCH_ID"
```

Resume a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resume -batchid "BATCH_ID"
```

Cancel a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -kill -batchid "BATCH_ID"
```

Restart Compressor background processing:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resetBackgroundProcessing
```

Cancelling all queued jobs and restarting background processing is destructive — requires explicit user authorization:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resetBackgroundProcessing cancelJobs
```
