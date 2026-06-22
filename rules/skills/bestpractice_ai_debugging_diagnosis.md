# AI-Assisted Debugging Diagnosis

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: When encountering "code won't fix" situations in AI-assisted development
- **Created**: 2026-02-21
- **Source**: Observation record from 2026-01-19

---

## Core Insight

**The vast majority of "AI can't fix the code" situations have root causes in human user issues, not system architecture issues.**

Common misconceptions:
- "The code is a mess, AI can't handle it" → actually insufficient context
- "AI isn't smart enough" → actually unclear instructions
- "Needs refactoring" → actually lacking success criteria

---

## Diagnosis Decision Tree

```
AI can't fix the code
    │
    ├─→ Was sufficient context provided?
    │       │
    │       └─→ No → Supplement context (related files, error logs, expected behavior)
    │       │
    │       └─→ Yes → Continue
    │
    ├─→ Were clear success criteria defined?
    │       │
    │       └─→ No → Define "what good looks like" (not just "it runs")
    │       │
    │       └─→ Yes → Continue
    │
    ├─→ Was a feedback channel provided?
    │       │
    │       └─→ No → Let AI see results (test output, screenshots, logs)
    │       │
    │       └─→ Yes → Continue
    │
    └─→ Possibly a genuine architecture problem
            │
            └─→ Consider local refactoring or problem decomposition
```

---

## Common Problems and Solutions

### 1. Insufficient Context

Symptoms:
- AI's proposed solutions deviate from actual needs
- Repeatedly modifying the same piece of code
- Introducing nonexistent dependencies or functions

Solution:
- Provide related files (not just the one reporting the error)
- Provide a project structure overview
- Provide similar correct implementations as reference

### 2. Fuzzy Success Criteria

Symptoms:
- AI asks "is this okay," human says "tweak it more"
- Still unsatisfied after multiple rounds of modification, but can't articulate the specific issue

Solution:
- Define quantitative metrics (performance, coverage, error types)
- Provide expected output examples
- Decompose into smaller verifiable steps

### 3. Missing Feedback Channel

Symptoms:
- AI doesn't know the effect after modification
- Human needs to manually test to discover issues

Solution:
- Provide test commands and expected output
- Let AI execute and view results
- Provide screenshots when offering UI

---

## When It's Actually an Architecture Problem

Signals that genuinely require refactoring:
- The same problem appears repeatedly in different places
- Still unsolvable after supplementing context
- Multiple solutions from AI all have obvious flaws
- The problem spans multiple module boundaries

Even then, try first:
- Local refactoring rather than large-scale rewrite
- Increase test coverage
- Improve documentation and comments

---

## Relationship with Other Skills

- Works with `bestpractice_ai_programming_mindset.md`'s "70% problem" diagnosis
- Works with `bestpractice_staged_approach.md`'s verification mechanism
- Works with the Todo task management mechanism in the system prompt for task decomposition

## Changelog

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from 2026-01-19 observation record |
