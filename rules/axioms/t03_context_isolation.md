---
id: axiom_context_isolation_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T03. Context Isolation: The Source of Multi-Agent Value

## 1. Core Axiom

The leverage of multi-agent systems comes from information domain isolation (independent contexts + shared scratchpad), not from mimicking organizational structures. The purpose of isolation is not division of labor — it is to let each agent make better decisions in a clean information environment.

## 2. Deep Reasoning

### Cognitive Load and Context Competition

The reason Cursor gets stuck in loops (fixing Bug A while reintroducing it in the process of fixing Bug B) is fundamentally that planning and execution details compete for attention within the same context window. When a single model carries both high-level planning and low-level implementation, it must first filter out the parts that are actually useful for planning from a messy pile of information before it can make a decision. This imposes an enormous cognitive load on the model. The reverse is also true: if the model dives into execution first, it easily loses track of what the planner said or loses focus amid the flood of execution details. The result is neither good planning nor good execution — both suffer. This is not a model capability problem; it is an information architecture failure — mixing things that should not be mixed.

Splitting Planner from Executor, even before switching to a stronger model, immediately reduces cognitive load and error rate. The Planner can focus on global decisions, verification, and reflection; the Executor can concentrate on low-level implementation and debugging. This simple layering lets each role work in a relatively clean information environment, leading to better decisions. The key: isolation is not about mimicking organizational structure — it is about making information flow manageable.

### Persistent State and the Amnesia Problem

But splitting roles alone is not enough. If Planner and Executor still communicate through conversation, they face a fatal problem: as soon as the context window grows long or gets truncated, the Planner's instructions are completely lost. For example, the Planner earlier said "remember to run a version compatibility test," but after the Executor debugs for several rounds and Cursor truncates the context window, that sentence disappears. Since it is no longer in the Executor's context window, the next time the Executor runs, it will have completely forgotten about it. This is like a company where both management and execution layers are busy working hard, but no one does the "minor" task of writing documentation, so the execution layer has no ability to track progress and relies entirely on the boss's reminders. The boss themselves can't remember the technical details and comes asking the same questions every day.

The solution is to enforce a shared Scratchpad document. Any analysis, test results, bugs encountered, and final discussion conclusions are written into this file. This way, the Planner can check current difficulties and progress in the document at any time and leave new task instructions; the Executor, after completing a feature or hitting a pitfall, updates the document with results and feedback, and the Planner won't forget after reading it. By turning the conversation pipe into a persistent notebook, we essentially solve the LLM context loss problem. Even if the conversation refreshes temporarily, just referencing the document again is enough. The probability of amnesia and stepping on the same pitfall drops immediately. This is not just an engineering trick — it is turning a fragile chat into a persistent state machine.

### Over-Engineering and the Necessity of Constraints

A stronger Planner (e.g., o1) brings deeper thinking but also raises the risk of over-engineering. An experienced senior engineer would validate on small-scale data first, then deploy to large-scale data, saving a lot of debugging time. But an insufficiently restrained Planner often jumps straight to debugging on the final large-scale data, or turns a small program design into a Concurrent Large-Scale Platform, making the process extremely bloated. This is like hiring a famous consulting firm for your human team — these consultants, to show how impressive they are, often produce exquisitely elaborate but bloated proposals. The people on the ground work hard, but it ultimately contributes nothing to the actual business goal and may not even improve efficiency.

Therefore, isolation must be paired with constraints and explicit verification. Through prompting, give the Planner a Founder Mindset — don't always aim for a one-shot, industry-best complete platform; instead, Bias for Action, seize whatever opportunity presents itself. Build a simple prototype first, validate feasibility, then add more features step by step. In particular, when the Planner assigns tasks to the Executor, it must clarify the necessity of each decomposition step and the verification method. At the same time, let the Executor raise questions in the document's feedback area — if a plan seems too complex, it can challenge the Planner to re-examine whether it is truly necessary or to decompose further. Use this set of interaction and acceptance mechanisms to control the Planner's reasoning.

### Cross-Verification and Abstract Thinking

When contexts stay clean, a multi-agent system can do genuine cross-verification and abstract thinking, rather than drowning in each other's noise. A clean Planner context means it can see the global decision history and verification results, rather than being submerged in execution details. A clean Executor context means it can focus on the current task, rather than being distracted by past planning discussions. This isolation lets both agents make high-quality decisions in their respective information domains, then coordinate effectively through the shared Scratchpad. The result is a system that can do both thoughtful planning and precise execution, rather than compromising on both.

## 3. Application Criteria

**When to use**:
- Tasks that simultaneously require macro-level planning and low-level editing/debugging
- When an agent starts looping/regressing due to context overload
- Long-running tasks that span multiple context window truncations
- When planning and execution have different failure modes (planning failure = wrong direction; execution failure = wrong details)

**How to practice**:
1. Define roles by information domain (Planner, Executor, optional Evaluator), not by organizational structure
2. Provide independent context for each role, clarifying what information each should see
3. Enforce a shared scratchpad to record goals, decisions, test results, and next actions
4. Design clear handoff artifacts: Planner outputs verification criteria and decomposition plans; Executor outputs execution results and feedback
5. Conduct explicit acceptance checks in the scratchpad regularly, rather than relying on implicit understanding

## 4. Pitfalls

**Pitfall 1: Isolation becomes silos**. If Planner and Executor contexts are completely isolated without an effective communication mechanism, they become two independent systems working at cross-purposes. The Scratchpad must be alive, regularly updated — not a dead document.

**Pitfall 2: Over-designed handoff artifacts**. Trying to guarantee perfect communication through complex handoff protocols only increases system complexity. The best handoff artifacts are simple, verifiable, and human-readable.

**Pitfall 3: Isolation becomes an excuse to evade responsibility**. The Executor cannot use "this is not in my context" as an excuse to ignore obvious problems. Isolation is for improving efficiency, not for shirking responsibility.

**Pitfall 4: Ignoring the cost of isolation**. The coordination overhead of multi-agent systems is real. Only when task complexity is high enough, or a single agent's context is genuinely the bottleneck, does the benefit of isolation exceed its cost.

## 5. Related Axioms

- **T02 Results Certainty Over Process Certainty**: The purpose of isolation is to let each agent better verify its own output, rather than trying to guarantee correctness through micromanagement.
- **T05 Cognition Is an Asset, Code Is a Commodity**: Isolation lets the Planner focus on capturing cognition (understanding, verification criteria, decision rationale) rather than being submerged in execution details.
- **T06 Dependency Topology Over Task Count**: The granularity of isolation should be determined by information dependency relationships, not arbitrary task decomposition.
- **T07 Isolation-Processing-Verification Loop**: Context isolation is the foundation of this loop: the Planner collects facts and plans in isolation, the Executor processes in isolation, and the shared Scratchpad is the verification interface.
