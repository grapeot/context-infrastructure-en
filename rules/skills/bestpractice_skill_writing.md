# Skill Writing Guide (Meta-Skill)

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: When creating or rewriting skill files
- **Created**: 2026-03-29

## What This File Does

A skill file is a capability definition for an AI agent. A well-written skill enables the agent to reliably complete tasks. A poorly written skill either turns the agent into a script mechanically executing a checklist, or causes the agent to expand in the wrong direction due to missing key boundaries and acceptance criteria.

This document defines the core principles, acceptance criteria, and known pitfalls for writing a good skill. It is not a template, nor does it prescribe a specific section order.

## Core Principles

### Principle 1: Outcome Determinism Over Process Determinism

The traditional approach breaks a task into steps: step 1 do X, step 2 do Y, if Z happens do W. This approach places determinism in the process — it's equivalent to writing a script in natural language. The problem is that agents have reasoning and tool-calling capabilities; using them as scripts is wasteful. More importantly, step-based writing cannot cover long-tail corner cases, and corner cases are precisely where agents outperform scripts.

The alternative is to shift determinism from process to outcome: define what the endpoint looks like, how to verify you've reached it, and let the agent decide how to get there.

In practice, the core questions a skill file needs to answer are:

1. **Goal**: what to accomplish. One sentence, clear.
2. **Acceptance criteria**: what result counts as success. Write to this standard: an agent with zero context, given only these criteria, can judge whether it's done. If it can't, the criteria aren't specific enough.
3. **Available resources**: what tools the agent can call, what files it can read, what boundaries it must respect.
4. **Output specification**: the format, storage location, and schema of deliverables.

These four items are the skeleton of a skill file. Everything else (methodology suggestions, domain knowledge, historical experience) revolves around them.

### Principle 2: Write Enabling Guidance, Not SOP

The reader of a skill file is an agent with reasoning capability, and its context window is a scarce resource. Every paragraph in a skill file should increase the agent's probability of completing the task, not consume its attention.

Methodology suggestions can be included, but should appear as suggestions and constraints — the agent has the right to adjust based on actual circumstances. For example, "group analysis by industry sector" is a good suggestion because it offers an effective analytical perspective, but when facing a day with only one macro news item, the agent should have the freedom to skip grouping and do a global analysis directly.

Known pitfalls and traps must be written down, because these are things the agent is unlikely to discover on its own. One concrete pitfall record is more valuable than ten vague methodology suggestions.

Two judgment criteria can help you decide whether a piece of content belongs in a skill file. First, if you delete this paragraph, does the agent's task completion quality or probability decrease? If not, delete it. Second, is this paragraph describing "how to do it" or "what the result should look like"? Prioritize the latter; keep the former only when it genuinely improves success rate.

## What a Skill File Should Contain

Below are the content areas a skill file typically needs to cover. The order and organization are up to you based on the specific skill; you don't need to follow this list rigidly.

**Metadata.** Type (API Guide / Workflow / BestPractice / Tutorial), applicable scenarios, output location, creation and update dates.

**Goal and boundaries.** What this skill does and does not do. Boundaries are especially important: a clear "what it doesn't do" prevents agent drift better than a vague "what it does."

**Acceptance criteria.** Testable success conditions. Those that can be automated should be written as automated checks (run a script, check schema, compare thresholds); those that can't should be written as manual audit criteria. Each criterion should be specific enough that the agent can self-assess at runtime whether it's met.

**Available resources and boundaries.** Tool list, file paths, external dependencies, mandatory constraints. The focus is on what can be used, what cannot be done, and which boundaries cannot be crossed.

**Methodology suggestions.** Analytical frameworks, grouping strategies, prioritization logic that the agent can reference but need not strictly follow. This section should clearly distinguish hard constraints from suggestions.

**Known pitfalls.** Pitfalls encountered in previous iterations, with specific failure symptoms and countermeasures. This is one of the highest ROI sections in a skill file.

A special emphasis here: **do not predict "possible pitfalls" upfront to fill this section.** Known pitfalls should come from actual failures, rework, misjudgments, or real lessons from multiple rounds of iteration. A brand-new skill in its first version can perfectly well have no such section, or only a very short placeholder note. Only when a mistake has actually occurred and is highly likely to recur does it deserve to be written into the meta-layer known pitfalls.

**Output specification.** Format, schema, storage path. If there's a JSON schema, providing a complete example is easier for the agent to understand than describing the schema.

## Acceptance Criteria (for this meta-skill itself)

After writing a skill file, check it against the following criteria.

**Outcome-oriented check.** Does the file contain clear, testable acceptance criteria? Can a new agent, reading only this skill file, judge whether the task is complete? If not, the acceptance criteria aren't specific enough.

**No redundant steps.** Does the file contain any step-by-step instructions ("Step 1... Step 2...")? If so, check whether each step is truly necessary. In most cases, they can be rewritten as goal + constraint form. Only retain sequence requirements when a step's order materially affects the outcome (e.g., "must complete X before Y because Y depends on X's output").

**Pitfall coverage.** Are real failure modes that have actually occurred recorded? If this is a brand-new skill, it's fine to leave this empty. Don't predict or fabricate pitfalls just to "look complete"; filling them in after actually hitting them is more valuable.

**Boundary clarity.** Are the agent's key boundaries sufficiently clear? For example, which tools can be used, which results count as out-of-bounds, which deliverables must be written to disk, which constraints are non-negotiable. Fuzzy boundaries strip a skill of its constraining power.

**Information density.** Is the file length reasonable? Does every paragraph increase the agent's probability of completing the task? If deleting a paragraph has no noticeable impact on the outcome, consider removing it.

## Common Pitfalls

| Pitfall | Manifestation | Countermeasure |
|---------|--------------|----------------|
| Writing skill as SOP | Full of Step 1, Step 2 throughout; agent becomes mechanical executor | Rewrite as goal + constraint + methodology suggestion form |
| Fuzzy acceptance criteria | "High output quality," "deep analysis" | Replace with measurable conditions: "all judgments must reference item_id," "Brier Score better than naive baseline" |
| Over-constraining process | Prescribing that agent must use a specific method, failing outright when it doesn't apply | Limit hard constraints to the outcome level; write methodology as suggestions |
| Missing boundary conditions | Not specifying what to do in exceptional cases (missing data, tool failure, timeout) | At minimum cover "no data" and "tool unavailable" two degradation scenarios |
| Piling on background knowledge | Large sections introducing domain knowledge, consuming agent's context window | Keep only background knowledge that directly affects task execution; reference the rest via file paths |
| Wrapping error messages | CLI/tool wraps underlying errors into vague "something went wrong," losing status_code, response body, and other critical debug info | Pass through raw error details (HTTP status, response body, exception type) so the AI agent can directly locate the root cause from error output. Better to expose more information than to make the agent go through a round of meaningless guessing |
| Forgetting to update INDEX.md | New skill can't be found by anyone | Immediately update `rules/skills/INDEX.md` after writing the skill |

## Relationship with Existing Skills

Before writing a new skill, read `rules/skills/INDEX.md` to confirm there's no duplication. If a similar skill already exists, prioritize modifying it over creating a new one.

For format reference, see `rules/skills/workflow_deep_research_survey.md` (exemplar for research-type skills) and `rules/skills/share_report.md` (exemplar for tool-type skills). Note that these are only format references; the core principles (outcome determinism, enabling rather than SOP) are more important than format.
