# Parallel Subagent Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Independent review, parallel research/exploration, and explicitly user-requested implementation delegation
- **Created**: 2026-02-20
- **Last Updated**: 2026-10-18

---

## Core Judgment

The primary value of subagents is not simulating a human team, nor wrapping an ordinary task in more complexity. It solves three specific problems:

1. **Context window isolation**: Let different agents each hold a manageable context, avoiding the main thread simultaneously ingesting large volumes of files, web pages, logs, and intermediate judgments.
2. **Parallel reading and independent exploration**: Let multiple agents simultaneously search, read, locate, and verify, reducing single-path dependency.
3. **Cross-validation**: Let different agents independently reach conclusions within intentionally overlapping scopes, using agreement and divergence to expose omissions, misreadings, and assumption conflicts.

External experience points to the same conclusion: multi-agent is more viable for research-heavy, read-heavy, high-value tasks; it is costly and fragile for tasks requiring multiple agents to share large amounts of state, continuously coordinate writes, or mutually correct in real time. Anthropic's multi-agent research system positions it as trading more tokens for stronger parallel exploration and compression capability, explicitly noting that multi-agent may consume approximately 15x the tokens of normal chat; LangChain's experience emphasizes that read-heavy is more suitable for parallelism than write-heavy, because write operations carry implicit decisions and merge conflicts are costly.

Research basis: Anthropic Engineering "How we built our multi-agent research system" (https://www.anthropic.com/engineering/multi-agent-research-system), LangChain "How and when to build multi-agent systems" (https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems), Cemri et al. "Why Do Multi-Agent LLM Systems Fail?" (https://arxiv.org/abs/2503.13657).

## Delegation Boundaries and When to Use Parallel Mode

Decide whether to delegate before deciding whether to parallelize. The main thread implements by default; delegate implementation only when the user explicitly requests it. Multi-file scope, clean module boundaries, context savings, and cheaper models do not authorize delegation. A selected writing workflow may designate a writer; prose drafting is not code implementation.

Code / privacy / design review normally uses an independent subagent or Antigravity CLI for a fresh context, with main-thread final acceptance. Trivial, low-risk local edits may be self-checked proportionally. A single review is exempt from the parallel threshold below. Broad surveys and exploration may use multiple subagents across independent dimensions.

When launching multiple subagents in parallel, meet at least 2 of the following conditions without triggering the anti-patterns below:

1. **Broad information surface**: Need to check multiple files, multiple web pages, multiple data sources, multiple time periods; reading them all in the main thread would pollute context.
2. **Splittable into independent read tasks**: Can be divided into at least 2 relatively independent exploration directions, each expected to need ≥5 tool calls.
3. **Independent judgment needed**: Need opposing review, fact-checking, competitor comparison, code review, solution comparison; a single path easily self-confirms.
4. **High-value uncertainty exists**: Task results will affect subsequent decisions, public output, code changes, or high-cost actions; spending extra tokens is worthwhile.
5. **Main thread needs to preserve design/integration capability**: The main agent should use its attention for problem decomposition, standard setting, evidence integration, and final judgment, not buried in low-level search or repeated reading.

When the multi-agent parallel threshold is not met, work directly or launch a single independent review as needed; do not split artificially.

## Anti-Patterns

Default to not splitting into multiple subagents in the following cases; task value does not replace the explicit user request required for implementation delegation:

1. **Single-point small task**: Reading 1-2 files or making a minor local edit does not need mechanical splitting. Judge a single independent review by risk; file count alone must not skip privacy or key design review.
2. **Strong sequential dependency**: The next step must depend on the previous step's output; splitting only creates waiting and handoff costs.
3. **Shared state writes**: Multiple agents simultaneously modifying the same set of files, the same table, the same copy; conflicts and implicit decisions are hard to merge.
4. **Context must be fully shared**: Every agent must know the full background to do it right; splitting only loses conditions.
5. **Verification criteria unclear**: No checkable output format, evidence requirements, or acceptance conditions; multiple agents will only produce multiple vague summaries.

## Task Type Reference

| Task Type | Suitability | Recommended Approach |
|-----------|-------------|---------------------|
| External research, paper/product/market survey | High | 3-5 agents, split by evidence function, 30-50% overlap |
| Large codebase understanding, file location, architecture mapping | High | `explore` parallel split by module or problem; main thread integrates |
| Code / privacy / design review, solution review, fact-checking | High | Normally 1 independent reviewer; complex high-risk changes may use multiple perspectives, with main-thread acceptance |
| Brainstorm, opposing viewpoints, thesis stress testing | Medium-High | Different agents assigned different judgment perspectives; output must answer the same set of questions |
| Engineering and code implementation (including multi-file) | Default: do not delegate | Delegate only on explicit user request; main thread owns merge and test acceptance |
| Single bug fix, local edit, format adjustment | Low | Main thread does directly |
| Multiple agents simultaneously writing the same file or same state | Low | Avoid; read/review independently first, then the main thread, authorized implementer, or writing-workflow writer writes |

---

## Parallel Execution Flow

### 1. Assessment and Splitting

A single independent review needs no forced splitting. When parallel work is appropriate, identify 2-5 dimensions and set overlap by task type:

| Task Type | Overlap Range | Reason |
|-----------|---------------|--------|
| Research / Multi-angle review / Creative tasks | 30% - 50% | Cross-validation, gap-filling |
| Codebase exploration / User-requested delegated implementation | 0% - 20% | Reduce duplication, retaining interface-boundary overlap |

Don't understand overlap as redundant work. Good overlap means adjacent agents jointly cover the boundary areas most prone to error, such as the intersection of official claims and independent evidence, module interfaces, data methodology, opposing opinions.

### 2. Parallel Launch

**Follow the live runtime schema.** Check that `functions.task`, the target agent, and parameters are available. State missing capabilities honestly; do not fabricate calls or silently swap models. A single review needs one call; bundle co-ready tasks in one message with `multi_tool_use.parallel`.

**Default to `background: true` when supported.** Wait for automatic completion without polling or sleeping to check progress. Continue independent work or end the turn while waiting. Use synchronous calls only when async is unsupported or the step must block on the result. Background tasks can remain concurrent across messages; co-ready tasks should still launch together.

The example assumes the schema supports `background`; omit that field otherwise. A launch receipt is not completion. Do not pass empty `task_id` / `command` placeholders for new tasks; `task_id` is for continuing an existing task.

```json
{
  "tool_uses": [
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "Official narrative",
        "subagent_type": "general",
        "prompt": "Read/search official sources, extract claims, URLs, original excerpts, write to tmp/<session>/tier1_official.md",
        "background": true
      }
    },
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "Independent experience",
        "subagent_type": "general",
        "prompt": "Search independent user experiences, community discussions, GitHub issues, write to tmp/<session>/tier3_independent.md",
        "background": true
      }
    }
  ]
}
```

`subagent_type` is the OpenCode native agent name, not a model name, and not the old `category`. OpenCode executes `agent.get(subagent_type)`; if no agent with that name is found, it reports `Unknown agent type`.

Source of built-in and custom agents:

- `general` / `explore` are built-in agents in the OpenCode source.
- Other named agents come from `~/.config/opencode/opencode.json`, the project `opencode.json`, or `.opencode/agent(s)/*.md`.
- `provider/model` is only the underlying model entry, not a substitute for a registered agent name.

Capability routing applies only after deciding to delegate; it does not authorize implementation delegation. The user's current explicit choice of model, agent, or CLI takes precedence over default capability routing, subject to runtime capabilities and data boundaries. If the specified runner is unavailable, report the blocker rather than substituting it. Names come from the active runtime configuration:

| subagent_type | Applicable Scenarios |
|---|---|
| `general` | General tasks; inherits main session model when no model configured. Suitable for ordinary parallel execution, but don't assume it's a cheap model |
| `explore` | Fast codebase internal search, file location, architecture understanding |
| Registered specialist agents | Match review, reasoning, coding, screening, or data-boundary needs; do not hardcode model mappings here |
| Antigravity CLI (not `functions.task`) | Independent review or a selected writing workflow; read the installed `ai-agent-cli` root skill and Antigravity focused skill, then use currently available models. Do not conflate it with a Gemini subagent |

Each task prompt should specify scope, output artifact, acceptance criteria, total deadline, logs, stop conditions, and exclusive write scope. Independent reviewers should normally write only their review artifacts; the main thread or authorized implementer makes fixes.

Independent review uses a new agent/task context or new CLI conversation that did not participate in implementing or drafting the artifact. Do not resume the original author's task/conversation as an independent reviewer. Author self-checks may remain, but do not count as independent review; a different model or vendor is not required.

### File-First Agent Handoff

By default, the main agent and subagents exchange substantive information through workspace files, rather than copying large context into prompts or relying on a subagent's last message to carry the full result.

Five principles:

1. **Prompt carries goals, boundaries, and paths.** Tell the subagent what to solve, what the acceptance criteria are, and which files to read. Material already in the workspace is passed by path, not pasted in full.
2. **Subagents read and iterate files themselves.** Let the subagent build context from source artifacts, scratchpads, claim tables, or code. When changes are needed, write to a namespaced output path; do not let multiple agents overwrite the canonical file simultaneously.
3. **Results land on disk first, then return a manifest.** The subagent's full research, judgment, code, or review goes into the designated artifact. The last message only returns path, status, key conclusions, and open issues; the chat summary cannot be the sole deliverable.
4. **Parent merges from artifacts.** The main agent reads child artifacts, verifies evidence, and writes back to the canonical output. Information transfer between agents is anchored on inspectable files; a previous agent's natural-language summary is not treated directly as source of truth.
5. **Preserve boundaries for failure recovery.** Long tasks update scratchpads, checkpoints, or partial outputs by stage. If a subagent is interrupted, a later agent should be able to continue from the file rather than only re-running the whole conversation.

File-first handoff has three purposes: reduce prompt preprocessing and context copying; let agents read and write repeatedly on existing material; and leave auditable recovery points for interruption, model swap, or parent takeover. Results may be returned directly when very short, without a workspace, for one-shot judgments, or when the agent/runtime has no write permission. Read-only exploration without write access should return verifiable file paths, line numbers, evidence, and conclusions; the parent verifies and saves the necessary results. Do not elevate permissions or bypass read-only limits to satisfy file-first handoff.

Main thread responsibilities:

1. Design task splitting and acceptance criteria.
2. Retain final judgment authority; do not directly concatenate subagent outputs as the final answer.
3. Handle conflicts, supplement key sources, run final verification.
4. Control costs; avoid turning lightweight tasks into multi-agent ceremonies.

### 3. Waiting and Integration

With `background: true`, the wrapper returns launch receipts only. Wait for automatic completion before reading results and artifacts; do not poll, call non-existent `background_output`, or use scheduled inspection as a workaround. Only a synchronous wrapper returns completed results directly. `task_id` is for continuation, not a wait handle. Set stage budgets, a total deadline, logs, and failure stop conditions before dispatch; preserve partial artifacts for recovery.

Integration steps:

1. Read artifact files when available; for children without write access, accept evidence and content under the read-only handoff exception above, then verify and save it in the parent.
2. Cross-validate overlapping areas: discovered by multiple agents → high credibility; single source → annotate pending verification; contradictory information → annotate and analyze reasons.
3. Write integration results to the session directory, e.g., `phase3_synthesis.md`, `fact_check.md`, `brainstorm_synthesis.md`.

### 3.1 Running Continuation and Steering

When appending a prompt with the same `task_id` to an already-running `functions.task`, a tool receipt such as `context sent` or `Background task updated` is transport-level acceptance only, not proof the child received or saw the new scope. In that check the appended scope was not visible, which only means no observable delivery record was seen at the time; async context does not necessarily land in the timeline. It does not let you claim the child received it, and it is not a universal platform behavior. So do not treat a tool `accepted` as delivered: a real scope change needs an observable `timeline` record or an explicit correlated acknowledgement before you rely on it, and once an ack exists you do not need to re-check the timeline. Background subagent completion still uses the built-in automatic parent chain; do not poll progress or turn waiting into a busy-wait. A delivery check is a single bounded step reserved for when you append meaningful scope or require an ack, not a monitor over every tool call. When an explicit append is the fallback, first verify it is still the same current owner, task, attempt, and directory, preserve the child's current model and agent, and do not guess defaults; on an unknown outcome, read state before retrying, do not blind-retry, deduplicate on the same request id (a caller-side convention that does not assume the legacy API implements idempotency), and do not double-post what was already delivered. A task-completion flag is not the deliverable; acceptance needs a correlated ack and the actual artifact in addition to the timeline, and a task-context tool receipt alone is not enough. See the acceptance criteria in the [Astra Coordinator workflow](./workflow_astra_coordinator.md).

## Routing Decisions

Route only after deciding to delegate, matching data boundaries and registered capabilities. The user's current explicit choice of model, agent, or CLI takes precedence over default routing, subject to runtime capabilities and privacy constraints; report an unavailable specified runner rather than substituting it. Routing must not force the main thread to outsource coding:

1. Use `explore` for exploration and `general` for general research. Match specialized review, reasoning, screening, and explicitly user-requested delegated implementation to currently registered capabilities.
2. Honor local/cloud boundaries for private data; insufficient capability does not authorize external disclosure. A selected writing workflow determines its writer.
3. Antigravity CLI can provide a fresh independent context for code / privacy / design review and is not a Gemini subagent. Read the installed `ai-agent-cli` root skill and Antigravity focused skill; use the current model list rather than fixed names.

Do not reuse legacy `category` parameters or historical agent aliases; invoke only agents registered in the active runtime.

Do not default to `temperature: 0` "for stability." Use provider/server sampling defaults unless the target model explicitly requires fixed sampling.

---

## Examples

### Research Task (30-50% overlap)

```
Research "adoption of a certain technical framework"
├─ Agent 1 (general): Official narrative + product definition
├─ Agent 2 (general): Independent experience + community feedback
├─ Agent 3 (general): Failure boundaries + competitor comparison
└─ Overlap: Community and enterprise cases both covered, cross-verifiable
```

### User-Requested Delegated Code Task (0-20% overlap)

```
Prerequisite: The user explicitly requested delegated implementation of "user authentication system"; otherwise the main thread implements directly
├─ Task 1: Auth core logic + Token management
├─ Task 2: Database models + migration scripts
├─ Task 3: API endpoints + test cases
└─ Overlap: Slight overlap at interface definitions to ensure correct integration
```

### Review Task (Single reviewer or multi-angle overlap)

Normally use one independent reviewer or Antigravity CLI, with main-thread acceptance; the multi-agent parallel threshold does not apply. Complex high-risk PRs may be split as follows:

```
Review "whether a PR is reliable"
├─ Agent 1 (explore / review agent): Code behavior and boundary conditions
├─ Agent 2 (explore): Test coverage, missing fixtures, regression risk
├─ Agent 3 (review agent): Architectural consistency and implicit dependencies
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
- **Runtime syntax**: Use the live schema; default to `background: true` when supported. Do not use legacy `mcp_task(run_in_background=True)`, `category`, or `load_skills`, or invent a `background_output` tool.

## Common Mistakes

| Mistake | Correct Approach |
|---|---|
| Treating a background wrapper receipt as completion, or polling for progress | Wait for automatic completion, then read artifacts; only synchronous calls return completed results directly |
| Rejecting a single review because fewer than 2 parallel conditions are met | Normally use one independent reviewer; trivial, low-risk local edits may be excepted proportionally |
| Delegating implementation for cheaper models or context savings | Delegate implementation only when explicitly requested by the user |
| Calling cross-message background work necessarily serial | Background tasks may remain concurrent; launch co-ready tasks together |
