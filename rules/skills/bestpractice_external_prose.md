# External Article Prose and Rhetoric Guide

## Metadata

- **Type**: BestPractice
- **Use cases**: Long-form articles, reports, and blog posts for strangers without shared context, public channels, customers, or external course audiences.
- **Created**: 2026-07-06
- **Last updated**: 2026-07-16

## Core Design Philosophy

The first principle of external writing is to **reduce decision and cognitive friction for an unfamiliar reader**. At the sentence and word level, remove AI-sounding prose, translation-like phrasing, and inflated false consensus.

---

## 1. Rhetoric, Metaphors, and Abstract Labels to Avoid

For systems, abstract concepts, and analytical judgments, describe the mechanism and difference directly. Avoid colloquial action metaphors, literary language, and labels without concrete referents:

*   **Colloquial action metaphors (prohibited throughout the article)**: This prohibition applies to the entire article. Do not use "grow out of," "grow into," "unpack," "break through," "pierce," "lock in," "rock solid," "sharp," or similar action metaphors anywhere in place of explanation.
    *   *Rewrite*: Replace the metaphor with a mechanism. "Breaks through the assumption" becomes "invalidates the assumption" or "the boundary no longer holds." "Unpack" becomes "analyze," "separate into layers," or "check item by item."
*   **Structural as an explanation**: Do not use vague labels such as "structural reason" or "structural contradiction."
    *   *Rewrite*: State the underlying mechanism, source of the constraint, or location of the conflict.
*   **Narrative arc as a placeholder**: Do not use "narrative arc" to avoid stating how an article or event develops.
    *   *Rewrite*: State the sequence and what drives it.
*   **Vague system-state words**: Avoid words such as "collapsed," "broke," or "couldn't hold" as summaries of a system or argument.
    *   *Rewrite*: Use verifiable descriptions such as "terminated abnormally," "the request failed," "the session drifted," "the premise no longer holds," or "the state cannot be maintained."

---

## 2. Translation-Like Prose and Meaning Mismatch

Do not mechanically transfer the semantic range of a word from another language. Common mismatches include:

*   **expensive / cheap**: For abstract trade-offs, use "high cost," "low cost," "high consequence," or "low consequence" rather than vocabulary reserved for a product's price.
*   **natural**: Distinguish "not artificial" from "inherent," "built in," or "native to the system."
*   **model / framework**: Distinguish machine-learning models from a mental model, line of reasoning, evaluation method, or conceptual framework.
*   **Literal metaphor translation**:
    *   Replace "stand on a layer" with "belongs to a layer."
    *   Replace "serves X" when necessary with the concrete audience or purpose it addresses.
    *   Remove "an uncomfortable fact" preambles. State the fact directly or say that it contradicts the prevailing narrative.
    *   Replace "blast radius" outside a necessary technical context with "scope of impact."

### No Redundant Bilingual Parentheticals

When the article's primary language already expresses a concept clearly, do not immediately repeat an English translation in parentheses. Forms equivalent to a translated ordinary concept followed by its English gloss add visual noise, create a translation-like cadence, and become a template that models repeat across articles.

Use the article's primary language for ordinary concepts without a parenthetical gloss. Preserve official product names, API names, protocol names, code identifiers, and standard industry abbreviations, such as `Turso Sync`, `push()`, and `RLS`. If the English term is more common than its translation, use the English term directly and explain it naturally once; do not turn the sentence into a bilingual lookup table.

A bilingual form is justified only when the article analyzes translation differences, resolves terminology ambiguity, or gives readers the original phrase needed to find primary sources. In those cases, state why the original term matters rather than silently appending it.

---

## 3. Article Openings, Presumptive Patterns, and Article-Wide Prohibitions

Do not pull the reader in through false consensus or a superior tone:

*   **"If you X, chances are Y" openings**: Do not use this pattern to open an article or paragraph. It manufactures consensus without adding information.
    *   *Rewrite*: State the fact directly or open with a concrete event.
*   **"If you X, you probably know Y" reader assumptions**: This excludes readers who do not know Y and wastes the time of readers who do.
    *   *Rewrite*: State Y directly with the objective subject as the grammatical subject.
*   **"Worth noting/considering/remembering" recommendations (prohibited throughout the article)**: This prohibition applies to the entire article, not only its opening. Do not use "worth noting," "worth considering," "worth remembering," or other "worth + X" expressions anywhere in the article. Do not tell readers which facts deserve their attention.
    *   *Rewrite*: Remove the label and present the fact or mechanism directly.

---

## 4. Downgrading Template-Like AI Rhetoric

AI systems frequently repeat these rhetorical templates. Replace or reduce them:

*   **"Not X, but Y" contrast**: If it appears three or more times in one article, rewrite it.
    *   *Rewrite*: State Y directly or use a light contrast such as "less X, more Y" or "X appears on the surface; the constraint is Y."
*   **Personification of abstract subjects**: Do not give buildings, years, neighborhoods, or systems intentional actions such as "writes to," "catches," or "draws a line."
    *   *Rewrite*: Restore the concrete actor and action.
*   **Mechanical parallelism**: Avoid repeated sentence templates such as "one rule defines materials, one style defines composition." Split them into ordinary sentences.

---

## 5. Prose Bad-to-Good Pairs

When drafting external articles, the main thread and writing agents should use these pairs to calibrate sentence structure and vocabulary:

### Pair 1: Split Overloaded Modifiers
*   ❌ **Bad**: The migration, cleanup, and boilerplate work that appears inefficient when viewed only through time spent becomes free in the AI era.
*   ✅ **Good**: These tasks look low-value on a schedule. A manager may classify them as inefficiency. For the brain, they still matter.

### Pair 2: Replace Elevated Words and Abstract Subjects
*   ❌ **Bad**: The release of this technology produced a stronger sense of fatigue, significantly correlating with user cognitive overload through a mechanism of critical importance.
*   ✅ **Good**: People became more tired after the technology arrived. Their attention was overloaded.

### Pair 3: Soften the Not-X-But-Y Contrast
*   ❌ **Bad**: You are not doing more physical work, but remaining in a high-cognitive-bandwidth state for longer.
*   ✅ **Good**: You are doing no more physical work. You are simply spending longer in a high-cognitive-bandwidth state.

### Pair 4: Replace a Presumptive Hook
*   ❌ **Bad**: If you followed AI engineering in early 2026, you probably heard that multi-agent systems were the major trend.
*   ✅ **Good**: Early 2026 put two opposing signals in front of AI engineers. Swarm systems set new benchmark highs while production frameworks continued to report high failure rates.

---

## 6. Explain Like a Person, Not a Textbook

Low cognitive burden means more than making every sentence understandable. Factually correct, concise prose can still read like a product manual when it repeatedly defines an object, announces an effect, and closes with an abstract category. The reader understands each sentence but never feels the writer discovering the problem with them.

Friendliness does not come from slang, forced second person, or decorative metaphors. It comes from narrative distance: the writer and reader face the same concrete problem, then follow the anomaly, question, and reasoning together. Concepts appear when an action makes them necessary rather than arriving in glossary order.

### 6.1 Do Not Turn Concept Introduction into Dictionary Definitions

These sentence forms are not prohibited individually, but repetition within a paragraph usually signals manual-like prose:

- "X is a product that allows users to..."
- "X refers to... Its primary role is..."
- "This adjustment changed or affected..."
- "This sparked a discussion about X."
- "In this process, system, or perspective..."
- "This provides a foundation for X."

Do not repair them by replacing synonyms. Ask what the reader wants to know now, who did what, what changed, and which judgment became impossible after the change. Writing those answers usually introduces the concept naturally.

*   ❌ **Bad**: Codex is an open-source local coding-agent client that allows developers to invoke models in their local environment.
*   ✅ **Good**: Codex reads and writes files on your computer, runs terminal commands, and stores execution records locally. When something fails, developers usually trace those records backward.

*   ❌ **Bad**: This adjustment directly affected local auditability.
*   ✅ **Good**: The problem appears when you investigate a failure. You can see the main agent create a subagent and inspect what the subagent later did, but the instruction between those events has become ciphertext.

The good examples demonstrate a transformation, not reusable openings. Do not turn their phrases into a new template.

### 6.2 Sentence Rhythm Must Not Become a Status Feed

Short sentences reduce local burden, but repeated subject-plus-is/can/will definitions create a broadcast rhythm. Natural explanation mixes lengths: short sentences land judgments; longer ones connect causes, examples, and contrasts. Do not split a coherent paragraph into five identical statements to satisfy a word-count target.

The test is not average sentence length. Read the prose aloud. If every sentence could stand alone in product documentation but none sounds like one knowledgeable person explaining a problem to another, rewrite the paragraph instead of splitting it further.

### 6.3 Ground Abstractions in Observable Consequences

"Reduced transparency," "blocked auditing," and "changed information boundaries" can summarize a paragraph but cannot replace the explanation. Before naming the abstraction, show what the reader can and cannot observe: the agent creation remains visible but its assigned task does not; command execution remains visible but its cause does not; tool records can be replayed but the complete causal chain cannot be reconstructed.

### 6.4 Reduce Narrative Distance

Prose can avoid long sentences and rare words while still sounding institutional. Common causes include invented role nouns, nominalized actions, system-centered result statements, and abstract losses:

- Replace `the client and its operator` or `the receiving entity` with the actual person, such as `you` or `the developer`, or remove the subject.
- Replace `perform encryption of the state` and `complete distribution of the task` with `encrypt the state` and `send the task`.
- Replace `causes the local log to become unable to display the content` with what happened and what the reader sees.
- Replace `loses a critical causal input` with the missing information and the two errors that can no longer be distinguished.

Second person is not the criterion. Ask whether someone who knows the problem would explain it this way to an intelligent reader. Do not simulate closeness with slang, memes, exaggerated metaphors, or filler.

### 6.5 Do Not Write the Editing Conversation into the Article

An editor's confusion usually diagnoses a missing prerequisite. It does not automatically belong as a heading, rebuttal, or paragraph center. A new reader who never saw the discussion will otherwise encounter a refutation of a claim nobody made.

*   ❌ **Bad**: Choosing 1.7B does not mean selecting the winner of two training results.
*   ✅ **Good**: Before a GPU job starts, it must choose either the 0.6B or 1.7B checkpoint. The growing share of jobs that chose 1.7B therefore shows a change in training-budget allocation.

After editing, hide the conversation and read only the article. If the reader cannot tell why a sentence answers or rejects something, restore the missing sequence, roles, and consequences instead of preserving the rebuttal.

### 6.6 Aim for Natural Explanation, Not Informality

A natural explanation usually begins with this article's specific contrast, question, or observation; follows a real process; introduces concepts when actions make them relevant; lets the writer appear only to state a genuine judgment; and ends each section with who waits, what moves, which capability disappears, or where the cost lands.

Keep three voices separate:

- **Textbook voice**: `The cause lies in two stages of a generation request. The scheduler must therefore trade off two objectives.`
- **Performative informality**: `The engine is a bus, and the stages fight over the steering wheel.`
- **Natural explanation**: `One engine tries to keep the whole machine busy. Another tries to finish the current request sooner. Why can one system not optimize both? The answer begins with how a model generates a response.`

These examples show narrative distance, not a reusable template. Every article must find its entry in its own evidence.

For each prose pass, prepare one user-approved positive sample with similar explanatory difficulty and two negative extremes from the current draft: textbook exposition and performative informality. Learn only the positive sample's narrative distance, not its opening, metaphors, first-person placement, or section count.

### 6.7 Comprehensible Does Not Mean Cognitively Comfortable

Low cognitive burden has two distinct layers. First, the reader has enough context to understand each concept. Second, the reader does not need to hold several new concepts and relationships in working memory at once. The first can pass while the second fails.

The common cause is exposing the writer's analytical process as the article's reading order. A writer may need four comparison axes to reason about a platform. Unless the article teaches readers to operate that checklist, let one concrete object move through the real process and name the differences afterward.

*   ❌ **Bad**: Understanding a platform requires checking stable identity, state ownership, scaling unit, and recovery unit.
*   ✅ **Good**: The same support ticket returns in three different ways. A restarted program may reload it from a database; a later message may use an Agent ID to find the same local state; or an approval response may resume the workflow at the step where it stopped.

Use four rules: prefer one continuous process; put action before naming; make H2s understandable in isolation; and advance one main relationship per paragraph. Then run a restatement test. After the first paragraph of a section, can the reader explain who did what, what changed, and why it differs without repeating the new terminology? If not, the article still asks the reader to operate the writer's framework.
