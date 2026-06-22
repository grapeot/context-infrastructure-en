---
id: axiom_docs_long_term_memory_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
raw_sources:
  - "contexts/blog/content/agentic-memory.md"
  - "contexts/blog/content/multi-agent.md"
  - "contexts/blog/content/ai-eternity.md"
  - "contexts/blog/content/life-api-part4.md"
  - "periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md"
---

# Docs as Long-Term Memory

## 1. Core Axiom

When projects and agent teams expand, context window limits become the biggest bottleneck. Documentation is not just a deliverable — it is the shared long-term memory system for both AI and humans. It keeps intent stable across multiple rounds of iteration, preventing context amnesia that leads to repeated pitfalls, self-contradiction, and forgetting global design. In AI-assisted development, doc-driven development is the key to breaking through scale limits — it transforms short-term context windows into persistent, versionable, diffable long-term assets.

## 2. Deep Reasoning

### 2.1 The Short-Term Memory Limit of Context Windows

Contemporary AI models' context windows are essentially a "seven-second-memory fish." It can remember code, decisions, and history within the current conversation, but once context is truncated (whether because the conversation is too long, a new session starts, or the task simply switches), that information is gone entirely. This limit is unnoticeable in small-scale projects (a few hundred lines of code), but becomes fatal when the codebase exceeds 5000 lines.

In actual development, this manifests as three typical failure patterns. The first is spatial forgetting: when AI modifies file A, it completely fails to see the same functionality already existing in file B, so it re-implements it, causing code duplication and logic conflicts. This is not AI being insufficiently smart — it's that the context window's auto-construction rules didn't include file B. The second is temporal self-contradiction: AI fixes error A in the first iteration, but after several rounds of debugging, when this fix disappears from context, AI forgets why it kept the fix and changes it back, reintroducing error A. The third is missing global perspective: especially when inheriting an existing codebase, AI lacks high-level design understanding of the entire system, causing it to prefer rewriting a feature from scratch rather than understanding and reusing existing code.

The root cause of all these problems points to the same fact: AI relies on the context window as its sole memory mechanism. Simple refactoring (splitting code into finer pieces) can only alleviate local problems but cannot fundamentally solve the challenge of insufficient global design understanding. Even with the cleanest code, AI still relies on short-term context to think — once context overflows, it forgets previous logic.

### 2.2 Doc-Driven Development: Building Long-Term Memory for AI

The core idea of doc-driven development is simple: don't just let AI write code — let AI maintain documentation. This documentation is not after-the-fact commentary but the project's "brain" — it records external behavior, product decisions, technical frameworks, high-level design, and historical attempts and lessons. When AI writes code, it can first read the docs and quickly gain a global perspective without stuffing all source files into the context window.

More importantly, this documentation becomes a citable, versionable, diffable asset. Unlike black-box heartbeat summaries (which may be rewritten or "forgotten"), documentation is explicit, controllable, and traceable. When you need to review why a certain decision was made, or why a certain approach was abandoned, the documentation is there. This explicitness itself improves work quality — it forces both AI and humans to make implicit knowledge explicit, a process that often surfaces problems not previously considered.

In practice, the doc-driven development workflow is: update docs → update code to align → run checks → Git records history. The key to this flow is treating documentation as a first-class deliverable, not an after-the-fact supplement. When AI makes major changes, it should first update the docs, then change the code according to the docs, ensuring code and docs stay aligned. The benefit is that documentation itself becomes a "design review" process — the design is scrutinized before the code is written.

### 2.3 Shared Memory in Multi-Agent Systems

In multi-agent systems, documentation's role becomes even more critical. When you have a planning agent (like o1) and an execution agent (like Claude), each has its own independent context window. If they only communicate through conversation, the planner's instructions easily get lost across the executor's multiple rounds of debugging. The solution is introducing a shared Scratchpad document as the communication bus between them.

The planner records the current task, strategy, known difficulties, and progress in this document. The executor updates the document with results and feedback after completing each feature or hitting a pitfall. This way, the planner can check current status at any time without stuffing all the executor's details into its own context. The executor can focus on specific work without being disturbed by high-level decisions. The power of this pattern is that it preserves instructions and progress without cramming every detail into every agent's context, forming a single source of truth spanning all agents.

But multi-agent systems also bring new challenges: how to maintain consistency across multiple agents. When two agents simultaneously read and write the same document, conflicts can arise. The solution comes from multi-person collaboration software experience: introduce locking mechanisms, auto-merge strategies, and diff analysis. These mechanisms ensure the document remains a reliable information source even under high concurrency.

### 2.4 From Static Documents to an Evolving Memory System

Initial doc-driven development may look simple: write a design document, then implement according to it. But in actual AI collaboration, the documentation itself continuously evolves. This evolution process reflects a deeper shift: from treating documentation as a "requirements spec" to treating it as a "living memory system."

In this evolving memory system, there are three key roles. Observer watches the project's daily progress, recording new discoveries, pitfalls encountered, and approaches tried. Reflector periodically reviews these observations, distilling patterns with long-term value and updating the core design documents. Promoter pushes these updates to all relevant agents, ensuring they all get the latest knowledge. This three-layer structure ensures the memory system captures both daily details and long-term patterns.

The value of this evolving memory system is that it records not just "what we did" but also "why we did it" and "what we learned." When a new agent joins the project, it can see not just the current code but also how this code evolved, why certain decisions were made, and which approaches were tried before and why they failed. This sense of history lets new agents integrate into the project faster and avoid repeating pitfalls.

### 2.5 From Prompt Engineering to Context Architecture

In the past, we treated prompts as "instructions" — the more cleverly you wrote them, the better AI performed. But under the doc-driven development framework, the prompt's role undergoes a fundamental shift. It is no longer a standalone instruction but a "door key" that opens a larger "world" built from documentation.

The deeper meaning of this shift is that we move from "crafting prompts meticulously" to "building immersive context." AI doesn't reason from scratch — it tries to become an acceptable collaborator within the history, style, rhythm, tone, preferences, and structural fragments you provide. When this context is rich and authentic enough, AI naturally emerges with smarter capabilities within it. This is "context-driven emergence" — a path to evoking AI's latent capabilities by constructing complex contextual spaces.

In this new paradigm, you are not "assigning tasks to AI" but "building a world where AI can become smarter." What you write is not a question but an environment for AI to operate in. This environment includes the project's design documents, key technical decisions, known pitfalls, acceptance criteria, and even your work style and aesthetic standards. Once AI is immersed in this environment, it can understand your implicit expectations and make decisions more aligned with your intent. The essence of this shift: from "instruction execution" to "environment adaptation."

## 3. Application Criteria

**When to apply**: Multi-day work, multi-agent collaboration, repeatedly returning to the same problem, or scenarios where the repo is too large for chat-based "remembering" to work. Especially when you find yourself repeatedly explaining the same design decision, or AI self-contradicts across multiple iterations — this is a signal that you need doc-driven development.

**How to practice**: Maintain continuously evolving design documents and scratchpads, treating docs as first-class deliverables. Establish the "update docs → update code → run checks" workflow, with Git providing history. For multi-agent systems, enforce shared documents as the communication channel rather than conversation. Periodically review docs, distilling observations with long-term value into rules.

## 4. Pitfalls and Insights

### 4.1 The "Save Everything" Trap

A common misunderstanding is that since documentation is long-term memory, all information should be saved. This turns documentation into an undifferentiated information heap, full of expired, low-value, mechanically repetitive content. The result: when AI needs to extract useful information from docs, it gets drowned in noise instead. Declining information density directly causes declining AI comprehension — it needs to spend more context filtering useful information, actually increasing the context burden.

The right approach is conscious "garbage collection." Not all observations are worth saving. An effective filtering criterion: if this piece of information won't have any reuse value for the project within the next 3 months, discard it decisively. Better to record less than to pad. This principle comes from AI Heartbeat's knowledge base design: information density is key — you need to think like a senior architect, not like a recorder. High-quality documentation should be refined, targeted, and capable of directly guiding AI action.

### 4.2 Static Docs vs Evolving Memory

Another trap is treating documentation as a "frozen spec." You write a design document at project start and never update it again. The result: docs and code gradually diverge, and eventually the docs become outdated and untrustworthy. When AI reads outdated docs, it gets misled and makes decisions inconsistent with the current project state.

Truly valuable documentation is living and evolving. It updates as the project progresses, reflecting the latest design decisions and lessons learned. This evolution process is itself a learning process — each time you update docs, you're reflecting on "why we made this decision," which often surfaces problems not previously considered. In multi-agent systems, this evolution process becomes even more important because new agents need to quickly understand the project's current state rather than being misled by outdated docs. Documentation update frequency should match the project's rate of change — fast-iterating projects need more frequent doc updates.

## 5. Related Axioms

- **A01: Ask-Do Paradigm Shift** — Doc-driven development is the foundation of the ask-do paradigm. Clear documentation defines what "done" means, enabling AI to iterate autonomously.
- **A03: IC to Manager Mindset Shift** — Maintaining documentation is a management skill, not a programming skill. It requires you to clearly define problems, decompose tasks, and provide enough context.

## 6. Practice Advice

**Things you can do immediately**:
1. Write a simple design document for your ongoing project, including background, key decisions, known pitfalls, and acceptance criteria.
2. Establish a Scratchpad to record current difficulties, approaches tried, and test results.
3. When assigning tasks to AI, have it read the docs first, then start working. Observe how this changes its understanding and output quality.
4. Periodically review docs, delete expired content, distill patterns with long-term value.

**Long-term mindset shifts**:
- Stop treating docs as after-the-fact commentary — start treating them as the project's "brain."
- Stop expecting AI to automatically understand your implicit expectations — start making your knowledge explicit.
- Stop using conversation as the sole communication channel between agents — start using docs as the single source of truth.
- Stop writing docs that freeze after one write — start maintaining a living, evolving memory system.

When you see AI reducing self-contradiction because of clear documentation, or multiple agents collaborating more smoothly because of shared docs, you'll understand that doc-driven development is not just a technical practice but a fundamental mindset shift. It transforms AI from a "clever code generator" into a genuine "long-term collaborator."
