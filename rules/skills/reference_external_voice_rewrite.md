# External Writing: Voice Rewrite and Style Calibration Guide

> [!NOTE]
> **Applicable Phase**: To be read and used by the **IC-2** session and by the **Manager** when preparing corresponding prompts.
> The permission boundaries and delivery contracts involved in this document are always governed by Section 0 of the [External Writing and Drafting Workflow](./workflow_external_writing.md). This guide only provides specific stage execution details and does not grant the Manager any authority to modify the final text.

## Inheriting the IC-1 Structural Draft

IC-1 reads the design brief and source pack and outputs the structural draft `article_structural.md`. The structural draft is responsible for placing the core thesis, thesis dependencies, evidence positions, counterargument boundaries, concept introductions, links, numbers, and image placeholders in the correct sections. Each section of the structural draft needs to mark the reader's question and specific observable consequences, but does not aim for publishable prose quality.

The structural draft must never be written as a lecture-note style semi-finished product. While the structural draft can explicitly expose structural metadata for the next phase, it must make clear to IC-2 that the IC-2 phase only inherits the claims, evidence, links, numbers, section dependencies, and image contract from the structural draft, and must not inherit its sentence structures, paragraph openings, or narrative rhythm.

## Calibration Set Configuration

Before starting the IC-2 phase, the Manager should select 3 to 5 recently published, clearly polished articles with similar explanatory difficulty from the same publication channel, and record them in `style_calibration.md`. The calibration set must include:

- The sample paths and 1 to 3 paragraphs most worthy of reference.
- The narrative distance to inherit, the way of transitioning from facts to judgments, the style of concept explanations, and sentence rhythm.
- Specific metaphors, sentence structures, section architectures, and first-person placements that are strictly prohibited from being copied.
- 2 to 3 negative examples of textbook-style writing and 2 to 3 negative examples of performative colloquial style selected from the current structural draft or previous failed drafts.

The Manager must not gather samples mechanically by date, nor should they provide abstract style rules without allowing the Agent to read actual high-quality articles.

## IC-2 Rewrite Task

IC-2 must completely rewrite the text from a blank page, generating `article.md`. The purpose of rewriting is not to simply replace written vocabulary with colloquial words, but to allow someone who truly understands the problem to naturally introduce their discoveries following the reader's line of questioning.

The target voice of the article should sit between these two extremes:
- **Textbook-Style Failure**: Starting by immediately announcing the topic, defining every noun concept in sequence, and closing each section with an abstract summary sentence.
- **Performative-Style Failure**: Over-relying on decorative metaphors (e.g., buses, wars, building houses) or frequently using internet slang and jargon to artificially build intimacy with the reader.
- **Ideal State**: Describing how concrete objects perform actions first, then bringing out core judgments. The first-person voice is used only to state genuine opinions and judgments, not to perform emotional theater.

## Reducing Reader Cognitive Load

To implement the principle of low cognitive load, the rewrite must adhere to the following specific methods:

1. **Actions Before Classifications**: Show the specific execution process of the same task under different approaches first, and only then summarize the differences between them.
2. **A Single Running Case**: When comparing the same set of abstract objects across sections, use the same request, ticket, person, or log record throughout.
3. **Delayed Nomenclature**: Describe the concrete, observable actions first. Name the component or pattern only after the underlying mechanism is clear.
4. **Single-Relationship Paragraphs**: Break down paragraphs so that the entry of each paragraph starts from an object or concept the reader is already familiar with.
5. **Simultaneous Arrival of Role, Definition, and Impact**: When a new term, metric, or figure appears for the first time, the reader should be able to immediately answer what it describes, what it measures, and whose outcome it alters.
6. **Local Map Rule**: When encountering three or more actual alternatives, steps, states, or risks, outline the total count, shared criteria, and mutual relationships to the reader before they appear.
7. **Complete Causal Chains**: Each section must fully explain the problem faced, the obvious alternatives, the current operational mechanism, and what the current mechanism cannot resolve. Do not fabricate alternatives if none naturally exist.
8. **Paired Handoffs**: Transitions between sections should be designed in pairs, such as using the same task to enter the next action, letting the current mechanism expose its limits, or transitioning naturally via the consequences of the previous choice.

Completeness of definitions does not equal readability. If the reader is required to maintain multiple abstract threads in working memory simultaneously, restructure the information into a linear progression where concepts emerge naturally in sequence.

## IC-2 Phase Self-Check

After completing the rewrite, IC-2 must verify the text against the following criteria:

- Read the first three paragraphs and the first paragraph under each subheading (H2) aloud. Rewrite any passage that reads like an academic abstract, product manual, press release, or course syllabus.
- From the perspective of a reader with zero context, check where each concept first appears. Prioritize adding dynamic processes and actions over dictionary definitions.
- Compare the generated draft blindly with the calibration set. If the draft reads like a dry manual, do not pass it under the pretext of "formal writing."
- Remove all explanations that rely on metaphors or slang to make sense, and restore the concrete underlying operational mechanisms.
- Hide all H2 subheadings and check whether adjacent sections still transition naturally.
- After reading the first paragraph of each section, check whether you can explain to someone else who did what and what changed in this section without using any newly introduced terms.

The output of IC-2 is not the final deliverable version. It must preserve the core thesis, thesis dependency graph, factual boundaries, links, numbers, and image contract defined in the design brief, providing a reliable input for IC-3 in a subsequent fresh session.
