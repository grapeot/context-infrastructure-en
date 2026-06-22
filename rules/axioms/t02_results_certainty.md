---
id: axiom_results_certainty_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T02. Results Certainty Over Process Certainty

## 1. Core Axiom

Define what counts as `correct` first and verify it; do not try to make AI reliable by micromanaging every step.

## 2. Deep Reasoning

### 2.1 The Upper Bound of Process Certainty

Confidence in traditional programming comes from process certainty: every line of code is under your control, every branch, every edge case has been designed by you. This certainty is tangible, and it is the core capability we have trained over many years — translating outcomes into program behavior. But this model encounters a fundamental dilemma in AI systems.

When you try to constrain AI behavior through rules, you find yourself trapped in an infinite defensive programming loop. One rule fixes one problem but introduces new problems in other situations. You add more rules to handle edge cases, but edge cases are infinite. Eventually, you find yourself maintaining more rules than product logic. This is exactly the dilemma I encountered in a certain AI translation project: chunking, retries, glossaries, checkpoint resumption, Chinese character detection, timeout handling — each one was designed to prevent a specific failure mode. But these defensive rules themselves became the main source of system complexity, and they could never cover all cases.

The upper bound of process certainty is determined by how many edge cases you can think of. In AI systems, edge cases are infinite because AI behavior is fundamentally non-deterministic. You can never fully constrain it through rules.

### 2.2 The Results Certainty Loop

Results certainty represents a fundamentally different approach: instead of prescribing the process, define a clear target state and let the system find its own way there. The key to this approach is establishing a closed loop: execute → observe → verify → correct.

This loop only became truly possible when I handed translation tasks to Claude Code. Claude Code's basic unit of operation is the file, and files are stateful and persistent. This means the AI can see what it did before, can run verification scripts to check results, and can adjust based on feedback. This is not a one-shot API call — it is an iterative, self-correcting process.

Concretely, when I define the criteria for "translation complete" — correct formatting, no residual Chinese characters, consistent terminology — I can encode these criteria as executable checks. The AI must not only complete the translation but also run these checks, see the failure messages, and fix the problems itself. This process can repeat until all checks pass. The key shift: I no longer need to foresee all possible failure modes; I only need to define what success looks like.

This principle also has profound implications for cost structure. In traditional programming, code execution is nearly free but human labor is expensive, so we invest heavily in designing perfect logic. But in the AI era, inference costs are dropping rapidly. The cost of multiple attempts, checks, and corrections is often cheaper than writing defensive rules for every long-tail failure mode. This is a fundamental economic shift.

### 2.3 Making Acceptance Criteria Explicit

The prerequisite for results certainty is the ability to clearly define "done." This sounds simple but is actually the biggest bottleneck. Most failures are not because the AI is not smart enough, but because the AI does not know what "done" means.

I use an analogy to understand this: imagine assigning a task to an amnesiac intern. This intern has no background knowledge, does not know what you discussed before, does not know your implicit expectations. They can only see the instructions you give them this one time. If you want them to reliably complete the task, you must write the acceptance criteria with extreme clarity — clear enough that they can judge whether they have completed the task based on these criteria. If they think they haven't, they know what is missing.

This is exactly how Claude Code works. When I say "translate this file, then run this Python script to check for residual Chinese characters, and fix them if found," I am essentially turning implicit expectations into explicit, verifiable standards. This transformation itself is the biggest leverage.

### 2.4 Architecture Over Rules

When a system underperforms, our first reaction is often "the model isn't good enough" or "we need more rules." But in reality, many failures stem from poor architectural design. The Wide Research example is instructive: rather than demanding a single AI call to perfectly execute a complex task, break the task into multiple small steps, each with clear acceptance criteria. This is not model magic — it is management repair.

The same principle applies to translation. When API calls "slack off" on long texts, I once thought it was a model problem. But in reality, it was an architectural problem: long outputs degrade instruction-following capability. The solution is not to demand the model be "smarter" but to change the architecture — let the AI translate chapter by chapter, each chapter with clear input and output, each chapter independently verifiable. This way, the problem shifts from "how to make one API call perfectly execute" to "how to design a process where each small step is reliable."

## 3. Application Criteria

### When to Use

Results certainty applies to any task whose output is checkable. This includes:

- **Formatting tasks**: code generation, document conversion, data cleaning — these all have clear success criteria
- **Verification tasks**: checking whether specific conditions are met (no residual Chinese, tests pass, spec compliance)
- **When guardrail rules start outnumbering product logic**: this is a signal that you should shift to results certainty

### How to Practice

1. **Write acceptance criteria first**: Don't say "generate high-quality code." Say "code must pass all unit tests, coverage > 80%, no security warnings." Turn implicit expectations into explicit, measurable standards.

2. **Solidify criteria into executable checks wherever possible**: Python scripts, unit tests, linters, regex — anything that can be automatically verified should be automated. This way the AI can run checks itself, see failures, and fix them.

3. **Let the agent choose its own method and iterate**: Don't prescribe how the AI should do it, only define what success is. The AI might use regex, or NLP, or some other method. As long as the final result meets the criteria, it is reliable.

4. **Establish a feedback loop**: Ensure the AI can see verification results and adjust based on failure information. This closed loop is the core of results certainty.

## 4. Pitfalls and Boundaries

### When Not to Apply

- **Acceptance criteria cannot be defined**: If success is fundamentally subjective (e.g., "creative writing"), results certainty becomes difficult
- **Extremely tight real-time requirements**: If the verification process would cause unacceptable latency, you may need to accept higher risk
- **Cost-benefit mismatch**: If verification cost far exceeds failure cost, it may not be worth the investment

### Common Pitfalls

1. **Fake acceptance criteria**: Defining criteria that appear clear but are actually vague. For example, "good code quality" is not a criterion; "passes all tests and complexity < 10" is.

2. **Verification blindness**: The verification rules themselves are flawed, causing outputs that pass verification to still fail. Regularly review verification rules to ensure they are truly measuring what you care about.

3. **Over-verification**: Designing overly complex verification processes for low-risk tasks, causing efficiency loss. Verification should match the risk level.

4. **Trust drift**: Over time, gradually relaxing verification standards until the system becomes unreliable. Regular review and recalibration are needed.

## 5. Relationships with Other Axioms

- **A04 Reliability Is a Management Problem**: Results certainty is the core method of reliability management
- **V02 Verifiability Is the Foundation of Trust**: Results certainty depends on clear acceptance criteria and executable checks
- **T07 Isolation-Processing-Verification Loop**: Results certainty is the verification phase of this loop
- **T01 Infrastructure Over Components**: Results certainty requires a runtime that supports feedback loops (e.g., Claude Code)
