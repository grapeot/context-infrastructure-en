---
id: axiom_a06_framework_worldview_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
raw_sources:
  - "/Users/grapeot/co/knowledge_working/contexts/blog/content/agentic-ai-frameworks-en.md"
  - "/Users/grapeot/co/knowledge_working/contexts/survey_sessions/pi-mono-agent-toolkit-analysis.md"
  - "/Users/grapeot/co/knowledge_working/contexts/survey_sessions/agent_architecture_selection_survey_20260222.md"
  - "/Users/grapeot/co/knowledge_working/contexts/survey_sessions/ai_programming_paradigm_shifts_survey_20260219.md"
  - "/Users/grapeot/co/knowledge_working/rules/axioms/a09_builders_mindset_moat.md"
---

# A6. Framework Choice as Worldview Lock-In

## 1. Core Axiom

Choosing an AI framework in a rapidly evolving domain is not a technical decision — it is a philosophical bet on future adaptability. Each framework is not merely a tool collection but a complete worldview — about how agents should think, collaborate, and execute. Choosing a framework means seeing the world through the framework author's lens, which, at a moment when the domain's foundations have yet to settle, severely limits your depth of understanding and adaptability.

---

## 2. Deep Reasoning

### 2.1 Every Framework is a Worldview

The major frameworks in the agentic AI domain each represent different understandings of what an agent fundamentally is. AutoGen believes multi-agent asynchronous collaboration is the key to solving complex problems — its entire architecture revolves around message passing and inter-agent conversation. LangGraph believes workflows are essentially directed graphs, with state flowing between nodes and conditional edges determining execution paths; this perspective leads to complex persistence, event systems, and async mechanisms. SmolAgents takes a completely different philosophy: code is the clearest intermediate medium, and agents should directly generate and execute code rather than going through abstract tool interfaces. All three frameworks work technically, but their design philosophies are mutually incompatible.

Locking into a framework means your thinking will be shaped by the framework designer's assumptions. If you later develop a different way of thinking — whether through your own practical experience or breakthrough advances in the domain — switching frameworks may be more complex than starting from scratch. Migrating from SmolAgents to LangGraph is not just a code rewrite but a complete mindset shift, because the two frameworks' foundational assumptions are fundamentally incompatible.

### 2.2 The Cost of Premature Lock-In in a Rapidly Evolving Domain

Agentic AI is still changing rapidly, and any breakthrough understanding could happen at any time. AutoGen's shift from v0.3 to v0.4 was essentially a complete rewrite, showing that even mature frameworks can face fundamental rethinking. Premature lock-in not only brings technical debt but also limits your ability to fully understand the domain. When you're bound by a framework's abstractions, you can't see the underlying real mechanisms; when new understanding emerges, you've already invested too much to pivot.

This problem doesn't exist in iOS development because the foundations of GUI programming have been stable for decades. MVC works because it's built on verified foundations unlikely to change. But agentic AI's foundations are still in flux. Frameworks' high-level abstractions are destined to be fragile because they're built on assumptions that haven't yet settled.

### 2.3 The Actual Value of Frameworks is Limited

From a short-term benefit perspective, existing frameworks provide far less value than advertised. Building a complete agent system (LLM + tool protocol + multi-turn orchestration) takes only five minutes. This system contains all the core elements of agentic AI: a language model that can call tools, a protocol defining tool interfaces, and a loop managing multi-turn conversation. Frameworks don't save much effort — instead, they add complexity when you need customization.

Worse, many frameworks suffer from over-abstraction. When you need to connect existing interfaces or do custom work (common in enterprise environments), you often have to trace through eight layers of abstract interfaces to find where to make changes. LangChain is notorious for this: you want to make a simple modification and find yourself trapped in a deep class inheritance tree, each layer adding new abstractions. This is the classic failure pattern of rapidly evolving domains — frameworks' high-level abstractions replace the builder's intuition and end up becoming obstacles instead.

### 2.4 The Fundamental Difference Between Framework and Library

A critical distinction is needed here. Not all agentic AI tools are "frameworks." pi-mono provides an instructive contrast: it is a library, not a framework. pi-mono provides only four basic tools (read, write, edit, bash), with a system prompt under 1000 tokens. Its design philosophy is "what's missing matters more than what's included" — the author explicitly rejected MCP support, sub-agents, plan mode, and other "hot" features because these would increase context overhead or introduce black boxes.

A framework imposes a worldview; a library merely provides tools. A framework says "this is how you should think about problems"; a library says "these are tools you can use, how you use them is up to you." LangGraph is a framework; pi-mono is a library. This distinction is critical because a library gives you choice, while a framework limits your choices.

---

## 3. Application Criteria

### 3.1 When to Use Framework vs Library

| Scenario | Use Framework | Use Library |
|----------|--------------|-------------|
| **Domain maturity** | Foundational concepts are stable (e.g., iOS GUI) | Domain is still rapidly evolving (e.g., agentic AI) |
| **Team size** | Large team needs unified thinking | Small team or personal project |
| **Customization needs** | Low (framework defaults suffice) | High (frequent need to modify underlying logic) |
| **Learning curve** | Willing to invest time learning framework concepts | Want to get started quickly, deepen gradually |
| **Long-term stability** | Framework's major versions won't change | Can accept changes in underlying implementation |
| **Integration complexity** | Integration within framework is simple | Need to connect multiple external systems |

### 3.2 Decision Criteria

Before choosing a framework, ask yourself these questions:

1. **Have the foundational concepts of this domain stabilized?** If no, the framework's high-level abstractions will quickly become obsolete.
2. **Do I understand the framework's core assumptions?** If you can't clearly articulate what the framework author's worldview is, you're not ready to be locked into it.
3. **If I need to change my thinking, what's the migration cost?** If migration cost is high, the risk of choosing a framework is high.
4. **Does the framework provide AI-friendly documentation?** If the framework's docs can't be directly understood and used by AI tools (like Cursor), its value in the AI era is greatly diminished.
5. **Can I quickly build a prototype without using the framework?** If yes, the framework's value is limited.

---

## 4. Pitfalls and Insights

### 4.1 The "Eight Layers of Abstraction" Nightmare

When you use an over-abstracted framework, a simple modification becomes a nightmare. You want to change a tool's behavior, but this tool is wrapped in a class, which inherits from another class, which depends on a third class... eventually you find yourself needing to understand eight layers of abstract interfaces to find where the real change needs to happen. This not only wastes time but also fragments your understanding of the framework.

This problem is especially severe in rapidly evolving domains because framework designers cannot foresee all usage scenarios. Their abstraction assumptions quickly become obsolete, and you're trapped in these obsolete assumptions. pi-mono's author explicitly criticized this, saying "over-abstraction is the failure pattern of high-speed development domains."

### 4.2 The "Five-Minute Prototype" Insight

Building a basic agent system takes only five minutes. This fact matters because it shows that frameworks' value lies not primarily in saving initial development time but in providing a "best practice" template. But in a rapidly evolving domain like agentic AI, "best practices" themselves are uncertain. A framework author's best practices may be obsolete in six months.

This means, rather than relying on a framework's "best practices," it's better to build your own system from first principles. The additional cost of doing so is small (because the basic system is simple), but the benefit is large (because you maintain full flexibility and depth of understanding).

### 4.3 The "Builder's Mindset" Shift

Frameworks encourage a passive tool-user mentality: you learn the framework's API, think the framework's way, accept the framework's limitations. But the agentic AI era demands a builder's mindset: when existing tools don't meet your needs, you should be able to quickly build your own tools. This mindset shift is critical.

pi-mono's design embodies this: it provides a minimal toolset, then encourages users to extend functionality by writing Extensions (TypeScript modules) or Skills (markdown files). When an agent needs a new capability, it can read existing extension code, write a new extension, and have it take effect immediately. This is a shift from "using a framework" to "building your own tools."

### 4.4 The Absence of "AI-Friendly Documentation"

None of the existing agentic AI frameworks provide documentation specifically designed for AI. LangGraph, AutoGen, and SmolAgents' documentation is all written for humans, full of natural language ambiguity and implicit assumptions. When AI tools (like Cursor) try to use these frameworks, they must do extensive trial and error because the information in the docs isn't precise enough.

In contrast, pi-mono's tools are themselves code, and its documentation is code comments and README. This lets AI directly read and understand without additional explanation. This is an important design insight: in the AI era, a tool's usability depends not only on whether humans can understand it but also on whether AI can understand it.

---

## 5. Related Axioms

**A9. Builder's Mindset is the Moat** — The decision of framework choice should be based on whether you have the ability and willingness to be a builder. If you choose a framework, you give up the builder's flexibility; if you stay with the library approach, you retain the builder's power.

---

## 6. Practice Advice

### 6.1 How to Make Framework Choices in the Agentic AI Domain

1. **Start from first principles**: Don't jump straight to a framework. First understand the core concepts of agents: LLM, tools, multi-turn orchestration. Use agentic programming tools like Cursor to gradually build your own system. This process itself is learning.

2. **Stay framework-neutral**: Don't deeply depend on any framework before the domain stabilizes. If you must use a framework, choose libraries that provide minimal abstraction (like pi-mono) rather than frameworks that impose a worldview (like LangGraph).

3. **Re-evaluate periodically**: Every three months, ask yourself: is my current framework choice still reasonable? Has the domain produced new understanding? Am I constrained by the framework's limitations?

4. **Invest in transferable knowledge**: Don't just learn a framework's API — learn the foundational concepts of agentic AI. This knowledge is useful in any framework, while framework APIs will keep changing.

5. **Embrace the builder's mindset**: When a framework doesn't meet your needs, don't try to force-fit the framework — build your own tools. This has become especially easy in the AI era because AI can help you prototype quickly.

### 6.2 When to Consider Using a Framework

Only consider using a framework when all of the following conditions are met:

- The domain's foundational concepts have stabilized (at least 2-3 years without fundamental change)
- The framework's major versions remain stable (no frequent large changes)
- Your team is large enough to need unified thinking for coordination
- The framework's "best practices" genuinely and significantly accelerate development
- The framework's documentation is clear enough that AI tools can also understand it

In the agentic AI domain, none of these conditions are currently met. So now is not the time to choose a framework.

---

## 7. Summary

Framework choice is a long-term commitment that affects your thinking, learning path, and adaptability. In rapidly evolving domains, the risk of this commitment is high. Agentic AI is still rapidly evolving, foundational concepts are still settling, and any framework's worldview may be proven incomplete or wrong in the near future.

The wisest approach is to stay framework-neutral, start from first principles, use libraries rather than frameworks, and embrace the builder's mindset. The cost of doing so is low (because the basic system is simple), but the benefit is high (because you maintain full flexibility and depth of understanding). When the domain finally stabilizes, frameworks' value will truly emerge. By then, you'll have enough knowledge and experience to make an informed choice.
