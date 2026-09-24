# Apple Compressor Skill

## Metadata

- Type: API Guide
- Use when: submitting, monitoring, pausing, resuming, or cancelling local Apple Compressor transcoding jobs from the command line
- Last updated: 2026-09-23

## Goal

Use Apple Compressor's CLI to submit transcoding batches reliably, then verify that the batch entered Compressor, the expected targets exist, output files start writing, and the final outputs complete.

This skill is useful for video workflows where another application, such as DaVinci Resolve, writes a source movie and Compressor should start only after that source file is complete.

## Trigger Phrases

- `Compressor`
- `Apple Compressor`
- `compressor preset`
- `custom preset`
- `Dolby preset`
- `batch transcode`
- `wait for Resolve export`
- `transcode after file finishes writing`

## Local Resources

Compressor app:

```bash
/Applications/Compressor.app
```

CLI entrypoint:

```bash
/Applications/Compressor.app/Contents/MacOS/Compressor
```

Common user setting location on recent macOS / Compressor installs:

```text
$HOME/Library/Group Containers/<TEAM_ID>.com.apple.videoProApps/Library/Application Support/Compressor/Settings/
```

Find custom settings by listing the settings directory or checking Compressor's group container. Do not assume older paths such as `$HOME/Library/Application Support/Compressor/Settings` exist.

## Boundaries

Compressor may not expose a usable AppleScript dictionary. If `sdef /Applications/Compressor.app` fails, do not try to build an AppleScript object-model workflow.

Prefer the CLI. GUI automation is a fallback because it depends on window state, permission prompts, and UI labels.

Do not submit a file that is still being written by Resolve or another process. Confirm file stability first with `lsof` and file-size checks.

## Submit A Batch

`-locationpath` must be a complete output file path, including the output file name. It cannot be only an output directory.

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" \
  -batchname "Example transcodes" \
  -priority medium \
  -jobpath "file:///path/to/input.mov" \
  -settingpath "$HOME/Library/Group Containers/<TEAM_ID>.com.apple.videoProApps/Library/Application Support/Compressor/Settings/high_res.compressorsetting" \
  -locationpath "$HOME/Downloads/input-high_res.mov" \
  -jobpath "file:///path/to/input.mov" \
  -settingpath "$HOME/Library/Group Containers/<TEAM_ID>.com.apple.videoProApps/Library/Application Support/Compressor/Settings/proxy.compressorsetting" \
  -locationpath "$HOME/Downloads/input-proxy.mov" \
  -outputformat json
```

Successful submission returns a batch id and one or more job ids:

```json
{
  "batch": {
    "batchID": "<batch_id>",
    "jobs": [
      {"jobID": "<job_id>"}
    ]
  }
}
```

One `jobID` can contain multiple targets. Do not infer target count only from the number of jobs in the JSON response. Verify target names through Compressor storage, monitoring, or output files.

## Monitor A Batch

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" \
  -monitor \
  -format json \
  -batchid "<batch_id>" \
  -once
```

On at least some Compressor versions, `-format json` must be placed immediately after `-monitor`. Placing it at the end can fail with `Invalid parameter: -format`.

Expected monitor fields include `status`, `percentComplete`, `timeRemaining`, `batchid`, and `jobid`. For continuous monitoring, omit `-once` and use `-query <seconds>` plus `-timeout <seconds>`.

`status` values include `Processing`, `Waiting`, `Successful`, `Failed`, and `Cancelled`. A status of `Waiting` (often accompanied by an empty `jobs` array) indicates that the batch is queued but no background processing service is currently idle; this is not a failure by itself. Transcoding will proceed once a service becomes free, though an unavailable service state may surface in the GUI as `No service available for processing this job`.

To verify whether transcoding is actively running, inspect the transcoder service log at `~/Library/Logs/Compressor/servicecontroller:com.apple.stomp.transcoder.stomp.log`. For each target, this log records `Preflighting` (including `Virtual service count = N`, where `0` means no processing service is currently idle), `preProcess ... done`, and `starting _processRequest for job target: ...`. Upon completion, it records `Time for AVAssetWriter transcode <seconds> seconds. Done _processRequest for job target: ...`. If a job remains stalled at `Processing 0%` or `Waiting` without new entries written to this log, Compressor is not actively encoding.

Check whether output files are being written:

```bash
lsof "$HOME/Downloads/input-high_res.mov"
ls -lT "$HOME/Downloads/input-high_res.mov" "$HOME/Downloads/input-proxy.mov"
```

Check Compressor storage for source and target names in a small scoped path:

```bash
grep -R "input\|input-high_res\|input-proxy" \
  "$HOME/Library/Group Containers/<TEAM_ID>.com.apple.videoProApps/Library/Application Support/Compressor/Storage"
```

In an AI coding harness, prefer scoped grep/read tools over global home-directory searches.

## Wait For The Source File

Before submitting, confirm both conditions:

1. `lsof /path/to/source.mov` shows no writer process.
2. File size remains stable for a short window, such as 60 seconds.

One-off check:

```bash
lsof "$HOME/Downloads/input.mov"
stat -f '%z %m %Sm' "$HOME/Downloads/input.mov"
sleep 60
stat -f '%z %m %Sm' "$HOME/Downloads/input.mov"
```

For long waits, use the workspace's durable process launcher or scheduler rather than bare `sleep` / `nohup`. Write watcher logs to a temporary workspace directory.

## Acceptance Criteria

A Compressor task is complete only when these checks pass:

1. The source file is no longer being written and its size is stable.
2. Compressor returns a `batchID`, or `-monitor` can read the target `batchid`.
3. Compressor storage contains the source path and expected output names, or the output files exist and are being written by Compressor's transcoder.
4. For multi-preset jobs, every expected target name is confirmed in storage or on disk.
5. Final monitoring shows completion, or all expected output files stop changing and no writer process holds them open.
6. Deliverable integrity is verified: completion requires at least a `-monitor` status of `Successful` and a corresponding `Done _processRequest` entry in the stomp log for each target. Perform a full decode check on every final output to detect stream truncation that basic metadata inspection misses: if `ffmpeg` is available, run `ffmpeg -v error -i "$HOME/Downloads/input-high_res.mov" -f null -` (no stdout/stderr output and exit code 0 indicates a clean decode). Confirm with `ffprobe` that the output duration matches the source file duration.

## Known Pitfalls

`-locationpath` with only a directory fails with `Parameter error: Destination is a directory; Expected complete output file path with file name.` Provide a full output path like `$HOME/Downloads/input-high_res.mov`.

Omitting `-locationpath` can appear to succeed with exit code 0 while leaving no easily verifiable output or storage entry. For production tasks, pass an explicit output path for every target.

`-monitor` argument order matters. Put `-format json` immediately after `-monitor`.

`fileURL is NOT a directory` may appear on stderr even for successful submissions. Judge success by `batchID`, `-monitor`, Compressor storage, and output files.

A single returned job id can still contain multiple targets. Verify all output target names explicitly.

`No service available for processing this job` in the GUI does not indicate an issue with the source file. It occurs when a running Compressor GUI loses connection to the background transcoding services—typically because background helper processes (`CompressorHelper`, `TranscoderService`, or `JobControllerService`) restarted while the GUI remained open, leaving the GUI holding stale service references. To resolve this, quit and relaunch the Compressor GUI, or restart background processing with `Compressor -resetBackgroundProcessing`. Because CLI invocations spawn fresh processes that connect directly to live helpers, CLI submissions often succeed even when the stale GUI fails.

Receiving a `batchID` indicates only that the batch was queued, not that transcoding has started. A submission returning a `batchID` and `jobID`—or even an initial `status` of `Processing`—does not guarantee active encoding. Use `-monitor` to verify that `percentComplete` and `timeElapsedSeconds` are genuinely incrementing, and cross-reference the stomp transcoder log. A job can stall at `Processing 0%` or `Waiting` with `timeElapsed` remaining `0` simply because it is waiting for an idle processing service; do not treat this state prematurely as either a failure or a success.

Temporary segment files (`.sb-<hash>`) appear alongside the output file during encoding for jobs where segmentation is enabled (`job-can-be-segmented yes`). These are in-progress working chunks rather than standalone files, and Compressor automatically cleans them up when the target completes or is cancelled. Do not treat these temporary files as finished outputs or as evidence of data loss. However, if a batch is killed midway through encoding, the output file may be left partially written and truncated; always validate deliverables before downstream use.

Preset file names do not reliably indicate output resolution. If a `.compressorsetting` file configures `video-encode` `bounds` or `automatic` width and height to `-100`, the preset dynamically inherits the source resolution ("same as source" / adaptive) rather than enforcing a fixed dimension. Furthermore, `.compressorsetting` files are custom `<setting>` XML documents rather than standard Apple property lists; parsing them with `plutil` will fail with an error. Read the XML file directly to confirm true resolution bounds, codec, and frame rate before relying on the preset name.

Avoid duplicate submissions between the GUI and CLI. Both interfaces share the same local processing service and process targets serially. If a job has already been submitted through the GUI, submitting it again via the CLI creates a duplicate batch queued behind it, encoding the same targets a second time. Before submitting, run `lsof` against the source file, inspect batch folders in Compressor's `Storage` directory, and search the stomp transcoder log for the destination target name to confirm that an active batch is not already running.

## Control Commands

Pause a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -pause -batchid "<batch_id>"
```

Resume a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resume -batchid "<batch_id>"
```

Cancel a batch:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -kill -batchid "<batch_id>"
```

Restart Compressor background processing:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resetBackgroundProcessing
```

Cancelling queued jobs while restarting background processing is destructive. Get explicit user approval first:

```bash
"/Applications/Compressor.app/Contents/MacOS/Compressor" -resetBackgroundProcessing cancelJobs
```
