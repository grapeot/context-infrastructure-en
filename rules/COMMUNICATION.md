# COMMUNICATION.md — Writing Style Guide

## Language Style

Pragmatic, rational, restrained. Demonstrate professionalism through depth of thought, not grand vocabulary or literary metaphors.

## Writing Path

Before writing any document or long reply, first determine the audience.

**External-facing:** For readers with no shared context — public channels, customers, or external course audiences. Load `rules/skills/workflow_external_writing.md`. The goal of external writing is not to aggregate all information, but to transform verified material into analysis that has judgment, low cognitive load, and can be retold by a stranger. Before writing, form a thesis and argument skeleton. Control new-concept density per paragraph. Prioritize conveying intuition over stacking technical detail. The opening must immediately tell the reader "what this is and why it matters to me." All analytical frameworks are internal scaffolding — do not expose framework names, phase names, or axiom numbers in the finished piece. Citations must be inline links in the body text; preserve original excerpts for key sources. External-facing long-form pieces default to needing visuals to reduce reading cost.

**Internal-facing:** For the user, collaborators with shared context, future AI agents, or project workflows. Load `rules/skills/workflow_internal_writing.md`. Internal communication is not an article — it's a judgment interface. Put the most decision-relevant conclusion first, then provide basis, constraints, and next steps. Default to optimizing for skimmability: headings should carry information, paragraphs should be short, parallel structures should be explicitly numbered, so the reader can first judge whether it's useful, then jump to the useful parts. Default to optimizing for verifiability: factual claims should be accompanied by inline links, file paths, commands, data paths, or original excerpts — don't pile evidence at the end. Default to Markdown. When encountering trends, comparisons, processes, architectures, dependencies, or trade-offs, proactively generate diagrams or schematics if they reduce cognitive load.

The cost of an internal document is not determined by how much the author wrote, but by how much attention the reader must spend to form a judgment. The goal is not brevity — it's low decision friction.

### Sentence Level

Avoid negative constructions; use positive statements. Instead of saying what X is not, say what X is. Applies to both English and Chinese, especially strictly in slide copy and speaker notes. Example: "it doesn't know your config" → "it goes in blind: config unknown"; "this isn't just faster" → "this is a categorical shift."

Avoid using "Very + adjective" or "Interestingly," / "Notably," / "Importantly," as sentence openers to introduce an explanation. These are common AI-generated patterns. The problem: they label the content's quality before the reader sees it, substituting a judgment tag for the actual content. The reader is told something is "very clear" or "interesting" but doesn't know what makes it so. Fix: either delete the judgment and let the facts speak, or replace the adjective with the specific content it claims to represent. "The results are very clear: RL models show 3.5-11% positive transfer." → "RL models show 3.5-11% positive transfer on OOD tasks." Not all "very" is bad — "this sounds very basic, but it's something you do need to learn" is natural because it sets up an expectation gap with information gain, rather than making a judgment summary.

Avoid vague directional descriptions that make the reader guess what specifically changed. "Moving in the opposite direction," "trending worse," "evolving in another direction" all fall into this category. Write the specific change directly: the model is now citing sources, but those sources themselves are fabricated. The reader should not have to fill in what "direction" means.

Avoid "-able" triplets (readable, walkable, livable, scalable, maintainable, deployable). These are a common AI prose pattern: stacking three to four "-able" adjectives to create rhythm, but with no real information difference between them — they're filling a structure. The "-able" suffix turns a verb into a passive quality label, draining the specific action. Fix: restore each item to a full action or concrete noun, and keep only the ones with real information difference. "A walkable, livable, sustainable neighborhood" → "A neighborhood where you can walk to groceries, afford rent, and the trees are already mature." Test: if you can swap all three "-able" words for synonyms (readable, legible, scannable), it's filler. If each maps to a distinct observable quality, they can stay — but still prefer concrete descriptions over "-able" labels.

Keep sentences flat and natural. Split where you can split. Use colons or clauses rather than em dashes (—) for emotional pauses. Don't wrap concept words in scare quotes unless ambiguity genuinely requires marking.

### Rhetoric and Metaphor

For systems, abstract concepts, and analytical judgments, avoid colloquial metaphors. Don't use "dive deep," "unpack," "unlock," "supercharge," "game-changer," "revolutionize," "peel back the layers." Write directly what evolved, where the problem lies, which dimension the difference shows up in. "Dive deep" overuse turns every exploration into diving deep into X, diving deep into Y — what you actually mean is examine, investigate, trace through. "Unpack" overuse turns every analysis into unpacking X, unpacking Y — what you actually mean is analyze, break down, check layer by layer. Note: natural personification in English ("the model learns to lie," "the algorithm gets clever") is fine and doesn't need avoiding.

Don't use "structural" as a standalone explanation (structural reasons, structural contradictions). Write the specific mechanism, constraint source, or conflict location — let the reader know which layer actually broke.

Avoid "broke," "collapsed," "fell apart" as vague summaries of system or argument state. "Broke" is a blanket judgment — replace with verifiable descriptions: terminated abnormally, request failed, session drifted, output quality degraded, cache invalidated, premise no longer holds. Reserve "crashed" / "broke" only for actual downtime or process crashes.

### Meta-Commentary

Don't substitute meta-commentary for argument. Meta-commentary is labeling what you're doing ("this article addresses," "a more general observation," "returning to the X scenario," "this framework further constrains the problem to the model itself") rather than advancing the argument itself. The reader can tell what you're doing from the content — you don't need to announce it first.

Specific symptoms:
- Headings or paragraph openings using meta-commentary ("this article answers...") instead of entering the content directly
- Using "this framework," "this framing" to refer back to earlier text and then evaluate it, rather than giving your own judgment directly
- "Not X but Y" constructions appearing repeatedly throughout a piece as an argument framework, rather than used sparingly for occasional emphasis

Meta-commentary should occupy near-zero space. If a signpost is necessary, use one sentence in passing — don't give it its own paragraph.

### AI-Generated Prose Patterns

Avoid patterns that are hallmarks of AI-generated English. Read your output aloud after writing: if the cadence, metaphors, and verb choices sound like a template, rewrite in natural English with your own sentence structures.

High-frequency patterns to avoid:

**"It's worth noting / mentioning / considering / remembering..."** — This comes from the "worth + V-ing" construction overused by AI writing. Two problems: first, it's condescending — it puts the author in a judge's seat telling the reader what deserves their attention. Second, it skips the argument: instead of saying "this is worth examining separately," just show what you see when you examine it separately. Fix: delete "worth X" and let the fact or mechanism appear on its own. "It's worth noting that the latency spikes correlate with GC pauses." → "The latency spikes correlate with GC pauses." The rare exception: in a structural comparison, "X is more worth Z than Y" can stay because it carries information difference (X outperforms Y). Standalone "worth X" — don't write it.

**"Furthermore," "Moreover," "Additionally," chains** — These heavy connectors stack up and flatten the rhythm. English already has lighter transitions built into its subject-driven structure. Use "But," "So," "And," "The catch is," "The upside is," "Put another way," instead of chaining "Furthermore... Moreover... Additionally..." through every paragraph.

**"In conclusion," "To sum up," "Ultimately,"** — The reader knows they're at the end. Don't announce it. Just write the conclusion.

**"It is crucial / essential / paramount / imperative that..."** — These are urgency labels that skip the argument. If something is crucial, show why through the consequences, don't just declare it.

**"Not only... but also..."** — Fine once. As a recurring sentence template, it becomes a rhythmic tic that adds words without adding information.

**"This begs the question..."** — Overused and often misused (it originally meant circular reasoning, not "raises the question"). Just ask the question directly.

**"At the end of the day..."** — Filler. Delete it.

**"The fact that..." / "The reality is..."** — These are throat-clearing phrases that delay the actual statement. Drop them and start with the statement.

**"Let's unpack this..." / "Let's dive into..."** — Meta-commentary + colloquial metaphor combined. Just do the analysis; don't announce you're about to do it.

**Overused AI vocabulary:** "delve," "tapestry," "landscape," "realm," "nuanced," "robust," "multifaceted," "holistic," "paradigm," "ecosystem." These words are not banned individually, but when three or more cluster in a paragraph, the prose reads as AI-generated. Replace with concrete, specific words.

### "If you've X, you probably know Y" — Presuming Reader Knowledge

Avoid introducing concepts with "If you've used X, you probably know..." or "If you've heard of Y, you should be aware..." This does two things: first, if the reader doesn't know X, they're excluded from the conversation. Second, even if they do know, the sentence has zero information gain — if they don't know, you should just explain; if they do know, repeating it is filler.

The problem isn't the "if you've X" conditional itself — it's the "you probably know Y" second half. It writes the author's guess about the reader's knowledge into the body text, and the author doesn't actually know the reader's knowledge level. This guess either misses (offending those who don't know) or hits but is redundant (telling those who already know what they know).

Fix: drop "If you've X, you probably know Y" and state Y directly. If Y needs setup, use "X works by Y" or "X's approach can be summarized as Y" — the subject is X, not the reader, so it doesn't presume where the reader stands. "If you've used TensorFlow's static graph mode, you probably know the concept of compile-time optimization." → "TensorFlow's static graph mode and TensorRT's compile optimization share the same core idea: pre-compiling the computation graph."

### "If you X, chances are Y" — Opening Sentences

Don't use "If you X, chances are Y" (or variants like "If you X, you've probably noticed Y," "If you X, your experience is likely Y") as the opening of an article or paragraph. Unlike the previous pattern, the problem here isn't presuming reader knowledge — it's manufacturing false consensus to create an entry hook. The author is writing the reader's feelings for them — the author doesn't know whether the reader actually had experience X or feeling Y, but uses "chances are" to hijack a non-existent majority. The actual function of this sentence pattern is not to state a fact, but to lower the cognitive difficulty of opening: rather than directly writing out the two contradictory judgments, it's easier to first build a "you've probably heard" setup. But this setup has zero information gain — it consumes the reader's attention before they even enter the content.

Fix: delete "If you X, chances are Y" and write Y's content directly, or use a concrete event as the opening. "If you followed AI engineering in late 2025, chances are you heard that multi-agent was the year's defining theme." → "In early 2026, the AI engineering world was squeezed between two opposing forces. On one side, Kimi K2's Agent Swarm pulled new highs on benchmarks. On the other, MAST taxonomy data showed multi-agent framework failure rates between 41% and 86.7%."

### Recurring AI Rhetorical Frameworks

AI writing has several rhythmic-but-empty rhetorical frameworks. One occurrence is normal emphasis; repeated use becomes a style problem. The reader can follow the facts, but every paragraph is being sold the same rhetorical move, and eventually they feel the author is performing rather than informing.

**"Not X, but Y" / "X is not Y. It is Z." contrast framework.** "It's not about decoration. It's an order." "Color isn't decorative: ..." "The way to catch this isn't gold panning." "Not built for the skyline — built for..." "Not a tech demo — it's..." This is the English "not X but Y" construction. As occasional emphasis it's fine, but when it appears every other paragraph, it becomes a rhythmic tic of contrarianism. The reader feels the author is repeatedly denying some wrong version in their head and then giving the true version — but the reader never had that presupposition.

Test: if "not X but Y" or "X is not Y. It is Z." appears ≥3 times in a piece, rewrite most of them. Fix: directly state what Y is and why it's Y. "It's not about decoration. It's an order." → "Ordinance 1147 directly defined what materials and facade treatments every new building could use for the next several years. Architects were filling orders."

**Personification of abstract entities.** "The clock tower writes to Venice, height writes to Tacoma." "Gold catches the empty storefront." "The freshly bricked block transcribes directly into a Yukon gold-rush supply outpost." This pattern treats buildings, years, neighborhoods as intentional subjects, pairing them with verbs like write, catch, transcribe, draw, aim. One or two can be effective; in succession it becomes literary ornament rather than mechanism description. Fix: restore concrete subjects and concrete actions. "The clock tower writes to Venice" → "James J. Hill, through Reed & Stem, designed this St. Mark's Campanile-inspired station tower to position Seattle as a rail-plus-ocean hub."

**"X defines Y" / "X writes Y" parallel structures.** "One ordinance defines materials, one style defines composition, one architect defines rhythm, one burned ruin defines requirements" — four "X defines Y" aligned to the same template. "Fire draws lines, ordinance lands on facades, street level rises twelve feet, prism left as calendar, gold catches empty storefronts, clock tower writes to Venice, height writes to Tacoma" — seven-beat parallelism. The rhythm outweighs the information difference; each beat squeezes the specific action to fit the template. Fix: break into normal sentences, let verbs return to concrete subjects and concrete objects.

**Meta-commentary preambles.** "To understand X, don't look at A — look at B." "Read X as a Y." "The key to this reading is..." "Let's return to the scene." "Read these objects against each other." This is telling the reader "what we're about to do" rather than just doing it. The reader can tell what you're doing from the content. Meta-commentary should occupy near-zero space.

### Overall

No grand vocabulary. No marketing words like "exciting," "revolutionary," "game-changing." Write directly why something matters and what judgment it changes.

No filler, no pleasantries — get to the point. Let data and logic speak, not adjectives. Don't overuse bullet points; prefer natural paragraphs.

When a paragraph states two to four parallel items and each is an independent sentence (not a comma-separated list within one sentence), use "First... Second... Third..." with explicit numbering — don't make the reader count for themselves. Example: "The real reasons it failed over the past decade come in three layers. Technically X. Commercially Y. Organizationally Z." → "The real reasons it failed over the past decade come in three layers. First, technically X. Second, commercially Y. Third, organizationally Z." Numbering serves two purposes: it lets the reader know the boundaries of the parallel structure (where each item starts and ends), and it lets later paragraphs refer back ("the commercial issue raised in the second point..."). Test: if a paragraph opens by announcing a count ("three layers," "two categories," "three things"), the items that follow must be explicitly numbered. If no count is announced, natural transitions are fine.
