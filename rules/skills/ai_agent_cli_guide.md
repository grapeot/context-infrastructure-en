# AI CLI Agent Practical Guide

## Metadata
- Type: API Guide
- Use when: building automation pipelines with CLI Agents, AI-calling-AI
- Last updated: 2026-07-21

---

## When to Use a CLI Agent Instead of Raw API

Direct LLM API calls have shortcomings for complex tasks. CLI Agents as an intermediate layer provide these core advantages:

1. **Countering "model laziness"**: Raw APIs tend to truncate output on large tasks; agents natively have loop execution and self-correction capabilities
2. **Native file context**: Agents automatically handle file reading, encoding, and writing, decoupling reasoning from I/O
3. **Inherited toolchain**: Built-in MCP plugins allow calling Tavily search, executing scripts, etc. on demand
4. **Optimized context management**: Automatic handling of context window consumption and long-conversation compression

---

## Tool Quick Reference

| Dimension | Claude Code | Codex CLI | OpenCode | Antigravity CLI |
|------|-------------|-----------|----------|-----------------|
| **Open source** | No | No | Yes, 100% | No |
| **Model lock-in** | Claude only | OpenAI only | Provider-agnostic (xAI, Anthropic, OpenAI, Google, etc.) | Models included with an Antigravity subscription |
| **CLI non-interactive** | `claude --print` | `codex exec` | `opencode serve` + `opencode run --attach` (two-step) | `agy --print` |
| **Web API** | No | No | Yes, full | No |
| **Recommended use** | Deep reasoning | Automation | Multi-model comparison, automation + visualization | Gemini agent work through subscription quota |

---

## File Response Pattern (Core Design Principle)

**Principle**: In production, all input and output go through files. Never use pipe mode for core logic.

**Why**:
- **Determinism**: When AI "edits a file", its mental model is "complete the work and save", making truncation less likely
- **Auditability**: File system changes before and after a task (git diff) are the single source of truth
- **High capacity**: Bypasses command-line argument length limits

**Implementation points**:
- **Input**: Prompts must first be written to a local file, then read by the program
- **Output**: CLI output must be written to a local file, then read and parsed by the program
- **JSON output**: Explicitly require "output only JSON" in the prompt

**Python example**:
```python
import subprocess
from pathlib import Path

# 1. Write prompt to file
Path("prompt.txt").write_text("Your task here...")

# 2. Construct driver prompt
driver_prompt = (
    f"Read the full prompt from {Path('prompt.txt').resolve()}\n"
    f"Write ONLY a JSON object to {Path('output.json').resolve()}\n"
    "Do not include Markdown or extra text."
)

# 3. Execute (Claude Code example)
subprocess.run([
    "claude", "--print", "--output-format", "json",
    "--model", "claude-opus-4-6",
    driver_prompt.replace('\0', '')  # Strip null bytes
])
```

---

## Claude Code Quick Reference

**Basic command**: `claude --print "prompt"`

**Key parameters**:

- `--model`: `claude-sonnet-4-6-20260217` for routine work or `claude-opus-4-6-20260205` for deep reasoning
- `--output-format`: `text`, `json`, or `stream-json`
- `--permission-mode`: `acceptEdits` or `bypassPermissions`
- `--json-schema`: require output conforming to a JSON Schema

Sonnet 4.6 is the default cost-effective choice; use Opus 4.6 when the task needs deeper reasoning.

---

## Antigravity CLI Quick Reference

Use the standalone `agy` command for Antigravity automation, not `agy-ide chat`. See [Antigravity CLI File-Based Invocation](./antigravity_cli.md) for installation, authentication, privacy boundaries, and the complete execution contract.

Core rules: persist the prompt, result, stdout, stderr, and event log as separate local-only files under a git-ignored `tmp/`; use `Gemini 3.5 Flash (High)` by default; pair `--dangerously-skip-permissions` with `--sandbox` only in a minimal trusted scratch workspace; set `--print-timeout 10m` and an outer process timeout of about 610 seconds.

AGY 1.1.4 uses the top-level `agy --print` headless interface and has no `agy run`, `login`, or JSON event stream. It reuses the Google sign-in from the Antigravity App or IDE through the system keyring. Version 1.1.4 also makes headless runs honor persisted `settings.json` policies, which must be reviewed before execution. A successful run requires exit code 0, a non-empty result file, satisfied hard constraints, and no unhandled stderr error.

Use a fresh AGY conversation for every independent writing or review stage. Do not pass `--continue` or `--conversation` between IC-1, IC-2, and IC-3.

---

## Codex CLI Quick Reference

> Verified against Codex CLI 0.144.x (2026-07-21). The 0.1.x series changed a lot: the old `--full-auto` is gone, sandbox/approval are now separate parameters, and structured-output plus last-message-to-file capabilities were added.

**Basic command**: `codex exec [options] "prompt"` (`exec` can be shortened to `e`). The prompt can also be read from stdin via `-`; when both stdin and a positional prompt are given, stdin is appended as a `<stdin>` block.

**Core parameters**:
- `-m, --model`: Select the model. The current generation is the GPT-5.x Codex family; no longer `gpt-5.2` as in old docs.
- `-c model_reasoning_effort=<level>`: `low` (translation / format conversion) / `medium` (regular) / `high` (deep refactoring). This overrides config via `-c`, not a standalone flag.
- `-s, --sandbox <mode>`: `read-only` / `workspace-write` / `danger-full-access`. **Replaces the old `--full-auto`.** Use `workspace-write` to let the agent write files; `read-only` for read-only reasoning.
- `-a, --ask-for-approval <policy>`: `untrusted` / `on-request` / `never`. For automation use `never` so execution failures flow straight back to the model instead of blocking.
- `--skip-git-repo-check`: Run outside a git repo (required in temp directories).
- `--ephemeral`: Don't persist the session to disk (recommended for one-shot calls, avoids rollout file buildup).
- `-C, --cd <dir>`: Set the agent's working root; `--add-dir <dir>` adds writable directories.
- `--color never`: Disable ANSI for easier stdout parsing.

**Automation essentials: structured output and result-to-file**

This is the biggest practical improvement over old versions, replacing the fragile "beg the model to output only JSON in the prompt" approach:

- `-o, --output-last-message <file>`: Write the agent's final message **cleanly** to a file (no event noise). The preferred exit for file-response mode.
- `--output-schema <file>`: Pass a JSON Schema file to force the final response to conform to that schema. Combined with `-o` you get validated JSON directly. Verified working:

```bash
# schema.json: {"type":"object","properties":{"answer":{"type":"integer"}},"required":["answer"],"additionalProperties":false}
codex exec --skip-git-repo-check --sandbox read-only --color never \
  -c model_reasoning_effort=low \
  --output-schema schema.json \
  -o out.json \
  "What is 17 times 3?"
# out.json => {"answer":51}
```

**JSONL event stream (`--json`)**

`--json` emits a JSONL event stream whose schema has been restructured. Current event types:

```
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"final answer here"}}
{"type":"turn.completed","usage":{"input_tokens":...,"output_tokens":...}}
```

The final answer is in the `text` field of the item with `item.type == "agent_message"`; tool calls appear as `command_execution` / `file_change` etc. item types. To monitor progress, parse items one by one. Note the occasional `failed to renew cache TTL` warning on stderr — it doesn't affect results; ignore it when parsing.

**Other new subcommands (automation-relevant)**:
- `codex exec resume <session_id>` or `--last`: Resume a prior session.
- `codex review [--uncommitted | --base <branch>]`: Non-interactive code review (also `codex exec review`).
- `codex sandbox <command...>`: Run arbitrary commands directly inside Codex's seatbelt sandbox.
- `codex doctor`: Diagnose install, auth, and runtime health (first step for CLI issues).

**Recommendation**: Use `low` + `read-only` for simple tasks, `workspace-write` when files must be written, `high` for complex refactoring. For production automation, standardize on `--output-schema` + `-o` to get structured results — more reliable than parsing stdout.

### Codex Built-in imagegen

Codex CLI can currently trigger the built-in `imagegen` capability through natural language. The key is having `codex exec` receive an instruction like `Use imagegen to create an image with this request:`; the prompt can be natural language, not necessarily JSON. JSON's value is mainly in templating and stable reuse, e.g. managing `subject / background / lighting / composition` separately for e-commerce assets.

Minimal working command:

```bash
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --color never - <<< "Use imagegen to create an image with this request:
A single transparent glass lemon sculpture on a clean white studio background. The lemon is made of thick translucent glass with subtle yellow tint, realistic refraction, caustic light patterns on the surface below, soft diffused studio lighting, centered product photography composition, high-end commercial still life, crisp details, no text, no watermark.

Requirements:
- Generate the image directly
- Do not provide explanation
- Return only the image result"
```

With reference images, pass them via `--image` to Codex and explain the reference usage in the prompt:

```bash
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --color never \
  --image /path/to/product.png \
  - <<< "Use imagegen to create an image with this request:
Create a premium e-commerce hero image of the same product as the reference image, clean white studio background, soft diffused lighting, centered product photography composition, no text, no watermark.

Reference image(s) are attached. Use them as visual identity/style references.
Requirements:
- Generate the image directly
- Do not provide explanation
- Return only the image result"
```

Generated results typically land in `~/.codex/generated_images/<session_id>/`. In practice, `codex exec` stdout may only output brief text and not directly print the image path; after calling, check this directory and copy the final image to the current project or user-specified path. This capability uses Codex/ChatGPT subscription quota, not the local `image-generation-skill` repo's Gemini/OpenAI API key path.

---

## OpenCode Quick Reference

OpenCode has two non-interactive invocation methods: CLI (`opencode run`) and Web Server API.

### Method A: CLI (serve + run --attach)

Running `opencode run` alone fails with "Session not found" due to built-in server startup failure. **The correct usage** is to start a headless server first, then attach to it:

```bash
# 1. Start headless server (background daemon, port customizable)
opencode serve --port 14097 &

# 2. Send task (attach to existing server)
opencode run \
  --attach "http://localhost:14097" \
  -m "xai/grok-4.20-experimental-beta-0304-non-reasoning" \
  --dir "/path/to/project" \
  "your prompt"
```

**Key parameters**:
- `--attach`: Connect to a running server (required)
- `-m, --model`: `provider/model` format (e.g. `xai/grok-4.20-experimental-beta-0304-non-reasoning`)
- `--dir`: Specify the agent's working directory (server-side path)
- `--format json`: JSON event stream output (suitable for program parsing)
- `--agent`: Specify agent (default: build)
- `--variant`: Reasoning effort (e.g. `high`, `max`, `minimal`, provider-specific)

**View available models**: `opencode models | grep xai`

**Server management**:
- Server is bound to a working directory. Start from a fixed directory for unified session management
- After startup, the server can handle multiple `run --attach` requests
- Stop: `kill` the process or `Ctrl+C`

### Method B: Web Server API (Python programmatic calls)

Suitable for scenarios requiring fine-grained session lifecycle control.

**Start server**: `opencode web --port 4096` (or `opencode serve --port 4096`)

Use an OpenCode client compatible with the current server API for operations such as `create_session()`, `send_message()`, `get_session_messages()`, and `wait_for_session_complete()`.

**Model format**: `provider/model` (e.g. `xai/grok-4.20-experimental-beta-0304-non-reasoning`, `anthropic/claude-opus-4-6`)

### Method Selection

| Scenario | Recommended Method |
|------|----------|
| One-off task, quick experiment | CLI (serve + run --attach) |
| Batch experiments, programmatic session control | Web Server API |
| AI-calling-AI (file response pattern) | CLI (simpler) or API (more controllable) |

### Common Model Quick Reference

| Provider | Model ID | Characteristics |
|----------|----------|------|
| xai | `grok-4.20-experimental-beta-0304-non-reasoning` | Grok 4.20 non-reasoning, fast |
| xai | `grok-4.20-experimental-beta-0304-reasoning` | Grok 4.20 reasoning edition |
| xai | `grok-4-1-fast-non-reasoning` | Grok 4.1 non-reasoning, $0.20/1M input |
| anthropic | `claude-opus-4-6` | Claude deep reasoning |
| anthropic | `claude-sonnet-4-6` | General Claude work with a lower cost |
| openai | `gpt-5.x` | Current GPT-5.x Codex generation (requires Codex plugin) |

---

## AI-Calling-AI Pattern

If you are writing an Agent to call these CLIs, provide the following meta-instruction:

> "When facing large-scale text processing or filesystem operations, call the underlying CLI Agent:
> 1. Prefer the file response pattern: first save content to a local temporary file
> 2. Use stream mode (`--json`) and parse events in real time to monitor progress
> 3. Set appropriate reasoning intensity (e.g. `low` for translation)
> 4. Strip null characters from the prompt before passing (`.replace('\0', '')`)
> 5. For OpenCode, prefer the Web Server API"

The JSON-stream recommendation does not apply to Antigravity CLI. AGY uses `--log-file` for progress visibility and the designated result file as the only deliverable.

---

## Minimalist Design Philosophy (pi-mono)

Core principle from the pi-mono project: **"What's missing matters more than what's included"**

**Core ideas**:
- **Context Engineering is Paramount**: Context engineering matters more than tool count
- **Full Observability**: Fully observable, no hidden state
- **External State**: Write files rather than maintain internal state
- **Builder's Mindset**: Design for builders, not consumers

**Insight**: In complex tasks, adding features is often a way to avoid the problem. The hard decision is: **what should not be there**.

---

## Model Selection Quick Reference

| Task Type | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| **Translation / format conversion** | Sonnet 4.6 | GPT-5.x Codex + low | glm-5 / grok-4-1-fast-non-reasoning |
| **Regular development** | Sonnet 4.6 | GPT-5.x Codex + medium | glm-5 / grok-4.20-non-reasoning |
| **Deep reasoning / refactoring** | Opus 4.6 | GPT-5.x Codex + high | grok-4.20-reasoning / claude-opus-4-6 |

---

## OpenCode Operational Notes

### Permission Model: Files Must Be Under Project Root

OpenCode agent **cannot access paths outside the project root** (including `/tmp/`). All file I/O (prompt input files, JSON output files) must be placed under the working directory where the server was started.

```python
# Wrong: /tmp will be rejected by the agent
prompt_path = Path("/tmp/opencode_prompt.txt")

# Correct: place in run directory or project-local directory
prompt_path = run_dir / "opencode_prompts" / f"{invocation_id}.txt"
# Or fallback to project root
prompt_path = Path(".opencode_tmp") / f"{invocation_id}.txt"
```

### Reliability: stdout JSON Fallback

Even when the prompt explicitly requires "write to file", the agent sometimes outputs JSON directly to stdout without writing the file (or writes an empty file). **Production must implement stdout JSON extraction as fallback**:

```python
import re

def _extract_json_from_text(text: str) -> dict | None:
    """Extract JSON object from stdout (fallback)"""
    # Prefer ```json code blocks
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # Fallback: find the largest {...} block
    candidates = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text)
    for c in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    return None
```

### Concurrency

One `opencode serve` process can handle multiple concurrent `run --attach` requests. Each request creates an independent session. In practice, 2 concurrent requests are stable; higher concurrency depends on the LLM provider's rate limit.

### Parameters Not Supported by Grok 4.20

`xai/grok-4.20-experimental-beta-0304-non-reasoning` does not support `presence_penalty`, `frequency_penalty`, or `stop` parameters. If OpenCode forwards these parameters, the API will error.

### Typical Call Flow (File Response Pattern)

```
1. Write prompt → run_dir/opencode_prompts/XXXX.txt
2. Construct driver prompt: "Read from {prompt_path}, write JSON to {response_path}"
3. opencode run --attach http://localhost:14097 -m model "driver_prompt"
4. Read run_dir/opencode_responses/XXXX.json
5. If file is empty → extract JSON from stdout (fallback)
6. If still fails → retry (max 3 times)
```

Start the server from the intended project root, for example with `opencode serve --port 14097`, so the file-access boundary matches the task.

---

## References

- [Claude Code Official Documentation](https://docs.anthropic.com)
- [OpenAI Codex Documentation](https://platform.openai.com/docs)
- [OpenCode Official Documentation](https://opencode.ai/docs)
- [Antigravity CLI Official Documentation](https://antigravity.google/docs/cli-overview)
