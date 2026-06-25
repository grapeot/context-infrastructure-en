# External Writing Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Transforming research materials into judgment-driven external-facing analysis articles, public survey reports, or course/client content for external readers
- **Prerequisites**: Output of Phase 1-3 of the Deep Research Survey Workflow (`workflow_deep_research_survey.md`), or equivalent verified materials
- **Created**: 2026-04-28
- **Last Updated**: 2026-06-22

## What Problem This Skill Solves

Research materials are sufficient but the writing reads like an AI summary, lacking the author's analytical perspective and judgment framework. This skill turns "a pile of verified facts" into "an analysis that an unfamiliar reader can understand, remember, and retell."

**Applicable Boundary**: For readers without shared context, public distribution channels, clients, or external course audiences. For internal documents aimed at the user themselves, collaborators sharing context, or future AI agents, use `workflow_internal_writing.md`.

**Output Type Judgment (must do before writing)**: The **default output for external-facing analysis is a survey report**, stored in `contexts/survey_sessions/`, without Pelican frontmatter and without Kit subscription scripts. Only when the user explicitly says "write a blog post" or "publish to blog" should it be treated as a blog, stored in `contexts/blog/content/` with frontmatter. "Write an article" does not equal blog; default to survey report. Wrong judgment pollutes frontmatter, misplaces storage, and skews image strategy.

**Relationship with Deep Research Skill**: The deep research skill handles information collection and verification; this skill handles judgment synthesis and writing. Research points here when complete.

---

## Acceptance Criteria: What a Good External Article Looks Like

After writing, self-check against these criteria. These are outcome definitions, not process steps.

**Criterion 1 is a gating constraint — if it's not met, send it back for rewrite. All other items are optimizations discussed only after it's satisfied.**

1. **A non-expert can understand and retell the thesis**: Find someone not working in this field and read the article aloud to them. Can they retell what the article is about in one or two sentences afterward? If they start frowning or zoning out at a particular section, that section has an information density or background assumption problem. This is the hardest criterion of all — not "is the writing smooth," but "did the reader actually understand." The most common AI writing failure is not a sentence problem; it's assuming the reader already knows SFT, RLHF, zero trust, bond spreads, and then pushing to the next concept before the reader has digested the previous one. **If this isn't met, don't bother checking the items below.**

2. **Has a thesis**: The article has a core judgment that a smart person unfamiliar with the details can retell in 1-2 sentences. Not "this is complex and worth paying attention to," but a specific judgment that can be agreed or disagreed with.

3. **Thesis up front**: After reading the first 25% of the article, the reader knows (a) what problem the article addresses, (b) what the author's judgment is, (c) what they'll gain by continuing. If any of these three questions requires reading past the halfway point to answer, the structure needs adjustment.

4. **Organized around the reader, not around the author's analytical framework**: The article advances along the reader's chain of questions (shock → fear/curiosity → relief → reality), not listing the author's analytical dimensions (categories like "combinatorial explosion + bypass"). Judgment criterion: if you read the article aloud to the target reader, would they think at any paragraph "what does this have to do with me?"

5. **Evidence economy**: Each argument uses one strongest case; do not pile up similar evidence. After the first case, the reader is already thinking "so what?" — if what follows is more of the same, their attention is already spent.

6. **Clean prose**: Pass post-writing scans (em dashes, "very + adjective" judgment summaries, internal framework terminology leakage, large blocks of English quotes). See `rules/COMMUNICATION.md` for details.

7. **Informative subheadings**: Articles over 1500 words use `##`-level subheadings. Subheadings carry information, not category names — if you delete the subheading, can the first sentence of the body independently serve as a subheading? If yes, the subheading is merely a category name.

8. **Analytical framework invisible**: Thesis Catalog (L1-L8), axiom numbers, Phase names, terms like "narrative reconstruction" are scaffolding for the writing process and must not appear in the final article. The reader should feel they are reading someone with their own way of thinking doing analysis.

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

**Article weight calibration**. Default target length is 2500-3500 words, no longer split into quick commentary / analysis / deep research tiers. This length corresponds to: complete Phase research process, complete evidence chain, 3-5 argument points with subheadings, argumentation density sufficient to support the thesis without compressing into a checklist. Images as needed; deep research type must have them, analysis type can skip. Short pieces (1500-2000 words) are written only when the user explicitly requests, and must clearly state "this one is short because X"; don't default to writing short. "Low cognitive burden" does not equal short — it equals the reader following a natural storyline without feeling force-fed. How long an article should be depends on the breathing room the argumentation needs, not a fixed word budget. **Exception**: when cognitive burden is the primary tension (reader says "I don't understand"), cutting content is more effective than rewriting, even if it ends up shorter than the default length. A 3000-word article the reader can understand is far more valuable than a 7000-word article the reader only grasps a third of.

### Cognitive Load

The goal of low cognitive burden is correct, but it's repeatedly misunderstood in AI writing. Mechanically applying rules — forcing short sentences, forcing short paragraphs, inserting a transition word every two paragraphs, replacing "three things" with "first thing / second thing / third thing" — does not reduce cognitive burden. It turns a flowing article into a dismembered checklist. What the reader gets is not an article but items肢解 by rules.

The only way to truly reduce cognitive burden is: let the reader follow a natural storyline, finishing without feeling force-fed. The following are specific techniques, confirmed effective from the pattern of rewriting the same article repeatedly to the fifth version.

**No taxonomy announcements.** "First thing / second thing / third thing," "there are several directions," "three things" — this kind of pre-announced numbering signals "what follows is a checklist," and the reader's attention shifts from following along to counting which number we're on. Let the content surface on its own. If three things have a sequential relationship, the narrative itself brings out the order; if they're merely parallel, that means you're listing rather than writing. Test: can the article stand on its own after deleting all the numbers? If yes, the numbering is redundant preamble.

**No mechanical connectives.** "However," "this way," "in other words," "then again" appear only when the reading rhythm needs breathing. When the paragraph itself flows, add none. Repeatedly writing multiple versions of the same article most easily exposes this problem: the mechanical connectives inserted in the previous version, when mostly deleted, the rhythm turns out better. Test: read aloud. If connectives appear like a template every two paragraphs, that's a machine filling slots. If a paragraph reads smoothly without stumbling, no need to force them.

**No information walls.** Don't cram five or six data points into a single paragraph. The role of data in an article is not to be listed, but to push the narrative one step forward. Before placing each data point, ask: what is it helping the reader understand? If the answer is just "it's here," move it to its own paragraph, or merge it into the narrative action currently advancing. Data is embedded in the story, not in a "number → meaning" Q&A pattern.

**Paragraphs have natural length.** When telling a complete mini-story, let it be long; when delivering a punchline, let it be short. Don't force any length. If you notice every paragraph is three to four lines with completely uniform rhythm, that means you're applying a template.

**Read aloud once.** The final check after writing is not a checklist scan, but reading the article aloud. Does it sound like someone talking? Like telling a friend something interesting, or like reading a work report? This test is more reliable than any rule — when reading aloud, you don't count "how many new concepts in this paragraph," you just feel whether the rhythm is right.

The above addresses narrative-level cognitive burden. Concept-level cognitive burden (no more than two new concepts per paragraph, ground new terms in known scenarios first, jargon doesn't appear by default) still applies, but it addresses "can the reader keep up," while the narrative level addresses "does the reader want to keep reading." Both are necessary.

### Methods for Reducing Cognitive Burden (Information Architecture Level)

The sentence patterns and rhythm discussed above are the micro level. In practice, the most common reason readers say "I don't understand" is not sentence-level, but macro information architecture: an article crams in too many angles, too many terms, too many cases. The following are operational methods confirmed effective from the process of repeatedly rewriting the same article until the reader said "a qualitative leap."

**One section holds only one core judgment + one concrete story.** This is the single most powerful operation for reducing cognitive burden. Assume your article has three angles; for each angle, keep only the anchor that best illustrates the point — one company did a certain thing, or one person said a certain sentence. Cut or compress all other numbers, quotes, and cases to half a sentence. Judgment criterion: after reading a section, can the reader summarize "what this section is about" in one sentence? If they can't summarize it themselves, the section is stuffed with too much.

**Cutting is more important than adding.** AI's (especially sub-agents like DeepSeek) default behavior is to use as much research material as possible, because more material seems "more thorough." But the goal of an external-facing article is not to display research to the reader, but to convey judgment. When you find an article has excessive cognitive burden, the first reaction should not be "how to rewrite more accessibly," but "what can be cut." A 7000-word article cut to 3000 words where the reader says "a qualitative leap" — what was cut was not filler, but interesting but unnecessary arguments, interesting but unnecessary cases, accurate but unnecessary terminology.

What specifically to cut: the second case of the same type (keeping the strongest one is enough), supporting quotes (keeping the core judgment is enough, not every sentence's source), intermediate analysis steps (keeping the start and conclusion is enough, not every step of the reasoning chain), precise definitions of terminology (replace with everyday scenarios, not academic definitions).

**The reader's existing knowledge is the entry point.** The first paragraph must start from something the reader already knows or can intuitively grasp. "OpenAI spent $34 billion last year" — anyone can grasp that. "Three signal chains" or "the paradigm shift from model safety to agent security" — only domain insiders can grasp that. The former is an entry point; the latter is not. If the article must introduce a new concept, first ground it in a scenario the reader already has, then give it a name. "The internet bubble lost shareholders' money; the AI bubble loses creditors' money" — this is a contrast the reader can intuitively understand, far stronger than "differences in loss transmission mechanisms."

**Professional terminology: delete or translate.** "Bond spreads widened" becomes "companies that already struggle to borrow are finding it even more expensive." "Unit economics" becomes "for every dollar earned, two dollars and sixty cents are spent." "Stranded assets" becomes "things built but unable to make money." If deleting a term doesn't affect the argument, delete it. If it can't be deleted, immediately follow with an everyday-language restatement. The reader doesn't need to learn your terminology; you need to learn to speak in the reader's language.

### Prose Rules (High-Risk Items for Long-Form Writing)

The following items are where AI repeatedly makes mistakes in long-form writing, even after reading COMMUNICATION.md, so they are repeated here. Complete rules are in COMMUNICATION.md.

**Zero tolerance for em dashes**. No —— may appear in the final piece. Break insertions into two sentences; replace causal dashes with periods or colons; break double-dash parentheticals into independent sentences.

**"Very + adjective" judgment summaries**. Do not write "demonstrated very directly," "explained very clearly," "results are very clear." This pattern uses one adjective to skip the burden of argument. After writing, scan with `rg 'very[direct clear simple obvious important thorough comprehensive deep key]'` (in the target language equivalent); delete all judgment summaries or replace with specific content.

**English quote handling**. English quotes in Chinese articles are judged by content density, not by number of sentences. Blockquotes exceeding 20 English words, or single sentences containing 3 or more key information points (numbers, proper nouns, clauses), should be restated in Chinese, preserving the URL. Short English (≤20 words, single information point) as an iconic quote can be kept as a blockquote. Inline short English (product names, terms, ≤15-word quotes) can be kept. Chinese readers face high cognitive cost with large English blocks: need to switch languages, parse grammar, then return to Chinese context. English-language articles are not subject to this restriction.

**Zero tolerance for meta-commentary**. Do not write "specifically," "here's a key distinction," "let's look at." Enter the content directly.

**Transition words**. Use light transitions between paragraphs (this way, however, in other words, the key is) to maintain rhythm; don't make every sentence land like an independent brick. But also be alert to mechanical insertion: connectives that are too dense, appearing at fixed template intervals, also break rhythm. Judge by reading aloud, not by counting.

**Do not wrap conceptual terms in quotation marks** (unless absolutely ambiguous).

### Format

- Chinese Markdown; all citations use absolute `https://` links inline in the body
- Do not separately list "Sources" or "References" at the end
- Do not write publication date or research date at the beginning of the body (injected by the system at publish time)
- Survey reports (default output) stored in `contexts/survey_sessions/`, no Pelican frontmatter. Blog posts stored in `contexts/blog/content/` with frontmatter.
- External-facing articles have 0-3 images. Data comparisons and flowcharts must have images; pure text analysis articles can skip. Images placed in the same directory as the MD, referenced with relative paths. Images default to a two-step process: first generate a structural draft with matplotlib (with text annotations, layout, positioning), then use gpt-image-2 to redraw with the draft as `-i` input for visual optimization. matplotlib-only is only for precise quantitative charts (bar charts, line charts, scatter plots). Concept diagrams, flowcharts, comparison diagrams, and stack diagrams all go through the two-step process. gpt-image-2 redraw timeout set to 300s+, reduce text density when containing Chinese, 16:9 landscape, require normal-width unstretched fonts. See `generate_image.md` for detailed operations.

---

## Model Division of Labor Protocol

The final prose of external-facing articles is completed through two writing passes using different model families. The main thread is responsible for research, judgment, material organization, fact-checking, style review, and final acceptance; writing sub-agents are responsible for turning finalized judgment into prose.

**Standard delivery must include two writing passes:**

| Pass | Sub-agent | `subagent_type` | Output file | Responsibility |
|------|-----------|-----------------|-------------|----------------|
| Pass 1: Draft | DeepSeek Pro | `writer_deepseek` | `tmp/<session_slug>/draft.md` | Read `writing_brief.md` and organize thesis, evidence, structure, and style constraints into a complete article |
| Pass 2: Language rewrite | Gemini 3.5 Flash | `gemini_3.5_flash` | `tmp/<session_slug>/rewrite.md` | Keep structure, facts, and URLs unchanged; rewrite the prose from scratch in Gemini's own language |

Unless the user explicitly requests only a draft, only an outline, or only an internal temporary memo, do not deliver the first-pass draft as the final piece.

**Why the second pass uses a different model family.** The biggest failure mode in language-layer rewriting is synonym substitution: when the same model or same model family rewrites its own draft, it tends to preserve the original sentence skeleton and swap words. Having Gemini rewrite a DeepSeek draft structurally breaks that inertia. The two model families have different language registers, sentence preferences, and rhythms, forcing Gemini to reorganize sentences instead of locally editing them. In testing, Gemini 3.5 Flash produced more natural rhythm and prose for this language-only pass; Flash is fast and cheap, which matches the job because it does not carry the reasoning burden.

**Both handoffs are file-based, not chat-based.** The main thread must not directly draft the final prose. It first writes research materials, thesis, evidence table, style requirements, prohibitions, target output path, and overwrite strategy to `tmp/<session_slug>/writing_brief.md`, then invokes `writer_deepseek` to read that file and write the first-pass Markdown. The second pass receives the first-pass draft path and must write a new file, not overwrite the original. Agents must not rely on chat to pass body materials; files are the handoff interface.

**Structural judgment for cognitive burden reduction is done by the main thread; writing sub-agents do not change structure.** The main thread first determines article structure, information selection, and reader cognitive path, then lets writing sub-agents handle language inside those constraints. If the reader says "I don't understand," the main thread should first reorganize structure and cut information, then rerun writing. Do not outsource structural judgment to writing sub-agents.

**Main-thread acceptance is the quality gate.** If the Gemini rewrite has more than 30% paragraph-level sentence similarity with the draft, treat it as synonym substitution rather than a true rewrite. Give `gemini_3.5_flash` clearer rhythm and sentence-level instructions and rerun; if it still fails, fall back to `writer_deepseek` for the second pass. Only after acceptance should the rewrite enter post-writing scans. Do not deliver unchecked sub-agent drafts or rewrites directly. Delegate execution; keep accountability with yourself.

When the user requests rewriting or overwriting the final file, the deliverable under `contexts/survey_sessions/` can be overwritten; but raw materials under `tmp/<session_slug>/` (source index, scratchpad, handoff brief, etc.) must be preserved as the audit chain.

---

## Revision Process

After receiving feedback, first diagnose the feedback type before acting.

**Structural issues** ("I don't know what you're talking about," "I didn't understand after the first two sections," "what does this have to do with me"): don't need to fix sentences; need to reorganize the article. First determine the reader's question chain (the reader's psychological state at each paragraph), then reorder around it. Structural feedback is the most important signal — it indicates the article's organizational logic doesn't match the reader's cognitive path.

**Style issues** ("this sentence feels off," "this reads like translationese"): fix in place without affecting structure.

**Factual issues** ("this number is wrong," "this case description is inaccurate"): verify sources, correct, then re-validate related arguments.

---

## Second-Pass Writing: Language-Layer Rewrite

After content and structure are finalized, and before post-writing self-check, must execute the second-pass writing: **language-layer rewrite**. This pass does not change structure, content, information volume, URLs, or facts. It only rewrites the entire article's prose from scratch using the rewriter's own language habits.

This is not optional polishing, nor is it a fix done only when style issues are discovered. The standard workflow for external-facing articles is: complete the first-pass draft, then complete the second-pass language rewrite, then enter post-writing scans. The first-pass draft is a draft; the second-pass rewrite is the final candidate.

Why this pass is needed: by this point the article's structure, thesis, and evidence are all settled, but the prose layer often retains the sentence-pattern inertia of the original author (main thread or first-pass sub-agent), including translationese, flat rhythm, missing transitions, conceptual terms wrapped in quotation marks, "very + adjective" judgment summaries, and em-dash emotional pauses. Post-writing scans only catch explicit violations, not rhythm and language feel. A fresh writing brain, without the inertia of the first draft, can rewrite in more natural language.

**Execution method**: Invoke a `gemini_3.5_flash` sub-agent, give it the first-pass draft MD path, and require it to output a completely new file: `tmp/<session_slug>/rewrite.md`. Do not overwrite the original. After the main thread accepts, copy or apply the rewrite to the final delivery path.

**Hard constraints for the rewriter**:

1. **Do not change structure**: section order, subheadings, paragraph count, and paragraph correspondence remain consistent.
2. **Do not change content**: thesis, judgments, cases, numbers, URLs, and quotes are all preserved.
3. **Do not change information volume**: the information density conveyed per paragraph does not change; do not add or remove arguments.
4. **Build from scratch, not sentence-by-sentence editing**: You are not editing words on the original; you are reading it, closing the original, and writing the same content from scratch in your own language. The original's role is to tell you "what information this paragraph needs to convey, which URLs to cite," not to give you a template for synonym replacement. You may change subjects, transitions, merge short sentences, split long sentences, reorder clauses, and reorganize the argumentation order within a paragraph. Judgment criterion: comparing the rewrite and the original paragraph by paragraph, no paragraph should have more than 30% sentence similarity. If it exceeds that, it means you're copying original sentences rather than rewriting, and you need to start over.
5. **Follow COMMUNICATION.md for style**: the rewriter must read COMMUNICATION.md before writing, loading the rules in before starting.

**Main thread acceptance**: After the rewrite is complete, the main thread compares it with the original paragraph by paragraph, checking three things: (a) structural integrity — section order, subheadings, paragraph count are consistent; (b) content integrity — all thesis, judgments, numbers, URLs are preserved; (c) language rewrite degree — check sentence similarity paragraph by paragraph; any paragraph exceeding 30% sentence similarity is judged as incomplete rewriting and must be redone. Only after acceptance does the rewrite enter the post-writing self-check phase. The original is preserved as the audit chain. When replying to the user, if the second-pass rewrite has not been completed, you must explicitly state that the deliverable is still the first-pass draft and cannot be called the final piece.

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

# 4. Long English blockquotes (blockquote lines over 100 chars need manual check for >20 words or >3 information points)
rg -n '^> ' <file> | awk '{ if (length($0) > 100) print }'

# 5. Evaluative leads before quotes/facts (meta-commentary variants)
rg -n 'says .{0,5} more|straightforward to|no need to restate|in itself shows|in itself is a bit|easy to miss|no need for reasoning' <file>

# 6. Passive voice (translationese disaster zone; passive voice is low-frequency and emphatic in Chinese)
rg -n '被' <file>
```

The first five scans must all return empty results (#4 hits need manual judgment). #6 will not be empty; classify each one: which are translationese that must be rewritten, which are natural Chinese usage that can be kept.

**#6 Judgment criteria**: Translationese loves to abuse passive voice, directly calquing English "is being Xed" / "X was done to Y." In Chinese, most cases should use active subjects or topic-comment structure. Check each passive construction:

- **Almost always translationese, must rewrite**: "正在被 X" / "在被 X" (being commoditized, being compressed); "被 + 持续/系统/整个/同时 + verb" (being continuously squeezed out, being systematically trained, being entirely deleted, being simultaneously compressed); "被 X 掉/被 X 出去" (was deleted, was squeezed out, was short-circuited, was dismantled). Rewrite approach: switch to active subject or natural Chinese. "执行正在被商品化" → "执行正在变成商品"; "环节正在被压缩" → "环节正在缩水"; "这个问题被删掉了" → "这个问题直接消失了"; "过滤器被拆了" → "AI 把过滤器拆了".
- **Natural usage that can be kept**: 被替代 (replaced), 被贴上标签 (labeled), 被工具取代 (replaced by tools), 被训练成 (trained as), 被要求 (required), 被骗 (deceived). These are acceptable passive constructions in Chinese, describing a subject genuinely receiving an unfavorable or directed action.
- **Quick test**: delete the "被" character; if the sentence still reads smoothly, the "被" is redundant translation flavor; read aloud, and if the subject is passively acted upon by some abstract process and reads like a translation, change it to active.

**Special note**: When fixing "not X, but Y" contrastive frames, do not use "没有被……，它被……" (negation + passive) as a replacement — that's trading one translationese for another, usually worse (double passive stacking negation then affirmation). Just rewrite into natural active Chinese.

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
| Cognitive burden too high | Multiple consecutive paragraphs introduce new concepts, reader zones out; or taxonomy announcements (first/second/third), mechanical connectives, information walls that chop the article into a checklist, reading feels like being force-fed | No more than two new concepts per paragraph; ban taxonomy announcements, mechanical connectives, information walls; embed data in stories rather than listing; read aloud to test rhythm |
| Em dash proliferation | Heavy use of —— throughout | Zero tolerance in final piece. One-time scan with `rg -n '——'` after writing |
| Large blocks of English quotes | Pasting multi-sentence English blockquotes in Chinese articles | Restate in Chinese, preserving core meaning and URL |
| "Very + adjective" judgment summaries | "demonstrated very directly," "explained very clearly" | Scan with `rg`; delete all judgment summaries or replace with specific content |
| Meta-commentary as transitions | "Specifically," "the key distinction is" | Enter content directly. If deleting it breaks coherence, the previous sentence wasn't clear enough |
| Complex metaphor cognitive overload | One paragraph crams scene + problem + solution + insight | One metaphor paragraph pushes only one concept; no more than 3 sentences per paragraph |
| Information-architecture-level cognitive overload | Reader says "I don't understand" or "I only understood a small part," but sentence-by-sentence inspection shows no obvious grammar problems | Root cause is not sentence patterns but information density: one section crams multiple concepts or multiple cases. The solution is to cut content, not to rewrite — keep only one core judgment + one concrete story per section. See "Methods for Reducing Cognitive Burden" section |
| Sub-agent rewrite becomes synonym replacement | After second-pass language-layer rewrite, paragraph-by-paragraph comparison shows heavy sentence similarity (over 30%) | `gemini_3.5_flash` must execute complete rewrite per "build from scratch." Main thread checks similarity paragraph by paragraph during acceptance; if threshold exceeded, require that paragraph or the entire piece to be redone. If the problem comes from structure or information density, the main thread first reorganizes structure and cuts content, then re-hands to the rewriting sub-agent |
| No images (analysis/research type) | Pure text long article | Data charts and flowcharts must have images; analysis-type articles can skip images |
| Duplicate publication date | Date written in body, injected again on publish page | Do not write publication date in body |

---

## Delivery Endpoint

Writing the final MD file is the delivery endpoint. Do not automatically execute publishing workflows (yage share, blog, Twitter, Circle, etc.). Only execute per the corresponding skill when the user explicitly requests it.
