# External Writing and Drafting Workflow

> [!IMPORTANT]
> **Before taking any writing or drafting action, the agent must read this document completely to the end of file (EOF).**
> The global permission boundaries and the non-overridable execution contract are explicitly defined on the first screen. The subsequent stage-specific reference guides serve only to progressively disclose implementation details and cannot override or modify the constraints in this chapter.

## Metadata

- **Type**: Workflow
- **Applicability**: Writing verified research materials into analytical articles, public investigation reports, client content, or external course materials for readers with zero shared context.
- **Prerequisites**: Output from the research phase, or an equivalent source pack (Source Pack).
- **Applicable Roles**: Manager (manager/auditor), IC-1/IC-2/IC-3 (independent session writers for each stage).
- **Default Output**: `contexts/survey_sessions/`; write to the target project's blog directory and format only if the user explicitly requests a blog post.
- **Last Updated**: 2026-07-20

## 0. Non-Overridable Execution Contract

This section defines the highest-priority execution contract for this workflow. If any local instructions, historical versions, or stage-specific guidelines conflict with this section, this section shall prevail.

1. **IC-3 is the sole final prose authority.** The final title, body, punctuation, link anchor text, image references, and image alt text must come entirely from an accepted, complete Antigravity output. No other role or stage has the authority to rewrite the text.
2. **The Manager has zero modification rights over the final text.** The Manager is responsible for research, drafting the writing brief, generating images, performing read-only audits, copying files, and running validation, but must never modify a single character in the IC-3 candidate text. Spelling, facts, links, or formatting issues must not be directly patched in the candidate text by the Manager. Any manual edit by the Manager violates this execution contract.
3. **Issues must be resolved in a closed loop through complete rewriting.** When the Manager identifies an issue, they are only responsible for writing a read-only audit report and starting a completely new Antigravity session. The new session must read the writing brief, the original source pack, the previous complete candidate text, and the latest audit report, and write a complete new candidate text from a blank page. Splicing different versions or applying local patches is prohibited.
4. **The image contract is frozen before IC-3.** The final image filenames, relative paths, placement in the text, and the semantic intent of each image must be locked in the writing brief. IC-3 is responsible for writing the final references into the text. After this point, the Manager can only copy the image files and must never modify the Markdown paths in the body.
5. **Delivery is blocked until all issues are resolved.** A candidate text is allowed to be archived only when the comprehension gate, cognitive comfort gate, factual boundaries, structural continuity, image integration, and deterministic checks are all passed, and there are no blocking issues in the self-QA report. A maximum of three automatic revision rounds is allowed per task. If issues persist after three rounds, all intermediate artifacts must be preserved, and the specific blockers must be reported to the user.
6. **Archiving requires direct copy and verification.** The final delivered archive file must be byte-for-byte identical to the accepted candidate text. There is zero tolerance for any modifications, and no word-level or mechanical exceptions are permitted (verified using the `cmp` command or by comparing SHA-256 hashes).
7. **Separation of writing and publication.** The endpoint of this workflow is the local deliverable file. Any operations such as blog deployment, email distribution, or social media posting require explicit user authorization.
8. **Exception limits for short articles or quick drafts.** Articles shorter than 1,000 words or quick drafts explicitly requested by the user may skip the IC-2 stage, but they must never skip the IC-3 stage, the Manager's read-only acceptance, or the final byte-for-byte comparison.

## 1. Routing and Applicability

This workflow is used for writing finished products aimed at external readers. For internal documents read by the user, internal collaborators, or future agents, use the [Internal Writing Workflow](./workflow_internal_writing.md).

External articles must ensure that readers with zero shared context obtain sufficient background when first encountering the company, product, events, or technical terms. Zero context means the reader's understanding does not rely on implicit premises provided by the current conversation, source pack, or the author's previous articles.

This workflow makes no prior assumptions about the reader. The reader is treated as an external entity with basic general knowledge but zero prior knowledge of the current project, technical details, internal decisions, or organizational structure. Therefore, clarity of writing and completeness of explanation are the highest priorities.

If a reader must understand prior background or specific editorial discussions to comprehend a passage, then that passage does not meet the requirements of external writing. After evaluating the nature of the article, the Manager should route articles with external audiences to this workflow and load the reference for each active stage. Short, simple articles may skip IC-2, but the remaining gates and byte-comparison contract still apply.

## 2. Thesis Mining Gate

Before entering the formal writing design (the Reasoning stage), the Thesis Mining Gate must be passed to ensure the article has a solid core argument:

- If the user has not provided a clear core thesis, or the existing thesis has not survived sufficient evidence and adversarial stress testing, [External-Facing Thesis Mining](./workflow_external_thesis_mining.md) must be run first.
- It reads the relevant inputs and generates a temporary decision file `tmp/<session_slug>/thesis_decision.md`.
- Creation of the design brief (`writing_brief.md`) is permitted only when its verdict is `PROCEED`.
- A verdict of `DO_NOT_WRITE_YET` indicates that the current materials or arguments cannot support an external article. In this case, writing must stop or missing evidence must be gathered; fabricating arguments just to complete the task is strictly prohibited.
- If the user has provided a clear thesis, preserve their writing direction, but still stress-test it against evidence, boundaries, the strongest counterargument, continuity with established views, and the reader delta (Reader Delta). The test results must be recorded in the brief.

## 3. Phases and Reading Order Map

Throughout the writing lifecycle, all participating parties must advance tasks in the order specified in the map below and ensure that the current exit gates are fully met before entering the next phase:

| Phase | Executor | Required Reading | Core Deliverable | Exit Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Preflight** | Manager | This document, `COMMUNICATION.md`, `bestpractice_external_prose.md` | Routing and task boundaries | Confirm external attributes, output location, and publication limits to ensure the process stays within boundaries. |
| **Thesis Mining (As Needed)** | Manager | [Thesis Mining](./workflow_external_thesis_mining.md) | `thesis_decision.md` | When mining or stress-testing a thesis, the verdict must be `PROCEED`. If `DO_NOT_WRITE_YET`, abort or gather missing evidence. |
| **Reasoning** | Manager | [Structure Guide](./reference_external_reasoning_structure.md), Source Pack, previous articles | Writing brief, style calibration | Determine core thesis, thesis dependency graph, concept introduction plan, and image contract. |
| **IC-1** | Fresh AGY Session | Writing brief, Source Pack, [Antigravity CLI](./antigravity_cli.md) | Structural draft | Complete structure and evidence; do not pursue final voice and micro-sentence styling. |
| **IC-2** | Fresh AGY Session | Writing brief, structural draft, calibration set, [Voice Guide](./reference_external_voice_rewrite.md), [Antigravity CLI](./antigravity_cli.md) | Rewrite draft | Natural introduction of concepts; pass cognitive comfort and chapter handoff checks. |
| **Image Freeze** | Manager | Writing brief, structural draft, [Delivery Guide](./reference_external_delivery_checks.md) | Final image files | Freeze image filenames, paths, placement, and intent to lock the visual contract. |
| **IC-3** | Fresh AGY Session | Writing brief, Source Pack, rewrite draft, calibration set, frozen image contract, [QA Guide](./reference_external_prose_qa.md), [Antigravity CLI](./antigravity_cli.md) | Complete candidate text, self-QA report | Pass both comprehension and cognitive comfort gates; no blocking issues in the self-QA report. |
| **Acceptance** | Manager | Writing brief, Source Pack, candidate text, self-QA report, [Delivery Guide](./reference_external_delivery_checks.md) | Audit report or approval decision | Pass all read-only regression checks and fact-checking; audit status is PASS. |
| **Delivery** | Manager | Accepted candidate text | Final file and images | Complete file copy and byte-level comparison; trigger final rendering on the client via the `read` tool. |

## 4. Core Artifacts List

All intermediate artifacts must be stored in the temporary session directory `tmp/<session_slug>/` and archived with explicit version numbers to ensure the revision history is fully traceable and easily referenced by new writing sessions:

- `source_pack.md`: Records facts, original links, citation boundaries, and immutable proper nouns. It acts as the authoritative factual boundary for the draft; no new facts outside its scope may be introduced in the body.
- `writing_brief.md`: Defines the reader's start state, target belief change, causal model, evidence roles, concept introduction plan, and the image contract. This is the primary brief guiding all subsequent writing stages.
- `style_calibration.md`: Contains 3 to 5 positive channel-specific samples, inheritable voice traits, and negative examples of both textbook and performative styles. It ensures the article's voice aligns with the target channel.
- `article_structural.md`: The structural draft generated by IC-1, marking structural metadata and evidence positions to lock the logical framework.
- `article.md`: The draft rewritten by IC-2, resolving terminology introduction issues and cognitive coherence.
- `article_final_vN.md`: The complete candidate text produced by IC-3, serving as the sole candidate for delivery.
- `prose_qa_vN.md`: The self-QA report submitted by IC-3, documenting the checklist results for all gates and review dimensions.
- `content_audit_vN.md`: The read-only audit report written by the Manager, highlighting problems and specifying permitted directions for revisions.

## 5. Unified Go/No-go Gates

A candidate text is permitted for delivery only when it fully satisfies the following conditions. The Manager must verify each gate systematically during the read-only audit, leaving no room for ambiguity:

1. **First-Screen Contract**: The title and first screen immediately clarify the subject, the core judgment, and the incremental value of reading further.
2. **Core Thesis**: The article contains a single, specific, and disputable core thesis, presented clearly within the first 25% of the content.
3. **Concept Introduction**: Every concept has sufficient context before its first mention and does not rely on any implicit reader background.
4. **Dependency Order**: Every section advances based on the reader's questions, with dependencies introduced before conclusions. Even with the headings hidden, adjacent sections must transition naturally.
5. **Cognitive Load**: The reader is not forced to hold multiple ungrounded classifications in working memory. For three or more real alternatives, a local map outlining the total count, shared criteria, and mutual relationships must be provided.
6. **Voice Balance**: The prose style sits between textbook lecture and performative colloquialism, and the analytical framework is kept out of the reader-facing body text.
7. **Factual Boundaries**: All facts, figures, attributions, links, and argument strengths remain strictly within the boundaries of the source pack.
8. **Visuals Compliance**: Visuals effectively reduce cognitive load, and their references, format, and dimensions comply with delivery specifications.
9. **QA Verdict**: The self-QA report indicates that both the comprehension gate and cognitive comfort gate have passed, and no blocking issues are present.
10. **Byte Identity**: The final archived file is byte-for-byte identical to the accepted candidate text.

## 6. Failure and Rework State Machine

IC-3 has the authority to polish the prose without changing the thesis, causal model, factual boundaries, or section dependencies. If IC-3 determines that new facts must be added, the core thesis must be changed, major sections reordered, or the evidence chain rebuilt, it must not execute these changes directly. Instead, it must mark a `BLOCKER` in the self-QA report, specifying the exact location and the dependency gap.

When the Manager identifies an issue, they must document it in a read-only audit report, identifying the original sentence, the failed gate, and the permitted direction of revision. The Manager must not write the corrected alternative paragraph in the audit report. Subsequently, a new AGY session must be started to generate a new candidate text from scratch.

The state machine transitions are defined as follows:
- If any gate fails, the Manager logs the audit report and starts the next round of IC-3.
- If blocking issues persist at the third round, generation must stop immediately. All intermediate artifacts must be preserved, and the failure details must be reported to the user. This prevents the agent from entering an endless loop of mechanical self-repetition. The fourth round may start only after the user recalibrates the brief, adjusts the source pack, or provides new instructions.
- If all gates pass and the audit report status is pass, archiving and delivery are permitted.

## 7. Micro-Language and Formatting Constraints

When writing any documents related to this workflow and reference guides, the following baseline constraints for English quality must be strictly followed:
- **Active Voice Preference**: Wherever a verb can be changed to active voice while keeping the sentence natural, avoid passive constructions.
- **Natural Sentence Rhythm**: Avoid stacking multiple actions or layering complex modifiers in a single sentence. Use short sentences to state core judgments and slightly longer sentences to connect cause, evidence, and constraints.
- **Eliminate Subjective Appraisals**: Do not use subjective evaluation labels like "straightforward", "clear", or "insightful". Use objective facts, data, and boundaries instead.
- **No Em Dashes**: Do not use em dashes ('—') for emotional pauses or transitions in the body text. Use commas, parentheses, or semicolons instead.
- **No Redundant Parentheticals**: Do not use redundant parenthetical explanations. Only use parentheses to enclose technical terminology when first introduced.
- **Terminology Consistency**: Capitalization, spelling, and spacing of proper nouns (product names, API identifiers, model names) must match the source pack exactly.

## 8. Reference Document Index

- [Reasoning, Brief, and Structure Guide](./reference_external_reasoning_structure.md)
- [Voice Rewrite and Style Calibration Guide](./reference_external_voice_rewrite.md)
- [Prose QA and Read-Only Acceptance Guide](./reference_external_prose_qa.md)
- [Visuals, Verification, and Delivery Guide](./reference_external_delivery_checks.md)
- [External Article Prose and Rhetoric Guide](./bestpractice_external_prose.md)
- [Thesis Catalog](./reference_writing_thesis_catalog.md)
- [Antigravity CLI File-Based Invocation](./antigravity_cli.md)

## 9. Local Delivery Endpoint

The final Markdown files and images remain in the workspace. After the final write, the Manager must use the `read` tool to read the final Markdown file and trigger client rendering. The final response provides the file paths and any known residual risks. No publication action is authorized without explicit user approval.

Before archiving, the Manager must verify that the content of the local delivery file is byte-for-byte identical to the accepted candidate text, and contains no internal debugging residue or incomplete placeholders.
