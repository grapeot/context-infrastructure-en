# Internal Writing Workflow

## Metadata

- **Type**: Workflow
- **Use cases**: Readers with shared context: the user, internal collaborators, AI agents, and project workflows. Covers research memos, decision briefs, work logs, and execution summaries.
- **Created**: 2026-06-11
- **Last updated**: 2026-07-06

---

## 1. When to Use It

Load this workflow when the audience shares context and the goal is to help them form a judgment, verify evidence, and decide the next step quickly.
*   For strangers without shared context, public channels, customers, or external course audiences, use `workflow_external_writing.md`.

AI has made the marginal cost of internal documents extremely low, but reader attention remains the bottleneck. The goal of form and layout is therefore to **reduce decision friction and give the reader the most actionable judgment in the same amount of time.**

---

## 2. Information Order and Structure (Bottom Line Up Front)

Put the most important decisions and recommendations first. Do not list work chronologically or begin with extensive background.
The first screen must let the reader decide within 15 seconds whether to continue and, if so, which section matters most.

### 1. Restore Minimum Context
The reader may be switching between tasks and may not have the current context in mind. Open with one or two sentences that restore the minimum context: what the project is, what question this round addresses, and why it matters now.

### 2. Recommended Conclusion Card Structure
```markdown
## Bottom Line

One-sentence conclusion.

## Why This Matters

Which judgment or action this affects.

## Recommended Action

What to do, or what not to do yet.
```

---

## 3. Skimmability

*   **Headings carry decision information**: Do not write `Findings` or `Notes`. Write the specific conclusion or discovery, such as "WebView runs only bundled JS; the sanitizer filters before execution."
*   **Short paragraphs and explicit numbering**: Each paragraph should resolve one judgment point. When stating several parallel items, number them explicitly with `First... Second...` as required by `COMMUNICATION.md` language hygiene.
*   **Mobile scanning**: Optimize the first screen for a narrow phone display by default. Use short paragraphs and narrow tables that do not require horizontal scrolling.
*   **Language consistency**: Keep internal documents in one primary language. Retain only necessary API names, code identifiers, and metric names from another language.

---

## 4. Verifiability

Internal documents earn trust through verifiability. Put evidence links **next to the factual claim, code behavior, or historical conclusion they support.**
*   **Evidence forms**: Inline links, file paths such as `file:line`, commands, commit hashes, log or raw-data paths, and original excerpts.
*   **Placement**: Keep evidence beside the statement it supports. Do not collect all evidence at the end.

---

## 5. Adaptive Reading Trajectory

Do not assume the reader will spend either 30 seconds or 30 minutes. The same long document should support both scanning and auditing:
1.  **Scanning layer**: A one-sentence conclusion, takeaway, and status card on the first screen.
2.  **Deep-reading layer**: Detailed argument, rejected alternatives, long data, and implementation details. **Collapse these in `<details>` sections by default or anchor them at the end.**

---

## 6. Layout and Visual Components

Internal documents should actively use visual components to reduce the reader's cognitive burden.
*   When the document needs specific layouts such as status-card grids, adaptive tables, semantic chips, or dark-mode-compatible CSS, load and follow the [Internal Document Layout and Adaptive Visual Components Guide](./bestpractice_internal_visuals.md).
*   **Charts and diagrams**: Prefer PNG/JPG/WebP images. **Do not use inline SVG**, because mobile rendering is inconsistent.
*   **Mermaid** may serve only as a supporting view. It must not carry the only version of a core conclusion, and it requires a Markdown fallback nearby.
