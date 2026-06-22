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

This harness can delegate work to multiple sub-agents. You don't need to use them by default, but keep the capability in mind for tasks that are large, parallelizable, research-heavy, or benefit from independent cross-checking.

Before using sub-agents, read `rules/skills/workflow_parallel_subagents.md`. The current OpenCode pattern is `multi_tool_use.parallel` wrapping multiple `functions.task` calls in the same assistant message.

Don't ask permission. Just do it.

## File Routing

**When looking for files, check `rules/WORKSPACE.md` first, then search.** WORKSPACE.md is the directory index for this workspace — it records where each type of content lives. In most cases, a quick lookup gets you to the target directory without a full glob/grep. If you discover a new directory or project that isn't listed, update WORKSPACE.md.

## Skills

**Skills** are reusable AI capabilities: workflows, API guides, best practices, and so on.

**Important: when you need to figure out how to do X, check skills first, then system tools.** Search order: (1) quick reference below → (2) `rules/skills/INDEX.md` → (3) system tools.

**Need to run a task** → check `rules/skills/INDEX.md` for the matching skill
**Want to add a new capability** → follow existing skill format, update INDEX.md

### Common Skill Quick Reference (INDEX.md is authoritative)

**Deep research tasks** → `rules/skills/workflow_deep_research_survey.md`
- Initial scan → split dimensions → multi-agent parallel → cross-validate → write report
- Output: `contexts/survey_sessions/`

**Background agent / parallel subagent** → `rules/skills/workflow_parallel_subagents.md`
- When to split tasks, when not to, how to dispatch multiple subagents in parallel
- Before calling multiple `functions.task`, read this skill first, then execute
- Current parallel method is `multi_tool_use.parallel`; do not use the old `run_in_background` / `background_output` pattern

## Axioms

Decision principles distilled from personal experience, used to inspire deeper thinking. For category index, usage guide, and trigger words, see `rules/axioms/INDEX.md`.

## Sub-agent Model Routing

Configuration entry: OpenCode native `opencode.json` `agent` field, or `.opencode/agent(s)/*.md` agent files. `subagent_type` must be a registered agent name, not a model name, and not the old `category`.

Common routing quick reference:
- **Codebase exploration** → `subagent_type="explore"`
- **General parallel tasks** → `subagent_type="general"`
- **High-reliability reasoning / engineering judgment** → `subagent_type="reasoning_gpt"`
- **Chinese writing / editing** → `subagent_type="writer_deepseek"`
- **Low-cost initial screening / lightweight organization** → `subagent_type="cheap_glm"`
- **Local privacy-sensitive tasks** → `subagent_type="private_ds4"`
- **Ollama Cloud zero-data-retention low-cost tasks** → `subagent_type="ollama_kimi"`
- **Ollama Cloud zero-data-retention high-quality tasks** → `subagent_type="ollama_deepseek_pro"`

For creative work (brainstorming, article structure, viewpoint collision), dispatch one subagent with a different approach in parallel by default for a counter-perspective or supplementary view. Do not use the old `category="artistry"` / `category="deep"` / `category="ultrabrain"` pattern unless the current OpenCode config has explicitly registered these agent names.

## Opus Work Mode

If your model ID contains `opus`, the following rules apply:

**Your context window is precious.** Opus's core strengths are design, quality control, and writing. Delegate research, scripting, and keyword search to sub-agents. Your two main tasks: (1) **Design**: break down problems, design plans, assign sub-agent tasks; (2) **Writing and quality control**: write the final text yourself, verify sub-agent results yourself. Delegate all coding, research, and data processing. Never outsource writing and quality verification. When designing task splits, default to considering parallelism. For execution details, follow `rules/skills/workflow_parallel_subagents.md`.

## Memory System

Three-tier memory architecture:
- **L3 (global constraints)**: All files under `rules/`, passively loaded every session
- **L1/L2 (dynamic memory)**: `contexts/memory/OBSERVATIONS.md`, agent actively retrieves
- **Automatic accumulation**: `periodic_jobs/ai_heartbeat/` daily observer + weekly reflector

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
