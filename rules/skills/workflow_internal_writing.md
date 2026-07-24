# Internal Writing Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: Collaborators, AI agents, and project workflows that already share the same project or decision context. Covers research memos, decision briefs, work logs, and execution summaries.
- **Created**: 2026-06-11
- **Last updated**: 2026-07-23

---

## 1. When to Use It

Load this workflow when the audience shares context and the goal is to help them form a judgment, verify evidence, and decide the next step quickly.
*   For strangers without shared context, public channels, customers, or external course audiences, use `workflow_external_writing.md`.

AI has made the marginal cost of internal documents extremely low, but reader attention remains the bottleneck. The goal of form and layout is therefore to **reduce decision friction and give the reader the most actionable judgment in the same amount of time.**

### Shared Project Context Is Not Shared Vocabulary

An internal reader may know the project, its goals, and the decision at hand without knowing concepts introduced by the current round of work. Treat these as two separate questions:

*   **Project context**: Does the reader know why the project exists, what problem is being addressed, and what decision follows?
*   **Concept context**: Does the reader already understand the new terms, metrics, system boundaries, and causal relationships used here?

When project context is thick but concept context is thin, build the full chain of conceptual dependencies. Shared context lets you omit facts that are genuinely shared. It does not let you skip concepts created by the current work.

### Do Not Treat the Research Endpoint as the Reader's Starting Point

After research, the author holds a compressed set of categories, terms, and boundaries. They are useful for review and retrieval, but not for building a reader's first understanding. Do not ask the reader to begin where the research ended.

When explaining a technology or product the reader has not encountered, establish a mental model in this order. If the object has no linear runtime path, use a before-and-after contrast, timeline, role relationship, or causal chain instead of forcing a process:

1. **Start with a concrete scene.** For a runtime path, show how the system used to work. Otherwise, use a specific event, role conflict, or before-and-after contrast.
2. **Name the observable old problem.** State who pays more, loses state, chooses the wrong path, or cannot judge the return, rather than replacing the phenomenon with an abstract label.
3. **Show the new action.** Explain what the new object can save, constrain, compare, or recover before naming that capability for later reuse.
4. **Add product boundaries and strict terminology last.** Shipped versus roadmap, GA versus experimental, metric definitions, and implementation details matter, but not before the reader understands the problem.

If removing the terms still leaves the reader unable to describe how the object works or changes, where the problem is, and what the new approach changes, the document is a research summary rather than an explanation.

---

## 2. Information Order and Structure (Bottom Line Up Front)

Put the most important decisions and recommendations first. Do not list work chronologically or begin with extensive background.
The first screen must pass a comprehension gate. Within 15 seconds, the reader should be able to restate in plain language what happened and why it changes the current decision, then decide whether to continue and which section matters most. A first screen that requires guessing terminology, searching ahead for definitions, or reconstructing missing reasoning fails the gate.

Putting the conclusion first does not justify placing it before its prerequisites. If a conclusion depends on an unfamiliar concept, first provide one or two sentences of concrete facts, actions, or contrasts that create the minimum step needed to understand it. This context exists only to make the current judgment intelligible, not to provide a full domain overview.

### Establish a Testable Writing Contract

For an explanatory memo with a clear main question, rewrite the question as a testable contract before drafting, for example:

> After reading, the reader can explain in ordinary language why this appeared now, where the old approach falls short, and what the new object specifically adds.

The body length and order must serve this contract. Related but distinct questions such as product status, roadmap, adoption advice, or a full experimental protocol may have their own sections, but cannot compete for the main thread. Do not turn an explanatory memo into a benchmark RFC, product history, or feature list.

When the user explicitly requests several parallel deliverables, the contract must cover each one. A work log or execution summary may likewise use multiple contracts for status, evidence, risk, and next steps.

The first screen still previews the conclusion and recommendation. After it, explanations of a new technology or product normally proceed through three layers without jumping back and forth:

1. **Problem layer:** How did the old system work, and when did it become insufficient?
2. **Solution layer:** Which actions or boundaries does the new object change?
3. **Decision layer:** What is complete now, and what should we do?

The first screen may preview the decision, but shipped-versus-roadmap boundaries and recommendations should follow only after the problem and solution are understandable. A decision preview does not replace either layer.

### Restore Minimum Context
The reader may be switching between tasks and may not have the current context in mind. Open with one or two sentences that restore the minimum context: what the project is, what question this round addresses, and why it matters now.

### Recommended Conclusion Card Structure
```markdown
## Bottom Line

One-sentence conclusion.

## Why This Matters

Which judgment or action this affects.

## Recommended Action

What to do, or what not to do yet.
```

### Two-Layer Conclusions

For a complex topic, use two layers on the first screen:

1. **Plain-language layer**: State who did what, what changed or differs, and which decision that affects. A reader who knows none of the new terms should still be able to restate it.
2. **Technical-precision layer**: Once the meaning is established, add the metric name, system name, or strict qualification needed for precision.

Technical language cannot replace the plain-language layer. If removing the terminology leaves the sentence unable to explain what actually happened, the labels are standing in for an explanation.

### Put Qualifications Later, Without Hiding Them

Keep factual boundaries accurate, but do not stack version numbers, paper limitations, schema names, and release states before the core object exists in the reader's mind. Establish the main model in two or three sentences, then state what is complete and what remains unfinished.

The first screen may retain one most important boundary. Put other qualifications next to the claims they limit. Accuracy does not mean front-loading every caveat, and lower cognitive burden does not mean omitting them.

---

## 3. Concept Dependencies and Exposition Order

### Default Order

Introduce a new concept in this order unless the material gives a clear reason not to:

1. **Concrete actor, object, or action**: Who saved, deleted, read, or changed what, and when?
2. **Observable difference or conflict**: What differs between the options? After a failure, what can the reader no longer see, recover, or avoid paying for?
3. **Decision consequence**: Which choice, cost, or risk changes as a result?
4. **Name the concept only when useful**: Introduce a term or metric name only if later sections need to compare, retrieve, or repeatedly reference it.

Do not write in the author's post-research compression order of term, framework, conclusion. If a judgment depends on facts or concepts that have not appeared yet, reorder the material. A parenthetical definition after the term does not repair a broken dependency chain.

### Role, Scope, and Consequence Arrive Together

The first appearance of a new term, metric, or ratio must also tell the reader:

*   what it describes in the current problem;
*   which object, stage, population, or comparison baseline it covers;
*   whose behavior, cost, or result changes when it rises or falls.

Prefer actions, contrasts, and concrete consequences over dictionary-style definitions. For example, explain that a program can resume the previous task after restarting before naming that property recoverability, if the name is needed at all.

### First-Screen Concept Budget

The scarce resource on the first screen is not word count. It is the number of unfamiliar concepts the reader must hold in working memory at once. For every new label, ask whether it helps the immediate judgment. Move or remove names that exist only to classify later material, signal expertise, or compress the writer's phrasing.

Maximizing cognitive bandwidth is not the same as maximizing information density. Compression beyond the reader's existing conceptual structure saves words for the writer while increasing decoding work for the reader.

---

## 4. Skimmability

*   **Headings carry decision information**: Do not write `Findings` or `Notes`. Write the specific conclusion, such as "The task resumes after restart without repeating completed steps."
*   **Short paragraphs and explicit numbering**: Each paragraph should resolve one judgment point. When stating several parallel items, number them explicitly with `First... Second...` as required by `COMMUNICATION.md` language hygiene.
*   **Mobile scanning**: Optimize the first screen for a narrow phone display by default. Use short paragraphs and narrow tables that do not require horizontal scrolling.
*   **Language consistency**: Keep internal documents in one primary language. Retain only necessary API names, code identifiers, and metric names from another language.

*   **Separate explanation from protocol**: The body of an explanatory document builds the mental model. Experimental parameters, full field tables, budget details, and kill criteria that exceed the main question belong in a short recommendation, appendix, or separate RFC. If protocol material approaches or exceeds the explanatory thread, the document has drifted in type.

Skimmability is not the same as comprehension. Short paragraphs, tables, and cards can still pack too many unexplained concepts onto the first screen. After optimizing the visual scan, verify that the reasoning remains continuous. A layout does not pass if the reader must pause, reread, or search ahead for definitions.

---

## 5. Verifiability

Internal documents earn trust through verifiability. Put evidence links **next to the factual claim, code behavior, or historical conclusion they support.**
*   **Evidence forms**: Inline links, file paths such as `file:line`, commands, commit hashes, log or raw-data paths, and original excerpts.
*   **Placement**: Keep evidence beside the statement it supports. Do not collect all evidence at the end.

---

## 6. Adaptive Reading Trajectory

Do not assume the reader will spend either 30 seconds or 30 minutes. The same long document should support both scanning and auditing:
1.  **Scanning layer**: A one-sentence conclusion, takeaway, and status card on the first screen.
2.  **Deep-reading layer**: Detailed argument, rejected alternatives, long data, and implementation details. **Collapse these in `<details>` sections by default or anchor them at the end.**

The scanning layer may omit evidence details, but it may not omit the premises required to understand the conclusion. The deep-reading layer explains why to trust the claim; it should not repair undefined concepts from the first screen.

---

## 7. Low-Cognitive-Burden Acceptance Checks

Before delivery, audit the document from the reader's perspective:

1. **First-screen restatement**: After reading only the first screen, can the reader explain in plain language what happened and why it affects the decision? Repeating the document's terminology without explaining it does not count.
2. **First-appearance audit**: When each new term or metric first appears, are its role, scope, and observable consequence already present?
3. **No pre-reading required**: Does any sentence require material that appears later? If so, reorder the dependency chain instead of sending the reader to another section.
4. **Decoding-tax audit**: Is the reader spending effort judging facts and conclusions, or translating terminology, expanding acronyms, and guessing abstractions? Replace the latter with concrete actors, actions, and outcomes.
5. **Abstraction grounding**: Before words such as governance, recovery, transparency, boundary, capability, or efficiency appear, does the text show what was added, removed, made impossible, or made costly?
6. **Two-layer conclusion**: Does every technical conclusion have a plain-language version that does not depend on the new terminology?
7. **Concrete mental-model test**: Can a first-time reader explain how the object works or changes through an appropriate process, before-and-after contrast, timeline, role relationship, or causal chain?
8. **Causal-thread test**: Can the reader answer where the old system falls short, why this is happening now, and which step the new approach changes, rather than merely repeating product positioning?
9. **Research-compression reversal**: Does the document begin with the author's final terminology system? If so, restart from concrete actions and failure modes.
10. **Question-share test**: Does material that directly answers the question contract occupy most of the body? If feature lists, chronology, implementation boundaries, or protocols dominate, rebuild the structure instead of adding another summary.
11. **Three-layer separation**: After the first-screen preview, do problem, solution, and decision arrive in dependency order? Is the reader forced to decode GA, roadmap, or adoption advice before understanding the object?

---

## 8. Layout and Visual Components

Internal documents should actively use visual components to reduce the reader's cognitive burden.
*   When the document needs specific layouts such as status-card grids, adaptive tables, semantic chips, or dark-mode-compatible CSS, load and follow the [Internal Document Layout and Adaptive Visual Components Guide](./bestpractice_internal_visuals.md).
*   **Charts and diagrams**: Prefer PNG/JPG/WebP images. **Do not use inline SVG**, because mobile rendering is inconsistent.
*   **Mermaid** may serve only as a supporting view. It must not carry the only version of a core conclusion, and it requires a Markdown fallback nearby.
