# External Writing Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Transforming research materials into judgment-driven external-facing analysis articles, public survey reports, or course/client content for external readers
- **Prerequisites**: Output of Phase 1-3 of the Deep Research Survey Workflow (`workflow_deep_research_survey.md`), or equivalent verified materials
- **Created**: 2026-04-28
- **Last Updated**: 2026-06-17

## What Problem This Skill Solves

Research materials are sufficient but the writing reads like an AI summary, lacking the author's analytical perspective and judgment framework. This skill turns "a pile of verified facts" into "an analysis that an unfamiliar reader can understand, remember, and retell."

**Applicable Boundary**: For readers without shared context, public distribution channels, clients, or external course audiences. For internal documents aimed at the user themselves, collaborators sharing context, or future AI agents, use `workflow_internal_writing.md`.

**Relationship with Deep Research Skill**: The deep research skill handles information collection and verification; this skill handles judgment synthesis and writing. Research points here when complete.

---

## Acceptance Criteria: What a Good External Article Looks Like

After writing, self-check against these criteria. These are outcome definitions, not process steps — how to get there is up to the agent.

1. **Has a thesis**: The article has a core judgment that a smart person unfamiliar with the details can retell in 1-2 sentences. Not "this is complex and worth paying attention to," but a specific judgment that can be agreed or disagreed with.

2. **Thesis up front**: After reading the first 25% of the article, the reader knows (a) what problem the article addresses, (b) what the author's judgment is, (c) what they'll gain by continuing. If any of these three questions requires reading past the halfway point to answer, the structure needs adjustment.

3. **Organized around the reader, not around the author's analytical framework**: The article advances along the reader's chain of questions (shock → fear/curiosity → relief → reality), not listing the author's analytical dimensions (categories like "combinatorial explosion + bypass"). Judgment criterion: if you read the article aloud to the target reader, would they think at any paragraph "what does this have to do with me?"

4. **Evidence economy**: Each argument uses one strongest case; do not pile up similar evidence. After the first case, the reader is already thinking "so what?" — if what follows is more of the same, their attention is already spent.

5. **Manageable cognitive load**: The reader receives no more than two new concepts in any single paragraph. New terms or frameworks are first grounded in scenarios the reader already knows, then given names.

6. **Clean prose**: Pass post-writing scans (em dashes, "very + adjective" judgment summaries, internal framework terminology leakage, large blocks of English quotes). See `rules/COMMUNICATION.md` for details.

7. **Informative subheadings**: Articles over 1500 words use `##`-level subheadings. Subheadings carry information, not category names — if you delete the subheading, can the first sentence of the body independently serve as a subheading? If yes, the subheading is merely a category name.

8. **Analytical framework invisible**: Thesis Catalog (L1-L6), axiom numbers, Phase names, terms like "narrative reconstruction" are scaffolding for the writing process and must not appear in the final article. The reader should feel they are reading someone with their own way of thinking doing analysis.

---

## Thesis Catalog: Inspiring Analytical Perspectives

The following perspectives are analytical habits distilled from the author's published articles, not frameworks that must be applied. They serve two purposes: helping you find the article's entry point ("what is the underlying mechanism here," "what dimension is the public overlooking"), and giving the article the author's judgment style rather than an AI summary flavor.

How many to use and which ones is entirely determined by the article. Many good articles don't explicitly use any of these perspectives — the author already has their own judgment. Treat these perspectives as an inspiration library, not a checklist: if a perspective naturally fits the current topic, use it; if not, ignore it. Don't force a framework just to "use an L." Perspectives guide how you think, but the reader only sees the result of that thinking.

L1-L3 share a common theme: diagnosing where AI system limitations come from (L1 diagnoses feedback loops, L2 diagnoses bottlenecks and cost structures, L3 diagnoses training priors). They often complement each other within the same article.

### L1: Feedback Loop Judgment

A system's capability ceiling depends on whether it can perceive its own output and self-correct. The most critical thing in an AI system is not model intelligence, but whether the model can see the consequences of its own actions. Systems with complete loops can self-iterate; systems with missing loops can only rely on human backfilling. This principle applies not only to system design but also defines the essence of learning: the ability to continuously calibrate direction matters more than the precision of a single aim.

**Corresponding axioms**: A02 (Amplifier), A04 (Reliability is a management problem), M01 (Closed-loop calibration)

**Typical Applications**: Three generations of creative AI evolution (Generation 1 cannot see rendering results, Generation 3 closes the loop via screenshots), Agentic AI deployment crises (code runs but no one knows if it's correct), closed-loop learning (open-loop vs closed-loop control theory applied to personal learning philosophy)

**Trigger Condition**: The analysis subject involves AI system reliability, degree of automation, or "why the demo is great but it doesn't work in practice"

### L2: Cost Structure Economics Reconstruction

When the cost of a key resource changes by orders of magnitude, systematically reconstruct the old economics and the new economics: why the old optimal strategy was rational under the old cost, and how the new optimal strategy differs. Not just saying "the bottleneck shifted," but a complete comparison of two sets of economics. Key insight: many practices we take pride in (DRY principle, intuitive decision-making, carefully designed defensive code) are not inherently correct, but rational products of the old cost structure — under the new cost structure they may become liabilities.

**Corresponding axioms**: X03 (Efficiency is determined by bottlenecks), T05 (Cognition is an asset, code is consumable)

**Typical Applications**: AI Native cost structure (code is expensive → reuse/DRY vs code approaches zero → disposable/use-and-discard), process determinism to outcome determinism (labor is expensive → careful design vs intelligence is cheap → spend tokens for certainty), Context infrastructure (model intelligence is the bottleneck → upgrade models vs context is the bottleneck → accumulate context)

**Trigger Condition**: When the analysis subject claims to "make X faster/cheaper/easier," ask why the old optimal strategy was rational and how the new optimal strategy differs

### L3: Consensus Ceiling Judgment

LLM default output is consensus. The training mechanism (next token prediction + RLHF safety alignment) determines that LLMs regress to the mean. Differentiation and depth come from injecting non-consensus personal context, not from switching to a better model. Deep Research is actually Wide Research. Primarily applicable to content creation and analysis quality topics.

**Corresponding axioms**: Core thesis of the context infrastructure blog, A10 (Familiarity trumps raw intelligence)

**Typical Applications**: Context infrastructure (comparative experiment of two reports), critique of Deep Research products

**Trigger Condition**: The analysis subject involves "can AI do X" capability boundary discussions, or any evaluation of AI output quality

### L4: Technology Lineage Tracing

No new release appears out of nowhere. Tracing its previous generations can locate its real position on the evolutionary trajectory, distinguishing "genuinely new" from "productization of an existing path." Typically divided into 2-4 generations, each solving the core problem left by the previous one. Primarily applicable to product reviews and technology release analysis.

**Corresponding axioms**: M06 (Connections surpass isolated knowledge), A13 (Three stages of technology adoption)

**Typical Applications**: Three generations of creative AI (script → protocol → closed loop), MCP evolution (research protocol → engineering reality collision → dialect fragmentation), GPT-5 positioning (o3/Gemini/Claude "personalities" unified through parameterization)

**Trigger Condition**: The analysis subject is a newly released product/technology/standard that needs positioning on the evolutionary trajectory

**Method**: Step 1, identify prior generations: what problem does this thing solve? How did people solve it before? What was the core limitation of the previous generation? Step 2, draw the generational evolution line: what each generation solved, what it left behind. Step 3, locate the current event on the evolution line: which generation's remaining problem does it solve? What will it itself leave behind? Step 4, predict the next step in evolution: based on current remaining problems, what might the next generation look like?

### L5: Surface Diagnosis and Underlying Mechanism

What you see on the surface is not what actually drives outcomes. The core work of the article is redirecting attention from the surface to the underlying mechanism. This "surface" can be media/vendor narratives ("AI can do design now"), anthropomorphic intuitions ("AI is slacking off"), or hidden premises embedded in success scenarios ("demo works = goal achieved"). The common structure: people stop at surface descriptions to make judgments, while what actually drives results is the underlying mechanism.

**Corresponding axioms**: T04 (Data trumps opinion), V02 (Verifiability is the foundation of trust)

**Typical Applications**: Almost every external article has this move. Creative AI (narrative focuses on "AI can do design," actual bottleneck is feedback loop), Wide Research ("slacking off" masks architectural constraints), AI Native cost structure ("intuition is a sign of expertise" is actually a forced compression strategy when observation cost is high)

**Trigger Condition**: Almost always needed. Ask yourself: about this topic, what is most people's first reaction? Is this first reaction looking at the surface or the mechanism? What technical essence does the anthropomorphic description mask?

**Method**: Step 1, extract the mainstream narrative or surface judgment. Step 2, identify which dimension it focuses attention on. Step 3, trace the underlying mechanism: what actually drives the results? Step 4, construct the redirect. Not every article needs to "refute" the mainstream narrative; sometimes it's "push one layer deeper."

### L6: Value Redistribution After Execution Friction Removal

When tools eliminate execution-level friction, competitive advantage shifts from "who executes faster" to "whose judgment is better." The value of tool mastery decreases; the value of taste and directional sense increases. In specific articles, this judgment typically appears as role repositioning — not just abstractly saying "judgment is more important," but depicting the human's concrete role in the new system. Three common variants: IC→Manager (management type, from hands-on to designing processes for the system to self-iterate), User→Builder (tool usage type, from passive invocation to actively building and improving tools), Question-setter vs Executor (workflow type, human's core value shifts from "doing" to "defining what to do and judging whether it's done well").

**Corresponding axioms**: T05 (Cognition is an asset), A02 (AI is an amplifier, not a replacement)

**Typical Applications**: Creative AI (human shifts from creator to boundary designer/feedback interpreter), Wide Research (Senior Manager perspective designing processes), Deep Research (division of labor: AI data mining + human cognitive alchemy)

**Trigger Condition**: When the analysis subject involves "AI makes a certain type of work easier," ask where value has shifted to, and what the human's new role concretely looks like

### L7: Management Framework Translation

Problems encountered in AI usage are often not AI-specific new problems, but problems already solved in human organizational management. Treat AI as a team member to manage, and you can invoke mature management frameworks (hiring/delegation/training/coaching/acceptance) for ready-made solutions. "There is nothing new under the sun" — AI's unreliability, hallucinations, slacking off, communication costs all have corresponding classic management problems and solutions in human organizations. The power of this perspective: it transforms the anxiety of "AI is entirely new and needs entirely new methodology" into the pragmatic sense of "we actually already know how to do this."

**Corresponding axioms**: A03 (IC→Manager), A04 (Reliability is a management problem)

**Typical Applications**: AI Management Trilogy (don't grab the keyboard / visualize context / teach to fish, each mapping to classic management), AI Key Decisions (manager designs processes for AI to self-iterate rather than following up on every work item), AI Management 2 ("AI is unreliable" maps to "new hires are unreliable," solution is situational leadership and hierarchical scaling)

**Trigger Condition**: The analysis subject involves reliability, efficiency, or collaboration quality issues in AI usage, and these problems have mature counterparts in human organizational management

### L8: Context and Information Architecture

A system's capability boundaries and failure modes depend on "what it can see" — what information is in the context, whether the information is clean, whether information is isolated across different roles. The first step in analyzing any LLM system is to reverse-engineer what is actually in its context window. This complements L1: L1 addresses "can it perceive and correct" (action layer), L8 addresses "what is the information basis for perception" (information layer). When AI behavior goes wrong, first ask "what information did it see" before asking "is its reasoning correct."

**Corresponding axioms**: M01 (Closed-loop calibration), core thesis of the context infrastructure blog

**Typical Applications**: Multi-agent redesign (role splitting, document communication, Planner selection all derived from context window management), Context infrastructure (after model intelligence crosses the threshold, context density becomes the bottleneck), AI Software Engineering (radical transparency = giving AI enough feedback information to self-correct)

**Trigger Condition**: The analysis subject involves LLM system failure modes, capability boundaries, or "why the same model performs so differently in different scenarios." Also applicable to information architecture decisions when designing AI systems (which information goes into context, which is externalized to files, which is isolated to different agents)

---

## From Materials to Thesis

The following are usable analytical tools for going from research materials to a writable thesis. Not a pipeline — if the user has already provided a thesis (e.g., from a discussion or a clear viewpoint), skip the discovery process and go directly to writing. Only use these tools when the thesis needs to be discovered from materials.

**Perspective Matching**: Scan the Thesis Catalog (L1-L6), annotate which are strongly relevant, auxiliary, or irrelevant to the current topic. An article typically uses 1-3 perspectives.

**Search Author's Existing Writing**: Search `contexts/blog/`, `contexts/survey_sessions/`, `rules/axioms/` for existing articles, research, and axioms directly related to the topic. If the user mentioned their own related thoughts or existing articles in the conversation, these are the strongest anchors for the thesis.

**Technology Lineage Tracing** (when L4 is strongly relevant): Identify 2-4 predecessor generations, draw the evolution line, locate the current event.

**Narrative Reconstruction** (when L5 is strongly relevant): Extract mainstream narrative → identify the dimension the narrative focuses on → identify the overlooked dimension → construct the redirect.

**Output**: thesis statement (2-3 sentences, understandable by a smart person unfamiliar with the details, containing specific judgment) + argument skeleton (3-5 points, each annotated with which perspective and which evidence was used). Write to `tmp/<session_slug>/scratchpad.md`.

---

## Writing Principles

Must read `rules/COMMUNICATION.md` before writing. Not reading it afterward for a checklist comparison — load the rules in before writing. The following only repeats the items AI most frequently gets wrong in long-form writing; complete rules are in COMMUNICATION.md.

### Structure: Organize Around the Reader

**Thesis up front and evidence economy**. Article structure is designed around the reader's psychological progression: hook (a phenomenon the reader can perceive) → how this relates to you → core thesis (1-2 sentences) → evidence (one strongest case per argument) → solution → constraints. Don't spend multiple sections proving the same argument. Don't organize by the author's analytical framework ("Dimension 1 + Dimension 2"); organize by the reader's chain of questions. Judgment criterion: would the reader think at any paragraph "what does this have to do with me?"

**Subheadings**. Articles over 1500 words use `##`-level subheadings. Subheadings carry information, not category names — "Why command-line filtering fails" is a category name; "Combinatorial explosion: shell syntax has infinitely many equivalent expressions" carries information. 3-5 subheadings, each with 2-4 paragraphs underneath.

**Title strategy**. The title is the article's only entry point in the information stream. Event-driven pieces must include specific event keywords (product name, company name, action word). Analytical pieces can start from judgment or tension but must still give a concrete subject. Judgment criterion: read the title to someone who follows AI but hasn't heard of this event — if they ask "what is this," the title has failed.

**Article weight calibration**. Different articles have different weights, corresponding to different minimum requirements. Quick commentary (800-1500 words, single viewpoint): no images needed, 1-2 cases sufficient, thesis can come from user-provided viewpoint. Analysis (1500-3000 words): subheadings needed, 3-5 argument points, images recommended. Deep research (3000+ words): full Phase process, images required, complete evidence chain. Before writing, determine which tier this falls into and adjust investment accordingly.

### Cognitive Load

No more than two new concepts per paragraph. New terms are first grounded in scenarios or sensations the reader already knows, then given names. When using metaphors, introduce only one core concept per paragraph, advance with multiple short paragraphs (no more than 3 sentences each), don't cram scene + problem + solution + insight four layers into one paragraph. When the target reader is not a domain expert, that domain's jargon does not appear by default; when it must be introduced, use references the reader already knows as anchors.

### Prose Rules (High-Risk Items for Long-Form Writing)

The following items are where AI repeatedly makes mistakes in long-form writing, even after reading COMMUNICATION.md, so they are repeated here. Complete rules are in COMMUNICATION.md.

**Zero tolerance for em dashes**. No —— may appear in the final piece. Break insertions into two sentences; replace causal dashes with periods or colons; break double-dash parentheticals into independent sentences.

**"Very + adjective" judgment summaries**. Do not write "demonstrated very directly," "explained very clearly," "results are very clear." This pattern uses one adjective to skip the burden of argument. After writing, scan with `rg 'very[direct clear simple obvious important thorough comprehensive deep key]'` (in the target language equivalent); delete all judgment summaries or replace with specific content.

**English quote handling**. Large blocks of English quotes in Chinese articles (blockquotes exceeding one full sentence) should be restated in Chinese, preserving core meaning and URL. Chinese readers face high cognitive cost with large English blocks: need to switch languages, parse grammar, then return to Chinese context. Short English phrases (product names, key terms) can be kept inline. English-language articles are not subject to this restriction.

**Zero tolerance for meta-commentary**. Do not write "specifically," "here's a key distinction," "let's look at." Enter the content directly.

**Transition words**. Use light transitions between paragraphs (this way, however, in other words, the key is) to maintain rhythm; don't make every sentence land like an independent brick.

**Do not wrap conceptual terms in quotation marks** (unless absolutely ambiguous).

### Format

- Chinese Markdown; all citations use absolute `https://` links inline in the body
- Do not separately list "Sources" or "References" at the end
- Do not write publication date or research date at the beginning of the body (injected by the system at publish time)
- Survey reports (default output) stored in `contexts/survey_sessions/`, no Pelican frontmatter. Blog posts stored in `contexts/blog/content/` with frontmatter.
- External-facing articles have 0-3 images. Data comparisons and flowcharts must have images; pure text analysis articles can skip. Images placed in the same directory as the MD, referenced with relative paths. Quantitative charts use matplotlib; process/concept diagrams use gpt-image-2. When GPT redraws content containing Chinese, reduce text density, 16:9 landscape, require normal-width unstretched fonts.

---

## Model Division of Labor Protocol

The final writing of external-facing articles defaults to strong writing models.

When the main thread model is an Opus series or DeepSeek series (including Flash, Pro, V4, and all variants), the main thread writes directly. Otherwise, the main thread must not directly draft the final piece; it must first write research materials, thesis, evidence table, style requirements, prohibitions, target output path, and overwrite strategy to `tmp/<session_slug>/`, then invoke a DeepSeek V4 Flash sub-agent to read these files and write the final Markdown. Agents must not rely on chat to pass body materials; files are the handoff interface. Judge by model ID.

The main thread is responsible for: preparing materials, fact-checking, style review, and final acceptance. Do not deliver unchecked sub-agent drafts directly. Delegate execution; keep accountability with yourself.

When the user requests rewriting or overwriting the final file, the deliverable under `contexts/survey_sessions/` can be overwritten; but raw materials under `tmp/<session_slug>/` (source index, scratchpad, handoff brief, etc.) must be preserved as the audit chain.

---

## Revision Process

After receiving feedback, first diagnose the feedback type before acting.

**Structural issues** ("I don't know what you're talking about," "I didn't understand after the first two sections," "what does this have to do with me"): don't need to fix sentences; need to reorganize the article. First determine the reader's question chain (the reader's psychological state at each paragraph), then reorder around it. Structural feedback is the most important signal — it indicates the article's organizational logic doesn't match the reader's cognitive path.

**Style issues** ("this sentence feels off," "this reads like translationese"): fix in place without affecting structure.

**Factual issues** ("this number is wrong," "this case description is inaccurate"): verify sources, correct, then re-validate related arguments.

---

## Post-Writing Quality Checks

After writing, must execute the following scans; do not rely on naked-eye review:

```bash
# 1. Em dashes
rg -n '——' <file>

# 2. "Very + adjective" judgment summaries
rg 'very[direct clear simple obvious important thorough comprehensive deep key]' <file>

# 3. Internal framework terminology leakage
rg 'L[0-6]|axiom|Phase [A-Z]|narrative reconstruction|technology lineage|bottleneck shift|Thesis Catalog' <file>
```

All three scans must return empty results. Check each hit location one by one; fix and re-scan.

After writing, also do a round of qualitative self-check (against the 8 acceptance criteria).

---

## Common Failure Modes

| Failure Mode | Symptom | Solution |
|-------------|---------|----------|
| Research summary instead of authorial writing | Reads like "AI searched around and wrote a summary" | No thesis formed. Go back to perspective matching and narrative reconstruction |
| Organized around author's framework, not reader's questions | Article lists "Dimension 1 + Dimension 2"; reader thinks "what does this have to do with me" at some paragraph | Reorganize as reader's fear/curiosity chain. Each case first answers "why is this relevant to the reader" |
| Evidence piling | Multiple sections proving the same argument; reader thinks "so what" after the first case | One strongest case per argument. Thesis up front: reader must know the problem, judgment, and expected takeaway in the first quarter |
| Relevance not landing | Reader doesn't know "what this has to do with me" after the first few paragraphs | The second paragraph of the opening must connect the analysis subject to the reader's situation |
| Opening starts from technical concepts | The first paragraph makes non-domain people frown | Switch to a sensory phenomenon the reader can directly perceive |
| Temporal dimension ambiguity | Simultaneously implying "important now" and "still very early" | Temporal dimension judgment must be explicitly expressed in the opening |
| Object-explainer | Always explaining from the analysis object's perspective, never judging from the reader's situation | Change the subject from the analysis object to "you (the reader)" |
| Internal framework leaking into final piece | "From the L4 technology lineage perspective," axiom numbers appear in the article | Scaffolding terms have zero appearance in the final article |
| Cognitive burden too high | Multiple consecutive paragraphs introduce new concepts; reader zones out or scrolls back | No more than two new concepts per paragraph; ground in known scenarios first, then give names |
| Em dash proliferation | Heavy use of —— throughout | Zero tolerance in final piece. One-time scan with `rg -n '——'` after writing |
| Large blocks of English quotes | Pasting multi-sentence English blockquotes in Chinese articles | Restate in Chinese, preserving core meaning and URL |
| "Very + adjective" judgment summaries | "demonstrated very directly," "explained very clearly" | Scan with `rg`; delete all judgment summaries or replace with specific content |
| Meta-commentary as transitions | "Specifically," "the key distinction is" | Enter content directly. If deleting it breaks coherence, the previous sentence wasn't clear enough |
| Complex metaphor cognitive overload | One paragraph crams scene + problem + solution + insight | One metaphor paragraph pushes only one concept; no more than 3 sentences per paragraph |
| No images (analysis/research type) | Pure text long article | Data charts and flowcharts must have images; analysis-type articles can skip images |
| Duplicate publication date | Date written in body, injected again on publish page | Do not write publication date in body |

---

## Delivery Endpoint

Writing the final MD file is the delivery endpoint. Do not automatically execute publishing workflows (yage share, blog, Twitter, Circle, etc.). Only execute per the corresponding skill when the user explicitly requests it.
