# Deep Research Survey Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: When deep, comprehensive, verifiable third-party research on a topic is needed
- **Output Location**: `contexts/survey_sessions/`
- **Created**: 2026-02-19
- **Last Updated**: 2026-07-22

## Core Principles

1. **Incentive-Aware Verification**: The value of information depends on the incentive structure of its source. Vendor narratives are useful but not self-proving. Every major claim must be traced back to independent evidence unrelated to the publisher's incentives.
2. **Cross-Validation**: Multiple sub-agents cover overlapping topics; use divergence and contradiction to expose blind spots.
3. **Traceability**: All citations retain URLs; key citations retain original excerpts, not relying on summaries.
4. **Progressive Focusing**: First scan the full picture, extract claims, then examine each dimension for verification.
5. **Single Primary Deliverable + Reusable Artifacts**: One final report; key intermediate artifacts stored in the session directory.
6. **Shared Research Spine, Forked Reader Mode**: Search, verification, and artifact retention are shared; before drafting, decide on internal / external mode based on the reader.

## Information Source Tiers

In every research project, source credibility is not equal. Stratify by incentive structure:

| Tier | Type | Signal Characteristics | How to Use |
|------|------|------------------------|------------|
| Tier 1 | Vendor official docs, blogs, case studies | Tells you how the product wants to be perceived | Extract claims; do not use as verification basis |
| Tier 2 | Press coverage, sponsored reviews, third-party evaluations | Understands market positioning, but incentives still lean positive | Aid in understanding market narratives; not independent evidence |
| Tier 3 | Independent developer blogs, HN/Reddit discussions, Stack Overflow | Stronger signal, but sampling is biased | Use as verification signal; note community bias |
| Tier 4 | GitHub issues, migration stories, production post-mortems, commit history | Behavioral evidence rather than attitude expression; the cost of migration far exceeds posting a positive review | Highest credibility; use to verify claims and mark boundaries |

Evidence credibility in ascending order: attitude expression ("I think it's good") < usage scenario descriptions < comparative decision records < Migration stories < Production post-mortems < code/commit-level evidence. Prioritize collecting the latter half.

## Two Reader Modes

Distinguish by **whether the reader's context is known and thick**, not by channel.

**Mode A: Internal (Shared-Context-Driven Decision Memo)** — For readers who are yourself or collaborators sharing long-term context. Writing contract: do not restate common knowledge; focus on unknown points that would change conclusions, points most likely to be opposed, and points conflicting with existing views; prioritize delivering conclusions, basis, unresolved issues, and recommended actions.

**Mode B: External (Zero-Preset-Context Publishable Argument)** — For readers who are not known entities. Writing contract: must explicitly answer why this matters; must place the most useful judgment in the first few paragraphs; key definitions, comparison frameworks, and constraints must be on the page, not left for the reader to fill in mentally.

After selecting External mode, one more fundamental question must be answered: **Is this topic's relevance to the target reader present, future, or likely irrelevant now?** For many research subjects, the honest answer is the third — no direct relevance to most readers in the short term, but potentially important long-term. If so, the article's thesis must explicitly acknowledge this, rather than stacking dazzling cases to imply greater short-term value than actually exists. Acknowledging "not relevant now" does not equal "not worth writing"; the reason to write may precisely be to help readers distinguish short-term noise from long-term signal.

Ask three questions before choosing a mode: (1) Is this reader known and sharing thick context? (2) Is the primary value helping them judge faster or helping them understand and believe? (3) Can the report stand independently after removing private context? Lean toward internal for shared context and fast judgment; lean toward external for self-contained, disseminable, and persuasive content.

## Workflow

### Phase 1: Initial Scan + Claim Extraction

**Goal**: Understand the full picture, distinguish vendor narratives, market narratives, and independent evidence, and extract claims to be verified.

**Operations**:

1. Use Tavily for 2-3 searches covering:
   - Basic description of the research subject (Tier 1 official information)
   - Market evaluations and media coverage (Tier 2 market narratives)
   - Criticism, controversy, known issues (Tier 3-4 signals)
2. Summarize 3-5 dimensions requiring in-depth research.
3. **Claim Extraction**: From Tier 1-2 sources, list the product/subject's key claims (performance, applicable scenarios, cost, advantages, etc.). For each claim, annotate the verification channel: in which Tier 3-4 sources can this claim be confirmed or refuted? Encode verification tasks into Phase 2 sub-agent prompts.

**Output**: Write to `tmp/<session_slug>/scratchpad.md`, including a claim extraction table:

```markdown
## Claim Extraction

| Claim | Source (Tier) | Verification Channel | Verification Status |
|-------|---------------|----------------------|---------------------|
| "zero-config, works out of the box" | Tier 1 official docs | GitHub issues for setup pain; Reddit for migration stories | Pending |
| "lower cost than competitors" | Tier 1 official blog | Production post-mortem; independent benchmark | Pending |
```

### Phase 1.5: Prior Work Positioning (Required for Academic Paper Research)

**Trigger Condition**: The research subject is an academic paper, or the core basis of the research topic is a paper / set of papers. If the subject is a product, company, or pure industry topic, skip this step.

**Why This Step Is Needed**: A paper's Related Work and Contribution statements are self-serving — the authors position themselves in the most favorable light. Without reading prior work, you cannot determine whether a paper is inventing a new problem or merely confirming with good measurement something the community already sensed. This distinction directly determines article positioning: whether to write a domain survey, a single-paper deep dive, or a hybrid.

**Operations**:

1. Read the paper's Related Work / Background section and extract:
   - Each cited prior work
   - How the authors position their advantage relative to prior work
   - The specific incremental contribution the authors claim

2. Build a cited work mapping table:

```markdown
| Prior Work | Year/Venue | What It Did | What It Didn't Do | This Paper's Claimed Advantage |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

3. For each cited cluster, externally verify what the prior work actually established (use Tavily to search original papers/blogs/community discussions; do not rely on this paper's own framing). Pay special attention to:
   - Whether the prior work's actual scope is broader or narrower than described in this paper
   - Whether the prior work already has independent verification or community reproduction
   - Whether this paper's claim of "first to do X" is accurate

4. Based on this, answer two questions:

**Incrementality Judgment**: What is this paper's genuine new contribution?
- Separate "facts already known in the domain" from "facts newly added by this paper"
- Assess increment size: conceptual level (medium/large), empirical level (medium/large), practical level (meaningful/marginal)

**Positioning Judgment**: What form should the write-up take?
- **A. Domain Survey**: If prior work is already rich, this paper is just one piece, and target readers need the full picture
- **B. Single-Paper Deep Dive**: If this paper's increment is large enough and self-contained, prior work only needs 1-2 paragraphs of background
- **C. Hybrid (Recommended Default)**: 30-40% domain background + 60-70% focus on this paper. First explain why the layer this paper attacks differs from the layer prior work focused on, then use this paper's measurements/data as the main thread

**Output**: Write to scratchpad under `## Prior Work Positioning`. If sub-agents were launched for this step, results also go to `tmp/<session_slug>/prior_work_survey.md`.

**Common Mistakes**:
- Accepting the paper's Related Work as fact without externally verifying prior work's actual scope
- Assuming "this field is mature" because the paper cites many prior works — many citations may also indicate a fragmented field
- Equating "this paper is the first to measure X" with "X didn't exist before" — measurement and discovery are different contribution types

### Phase 2: Splitting and Parallel Research

**Goal**: Deep dive from multiple angles while simultaneously verifying claims extracted in Phase 1.

**Splitting Principle**:

Divide into 3-5 dimensions, each serving two functions: covering a topic and verifying specific claims. Dimensions must have ≥50% overlap so different agents have the opportunity to discover different interpretations of the same information or contradictory conclusions.

**Design dimensions by evidence function**, not just by topic:

- Official narrative (Tier 1-2): product self-definition, official cases, pricing logic
- Independent usage experience (Tier 3): actual developer usage records, community discussions, comparative decisions
- Failures and boundaries (Tier 3-4): known issues, GitHub issues, limitations, criticism
- Migration behavior (Tier 4): records of users migrating to/from competitors, and reasons why

**Launching Sub-agents**:

Launch 3-5 sub-agents simultaneously, each responsible for one dimension. Use `multi_tool_use.parallel` wrapping multiple `functions.task` calls; see `workflow_parallel_subagents.md` for specific invocation. Default to `general`; use a low-cost screening agent for initial triage, a locally configured privacy-preserving agent for sensitive material, and a high-reliability reasoning agent for complex judgment or final QA. Use only agent names registered in the current harness.

```json
{
  "description": "Research XX dimension",
  "subagent_type": "general",
  "prompt": "[specific research dimension prompt]",
  "task_id": "",
  "command": ""
}
```

Each sub-agent's prompt must explicitly state:
1. What specific topic to research
2. Claims relevant to this dimension extracted from Phase 1 claim extraction (requiring supporting or refuting evidence from Tier 3-4 sources)
3. Prioritize returning behavioral evidence (migration, production issues, commit history) over attitude expressions (positive/negative reviews)
4. Must return URLs and original excerpts (not summaries)
5. Other related dimensions that can be covered (forming overlap)

The main thread organizes key conclusions, source indices, and judgment processes into artifact files in the session directory; raw output does not need to be saved verbatim, but critical information must not remain only in stdout.

**Tavily Parameter Preferences**:
- `max_results=6` (increase to 10 if coverage is insufficient)
- `search_depth="advanced"`
- `include_answer=false` (directly review results and original excerpts; do not rely on aggregated summaries)
- Enable `include_images` / `include_image_descriptions` as needed

### Phase 3: Integration and Cross-Validation

**Goal**: Discover contradictions, compare how claims perform across different source tiers, and form credible conclusions.

**Operations**:

1. Compare results from each sub-agent, focusing on:
   - Information discovered by multiple agents → high credibility
   - Information from a single source → annotate source, flag for verification
   - Contradictory information → specially annotate, analyze reasons
2. For each claim from Phase 1, check verification status:
   - Independent evidence exists in Tier 3-4 sources → mark as verified, record sources
   - Only appears in Tier 1-2 sources → mark as "vendor source only, not independently verified"; do not write into report as fact
   - Tier 3-4 sources show evidence contradicting Tier 1-2 → prioritize Tier 3-4, record contradiction points
3. If major contradictions are found, launch additional sub-agents for targeted verification.

### Phase 3.3: Source-Level Fact-Check

**Goal**: Before thesis brainstorming, return to the primary sources behind the central claims and eliminate subagent misreading, hallucination, or selective quotation. Run this phase by default except for purely factual compilations.

1. Select five to ten critical references: sources that directly support or challenge the likely thesis, sources that appear to conflict, sources containing key numbers, and sources of uncertain credibility.
2. Use Tavily extract to reread the original material. Verify the paraphrase, qualifications, URL, and numerical precision. One subagent summary cannot validate another subagent summary.
3. Write `tmp/<session_slug>/fact_check.md`. For every item, record the source, current paraphrase, verdict (`consistent`, `partial deviation`, or `hallucination`), and original excerpt.
4. Mark corrections in the scratchpad. Brainstorm only from corrected facts; if a central source fails verification, return to research first.

### Phase 3.5: Brainstorm and Targeted Research Decision

**Goal**: After fact-checking, use independent perspectives to expose thesis weaknesses, counterarguments, and missing information. Run this phase by default for external-facing articles, judgment-driven research, and any task that needs a thesis. A purely factual compilation may skip it.

1. The main thread writes `tmp/<session_slug>/brainstorm_brief.md` with the initial thesis, verified facts, uncertain claims, counterexamples, target reader, and writing constraints.
2. In parallel, assign agents distinct roles such as evidence skeptic, target reader, and product decision-maker. Each answers: What is the strongest version of the thesis? What is its weakest premise? Which three to five questions need more research? What evidence would change the conclusion?
3. Integrate the results into `tmp/<session_slug>/brainstorm_synthesis.md`, listing thesis candidates, mandatory follow-up questions, and verification routes.
4. Run one focused research round narrower than Phase 2, limited to the weakest premises and counterexamples. Append new sources to `source_index.md`.

Brainstorming is not title polishing or generic multi-agent restatement. It must produce targeted research or a clearer judgment.

### Phase 4: Writing

After Phase 1-3 research is complete, enter the writing phase. Choose the path based on target output type:

**External-facing analysis article** -> Enter the [External Writing Workflow](./workflow_external_writing.md). Start with its thesis-and-outline selection and article-warrant check. The Main Agent then establishes the source contract, writing brief, voice contract, and prose-neutral content map. Use the [Antigravity CLI](./antigravity_cli.md) to generate independent prose candidates in parallel. The Main Agent cold-reads independently before cross-checking a blind-reader audit, permits at most one fresh AGY prose retry when the verdict is `RETRY_PROSE`, and finishes with logged surgical edits.

**Internal memo** (for yourself or collaborators sharing context) → Load the [Internal Writing Workflow](./workflow_internal_writing.md). First surface the conclusions and basis that most affect decisions, and clearly note unresolved points and next steps. Read [`COMMUNICATION.md`](../COMMUNICATION.md) before writing.

**Shared Format Requirements** (common to both modes):
- Use the requested output language consistently in Markdown
- All external citations must use absolute `https://` URLs so they remain valid across publication environments
- Key citations retain original excerpts, not just summaries
- If the final deliverable is an external article, important sources go directly into inline Markdown links in the body, not just piled at the end

**Difference between survey report and blog post**: This workflow produces a survey report in `contexts/survey_sessions/`. Do not add blog frontmatter, subscription components, or channel-specific metadata by default. When the user explicitly requests a blog post, follow the target project's blog format and location as a separate step.

**Delivery Endpoint**: Writing the final MD file under `contexts/survey_sessions/` is the delivery endpoint. Do not automatically publish to a blog, social platform, community, or another external channel. Publication requires explicit authorization for that action.

**Storage Location**: `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md`

**Recommended artifact directory** `tmp/<session_slug>/`, at minimum containing:
- `scratchpad.md` (with claim extraction table)
- `search_manifest.md` (with output file index table, subagent positioning method, data coverage assessment)
- `fact_check.md` (Phase 3.3 source-level verification)
- `brainstorm_brief.md` and `brainstorm_synthesis.md` (judgment-driven or external-facing work)
- `search_notes.md` (as needed)
- `source_index.md` (as needed)

## Search Manifest Must Include Output File Index

```markdown
## Output File Index

| File | Path | Description |
|------|------|-------------|
| Scratchpad | `tmp/<session_slug>/scratchpad.md` | Main thread research notes |
| Search Manifest | `tmp/<session_slug>/search_manifest.md` | This file |
| Final Report | `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md` | Final report |

## Subagent Raw Output

| Agent | Session ID | URLs | Status |
|-------|-----------|------|--------|
| Agent 1 | `ses_xxx` | 50+ | completed |
```

## URL Retention Standards

Cases where URLs must be retained: direct citations, data sources (numbers/statistics/ratings), evaluation sources, official information.

If the final deliverable is an external-facing article, the default requirement is: **important sources go directly into inline Markdown links in the body.** Do not pile links only in end-of-article references or only in scratchpad / manifest. Readers should be able to jump to verify judgments, facts, and quotes in the body on the spot.

```markdown
**Source description** (URL)
> Original excerpt

or

Someone commented on a platform (URL):
> "Original text"
> (👍 X 👎 Y)
```

Avoid: citations without URLs ("someone said..."), summaries without original excerpts.

If the research will later be turned into an external article, do one more check before writing: are these URLs actually retained in the final draft, rather than only existing in research artifacts?

## Common Research Dimension Reference

| Research Subject | Possible Dimensions |
|------------------|---------------------|
| Product/Service | Feature evaluation, price comparison, user cases, negative feedback, competitor analysis |
| Course/Training | Course content, instructor background, student reviews, price-value, alternatives |
| Company/Organization | Business model, market position, reputation, controversies, financial status |
| Technology/Tool | Technical principles, usage experience, applicable scenarios, limitations, alternatives |
| Viewpoint/Framework | Consensus level, authoritative endorsement, opposing voices, practical implementation, timeline accuracy |

## Common Pitfalls

| Pitfall | Countermeasure |
|---------|---------------|
| Only finding positive information | Specifically search for "criticism", "negative review", "scam", "overpriced" |
| Single information source | Mandate sub-agents to find multiple independent sources |
| Over-summarization losing detail | Require retention of original excerpts, not just summaries |
| Dimension division too clean with no overlap | Deliberately blur edges when designing dimensions |
| Sub-agent returns too shallow information | Emphasize "depth", "specificity", "original text" in prompts |
| Intermediate file clutter | Centralize in `tmp/<session_slug>/`, only retain key indices and judgments |
| Using wrong subagent type | `subagent_type` must be a currently registered agent name; default to `general` for external research, `explore` for codebase exploration, and a locally configured privacy-preserving agent for sensitive material |
| Research results become vendor marketing summaries | Phase 1 extracts claims, Phase 2 allocates dimensions by evidence function, Phase 3 checks verification status |

For writing-stage requirements and failure prevention, see the [External Writing Workflow](./workflow_external_writing.md).
