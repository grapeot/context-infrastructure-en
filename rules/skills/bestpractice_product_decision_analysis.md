# Product/Technical Decision Reverse Engineering

When facing a new product, new feature, or competitor move, systematically deconstruct its design decisions, target users, problems being solved, and trade-offs. Avoid staying at the feature-description level; penetrate to the cost structure and strategic intent.

## When to Use

Trigger in the following scenarios:
- "Analyze this new feature/product"
- "Company X released Y, what do you think"
- "What is this thing actually doing"
- Any scenario requiring deep evaluation of an external product/technology
- The analysis phase of a research report (after fact collection is complete)

## Five-Step Deconstruction Framework

### Step 1: Reconstruct the Design Space

Before analyzing "what it chose," first ask "what it could have chosen."

- List the key decision points facing this product (typically 2-4)
- For each decision point, list the available paths
- No need to be exhaustive; focus on paths with substantive differences

**Example** (Claude Interactive Visualizations):
- Output modality: image generation vs code generation vs preset templates
- Lifecycle: temporary vs persistent
- Display method: inline vs sidebar vs new window
- Target user: developers vs all users

### Step 2: Identify the Choices

Which path it chose at each decision point. This step is factual description, not judgment.

### Step 3: Reverse-Engineer the Constraints

Why this path? Each choice is typically driven by one or more constraints:

- **Capability constraint**: what is the team/model's strength? (Anthropic strong at programming → chose code generation)
- **Market constraint**: which position is already occupied by competitors? (Google/OpenAI own image generation → differentiate)
- **User constraint**: what is the target audience's capability boundary? (non-developers can't use Cursor → need zero barrier)
- **Technical constraint**: what is the feasibility boundary of current technology? (browser-side rendering → can't handle large datasets)
- **Business constraint**: monetization model, user growth needs? (open to all → expand user base)

**Key question**: are there conflicts between constraints? If so, which constraint won? This often reveals the true strategic priority.

### Step 4: Expose the Trade-offs

Every choice has a cost. Ask two questions:

1. **What did this choice give up?** Not hypothetical "what might have been given up," but concrete, identifiable features/attributes/user groups.
2. **Who cares about what was given up?** This determines the product's true positioning — who it serves, who it doesn't.

**Reversal test**: if it had made the opposite choice, who would benefit and who would lose? This thought experiment quickly exposes the core of the trade-off.

### Step 5: Position in the Cost Structure

This is the most critical step, and the most easily skipped.

- **Which cost link did this product change?** What did it turn from "expensive" to "cheap"?
- **Who gained a capability they didn't have before?** Who are the new beneficiaries?
- **Did this capability already exist?** If it already existed (just with a higher barrier), then this is not a new capability but cost compression.
- **What is the price of compression?** Lowering the barrier typically comes with loss of control/verifiability/composability.

**Core judgment**: is it creating new possibilities (0→1), or lowering the barrier to an existing capability (expert→mass)? These two have completely different strategic implications.

## Interface with the Axiom System

This framework is a method for using the axiom toolkit. Different steps naturally connect to different axioms:

| Step | Common Axioms | Trigger Condition |
|------|--------------|-------------------|
| Step 1: Reconstruct design space | A06 (framework choice locks worldview) | When decisions involve framework/platform choices |
| Step 3: Reverse-engineer constraints | A07 (design philosophy determines ceiling) | When choices reflect deep design philosophy |
| Step 4: Expose trade-offs | X03 (efficiency determined by bottleneck) | When a choice removes one bottleneck but exposes a new one |
| Step 4: Expose trade-offs | A09 (builder mindset is the moat) | When trade-offs involve Builder vs Consumer divide |
| Step 5: Cost structure positioning | T05 (cognition is asset, code is consumable) | When the product changes the cost of "building tools" or "acquiring cognition" |
| Step 5: Cost structure positioning | A13 (three stages of technology adoption) | When needing to judge which stage a feature is at: Driver/Co-pilot/Architect |

## Output Format

The analysis report should contain:

1. **Fact layer** (Steps 1-2): technical implementation, product positioning, known limitations, competitive landscape. Pure facts, no judgment mixed in.
2. **Analysis layer** (Steps 3-5): design constraints, trade-offs, cost structure positioning. This is the core value of the report.
3. **Judgment layer**: conclusions based on the analysis. Provide separate judgments for different roles (Builder / Consumer / Competitor).

## Common Pitfalls

### Feature Description Trap
Staying at the level of "what it can do," without asking "why it does it this way" and "what it gave up." This kind of analysis is useless for decision-making.

### Isolated Evaluation Trap
Evaluating a new feature in isolation from competitors and existing capabilities. Must ask "did this capability already exist" — if the answer is "Cursor could already do this," the analysis focus should shift from "new capability" to "cost compression."

### Official Narrative Trap
Organizing analysis using the official messaging from the product launch. Official narrative is a marketing perspective, not an analytical one. Use your own framework to reorganize the facts.

## Source

Distilled from the Claude Interactive Visualizations research process (2026-03-16). The key turning point was asking "Isn't this just what Cursor could already do," which elevated the analysis from the feature-description level to the cost-structure level.
