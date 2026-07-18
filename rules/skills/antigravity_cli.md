# Antigravity CLI File-Based Invocation

## Metadata

- Type: API Guide
- Use when: using Antigravity subscription quota to run a Gemini agent for writing, rewriting, review, or file processing
- Command: `agy`
- Verified version: 1.1.2 (2026-07-14)

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

`agy` 1.1.2 has no standalone `login` command. `agy models` or the first `agy --print` attempts to retrieve Antigravity credentials silently from the system keyring. If the machine is not authenticated, sign in with Google through the Antigravity App or IDE, then retry `agy models`.

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

Use `Gemini 3.5 Flash (High)` by default for writing and prose QA:

```bash
agy --print \
  "Read the complete task from /absolute/path/to/agy_task_prompt.md and follow it exactly." \
  --model "Gemini 3.5 Flash (High)" \
  --mode accept-edits \
  --sandbox \
  --dangerously-skip-permissions \
  --print-timeout 10m \
  --log-file "/absolute/path/to/agy_task_events.log" \
  > "/absolute/path/to/agy_task_stdout.txt" \
  2> "/absolute/path/to/agy_task_stderr.txt"
```

Set the outer process timeout to about 610 seconds. `--print-timeout 10m` is AGY's internal wait limit; the extra time allows process shutdown and log flushing.

Use `--dangerously-skip-permissions` only together with `--sandbox`, and only in the minimal trusted scratch workspace described above. The task file must name one output path or enumerate a bounded set of output paths, then prohibit modification of every file outside that list.

## Models and Observability

After first installation or an upgrade, run `agy --version`, `agy --help`, and `agy models`. Verified models include:

- `Gemini 3.5 Flash (Low)`
- `Gemini 3.5 Flash (Medium)`
- `Gemini 3.5 Flash (High)`
- `Gemini 3.1 Pro (Low)`
- `Gemini 3.1 Pro (High)`

Always pass `--model` explicitly. Do not rely on an interactive `/model` setting. Treat an invalid model name as a failure; do not silently fall back.

AGY 1.1.2 has no `--json` or streaming JSON output. Use `--log-file` for observability. Events such as `Print mode: starting`, `silent auth succeeded`, `streamGenerateContent`, tool confirmation, and shutdown help establish liveness. Startup logs may report an unauthenticated state before keyring-based silent authentication succeeds; judge the run by its final exit status and result file.

A run is complete only when all checks pass:

1. The process exits with code 0.
2. Every designated result file exists and is non-empty.
3. The results satisfy hard constraints for structure, numbers, URLs, and other task requirements.
4. Stdout contains a completion note and stderr contains no unhandled error.

A timeout or any missing or empty result file is a failed run. Never substitute a stdout summary for the requested artifacts.

## Writing Task Requirements

The task file must identify the brief, draft, and prose rules that AGY must read in full; one result path or an enumerated bounded set of result paths; the prohibition on editing files outside that list; and every thesis, fact, number, URL, image, H2 order, or term that must remain unchanged.

Include an immutable-term list for product names, model names, API names, code identifiers, easily mistranslated terms, and labels that must be preserved verbatim. Use normal paragraphs in prose output. Short sentences are a tendency, not a reason to put every sentence on a separate line.

A minimal task file template:

```markdown
# Task

Read these files completely:
1. `/absolute/path/to/writing_brief.md`
2. `/absolute/path/to/source_draft.md`
3. `/absolute/path/to/COMMUNICATION.md`
4. `/absolute/path/to/bestpractice_external_prose.md`

Write the complete result to:
`/absolute/path/to/result.md`

Do not modify any other file.

## Hard invariants

- Preserve the thesis, facts, numbers, URLs, image references, and H2 order.
- Preserve product names and project-specific terms exactly as listed below.
- Do not translate identifiers such as model names, API names, or code symbols.
- Use normal paragraphs. Do not put every sentence on its own line.
- Short sentences are a tendency, not a reason to create telegraph prose.
- Read the output once after writing and verify every invariant.
```

The writing brief should provide an "immutable term list" of product names, model names, easily mistranslated terms, and labels that must be preserved verbatim. In practice AGY will proactively translate terms such as `Oracle`, `reset card`, `system of record`; without a term list, factual wording can drift.

## Fresh AGY Conversations

Each `agy --print` call without `--continue` or `--conversation` creates a fresh AGY conversation. Run IC-1, IC-2, and IC-3 as separate calls. Store every prompt, draft, calibration artifact, review report, and runtime log under the gitignored `tmp/<session_slug>/` directory:

- IC-1 reads only the brief and writes the structural draft.
- IC-2 reads the brief, structural draft, and same-channel prose calibration, then performs a complete rewrite from a blank page. The prompt must state that only the structural draft's claims, evidence, URLs, numbers, and H2 order are inherited; original sentences and paragraph entries are not. Rewrite per the brief's voice route. The goal is "a person who understands the technology naturally introduces their discovery to a smart friend," while avoiding both textbook voice and performative colloquialism.
- IC-3 reads the brief, IC-2 deliverable, calibration material, prose rules (with the positive sample and both negative extremes), then first judges the whole-article voice. If the opening, multiple H2 entries, and the ending still read like a lecture, the whole prose must be rewritten, not just word-swapped. Then check whether familiarity was added by introducing metaphors, slang, absolute conclusions, or new facts not in the source pack. Output `article_qa.md` and `prose_qa.md` candidates; do not treat your own prose as the final draft.
- The main thread then performs the Manager Voice Pass per `workflow_external_writing.md`: reads `article_qa.md`, writes `article_final.md`, and writes `voice_audit.md` (and `translationese_audit.md` with real before/after pairs). This pass is not an AGY conversation; the final prose responsibility stays with the main thread.

Give every stage separate prompt, result, stdout, stderr, and events files. File names should include the stage, for example:

- `agy_ic1_prompt.md` / `agy_ic1_events.log`
- `agy_ic2_prompt.md` / `agy_ic2_events.log`
- `agy_ic3_prompt.md` / `agy_ic3_events.log`

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
- A fresh AGY conversation ran an independent prose QA, preserving the Top 5 ordering, four-paragraph structure, two deep-dive candidates, and all 17 URLs, while correcting exaggerated wording and term drift. Therefore external-facing deliverables still default to keeping an independent IC-3; a single AGY rewrite cannot be treated as a ready-to-ship draft.

## Official Sources

- https://github.com/google-antigravity/antigravity-cli
- https://antigravity.google/product/antigravity-cli
- https://antigravity.google/docs/cli-overview
