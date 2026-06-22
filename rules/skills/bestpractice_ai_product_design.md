# AI Product Design Principles

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: AI product design, interaction design, system architecture
- **Created**: 2026-02-22
- **Source**: Summarized from multiple AI product practices

---

## The Fundamental Conflict: Linear Chat vs Nonlinear Knowledge Work

### Problem Essence

The dominant form of AI products is the "linear chat entry point" (ChatGPT, Claude Chat), but the nature of knowledge work is nonlinear:
- Thinking jumps, branches, and backtracks
- Requires parallel reference across multiple documents
- Needs visual structures (mind maps, outlines)

### Conflict Manifestations

- Users are forced to handle complex problems in a single thread
- Context piles up linearly, making it hard to locate key information
- Cannot explore multiple lines of thought in parallel

### Design Implications

- Linear chat suits simple Q&A, not deep knowledge work
- Knowledge tools need to support nonlinear structures (branching, linking, visualization)
- Consider a hybrid "conversation + document" form

---

## Perception-Rule Decoupling Principle

### Architectural Decision

Strictly separate the "Perception" layer from the "Rules" layer.

### Perception Layer Responsibilities

Output raw perception signals:
- Lane position, line type
- Vehicle heading angle
- Road context

### Rules Layer Responsibilities

Make business judgments based on perception signals:
- What constitutes "deviation"
- When to alert
- Alert severity level

### Benefits of Decoupling

1. **Fast iteration**: product rules can be modified independently without retraining models
2. **Personalization**: different customers/regions can have different rules
3. **Auditability**: rule changes are traceable, model output remains stable
4. **LLM integration**: future LLMs can flexibly combine signals

### Applicable Scenarios

- Safety-critical systems (requiring deterministic rules)
- Multi-market/multi-customer products (requiring personalization)
- Business logic requiring rapid iteration

---

## The One-Size-Fits-All Product Definition Trap

### Problem

"A single product for all customers" inevitably fails in the face of diverse needs.

### Root Cause

- Different customers have vastly different usage scenarios
- Different risk tolerance levels
- Different business processes

### Solution

- Provide configurable parameters and rules
- Let PMs or future LLMs flexibly combine signals
- Give users the authority to define "what good means"

### Case Insight

LDW lane departure warning: different customers have completely different definitions of "deviation," alert timing, and tolerance levels.

---

## Guideline Overload Problem

### Phenomenon

A 10-page Guideline used directly as a Prompt will confuse the LLM, making fine-grained trade-off handling impossible.

### This Is a Hard Limitation of General-Purpose LLMs

- LLMs are not good at handling many constraints simultaneously
- Constraints may have implicit conflicts with each other
- Lack of business context understanding

### Solution

1. **Structured constraints**: break the Guideline into independent rules, apply progressively
2. **Few-shot examples**: use cases instead of long documents
3. **Hybrid architecture**: LLM handles perception, deterministic programs handle rules

---

## Multi-Agent Design Principles

### Core Insight

LLMs have inherent "personalities":
- O3: good at search and exploration, but shallow analysis
- Gemini: weak at search, but deep analysis and strong synthesis

These personalities are difficult to change through prompts.

### Design Implications

1. **Leverage complementary strengths**: let different models do what they're good at
2. **Don't mimic human role divisions**: PM/QA/Dev are human organizational patterns, not applicable to Agents
3. **Context window separation**: different Agents handle different context subsets
4. **Force handoff when necessary**: when a model resists instructions, force a switch through code

### Current-Stage Recommendation

Hybrid systems combining hard rules and AI capabilities are more reliable than purely Agentic systems.

---

## Product Definition Precedes Engineering Implementation

### Core Bottleneck

The core bottleneck in projects like red-light detection is the lack of a PRD, not technical capability.

### Strategy

- Turn RFC meetings into PRD discussions
- Clarify product requirements first, then discuss engineering details
- "What we want" is more important than "how to implement it"

### Causal Chain

Product form → evaluation method → model development strategy

The starting point is a clear product definition.

---

## Cautions

- Consider regulatory differences across markets/regions
- Safety-critical systems need deterministic fallbacks
- User trust is hard to build, easy to break

---

## Changelog

| Date | Change |
|------|--------|
| 2026-02-22 | Initial version, consolidating multiple product design observations |
