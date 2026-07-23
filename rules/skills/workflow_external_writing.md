# External Writing and Drafting Workflow

## Metadata

- **Type**: Workflow
- **Use when**: Turning verified research into an external-facing analytical article, public survey report, course asset, or client deliverable.
- **Prerequisite**: Phases 1-3 of `workflow_deep_research_survey.md`, or an equivalent verified factual record.
- **Last updated**: 2026-07-22

## 1. Core Model

External writing contains three different kinds of work that should not share one generation context:

1. **Editorial judgment**: why the article deserves to exist, what belief it should change, and in what order the evidence should arrive.
2. **Complete drafting**: turning locked content into natural, coherent prose.
3. **Acceptance**: checking factual fidelity, constraints, reader path, and whole-article voice.

The Main Agent is the editor, factual owner, and sole acceptance authority. An Antigravity writer produces a complete candidate; it does not audit its own article and cannot declare `PASS`. Deterministic checks cover numbers, URLs, images, and formatting. The Main Agent judges meaning, structure, cognitive comfort, and voice.

Do not ask a writer to read this workflow, all of `bestpractice_external_prose.md`, `COMMUNICATION.md`, or a large archive of prior feedback. The Main Agent must compress the requirements that matter for the current article into a short task packet. Long rule sets are Manager references, not writer context.

## 2. Output Routing and Publication Boundary

- If the user requests an external-facing deliverable without naming a channel, use the workspace's survey-report location.
- If the user explicitly requests a blog post, use the target project's documented blog location and format. Do not assume a private or machine-specific directory.
- The completed local Markdown file is the endpoint of this workflow. Publishing, scheduling, emailing, or posting to any external channel requires separate explicit authorization.
- Images are part of the deliverable and follow Section 10.

## 3. Acceptance Standard

An article passes only when all of these conditions hold:

- A smart reader with no shared context can understand it from the first paragraph without searching later sections for prerequisites.
- The first 25% establishes the subject, current trigger, core judgment, and the value of reading further.
- The article has one thesis. Every section advances that thesis rather than mirroring the categories in the research notes.
- Concepts arrive through actions, conflicts, and consequences. The article does not repeatedly follow a lecture pattern of definition, mechanism, and abstract summary.
- The reader is not asked to hold several ungrounded taxonomies or comparison axes at once. When three or more parallel items genuinely matter, provide a local map first.
- Adjacent H2 sections connect through the same object, action, limitation, or consequence. The transition still makes sense with the headings hidden.
- Numbers, URLs, attributions, qualifications, images, and proper nouns match the source of truth. The prose introduces no invented scenes, causes, or user reactions.
- The voice sounds like someone familiar with the problem sharing a verified finding. It is neither ceremonious nor artificially casual through slang, exaggerated metaphors, or copywriting tricks.

A writer's self-assessment cannot compensate for a failed condition.

## 4. Choose the Right Article Before Drafting

### 4.0 Extract the Framing Already Seeded in the Initial Ask

Before drafting or building options, the Main Agent first restates what already exists in the initial request. Users frequently seed a thesis, a protagonist, an oppositional structure, or a reader positioning in the very first sentence. Ignoring it and converging directly on a mechanism the Main Agent personally finds more elegant is the most common way this goes wrong. Handle it as one of three cases:

- **Already locked**: Do not reinvent three options. Restate the seed as the reader takeaway, proof route, and depth boundary; surface likely misunderstandings, then continue.
- **Seeded but not locked**: Still produce three options, but one of them must be a faithful execution of that seed; the other two are the Main Agent's alternative framings. The seed is not a default to be overturned — it is one option to place on the table alongside the rest.
- **Genuinely open-ended**: The three options are free to diverge, but the Main Agent must still verify object attribution and load-bearing premises first.

The gray zone between "seeded" and "locked" is a high-accident area historically. When in doubt, default to treating it as "seeded but not locked," and say that judgment out loud to the user.

### 4.1 Thesis-and-Outline Options

When the case falls into the second or third bucket above, the Main Agent should develop about three genuinely different options before drafting. They cannot be title paraphrases. Choosing another option should change the article's protagonist, evidence order, excluded material, and closing judgment.

Useful distances include, without becoming templates:

- **Object explanation**: make the project, paper, or event itself legible.
- **Landscape or belief change**: use the object to revise how readers understand a persistent problem.
- **Decision framework**: use the object as a worked example that improves future judgment.

For each option, record:

```markdown
## Option name

One-sentence thesis: What judgment should change after reading?
Why now: What event, evidence, or persistent confusion creates the warrant?
Target reader: What do they already know, and why would they continue?
Article protagonist: The object, the landscape, or the reader's decision?
Proof route: Four to six evidentiary steps, not a source inventory.
Must explain deeply: What mechanism or comparison is indispensable?
Deliberately omit: What useful research would dilute the takeaway?
Largest risk: Why might this feel flat, old, empty, too specialized, or under-supported?
Recommendation: Which option does the Main Agent recommend, and why?
```

**What counts as genuinely different**: rephrasing the same thesis as a question, a verdict, or a metaphor does not count as three options. Practical test: if the user picked another option, which material leaves the body, which evidence moves up, and what different verdict does the ending leave? If the answer isn't obvious, the options aren't different enough. The Main Agent may recommend one, but the reasoning must be grounded in this article's evidence and the calibration criteria below, not in "more depth" or "more shareable."

### 4.2 Six Calibration Criteria (Both the Yardstick for Options and the Article's Targets)

1. **The object is downgraded to a case, but the altitude stays mid-level.** Carry a claim about the field through a concrete mechanism — not stuck at object-introduction, and not floating up into abstract economic or legal conclusions. *Ceiling test*: for every load-bearing noun in the thesis sentence, can you point at a concrete mechanism or number in the case and say "this is it"? A noun you can't point to is the abstraction to cut. *Floor test*: delete the project's name — does the article still help the reader understand some long-term problem? Both tests must pass.
2. **Critical adjudication (a sharp verdict), not relay.** The article should correct the reader's most likely wrong default and render a verdict on whether something actually matters, treating the object's own headline framing as suspect by default. A useful gate: how is this judgment different from a three-year-old cliché? If you can't say, there's no informational increment. Critique stays positive in tone and on target — aimed at problem framing and evidence boundaries, never at the author's motive or competence — and a debunked thing still gets its due.
3. **Minimize cognitive load.** The reader should spend mental budget judging the conclusion, not decoding omitted premises, stacked abstract nouns, dense number clusters, or code-mixed jargon. Distinguish "thick relational context" (the reader already knows the big background) from "thin conceptual context" (terms introduced for the first time in this piece) — don't mistake shared context for shared vocabulary. This is not about less information; it's about reordering, unpacking, and glossing in place: gloss a proper noun with one grounding clause the moment it first appears.
4. **The entry point earns a stranger's attention on the stranger's own terms.** The opening must pass "why would an unfamiliar reader care in the first second," anchored in the reader's felt experience — not an insider event, a paradox only experts find counterintuitive, a straw man, or the news story that triggered the research. Unifying rule: the first screen must deliver either a tension the reader genuinely owns, or the article's increment itself. For news-driven pieces, freshness is also a gate — the first screen must show new information; don't let the reader feel it's old news by the first paragraph.
5. **Explanatory depth (the mechanism/causal why), not descriptive coverage.** Don't stop at "who did what" — give "why this player, why now," and give the reader a transferable model rather than more terminology. The transferable model must come from a real conflict in the case; there is an upper bound on the operational side too — give a high-level perspective, stop at the measurement framework, and don't drop into a spec sheet.
6. **End on an actionable hook in the reader's own domain.** External pieces typically deliver the freshest signal up top and what the reader should do at the bottom — not "who won" or "what the paper said."

### 4.3 Article Warrant and Reasoning Architecture

Before Round 1 is complete, the Main Agent must be able to answer:

- **Reader start state**: How does the reader currently understand the subject, and which prerequisite is missing?
- **Target belief change**: Which judgment should move from A to B?
- **Article warrant**: Why does this require an article rather than a short summary?
- **Causal model**: How do three to seven directional claims support the thesis?
- **Evidence roles**: Which claim does each core source prove, explain, or limit?
- **Concrete carrier**: Which request, task, number, person, or business record can carry the argument?
- **Answer timing**: When does the reader encounter the question, evidence, and complete answer? A real tension may remain open briefly, but the answer must be established within the first 25%.

An analytical tool does not automatically belong in the public thesis. Timelines, taxonomies, axes, and question sets may help discover the judgment. Keep them as private evidence organization unless readers need to learn the method itself.

## 5. Round 1: Main Agent Establishes the Source of Truth

The Main Agent completes the research, editorial choice, and factual draft. Round 1 creates four artifacts in the session's temporary working directory.

### `source_contract.md`

This is the factual authority for every later writer. Include:

- Every claim permitted in the article and the source that supports it.
- Exact numbers, dates, versions, URLs, image references, and immutable terms.
- Attribution, measurement definitions, comparison baselines, and limits on extrapolation.
- Unknowns that the writer must not fill in.
- For any running example, which actions come from evidence and which may appear only as clearly hypothetical illustrations.

Do not provide a bare link list. State what each source supports.

### `writing_brief.md`

Include at least:

- Reader start state, reader takeaway, exact thesis, and article warrant.
- Article protagonist, current trigger, and first-screen promise.
- Continuity with the author's prior judgments: whether current evidence fills, revises, or contradicts an earlier view, with relevant public URLs when available.
- Claim dependencies, H2 order, and section handoffs.
- Concrete carrier, material that requires depth, and material deliberately omitted.
- Three to five title candidates from different angles, plus why the selected title accurately names both the subject and the article's increment.
- What new evidence would weaken or overturn the thesis.

### `voice_contract.md`

Keep the writer-facing voice instructions to roughly one page and specific to this article:

- Two or three sentences defining the desired narrative stance.
- One or two user-approved positive excerpts of similar explanatory difficulty, with a note on what to learn from each.
- Two or three likely failure excerpts from the current draft, with a direct diagnosis of what feels ceremonious, instructional, or performatively casual.
- Boundaries for first person, questions, technical density, and local lists.
- No more than eight high-impact voice constraints.

Do not paste an entire published article, a universal banned-word list, this workflow, `COMMUNICATION.md`, or the full prose guide into the writer context. Use `bestpractice_external_prose.md` to produce this short contract.

### `article_source.md`

The Main Agent writes a complete, verifiable content draft with the correct thesis, facts, evidence order, H2 sections, links, and image positions. It does not need final prose, but it must be more than keywords or a claim outline. Complete concrete information reduces the writer's incentive to invent actions or causality.

Before leaving Round 1, compare `article_source.md` against `source_contract.md`. Resolve factual gaps here instead of assigning research to a prose writer.

## 6. Round 2: Two Independent Antigravity Candidates

By default, start two fresh Antigravity conversations in parallel. Both receive the same task packet and independently write `candidate_a.md` and `candidate_b.md`. For a very short article or an explicit single-version request, one candidate is acceptable, but never generate B by asking it to revise A.

Each writer reads only:

1. `source_contract.md`
2. `writing_brief.md`
3. `voice_contract.md`
4. `article_source.md`
5. Its own short round prompt

The writer returns the complete article only. It does not output an audit, explanation, invariant count, or `PASS` statement. Both candidates use the same facts and thesis; parallelism exists to obtain independent prose paths, not exaggerated style variants.

The Round 2 prompt should say only what is necessary:

- Draft from a blank page without adding facts, scenes, or causal claims outside `source_contract.md`.
- Preserve the thesis, claim strength, numbers, URLs, image references, and immutable terms.
- Paragraph entries, syntax, and H2 wording may change. If the supplied structure makes natural expression difficult, still produce the best complete candidate without discussing the problem outside the article.
- Advance through the concrete carrier rather than teaching the rules by category.
- Write only the article.

Every call follows the file-based contract in `antigravity_cli.md`. Persist prompt, result, stdout, stderr, and events separately.

## 7. Round 3: Main Agent Cold-Read Acceptance

The Main Agent is the only `PASS` authority. Read each candidate body before reading its stdout; the writer provides no self-QA report.

### 7.1 Deterministic checks first

Use scripts or direct comparison for:

- Numbers, dates, and versions.
- URL targets and image paths.
- Required and prohibited terms.
- H2 count and any required order.
- Markdown, word count, and output path.

Do not substitute a model-written natural-language audit for these checks.

### 7.2 Semantic acceptance second

Compare candidates with `source_contract.md`, `writing_brief.md`, and the positive excerpts. Judge in this order:

1. Does the candidate add an unsupported fact, action, cause, or absolute conclusion?
2. Do the opening, first paragraph under each H2, and ending sound like a natural explanation, or do they announce a topic, define it, and summarize its significance?
3. Can readers understand a concept's role and consequence when it first appears?
4. Did analysis scaffolding, editorial feedback, or QA language leak into the article?
5. Did the writer add decorative metaphors, slang, hypothetical failures, or unsupported detail to sound approachable?
6. Do section handoffs and whole-article rhythm work?
7. Does the title accurately state the subject and analytical increment, and does the article fulfill that promise?

Choosing the better candidate does not authorize paragraph splicing. Write `acceptance_audit.md` with the selection, evidence, and exactly one verdict:

- `ACCEPT`: Content and prose may proceed to Round 5.
- `RETRY_PROSE`: Thesis and structure are sound, but one complete rewrite can address specific prose blockers. Proceed to Round 4.
- `RETURN_TO_ROUND_1`: The problem lies in the thesis, evidence, structure, or source contract. The Main Agent must repair the upstream artifacts instead of labeling it a prose issue.

## 8. Round 4: One Optional Fresh Antigravity Retry

Run Round 4 only after a `RETRY_PROSE` verdict, and run it at most once. Use one fresh Antigravity conversation, never the candidate-generation conversation.

The Main Agent writes `revision_delta.md` with only the three to five highest-impact blockers. Each item identifies the original location, why it fails, and the correct direction. Do not attach the complete prose taxonomy again.

The Round 4 writer reads:

1. The selected candidate
2. `source_contract.md`
3. `writing_brief.md`
4. `voice_contract.md`
5. `revision_delta.md`

It returns one complete revised article and no QA commentary. The Main Agent repeats the deterministic and semantic acceptance from Round 3. If a non-surgical blocker remains, do not start another writer. Return to Round 1 or report that the article did not pass, avoiding an indefinite mutation loop.

## 9. Round 5: Logged Surgical Completion by the Main Agent

After acceptance, the Main Agent may directly fix:

- Typos, missing words, punctuation, and unambiguous grammar errors.
- Markdown, URLs, image paths, and alt text.
- Mechanical misspellings of proper nouns.
- Numbers, qualifications, or attributions with one uniquely correct form in `source_contract.md`.
- A local single-sentence issue that does not change paragraph purpose or claim strength.

Round 5 must not silently replace the thesis, reorder sections, splice candidates, or rewrite whole paragraphs without another acceptance cycle. Record every change in `completion_edits.md`. If a correction requires renewed judgment about structure or whole-article voice, Round 3 accepted the draft incorrectly; return to the appropriate earlier round.

**The gate only detects; it never hand-edits prose.** Round 5 handles only the mechanical five categories above. Issues that require prose judgment — banned metaphors or personification, spoken-word performance, meta-instructions or analysis scaffolding leaking into the body, a stiff or affected tone — are not Round 5 hand-fixes, even for a single sentence. The correct handling is to write these as blockers in `revision_delta.md` and re-run the designated writing model in a clean context (Round 4); the rewriter is always the writing model, never the Main Agent. The Main Agent "touching up" the writer's prose by personal feel is a repeatedly-corrected overreach, and its output gets reverted wholesale. The dividing line: mechanical fixes uniquely determined against `source_contract.md` (typos, numbers, paths) may be hand-edited; prose issues that require taste judgment must go back to the writing model.

## 10. Images

Images are a hard requirement for an external-facing deliverable and must reduce cognitive burden rather than decorate the page. An article shorter than 2,000 words needs at least one image. An article of 2,000 words or more needs two to three images.

Every generated image in the final Markdown must come from the image generation or redrawing tool available in the current workspace. Compress final assets to JPG or WebP with a long edge no greater than 1024 pixels and a file size below 200 KB. For quantitative visuals, the Main Agent must first draw or calculate the data accurately with deterministic tools, then use the available image tool for redrawing. Every image needs a relative path and meaningful alt text.

Visual style is a standing constraint: light background, elegant, simple, business. No dark themes, sci-fi look, purple, or high-saturation colors — a sci-fi visual lowers an external piece's credibility. Infographics carry the distinctions that are hardest to put into words (scope and boundary, lifecycle, parallel versus sequential relationships) and must stay faithful to the concept's real topology; don't linearize a genuinely parallel relationship into a pipeline for the sake of tidiness. Redraw a diagram whenever it reads as messy or misleading.

## 11. Final Verification and Delivery

Delivery is not just prose. The canonical file, the render form, the title, and the images all count toward "the article being right," carrying the same weight as a framing error. After the last edit, the Main Agent works through this checklist:

1. **Title** has been generated as a first-class artifact, not an afterthought; the title lives at the thesis/tension level, not the action level — an action-level title demotes a paradigm-level analysis to a tool introduction.
2. Scans the final file for numbers, URLs, images, H2 sections, leaked scaffolding terms, and Markdown problems.
3. **First-screen line-by-line scan** for prompt residue and leaked meta-instructions — an instruction to the writer like "replace the first sentence with…" is the thing most easily pasted into the body as if it were content.
4. **Language-consistency scan**: no machine-translation residue, no accidental code-mixing of languages within a sentence, terminology rendered consistently throughout; judge cumulative density by the reader's felt experience, not by flagging every line individually.
5. **Canonical path** is clear, with no stale known-bad draft sitting unmarked in the durable directory.
6. **Render form is faithful to the content**: the article is presented in its readable article form, not a stand-in chart; if pushed to a device or render endpoint, orientation, font, and size must be correct.
7. Confirms that the archived deliverable equals the accepted candidate plus the changes recorded in `completion_edits.md`.
8. Reads the final Markdown from the beginning with the available file-reading tool to trigger rendering and perform one last visual review.
9. Reports the final path and any residual risk.

If final verification finds a mechanical issue, repair it under Round 5 and reread the result. If it finds a non-surgical issue, do not deliver a failed article merely because the workflow reached its last step, and do not add more writers indefinitely. Return to Round 1 or report the blocker.

## 12. Codify Corrections Back Into the Skill

A meta rule the user has repeatedly emphasized: every correction should be codified back into this skill or the relevant config so the same error can't recur. The landing point of feedback is a reusable process asset, not a single edited paragraph. When a correction reveals that this skill is missing a rule or is ambiguous, edit this file — add a gate or a banned item — then rewrite the product from the updated rule. If you suspect the model-routing table lacks a role or is wrong, propose a config or skill change for the user's approval, and use an equivalent existing agent for the current session rather than unilaterally deviating from the routing table.
