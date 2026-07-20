# External Writing and Drafting Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: Turning verified research into an external-facing analysis, public survey report, or course/client material.
- **Prerequisites**: Phase 1-3 output from the [Deep Research Survey Workflow](./workflow_deep_research_survey.md), or equivalent verified material.
- **Last updated**: 2026-07-20

## 1. Goal and Output Route

This skill addresses the case where the material is sufficient but the article still reads like an AI summary. The goal is an evidence-backed article with exactly one core thesis that an unfamiliar reader can retell.

For the user, internal collaborators, or future AI agents, use the [Internal Writing Workflow](./workflow_internal_writing.md). External-facing research analysis defaults to a survey report in `contexts/survey_sessions/`. Use a target project's blog directory and format only when the user explicitly requests a blog post.

## 2. Acceptance Criteria

1. **Concept before reference (blocking gate)**: Give enough context before the first mention of every proper noun, regulation, event, and technical term. This does not require a dictionary definition; one background anchor is often enough. The rule applies throughout the article, not only at the opening.
2. **Natural explanation, not a lecture (blocking gate)**: The article should sound like someone who understands the problem sharing a discovery. It must not repeatedly follow a define-object, explain-mechanism, announce-abstraction lecture rhythm or perform friendliness through exaggerated metaphors and slang.
3. **Comprehensible and cognitively comfortable (blocking gate)**: Let concepts arrive one at a time. Show what happens through a concrete object or process before naming the difference. Do not turn the writer's multi-axis analysis into the reader's exposition order.
4. **One thesis**: The core judgment is specific and open to agreement or disagreement, not merely that the topic is complex or interesting.
5. **Thesis up front**: The first 25% establishes the problem, the author's judgment, and the reader's gain.
6. **Reader-led organization**: Follow the reader's chain of questions instead of listing the author's analytical dimensions.
7. **Author continuity**: Remain consistent with relevant Axioms and historical writing. If the judgment changes, explain the new evidence and why it changed.
8. **Visuals reduce cognitive burden**: Images compress a mechanism, trend, or comparison; include alt text and correct relative references. Do not use decorative images as evidence.
9. **Invisible scaffolding**: L1-L8, Axiom numbers, Phase labels, Thesis Catalog, and similar internal terms do not appear in the final draft.
10. **Five-second continue-reading gate**: The title and opening immediately establish the subject, core judgment, and increment beyond the public summary.

## 3. Thesis Mining Gate

If the user has not supplied a clear thesis, or the proposed thesis has not survived evidence and counterargument testing, first run [External-Facing Thesis Mining](./workflow_external_thesis_mining.md). It reads Axioms, the Thesis Catalog, historical writing, adjacent work in the target publication environment, and the research packet, then writes `tmp/<session_slug>/thesis_decision.md`.

Create `writing_brief.md` only when the verdict is `PROCEED`. `DO_NOT_WRITE_YET` means the topic cannot yet support a judgment-driven article; gather missing evidence or stop rather than forcing a thesis.

When the user supplied the thesis, preserve its direction. Still test evidence, boundaries, the strongest counterargument, author continuity, and reader delta. The main thread may perform a lightweight check for a low-risk short piece and record it in the brief.

## 4. Brief and Prose Calibration

Drafting, rewriting, and review must all load the [External Article Prose and Rhetoric Guide](./bestpractice_external_prose.md). `writing_brief.md` includes at least:

- the thesis, reader contract, three to five argument nodes, and strongest counterargument;
- the reader's start state, target belief change, and three to seven directional causal claims;
- verified facts, numbers, URLs, image placeholders, and limits on conclusion strength;
- the role each core piece of evidence plays in the argument;
- a concept-introduction plan naming concepts an unfamiliar reader may not know and where each first appears;
- an immutable-term list for product names, model names, API names, code identifiers, and easily mistranslated terms;
- three to five title candidates based on distinct judgments, plus the reason for the final choice;
- a duplication check against the titles and openings of the last five to ten pieces in the same channel.

Do not add redundant bilingual parentheticals when the primary language already communicates an ordinary concept. Preserve official product names, APIs, protocols, code identifiers, and standard abbreviations.

### 4.1 Reasoning Architecture Gate

A thesis is not an isolated sentence, and an outline is not a material-classification list. Before drafting, define the change in understanding the article should create, then order the material by comprehension dependencies:

1. **Reader start state**: How the target reader probably understands the subject and which prerequisites are missing.
2. **Target belief change**: The specific before-and-after understanding. It must be more precise than "understand the product or event" and open to agreement or disagreement.
3. **Causal model**: Three to seven directional claims that show the thesis's causal dependencies.
4. **Evidence roles**: Whether each core source establishes the old model, proves a change, explains a mechanism, validates a judgment, or limits extrapolation. Material without a role stays out of the draft.

The brief also includes a **Voice Route**. It does not replace the outline; it prevents the claim graph from becoming a lecture:

1. **Opening oddity or observation**: The contrast, anomaly, or change the writer would genuinely tell a friend about.
2. **Author stake**: An optional light first-person sentence explaining why the writer cares, without emotional performance.
3. **Reader question chain**: The natural question the reader asks at each section, not "this section introduces X."
4. **Concrete consequence anchors**: At least one observable action or consequence per section.
5. **Tone hazards**: Likely textbook phrasing and performative informality for this topic.
6. **Concrete carrier or running example**: When comparing three or more abstract objects, prefer one task, person, request, or business record across sections.

Analytical frameworks may help discover the thesis but do not enter the article by default. Unless readers need to operate the framework themselves, show the difference through a concrete process and name it only after they can see it. Every section must answer four questions: which reader belief changes; whether all prerequisites have appeared; which concrete object, action, or consequence carries it; and whether the reader must hold several ungrounded concepts at once.

### 4.2 Title: The Shortest Reader Contract

The title identifies the subject, establishes relevance, and signals what the article adds beyond public information.

- Pair an unfamiliar company, paper, or protocol with its category, action, or change.
- Name the news subject or concrete change in an event-driven article.
- Put the analytical increment in mechanism, evolution, competitive position, boundary, or decision impact rather than repeating what launched.
- Prefer accuracy. Avoid clickbait, false suspense, and inflated causality; a title may state the judgment directly.
- Do not default to templates such as "not A but B," "why X is becoming Y," or "trend or hype."

Apply the substitution test: if replacing the company, paper, or event leaves a title reusable for ten other articles, it does not identify this article. Recheck title-body fit after IC-3 and update the title if the article's increment became clearer.

### 4.3 Opening: Let Evidence Choose the Entry Point

There is no default opening template. A concrete scenario, second-person simulation, incident, or definition is not an automatic entry. The title makes the reader contract; the opening immediately confirms the subject, judgment, and increment without delaying them through atmosphere, reflection, generic history, or a definition.

Let distinctive evidence choose the entry: a real log may begin with its timeline; a paper with its key result or measurement; a product release with its defining design choice; a technical evolution with a pivot, deprecation, or changed constraint; a market analysis with its classification or strongest substitute. If no distinctive entry evidence exists, state the judgment directly rather than inventing a scene.

Specific details must come from evidence. Do not invent step counts, character actions, incident sequences, or user reactions. An event-driven piece completes event anchoring and analytical increment on the first screen. By the end of the first two or three paragraphs, the reader can retell what happened, what the article says it changes, and why the rest is useful.

Apply the substitution test to the opening. Read the first 150-300 words of the last five to ten pieces in the same channel. If two of the last five use the same entry pattern, do not repeat it without an evidence-based reason.

Also check continuity with the author's existing views. Do not search only the current product or event name. Search by problem and concept to determine whether the current subject fills, revises, or contradicts an earlier judgment. When that continuity explains "why now" better than an isolated product introduction, connect the old judgment in one or two sentences before introducing the current subject. Record the old judgment, the relationship, the prior URL, and the reason for using or rejecting this entry in the brief.

## 5. AGY Two-Pass Drafting and Independent Prose QA

Every writing agent follows the [Antigravity CLI File-Based Invocation](./antigravity_cli.md).

| Role | Execution model | Artifact | Responsibility |
|---|---|---|---|
| Main-thread Manager | Main model | `tmp/<session_slug>/writing_brief.md` | Research, fact-checking, thesis gate, reasoning architecture, Voice Route, concept plan, final visuals, and acceptance checks |
| IC-1 structural draft | AGY / `Gemini 3.5 Flash (High)` | `tmp/<session_slug>/article_structural.md` | Build the claim dependency graph with evidence, concepts, links, and images; mark the reader question and concrete consequence without aiming for publishable prose |
| IC-2 natural-explanation rewrite | fresh AGY / `Gemini 3.5 Flash (High)` | `tmp/<session_slug>/article.md` | Read the brief, structural draft, and same-channel calibration pieces; inherit claims and hard constraints but retell the article from the Voice Route |
| IC-3 independent voice QA / Final Writer | fresh AGY / `Gemini 3.5 Flash (High)` | `tmp/<session_slug>/article_qa.md`, `prose_qa.md` | Judge whole-article voice and cognitive comfort before revising prose; preserve claims, facts, evidence, numbers, URLs, images, and structural intent. IC-3 is the final prose authority |
| Manager Content Acceptance | Main model | `tmp/<session_slug>/article_final.md`, `content_audit.md` | Treat `article_qa.md` as the irreplaceable base document, perform invariant and new-claim audits, and make only word-level factual corrections within a 5% body-text budget |

IC-1, IC-2, and IC-3 each use a fresh AGY conversation: one `agy --print` call without `--continue` or `--conversation`. Store a separate `agy_icN_prompt.md`, result, `agy_icN_stdout.txt`, `agy_icN_stderr.txt`, and `agy_icN_events.log` for each stage. Use the 10-minute internal timeout, an outer timeout of about 610 seconds, sandboxing, and non-interactive permission confirmation.

Store every brief, calibration artifact, prompt, draft, review report, and runtime log under the gitignored `tmp/<session_slug>/` directory so unpublished material and local paths do not enter version control.

After each stage, the main thread checks exit code, non-empty result file, absence of unhandled stderr errors, and preservation of numbers, URLs, images, structure, and immutable terms. Stdout self-reporting never replaces artifact inspection.

### 5.1 IC-2: Retell the Structural Draft Instead of Polishing It

Low cognitive burden has three gates: whether context exists when a concept arrives; whether the prose sounds like a person following a real question; and how many ungrounded concepts the reader must hold at once. Defined concepts and short sentences can still produce a lecture.

IC-2 reads the structural draft to recover claims, evidence positions, URLs, numbers, and section dependencies, not to polish its sentences. Reduce each section to reader question, concrete action or consequence, and judgment, then rewrite from a blank page. Preserving the same opening logic for two consecutive paragraphs means the rewrite failed.

When comparing options, prefer one request, ticket, person, or data record across sections. Put actions before categories, delay terminology, and advance one main relationship per paragraph. An H2 must survive a cold read; if it requires the article's internal taxonomy, rewrite it as an action, change, or reader question.

Before every IC-2 pass, select three to five recent, human-edited pieces from the same channel with similar explanatory difficulty. `tmp/<session_slug>/style_calibration.md` records sample paths, useful paragraphs and voice traits, plus textbook and performatively informal counterexamples from the current structural draft. Calibrate narrative distance, not reusable phrases, openings, or metaphors.

Read the opening three paragraphs and the first paragraph under every H2 aloud. For each section, check whether an unfamiliar reader understands first-occurrence concepts, can restate the action without the new terms, avoids repeated rereading, and still understands the mechanism after metaphors and slang are removed.

### 5.2 IC-3: Independent Authority Boundary

Within one fresh AGY conversation, IC-3 reviews before editing. First read only the opening, first paragraph under every H2, and ending. Decide whether the article naturally explains a discovery or lectures from an outline. Three or more repetitions of announce-topic, define-object, abstract-summary require a whole-prose rewrite rather than word replacement.

Then check concept before reference, title and opening, natural language, cognitive comfort, AI templates, scaffold leakage, local coherence, repetition, same-channel voice, performative informality, and statements that make sense only to someone who saw the editing conversation.

IC-3 may split or combine sentences, replace words, revise local paragraphs, adjust paragraph breaks, and change subheadings. When the whole-article voice fails, it may also rewrite all prose while preserving claims, facts, numbers, URLs, images, and major section order. It may not add or remove brief-authorized claims or alter factual attribution, thesis, or conclusion strength.

If the draft needs a new fact, a changed thesis, major section reordering, removal of an analytical framework readers do not need to operate, or a rebuilt evidence chain, IC-3 records a `BLOCKER` in `prose_qa.md` instead of repairing it. The main thread returns to fact-checking, the brief, or IC-1.

`prose_qa.md` separately records the comprehension gate and cognitive-comfort gate. It also records the whole-article voice judgment, major revisions, at least four real before-and-after pairs, cold-heading and restatement tests, preserved counts of numbers/URLs/images, performative-informality scan, and blocker state. Both gates must pass with no blocker before `article_qa.md` enters Manager Content Acceptance.

### 5.3 Manager Content Acceptance

Antigravity / Gemini owns final prose authority for external-facing articles. The main thread remains responsible for factual correctness and delivery acceptance, but review authority does not imply writing authority. `article_qa.md` is the irreplaceable base document. At least 95% of the final body text must come directly from it or a later AGY final-integration draft. Measure the main thread's direct changes as a non-whitespace-character diff; deletion, movement, and replacement all count toward the 5% limit. A title change explicitly requested by the user does not count toward the body-text ratio.

The main thread may make only four types of word-level surgical change: correct names, organizations, dates, numbers, URLs, code identifiers, and official product names; reduce guarantees, causal conclusions, or absolutes to the strength supported by the source pack; fix an unambiguous typo, grammar defect, repeated word, or punctuation error; or delete one unsupported local fact without rewriting its paragraph. It must not select and splice paragraphs, create a replacement draft, reorder paragraphs, or rewrite paragraph entries, transitions, or endings.

When a paragraph-level or structural change is required, the main thread writes an itemized `content_audit.md` naming the affected sentence, evidence boundary, and permitted wording, then sends it to a fresh AGY conversation for targeted final integration. The prompt must require every unmarked paragraph to remain verbatim. After AGY returns, the main thread performs read-only acceptance plus the surgical corrections above. Any remaining large change goes back to AGY rather than being rewritten by the main thread.

Finally, compare the AGY final draft with `article_final.md`: body-text preservation is at least 95%; numbers match; URL counts and targets match; image references match; H2 order matches; and no claim was added, removed, or strengthened. `content_audit.md` records every direct main-thread edit with its original text, reason, replacement, and body-text preservation rate.

## 6. Visuals

Visuals are a hard constraint for external-facing articles. Each image must compress a mechanism or show a trend or comparison, use a publication format supported by the target project such as PNG/JPG/WebP, remain reasonably sized, and appear through descriptive alt text and a relative Markdown path. Establish quantitative accuracy before visual refinement. Decoration does not replace evidence.

## 7. Post-Writing Scans

After IC-3 semantic review and Manager Content Acceptance, the main thread runs deterministic regression scans on `article_final.md`. It may fix a hit only within the word-level boundary in Section 5.3. A paragraph-level change goes to a fresh AGY final-integration pass, followed by content acceptance and every scan again:

```bash
# Em dashes
rg -n '—' <file>

# Evaluative intensifiers
rg -ni '\b(very|clearly|obviously|notably|importantly)\b' <file>

# Internal scaffolding
rg -ni 'L[0-8]|axiom|Phase [A-Z]|narrative reconstruction|technology lineage|bottleneck shift|Thesis Catalog' <file>

# Meta-commentary and prohibited evaluative leads
rg -ni 'specifically|next we|it is important to note|clearly shows|\bworth\b|\b(grow|grows|grew|grown|growing) (out of|into)\b' <file>

# Passive voice; review each hit
rg -n '\b(is|are|was|were|be|been|being)\s+\w+(ed|en)\b' <file>

# Image references
rg -n '!\[[^\]]+\]\([^\)]+\)' <file>

# Unexpected Chinese output. This Unicode range matches common CJK ideographs.
rg -n '[\x{3400}-\x{4DBF}\x{4E00}-\x{9FFF}]' <file>

# Mechanical adjective stacks that hide actors and sequence
rg -ni '\b(waitable|rejectable|resumable|recoverable|traceable|verifiable)(,| and)\s*(waitable|rejectable|resumable|recoverable|traceable|verifiable)' <file>
```

A regex cannot reliably verify concept before reference, lecture-like voice, cognitive comfort, performative informality, or redundant cross-language parentheticals. IC-3 reviews them semantically and records the results in `prose_qa.md`. The main thread separately compares `article.md` to `article_qa.md` and the AGY final draft to `article_final.md` for numbers, URLs, image counts and targets, H2 order, evidence sections, conclusion strength, and at least 95% body-text preservation. If direct main-thread edits exceed 5%, restore the AGY draft as the base and return the problem to AGY.

## 8. Final Read Gate

After drafting, visuals, fact-checking, and scans are complete, the main thread uses the current harness's file-reading tool to read the final Markdown from its beginning. This read must occur after the last edit; the brief, a temporary draft, a partial grep, or a diff does not satisfy the gate.

Do not edit after the final read unless a mechanical defect must be corrected. If corrected, read the final file again. The final response links to that file with Markdown.

## 9. Delivery Endpoint

The final Markdown and visuals remaining in the local workspace are the delivery endpoint. Do not publish automatically to a blog, social platform, community, or other external channel. Every external action requires explicit authorization for that publication.
