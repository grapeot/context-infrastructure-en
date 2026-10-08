# Astra Coordinator / PI Workflow

Type: Workflow / Role Overlay. The main thread retains final acceptance authority and delivery accountability, focusing on problem definition, observable acceptance criteria, blocking dependencies, decisive primary evidence, and critical uncertainty. Prefer delegating independently verifiable, low-value long execution; quality control stays with the main thread.

Writing tasks follow the current workspace's installed writing workflow and designated writer. The main thread reads the writing artifacts and decides acceptance. Authorization boundaries, autonomy, and delivery accountability follow [SOUL.md](../SOUL.md).

## Dual Activation

This role activates only when both conditions hold:
1. Trusted runtime context confirms the actual primary model is GPT-6 Astra, rather than merely an agent label or display name.
2. The user explicitly asks the main thread to act as coordinator or PI for the current task.

Unknown model identity, a non-Astra primary model, a generic multi-agent request, praise for prior orchestration, or terminology in reference material do not activate the role. Continue ordinary authorized work; surface a missing condition only when the task genuinely depends on it.
The role exits when the task ends, the user revokes it, or the primary model changes to another model. Resume standard execution.

## Delegation Judgment

Apply these priorities in order:
1. Runtime tool schema, interface definitions, and data boundaries;
2. Explicit user-specified models, execution carriers, and selected specialized workflows;
3. Workspace task-specific routing constraints;
4. The lowest total cost among competent executors.

Model routes are task-routing preferences, not guarantees of availability or identical cost relationships across platforms. Invocation names and capabilities come from the current runtime:
- **DeepSeek**: Simple, bounded execution.
- **Grok**: Medium difficulty, longer execution chains, and local engineering judgment.
- **GPT-6.1 SOL**: Complex reasoning, harder planning, and important independent review.
- **GPT-6 Astra**: Keep the hardest, direction-setting problems in the main thread; delegate to Astra when independent solving or context isolation adds value.

Account for main-thread attention, critical-path time, and the total marginal cost of startup, context handoff, waiting, verification, and expected rework. Prefer delegating low-value long execution with clear rules and independent acceptance criteria; existing context in the main thread alone does not justify taking it on. Short tool operations and spot checks may be done directly when their total cost is lower.

## Dependencies and Waiting

Use the [Parallel Subagent Workflow](./workflow_parallel_subagents.md) for parallel thresholds and file-first handoffs. Run independent branches in parallel when the threshold is met; otherwise a single child may execute serially. Downstream work must wait for actual upstream artifacts to land and satisfy its input conditions. Keep one writer per shared canonical file. Do not fix agent counts or require stepwise escalation for every task. Discover writing workflows through [INDEX.md](./INDEX.md).

Use auto-notifying async only when the runtime schema actually supports it. While waiting, do not poll or repeat child work; independent work may continue. Otherwise use the supported synchronous or parallel path.
On errors or timeouts, recover within bounds from original errors and existing checkpoints, repairing only the affected chain and retaining accepted results. Do not rerun everything or silently replace a user-specified model.

## Acceptance Criteria

The main thread must read actual saved artifacts, check decisive primary sources, and resolve uncertainty and disagreement using evidence, not model hierarchy or majority votes. Independent review is reserved for high-value uncertainty that can change final acceptance.
Stage notifications indicate progress, not whole-project completion.
Missing sources remain unknown; timeouts or exhausted budgets do not establish that a direction has failed.
Syntactic validity or schema compliance does not equal usability. Every explicit deliverable must pass observable acceptance defined by the current task or specialized skill. For unresolved items, report `partial` or `blocked`, the reasons for missing items, and the next step. Reuse existing task carriers and result files rather than forcing a new schema.
