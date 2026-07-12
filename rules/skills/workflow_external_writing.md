# External Writing and Drafting Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: Transforming research materials into judgment-driven external-facing analysis articles, public survey reports, or course/client content for external readers.
- **Prerequisites**: Phase 1-3 output from the Deep Research Workflow (`workflow_deep_research_survey.md`), or equivalent verified material.
- **Created**: 2026-04-28
- **Last updated**: 2026-07-11

---

## 1. What Problem This Skill Solves

Research material may be sufficient while the resulting text still reads like an AI summary and lacks the author's analytical perspective and judgment framework. This skill defines how to turn facts into a retellable analysis whose core thesis can be stated in one or two sentences.

*   **Boundary**: Use for strangers without shared context, public channels, customers, or external course audiences. For internal documents written for the user, internal collaborators, or future AI agents, use `workflow_internal_writing.md`.
*   **Output type decision (required before drafting)**: The default output for external-facing research analysis is a **survey report**, stored in `contexts/survey_sessions/`. Treat it as a blog post and store it in `contexts/blog/content/` only when the user explicitly says "write a blog post" or "publish to the blog."

---

## 2. Acceptance Criteria for a Good External Article

Validate the result against these criteria after writing:

1.  **A non-expert can understand and retell the thesis (blocking gate)**: A smart person who does not work in the field can retell the article in one or two sentences after hearing it read aloud. Friction in any section means its background assumptions or information density are wrong.
2.  **One explicit core thesis**: The article has exactly one core judgment. It is specific and open to agreement or disagreement, not a vague statement such as "complex and worth watching."
3.  **Thesis up front**: After the first 25%, the reader must know which problem the article discusses, what the author's judgment is, and what they will gain by finishing it.
4.  **Organized around the reader**: Advance through the reader's chain of questions or needs rather than listing the author's analytical dimensions.
5.  **Consistent with the existing viewpoint system**: Stay consistent with the author's established core views, axioms in `rules/axioms/`, and existing articles on the same subject. If the judgment changes, naturally explain the new evidence and why it changed the earlier view.
6.  **Visuals reduce cognitive burden (hard constraint)**: Visuals compress a mechanism or show a trend or comparison. They are never decoration. The body must reference each visual with a relative link and descriptive alt text.
7.  **The analytical framework remains invisible**: Thesis Catalog labels L1-L8, axiom numbers, Phase labels, and other writing-scaffold terms must never appear in the final draft.
8.  **Five-second continue-reading gate**: After scanning the title and first few sentences, the reader can immediately confirm the subject or event, the author's core judgment, and what mechanisms, boundaries, counterexamples, or consequences the full article adds beyond the public summary.

---

## 3. Discovering a Thesis from the Material

If the user has not supplied an explicit thesis, use these tools to discover and synthesize one in `tmp/<session_slug>/scratchpad.md`:

1.  **Perspective matching**: Read the [Thesis Catalog](./reference_writing_thesis_catalog.md). Choose one to three perspectives that strongly fit the topic as inspiration. Do not force a framework.
2.  **Search the author's existing writing**: Search `contexts/blog/`, `contexts/survey_sessions/`, and `rules/axioms/` for historical views and related axioms.
3.  **Read existing work in the target environment**: Read three to six adjacent or same-topic articles in the target publication environment. Determine how the new article adds, fills a gap, or corrects earlier work instead of reproducing a familiar media narrative.
4.  **Multi-model thesis brainstorm**: Before finalizing, use parallel subagents for divergence. Follow `workflow_parallel_subagents.md` and issue the calls in one message through `multi_tool_use.parallel`. Suggested roles:
    *   `gemini_3.5_flash`: Reader entry point and low cognitive burden.
    *   `glm`: Contrarian divergence and blind-spot detection.
    *   `reasoning_gpt`: Argument strength, evidence risk, and consistency audit.
5.  **Main-thread synthesis**: The main thread deeply integrates the subagent results. The synthesis must be written to disk and include:
    *   **Thesis statement**: Two or three sentences, with a clear view that a non-expert can understand.
    *   **Argument skeleton**: Three to five points matched to perspectives and the strongest evidence.
    *   **Evidence risks and attribution limits**.

---

## 4. Drafting Principles and Prose Calibration

During drafting, rewriting, and review, load and strictly follow the [External Article Prose and Rhetoric Guide](./bestpractice_external_prose.md).
*   Split overloaded modifiers and replace abstract subjects with people and actions.
*   Do not use category-name headings or numbered announcements with no information gain at paragraph openings or in headings.
*   Do not use the hard "not X but Y" AI template. State the point directly or use a light contrast.
*   Do not add redundant bilingual parentheticals when the primary language already expresses the concept. Preserve official product names, APIs, protocols, code identifiers, and standard abbreviations.

### 4.1 Title Design: The Shortest Reading Contract

In the fewest words possible, the title should identify the subject, establish why it matters, and expose the article's analytical increment over public information. The title makes a promise, the opening confirms it, and the body fulfills it.

Pair an unfamiliar company, paper, or protocol with its category, action, or change. Event-driven pieces should normally name the news subject. Analytical titles should signal that the body adds mechanism, evolution, competitive context, boundaries, or decision impact. Accuracy comes first: no clickbait, false suspense, hidden answers, or inflated causality.

Do not standardize titles around formulas such as "not A but B," "why X is becoming Y," "is X a trend or hype," or "stop doing X." Apply the substitution test: if replacing the company, paper, or event name leaves a title reusable for ten other pieces, it does not express this article's identity.

In `writing_brief.md`, draft three to five candidates from genuinely different judgment angles rather than synonymous variants of one template. Compare the last five to ten titles from the same channel to avoid repeated questions, contrasts, imperatives, or "from A to B" constructions. Recheck title-body fit after IC-2 finishes.

### 4.2 Opening Design: Let the Evidence Choose the Entry Point

Do not treat a concrete scenario, second-person simulation, incident, or "phenomenon first" as the default algorithm. Ask which evidence is most distinctive and best carries the thesis. A real log may begin with its first anomaly; a paper with its key result; product archaeology with a pivot or deprecation; a market analysis with its classification or strongest substitute. If no distinctive evidence exists, state the judgment directly rather than inventing a scene.

Specificity must come from evidence. Do not invent step counts, user reactions, character actions, or incident details for atmosphere. In event-driven writing, the title or first screen must name the event and immediately expose the analytical increment. Avoid an archaeological detour that spends paragraphs on distant history before mentioning the current event, and avoid a news-summary ceiling where the body adds no new judgment. By the end of the first two or three paragraphs, the reader should be able to retell what happened, what the article says it changes, and why continuing is useful.

Apply the substitution test to the opening as well. Before writing the brief, compare the first 150-300 words of the last five to ten articles from the same channel. If two of the last five already use the same entry pattern, do not repeat it without a reason grounded in this article's strongest evidence.

---

## 5. Two-Pass Drafting and Model Division of Labor

An external article is delivered through close coordination between the main thread and writing subagents.

| Role | Execution model | Artifact | Responsibility |
| :--- | :--- | :--- | :--- |
| **Main thread (Manager)** | Main model | `tmp/<session_slug>/writing_brief.md` | Phase 1-3 research, fact-checking, thesis generation, brief structure including negative examples, and final image generation |
| **Structural draft agent (IC-1)** | `gemini_3.5_flash` | `tmp/<session_slug>/article_structural.md` | Read `writing_brief.md` and produce a structurally complete draft with arguments, evidence, paragraph order, links, and image placeholders |
| **Low-cognitive-burden rewrite agent (IC-2)** | `gemini_3.5_flash` | `tmp/<session_slug>/article.md` | Read `writing_brief.md` and `article_structural.md`; preserve the thesis, evidence, links, image references, and structural intent while rewriting the entire article for low cognitive burden |

### Concrete Methods for the IC-2 Rewrite

IC-2 turns academic or stiff prose into language addressed to a smart reader outside the field. "Low cognitive burden" alone is not specific enough: Gemini can easily produce a translation-like summary. During the rewrite, do all four of the following and compare each against the negative examples in Section 5 of `bestpractice_external_prose.md`:

1. **Do not default to a definition; let the evidence choose the entry point**. Follow Section 4.2 and select the article's distinctive fact, anomalous result, product decision, historical turn, lived experience, or direct judgment. Put the most informative material first, then name it when a label helps.
2. **Turn abstract subjects into people and actions**. Replace "the discovery of this phenomenon produced a new judgment" with "maille reviewed 390,000 records and found..." Replace "failure occurs at the reasoning layer" with "the part that fails is the model's thinking layer." When the subject is a category word such as phenomenon, mechanism, failure surface, or paradigm, ask whether a concrete person and action can replace it.
3. **Advance in short sentences, one action per sentence**. Default to no more than 30 words. Split overloaded modifiers into separate sentences. Avoid stacking multiple dependent clauses.
4. **Replace specialized phrasing with everyday words**. "Benchmarks cannot cover it" becomes "benchmarks do not reveal it." "A new failure surface" becomes "a new way to fail." "Monotonic degradation" becomes "it gets worse every month." Keep necessary technical terms such as reasoning, doom loop, benchmark, token, and adaptive thinking, but describe them with ordinary verbs and adjectives rather than elevated vocabulary.

Hard acceptance gate: Read the opening three paragraphs aloud. Rewrite any sentence that sounds like a paper abstract or requires rereading.

### 0. The Main Thread's Prose Authority Depends on Its Base Model

The IC-2 output is the delivery draft. Whether the main thread may review its prose quality depends on the model running the main thread:

- **The main thread is a Gemini model, including `gemini_3.5_flash`**: It may apply the prose quality gate below because a same-family model editing same-family prose does not introduce a different model's style.
- **The main thread is not a Gemini model, including Opus, DeepSeek, GPT, or GLM**: **Do not manually edit IC-2 prose.** Adopt the final draft directly. The main thread may perform only three mechanical checks: (a) numbers match the brief's numerical-precision constraints, (b) all inline link URLs are present and reachable, and (c) Markdown syntax is valid, including image placeholders not enclosed in code formatting and no duplicate H1. Record prose problems in the brief's writing retrospective for the next run instead of fixing them. A non-Gemini main thread editing Gemini prose introduces another model's style and makes the text less consistent.

### 1. Why Two Passes
The first pass, the structural draft, decides what to say by placing the thesis, evidence, objections, image references, inline links, and paragraph order correctly. The second pass decides how to make the text easy to follow.
*   Short pieces under 1,000 words, internal memos, or explicitly requested quick drafts may skip the second pass. External-facing analysis does not skip it by default.

### 2. Three-Question Gate Against Out-of-Scope Rewriting (Gemini Main Threads Only)
This section applies only when the main thread is a Gemini model. Non-Gemini main threads adopt the IC-2 output directly and do not enter this gate.

Before overturning or manually rewriting large parts of the second-pass prose, the main thread must answer all three questions. If any answer is missing, revise the rewrite brief and rerun the second pass:
1.  Does the reason fall into one of these hard categories: (a) missing facts, (b) missing URLs, (c) structure does not follow the brief, (d) an objective finished-product defect, or (e) failure of the low-cognitive-burden gate? Subjective reactions such as "the voice feels wrong" do not justify a manual rewrite.
2.  Does the objection come from an explicit rule in `COMMUNICATION.md` or `bestpractice_external_prose.md`, or from subjective preference?
3.  Is the problem a local objective defect or excessive reader burden across the whole article? Fix local defects narrowly. Rerun the low-cognitive-burden rewrite for article-wide burden.

---

## 6. Image Generation Rules

Visuals are a **hard constraint** for external-facing articles. An external article without visuals is incomplete and cannot be delivered. Short articles under 2,000 words need at least one image. Longer articles need at least two or three.

1.  **Final-image gate**: Every image embedded in Markdown must be a PNG/JPG/WebP generated or redrawn by **`gpt-image-2`**. Matplotlib structural drafts, Mermaid, SVG, or Keynote exports may only serve as inputs and must never appear directly as final article images.
2.  **Quantitative chart redraw**: The main thread first creates a structural draft with matplotlib to preserve data accuracy, then calls the Image Generation Skill with `gpt-image-2`, passing the matplotlib draft through `-i` for visual redrawing.
3.  **Visual style**: Default to light backgrounds, low-saturation colors, and an understated business or research-report style. Avoid dark backgrounds, neon purple, high-contrast glow, and other decorative effects.
4.  **File-size limit**: Compress final images to **JPG/WebP**. Keep each image under **200 KB** with a 1024-pixel long edge. Do not inline base64 images.

---

## 7. Post-Writing Quality Scans

The scan scope depends on the main thread's base model, following the authority split in Section 5:

- **Gemini main thread**: Run all nine scans below. For prose-related hits, use the three-question gate in Section 5.2 to decide between a narrow fix and a rerun.
- **Non-Gemini main thread**: Run only scans 1 (em-dash Markdown defect), 7 (image-reference syntax), 8 (mixed-language defects), and 9 (redundant bilingual parentheticals), plus one numerical and link verification against the brief. Do not run prose scans 2, 3, 5, or 6. Return scan 9 hits to the writing model instead of rewriting them with a different model family.

After drafting and image generation, the main thread **must run the applicable scans** rather than relying on visual review:

```bash
# 1. Em dashes (required for every main thread)
rg -n '—' <file>

# 2. Evaluative adjective summaries (Gemini main threads only)
rg -n '\b(very|clearly|obviously|notably|importantly)\b' <file>

# 3. Internal scaffold leakage (Gemini main threads only)
rg -n 'L[0-6]|axiom|Phase [A-Z]|narrative reconstruction|technology lineage|bottleneck shift|Thesis Catalog' <file>

# 4. Long blockquote audit (Gemini main threads only)
rg -n '^> ' <file> | awk '{ if (length($0) > 100) print }'

# 5. Meta-commentary, evaluative leads, and article-wide prohibited-expression audit (Gemini main threads only)
rg -ni 'specifically|next we|it is important to note|clearly shows|\bworth\b|\b(grow|grows|grew|grown|growing) (out of|into)\b' <file>

# 6. Passive-voice audit (Gemini main threads only; review each hit)
rg -n '\b(is|are|was|were|be|been|being)\s+\w+(ed|en)\b' <file>

# 7. Image-reference check (required for every main thread)
rg -n '!\[[^\]]+\]\([^\)]+\)' <file>

# 8. Mixed-language residue audit (required for every main thread; adapt to target language)
rg -n '<target-language residue pattern>' <file>

# 9. Redundant bilingual parentheticals in Chinese output, e.g. “执行状态（execution state）”
rg -n '[\p{Han}”’」』][（(][A-Za-z][A-Za-z0-9 _./+:-]{1,50}[）)]' <file> | rg -v 'https?://|!\['
```

---

## 8. Delivery Endpoint

The final Markdown file with complete images, retained in the local workspace, is the delivery endpoint. The main thread **must not automatically run any external publication flow**, including `yage_share`, blog deployment, Twitter, or Circle community publishing. Publication requires explicit user instruction, keeping research and writing separate from the publication decision.
