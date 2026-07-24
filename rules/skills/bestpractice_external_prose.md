# External Prose Diagnosis and Voice Contract Guide

## Metadata

- **Type**: Manager Reference
- **Use when**: The Main Agent needs to diagnose narrative distance, cognitive load, or paragraph architecture in an external article and produce a roughly one-page `voice_contract.md`.
- **Restriction**: Manager-only. Never pass this complete guide to a prose writer.
- **Last updated**: 2026-07-23

## 1. Boundary and Editorial Responsibility

This is a diagnostic guide for the Main Agent, not writer context. Natural prose is not what remains after satisfying hundreds of prohibitions. Giving a writer a taxonomy of failures, years of feedback, and an exhaustive style manual dilutes the voice target and encourages audit or lecture language.

The Main Agent has three responsibilities:

1. **Diagnose stance and architecture**: identify why the draft sounds ceremonious, instructional, cognitively overloaded, or artificially casual.
2. **Distill the contract**: turn evidence from the current article into a `voice_contract.md` of roughly one page.
3. **Cold-read acceptance**: judge the complete reading experience and distinguish a whole-article voice failure from a surgical local defect.

## 2. Narrative Stance: State the Finding Directly

Good external prose establishes peer distance. The writer addresses a smart reader who lacks this article's private context and explains a verified change or finding directly.

Diagnose two opposite failures:

- **Textbook voice**: announce the topic, define the object, explain the mechanism, then summarize its abstract significance. The reader becomes a student receiving a lesson.
- **Performative casualness**: use slang, exaggerated metaphors, fake dialogue, or excessive second person to imitate intimacy while leaving the mechanism unclear.

The target stance keeps the writer and reader focused on the same concrete object. It advances through actions, constraints, and consequences; introduces concepts when they become necessary; and places judgments after evidence. Any running scene must come from `source_contract.md` or be marked explicitly as hypothetical. Naturalness never licenses invented incidents, user reactions, or causal detail.

Sentence rhythm should breathe. Longer sentences can connect causes and examples; shorter ones can land judgments. Enter through a fact or conflict unique to this article. Let paragraphs end on an observable consequence or genuine open question instead of forcing a grand conclusion.

## 3. Information Architecture and Cognitive Comfort

Voice problems often begin as architecture problems.

### Concept dependency

Avoid defining an abstraction before the reader has a reason to care. A smoother sequence starts with a real constraint or action: when the system stalls, what someone does, and what changes. Name the concept when it resolves or explains that sequence.

### Cognitive comfort

A draft can define every term and still overload the reader. If a paragraph requires several ungrounded classifications, comparison axes, or components to remain active in working memory, the reader must pause, reread, or draw the relation. Reorder the material around one concrete carrier rather than splitting the same overload into shorter sentences.

### Local map rule

When readers genuinely need to compare three or more finite alternatives or parallel items, state the total set and shared comparison basis before expanding it. A numbered comparison is not automatically textbook voice; omitting the local map can impose more cognitive cost.

### Section handoffs

Hide adjacent H2 headings and read the end of one section into the beginning of the next. A natural handoff follows the same object's next action, a boundary exposed by the mechanism, or the consequence of the previous choice. If only the heading supplies the connection, rewrite both ends as a pair.

### Pattern phrases are signals, not a banned-word list

Phrases such as "X is a...", "to understand X, first understand Y", or "this shows the broader significance" often signal definition-first openings, abstract subjects, or summary tails. Diagnose and rebuild the paragraph's movement. Synonym replacement does not fix the architecture.

### Over-compression is not low cognitive burden

Another common failure compresses an article into "institution plus one verdict," "jurisdiction plus one difference," or "recommendation plus one checklist." The facts may be correct, but the reader never follows the causal chain from the old arrangement through a concrete action to a new consequence. Lower cognitive burden does not mean deleting explanation. It means that at any moment the reader follows one changing object. If reducing each paragraph to one sentence loses almost no information, the draft is a correct outline, not an article.

### Parenthetical translation is not terminology explanation

Doubling terms such as "observability (可观测能力)" or "provenance（来源链）" often proves only that the writer knows both labels. Except for formal names, acronym expansion, quotations, or a first name with genuine retrieval value, do not use `Chinese (English)` or `English (Chinese gloss)`. Choose one body term and let the surrounding actions explain it.

Parenthetical density is also an early signal of translationese. If deleting the parenthetical loses nothing, delete it. If deleting it breaks comprehension, rewrite the relation rather than retaining a glossary entry.

### Analytical frameworks must melt into the article

Timelines, two axes, three layers, four questions, and six-item checklists can help the Main Agent think, but they cannot automatically become H2s, images, body lists, and closing summaries at once. Make a framework explicit only when readers need it to judge, or when it compresses a conflict already established in the body.

Use a scaffold-deletion test: remove labels such as "two axes" or "three layers." If concrete objects, actions, and consequences no longer carry the article, it has no narrative spine. If they do, retain only the one explicit framework that lowers cognitive burden.

## 4. Produce the Voice Contract

Keep `voice_contract.md` to roughly one page and include only evidence relevant to the current article.

- **Positive excerpts**: one or two real excerpts the user has explicitly approved, chosen from work with similar explanatory difficulty. Note the pacing or narrative movement to learn, not sentence templates to copy.
- **Current-draft hazards**: two or three representative excerpts from the current draft. Diagnose the exact problem in the entry, progression, or ending.
- **Boundaries**: state what this article permits for first person, questions, technical density, lists, and local maps.
- **Constraints**: no more than eight high-impact instructions specific to this draft.

Use this template:

```markdown
# Voice Target

[Two or three sentences: who is explaining what to whom, and at what narrative distance?]

## Positive Excerpts

[One or two approved excerpts]
- **Learn**: [The movement, pacing, or explanation behavior to absorb]

## Current-Draft Hazards

[Two or three representative failed excerpts]
- **Diagnosis**: [Definition-first entry, performative metaphor, abstract summary tail, or another specific failure]

## Boundaries and Constraints

- [First-person and question boundary]
- [Technical density and explanation depth]
- [Local-map and finite-comparison boundary]
- [Terminology boundary: choose one body term; do not use glossary-style parenthetical translation]
- [No more than eight article-specific constraints total]
```

## 5. Manager Cold-Read Check

Ignore generation commentary and audit claims. Read the candidate itself.

Factual fidelity is a hard gate: numbers, dates, URLs, proper nouns, attributions, and qualifications must match `source_contract.md`. Unsupported incidents, psychological guesses, and absolute extrapolations fail immediately.

For voice and cognitive comfort, ask:

1. Does the opening share a concrete finding, or announce what the article will teach?
2. With H2 headings hidden, do sections still follow one another naturally?
3. When a concept first appears, can the reader understand its role and consequence?
4. Must the reader hold several unattached classifications or axes at once?
5. Before three or more options appear, does the article provide their count and comparison basis?
6. Does approachability come from a clear mechanism, or from slang, decorative metaphors, and invented detail?
7. Do three consecutive paragraphs define, classify, explain items, or summarize abstractions without the same concrete object continuing to change?
8. Does the article contain bilingual parenthetical translation that can be deleted without losing information?
9. Has a taxonomy used for analysis been copied directly into H2s, lists, and the ending instead of melting into the narrative?

A natural, comprehensible article may need a few surgical edits even if it contains an occasional pattern phrase. Conversely, a draft can avoid every flagged phrase and still fail because its whole rhythm remains "announce, define, summarize." Treat the latter as `RETRY_PROSE` or `RETURN_TO_ROUND_1`, not as a word-replacement task.
