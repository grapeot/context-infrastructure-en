# Antigravity CLI File-Based Invocation

## Metadata

- Type: API Guide
- Use when: using Antigravity subscription quota to run a Gemini agent for writing, rewriting, review, or file processing
- Command: `agy`
- Verified version: 1.1.5 (2026-07-21)

## Core Distinction

`agy-ide` is an IDE launcher. Its `chat` subcommand sends a prompt to the graphical interface; it is not a headless agent CLI. Automation must use the separate Antigravity CLI, `agy`.

## First Run: Detect, Review, Install

Check for the command before the first use on each machine. Download the official installer to a temporary file, review it, and only then execute it:

```bash
if ! command -v agy >/dev/null 2>&1; then
  installer="$(mktemp)"
  curl -fsSL https://antigravity.google/cli/install.sh -o "$installer"
  less "$installer"  # Review the downloaded script before executing it.
  bash "$installer"
  rm -f "$installer"
fi
```

The installer URL is mutable. The reviewed-installer path is appropriate only for a trusted personal workstation. On a managed or security-sensitive machine, use a versioned asset from the [official GitHub release](https://github.com/google-antigravity/antigravity-cli/releases), pin the version, and verify the downloaded archive against the SHA-256 digest published in that release's GitHub asset metadata before extracting or executing it. If the organization cannot approve the release and digest, do not install the CLI.

The installer normally places the binary at `~/.local/bin/agy`. If the current shell still cannot find it, run the installer's environment setup and then open a new shell:

```bash
~/.local/bin/agy install
```

Complete the initialization checks:

```bash
agy --version
agy --help
agy models
```

`agy` 1.1.5 has no standalone `login` command. `agy models` or the first `agy --print` attempts to retrieve Antigravity credentials silently from the system keyring. If the machine is not authenticated, sign in with Google through the Antigravity App or IDE, then retry `agy models`.

`agy` uses the Antigravity subscription and system keyring. It does not read `GEMINI_API_KEY`. Do not fall back to an API key, because that switches to API billing rather than the subscription route this skill covers.

Initialization is complete only when `command -v agy` returns a valid path, `agy --version` exits successfully, and `agy models` lists models.

## File-Based Invocation Contract

Every production invocation uses three layers of files:

1. **Task file**: write the complete prompt to `tmp/<session>/agy_<task>_prompt.md` inside the workspace.
2. **Result file**: require the agent to write the complete deliverable to an explicit path such as `tmp/<session>/agy_<task>_result.md`.
3. **Run records**: save CLI stdout, stderr, and `--log-file` separately. Stdout is a completion note, not the deliverable.

Prompts, results, stdout, stderr, and event logs may contain task text, paths, account metadata, or model events. They are local-only runtime artifacts. Keep them under a git-ignored `tmp/`; never commit, upload, publish, or share them. The repository must ignore at least `tmp/`, `*.log`, `.env`, and `.env.*`, while allowing a sanitized `.env.example` when needed.

Do not place a long prompt directly on the command line. Pass only a driver prompt that tells the agent to read the complete task file. Keep task files, references, and outputs in the launch directory or its descendants.

Launch from a minimal trusted scratch workspace containing only inputs required for the task. Do not launch from a home directory, a broad monorepo root, or a directory containing credentials, `.env` files, customer data, or unrelated private material. `--sandbox` limits tool behavior; it does not guarantee that every file in the workspace stays out of remote model context. Inspect the scratch workspace before each production run and remove unrelated secrets or private data.

## Standard Command

Use `gemini-3.6-flash-high` (Gemini 3.6 Flash High) by default for writing and prose QA:

```bash
agy --print \
  "Read the complete task from /absolute/path/to/agy_task_prompt.md and follow it exactly." \
  --model "gemini-3.6-flash-high" \
  --mode accept-edits \
  --sandbox \
  --dangerously-skip-permissions \
  --print-timeout 10m \
  --log-file "/absolute/path/to/agy_task_events.log" \
  > "/absolute/path/to/agy_task_stdout.txt" \
  2> "/absolute/path/to/agy_task_stderr.txt"
```

`--print` / `-p` is a top-level flag, not a subcommand. AGY 1.1.5 has no `agy run` subcommand and no `--trust`, `--format`, or `--output-events` flags. Do not copy another agent CLI's command shape: `agy run ...` enters the wrong interactive path and may fail with a Bubble Tea `/dev/tty` error or hang in a non-TTY subprocess. Persist diagnostics and events with `--log-file` only.

AGY 1.1.5 retains the headless `--print` support for persisted `settings.json` policies introduced in 1.1.4. Permissions, file access, sandbox mode, auto-execution, and artifact review settings can affect non-interactive runs. Before a production invocation, inspect both global and project-level AGY settings in addition to the command-line flags; do not assume print mode is isolated from persisted configuration.

Set the outer process timeout to about 610 seconds. `--print-timeout 10m` is AGY's internal wait limit; the extra time allows process shutdown and log flushing.

Use `--dangerously-skip-permissions` only together with `--sandbox`, and only in the minimal trusted scratch workspace described above. The task file must name one output path or enumerate a bounded set of output paths, then prohibit modification of every file outside that list.

## Models and Observability

After first installation or an upgrade, run `agy --version`, `agy --help`, and `agy models`. Models verified with AGY 1.1.5 on 2026-07-21 include:

- `gemini-3.6-flash-low` (Gemini 3.6 Flash Low)
- `gemini-3.6-flash-medium` (Gemini 3.6 Flash Medium)
- `gemini-3.6-flash-high` (Gemini 3.6 Flash High)
- `gemini-3.5-flash-low`, `gemini-3.5-flash-medium`, `gemini-3.5-flash-high`
- `gemini-3.1-pro-low`, `gemini-3.1-pro-high`

Always pass `--model` explicitly. Do not rely on an interactive `/model` setting. Treat an invalid model name as a failure; do not silently fall back.

AGY 1.1.5 has no `--json` or streaming JSON output. Use `--log-file` for observability. Events such as `Print mode: starting`, `silent auth succeeded`, `streamGenerateContent`, tool confirmation, and shutdown help establish liveness. Startup logs may report an unauthenticated state before keyring-based silent authentication succeeds; judge the run by its final exit status and result file.

A run is complete only when all checks pass:

1. The process exits with code 0.
2. Every designated result file exists and is non-empty.
3. The results satisfy hard constraints for structure, numbers, URLs, and other task requirements.
4. Stdout contains a completion note and stderr contains no unhandled error.

A timeout or any missing or empty result file is a failed run. Never substitute a stdout summary for the requested artifacts.

## External-Writing Task Packet

For external writing, AGY does not read the complete workflow, `COMMUNICATION.md`, or `bestpractice_external_prose.md`. The Main Agent first establishes the article's source of truth and compresses the requirements into a small writer packet. AGY then performs complete drafting only.

A Round 2 candidate task file includes at least:

```markdown
# Task

Read these files completely:
1. `/absolute/path/to/source_contract.md`
2. `/absolute/path/to/writing_brief.md`
3. `/absolute/path/to/voice_contract.md`
4. `/absolute/path/to/content_map.md`

Write the complete result to:
`/absolute/path/to/result.md`

Do not modify any other file.

## Task

- Write one complete external-facing article from a blank page.
- Use only facts, scenes, causal claims, and boundaries present in `source_contract.md` and `content_map.md`.
- Preserve the thesis, claim strength, numbers, URLs, image references, and immutable terms.
- Follow `voice_contract.md`. Do not output an audit, explanation, invariant count, or PASS statement.
- Decide H2 wording and paragraph entrances independently. Do not copy content-map labels or research taxonomy into the article outline.
- Use normal paragraphs. Do not put every sentence on its own line.
```

`source_contract.md` should include an immutable-term list for product names, model names, API names, code identifiers, easily mistranslated terms, and labels that must remain verbatim. In practice, AGY may proactively translate terms such as `Oracle`, `reset card`, or `system of record`; without this list, factual wording can drift.

## Fresh Context, Parallel Candidates, and One Retry

Each `agy --print` call without `--continue` or `--conversation` creates a fresh conversation. The external-writing workflow uses three kinds of AGY calls:

- **Round 2 parallel candidates**: By default, start two fresh conversations from the same task packet. They independently write `candidate_a.md` and `candidate_b.md`; neither reads nor revises the other. Prefer different available model families when possible.
- **Round 3 blind reader**: For each candidate, start a fresh conversation that reads only the candidate body and writes `blind_reader_audit_a.md` or `blind_reader_audit_b.md`. It neither fact-checks nor decides `PASS`.
- **Round 4 optional revision**: Start one fresh conversation only when the Main Agent's cold-read acceptance returns `RETRY_PROSE`. It reads the selected candidate, original task packet, and a `revision_delta.md` containing no more than three to five blockers, then writes one complete revision.

The AGY writer does not write QA and is not the `PASS` authority. The Main Agent first writes `main_cold_read_a.md` or `main_cold_read_b.md` from the candidate alone, then reads the blind-reader audit, checks numbers, URLs, images, and structure deterministically, and judges factual fidelity and whole-article voice. Round 3 records exactly one verdict in `acceptance_audit.md`:

- `ACCEPT`: Content and prose may proceed to surgical completion.
- `RETRY_PROSE`: Thesis and structure are sound, but one complete prose rewrite can address specific blockers.
- `RETURN_TO_ROUND_1`: Thesis, evidence, structure, or the source contract must be repaired upstream.

Round 4 is allowed at most once. If a non-surgical blocker remains, return to the Main Agent's upstream artifacts or report the failure; do not start another AGY conversation automatically.

After acceptance, the Main Agent may perform logged surgical completion for typos, punctuation, Markdown, proper nouns, and local single-sentence corrections uniquely determined by `source_contract.md`. Record every change in `completion_edits.md`. This contract does not permit changing the thesis, reordering sections, splicing candidates, or rewriting whole paragraphs without returning to acceptance.

Give every call separate prompt, result, stdout, stderr, and events files. Include the purpose in each filename, for example:

- `agy_candidate_a_prompt.md` / `agy_candidate_a_events.log`
- `agy_candidate_b_prompt.md` / `agy_candidate_b_events.log`
- `agy_revision_prompt.md` / `agy_revision_events.log`

## Limitations

- No JSON or streaming JSON output.
- Stdout is unsuitable as the primary artifact.
- Event logs are implementation details for liveness checks, not a stable business API.
- `agy-ide chat` opens or reuses a GUI and is not a headless fallback.
- AGY may invoke agent tools and take longer than a single API request. Use the 10-minute timeout and do not retry indefinitely.

## Validation Records

On 2026-07-14, a smoke test was completed on macOS arm64 with AGY 1.1.2:

- Reading the task from a persisted prompt file succeeded.
- Writing the designated result file inside the sandbox succeeded.
- Stdout redirection succeeded; stderr was empty.
- The event log contained timestamped auth, model request, file tool, and shutdown records.
- Using `Gemini 3.5 Flash (High)`, a ~2,000-word memo rewrite completed while preserving all 17 URLs.
- The first rewrite exposed technical-term mistranslation, line-by-line wrapping, and first-person drift; these improved markedly after adding an immutable term list and a normal-paragraph constraint.
- A fresh AGY conversation also completed an independent prose-QA experiment while preserving the Top 5 ordering, four-paragraph structure, two deep-dive candidates, and all 17 URLs. Later writing runs showed that writer self-review is not a reliable `PASS` decision. The current workflow therefore keeps acceptance with the Main Agent and permits at most one fresh prose retry.

On 2026-07-20, the CLI interface and headless path were rechecked on macOS arm64 with AGY 1.1.4:

- The official GitHub latest release and local `agy --version` both reported 1.1.4.
- `agy --help` confirmed that headless execution remains the top-level `--print` / `-p` flag, with no `run` subcommand or JSON event flags.
- `agy --print` completed in a non-TTY subprocess with stdout, stderr, and `--log-file` redirected separately.
- The 1.1.4 release explicitly changed headless runs to honor persisted `settings.json` policies; future upgrade reviews must compare both CLI help and release notes rather than replacing only the version string.

On 2026-07-21, a Gemini 3.6 Flash High smoke test completed on macOS arm64 with AGY 1.1.5:

- `agy models` listed `gemini-3.6-flash-low`, `gemini-3.6-flash-medium`, and `gemini-3.6-flash-high`.
- `gemini-3.6-flash-high` read a persisted prompt, wrote only the designated result file in a minimal sandbox workspace, and verified the exact result.
- The command exited successfully, stderr was empty, and the event log resolved the model as `Gemini 3.6 Flash (High)`.

## Official Sources

- https://github.com/google-antigravity/antigravity-cli
- https://antigravity.google/product/antigravity-cli
- https://antigravity.google/docs/cli-overview
