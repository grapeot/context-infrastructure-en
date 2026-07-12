# External Article Prose and Rhetoric Guide

## Metadata

- **Type**: BestPractice
- **Use cases**: Long-form articles, reports, and blog posts for strangers without shared context, public channels, customers, or external course audiences.
- **Created**: 2026-07-06

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

When the article's primary language already expresses a concept clearly, do not immediately repeat an English translation in parentheses. This pattern adds visual noise without information gain.

Keep ordinary concepts in the article's primary language. Preserve official product names, APIs, protocols, code identifiers, and standard abbreviations. If the English term is itself the common form, use it directly and explain it naturally once. Use bilingual forms only when the article discusses translation differences, terminology ambiguity, or searchability of the original source.

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
