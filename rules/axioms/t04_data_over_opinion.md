---
id: axiom_data_over_opinion_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T04. Data Over Opinion in Decision-Making

## 1. Core Axiom

When measurement is available, use data and instrumentation to support decisions, not opinions and narratives. Data is direct observation of reality; opinion is indirect inference about reality. The former can be verified and reproduced; the latter is easily distorted by bias and memory.

## 2. Deep Reasoning

### Signal Quality Determines Feedback Loop Tightness

In my own weight management project, the weight signal was noisy and high-latency, actually rewarding gut-feel decisions. Weight is affected by multiple factors — hydration, digestion, hormonal cycles — so a single measurement carries extremely low information; even looking at weekly averages, you have to wait seven days for one data point, meaning you cannot quickly correlate "what I did" with "what the result was." In this high-latency, low signal-to-noise environment, the human brain automatically fills in the gaps, explaining outcomes with stories rather than evidence. After switching to a more responsive proxy signal (blood glucose level, one data point every five minutes), causal relationships became clear: how blood sugar reacts after eating a certain food, how it drops after exercise. This tight feedback loop not only improved decision accuracy but also dramatically increased iteration speed and motivation — because the reward cycle compressed from seven days to five minutes. This pattern applies in product development, QA inspection, and personal habit optimization: choosing a fast-responding, highly correlated metric often drives behavior change more effectively than choosing the "ultimate goal" metric.

### Data Turns Arguments into Experiments

In Labelbox's re-labeling inspection, manual sampling was fast but low-resolution, with results dependent on luck. Two people could look at the same 100 samples and reach completely opposite conclusions — "labeling quality is great" vs. "labeling quality is terrible" — because their respective samples might happen to represent different distributions. After building a quick diff/visualization tool, decisions became full-coverage and reproducible: you could see every labeling error, rather than guessing. This transforms "I think" arguments into "the data shows" facts. In team decision-making, the value of this transformation is enormous: the most persuasive person no longer wins — reality speaks instead. Data does not change because of your seniority, nor does it distort because of your eloquent reasoning.

### Funnel Analysis Forces Prioritization

Funnel analysis is effective because it forces you to locate the largest drop-off point before investing effort, avoiding blind micro-optimization. If your conversion funnel loses 80% of users at step two, then optimizing the user experience at step five is a waste of time — even if step five optimization is technically more interesting. Data forces you to face reality: invest where the bottleneck is. This is closely related to M3 (Quantify Priorities), but goes further: not only quantify priorities, but use actual drop-off data to validate your hypotheses. Many teams say "we should improve X," but when you pull out funnel data, the real bottleneck is often completely different.

### Low-Latency Metrics Improve Iteration Speed and Psychological Motivation

High-latency feedback not only reduces accuracy but also destroys team motivation. If you make an improvement and have to wait a month to see results, you will spend that month constantly doubting your decision. But if you have a low-latency proxy metric (e.g., user click-through rate, API response time, labeling error rate), you can see feedback within hours and adjust immediately. This rapid iteration capability not only helps you find the optimal solution faster but also gives the team real-time feedback that "we are making progress," sustaining motivation. Psychologically, tight reward loops drive behavior change more effectively than distant large rewards.

## 3. Application Criteria

### When to Use

- **Product conversion decisions**: Use funnel analysis to locate the largest drop-off point, rather than guessing user pain points by intuition.
- **QA/labeling inspection**: Use full-coverage diff or visualization tools, rather than manual sampling.
- **Debugging**: Use logs, metrics, reproducible tests, rather than "I tried it, seems fine."
- **Personal habit optimization**: Choose low-latency proxy metrics (blood glucose, step count, focus time), rather than ultimate goal metrics (weight, health, sense of achievement).
- **Bottleneck identification in multi-step processes**: Any system with multiple stages where you are unsure where the bottleneck lies — measure first, then optimize.

### How to Practice

1. **Choose a metric**: Find one that is fast-responding, highly correlated, and easy to measure. It does not have to be the ultimate goal, but it must be correlated with the ultimate goal.
2. **Build observation tools**: Create the smallest possible dashboard, diff tool, or visualization that makes the data clear at a glance.
3. **Measure regularly**: Establish a regular measurement cadence (daily, weekly, per iteration), rather than sporadic spot checks.
4. **Decompose with funnels**: For multi-step processes, draw the funnel and find the largest drop-off point.
5. **Experiment and iterate**: Form hypotheses based on data, design controlled experiments (see X2), observe results, repeat.

## 4. Pitfalls and Counterexamples

### Pitfall 1: Optimizing the Wrong Metric

Choosing a metric that is easy to measure but unrelated to the real goal leads to "data-driven wrong decisions." For example, optimizing page load time while ignoring user retention, or optimizing labeling speed while ignoring labeling accuracy. Data itself is neutral, but metric choice reflects your values. Ensure your metric is correlated with the ultimate goal, even if it is not the ultimate goal itself.

### Pitfall 2: Over-Reliance on Short-Term Metrics

Low-latency metrics are useful, but if you completely ignore long-term metrics, you may fall into local optima. For example, to boost daily active users, you might make decisions that harm long-term retention. Track metrics at multiple time scales simultaneously, not just the fastest-feedback one.

### Pitfall 3: False Precision from Insufficient Data

When sample size is too small or measurement methods are biased, data gives a false sense of precision. For example, drawing conclusions from only 10 samples, or using biased sampling methods. In such cases, admitting uncertainty is more honest than pretending to have data support.

### Pitfall 4: Ignoring the Cost Behind Data

Sometimes, obtaining perfect data is too expensive. For example, to get full-coverage labeling inspection, you might need to build a complex tool. In such cases, weigh data quality against acquisition cost, rather than blindly pursuing perfection.

## 5. Relationships with Other Axioms

- **M3 (Quantify Priorities)**: Data is the foundation of quantification. Without data, priority ranking becomes gut-feel guessing.
- **X2 (Systematic Debugging)**: Debugging is experimental design, and experimental results are data. Data drives every step of debugging.
- **V2 (Verifiability)**: Data is the core of verifiability. What cannot be measured cannot be verified; what cannot be verified cannot be trusted.
- **T02 (Results Certainty)**: Data is the source of certainty. Opinions may be vague, but data is clear.
- **T03 (Context Isolation)**: Measuring data in isolated contexts can exclude confounding factors and improve signal quality.

---

**Final thought**: Data does not lie, but data can be misread. The key is choosing the right metric, measuring with the right method, and observing at the right time scale. When you do this, data becomes your most reliable advisor — it cannot be distorted by emotion, bias, or power dynamics.
