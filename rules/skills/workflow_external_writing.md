# External Writing and Drafting Workflow

## Metadata

- **Type**: Workflow
- **Use when**: Turning verified research into an external-facing analytical article, public survey report, course asset, or client deliverable.
- **Prerequisite**: Phases 1-3 of `workflow_deep_research_survey.md`, or an equivalent verified factual record.
- **Last updated**: 2026-07-23

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
- Technical concepts become legible through actions and consequences, not glossary-style bilingual parentheticals.
- Make frameworks explicit only when they help the reader judge. Repeated patterns such as two axes, three layers, four items, or define-classify-explain-summarize are textbook voice unless the reader genuinely needs the framework.
- **The explanatory increment must be irreplaceable**: every core claim needs the chain of concrete action or scene, why the old arrangement existed, what the new action changes, and which consequence follows.
- **Anti-outline test**: with titles and H2s hidden, the body must remain a continuous argument. If reducing each paragraph to one sentence loses almost no information, return to Round 1.

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

- Every claim permitted in the article and the source that supports it, with stable claim IDs for later artifacts.
- Exact numbers, dates, versions, URLs, image references, and truly immutable product, protocol, or legal names. Do not mark ordinary analytical English as immutable wholesale.
- Attribution, measurement definitions, comparison baselines, and limits on extrapolation.
- Unknowns that the writer must not fill in.
- For any running example, which actions come from evidence and which may appear only as clearly hypothetical illustrations.

Do not provide a bare link list. State what each source supports.

### `writing_brief.md`

Include at least:

- Reader start state, reader takeaway, exact thesis, and article warrant.
- Article protagonist, current trigger, and first-screen promise.
- Continuity with the author's prior judgments: whether current evidence fills, revises, or contradicts an earlier view, with relevant public URLs when available.
- Claim dependencies, evidence order, and section handoffs. Unless locked by the user, do not prewrite final H2 wording or turn research taxonomy into the article outline.
- Concrete carrier, material that requires depth, and material deliberately omitted.
- Three to five title candidates from different angles, plus why the selected title accurately names both the subject and the article's increment.
- What new evidence would weaken or overturn the thesis.

### `voice_contract.md`

Keep the writer-facing voice instructions to roughly one page and specific to this article:

- Two or three sentences defining the desired narrative stance.
- One or two user-approved positive excerpts of similar explanatory difficulty, with a note on what to learn from each.
- Two or three likely failure excerpts from the current draft, with a direct diagnosis of what feels ceremonious, instructional, or performatively casual.
- Boundaries for first person, questions, technical density, and local lists.
- Do not use "very + adjective + colon" as an evaluative label before a fact; begin with the fact, action, or consequence.
- Do not use bilingual parenthetical glosses for ordinary concepts; explain necessary English terms in natural syntax.
- No more than eight high-impact voice constraints.

Do not paste an entire published article, a universal banned-word list, this workflow, `COMMUNICATION.md`, or the full prose guide into the writer context. Use `bestpractice_external_prose.md` to produce this short contract.

### `content_map.md`

The Main Agent writes a **fact-complete, prose-neutral** content map. Each block contains only the current concrete object or action, referenced claim IDs, the belief the evidence should change, the causal relation to the preceding block, the next question, and image placement. It may contain essential quotations and immutable numbers, but not continuous prose, paragraph entrances, summary sentences, final H2s, or analysis scaffolds.

`content_map.md` is neither a keyword outline nor a half-written article: the writer should not need to invent research, causality, or scenes, while three adjacent blocks should not paste into body prose. Before leaving Round 1, reconcile it against `source_contract.md` by claim ID.

**Anti-anchoring gate:** if `content_map.md` contains final titles or H2s, continuous paragraphs, definition-first openings, or copy-ready endings, rebuild it.

### Article-warrant gate

Before handing work to a writer, create `article_warrant_audit.md`: how the reader currently understands the problem, what must change, the concrete carrier, the first content block that answers why, and the block whose removal would reduce the article to a summary. If these answers are unavailable, rebuild the map.

### Reader-path gate

Create a short `reader_path_audit.md` before drafting. For each block, record the known object, one new relationship, the next question and handoff, and whether new terms can be restated in ordinary language. If readers must hold more than two ungrounded categories at once, rebuild the map and brief instead of asking prose to repair it.

## 6. Round 2: Two Independent Antigravity Candidates

By default, start two fresh Antigravity conversations in parallel. Both receive the same task packet and independently write `candidate_a.md` and `candidate_b.md`. For a very short article or an explicit single-version request, one candidate is acceptable, but never generate B by asking it to revise A.

Each writer reads only:

1. `source_contract.md`
2. `writing_brief.md`
3. `voice_contract.md`
4. `content_map.md`
5. Its own short round prompt

The writer returns the complete article only. It does not output an audit, explanation, invariant count, or `PASS` statement. Both candidates use the same facts and thesis; parallelism exists to obtain independent prose paths, not exaggerated style variants.

The Round 2 prompt should say only what is necessary:

- Draft from a blank page without adding facts, scenes, or causal claims outside `source_contract.md`.
- Preserve the thesis, claim strength, numbers, URLs, image references, and immutable terms.
- Decide paragraph entries, syntax, and H2 wording independently. Do not copy content-map labels or research taxonomies into the article outline.
- Advance through the concrete carrier rather than teaching the rules by category.
- Explain technical terms through what they are doing, not parenthetical glosses or definition-first entries.
- Write only the article.

Every call follows the file-based contract in `antigravity_cli.md`. Persist prompt, result, stdout, stderr, and events separately.

## 7. Round 3: Two-Stage Cold-Read Acceptance

The Main Agent is the only `PASS` authority, but a fresh isolated blind reader performs the first cold read. The Main Agent then makes its own factual and structural judgment.

### 7.1 Blind-reader audit

For each candidate, use a fresh context that reads only the candidate body, not source artifacts, this workflow, prior audits, chat history, or the web. It does not edit or fact-check. Write separate `blind_reader_audit_a.md` and `blind_reader_audit_b.md` files. At the first screen, each H2 entrance, and ending, record the known object/action/problem, new names or rules, why they appear now, and whether the next section catches the formed question. Run explanatory-increment and anti-textbook-voice rejection tests. Its verdict is diagnostic only.

### 7.2 Main Agent final acceptance

Before reading the blind-reader verdict, the Main Agent writes `main_cold_read_a.md` or `main_cold_read_b.md` from the candidate body alone. It then reconciles blind-reader findings, source artifacts, and positive excerpts in `acceptance_audit.md`, documenting any disagreement.

### 7.2.1 Deterministic checks first

Use scripts or direct comparison for:

- Numbers, dates, and versions.
- URL targets and image paths.
- Required and prohibited terms.
- H2 count and any required order.
- Markdown, word count, and output path.
- Candidate bilingual parenthetical glosses. Scanning locates candidates; the Main Agent decides whether an item is a necessary full name or redundant doubling.

Do not substitute a model-written natural-language audit for these checks.

### 7.2.2 Semantic acceptance second

Compare candidates with `source_contract.md`, `writing_brief.md`, and the positive excerpts. Judge in this order:

1. Does the candidate add an unsupported fact, action, cause, or absolute conclusion?
2. Do the opening, first paragraph under each H2, and ending sound like a natural explanation, or do they announce a topic, define it, and summarize its significance?
3. Can readers understand a concept's role and consequence when it first appears?
4. Did analysis scaffolding, editorial feedback, or QA language leak into the article?
5. Did the writer add decorative metaphors, slang, hypothetical failures, or unsupported detail to sound approachable?
6. Do section handoffs and whole-article rhythm work?
7. Does the title accurately state the subject and analytical increment, and does the article fulfill that promise?
8. Can readers restate each H2 opening through an already-known concrete object, rather than only a new term, category, or author label?
9. Do three consecutive paragraphs define, classify, explain items, or summarize abstractions without the same concrete object continuing to act?
10. Does deleting a bilingual parenthetical leave information unchanged? If so, retry prose; systemic use returns to Round 1.
11. Do analytical scaffolds need to be taught explicitly, or can the concrete comparison or action carry the argument without becoming H2s, lists, and a closing summary?

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

For any infographic with text, maintain `image_text_contract.md` listing every required heading, label, number, and prohibited variant. Inspect the final compressed image character by character at 100% size. Any typo, omission, changed number, or malformed product name requires regeneration before the image enters final Markdown.

## 11. Final Verification and Delivery

Delivery is not just prose. The canonical file, the render form, the title, and the images all count toward "the article being right," carrying the same weight as a framing error. After the last edit, the Main Agent works through this checklist:

1. **Title** has been generated as a first-class artifact, not an afterthought; the title lives at the thesis/tension level, not the action level — an action-level title demotes a paradigm-level analysis to a tool introduction.
2. Scans the final file for numbers, URLs, images, H2 sections, leaked scaffolding terms, and Markdown problems.
3. **First-screen line-by-line scan** for prompt residue and leaked meta-instructions — an instruction to the writer like "replace the first sentence with…" is the thing most easily pasted into the body as if it were content.
4. **Language-consistency and parenthetical scan**: no machine-translation residue or accidental code-mixing; choose the needed Chinese or English body name without repeating the same meaning in bilingual parentheticals.
5. **Canonical path** is clear, with no stale known-bad draft sitting unmarked in the durable directory.
6. **Render form is faithful to the content**: the article is presented in its readable article form, not a stand-in chart; if pushed to a device or render endpoint, orientation, font, and size must be correct.
7. Confirms that the archived deliverable equals the accepted candidate plus the changes recorded in `completion_edits.md`.
8. Reads the final Markdown from the beginning with the available file-reading tool to trigger rendering and perform one last visual review.
9. Reports the final path and any residual risk.

If final verification finds a mechanical issue, repair it under Round 5 and reread the result. If it finds a non-surgical issue, do not deliver a failed article merely because the workflow reached its last step, and do not add more writers indefinitely. Return to Round 1 or report the blocker.

## 12. Codify Corrections Back Into the Skill

A meta rule the user has repeatedly emphasized: every correction should be codified back into this skill or the relevant config so the same error can't recur. The landing point of feedback is a reusable process asset, not a single edited paragraph. When a correction reveals that this skill is missing a rule or is ambiguous, edit this file — add a gate or a banned item — then rewrite the product from the updated rule. If you suspect the model-routing table lacks a role or is wrong, propose a config or skill change for the user's approval, and use an equivalent existing agent for the current session rather than unilaterally deviating from the routing table.
