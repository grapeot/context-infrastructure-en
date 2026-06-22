# Knowledge Flywheel Design Pattern

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Knowledge engineering, unstructured information processing, knowledge graph construction
- **Created**: 2026-02-21
- **Source**: Knowledge graph project practice

---

## Core Formula

**Dumb Data + Dumb Methods + Dumb Models = Refined Knowledge**

Accept the imperfection of starting data; gradually increase knowledge purity through an iterable system.

---

## Why Choose "Dumb Methods"?

### The Double Shackles of Closed-Source APIs

1. **Cost anxiety**: Per-token billing discourages trying computation-intensive dumb methods
2. **Rhythm drag**: Batch processing request response times measured in hours, breaking the smooth "think-verify-adjust" rhythm

### Liberation Through Local Deployment

After switching to locally deployed open-source models:
- Marginal cost approaches zero
- Large-scale iteration becomes a viable path
- 5090 cluster + vLLM: 32B model with 128k context needs only two GPUs

---

## Flywheel Four-Step Cycle

```
Trigger → Invoke Basic Module → Produce Small Progress → Refine
  ↑                                                      ↓
  ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### 1. Trigger

Identify a tiny, verifiable sub-problem.

### 2. Invoke Basic Module

Use simple, reliable atomic operations:
- Linear scan (rather than complex indexing)
- Semantic search (embedding + cosine)
- Structured output (JSON/tables)

### 3. Produce Small Progress

Each cycle must have measurable output:
- Extract one entity relationship
- Clarify one ambiguous concept
- Fill one information gap

### 4. Refine

Solidify progress into the knowledge base, becoming the next cycle's basic module.

---

## Design Principles

### 1. Problem Decomposition

Break grand problems into countless tiny, verifiable sub-problems.

### 2. Independence

Each cycle is an independent, logically clear process, not dependent on complex state.

### 3. High Success Rate

Each sub-task is designed to inevitably succeed, avoiding frustration.

### 4. Convergence

The flywheel direction is clear; each iteration moves closer to the goal.

### 5. Stagnation Point Breakthrough Strategy

Data flywheel "stagnation point" (extremely rare data) breakthrough method:
 Use VLM for initial harvesting
 Correct via Human-in-the-loop
 Form cold-start seed data

---

## Basic Module Examples

### Linear Scan

```python
# Don't over-engineer indexing; start with linear scan
for chunk in text_chunks:
    if is_relevant(chunk, query):
        yield extract_info(chunk)
```

### Semantic Search

```python
# embedding + cosine similarity is sufficient for most scenarios
def semantic_search(query, corpus, top_k=10):
    query_emb = embed(query)
    scores = [cosine(query_emb, doc_emb) for doc_emb in corpus_embs]
    return top_k_indices(scores)
```

### Structured Output

```python
# Force JSON output for easier downstream processing
prompt = """
Extract person relationships from the following text; output JSON format:
{"relations": [{"person_a": "...", "relation": "...", "person_b": "..."}]}
"""
```

---

## Model Selection Recommendations

### Recommended: Controllable Local Models

- **Qwen3-32B**: Stability verified in knowledge engineering tasks; stable output without special prompt tuning
- **Quantization**: INT4 quantized 32B model with 128k context window needs only two GPUs

### Not Recommended

- Expensive closed-source APIs (unless budget is unlimited)
- Models requiring complex prompt engineering just to output format

---

## Pitfalls to Avoid

1. **Over-engineered indexing**: Start with dumb methods first, then consider optimization
2. **Pursuing perfect data**: Accept imperfect starting points; rely on flywheel iteration
3. **Complex pipelines**: Each added link adds a failure point
4. **Premature optimization**: Have a 1.0 first, then talk about optimization

---

## Real-World Case

### Example: Structured Knowledge Graph

- **Input**: Tens of millions of words of novel text
- **Output**: Interactively queryable structured knowledge graph
- **Method**: Linear scan + semantic search + four-step flywheel
- **Deployment**: *(your own deployment address)*
- **Cost**: First version with closed-source API was costly; after switching to local deployment, marginal cost is zero

---

## See Also

- [T9. Data Strategy and MDP](../axioms/t09_data_strategy_mdp.md) — MDP concepts, data flywheel stagnation point breakthrough, data sovereignty and accumulation

---

## Changelog

| Date | Change |
|------|--------|
| 2026-02-21 | Promoted from OBSERVATIONS.md; organized as independent skill |
