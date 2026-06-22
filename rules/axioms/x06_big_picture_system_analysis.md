---
id: axiom_x6_big_picture_system_analysis_2026
category: cross_domain
created: 2026-03-01
updated: 2026-03-01
---

# X6. Big-Picture System Analysis

## 1. Core Axiom

When facing complex systems, missing documentation, and scattered logic, first find the biggest decision points. Accumulate questions before seeking answers. The places that contradict your assumptions are the most valuable signals.

## 2. Deep Deduction

### Methodology Steps

1. **First find the biggest decision points** — don't try to understand everything; first grasp the backbone. Every system has one or a few core decisions that determine its overall architecture and behavior. Finding them matters more than understanding the details.

2. **Continuously ask questions and record them** — questions themselves are clues; don't rush to solve them. Each question points to a cognitive gap. The process of recording questions is the process of organizing your thinking.

3. **Aggregate questions to find cognitive confusion points** — multiple seemingly independent questions often point to the same root cause. By aggregating questions, you can quickly locate the system's core confusion points.

4. **Pay attention to "places that contradict assumptions"** — the least intuitive parts often hide the system's core or improvement opportunities. These places are worth deep exploration.

### Relationship to Other Methods

This method is complementary to progressive disclosure (from coarse to fine) and documentation-first (understanding first, documentation follows). The "Data vs Opinion decision principle" in the source file is already covered by T04 (Data Over Opinion).

## 3. Application Criteria

Applicable scenarios:
- Facing unfamiliar systems or new domains
- Dealing with legacy codebases or complex architectures
- Projects with missing or incomplete documentation
- Needing to quickly understand how a system fits together

## 4. Relationship to Other Axioms

- **T04 Data Over Opinion** — the decision principle in the source file is already covered by T04; this axiom focuses on the methodology level
- **X02 Hypothesis-Driven Systematic Debugging** — both use a hypothesis-driven approach, but X02 focuses on debugging while this axiom focuses on system analysis
- **M02 Reverse Debugging Mindset** — both accelerate cognition by shrinking the possibility space
