# Interview Evaluation Framework in the AI Era

Interview evaluation shifts from assessing Skill to assessing Trait, and identifies AI-assisted cheating.

## Core Principles

### Roles Are Defined by Trait, Not Skill

In the AI era, skills depreciate rapidly. Interviews should assess:
- Business sensitivity
- Problem-solving motivation
- Resilience under pressure
- Storytelling and persuasion

Rather than pure programming ability or framework proficiency.

### Senior Interview Strategy Shift

Abandon asking "what did you do" and dig into "why (Rationale)":
- Why choose this approach?
- What alternatives existed? Why were they rejected?
- What would you do differently if starting over?

Be wary of candidates who use Accuracy on imbalanced datasets.

## AI Cheating Detection

### Visual Characteristics

- Eyes fixed on a narrow area (screen)
- No filler words (normal speech has pauses and hesitation)
- Overly rigorous structure (typical AI output characteristic)

### Logical Characteristics

- Overly polished hallucination
- Can "fluently" answer about nonexistent content
- Cannot recognize non-standard word pronunciations (AI reads directly rather than recognizing)

### Probe Tactics

1. **Knowledge Cutoff fishing**: fabricate nonexistent models/frameworks/versions, observe candidate reaction
2. **Reverse follow-up**: ask for specific details of what was "just mentioned"
3. **Pronunciation trap**: use terms with non-standard pronunciation, observe whether they can correctly identify them

## Technical Depth Probing

### Auto Labeling Pipeline Background

For candidates with auto-labeling pipeline experience:
1. **Systematic recall bias identification**: does the training data have systematic bias?
2. **Evaluation blind spot detection**: do the evaluation metrics cover all failure modes?

### Edge vs Cloud Decision Framework

Decision based on three dimensions:
1. **Latency requirement**: real-time requirement high → Edge
2. **Criticality**: severe failure consequences → Edge + redundancy
3. **Technical feasibility**: model size vs device compute

In Magic Leap practice, ORB features outperformed cutting-edge approaches like Superglue — classical algorithms still have value in specific scenarios.
