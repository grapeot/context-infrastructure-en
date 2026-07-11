# Internal Document Layout and Adaptive Visual Components Guide

## Metadata

- **Type**: BestPractice
- **Use cases**: Visualization and layout for internal documents such as memos, RFCs, and weekly reports written for the user, internal collaborators, or future AI agents.
- **Created**: 2026-07-06

## Core Design Philosophy

The fundamental goal of internal visualization is to **let form carry value independently, reduce the time readers spend reading text, and accelerate decisions and audits.**
Visuals are tools for increasing cognitive bandwidth, not decoration.

---

## 1. Visual Component Toolkit

Choose the visual component that addresses the specific cognitive problem. Do not add visuals merely for the sake of visualization:

| Visual component | Cognitive problem it solves | Use case |
| :--- | :--- | :--- |
| **Short paragraphs** | The default form for detailed argument and logical reasoning. | Almost all detailed explanations. |
| **Compact tables** | Comparison across stable dimensions, using spatial memory. | At least four items with a consistent data structure. |
| **Card grids** | Status and takeaways for a few parallel items, with color blocks supporting quick judgment. | Four to six items or fewer, with an even distribution of color states. |
| **Chip / pill** | Marks the type or status of one item, creating a parallel scanning channel. | At least two categories in the same column, with color semantics explained in place. |
| **`<details>` disclosure** | Audit material, long logs, implementation details, and discarded historical approaches. | Content the reader may want to verify but does not need for the first-screen decision. |
| **Anchor links** | Creates in-place navigation from a claim to its evidence. | Any core conclusion that needs support from a source file or code. |

---

## 2. Local HTML-in-Markdown Enhancement and Adaptation

Markdown may use HTML/CSS for cards, side-by-side comparisons, and status bars, but these components must adapt to mobile displays and both dark and light modes.

### Constraint 1: Local Enhancement and Explicit Closing Tags
*   Never wrap the entire document in one outer `<div>`. Style only individual cards or components.
*   Explicitly close every HTML tag, such as `</div>`. Leaked tags can shift the layout and colors of the entire document.

### Constraint 2: CSS Colors Must Use Theme Variables with Fallbacks
To prevent white-background/black-text or dark-background/dark-text failures in Dark Mode, use `var(--theme-variable, fallback)`.
*   **Common variables and fallback values**:
    *   Body text: `var(--fg, #1a1a1a)`
    *   Background: `var(--bg, #ffffff)`
    *   Muted text: `var(--fg-muted, #666666)`
    *   Card background: `var(--card-bg, #f6f6f6)`
    *   Border: `var(--border, #e5e5e5)`
    *   Semantic state colors (green/accepted): `--ok-border` (`#10b981`), `--ok-bg` (`#d1fae5`), `--ok-fg` (`#065f46`)
    *   Semantic state colors (red/rejected): `--bad-border` (`#ef4444`), `--bad-bg` (`#fee2e2`), `--bad-fg` (`#991b1b`)
*   **Example**:
    ```html
    <div style="border-left: 5px solid var(--ok-border, #10b981); background: var(--card-bg, #f6f6f6); color: var(--fg, #1a1a1a); padding: 10px;">
      <strong>Business conclusion</strong>: Approach A works.
    </div>
    ```

### Constraint 3: Semantic Classes Must Use Compound Selectors
When applying CSS classes to decorative inline elements such as chips, badges, or pills, bind two classes, such as `.vx-chip.ok` or `.chip.ok`, instead of using a bare single class such as `.ok`. The higher specificity prevents a parent container's `--fg` from overriding the semantic color.
*   *Correct*: `class="vx-chip ok"`
*   *Incorrect*: `class="ok"`

---

## 3. Common Visualization Anti-Patterns

Before designing or producing an internal document, check for these failure modes:

1.  **Writing cards like encyclopedia entries**: Do not put more than 150 words of long prose in a card. A card should contain only a chip, a heading, and one or two judgment sentences. Move long paragraphs into the Markdown body below the card.
2.  **Hard-coded light backgrounds**: Values such as `background: white` or `background: #f8fafc` create a glaring white block in Dark Mode and can make white text on the background invisible.
3.  **Walls of information**: Do not place more than five data metrics in one paragraph. Split them into a short key-value list or a small two-column table.
4.  **Inline SVG images**: Do not include inline SVG code in final Markdown. Mobile rendering is highly inconsistent. Render the visual as PNG/JPG and reference it instead.
