---
id: axiom_a13_tech_adoption_stages_2026
category: ai_agentic
created: 2026-03-01
updated: 2026-03-01
raw_sources:
  - "rules/skills/bestpractice_tech_adoption.md"
---

# A13. Technology Adoption Stages

## 1. Core Axiom

The adoption of technology that changes a system is not component replacement but system reset. Electric motors took 60 years to transform the entire economic system, not because of the technology itself, but because factories, power grids, and production processes needed to be redesigned. The same applies to AI.

Technology adoption has three stages: **Driver** (passive use) → **Co-pilot** (collaborative optimization) → **Architect** (system reset). Each stage has different bottlenecks, and the solutions are completely different.

## 2. Deep Reasoning

**Steam Engine Thinking vs Power Grid Thinking**

In the steam engine era, factories used one large steam engine to drive all machines. When electric motors appeared, people initially used them the same way — one large motor replacing the steam engine. But the real revolution came from the power grid: each machine independently powered, factories could flexibly lay out and start on demand. This required completely different infrastructure.

**The Focus Shift Across Three Stages**

- **Driver stage**: Users passively receive AI output. The bottleneck is prompt quality and model capability.
- **Co-pilot stage**: Users and AI collaborate iteratively. The bottleneck shifts to data quality, feedback loops, and evaluation criteria.
- **Architect stage**: Systems are redesigned around AI. The bottleneck is infrastructure — documentation clarity, data accessibility, API stability, evaluation frameworks.

**The Infrastructure Bottleneck Metaphor**

A supercar can't run fast on a dirt road. Similarly, the strongest AI model, faced with messy data, unclear requirement definitions, and unstable APIs, cannot deliver value.

**Adoption Checklist**

Assess readiness to enter the Co-pilot or Architect stage:
- Is documentation clear enough for AI to understand business logic?
- Is data accessible and structured?
- Are APIs stable with clear error handling?
- Are clear evaluation criteria defined (rather than vague "works well")?

## 3. Application Criteria

Reference this axiom when:

- Evaluating new technology adoption: first diagnose which stage you're in, then decide investment direction
- Hearing complaints that "AI isn't good enough": the problem may not be the model but the infrastructure
- Designing AI-native systems: prioritize infrastructure investment over pursuing model upgrades

## 4. Relationships with Other Axioms

- **T01 Infrastructure Over Components**: Direct echo. The long-term return on infrastructure investment far exceeds point optimization.
- **A08 Prompt Quality is the Primary Lever**: Holds true in the Driver stage; entering Co-pilot, data quality and evaluation framework weight rise.
- **A12 AI-Native Development Paradigm**: The concrete practice of the Architect stage — redesigning system architecture around AI capabilities.
