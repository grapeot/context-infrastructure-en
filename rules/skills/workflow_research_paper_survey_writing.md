# Research Paper Survey and Writing Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Research, niche analysis, and reader-facing writing on a research paper (or technical report)
- **Created**: 2026-03-25

## What This Is

A complete end-to-end process for turning a research paper (or a set of papers) into an analysis article aimed at technical practitioners.

It differs from a plain paper summary in two fundamental ways. First, the writing order is arranged by reader importance, not by the paper's section order. Second, the analysis goes beyond the paper's own claims and positions the paper inside the product ecosystem and technical stack.

## When to Use

- After reading a paper, you need to write analysis or share it
- You need to judge a paper's impact on real products / workflows
- You need to convey paper content to people who understand technology but have not read the original

Not applicable for: pure academic surveys (those require covering dozens of references), or one-sentence summary situations.

## Success Criteria

A qualified output must pass three tests simultaneously:

1. **Five-paragraph test**: A technical reader with half the background can, after the first five paragraphs, state what this paper changes, why it matters, and what remains unvalidated. If the first five paragraphs are still on background or method detail, the ordering is wrong.

2. **Three-layer separability test**: Pick a paragraph at random; the reader can tell whether it is the paper's own claim, external verification / context, or our own judgment. If the three layers are mixed together, the labeling is insufficient.

3. **Niche test**: After reading, the reader can answer: which bottleneck does this paper solve, how did people work around it before, and which layer of the stack is it on. If these questions cannot be answered from the text, the niche analysis is missing.

## Core Writing Order: By Importance, Not by Paper Order

This is the most important rule of this workflow. The paper's narrative order is designed for reviewers (background → method → experiments → conclusion). Our readers are not reviewers; the order they need is entirely different:

**Layer 1: What happened, why it matters (covered within the first 3 paragraphs)**

In one or two sentences, state what the paper does, then immediately answer: what concrete consequence does it have, for whom. The consequence should be specific enough to imagine, e.g., "a task that previously needed 8x A100s for 3 days now finishes in 4 hours on a single card," rather than "greatly reduced compute cost."

**Layer 2: Which pain point it solves, what people did before**

Readers need an anchor — before this paper, what scheme did people doing the same thing use, and what did those schemes cost. This layer establishes a reference frame, letting readers judge the magnitude of the improvement.

**Layer 3: How it does it (intuition version)**

First explain the core mechanism with an analogy or intuition, letting the reader build a mental model. E.g., "it doesn't compress the model during training; it dynamically skips compute paths that aren't needed during inference." Formal math comes after, or in a separate technical detail subsection.

**Layer 4: How strong the evidence is, where the boundary lies**

What scenarios the experiments cover, what they don't. What limitations the authors themselves acknowledge. Community reaction. If there are third-party replications or challenges, here is the place.

**Layer 5: Niche analysis**

Where this paper sits in the larger technical map. See the niche analysis framework below.

## Research Process

### Step 1: Read the paper, extract the skeleton

Read the original (or abstract + introduction + experiments + conclusion), and extract four things:

- **Core claim**: what the paper says it achieved (one sentence)
- **Method intuition**: ignoring formulas, can the core idea be stated as a one-line analogy
- **Experimental coverage**: on what datasets/tasks/scales it was tested, and what the baseline is
- **Author-acknowledged limitations**: usually in the conclusion or limitations subsection

Write these four into a scratchpad.

### Step 2: Search external reactions

Use Tavily to search the paper title, author names, and key method names. Focus on three categories:

- **Community discussion** (Twitter/X, Reddit, HN): anyone replicating, challenging, or pointing out unnoticed details
- **Peer review** (OpenReview, NeurIPS/ICML reviews): if public reviews exist, look at the main reviewer concerns
- **Follow-up work**: anyone improving on this paper, or integrating it into a product

This step can dispatch sub-agents in parallel, but the search dimensions must be split explicitly. Add key findings and URLs back to the scratchpad.

### Step 3: Gather context needed for niche analysis

This step answers not "what the paper says," but "what was the state of the field before this paper." Specifically search for:

- Baseline methods the paper itself cites (the rivals it compares against)
- Commercial products or open-source projects doing the same thing
- Alternative paths in adjacent fields (e.g., for a model-compression paper, an alternative path may be cheaper API pricing)

### Step 4: Form judgments, separate the three layers

In the scratchpad, organize all information by three layers:

- **The paper's own claims**: what the authors say, how far the experiments support it. This layer only states facts
- **External verification and context**: community reaction, third-party replication, reviewer opinions, related product moves. This layer provides references outside the paper
- **Our judgment**: based on the first two layers, how large we think this paper's actual impact is, how confident, which claims deserve to be kept and which discounted

The three layers must have explicit markers or paragraph separation; they cannot be mixed.

## Niche Analysis Framework

This is what distinguishes a paper summary from a paper analysis. The following five questions must each be answered:

**1. Which bottleneck does it solve?**

Describe with concrete constraints, not vague terms like "insufficient performance." A good answer looks like "models under 7B parameters achieve less than 40% accuracy on multi-step reasoning tasks, making usable on-device agents impossible to deploy."

**2. What alternative paths existed before it?**

List existing solutions (both papers and products), and state what each path costs. E.g., "option A needs 8x memory, option B sacrifices 30% accuracy, option C depends on specific hardware."

**3. Is it creating new capability, or driving down the cost of existing capability?**

This distinction is crucial. Creating new capability means something previously impossible is now possible (0→1). Cost compression means something only a few could do is now accessible to many (expert→mass). The strategic implications are entirely different: the former opens new markets; the latter reallocates existing ones.

**4. Which layer of the stack is it on?**

Pin the layer explicitly: model layer / runtime & inference / infrastructure / data pipeline / product UX / org workflow. A paper may span layers but usually has a primary layer. Which layer it is on determines the impact propagation path — lower-layer improvements have wider reach but slower propagation.

**5. If it holds, which adjacent systems, products, or workflows does it change?**

This is the most practically valuable question. E.g., a paper that lets small models approach large models on reasoning, if it holds, directly affects on-device agent products, edge inference frameworks, and the pricing strategy of SaaS that depends on large-model APIs.

## Draft Template

Below is the recommended output structure. Specific subsection titles can be adjusted to the paper's content, but keep the order.

```markdown
# [Paper short name]: [one sentence stating what it changes]

## Core Findings

[2-3 paragraphs: what it does, the concrete consequence, who is most affected.
Do not explain the method here.]

## Background: How the problem was solved before

[2-3 paragraphs: before this paper, what constraints did people doing the same thing face,
what alternative schemes were used, what those schemes cost.]

## Core Method (intuition version)

[First explain the core idea with an analogy or intuition,
then 1-2 paragraphs of formal detail.
If the method is very complex, open a separate "Technical details" subsection.]

## Evidence and Boundaries

[What the experiments cover and don't.
Community reaction. Third-party verification.
Explicitly mark: the following are paper claims / external verification / our judgment.]

## Niche

[Answer the five niche questions above.
This section's value is helping the reader judge "how much attention should I pay to follow this."]

## Judgment

[Our overall assessment. How much attention this paper deserves,
how confident we are, under what conditions the conclusion would flip.]
```

## Review Checklist

After the draft, check item by item:

**Ordering**
- [ ] Do the first three paragraphs answer "what happened" and "why it matters"
- [ ] Does method detail come after background and impact
- [ ] Are there paragraphs the reader must read later content to understand

**Cognitive load**
- [ ] Does each key concept have a concrete example or analogy on first appearance
- [ ] Are there more than two consecutive paragraphs of pure abstraction (no concrete example interleaved)
- [ ] Do numbers have a reference frame ("3x" — 3x relative to what)

**Three-layer separation**
- [ ] Pick a paragraph at random; can you tell if it's paper claim / external verification / our judgment
- [ ] Are there paragraphs that state paper claims as verified facts

**Niche completeness**
- [ ] Does it answer what the bottleneck is
- [ ] Does it list alternative paths
- [ ] Does it judge new capability vs cost compression
- [ ] Does it position the stack layer
- [ ] Does it analyze impact on adjacent systems

**Style (per COMMUNICATION.md)**
- [ ] Are there adjectives without reference frames like "greatly improved" "significantly better"
- [ ] Is there paper-tone ("this paper proposes" "experiments show" as sentence openings)
- [ ] Does it violate the positive-statement principle (negation replacing direct explanation)

## Common Failure Modes

**1. Paper-order trap**

Writing in introduction → method → experiments → conclusion order. The reader still doesn't know why this paper is worth reading by paragraph three. Fix: after drafting, check the first three paragraphs; if they're still on background or method, pull the conclusion and impact to the front.

**2. Abstraction stacking**

Multiple consecutive paragraphs saying "improved efficiency" "reduced cost" "enhanced capability," but not a single concrete number or scenario. The reader's brain starts sliding by paragraph two. Fix: follow every claim with a concrete scenario or number.

**3. Confusing paper claims with verified facts**

Stating a result obtained under the paper's own experimental setup as a universally held conclusion. E.g., the paper improves 5% on MMLU, but it's written as "comprehensively surpasses in reasoning ability." Fix: every time you cite paper data, mark the experimental condition.

**4. Missing niche analysis**

The paper is explained clearly, but "so what" is not answered. The reader knows what it does, but not where it sits in the bigger map. Fix: force answers to the five niche questions, even if some answers are "cannot judge yet."

**5. Official narrative transplant**

Directly using the paper abstract's wording to organize the article. The abstract is written for reviewers, emphasizing novelty and contribution, but readers need significance and context. Fix: treat the abstract as a source of information, not a narrative frame.

**6. Over-weighting or ignoring community reaction**

One error is treating Twitter buzz as validation; another is ignoring community discussion and looking only at the paper. Fix: community reaction is signal, not evidence — it needs source and confidence labeling, but cannot be skipped.

## Relationship to Other Skills

- `workflow_deep_research_survey.md`: the research phase can reuse its parallel search and cross-validation flow
- `bestpractice_product_decision_analysis.md`: the niche analysis framework borrows its design-space restoration and cost-structure positioning, adapted for papers