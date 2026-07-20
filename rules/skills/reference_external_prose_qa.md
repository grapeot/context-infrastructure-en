# External Writing: Self-QA and Read-Only Acceptance Guide

> [!NOTE]
> **Applicable Phase**: To be read and used by the **IC-3** final writing role and by the **Manager** during the read-only acceptance phase.
> The permission boundaries and delivery contracts involved in this document are always governed by Section 0 of the [External Writing and Drafting Workflow](./workflow_external_writing.md). This guide only provides specific stage execution details and does not grant the Manager any authority to modify the final text.

## IC-3 Input and Output Requirements

IC-3 must run in a completely new Antigravity session. It needs to read the design brief, source pack, rewrite draft, style calibration set, communication style guide, micro-style manual, and the frozen image contract. Its deliverables include:

- `article_final_vN.md`: The complete, independently deliverable candidate text. Providing partial patches is strictly prohibited.
- `prose_qa_vN.md`: The self-QA report containing review evidence and check results for all gates.

IC-3 is the sole authority for the final prose. It has full discretion to split sentences, merge paragraphs, adjust vocabulary, or rewrite the entire article from a blank page. However, it must never alter the core thesis, core claims, factual attributions, numbers, links, H2 subheading dependencies, or the image contract defined in the design brief.

## IC-3 Ten Review Dimensions

When generating candidate text, IC-3 must perform a deep review against the following ten dimensions:

1. **Overall Voice Control**: Check whether the opening, the entries of all subheadings (H2), and the ending contain obvious textbook-style elements. If three or more instances of the "announce theme -> define object -> abstract summary" structure appear, the entire prose must be rewritten from a blank page; fixing only the affected sections is prohibited.
2. **Zero-Context Friendliness**: Ensure that company names, papers, regulations, products, key events, and technical terms have sufficient explanations or context upon their first appearance, without relying on any hidden reader background.
3. **Elimination of Translation Cadence**: Remove abstract subjects produced by literal translation, stiffly translated verbs, redundant bilingual parentheticals, mixed formatting without proper spacing, and mechanical transition words.
4. **Enhanced Cognitive Comfort**: Ensure that the reader does not encounter confusion by running cold-read tests, checking working memory load, testing first-paragraph recall, verifying scene continuity, and reviewing local map designs.
5. **Removal of AI Templates and Scaffolding**: Thoroughly eliminate high-frequency AI templates (e.g., rigid contrasts), subjective self-evaluation words, and leaks of internal analytical frameworks (such as design briefs, axioms, or phase labels).
6. **Local Coherence**: Ensure natural causal or logical transitions between adjacent sentences and paragraphs, clear pronoun references, and subheadings that precisely summarize their underlying text.
7. **Avoiding Superfluous Repetition**: Check for high-frequency repetition of facts, judgments, transition words, and specific sentence structures in close proximity.
8. **Comparison with Calibration Set**: Ensure the article does not read like a manual, press release, or lecture note compared to the positive calibration samples.
9. **Prevention of Over-Colloquialism**: Remove all decorative metaphors, internet slang, anthropomorphic rhetoric, jargon, and absolute judgments unsupported by evidence.
10. **Contextual Continuity**: Do not answer questions in the body text that the reader has not asked. When deleting sections, clean up any unfulfilled setups, cross-references, or isolated images.

## Two Core Reader Gates

- **Comprehension Gate**: A reader with zero background can fully understand every concept in the body text without consulting external materials, and can accurately restate the core thesis of the article.
- **Cognitive Comfort Gate**: The reader does not need to pause frequently or reread passages, and is not forced to hold multiple ungrounded abstract relationships in mind simultaneously.

The self-QA report `prose_qa_vN.md` must document: the overall voice judgment, the inspection process for all ten dimensions, the main locations of revisions, at least four pairs of before-and-after sentence comparisons, the results of title cold-reading and first-paragraph recall tests, the count of preserved numbers, URLs, and images, the specific conclusions of both gates, deterministic scan results, and whether any blocking issues exist.

## IC-3's Permission Boundaries

If IC-3 identifies issues that require adding new facts, modifying the core thesis, adding or removing primary claims, reordering major sections, or restructuring the evidence chain, IC-3 must not handle these issues itself. Instead, it must keep the corresponding content unchanged and mark a `BLOCKER` in the self-QA report, specifying the exact location, the dependency gap, and which upstream artifact needs revision.

## Manager Read-Only Acceptance Protocol

The Manager must read the candidate text, self-QA report, design brief, and source pack in their entirety to perform a new-claim audit. During this audit, the Manager must not make any character-level changes to the candidate text. The Manager should focus on verifying:

- Whether every fact, figure, attribution, link, and proper noun is fully supported by the source pack.
- Whether the strength of the claims in the article exceeds the evidence boundaries of the source pack.
- Whether the title, the sequence of subheadings (H2), and image paths and placements align with the brief.
- Whether IC-3 mistakenly removed constraints, introduced new facts outside the brief, or changed established conclusions during the rewrite.
- Whether both core reader gates and the unified Go/No-go gates have truly passed.

If any issues are found, the Manager must compile a read-only audit report `content_audit_vN.md`. The audit report must list the original sentence or location in the candidate text, the corresponding evidence boundary, the failed gate, the resulting comprehension risk, and the permitted direction of revision. **The audit report must not contain corrected paragraphs written by the Manager.**

After completing the audit report, the Manager must start a completely new Antigravity session. The new session reads the authoritative design brief, the source pack, the previous complete candidate text, the latest audit report, and the style calibration file, and outputs a complete new candidate text and self-QA report from a blank page. Splicing different versions by the Manager is strictly prohibited.

## Convergence and Stop Conditions

A maximum of three rounds of IC-3 candidate iterations is permitted for each task. During these three rounds, as soon as a version of the candidate text passes all gate inspections, generation must stop immediately and transition to delivery. If blocking issues persist at the third round, generation must stop immediately. All intermediate artifacts must be preserved, and the specific failure details must be reported to the user. Marking a candidate text that has not passed all gates as the final version is strictly prohibited.
