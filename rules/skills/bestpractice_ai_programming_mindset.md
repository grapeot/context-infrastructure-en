# Core AI Programming Methodology

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: AI-assisted programming, Agent system design
- **Created**: 2026-02-21
- **Source**: Summarized from multiple AI programming practices
- **Last Updated**: 2026-03-01

---

## Foundational Axioms (see axioms for details)

The methodology in this document builds on the following axioms, not repeated here:
- **T05**: Cognition is an asset, code is consumable
- **T02**: Outcome determinism over process determinism
---

## Diagnosis and Resolution of the "70% Problem"

### Problem Essence

The common "70% problem" in AI programming — AI can complete 70%, but the last 30% always has issues — has a root cause: **the self-iteration feedback loop is broken**:

1. **AI cannot perceive whether output meets expectations**: no "eyes" to see results
2. **Success criteria are too subjective**: lacking a clear definition of "good," AI doesn't know which direction to iterate toward

### Solutions

1. **Open perception channels for AI**:
   - Let AI see execution results (screenshots, logs, test output)
   - Provide visual feedback when offering UI
   - Return complete output after executing commands

2. **Establish clear success criteria**:
   - Define "what good looks like" (not just "it runs")
   - Quantitative metrics over subjective descriptions
   - Provide reference examples or expected output

---

## Relationship Between Reasoning Model and Agentic Workflow

### Complementary, Not Substitutive

- **Reasoning Model**: excels at deep analysis, complex reasoning, planning
- **Agentic Workflow**: excels at coordinating execution, tool calling, state management

### Limitations of Reasoning Model

Reasoning Model's "reflection" is stateless — it cannot perceive changes in the external world. By the time thinking ends, the world has already changed.

### Recommended Architecture

Adopt a **hybrid architecture** in production:
- Reasoning Model for deep analysis and planning
- Agentic Workflow for coordinating execution and state management
- External orchestration for overall process control

---

## Boundaries of Cognitive Outsourcing

In an era of increasingly capable and affordable AI, we need clarity on which tasks can be outsourced and which must be retained:

### Can Be Outsourced

- Gap-filling: information gathering, formatting
- Mechanical execution: repetitive coding, document generation
- Rapid prototyping: exploratory implementation

### Must Be Retained

- Forming your own opinions
- Defining problems and success criteria
- Value judgment for key decisions
- Final review of output quality

---

## The "Intuition Over Program" Inflection Point

For complex semantic tasks, LLM's "black-box intuition" may be more robust and efficient than explicit logic code.

When tasks involve:
- Complex semantic understanding
- Multi-factor trade-offs
- Judgment with fuzzy boundaries

LLM's end-to-end processing may be more robust than explicit rules. This is a paradigm shift from "programmatic thinking" to "intuitive thinking."

---

## File System as Natural State Machine

Core design principles for local Agent mode:
- The file system itself is the most reliable state persistence layer
- State changes = file operations, naturally auditable and rollback-able
- Avoid the complexity of "in-memory state + manual persistence"

---

## Three Archetypes of Data Scientists in the AI Era

Skills are depreciating, but traits and character are becoming increasingly important. Three roles:

1. **Architect**: defines problems, designs systems, orchestrates capability boundaries
2. **Auditor**: evaluates quality, discovers patterns, cross-validates
3. **Full-stack Builder**: end-to-end delivery, rapid prototyping, integration verification

Core insight: the same person can play different roles, but clarifying the current role avoids mental confusion.

## Cautions

- **Productivity trap**: sacrificing developer mental bandwidth and flow state to save minor token costs is premature optimization
- **Physical anchor**: the final defense for complex logic verification is physical common sense (see `bestpractice_temporal_info_verification.md`)
- **Context decay**: periodically reflect and solidify methodology to avoid context loss between sessions

---

## Core Decisions for AI Implementation

Distilled from "Key Decisions in AI Implementation Through a Simple Task":

### 1. Use Local Coding Agent Instead of ChatGPT

- Reduce context transfer and implementation friction
- Agent directly operates on the codebase, not copy-paste
- ChatGPT is suitable for quick Q&A, not system development

### 2. Define Success Criteria Before Starting

- Establish tests as a feedback loop
- Define "what good looks like," not just "it runs"
- Tests are navigation signals for AI

### 3. Let Agent Handle Corner Cases Itself

- Outcome determinism vs process determinism
- Don't prescribe every step; let AI decide its own implementation path
- Focus on whether output meets expectations, not whether the implementation process is "correct"

### 4. Divide and Conquer to Handle Context Window Saturation

- 8 sub-agents processing in parallel
- Each sub-agent has a single responsibility
- Aggregate at the end rather than stuffing all information in at once

### 5. Prompt Bootstrapping and Outcome-Oriented

- Let AI iterate and improve itself
- Don't prescribe how to do each step
- Use 2 minutes to leverage 45 minutes of AI work — AI is a lever

---

**Last Updated**: 2026-03-01
