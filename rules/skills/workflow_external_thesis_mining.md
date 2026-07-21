# External-Facing Thesis Mining Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: A topic and preliminary research exist, but the team must decide whether they support an external-facing analysis and what that article should prove.
- **Input**: Phase 1-3 output from the [Deep Research Survey Workflow](./workflow_deep_research_survey.md), or an equivalent research packet.
- **Output directory**: `tmp/<session_slug>/`

## Purpose and Boundary

This workflow turns an interesting topic into one evidence-backed, falsifiable core thesis that adds value for the reader and remains continuous with the author's established judgment. It is the decision layer between research and external writing.

It does not discover daily news candidates, replace missing large-scale research, or write final prose. Axioms and the [Thesis Catalog](./reference_writing_thesis_catalog.md) remain the canonical sources for established views. This workflow retrieves, combines, stress-tests, and makes an editorial decision.

If the user supplied a clear thesis, do not invent another one for process completeness. Preserve it and test its evidence, scope, strongest counterargument, and reader delta.

## Success Criteria

Before external writing begins, all criteria must pass:

1. **One judgment**: Expressible in two or three sentences and open to agreement or disagreement, rather than a news recap, topic label, or claim that something is interesting.
2. **Evidence-bearing**: At least two independent evidence types support the critical inference; facts, inference, and author judgment remain distinct.
3. **Reader delta**: States the mechanism, boundary, counterexample, comparison, or consequence the reader gains beyond the public summary.
4. **Author continuity**: Relevant Axioms, prior articles, and surveys have been checked. Any changed judgment identifies the new evidence.
5. **Corpus increment**: The conclusion, entry point, and argument structure do not repeat recent work in the same channel.
6. **Falsifiability and boundaries**: Names the strongest counterargument, key uncertainty, scope, and falsifier.
7. **Writeability**: Supports three to five argument nodes that advance rather than repeat one another.

When evidence is insufficient, narrow the thesis or return `DO_NOT_WRITE_YET`. Topic popularity and sunk research cost do not lower the gate.

## Required Cognitive Inputs

The main thread builds a small, discriminating comparison set:

- `../axioms/INDEX.md` and one to three directly relevant Axiom documents.
- One to three relevant perspectives from the [Thesis Catalog](./reference_writing_thesis_catalog.md). Use them for inspiration, never as an L1-L8 article outline.
- Related historical judgments in `contexts/blog/` and `contexts/survey_sessions/`.
- Three to six adjacent pieces from the target publication environment, covering the same topic, a similar argument, or material that received substantial human correction. The target project supplies the paths; this workflow assumes no fixed private directory convention.
- The current research packet, source URLs, fact-check results, and known evidence gaps.

Write the retrieval results and selection rationale to `tmp/<session_slug>/thesis_inputs.md`. This is a decision evidence list, not a new knowledge base.

## Independent Candidates and the AGY Reader Route

For a high-value topic with substantial judgment uncertainty, follow the [Parallel Subagent Workflow](./workflow_parallel_subagents.md) to launch two independent subagents and use the [Antigravity CLI](./antigravity_cli.md) for one independent AGY reader. All three read `thesis_inputs.md`, but each writes to a separate file.

- **Evidence and mechanism reader**: derives defensible mechanism claims from the strongest evidence and identifies attribution or scope overreach.
- **Continuity and novelty reader**: compares Axioms, earlier writing, and correction history to find a judgment the author has not already published.
- **Unfamiliar-reader and antithesis reader**: AGY CLI with `gemini-3.6-flash-high`. Put the complete task in `agy_reader_prompt.md`, use a fresh AGY conversation, explain why a reader would care, propose the strongest alternative explanation, and test whether each candidate merely restates industry consensus. Store result, stdout, stderr, and events separately.

Each reader writes two to four candidates. Every candidate includes: Thesis, Reader Delta, Reasoning Chain, Strongest Evidence, Strongest Counterargument, Scope and Falsifier, Relationship to Prior Writing, and Whether to Write Now. A reader may return no qualifying thesis; never manufacture candidates to fill a quota.

For low-risk, lightweight work, or when the user supplied a clear thesis, the main thread may skip parallel divergence and proceed directly to critique. Record the reason in `thesis_decision.md`.

## Fresh Critique Gate

After candidate generation, use a fresh high-reliability reasoning context that did not participate in the brainstorm. The critic may read the research packet, historical material, and all candidates, but not candidate authorship, and does not polish prose.

The critic checks whether evidence carries each thesis, whether a simpler alternative explanation exists, whether the reader delta is concrete, whether the candidate adds to prior writing, whether scope matches evidence strength, whether candidates should be rejected or merged, and whether the correct result is `DO_NOT_WRITE_YET`. Write the review to `tmp/<session_slug>/thesis_critique.md`.

## Main-Thread Decision and Output

The main thread retains editorial authority. Do not select by vote or mechanically combine candidates into a double thesis. Write `tmp/<session_slug>/thesis_decision.md` with:

- `Verdict: PROCEED | DO_NOT_WRITE_YET`
- Core Thesis
- Reader Contract
- Argument Spine of three to five nodes with supporting evidence
- Boundaries and Counterargument
- Continuity and Novelty
- Evidence Gaps
- Rejected Candidates and reasons

Only `PROCEED` permits creation of `writing_brief.md` and entry into the [External Writing Workflow](./workflow_external_writing.md). `DO_NOT_WRITE_YET` is a valid output; do not soften it into a vague monitoring recommendation.

## Known Failure Modes

- Selecting an L1-L8 lens first and forcing facts into it.
- Packaging consensus, a news summary, or topic heat as a thesis.
- Replacing verification with a multi-model vote.
- Combining two candidates into an unfocused double thesis.
- Optimizing titles or prose in this stage instead of leaving expression to external writing IC-1 through IC-3.
