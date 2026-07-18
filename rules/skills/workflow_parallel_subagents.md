# Parallel Subagent Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Using `multi_tool_use.parallel` to execute multiple `functions.task` subagents in parallel
- **Created**: 2026-02-20
- **Last Updated**: 2026-06-08

---

## Core Judgment

The primary value of subagents is not simulating a human team, nor wrapping an ordinary task in more complexity. It solves three specific problems:

1. **Context window isolation**: Let different agents each hold a manageable context, avoiding the main thread simultaneously ingesting large volumes of files, web pages, logs, and intermediate judgments.
2. **Parallel reading and independent exploration**: Let multiple agents simultaneously search, read, locate, and verify, reducing single-path dependency.
3. **Cross-validation**: Let different agents independently reach conclusions within intentionally overlapping scopes, using agreement and divergence to expose omissions, misreadings, and assumption conflicts.

External experience points to the same conclusion: multi-agent is more viable for research-heavy, read-heavy, high-value tasks; it is costly and fragile for tasks requiring multiple agents to share large amounts of state, continuously coordinate writes, or mutually correct in real time. Anthropic's multi-agent research system positions it as trading more tokens for stronger parallel exploration and compression capability, explicitly noting that multi-agent may consume approximately 15x the tokens of normal chat; LangChain's experience emphasizes that read-heavy is more suitable for parallelism than write-heavy, because write operations carry implicit decisions and merge conflicts are costly.

Research basis: Anthropic Engineering "How we built our multi-agent research system" (https://www.anthropic.com/engineering/multi-agent-research-system), LangChain "How and when to build multi-agent systems" (https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems), Cemri et al. "Why Do Multi-Agent LLM Systems Fail?" (https://arxiv.org/abs/2503.13657).

## When to Use Parallel Mode

When at least 2 of the following conditions are met, and none of the anti-patterns below are triggered, prefer subagents:

1. **Broad information surface**: Need to check multiple files, multiple web pages, multiple data sources, multiple time periods; reading them all in the main thread would pollute context.
2. **Splittable into independent read tasks**: Can be divided into at least 2 relatively independent exploration directions, each expected to need ≥5 tool calls.
3. **Independent judgment needed**: Need opposing review, fact-checking, competitor comparison, code review, solution comparison; a single path easily self-confirms.
4. **High-value uncertainty exists**: Task results will affect subsequent decisions, public output, code changes, or high-cost actions; spending extra tokens is worthwhile.
5. **Main thread needs to preserve design/integration capability**: The main agent should use its attention for problem decomposition, standard setting, evidence integration, and final judgment, not buried in low-level search or repeated reading.

When not met, execute serially directly; don't parallelize for parallelism's sake.

## Anti-Patterns

In the following cases, default to not using subagents unless the user explicitly requests or the task value justifies the extra cost:

1. **Single-point small task**: Only need to read 1-2 files, run one command, fix one local bug.
2. **Strong sequential dependency**: The next step must depend on the previous step's output; splitting only creates waiting and handoff costs.
3. **Shared state writes**: Multiple agents simultaneously modifying the same set of files, the same table, the same copy; conflicts and implicit decisions are hard to merge.
4. **Context must be fully shared**: Every agent must know the full background to do it right; splitting only loses conditions.
5. **Verification criteria unclear**: No checkable output format, evidence requirements, or acceptance conditions; multiple agents will only produce multiple vague summaries.

## Task Type Reference

| Task Type | Suitability | Recommended Approach |
|-----------|-------------|---------------------|
| External research, paper/product/market survey | High | 3-5 agents, split by evidence function, 30-50% overlap |
| Large codebase understanding, file location, architecture mapping | High | `explore` parallel split by module or problem; main thread integrates |
| Code review, solution review, fact-checking | High | 2-3 agents independent review; retain overlap on the same critical area |
| Brainstorm, opposing viewpoints, thesis stress testing | Medium-High | Different agents assigned different judgment perspectives; output must answer the same set of questions |
| Multi-file implementation | Medium | Only parallel when module boundaries are clear; main thread retains final merge and testing responsibility |
| Single bug fix, local edit, format adjustment | Low | Main thread does directly |
| Multiple agents simultaneously writing the same file or same state | Low | Avoid; change to parallel read/review first, then main thread or single agent writes |

---

## Parallel Execution Flow

### 1. Assessment and Splitting

After identifying 2-5 key dimensions, determine overlap based on task type:

| Task Type | Overlap Range | Reason |
|-----------|---------------|--------|
| Research/Creative tasks | 30% - 50% | Cross-validation, gap-filling |
| Code/Execution tasks | 0% - 20% | Efficiency priority, reduce duplication |

Don't understand overlap as redundant work. Good overlap means adjacent agents jointly cover the boundary areas most prone to error, such as the intersection of official claims and independent evidence, module interfaces, data methodology, opposing opinions.

### 2. Parallel Launch

The correct parallel method in the current OpenCode environment is: in the same assistant message, use `multi_tool_use.parallel` to wrap multiple `functions.task` calls. Invoking multiple `task` calls individually in sequence, even if described as "parallel" in text, is actually serial.

```json
{
  "tool_uses": [
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "Official narrative",
        "subagent_type": "general",
        "prompt": "Read/search official sources, extract claims, URLs, original excerpts, write to tmp/<session>/tier1_official.md",
        "task_id": "",
        "command": ""
      }
    },
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "Independent experience",
        "subagent_type": "cheap_glm",
        "prompt": "Search independent user experiences, community discussions, GitHub issues, write to tmp/<session>/tier3_independent.md",
        "task_id": "",
        "command": ""
      }
    }
  ]
}
```

`subagent_type` is the OpenCode native agent name, not a model name, and not the old `category`. OpenCode executes `agent.get(subagent_type)`; if no agent with that name is found, it reports `Unknown agent type`.

Source of built-in and custom agents:

- `general` / `explore` are built-in agents in the OpenCode source.
- Other named agents come from `~/.config/opencode/opencode.json`, the project `opencode.json`, or `.opencode/agent(s)/*.md`.
- `provider/model` is only the underlying model entry. To be callable by `task`, it must be wrapped as an agent, e.g., `writer_deepseek -> deepseek/deepseek-v4-pro`.

Common `subagent_type`:

| subagent_type | Applicable Scenarios |
|---|---|
| `general` | General tasks; inherits main session model when no model configured. Suitable for ordinary parallel execution, but don't assume it's a cheap model |
| `explore` | Fast codebase internal search, file location, architecture understanding |
| `reasoning_gpt` | High-reliability reasoning, engineering judgment, solution design, complex code review |
| `writer_deepseek` | Chinese writing, editing, style polishing, final prose polishing; avoid high-privacy materials |
| `cheap_glm` | Low-cost initial screening, classification, outlining, lightweight research and non-critical summaries |
| `private_ds4` | Local DS4 route; suitable for privacy-sensitive, local-execution-priority, low-cost drafts |
| `ollama_kimi` | Ollama Cloud Kimi K2.6, zero-data-retention, relatively cheap; suitable for tasks requiring high privacy posture but not the strongest model |
| `ollama_deepseek_pro` | Ollama Cloud DeepSeek V4 Pro, zero-data-retention, relatively expensive; suitable for tasks requiring high privacy posture and stronger DeepSeek Pro |
| `ds4` | Old alias; prefer `private_ds4` for new tasks |

### File-First Agent Handoff

By default, the main agent and subagents exchange substantive information through workspace files, rather than copying large context into prompts or relying on a subagent's last message to carry the full result.

Five principles:

1. **Prompt carries goals, boundaries, and paths.** Tell the subagent what to solve, what the acceptance criteria are, and which files to read. Material already in the workspace is passed by path, not pasted in full.
2. **Subagents read and iterate files themselves.** Let the subagent build context from source artifacts, scratchpads, claim tables, or code. When changes are needed, write to a namespaced output path; do not let multiple agents overwrite the canonical file simultaneously.
3. **Results land on disk first, then return a manifest.** The subagent's full research, judgment, code, or review goes into the designated artifact. The last message only returns path, status, key conclusions, and open issues; the chat summary cannot be the sole deliverable.
4. **Parent merges from artifacts.** The main agent reads child artifacts, verifies evidence, and writes back to the canonical output. Information transfer between agents is anchored on inspectable files; a previous agent's natural-language summary is not treated directly as source of truth.
5. **Preserve boundaries for failure recovery.** Long tasks update scratchpads, checkpoints, or partial outputs by stage. If a subagent is interrupted, a later agent should be able to continue from the file rather than only re-running the whole conversation.

File-first handoff has three purposes: reduce prompt preprocessing and context copying; let agents read and write repeatedly on existing material; and leave auditable recovery points for interruption, model swap, or parent takeover. Only when the result is very short, there is no workspace, or it is a pure one-shot judgment, may the full deliverable be returned directly in the message.

Main thread responsibilities:

1. Design task splitting and acceptance criteria.
2. Retain final judgment authority; do not directly concatenate subagent outputs as the final answer.
3. Handle conflicts, supplement key sources, run final verification.
4. Control costs; avoid turning lightweight tasks into multi-agent ceremonies.

### 3. Waiting and Integration

`multi_tool_use.parallel` returns all subtask results in the same round of tool response; there is no need and no way to call `background_output`. The `task_id` returned by each `functions.task` is only used when needing to resume the same subagent session later; it is not a parallel wait handle.

Integration steps:

1. Read the artifact files written by each subagent.
2. Cross-validate overlapping areas: discovered by multiple agents → high credibility; single source → annotate pending verification; contradictory information → annotate and analyze reasons.
3. Write integration results to the session directory, e.g., `phase3_synthesis.md`, `fact_check.md`, `brainstorm_synthesis.md`.

## Routing Decisions

First split by data sensitivity, then by task capability:

1. High privacy, cannot leave the local machine: prioritize `private_ds4`. If the task exceeds local Flash capability, pause and let the user decide whether to use the Ollama Cloud zero-data-retention route.
2. Need zero-data-retention but can go to cloud: lightweight tasks use `ollama_kimi`; high-quality reasoning or writing use `ollama_deepseek_pro`.
3. Chinese writing quality priority and content not sensitive: use `writer_deepseek`.
4. Complex engineering judgment, planning, architecture, code review: use `reasoning_gpt`.
5. Cheap, rough, re-runnable initial screening tasks: use `cheap_glm`.
6. Codebase exploration, file location, answering internal structure questions: use `explore`.

Do not use old routing names like `category="deep"`, `category="writing"`, `librarian`, `ultrabrain`, `glm51` in prompts. Unless they are already registered as same-name agents in the current `opencode.json`, the `task` tool cannot invoke them.

Do not default to setting `temperature: 0` for agents "for stability." Many providers/models have their own sampling strategies; DS4 also does deterministic handling for protocol structures, but forcing determinism on long text payloads may cause repetition. Default to not setting temperature; let the provider/server use their own defaults. Only configure when you explicitly know a specific model needs fixed sampling.

---

## Examples

### Research Task (30-50% overlap)

```
Research "adoption of a certain technical framework"
├─ Agent 1 (general): Official narrative + product definition
├─ Agent 2 (cheap_glm): Independent experience + community feedback
├─ Agent 3 (reasoning_gpt): Failure boundaries + competitor comparison
└─ Overlap: Community and enterprise cases both covered, cross-verifiable
```

### Code Task (0-20% overlap)

```
Implement "user authentication system"
├─ Task 1: Auth core logic + Token management
├─ Task 2: Database models + migration scripts
├─ Task 3: API endpoints + test cases
└─ Overlap: Slight overlap at interface definitions to ensure correct integration
```

### Review Task (30% overlap)

```
Review "whether a PR is reliable"
├─ Agent 1 (explore/reasoning_gpt): Code behavior and boundary conditions
├─ Agent 2 (explore): Test coverage, missing fixtures, regression risk
├─ Agent 3 (reasoning_gpt): Architectural consistency and implicit dependencies
└─ Overlap: All agents look at the core diff, but peripheral files split by responsibility
```

### Tasks Unsuitable for Parallelization

```
Fix "an off-by-one in a function"
└─ Main thread directly reads file, changes code, runs tests. Subagent launch and integration cost exceeds the task itself.
```

---

## Notes

- **Don't over-parallelize**: 2-3 well-designed subagents usually outperform 5 loose ones
- **Prompt quality**: Subagent prompts must be sufficiently specific, otherwise results will be shallow
- **Cost awareness**: Parallelism consumes more tokens; evaluate whether it's worth it
- **Intermediate results**: By default, don't need to persist every subagent's raw output; but research / writing workflows should organize key intermediate artifacts into `tmp/<session_slug>/`
- **Old syntax prohibited**: Do not use `mcp_task(run_in_background=True)`, `background_output`, `category`, or `load_skills`; the current tool schema only accepts `description`, `prompt`, `subagent_type`, `task_id`, `command`
