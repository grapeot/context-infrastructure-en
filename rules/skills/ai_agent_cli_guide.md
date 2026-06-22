# AI CLI Agent Practical Guide

## Metadata
- Type: API Guide
- Use when: building automation pipelines with CLI Agents, AI-calling-AI
- Last updated: 2026-04-29

---

## When to Use a CLI Agent Instead of Raw API

Direct LLM API calls have shortcomings for complex tasks. CLI Agents as an intermediate layer provide these core advantages:

1. **Countering "model laziness"**: Raw APIs tend to truncate output on large tasks; agents natively have loop execution and self-correction capabilities
2. **Native file context**: Agents automatically handle file reading, encoding, and writing, decoupling reasoning from I/O
3. **Inherited toolchain**: Built-in MCP plugins allow calling Tavily search, executing scripts, etc. on demand
4. **Optimized context management**: Automatic handling of context window consumption and long-conversation compression

---

## Tool Quick Reference

| Dimension | Claude Code | Codex CLI | OpenCode |
|------|-------------|-----------|----------|
| **Open source** | No | No | Yes, 100% |
| **Model lock-in** | Claude only | OpenAI only | Provider-agnostic (xAI, Anthropic, OpenAI, Google, etc.) |
| **CLI non-interactive** | `claude --print` | `codex exec` | `opencode serve` + `opencode run --attach` (two-step) |
| **Web API** | No | No | Yes, full |
| **Recommended use** | Deep reasoning | Automation | Multi-model comparison, automation + visualization |

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

Claude Code content has been split into a separate skill: [`claude_code.md`](./claude_code.md).

This overview page only retains cross-tool common content. For the following topics, jump directly to `claude_code.md`:

- Using the `claude` CLI, not the Claude routing subagent
- Default to Opus
- Wrap Claude Code with a background subagent to stay non-blocking, but don't pre-do research for it
- Launch from workspace root
- `claude -p` non-interactive invocation, permissions, and tool control
- Temporary context files and Python wrapper notes

---

## Codex CLI Quick Reference

**Basic command**: `codex exec [options] "prompt"`

**Key parameters**:
- `-m, --model`: `gpt-5.2` (recommended)
- `-c model_reasoning_effort`: `low` (translation) / `medium` (regular) / `high` (deep refactoring)
- `--full-auto`: Auto-accept all operations
- `--json`: JSON output format

**Recommendation**: Use `low` for simple tasks, `high` for complex tasks

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

**Python client**: `periodic_jobs/ai_heartbeat/src/v0/opencode_client.py` has implemented common API wrappers
- `create_session()` / `send_message()` / `get_session_messages()` / `wait_for_session_complete()`

**Model format**: `provider/model` (e.g. `xai/grok-4.20-experimental-beta-0304-non-reasoning`, `anthropic/claude-opus-4-6`)

### Method Selection

| Scenario | Recommended Method |
|------|----------|
| One-off task, quick experiment | CLI (serve + run --attach) |
| Batch experiments, programmatic session control | Web Server API |
| AI-calling-AI (file response pattern) | CLI (simpler) or API (more controllable) |

### Common Model Quick Reference

Claude Code default model selection rule: **Always use Opus 4.6.** No longer distinguish trivial vs. non-trivial, and no proactive downgrade to Sonnet. For any Claude Code invocation, default to explicitly specifying Opus.

| Provider | Model ID | Characteristics |
|----------|----------|------|
| xai | `grok-4.20-experimental-beta-0304-non-reasoning` | Grok 4.20 non-reasoning, fast |
| xai | `grok-4.20-experimental-beta-0304-reasoning` | Grok 4.20 reasoning edition |
| xai | `grok-4-1-fast-non-reasoning` | Grok 4.1 non-reasoning, $0.20/1M input |
| anthropic | `claude-opus-4-6` | Claude Code default and sole first choice; suitable for research, comprehensive analysis, multi-step tasks, and high-quality output |
| openai | `gpt-5.4` | GPT-5.4 (requires Codex plugin) |

---

## AI-Calling-AI Pattern

If you are writing an Agent to call these CLIs, provide the following meta-instruction:

> "When facing large-scale text processing or filesystem operations, call the underlying CLI Agent:
> 1. Prefer the file response pattern: first save content to a local temporary file
> 2. Use stream mode (`--json`) and parse events in real time to monitor progress
> 3. Set appropriate reasoning intensity (e.g. `low` for translation)
> 4. Strip null characters from the prompt before passing (`.replace('\0', '')`)
> 5. For OpenCode, prefer the Web Server API"

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

Default strategy: **Claude Code always uses Opus 4.6.** No Sonnet fallback, no downgrade based on triviality judgment.

| Task Type | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| **Translation / format conversion (clearly trivial)** | Opus 4.6 | gpt-5.2 + low | glm-5 / grok-4-1-fast-non-reasoning |
| **Regular development** | Opus 4.6 | gpt-5.2 + medium | glm-5 / grok-4.20-non-reasoning |
| **Deep reasoning / refactoring** | Opus 4.6 | gpt-5.2 + high | grok-4.20-reasoning / claude-opus-4-6 |

---

## OpenCode Production Experience (agentic_trading experiment summary)

The following comes from practical experience running V9.4 backtest experiments with OpenCode + Grok 4.20 in the agentic_trading project.

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

### Key Data

- Smoke test: 7/7 success (zero retries), ~3 minutes wall clock (6 × 30-minute intervals)
- Average per-decision time: ~20-30 seconds (Grok 4.20 non-reasoning)
- Server start command: `opencode serve --port 14097` (started from agentic_trading directory)

---

## References

- [Claude Code Official Documentation](https://docs.anthropic.com)
- [OpenAI Codex Documentation](https://platform.openai.com/docs)
- [OpenCode Official Documentation](https://opencode.ai/docs)
