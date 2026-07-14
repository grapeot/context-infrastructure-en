# External Writing and Drafting Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: Turning verified research into an external-facing analysis, public survey report, or course/client material.
- **Prerequisites**: Phase 1-3 output from the [Deep Research Survey Workflow](./workflow_deep_research_survey.md), or equivalent verified material.
- **Last updated**: 2026-07-14

## 1. Goal and Output Route

This skill addresses the case where the material is sufficient but the article still reads like an AI summary. The goal is an evidence-backed article with exactly one core thesis that an unfamiliar reader can retell.

For the user, internal collaborators, or future AI agents, use the [Internal Writing Workflow](./workflow_internal_writing.md). External-facing research analysis defaults to a survey report in `contexts/survey_sessions/`. Use a target project's blog directory and format only when the user explicitly requests a blog post.

## 2. Acceptance Criteria

1. **Concept before reference (blocking gate)**: Give enough context before the first mention of every proper noun, regulation, event, and technical term. This does not require a dictionary definition; one background anchor is often enough. The rule applies throughout the article, not only at the opening.
2. **One thesis**: The core judgment is specific and open to agreement or disagreement, not merely that the topic is complex or interesting.
3. **Thesis up front**: The first 25% establishes the problem, the author's judgment, and the reader's gain.
4. **Reader-led organization**: Follow the reader's chain of questions instead of listing the author's analytical dimensions.
5. **Author continuity**: Remain consistent with relevant Axioms and historical writing. If the judgment changes, explain the new evidence and why it changed.
6. **Visuals reduce cognitive burden**: Images compress a mechanism, trend, or comparison; include alt text and correct relative references. Do not use decorative images as evidence.
7. **Invisible scaffolding**: L1-L8, Axiom numbers, Phase labels, Thesis Catalog, and similar internal terms do not appear in the final draft.
8. **Five-second continue-reading gate**: The title and opening immediately establish the subject, core judgment, and increment beyond the public summary.

## 3. Thesis Mining Gate

If the user has not supplied a clear thesis, or the proposed thesis has not survived evidence and counterargument testing, first run [External-Facing Thesis Mining](./workflow_external_thesis_mining.md). It reads Axioms, the Thesis Catalog, historical writing, adjacent work in the target publication environment, and the research packet, then writes `tmp/<session_slug>/thesis_decision.md`.

Create `writing_brief.md` only when the verdict is `PROCEED`. `DO_NOT_WRITE_YET` means the topic cannot yet support a judgment-driven article; gather missing evidence or stop rather than forcing a thesis.

When the user supplied the thesis, preserve its direction. Still test evidence, boundaries, the strongest counterargument, author continuity, and reader delta. The main thread may perform a lightweight check for a low-risk short piece and record it in the brief.

## 4. Brief and Prose Calibration

Drafting, rewriting, and review must all load the [External Article Prose and Rhetoric Guide](./bestpractice_external_prose.md). `writing_brief.md` includes at least:

- the thesis, reader contract, three to five argument nodes, and strongest counterargument;
- verified facts, numbers, URLs, image placeholders, and limits on conclusion strength;
- a concept-introduction plan naming concepts an unfamiliar reader may not know and where each first appears;
- an immutable-term list for product names, model names, API names, code identifiers, and easily mistranslated terms;
- three to five title candidates based on distinct judgments, plus the reason for the final choice;
- a duplication check against the titles and openings of the last five to ten pieces in the same channel.

Do not add redundant bilingual parentheticals when the primary language already communicates an ordinary concept. Preserve official product names, APIs, protocols, code identifiers, and standard abbreviations.

### 4.1 Title: The Shortest Reader Contract

The title identifies the subject, establishes relevance, and signals what the article adds beyond public information.

- Pair an unfamiliar company, paper, or protocol with its category, action, or change.
- Name the news subject or concrete change in an event-driven article.
- Put the analytical increment in mechanism, evolution, competitive position, boundary, or decision impact rather than repeating what launched.
- Prefer accuracy. Avoid clickbait, false suspense, and inflated causality; a title may state the judgment directly.
- Do not default to templates such as "not A but B," "why X is becoming Y," or "trend or hype."

Apply the substitution test: if replacing the company, paper, or event leaves a title reusable for ten other articles, it does not identify this article. Recheck title-body fit after IC-3 and update the title if the article's increment became clearer.

### 4.2 Opening: Let Evidence Choose the Entry Point

There is no default opening template. A concrete scenario, second-person simulation, incident, or definition is not an automatic entry. The title makes the reader contract; the opening immediately confirms the subject, judgment, and increment without delaying them through atmosphere, reflection, generic history, or a definition.

Let distinctive evidence choose the entry: a real log may begin with its timeline; a paper with its key result or measurement; a product release with its defining design choice; a technical evolution with a pivot, deprecation, or changed constraint; a market analysis with its classification or strongest substitute. If no distinctive entry evidence exists, state the judgment directly rather than inventing a scene.

Specific details must come from evidence. Do not invent step counts, character actions, incident sequences, or user reactions. An event-driven piece completes event anchoring and analytical increment on the first screen. By the end of the first two or three paragraphs, the reader can retell what happened, what the article says it changes, and why the rest is useful.

Apply the substitution test to the opening. Read the first 150-300 words of the last five to ten pieces in the same channel. If two of the last five use the same entry pattern, do not repeat it without an evidence-based reason.

## 5. AGY Two-Pass Drafting and Independent Prose QA

Every writing agent follows the [Antigravity CLI File-Based Invocation](./antigravity_cli.md).

| Role | Execution model | Artifact | Responsibility |
|---|---|---|---|
| Main-thread Manager | Main model | `tmp/<session_slug>/writing_brief.md` | Research, fact-checking, thesis gate, brief, concept plan, final visuals, and mechanical acceptance checks |
| IC-1 structural draft | AGY / `Gemini 3.5 Flash (High)` | `article_structural.md` | Read only the brief; place every argument, item of evidence, paragraph, concept introduction, link, and image placeholder |
| IC-2 low-cognitive-burden rewrite | fresh AGY / `Gemini 3.5 Flash (High)` | `article.md` | Read the brief and structural draft; preserve every hard constraint and rewrite the complete article |
| IC-3 independent prose QA | fresh AGY / `Gemini 3.5 Flash (High)` | `article_final.md`, `prose_qa.md` | Review first as an unfamiliar reader and editor, then revise without changing the thesis, facts, evidence, numbers, URLs, images, or structural intent |

IC-1, IC-2, and IC-3 each use a fresh AGY conversation: one `agy --print` call without `--continue` or `--conversation`. Store a separate `agy_icN_prompt.md`, result, `agy_icN_stdout.txt`, `agy_icN_stderr.txt`, and `agy_icN_events.log` for each stage. Use the 10-minute internal timeout, an outer timeout of about 610 seconds, sandboxing, and non-interactive permission confirmation.

After each stage, the main thread checks exit code, non-empty result file, absence of unhandled stderr errors, and preservation of numbers, URLs, images, structure, and immutable terms. Stdout self-reporting never replaces artifact inspection.

### 5.1 IC-2: Audit Concepts Before Sentences

Low cognitive burden starts with information availability, not sentence length. IC-2 reads from the beginning and asks at every first occurrence of a proper noun, regulation, event, or term: "Would a reader who never saw the structural draft know what this is here?" If not, add a background anchor before the reference. When a concept returns after a long gap, provide a light reminder.

Then revise sentences: replace abstract subjects with people and actions, split overloaded modifiers, advance one primary action per sentence, and prefer ordinary words over elevated abstractions. Short sentences are a tendency; do not put every sentence on a separate line.

Read the opening three paragraphs aloud and audit every new concept from an unfamiliar reader's perspective. Fluent sentences still fail when the reader cannot identify the concepts.

### 5.2 IC-3: Independent Authority Boundary

Within one fresh AGY conversation, IC-3 reviews before editing. It checks concept before reference, title and opening, natural language, cognitive burden, AI templates, scaffold leakage, local coherence, and repetition.

IC-3 may split or combine sentences, replace words, revise local paragraphs, adjust paragraph breaks, and change subheadings. It may not add or remove claims or alter factual attribution, numbers, URLs, images, thesis, conclusion strength, or the main argument order.

If the draft needs a new fact, a changed thesis, major section reordering, or a rebuilt evidence chain, IC-3 records a `BLOCKER` in `prose_qa.md` instead of repairing it. The main thread returns to fact-checking, the brief, or IC-1. `prose_qa.md` records review dimensions, major changes, preserved counts of numbers/URLs/images, and blocker status.

After IC-3, the main thread performs only mechanical checks and does not manually edit prose. Prose issues return to IC-3; factual, thesis, or structural issues return upstream.

## 6. Visuals

Visuals are a hard constraint for external-facing articles. Each image must compress a mechanism or show a trend or comparison, use a publication format supported by the target project such as PNG/JPG/WebP, remain reasonably sized, and appear through descriptive alt text and a relative Markdown path. Establish quantitative accuracy before visual refinement. Decoration does not replace evidence.

## 7. Post-Writing Scans

After IC-3 semantic review, the main thread runs deterministic regression scans on `article_final.md`. Return prose hits to IC-3 rather than editing them directly:

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
```

A regex cannot reliably detect redundant cross-language parentheticals or verify concept before reference. IC-3 reviews both semantically and explicitly records a full first-occurrence concept audit in `prose_qa.md`. The main thread also compares `article.md` with `article_final.md` for numbers, URLs, image counts and targets, H2 order, evidence sections, and conclusion strength.

## 8. Final Read Gate

After drafting, visuals, fact-checking, and scans are complete, the main thread uses the current harness's file-reading tool to read the final Markdown from its beginning. This read must occur after the last edit; the brief, a temporary draft, a partial grep, or a diff does not satisfy the gate.

Do not edit after the final read unless a mechanical defect must be corrected. If corrected, read the final file again. The final response links to that file with Markdown.

## 9. Delivery Endpoint

The final Markdown and visuals remaining in the local workspace are the delivery endpoint. Do not publish automatically to a blog, social platform, community, or other external channel. Every external action requires explicit authorization for that publication.
