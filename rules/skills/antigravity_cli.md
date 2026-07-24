# Antigravity CLI File-Based Invocation

## Metadata

- Type: API Guide
- Use when: using Antigravity subscription quota to run a Gemini agent as a replacement for a Gemini API sub-agent; automated writing, rewriting, review, or file processing
- Command: `agy`
- Verified version: 1.1.5 (2026-07-21)

## Core Distinction

`agy-ide` is an IDE launcher. Its `chat` subcommand sends a prompt to the graphical interface; it is not a headless agent CLI.

Automation must use the separate Antigravity CLI, `agy`. The official installer lives at `https://antigravity.google/cli/install.sh`; follow the initialization flow below to download and review it before executing.

`agy` uses the Antigravity subscription and system keyring for login; it does not read `GEMINI_API_KEY`. The local CLI can reuse the Google login credentials already present in the Antigravity App or IDE.

## First Install and Initialization

Check whether the command exists before the first use on each machine; do not assume it is installed:

```bash
if ! command -v agy >/dev/null 2>&1; then
  installer="$(mktemp)"
  curl -fsSL https://antigravity.google/cli/install.sh -o "$installer"
  less "$installer"  # Review the downloaded script before executing it.
  bash "$installer"
  rm -f "$installer"
fi
```

The installer URL changes as the official releases evolve. The download-then-manually-review path above is appropriate only for a trusted personal workstation. On a managed or security-sensitive machine, download a pinned version asset from the [official GitHub release](https://github.com/google-antigravity/antigravity-cli/releases) and verify it against the SHA-256 digest published in that release's GitHub asset metadata before extracting or executing it. If the organization cannot approve the release and digest, do not install.

The installer normally places the binary at `~/.local/bin/agy`. If the current shell still cannot find the command, run the installer's own environment setup and then open a new shell:

```bash
~/.local/bin/agy install
```

Then complete the initialization checks:

```bash
agy --version
agy --help
agy models
```

`agy` 1.1.5 has no standalone `login` subcommand. `agy models` or the first `agy --print` attempts to retrieve Antigravity credentials silently from the system keyring. If the machine is not yet authenticated, sign in with Google through the Antigravity App or IDE first, then retry `agy models`. Do not fall back to `GEMINI_API_KEY`, because that reverts to the API billing route and is no longer the subscription channel this skill validates.

Initialization is complete only when all three checks pass: `command -v agy` returns a valid path, `agy --version` exits normally, and `agy models` lists models. Only after all three pass should you run production file-based tasks.

## File-Based Invocation Contract

Every production invocation uses three input/output layers:

1. **Task file**: write the complete prompt to `tmp/<session>/agy_<task>_prompt.md` inside the workspace.
2. **Result file**: the prompt requires the agent to write the complete deliverable to an explicit path such as `tmp/<session>/agy_<task>_result.md`.
3. **Run records**: save CLI stdout, stderr, and `--log-file` separately. Stdout is only the agent's completion note; it cannot replace the result file.

Prompts, results, and run records may contain task text, file paths, account metadata, or model events. They must live in a git-ignored `tmp/`, be used only for local audit, and never be committed, uploaded, or shared publicly. The repository should ignore at least `tmp/`, `*.log`, `.env`, and `.env.*`, and only allow a sanitized `.env.example` when needed.

Do not place a long prompt directly on the command line. Pass only a single driver prompt: read the task file and follow it exactly.

Task files, reference material, and output files should all live in the launch directory or its descendants. Launch from a minimal trusted scratch workspace that contains only the inputs required for this task. Do not launch from a home directory, a broad monorepo root full of private material, or a directory containing `.env` files, credentials, or customer data.

`--sandbox` limits tool behavior, but it does not guarantee that every file in the workspace stays out of remote model context. Before a production invocation, inspect the scratch workspace and remove or move out any secrets or private material unrelated to the task.

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

`--print` / `-p` is a top-level flag, not a subcommand. AGY 1.1.5 has no `agy run` and no `--trust`, `--format`, or `--output-events` flags. Do not copy another agent CLI's command shape; `agy run ...` enters the wrong interactive path and may fail with a Bubble Tea `/dev/tty` error or hang in a non-TTY subprocess. Events and diagnostics are written to `--log-file` only.

AGY 1.1.5 continues the headless `--print` support for persisted `settings.json` policies. Persisted settings for permissions, file access, sandbox mode, auto-execution, and artifact review all affect non-interactive runs. Before a production invocation, inspect both global and project-level AGY settings in addition to the command-line flags; do not assume `--print` is a clean execution environment isolated from persisted configuration.

The caller should also set an outer process timeout of about 610 seconds. `--print-timeout 10m` is AGY's internal wait limit; the extra ~10 seconds allows process shutdown and log flushing.

Use `--dangerously-skip-permissions` only together with `--sandbox`, and only in the minimal trusted scratch workspace described above. It exists to keep non-interactive mode from stalling on file-write confirmations; it does not authorize the agent to widen the task scope. The task file must name a single output path and state "do not modify any other file."

## Models and Capability Checks

Check on every first use or after an upgrade:

```bash
agy --version
agy --help
agy models
```

Models verified available with AGY 1.1.5 on 2026-07-21 include:

- `gemini-3.6-flash-low` (Gemini 3.6 Flash Low)
- `gemini-3.6-flash-medium` (Gemini 3.6 Flash Medium)
- `gemini-3.6-flash-high` (Gemini 3.6 Flash High)
- `gemini-3.5-flash-low`, `gemini-3.5-flash-medium`, `gemini-3.5-flash-high`
- `gemini-3.1-pro-low`, `gemini-3.1-pro-high`

The writing workflow defaults to `gemini-3.6-flash-high`. Only switch explicitly to `gemini-3.1-pro-high` when stronger reasoning is required and the subscription quota allows it. Do not rely on the persisted setting from an interactive `/model`; production invocations always pass `--model`.

AGY 1.1.5 print mode returns a non-zero exit code and lists available models when the model name is invalid. Do not silently fall back.

## Progress and Stall Judgment

AGY 1.1.5 has no `--json` or `--output-format stream-json`. Do not invent a JSON mode, and do not wrap plain stdout into a pseudo event stream.

Current observability comes from `--log-file`. Every log line carries its own timestamp, and you can see:

- `Print mode: starting`
- `silent auth succeeded`
- `streamGenerateContent` and `ResponseID`
- `Auto-approving tool confirmation`
- `CLI store manager shutting down`
- `Language server shutting down`

For a foreground synchronous invocation, wait for the process to exit before reading the result file. For a background invocation, poll the event log's last-modified time and the events above to judge whether the model is still active.

The log startup phase may first show `You are not logged into Antigravity` and then complete `silent auth succeeded` through the keyring. As long as the process finally exits successfully and the result file is complete, do not misread these pre-authentication logs as a failure.

The completion conditions must all be satisfied:

1. The process exit code is 0.
2. The designated result file exists and is non-empty.
3. The result file contains the structure and hard constraints (URLs, numbers, etc.) the task requires.
4. Stdout has a completion note; stderr has no unhandled error.

If the process times out or the result file is missing or empty, the task failed. Do not fall back to treating a stdout summary as the deliverable.

## Writing Task Template

The External-writing Writer does not read the complete workflow, `COMMUNICATION.md`, or `bestpractice_external_prose.md`. The Main Agent first compresses this article's requirements into a task packet, then lets AGY handle complete drafting only.

A Round 2 candidate task file includes at least:

```markdown
# Task

Read these files completely:
1. `/absolute/path/to/source_contract.md`
2. `/absolute/path/to/writing_brief.md`
3. `/absolute/path/to/voice_contract.md`
4. `/absolute/path/to/content_map.md`
5. `/absolute/path/to/audience_contract.md`

Write the complete result to:
`/absolute/path/to/result.md`

Do not modify any other file.

## Task

- Write one complete external-facing Chinese article from a blank page.
- Use only facts, scenes, causal claims, and boundaries present in `source_contract.md` and `content_map.md`.
- Treat `source_contract.md` as a fact boundary, not a coverage checklist. Respect the reader baseline and concept budget in `audience_contract.md`.
- Preserve the thesis, claim strength, numbers, URLs, image references, and immutable terms.
- Follow `voice_contract.md`; do not output an audit, explanation, invariant count, or PASS statement.
- Decide the article's own H2 wording and paragraph entrances. Do not copy content-map block labels or turn research taxonomies into the article outline.
- Use normal Chinese paragraphs. Do not put every sentence on its own line.
```

`source_contract.md` should provide an immutable-term list covering product names, model names, terms that are easily mistranslated, and labels that must be preserved verbatim. In practice, AGY will proactively translate terms such as `Oracle`, `reset card`, or `system of record`; without this list, factual wording can drift.

## Fresh Context, Parallel Candidates, and One Retry

Each `agy --print` call without `--continue` or `--conversation` creates a fresh conversation. External writing uses two categories of AGY calls:

- **Round 2 double generation**: By default, use two fresh conversations to generate `candidate_a.md` and `candidate_b.md` separately from the same task packet. When multiple model families are available at runtime, default to generating one draft each with `gemini-3.6-flash-high` and `claude-sonnet-4-6`; they do not read one another and do not serially rewrite. The two calls can run in parallel. The value of double generation is **sampling diversity** — sampling across model families is one of the few levers that genuinely affects "warmth/approachability."
- **Single review to pick the winner**: Do not run full acceptance on both. First do a cheap blind read on each (posture only) to pick the one closer to the target voice, and run the complete Round 3 acceptance on the **winner** only.
- **Round 3 blind reader**: Must use a model family different from the candidate under review. A Gemini candidate goes to Claude, a Claude candidate goes to Gemini; the conversation is still fresh, and it reads only the candidate body.
- **Round 4 optional revision**: Start one fresh conversation only when the Round 3 cold-read acceptance returns `RETRY_PROSE`. It reads the selected candidate, the four contracts, and a `revision_delta.md` of no more than three to five items, then outputs one complete revision. After it finishes, all Round 3 live gates must be rerun.
- **Terminal cold read (the only global gate)**: After the canonical file is finalized, use a fresh conversation with a model family different from the Writer's to **read only the final file body** — no contracts, candidates, or prior verdicts. It must end with a machine-parseable `TERMINAL_VERDICT: SHIP` or `TERMINAL_VERDICT: BLOCK`. The Main Agent greps out this line with a command and pastes the captured output; only a captured `SHIP` permits claiming completion.

The AGY Writer does not write QA and is not the PASS authority. The Main Agent must read the candidate body directly, use deterministic tools to verify numbers, URLs, images, and structure, and then judge facts and voice against the source contract. Round 4 happens at most once; if a non-surgical blocker remains, return to the Main Agent's upstream artifacts or report to the user, and do not automatically start more AGY conversations.

The Round 3 acceptance verdict is written to `acceptance_audit.md` and can only be `ACCEPT`, `RETRY_PROSE`, or `RETURN_TO_ROUND_1`. The Writer's stdout only proves that the process finished; it does not participate in selection or the PASS decision.

All local reviewers, revision re-checks, and image QA must declare their scope at the top of the result and may only output `LOCAL_PASS(scope=[...])`, `LOCAL_BLOCK(scope=[...])`, or observation notes. Automation **must not** merge multiple `LOCAL_PASS` results into an `ACCEPT`; the global `SHIP` verdict belongs to the terminal cold read alone, and a script greps to block the word "done" rather than the Main Agent overriding it by feel. **Deterministic scans (numbers / URLs / parenthetical-annotation regex / evaluation-label regex) must actually run the command and paste the captured output; reporting "scanned, looks fine" in natural language is defined as a gate failure.**

The Round 4 task file must additionally read the selected candidate and `revision_delta.md`. `revision_delta.md` lists only the three to five highest-impact blockers, their location in the text, and the correct direction; it must not re-attach the entire workflow or prose taxonomy. Round 4 outputs a complete revision, not QA.

After acceptance passes, the Main Agent may perform logged surgical completion, including typos, punctuation, Markdown, proper nouns, and local single-sentence corrections uniquely determined by the source contract. Record every change in `completion_edits.md`; this must not be used to reorder structure or rewrite whole paragraphs.

Give every round separate prompt, result, stdout, stderr, and events files. Filenames should include the phase, for example:

- `agy_candidate_a_prompt.md` / `agy_candidate_a_events.log`
- `agy_candidate_b_prompt.md` / `agy_candidate_b_events.log`
- `agy_revision_prompt.md` / `agy_revision_events.log`

## Known Limitations

- No JSON / streaming JSON output.
- Stdout provides only the final text or a summary when the task ends, and is unsuitable as the primary artifact.
- The log is an implementation detail suited to judging liveness; it should not be parsed as a stable API for business results.
- `agy-ide chat` is not a fallback for this skill. It opens or reuses a GUI window and cannot provide an auditable headless completion contract.
- AGY invokes agent tools and may be slower than a single Gemini API request. Use the default 10-minute timeout and do not retry indefinitely just to satisfy a nominal model route.

## Validation Records

On 2026-07-14, a smoke test was completed on macOS arm64 with AGY 1.1.2:

- Reading the task from a persisted prompt file succeeded.
- Writing the designated result file inside the sandbox succeeded.
- Stdout redirection succeeded; stderr was empty.
- The event log contained timestamped auth, model request, file tool, and shutdown records.
- Using `Gemini 3.5 Flash (High)`, a ~2,000-word Chinese memo rewrite completed while preserving all 17 URLs.
- The first rewrite exposed technical-term mistranslation, line-by-line wrapping, and first-person drift; these improved markedly after adding an immutable-term list and a normal-paragraph constraint.
- A fresh AGY conversation also completed an independent prose-QA experiment at the time, successfully preserving the Top 5 ordering, four-paragraph structure, two deep-dive candidates, and all 17 URLs. Later writing runs showed that a Writer self-reviewing within the same completion cannot reliably decide PASS; the current workflow therefore keeps acceptance as a Main Agent cold read plus at most one fresh AGY retry. A single AGY rewrite still cannot be treated as an inspection-free final draft.

On 2026-07-20, the CLI interface and headless path were rechecked on macOS arm64 with AGY 1.1.4:

- The official GitHub latest release and local `agy --version` both reported 1.1.4.
- `agy --help` confirmed that the headless entry point remains the top-level `--print` / `-p`, with no `run` subcommand or JSON event flags.
- `agy --print` completed in a non-TTY subprocess with stdout, stderr, and `--log-file` redirected separately.
- The 1.1.4 release explicitly fixed headless runs to inherit persisted `settings.json` policies; future upgrade reviews must check both CLI help and release notes rather than replacing only the version string.

On 2026-07-21, a Gemini 3.6 Flash High smoke test completed on macOS arm64 with AGY 1.1.5:

- `agy models` listed `gemini-3.6-flash-low`, `gemini-3.6-flash-medium`, and `gemini-3.6-flash-high`.
- `gemini-3.6-flash-high` read a persisted prompt in a minimal sandbox workspace, wrote the designated result file, and read it back for verification.
- The process exited successfully, the result content was exact, and stderr was empty; the event log confirmed the model resolved as `Gemini 3.6 Flash (High)`.

## Official Sources

- https://github.com/google-antigravity/antigravity-cli
- https://antigravity.google/product/antigravity-cli
- https://antigravity.google/docs/cli-overview
