# Cognitive Profile Extraction Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Extracting predictable cognitive profiles from unstructured conversation data (group chats, Slack, Discord, email, podcast transcripts, etc.)
- **Output**: A set of "axioms" — conditionally triggered rules that can predict the target person's reaction direction, argumentation stance, and rhetorical devices on new topics
- **Dependencies**: [Parallel Subagent Workflow](./workflow_parallel_subagents.md), [Deep Research Survey Workflow](./workflow_deep_research_survey.md)
- **Created**: 2026-03-13
- **Source**: Example observation project (8,139 WeChat messages → 15 axioms, predictive power backtest 89%)

---

## Model Guardrail

**Pre-execution check**: Confirm whether the current model ID contains `opus`.

- **Is Opus** → Continue. Your context window is extremely precious; your core capabilities are design, quality assurance, and writing. All research, data processing, and code writing must be delegated to sub-agents, and parallel by default. Writing — including axiom text, indices, and final reports — must be done by you personally; do not outsource.
- **Not Opus** → Pause and ask the user:

  > "This workflow is designed to be executed by Opus — Opus's context window and writing capability are core assumptions of the process. Your current model is not Opus. Are you sure you want to continue? If this is a model selection mistake, it is recommended to switch to Opus before starting."

---

## Core Principles

### 1. Parallel + Delegation Is the First Principle

Opus's context window is a scarce resource and should not be consumed by scanning and retrieval. Workflow division of labor:

| Role | Who Does It | Description |
|------|-------------|-------------|
| **Plan (Design)** | Opus main agent | Research plan for each iteration round, dimension division, task boundaries |
| **Execute (Research)** | Sub-agents (parallel) | Data scanning, keyword retrieval, counterexample hunting, statistical analysis |
| **Write (Writing)** | Opus main agent | Axiom text, indices, reports — conceptual consistency and stylistic unity can only be guaranteed by one agent |
| **QA (Quality Assurance)** | Opus main agent | Cross-validate sub-agent results, discover contradictions, judge convergence |

Sub-agent scheduling follows the rules of [Parallel Subagent Workflow](./workflow_parallel_subagents.md): parallelism ≤5, research overlap 30-50%, use `multi_tool_use.parallel` to wrap multiple `functions.task` calls in the same message. Do not use the old `run_in_background=true` syntax.

### 2. Writing Is Not Delegated (Hard Constraint)

All final-output-facing text — axiom definitions, indices, methodology reports — must be personally written by Opus. Reasons:
- Conceptual consistency between axioms (the same phenomenon described in different axioms must not contradict in wording)
- Precision of cross-references (V05's reference to V07's tension description must be aligned on both sides)
- Stylistic unity (15 axioms read like they were written by the same person, not stitched together by 5 agents)

Sub-agent output is **raw research material**, not any part of the final draft.

### 3. Iteration Rounds Dynamically Roll

**Minimum floor**: 3 rounds (broad scan + deep verification + at least one round of stress testing/finalization).

**No upper limit**, but before each round begins, evaluate whether to continue (see "Convergence Judgment Criteria"). Empirical experience: 3-4 rounds is the common convergence point; beyond 5 rounds, marginal returns diminish noticeably, and there is overfitting risk.

### 4. Axioms Are Conditional Trigger Rules, Not Absolute Laws

Every axiom should have counterexamples and boundary conditions. An axiom without counterexamples is either too broad ("he pays attention to AI") or insufficiently evidenced (looks perfect only because no one seriously looked for counterexamples).

---

## Workflow

### Phase 0: Data Preparation

**Goal**: Transform raw data into a searchable set of target person messages.

**Input Requirements**:
- Text message collection of the target person
- Preferably with timestamps (required: for temporal evolution analysis)
- Preferably with source labels — group name/channel name/conversation type (required: for cross-source comparison)
- Optional: version with context (each message accompanied by N preceding/following messages from others, for understanding interaction patterns)

**Preprocessing Steps** (delegate to sub-agents):
1. Extract target person messages from raw format (filter by ID, not display name — display names may change across groups)
2. Produce statistical summary: total message count, time span, message distribution by source
3. If multiple conversation sources exist, produce a version with context

**Scale Assessment → Determine Verification Tier**:

| Data Scale | Recommended Axiom Count | Verification Tier | Notes |
|-----------|------------------------|-------------------|-------|
| < 500 messages | 3-5 axioms | Lightweight | Sparse data; skip stress testing |
| 500-2000 messages | 5-8 axioms | Standard | Simplified stress testing (mutual exclusivity + counterexamples, skip predictive backtest) |
| 2000-5000 messages | 8-12 axioms | Standard+ | Can do simplified predictive backtest (3 topics) |
| 5000+ messages | 10-15 axioms | Full | All three layers of verification, including predictive power backtest (5+ topics) |

**Semantic Search Preparation** (recommended): If data volume ≥ 1000 messages, it is recommended to build an embedding cache at this stage (see [Semantic Search Skill](./semantic_search.md)). Split messages into individual text files or chunks, run one embedding pass to build cache. Subsequent Phase 1/2 sub-agents can use semantic search instead of pure keyword grep — semantic search can find messages with "different keywords but similar meaning," especially valuable for discovering implicit viewpoints and boundary cases.

**Phase 0 Output**: Data overview report, verification tier decision, preliminary dimension hypotheses, embedding cache (if applicable).

---

### Phase 1: Broad Scan (R0)

**Goal**: Parallel scan from five orthogonal dimensions, producing a candidate axiom pool.

**What Opus Does (Plan)**:
1. Determine 5 scan dimensions — suggested default dimensions:

| Dimension | Focus | Typical Keywords |
|-----------|-------|-----------------|
| Domain Expertise Views | Core judgments in the target person's professional domain (tech, business, academia, etc.) | Domain-dependent |
| Methodological Preferences | How to do things, how to decide, how to evaluate | Process, standards, methods, principles |
| Values and Stances | Social issues, ethical judgments, institutional preferences | Fairness, efficiency, should, shouldn't |
| Argumentation Style | How to refute, how to persuade, how to concede | Refutation markers, concession markers |
| Language and Expression Patterns | Sentence structure preferences, analogy habits, emotional markers | High-frequency phrases, punctuation usage |

2. Write prompts for each sub-agent, specifying: search scope, output format (timestamp + source + original text + candidate axiom), allowed overlap range
3. Use `multi_tool_use.parallel` to dispatch 5 `functions.task` sub-agents in parallel within the same message

**What Sub-agents Do (Execute)**:
- Scan all data, extract patterns by assigned dimension
- Each dimension produces 3-5 candidate axioms, each with 3+ timestamped pieces of evidence
- Annotate cross-dimensional discoveries (for cross-validation use)

**What Opus Does (Consolidate)**:
1. Collect results from 5 sub-agents
2. Merge overlapping candidate axioms (merge criterion: same underlying judgment, not similar phrasing)
3. Split overly broad candidate axioms
4. Produce **candidate axiom list** (expected 12-20 candidates) and **preliminary synthesis analysis**

---

### Phase 2: Deep Verification (R1)

**Goal**: Verify the stability, uniqueness, and boundary conditions of candidate axioms.

**What Opus Does (Plan)**:
1. Design 5 verification tasks — suggested default configuration:

| Task | Goal | Method |
|------|------|--------|
| Core Verification | Deepen evidence chain for the 3-5 highest-credibility candidates | Exhaustive search of related messages |
| Cross-Source Comparison | Performance differences of the same viewpoint across different sources | Grouped comparison by source |
| Gap Supplementation | Topics or patterns possibly missed in R0 | Open-ended scan of keywords not covered in R0 |
| Style Verification | Consistency of argumentation style and language patterns | Marker word frequency statistics + pattern matching |
| Time Series | Temporal stability and evolution trajectory of viewpoints | Group by month/quarter; annotate inflection points |

2. **Key deduplication constraint**: Inform each sub-agent "do not repeat evidence already cited in the previous round" — this single constraint provides the greatest report quality improvement
3. Dispatch 5 sub-agents in parallel

**What Sub-agents Do (Execute)**:
- Perform deep verification per assigned task
- For each candidate axiom, provide credibility score (1-10), counterexample list, boundary condition suggestions

**What Opus Does (Consolidate)**:
1. Cross-validate findings from each sub-agent
2. Update credibility for each candidate axiom, add boundary conditions
3. Eliminate candidates with too-low credibility (suggested threshold: < 6.0)
4. **Judge convergence**: Need to continue to Phase 3?

---

### Phase 3: Stress Testing (R2)

**Applicable Condition**: Standard tier and above (data ≥ 500 messages).

**Goal**: Actively attack axiom weaknesses; test the overall framework's predictive power.

**What Opus Does (Plan)**: Design 3-5 stress test tasks. Three core items:

#### 3a. Mutual Exclusivity Check

Check for logical contradictions between axioms.

Operation: Group axioms by relevance (3-4 per group); have sub-agents check for mutual exclusion within groups. Mutual exclusion doesn't necessarily need elimination — it can be absorbed through layered explanations like "descriptive vs normative," "default mode vs boundary mode." But conflict level must be annotated (1-10).

#### 3b. Counterexample Hunting

Explicitly require sub-agents to **actively search for messages that refute axioms**.

Operation: Find at least 2 counterexamples per axiom; assign each counterexample a disruption score (1-10). Counterexamples are not signals of axiom failure — counterexamples absorbable by boundary conditions actually make axioms more precise.

#### 3c. Predictive Power Backtest (Full Version)

Test the effectiveness of the axiom combination as a predictor.

Operation (strict order):
1. Design 5-10 hypothetical topics (covering different axiom combinations)
2. **Without retrieving original data**, use axioms for prior prediction: stance direction, argumentation strategy, possible analogies/short phrases
3. Retrieve original data; search for semantically similar real conversations
4. Compare prediction vs actual consistency; score

**Improved Backtest Protocol** (optional, more credible but more expensive):
- Topics randomly sampled from real data, not agent-selected
- Use an **independent agent not involved in axiom formulation** for consistency judgment
- Score prediction confidence and consistency separately

**Known Limitations** (must be disclosed in the report):
- Small sample (5-10 topics) statistical conclusions are not robust
- LLM judging LLM predictions has systematic bias
- Continuous scale (e.g., 89%) and binary scale (e.g., 60%) differ greatly; recommend reporting both numbers

**What Opus Does (Consolidate)**:
1. Revise each axiom's boundary conditions and credibility based on stress test results
2. Annotate inter-axiom relationship diagram (closed loops, tensions, orthogonal relationships)
3. **Judge convergence**: Need additional rounds?

---

### Phase 4+: Finalization (R3+)

**Goal**: Opus personally writes all axiom text.

**Hard Constraint**: This Phase is not delegated. All axiom text is written by Opus alone.

**Axiom File Template**:

```markdown
# Number Title

## Core Statement
One sentence, independently citable.

## Elaboration
2-3 paragraphs. Explain the logical chain; describe relationships with other axioms.

## Boundary Conditions
Scenarios where it weakens or does not apply. Includes counterexamples and tensions discovered in R2.

## Representative Evidence
Original statements with timestamps and sources (3-5 items).

## Cross-Source Performance
Expression differences of the same viewpoint across different sources.

## Credibility
1-10 score, with brief rationale.
```

**Additional Fields for Style Axioms**:
- **Applicable Scope / Default Mode**: Describe under what context the style axiom activates, and under what context it switches

**Index File**:
- Quick-reference table of all axioms (number, title, core statement, credibility)
- Inter-axiom relationship diagram (closed loops, tensions, orthogonal)
- Key findings summary from stress testing

**If stress test feedback requires major revision** (not just boundary condition tweaks), add one round R3→R4: revise, then run one more round of simplified stress testing to verify revision effects, then finalize.

---

### Phase 5: Publish as Web Site (Only Execute When User Explicitly Requests)

**Do not proactively publish.** Finalization is completion. Only enter this phase when the user explicitly says "publish," "go live," "give me a link."

Basic conversion flow see [Share Report to Web](./share_report.md); the following are **additional experience for multi-page axiom sites**:

**Structure**: Index page (index.html) + one sub-page per axiom. Index page uses a table listing all axioms (number, title, core statement, credibility); each row's title is a hyperlink to the sub-page. Each sub-page has a "← Back to Index" navigation link at the top.

**Practical Tips**:
1. First add inter-page links in Markdown source files (`[V01](V01_xxx.html)`); pandoc conversion automatically preserves links
2. Each HTML file is independently self-contained (CSS embedded with `--embed-resources`), not dependent on external stylesheets — this way opening any sub-page alone displays correctly
3. Use rsync to upload the entire folder, not file by file — ensures directory structure and link consistency
4. After upload, use curl to verify HTTP 200 for the index page and at least 2 sub-pages

**Delegation Rules**: HTML conversion and upload can be delegated to sub-agents, but the index page's Markdown source file (inter-axiom relationship diagram, summary text) is personally written by Opus — this is writing, not mechanical conversion.

---

## Convergence Judgment Criteria

After each round, evaluate these four signals:

| Signal | Meaning |
|--------|---------|
| Revision instructions are directly executable | No more data needed to revise → can converge |
| Predictive power reaches usable level | Continuous metric ≥ 80% → framework has captured core structure |
| Counterexample types begin repeating | New round finds counterexamples of the same type as before → diminishing returns |
| Inter-axiom relationships are stable | No more need to add, merge, or significantly reorganize → structure converged |

**Converge when 3 of the 4 signals are met.** When 2 are met, recommend one more round of lightweight verification for confirmation.

**Risk of over-iteration**: Beyond 4-5 rounds, each round's revisions tend to grind axioms from "generalizable cognitive patterns" into "precise fits to training data." It's better to retain some roughness than to overfit.

---

## Axiom Design Standards

A good axiom should satisfy:

1. **Persistence**: Recurring across time periods and topics, not a one-time statement
2. **Uniqueness**: Specific to the target person, not common sense most people would say
3. **Predictiveness**: Can be used to predict their stance and expression on new topics
4. **Specificity**: Multiple original statements as evidence, from multiple independent time points
5. **Non-redundancy**: Axioms do not overlap; each covers a different facet
6. **Has boundaries**: Annotated under what scenarios it weakens or does not apply

**Axiom Types**: Recommend two categories —
- **Viewpoint type**: Defines "what stance they will take"
- **Style type**: Defines "how they will express it"

**Merge vs Split Judgment**: Same underlying judgment → merge (even if phrasing differs); orthogonal underlying logic → keep as independent axioms (even if domains are close).

---

## Methodological Insights

The following insights are distilled from the example project and apply to all cognitive profile extraction tasks:

### 1. Predictive Power Is the Ultimate Verification Standard

Evidence quantity and credibility scores are intermediate metrics. The final criterion for whether an axiom holds is whether it can be used to predict reactions on new topics.

### 2. Counterexamples Are More Valuable Than Positive Examples

Actively searching for counterexamples, quantifying disruption, absorbing counterexamples with boundary conditions — this process is far more useful than piling up positive evidence. Axioms not stress-tested with counterexamples are merely observations; only after testing are they axioms.

### 3. Axioms Should Anchor at Stable Judgment Levels

When the target person themselves begin questioning a specific method but maintain the higher-level concept, axioms should anchor at the higher-level concept. For example: anchor at "verification is the control surface" rather than "TDD is the control surface" — the former can absorb methodological drift; the latter will be broken by new data.

### 4. Cross-Source Comparison Distinguishes "Genuine Views" from "Social Performance"

The same person's expression differences across different scenarios reveal which are underlying beliefs and which are audience adaptation. If a viewpoint only appears in one source, it may be a situational product; if the direction is consistent across sources but expression differs, it is more likely a genuine stance.

### 5. Time Series Distinguishes "Beliefs" from "Statements"

Without the temporal dimension, stable viewpoints and momentary whims cannot be distinguished. The temporal evolution of viewpoints is itself part of the axiom — record inflection points and evolution trajectories.

### 6. Emotional Deviation Needs Quantification

When discovering that the target person deviates from axiom predictions in certain scenarios, quantify the deviation rate (e.g., "strict metric 2%, composite disruption 6.5/10"), rather than vaguely saying "sometimes deviates."

### 7. Deduplication Constraint Provides the Greatest Sub-Agent Quality Improvement

Informing sub-agents "do not repeat evidence already cited in the previous round" — this simple constraint significantly reduces redundancy and forces agents to find new evidence.

### 8. Style Axioms Are Default Strategy Clusters

The target person typically has audience-adaptive capability. Style axioms describe default high-frequency patterns, not the only patterns. Axiom text needs to explicitly annotate activation conditions and mode-switching scenarios.

### 9. Convergence Signals > Fixed Rounds

Don't preset "do N rounds"; monitor convergence signals. Over-iteration has two costs: context window consumption, and overfitting.

---

## Pitfalls and Countermeasures

| Pitfall | Countermeasure |
|---------|---------------|
| Axiom too broad ("he pays attention to AI") | Ask: what specific behavior can this predict? Can't → not an axiom |
| Axiom too narrow ("he opposes TDD") | Elevate to higher-level concept |
| Evidence selection bias (only finding supporting) | R2 counterexample hunting forces hedging |
| Cross-axiom conceptual inconsistency | Writing not delegated; one person does the full draft |
| Treating forwarded content as personal views | Distinguish "forwarding behavior" from "stance expression on forwarded content" |
| Treating social scenario statements as stable beliefs | Cross-source comparison + time series verification |
| Inflated predictive backtest | Report both continuous and binary scales; disclose judge limitations |
| Over-iteration leading to overfitting | Monitor convergence signals; stop when ≥3 signals met |
| Sub-agent research depth insufficient | Prompt explicitly requires original excerpts + timestamps; do not accept pure summaries |
| Context window consumed by research | Strictly follow Plan/Write self-do, Execute fully delegate division of labor |

---

## Scale and Cost Reference

| Data Scale | Total Sub-Agent Invocations | Estimated Rounds |
|-----------|----------------------------|------------------|
| < 500 messages | 10-12 | 2-3 rounds |
| 500-2000 messages | 12-15 | 3 rounds |
| 2000-5000 messages | 15-20 | 3-4 rounds |
| 5000+ messages | 18-25 | 3-5 rounds |

5 parallel sub-agents per round is the default configuration. Adjustable to 3-7 based on data volume and dimension complexity.

---

## See Also

- [Semantic Search Skill](./semantic_search.md) — Beyond keyword matching; use embedding similarity to discover semantically related messages
- [Parallel Subagent Workflow](./workflow_parallel_subagents.md) — Sub-agent scheduling, overlap, cross-validation, and applicability criteria
- [Deep Research Survey Workflow](./workflow_deep_research_survey.md) — Multi-agent parallel + cross-validation base architecture
- Example observation project (original source of this skill) — `contexts/people/magong/`

---

## Changelog

| Date | Change |
|------|--------|
| 2026-03-13 | Initial version; abstracted and generalized from example observation project methodology.md |
