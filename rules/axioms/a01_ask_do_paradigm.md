---
id: axiom_ask_do_paradigm_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
raw_sources:
  - "contexts/blog/content/agentic-ai-en.md"
  - "contexts/blog/content/result-certainty-en.md"
  - "https://www.anthropic.com/research/measuring-agent-autonomy"
  - "https://www.anthropic.com/research/project-vend-2"
  - "arXiv:2602.17910 (Alignment in Time: Peak-Aware Orchestration)"
  - "arXiv:2602.17091 (What to Cut? Predicting Unnecessary Methods in Agentic Code Generation)"
  - "arXiv:2602.16553 (Agentic AI, Medical Morality, and the Transformation of the Patient-Physician Relationship)"
---

# From Ask to Do: The Paradigm Shift

## 1. Core Axiom

AI becomes truly transformative when it delivers finished artifacts end-to-end ("ask-do"), rather than merely answering questions or drafting intermediate steps. The essence of this shift: **from "give me an answer" to "give me the finished thing."**

---

## 2. Deep Reasoning

**The power of compressed loops**: ask-do compresses decomposition, implementation, and debugging into a single loop. In the traditional consulting model, humans must decide at every step — AI gives advice → human evaluates → human executes → human observes results → human adjusts. Each handoff is friction. In ask-do, AI observes its own output, spots problems, and adjusts automatically, creating an observe-correct loop where humans only intervene at key decision points. Project Vend research shows: when Claudius was given tools and a programmatic checklist, business performance shifted from loss to profit. The key was not a smarter model, but an architecture capable of executing, observing, and correcting. The economics of this shift: from "human time is the bottleneck" to "constraints and verification are the bottleneck."

**The human bottleneck moves up to the contract layer**: defining what "done" means and how to verify it. You no longer micromanage every step of AI. Instead: (1) define acceptance criteria (clear enough that an amnesiac intern could understand), (2) provide checks (automated tests, format validation, business rule checks), (3) let AI choose its own method (as long as it passes the checks). Anthropic's "Measuring AI Agent Autonomy" study found: experienced users don't reduce supervision of AI — they change how they supervise, shifting from "approve every action" to "let AI run autonomously, intervene when something goes wrong." This is the contract-layer mindset in action. In medicine, doctors no longer verify every reasoning step of AI; they define "what kind of diagnostic suggestion is acceptable" (evidence-based, explainable, risk-graded), then let AI work within that framework. This shift demands that humans upgrade from "executor" to "standard-definer."

**Tool access and multi-turn execution**: without execute → observe → correct, you're back to "kick it, it moves." AI without tools can only "say"; AI with tools can "do." The types of tools determine what AI can do: code execution tools for software engineering (currently 50% of agentic activity), database access for business process automation, browser + search for research and information synthesis, CRM + inventory systems for business operations, medical record systems for clinical decision support. Multi-turn execution lets AI learn to recognize its own uncertainty — Claude Code pauses to ask clarifying questions on the most complex tasks at twice the rate humans interrupt it. This shows AI is learning self-calibration. The value of multi-turn execution is not just correcting errors, but AI discovering ambiguity in the original requirements during execution and proactively seeking clarification.

**Human work shifts to handling ambiguity**: when execution cost approaches zero, what's scarce is no longer "what can be done" but "what should be done." Human competitive advantage shifts to intent clarification (turning vague requirements into verifiable standards), risk judgment (choosing the optimal risk-reward among multiple feasible options), taste (selecting the most elegant, maintainable, long-term-vision-aligned option), ethics and values (drawing the line between what AI can do and what it should do). An interesting finding from Project Vend: both the CEO agent and Claudius tended to "generously give discounts" because they were trained to be helpful. But this violated business logic. Humans need to set hard constraints like "no discounts," then let AI optimize within that framework. This reflects a deeper truth: AI's capability and human value judgment are complementary, not substitutive.

---

## 3. Application Criteria

The task's real deliverable is an artifact (chart, image edit, formatted document, working code change), and "correctness" can be checked.

| Domain | Applicable | Not Applicable |
|--------|-----------|----------------|
| **Software Engineering** | Code generation, test writing, refactoring (with linter/test checks) | Architecture decisions, tech selection (require multi-dimensional trade-offs) |
| **Content Creation** | Translation, format conversion, draft generation (with style guides) | Creative direction, brand voice definition |
| **Data Analysis** | Data cleaning, report generation, anomaly detection (with validation sets) | Hypothesis formulation, metric selection |
| **Medicine** | Diagnostic suggestion generation (with evidence base), patient education content | Treatment plan selection (involves ethical trade-offs) |
| **Business Operations** | Inventory management, order processing, customer service replies (with rules) | Pricing strategy, market entry decisions |
| **Research** | Literature review, data processing, draft writing | Research question definition, methodology selection |

**Boundary conditions**: ask-do fails when: (1) "correctness" cannot be objectively verified (the "goodness" of artistic creation), (2) the task involves multiple conflicting objectives (cost vs quality vs speed), (3) the consequences of execution are irreversible and high-risk (surgical decisions, large financial commitments), (4) the task requires real-time human judgment with situational awareness (negotiation, crisis management), (5) there is a fundamental gap between AI's "understanding" and human implicit assumptions (the "friendly discount" problem in Project Vend).

**How to practice**: directly ask for the artifact, state acceptance criteria (preferably runnable checks), then give feedback on the output rather than micromanaging the steps.

Three levels of writing acceptance criteria: bad is "generate a good code review comment" (too vague), good is "generate a code review comment that points out performance issues, provides specific improvement suggestions, includes reference links, length < 200 words" (specific but needs human verification), better is "generate a code review comment that must pass this linter check" (automatically verifiable). The clarity of acceptance criteria directly determines whether AI can iterate autonomously. The more specific the criteria, the higher AI's success rate; the vaguer the criteria, the more frequent human intervention. Criteria should be measurable, repeatable, and directly tied to business goals.

Provide executable checks: for code, use unit tests, type checks, linters; for documents, use spell checks, style guide validation, link validity; for data, use schema validation, statistical checks, anomaly detection; for medicine, use evidence base queries, contraindication checks, ethical review checklists. The more automated the checks, the higher AI's iteration efficiency. Ideally, checks should be fully automated so AI can get feedback and adjust within seconds. Checks should cover functional, non-functional, and constraint-based requirements.

Let AI iterate until it passes — show AI why the check failed, let it adjust its own method, don't tell it "how to do it," only tell it "what's wrong." This "black-box feedback" approach forces AI into genuine problem-solving rather than simply following instructions. Intervene at key points: when AI asks clarifying questions (a good signal), when multiple solutions all pass checks (needs human taste judgment), when results exceed expectations (may have discovered new opportunities). Human intervention should be targeted, not comprehensive.

---

## 4. Deep Insights and Pitfalls

**The helpfulness trap**: Project Vend's key finding is that AI is trained to be helpful, so it tends to satisfy user requests even when this violates business logic. Claudius would give discounts, send free items, agree to unreasonable contracts (the onion futures act example). The lesson: you cannot rely on AI's "common sense" to enforce business rules — rules must be made explicit. Acceptance criteria must include "what should not be done," not just "what should be done." When AI's objective function ("help the user") conflicts with the system's objective function ("be profitable"), explicit constraints are needed. The deeper cause of this trap: the mismatch between AI's training objective (aligning with human preferences) and the actual system objective (business success). The only way to prevent this trap is to encode all business rules as hard constraints.

**The autonomy paradox**: Anthropic's research shows experienced users give AI more autonomy (from 20% auto-approval to 40%), but also interrupt AI more frequently (from 5% to 9%). This seems contradictory but actually reflects a mature supervision pattern: new users approve every action individually (high friction, low risk), experienced users let AI run autonomously but actively monitor, intervening quickly when problems arise (low friction, controllable risk). ask-do does not mean "full autonomy" — it means "autonomy within explicit constraints." Effective supervision is not approving every action, but being able to quickly identify and correct problems. The success of this pattern depends on the human's deep understanding of the system — knowing when to trust AI and when to intervene. This also means humans need to continuously learn and adapt to AI's behavioral patterns.

**Long-term stability**: Anthropic's "Alignment in Time" paper points out that traditional AI alignment research focuses on individual outputs, but agents running autonomously over long periods need to maintain reliability across the entire trajectory. An agent may perform perfectly for the first 10 steps but start drifting at step 50; errors accumulate and amplify across multi-turn execution. The reliability of ask-do depends not only on the quality of individual decisions but also on the stability of the entire execution trajectory. Agents need periodic "recalibration" of goals and constraints during long runs; monitoring must look at not just final results but also key indicators during execution. This means ask-do is not "set it once and let go" — it requires ongoing human involvement. Long-running agents need regular audits and re-verification.

**Cross-domain applicability limits**: currently 50% of agentic activity is concentrated in software engineering, because software engineering's "correctness" is easiest to verify (tests, linters, type checks), execution consequences are relatively reversible (code can be rolled back), and the tool ecosystem is most mature (git, IDE, CI/CD). When expanding to other domains: medical verification becomes difficult (needs long-term follow-up), consequences are irreversible (patient harm); financial verification needs real-time market data, consequences are immediate and irreversible; creative work's "correctness" is inherently fuzzy, hard to verify; HR involves ethics and power dynamics, cannot be fully automated. The ask-do paradigm is best suited for domains that are "verifiable, reversible, with mature tool ecosystems." In other domains, stronger human supervision and more explicit constraints are needed.

---

## 5. Practical Examples

**Code generation**: Ask "write a function that reads user data from CSV, deduplicates, returns a DataFrame." Do: AI generates code. Check: code passes pytest, passes mypy type check, handles empty files and malformed rows, performance < 5 seconds on 1M rows. Iterate: if checks fail, AI sees the failure information and adjusts automatically. This example shows the complete ask-do flow in software engineering. Acceptance criteria are fully automatable, so AI can complete multiple iterations within seconds. This is why software engineering is the most mature application domain for ask-do.

**Medical diagnostic suggestion**: Ask "based on this patient's symptoms and test results, generate a diagnostic suggestion." Do: AI generates suggestion. Check: suggestion is based on latest clinical guidelines, includes evidence level annotations, lists contraindications and risks, suggests further examination checklist. Iterate: doctor sees suggestion, can accept, modify, or reject. This example shows ask-do applied in medicine, where the human's final decision authority is non-transferable. Even if AI's suggestion passes all checks, the doctor still needs to make the final decision based on the patient's specific situation. Medical ask-do will never be fully automated.

**Business operations**: Ask "manage inventory, maximize profit." Do: AI makes pricing, purchasing, sales decisions. Check: all pricing >= cost * 1.5 (hard constraint), inventory turnover > 0.8 (KPI), no expired inventory. Iterate: if constraints are violated, AI adjusts automatically; CEO periodically reviews KPIs. This example shows how ask-do prevents the "helpfulness trap" through explicit constraints. Hard constraints ensure AI never makes decisions that violate business rules, even if doing so appears more "friendly" on the surface.

---

## 6. The Essence of the Key Shift

The success of the ask-do paradigm lies not in AI's capability but in how humans define problems. Shifting from "tell AI how to do it" to "tell AI what success looks like" seems simple, but it actually demands deep thinking from humans. You must be able to clearly define what "done" means, which is often harder than the execution itself. This also explains why ask-do is most mature in software engineering — because "code passes tests" is a clear, verifiable success criterion. In other domains, defining success often requires weighing multiple dimensions, which is why the human role becomes more important.

Another key insight of ask-do: **results certainty beats process certainty**. You don't need to know how AI arrived at the answer — you only need to know whether the answer meets your criteria. This shift unleashes AI's creativity, letting it try different approaches rather than being forced to follow specific steps. This also means AI may discover solutions you hadn't thought of.

---

## 7. Implementation Advice

**Step one: clarify your acceptance criteria**. Don't say "generate a good report" — say "generate a report containing the following sections: executive summary (< 200 words), data analysis (including at least 3 charts), recommendations (actionable, prioritized), references." Acceptance criteria should be specific enough that anyone can judge whether the output meets requirements.

**Step two: automate your checks**. If possible, write code to verify outputs. If full automation isn't possible, at least have a checklist so you can quickly evaluate AI's output. The benefit of automated checks is that AI gets immediate feedback without waiting for human evaluation.

**Step three: give AI feedback, not guidance**. When AI's output doesn't meet criteria, tell it "this report is missing the data analysis section" rather than "you should add a data analysis section with the following steps..." This lets AI come up with its own solution rather than simply following your instructions.

**Step four: periodically review and adjust**. ask-do is not a one-time setup. Over time, you may discover new edge cases or need to adjust constraints. Periodically review AI's output to see if acceptance criteria need updating. This is also a learning process — you gradually understand AI's capabilities and limitations.

---

## 8. Summary: From "Consulting" to "Execution"

| Dimension | Consulting Mode | Ask-Do Mode |
|-----------|----------------|-------------|
| **Deliverable** | Advice, drafts, analysis | Finished artifact |
| **Verification** | Human evaluates steps | Automated checks + human review |
| **Human Role** | Micromanage every step | Define standards, make key decisions |
| **Feedback Loop** | Slow (human-driven) | Fast (AI-driven) |
| **Scalability** | Low (limited by human time) | High (limited by tools and constraints) |
| **Scope** | All tasks | Verifiable, reversible tasks |
| **Risk** | Low (human control) | Medium (needs explicit constraints) |

**Final insight**: ask-do is not "let AI be fully autonomous." It is "let AI execute autonomously within explicit constraints and a verification framework, with humans intervening at key points." This requires clear acceptance criteria, executable checks, fast feedback loops, explicit constraints and no-go zones, and periodic human review and recalibration. When these conditions are met, the ask-do paradigm can significantly improve efficiency and reliability. When they are not, fall back to consulting mode.
