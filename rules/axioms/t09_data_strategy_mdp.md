---
id: axiom_t9_data_strategy_mdp_2026
category: technical
created: 2026-03-01
updated: 2026-03-01
---

# T09. Data Strategy and MDP

## 1. Core Axiom

In AI products, data capture is itself the first-stage product (MDP = Minimum Data Product). Data sovereignty and local accumulation create lasting competitive advantage.

## 2. Deep Reasoning

**The Paradigm Shift of the MDP Concept**

Traditional product thinking: product first, data as a byproduct. MDP thinking: data capture is itself the product. This means establishing a data collection closed loop before feature completeness — even simple user interaction logging forms an iterable foundation.

**Breaking Through the Data Flywheel's Standstill Point**

When initial data is scarce, VLMs (Vision Language Models) can serve as the initial harvesting tool, rapidly generating annotations or features. Then introduce human feedback to form a closed loop, progressively improving model quality. This process is not one-shot — it is continuous iteration, where each round of feedback strengthens the next round's data quality.

**The Architectural Choice of Data Sovereignty**

Local agents retain data control; cloud solutions mean data outflow. This is not merely a technical choice — it is a strategic choice. Locally accumulated data becomes an irreplicable asset, while cloud dependency faces vendor lock-in and data leakage risks.

**The Entropy Increase Phenomenon in Data Labeling**

As labeling scale expands, quality often declines — this is entropy increase in the labeling process. Sampling audits and continuous quality monitoring are needed to counter this trend and ensure dataset usability.

## 3. Application Criteria

Apply this axiom in the following scenarios:
- When building AI features or ML models, prioritize data collection mechanisms
- When choosing between cloud vs. local architecture, evaluate data sovereignty costs
- When designing personalization systems, establish a closed loop for local data accumulation

## 4. Relationships with Other Axioms

- **T04 Data Over Opinion**: Establishes the data-first mindset at a higher level
- **M01 Closed-Loop Calibration**: The data flywheel is essentially a calibration loop, continuously approaching truth through feedback

**See also**: [Knowledge Flywheel Design Pattern](../skills/workflow_knowledge_flywheel.md) — Iterating with simple methods in knowledge engineering
