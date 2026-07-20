# External Writing: Thesis and Structure Guide

> [!NOTE]
> **Applicable Phase**: To be read and used by the **Manager** during the **Reasoning** phase and when drafting `writing_brief.md`.
> The permission boundaries and delivery contracts involved in this document are always governed by Section 0 of the [External Writing and Drafting Workflow](./workflow_external_writing.md). This guide only provides specific stage execution details and does not grant the Manager any authority to modify the final text.

## Core Thesis Discovery

The core thesis (Thesis) is the soul of the article. When the user provides a clear core thesis, preserve their basic judgment. Focus on checking whether the evidence supports the thesis and whether the thesis is continuous with the author's established views, avoiding reinventing the writing direction. When the user has not provided a core thesis, the Manager should explore using the following steps:

1. **Consult the Thesis Catalog**: Select 1 to 3 relevant analytical perspectives from the thesis catalog file as inspiration, but do not mechanically force them onto the content.
2. **Retrieve Historical Context**: Search the author's previous articles, axiom database, and adjacent public articles based on the product name and core issues.
3. **Position the Article**: Determine whether the new article fills an existing gap, revises a previous judgment, or provides a counterexample.
4. **Formulate a Falsifiable Core Judgment**: Write a specific core thesis that readers can agree or disagree with, and deconstruct it into 3 to 7 causal claims with clear directions.

**Do not turn an analytical lens into a core thesis.** When editors require analyzing materials by chronology, dimensions, or specific sequences, filter out these methodological terms in your mind first. Check if removing them leaves a clear, reader-facing substantive judgment. Only these substantive judgments can serve as the core thesis of the article; timelines and classification matrices should only serve as auxiliary ways to organize evidence.

## Design Brief Contract

The design brief (`writing_brief.md`) is the authoritative guidance document for all subsequent writing stages and must contain the following core elements:

- **Reader Start State**: Clearly explain how the reader currently understands the subject and what prerequisite knowledge they lack.
- **Target Belief Change**: Summarize in a single sentence what the reader's core understanding should shift from and to.
- **Causal Model**: List 3 to 7 claims with clear causal directions and their mutual dependencies.
- **Evidence Roles**: Define the specific role of each piece of core evidence—whether it establishes the old model, proves recent changes, explains a specific mechanism, validates the core judgment, or constrains the extrapolation boundary of the conclusion.
- **Concept Introduction Plan**: List each unfamiliar noun or term, its location of first occurrence, and the contextual preparation the reader needs before seeing the term.
- **Immutable Terms**: List product names, model names, API identifiers, and terms that are easily mistranslated, which must remain unchanged.
- **Image Contract**: Specify the mechanism to be compressed or explained by each image, the final image filename, relative path, placement location in the text, and the semantic intent of the image.

Materials without clear evidence roles must not be included in the body text. The context provided by the brief should represent only the minimal causal model required for the core thesis to hold; it must not function as an encyclopedic overview.

## Narrative Design Path

The narrative design path (Voice Route) is a design for how to unfold the story for the reader step-by-step, rather than a simple article outline:

1. **Identify the Core Contrast**: Discover the most unique contrast, anomaly, or change in this piece that you would genuinely want to tell a friend about.
2. **Clarify the Author's Stake**: State why the author cares about this issue. Do not force the first-person voice if there is no genuine personal judgment.
3. **Simulate the Reader's Follow-up Questions**: Clarify what questions the reader will naturally ask in each section, and how the previous section leads the reader to the current section via a specific action, constraint, or consequence.
4. **Ensure Actions Land**: Each section must contain at least one observable action or consequence.
5. **Set Tone Red Lines**: For the article's topic, list 3 to 5 textbook-style phrases and performative colloquial expressions to avoid in subsequent stages.
6. **Select a Running Example**: When comparing multiple abstract objects across sections, select a single concrete case to use throughout.
7. **Local Map Exception**: For three or more actual alternatives, steps, states, or risks, the reader must be told the total count, shared criteria, and whether their relationship is alternative, progressive, or sequential before they appear. This is the local map exception rule.

The analytical framework and the reader-facing bridge must be kept strictly separate. Although frameworks like "four questions, five layers, three dimensions" and classification matrices help the author clarify their thinking, if readers do not need to operate these frameworks in practice, the body text should show differences along concrete processes and name them only after the concrete actions appear.

## Dependency Checks

Before entering the IC-1 stage, the Manager must verify each section against the following questions:

- What specific existing understanding of the reader does this section change?
- Have the concepts and facts required for this section appeared and been explained clearly beforehand?
- Which previously introduced object, action, or consequence carries the discussion in this section?
- Is the reader required to hold multiple ungrounded concepts in working memory simultaneously?
- When three or more parallel items appear, is a local map provided in advance?
- Does the first paragraph of this section connect to the suspense or object left at the end of the previous section?

If there is no clear answer to the first question, the section is redundant and should be deleted or merged. If a required prerequisite concept has not appeared, the structural sequence must be re-ordered instead of trying to fix it by inserting ad-hoc definitions into the body text. If section handoffs fail, the end of the previous section and the entry of the next section must be designed in pairs.

## Title Design

The title is the shortest reading contract between the author and the reader. It must allow the reader to immediately recognize the subject, relevance, and analytical increment. If the subject is unfamiliar to the reader, the title should include its category, core action, or major change. For event-driven articles, the subject of the news event should generally be mentioned. Accuracy must take priority over suspense; using generic templates that could fit multiple articles is strictly prohibited.

When drafting the brief, design 3 to 5 candidate titles from different analytical angles. Compare them against 5 to 10 recently published articles in the same channel, analyzing structural similarities (questions, contrasts, imperatives) to avoid repeating the same sentence patterns.

## Opening Design

There is no single opening template. The title and the first three paragraphs of the body must enable a reader with zero context to state: who did what, what the core judgment of the article is, and what additional mechanism or boundary they will gain by reading on. For event-driven articles, the event anchoring and analytical increment must be established within the first two or three paragraphs at the latest.

The design of the entry point should align with the strongest form of evidence: for log analysis, start with the timeline; for research papers, start with the key result or measurement; for product releases, start with design choices; for product evolution, start with a pivot or deprecation. If there is no unique entry point, present the core judgment directly rather than fabricating irrelevant scenarios.

**Perform a first-screen cold-read test**: Hide the design brief, editorial conversations, background sources, and the rest of the text, and read only the title and the first three paragraphs. If a test reader can only repeat unfamiliar names or cannot explain how the facts relate to the core thesis, the opening design has failed.

## De-contextualizing Editorial Feedback

Local questions in editorial feedback are diagnostic signals, not direct outlines for the body text. When feedback is received, identify the underlying information gaps and fix them by adjusting the overall comprehension path.

**Perform a hidden editing context test**: The revised body text must assume the reader has zero knowledge of the editorial conversation. If the body contains defensive arguments, subheadings, or explanations that only make sense if the reader is aware of the conversation, they must be removed.

"Thin content in a section" usually indicates a lack of dynamic processes, obvious alternatives, applicability boundaries, or causal links between mechanisms and consequences. The Manager should direct the writing agent to restore those missing causal links. The agent must not pad the content by repeating conclusions, adding decorative metaphors, or exaggerating source claims.
