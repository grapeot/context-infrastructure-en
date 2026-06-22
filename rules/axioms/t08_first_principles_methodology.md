---
id: axiom_first_principles_methodology_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T08. First-Principles Methodology Design

## 1. Core Axiom

Before adopting any framework, restate the problem from first principles (uncertainty, constraints, success criteria), and borrow only the parts that directly serve it. A methodology is not a fixed set of rituals — it is a product designed for a specific user, a specific task, and specific failure modes.

## 2. Deep Reasoning

### 2.1 The Hidden Cost of Frameworks: Worldview Lock-In

A complete framework is often a form of worldview lock-in. It quietly smuggles in assumptions about roles, phases, and artifacts that may not match your domain. When you choose a framework, you are not just choosing a set of tools — you are choosing the framework author's understanding of "what is the right way to solve problems." This is especially dangerous at moments when the domain's foundations have not yet settled. Agentic AI is still evolving rapidly; any mid-to-high-level abstraction is destined to be fragile — AutoGen's transition from v0.3 to v0.4 was essentially a complete rewrite, showing that even mature frameworks can face fundamental rethinking. Premature lock-in not only brings technical debt but also limits your ability to fully understand the domain. When you are bound by a framework's abstractions, you cannot see the underlying real mechanisms; when new understanding emerges, you have already invested too much to pivot.

### 2.2 The Mismatch Between Human Organization and AI Systems

Methods built for coordinating humans (rituals, role granularity, process certainty) can backfire when the bottleneck is AI reliability or scientific uncertainty. The BMAD-METHOD case is instructive: it mechanically transplanted human professional divisions (Analyst, PM, Architect, Scrum Master, Developer, QA) into the AI world. But this assumption itself deserves scrutiny. Human society has professional specialization because we are too weak — one person cannot, within a dozen years of education, simultaneously master product, design, engineering, and testing. But LLMs are different. A sufficiently strong model can simultaneously understand business, design architecture, write code, and run tests. When you give it a prompt saying "you are a senior software engineer," you are actually constraining it, not enhancing it. You are dragging an omniscient, omnipotent LLM down to the level of a weak human who can only wear one hat.

Real multi-agent value should come from context isolation, not role-playing. The boundaries between different agents should be drawn based on the coupling of the tasks themselves, not based on human society's professional divisions. The split between a planning agent and an execution agent exists because planning and execution have completely different context requirements — not because "PM and Developer are different roles in human society."

### 2.3 Methodology as Product: A Design Perspective

I treat methodology as a product: it needs a user (me/the team), a job-to-be-done, and measurable failure modes. This perspective changes everything. Instead of asking "does this framework look disciplined," ask "can this methodology help me solve my specific problem." In the FCW/TTC debate retrospective, backward-chaining engineering management clashed with modeling uncertainty; this taught me to choose methods by uncertainty intervals, not by whether they look "disciplined."

When uncertainty is high (e.g., exploratory research, early stages of a new domain), heavy processes become a burden. What you need is fast feedback loops, flexible iteration, and minimal documentation. When uncertainty is low (e.g., known engineering tasks, clear requirements), structured processes have value — they ensure no details are missed and no detours are taken. If the same methodology works for both situations, it means it has not truly understood the nature of the problem.

### 2.4 The Cost of Overweight Processes: Using a Sledgehammer on a Thumbtack

BMAD's standard process is: market research → project brief → PRD → architecture document → user stories → development cycles → acceptance and release. This process is reasonable for medium-to-large projects requiring long-term maintenance. But the problem is, not all software development needs such a process. The AI era has produced a large amount of "user-generated software" — software that may serve only one person, be used only once, and be discarded after use. For example, a script that checks daily whether a certain website has new items; or renaming thirty videos according to some rule. For these kinds of tasks, forcing them through a PRD → architecture → user stories process is using a sledgehammer on a thumbtack.

The more fundamental issue is that BMAD treats the agile process as a fixed template, rather than a set of principles to be adapted to local conditions. True agility's core is rapid response to change. But BMAD's design, to some extent, substitutes process certainty for judgment flexibility. This has value in certain scenarios, but you must be clear about its cost.

### 2.5 Composability and Exit Ramps

The best methodology is composable: it preserves exit ramps (when cost exceeds benefit, what do we stop doing). This means every part of the methodology should be optional and replaceable, not a tightly coupled whole. If you find that a certain step (e.g., detailed architecture documentation) does not help your project, you should be able to skip it directly, rather than being forced to follow the entire process.

The benefit of this design is that it allows you to adjust based on actual circumstances. You can start from a lightweight version and gradually add more structure as the project's complexity increases. When the project's complexity decreases, you can also simplify the process. This flexibility is key to surviving in a rapidly changing environment.

## 3. Application Criteria

### When to Use

Apply first-principles methodology design when evaluating popular AI development frameworks (e.g., agent role-playing workflows), choosing between research and engineering cadences, and standardizing team practices. Specific scenarios include:

- **Framework selection**: Before adopting frameworks like BMAD, LangGraph, or AutoGen, first ask: what are this framework's core assumptions? Do these assumptions match my problem? If they don't, should I change the problem to fit the framework, or should I reject the framework?
- **Process design**: When designing workflows for a team or project, don't directly copy industry best practices — start from your specific constraints. What is your main uncertainty? What are your failure modes? What kind of process can most effectively address these challenges?
- **Tool selection**: When choosing development tools, frameworks, or methodologies, evaluate whether they truly solve your core problems, rather than being swayed by marketing.

### How to Practice

**Step 1: Make Assumptions Explicit**

Write down the core assumptions of the framework or methodology. For example, BMAD's assumptions include:
- Software development requires explicit phase divisions
- Different roles should have different responsibilities and contexts
- Documentation is an important project deliverable
- Process certainty can improve quality

**Step 2: Map to Constraints**

Map each assumption to your specific constraints. Does your project truly need such phase divisions? Does your team truly need such role separation? Is your uncertainty low enough that process certainty can yield benefits?

**Step 3: Small-Scale Pilot**

Run a small-scale pilot with clear success metrics. Don't adopt fully from the start — test the methodology within a limited scope. The metrics to measure: does this methodology truly help us complete tasks faster? Does it reduce errors? Does it improve code quality?

**Step 4: Keep Templates, Discard Rituals**

If the pilot succeeds, keep the parts that are truly valuable (e.g., PRD templates, architecture document structures), but discard the pure rituals (e.g., daily standups, lengthy review processes). The value of a methodology lies in its artifacts and ways of thinking, not in its rituals.

**Step 5: Continuous Iteration**

Regularly review your methodology. Every three months, ask yourself: is this methodology still effective? Have new constraints or failure modes emerged? Does it need adjustment? A methodology is not static — it should evolve as your understanding of the problem evolves.

## 4. Pitfalls and Insights

### 4.1 The "Framework Worship" Trap

Many people say "we adopt BMAD" or "we use Scrum," as if choosing a framework solves all problems. But in reality, a framework is only a reference, not a bible. Tools become obsolete; understanding the essence of tools does not. What is worth learning from BMAD is its engineering-oriented thinking about agile processes, not framework worship. Treat it as a reference, not a mandatory specification.

### 4.2 The "One-Size-Fits-All" Trap

If the same methodology works for all projects, it means it has not truly understood the nature of the problem. A good methodology should be adjustable based on specific circumstances. If you find yourself forcing adaptation to a methodology, rather than the methodology adapting to your problem, it is time to re-evaluate.

### 4.3 The "Cost-Benefit Imbalance" Trap

Many teams invest enormous time and energy following a methodology but never ask whether this investment truly yields returns. When cost exceeds benefit, you should have the courage to abandon the methodology rather than persist. This is why "exit ramps" matter — they give you a graceful way to let go.

## 5. Related Axioms

- **A06. Framework Choice Is Worldview Lock-In** — The purpose of first-principles methodology design is to help you make conscious decisions when choosing frameworks, rather than passively accepting the framework author's worldview.
- **A07. Design Philosophy Determines Capability Ceiling** — Different methodologies embody different design philosophies. Understanding the differences among these philosophies helps you choose the methodology best suited to you.
- **T01. Infrastructure Over Components** — The value of a methodology lies in its infrastructure (document structure, context management, observability), not in its components (tools, frameworks, processes).
- **T02. Results Certainty** — The ultimate goal of first-principles methodology design is to ensure you can reliably achieve expected results.

## 6. Summary

The core idea of first-principles methodology design is simple: don't blindly adopt frameworks — start from your specific problem and design a methodology tailored to it. This process includes making assumptions explicit, mapping to constraints, small-scale piloting, keeping valuable parts, and continuous iteration.

In the AI era, this principle becomes even more important. Because AI's capability boundaries are still rapidly shifting, any framework's assumptions may quickly become obsolete. The wisest approach is to remain framework-neutral, start from first principles, use libraries rather than frameworks, and embrace the builder mindset. The cost of doing this is low (because the foundational system is simple), but the payoff is high (because you retain full flexibility and depth of understanding).

Finally, remember: methodology serves people, not the other way around. When methodology becomes a burden, it is time to re-evaluate.
