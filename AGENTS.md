# AGENTS.md - Your Workspace

> **First time here?** Start with `setup_guide.md` — it'll walk you through setup in under an hour.

This folder is home. Treat it that way.

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` — this is who you are
2. Read `rules/USER.md` — this is who you're helping
3. Read `rules/WORKSPACE.md` — file routing table, check before searching for files
4. Read `rules/COMMUNICATION.md` — how to think and communicate (especially for non-coding tasks)
5. Read `rules/skills/INDEX.md` — understand available skills

## Multi-Agent Nudge

Before invoking sub-agents or an independent review runner, read `rules/skills/workflow_parallel_subagents.md`.

- **Engineering and code implementation**: The main thread implements by default; delegate implementation only when the user explicitly requests it.
- **Code / privacy / design review**: Normally use an independent sub-agent or Antigravity CLI for a fresh context, with main-thread final acceptance. Trivial, low-risk local edits may be excepted proportionally. A single review is exempt from the multi-agent parallel threshold.

- **Broad survey and codebase exploration**: Use multiple sub-agents when the parallel threshold is met; launch co-ready tasks in one message via `multi_tool_use.parallel`, default to `background: true` when supported, and wait for automatic completion without polling.

## File Routing

**When looking for files, check `rules/WORKSPACE.md` first, then search.** WORKSPACE.md is the directory index for this workspace — it records where each type of content lives. In most cases, a quick lookup gets you to the target directory without a full glob/grep. If you discover a new directory or project that isn't listed, update WORKSPACE.md.

## Skills

**Skills** are reusable AI capabilities: workflows, API guides, best practices, and so on.

**Important: when you need to figure out how to do X, check skills first, then system tools.** Search order: (1) quick reference below → (2) `rules/skills/INDEX.md` → (3) system tools.

**Need to run a task** → check `rules/skills/INDEX.md` for the matching skill
**Want to add a new capability** → follow existing skill format, update INDEX.md

### Common Skill Quick Reference (INDEX.md is authoritative)

**Deep research tasks** → `rules/skills/workflow_deep_research_survey.md`
**Background agent / parallel subagent** → `rules/skills/workflow_parallel_subagents.md`

Read the matching skill file after a hit, then execute. INDEX.md is the single routing source; no step details here.

## Axioms

Decision principles distilled from personal experience, used to inspire deeper thinking. For category index, usage guide, and trigger words, see `rules/axioms/INDEX.md`.

## Sub-agent Model Routing

Configuration entry: OpenCode native `opencode.json` `agent` field, or `.opencode/agent(s)/*.md` agent files. `subagent_type` must be a registered agent name, not a model name, and not the old `category`.

Select a capability from the runtime schema only after deciding to delegate under the workflow: `explore` for codebase exploration, `general` for general research, and currently registered agents for specialized review, coding, screening, or privacy needs. Do not maintain fixed model or historical alias lists; routing does not authorize implementation delegation.

Antigravity CLI is an external runner, not a Gemini subagent. For independent review or a selected writing workflow, read the installed `ai-agent-cli` root skill and its Antigravity focused skill, then use the current available model list.

## Opus Work Mode

If your model ID contains `opus`, the following rules apply:

**Implementation and final acceptance stay on the main thread by default.** Opus also implements directly unless the user explicitly requests delegation. Broad research and exploration may be delegated as needed; code / privacy / design review normally uses an independent runner. A selected writing workflow may designate a writer, while the main thread still reads back, verifies, and owns final delivery. Follow `rules/skills/workflow_parallel_subagents.md` for scheduling boundaries.

## Memory System

Three-tier memory architecture:
- **L3 (global constraints)**: All files under `rules/`, passively loaded every session
- **L1/L2 (dynamic memory)**: `contexts/memory/OBSERVATIONS.md`, agent actively retrieves
- **Automatic accumulation**: `periodic_jobs/ai_heartbeat/` daily observer + weekly reflector

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
