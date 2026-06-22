# Internal Writing Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: For readers with shared context: the user themselves, collaborators, AI agents, project workflows. Covers research memos, decision briefs, work records, executive summaries.
- **Created**: 2026-06-11

## When to Use

Loading condition: the output audience already shares context; the goal is to help them quickly form judgments, review evidence, and decide next steps.

Internal-facing writing is not a public article, not a presentation. Its value is enabling the reader to judge with minimal reading cost: is this useful, where is it useful, what is the basis for belief, what's the next step.

When the output audience is unfamiliar readers without shared context, public distribution channels, clients, or external course audiences, use `workflow_external_writing.md`.

## Core Principles

The cost of an internal document is not determined by how much the author wrote, but by the attention the reader must expend to form a judgment. The goal is not brevity — it's low decision friction.

Sometimes three sentences are enough; sometimes a table, a diagram, or an evidence index saves more cognition. Choose form based on content, not based on length.

## Information Order

Put the most important information first. Don't start with "what I did"; don't lay out background first. First give the conclusions, judgments, risks, or recommended actions that most affect decisions, then give basis, constraints, and next steps.

The opening should let the reader judge three things within 15 seconds: whether it's worth continuing; if so, which section to read most; if not, why they can close it.

Putting conclusions first does not mean directly throwing out project-internal terminology. Internal readers may also be on mobile, switching between tasks, and short-term context may not be in mind. The first screen of the opening must first restore minimal background in 1-2 sentences: what project this is, what question this round of work answers, why read now. Don't use shorthand only understandable within the current session as the first sentence, e.g., directly writing `news -> direction -> gating` or `taxonomy not migrated`; first explain "this week we're testing whether LLMs can screen trading signals using public forex news."

Optional structure:

```markdown
## Bottom Line

One-sentence conclusion.

## Why This Matters

What judgment or action this affects.

## Recommended Action

What to do, or what not to do for now.
```

Not every piece must follow a template, but the information order should be stable: conclusions before process, judgments before materials, actions before background.

## Skimmability

Internal documents must allow skip-reading. Readers should not be forced to read from beginning to end to know the structure.

- Headings carry information, not just classification labels. Don't write `Findings`; write the specific conclusion or discovery.
- Each paragraph addresses only one judgment point; keep paragraphs short.
- Parallel items are explicitly numbered. Especially when "there are three points" or "two types of risks" is stated, they must be numbered accordingly.
- Memos over 1000 words should have a mini TOC at the beginning.
- Tables are only for scenarios with stable comparison dimensions. Don't force complex judgments into tables for the sake of neatness.
- Default to optimizing the first screen for mobile reading: short paragraphs, narrow tables, few columns, avoiding the need for horizontal scrolling to understand. Wide tables at most serve as audit layers; the first-screen judgment zone prioritizes short lists, 2-3 column small tables, or chunked cards.
- Chinese internal documents default to full Chinese. Retain necessary English terms, code names, model names, filenames, and metric names, but do not have large blocks of Chinese suddenly switching to English headings, English explanations, or English table column names. Chinese-English drift significantly increases mobile reading burden.

## Verifiability

Trust in internal communication comes from verifiability, not from confident tone. For factual judgments, external information, project status, code behavior, and historical conclusions, default to placing evidence next to the judgment.

Usable evidence forms: inline links, file paths, commands, commit hashes, issue numbers, log paths, raw data paths, original excerpts.

Evidence should not be piled at the end; it should be placed next to the sentence it supports. Readers can verify immediately upon seeing the judgment, without needing to search.

## Navigation

Internal documents are often not final answers but entry points for future actions, and should be organized as navigation systems.

- Default to Markdown.
- Local files use relative paths or workspace-stable paths.
- External sources use inline Markdown links.
- When involving code, give `file:line` or at least the file path.
- When involving data, give raw data path and generation script path.
- When involving images, place images in the same directory, or clearly annotate the generation method.
- When a section comes from another document, link back to the original; don't copy large unsourced summaries.

## Visual Cognitive Load Reduction

### Why This Section Is Needed Now

Past writing methodologies (Markdown-first, form serves content, bottom-line up front, etc.) were all built on an implicit assumption: **writing documents is expensive, reading documents is cheap enough not to warrant dedicated optimization**. An engineer writes one design doc per week; readers are willing to spend 30 minutes reading carefully — ROI naturally holds. Under this cost structure, the optimization point is "content quality"; form just needs to not get in the way.

AI changed this cost structure. The marginal cost of writing documents approaches zero (drafting, rewriting, expanding, cross-document syncing are all minute-level; one week can produce 50 design docs instead of 1), and publishing documents also dropped to zero (Web Preview, HTML artifact, auto share). But **the cost of reading documents hasn't changed** — still constrained by human attention bandwidth. A team member can review 30 minutes of documents per day (optimistically); they won't expand to 25 hours just because AI produces 50x more.

Result: document production capacity exploded; consumption capacity didn't move. The bottleneck shifted from "writing" to "reading." The axiom "form serves content" isn't wrong, but the implicit corollary "content is everything" is wrong. When reading is no longer cheap, **form begins to independently carry value** — well-formed documents convey more actionable judgments in the same reading time; poorly-formed documents cause reader overload or feigned understanding.

This section explicitly optimizes "reading rate."

### Three Axioms

The methodology is not a rule set; it's a few fundamental judgments from which specific rules can be derived. This skill commits to three:

1. **Visual is a bandwidth tool, not decoration**. Every visual element must answer: "What specific cognitive friction does it reduce for the reader?" Three genuine reduction mechanisms: **parallel channels** (color chip + text title = visual scanning + linguistic deep reading in parallel), **spatial memory** (tables use position to carry relationships, same column = same dimension, readers use spatial indexing instead of linear search), **expectation templates** (form carries its own semantics — progress bar = linear, matrix = two-dimensional tradeoff, card = side-by-side status — readers apply templates instead of constructing from scratch). A visual that triggers none of these three mechanisms = decoration; delete it.
2. **Adaptive beats static**. "How much time the reader is willing to spend" is a variable, not a constant. For the same RFC, a reader making an intuitive small change can scan in 30 seconds; a reader auditing a major change will go paragraph by paragraph. Presetting the attention budget to a single value will be wrong no matter which side you pick. Documents should **simultaneously carry multiple trajectories**, using anchors / `<details>` / links to let scanning and deep reading coexist.
3. **Markdown is source of truth; HTML is the cognitive optimization layer**. Markdown must be independently readable — any stripped-HTML renderer (GitHub, plain text email, grep output) can get 80% of the value. HTML extensions add scanning structure, adaptive hooks, and visual templates to existing Markdown, but do not carry unique information.

---

**Fundamental goal**: All visual decisions serve one thing — letting readers **read fewer words, judge faster**. Visual is not about making documents pretty, not "adding a feature," not "looking visual." It is a tool for **increasing cognitive bandwidth / accelerating decision precision** for the reader. If after reading a visual block the reader hasn't reached a judgment faster than reading a plain paragraph, it has failed — even if it has chips, colors, and borders.

Internal documents should proactively use visual structure to reduce cognitive load.

When the problem involves temporal trends, dependency relationships, classification, decision trees, processes, architecture, or comparison matrices, generate diagrams, tables, or schematics. The goal of diagrams is to help readers judge faster, not decoration.

Default to **MD-first visual**: Markdown is source of truth; visual blocks are cognitive compression layers. Prioritize visual structures directly readable on mobile: short tables, comparison cards, numbered state diagrams, ASCII/Unicode simple diagrams, inline images, few-column matrices, and `<details>` progressive disclosure. Mermaid can serve as an enhanced view but must not be the sole carrier of information, as mobile or certain Markdown browsers may not render it; Mermaid must have an equivalent-information plain Markdown fallback before and after.

Each visual block must answer a clear question, e.g., "which research path was negated this week," "which feature migrated across products," "what are the three choices for next week." Don't stuff text into large diagrams just to appear visual. Table, diagram, and card titles should state conclusions, not write form labels like `Flowchart` or `Matrix`.

### The Unit of Judgment Is the Block, Not the Whole Document

Don't lock the entire document into "all commit" or "all explore" mode. A weekly report can have the first screen be commit (status cards at top, one glance for decisions) and below be explore (argument paragraphs must be text for readers to audit reasoning). Every visual decision is a block-level judgment, not a whole-document judgment. Whole-document one-size-fits-all is overfitting; common symptoms are simple structures on the first screen followed by same-form complex structures (card grids cramming argument paragraphs), or the reverse (argument paragraphs with a status card forced at the beginning).

### Front Gate: Shared Context Thickness (Pass This First)

Before entering any visual judgment, first ask: Can the reader decode the visual semantics you intend to use?

- **Thick** (reader set ≤ 3 people + same project same week) → can use any chips / colors / cards; semantics don't need to be self-explanatory
- **Thin** (cross-team / cross-quarter / newcomers / external readers) → any visual must first pay the explanation tax. Chips must have a legend at first appearance; color semantics must be self-contained within this document; cannot assume readers inherit context

Thin context + complex visual = directly veto the visual, regardless of what the tension axis says later. This gate is not a tension; it's a prerequisite.

### Back Gate: Factual Confidence (Downgrade Visual When Facts Are Unstable)

Visual makes things "look very certain." When underlying facts are changing — decisions reversing, data unstable, PR not yet merged, experiment not reproduced — visual's appearance of certainty is a liability; readers will over-trust. **When facts are unstable, downgrade visual to table + timestamp, or plain text**. A status chip with green "live" is a commitment; don't commit when facts aren't stable.

### Adaptive Reading Paths: Let Documents Simultaneously Carry Multiple Trajectories

Don't preset whether the reader will spend 30 seconds or 30 minutes. The same document (especially RFCs / long docs) may be scanned by a reader making an intuitive small change, or audited paragraph by paragraph by a reader reviewing a major change. Treating "attention budget" as a static preset will be wrong no matter which side you pick.

The correct approach is to simultaneously carry both trajectories:

1. **First-screen scan layer**: visual + one-sentence takeaway + status chip; 30 seconds gets the core judgment
2. **Deep-read hooks**: provide "I want to look closer" entry points via anchors / links / `<details>`, letting every claim in the scan layer zoom into evidence / tradeoffs / reasoning
3. **Deep-read layer**: detailed argumentation, rejected alternatives, tradeoffs, raw data — default collapsed or anchored at the end, not blocking the first screen

This is why we need the HTML extension layer rather than just Markdown: adaptive paths rely on mechanisms like anchors / collapsing / hover preview; Markdown alone isn't enough. Markdown is source of truth; HTML is the cognitive optimization layer.

**Specific adaptive mechanisms (stratified by committed / evolving)**:

Committed, usable immediately:
1. **First-screen takeaway anchor** — the document's first sentence must be a one-sentence conclusion; scan readers take it and leave
2. **Anchor jumps** — `[see details](#deep-link)` lets scan readers jump to the deep-read layer in one click; table row `see RFC §7.5` for cross-document single source
3. **`<details>` collapsing** — deep-read layer default collapsed, not blocking scanning

Evolving (OpenCode Web Preview future phase capabilities, usable as methodological evolution direction, not current requirements):
4. **hover preview / tooltip** — mouse hover on anchor previews target content, so deep-read hooks don't require actual page jumps
5. **chunked progressive disclosure** — long docs lazy-load subsequent chapters by milestone; scanning doesn't pay load cost

Low cognitive load **does not equal short**, nor **does it equal long**. The key is that the **number of new concepts introduced per unit space** matches the reader's current mental model — neither overloaded nor redundant.

- **Too high (densely packed jargon)**: A sentence like "WKWebView loads preview.html from bundle, Swift injects markdown via JSON serialization" reads short, but contains 4 new concepts (WKWebView, bundle, preview.html, JSON serialization); the reader's first reaction is "which bundle, what preview.html," needing to mentally clarify 4 things before absorbing this one sentence — this is high cognitive load, even with few words.
- **Too low (re-explaining every concept from scratch)**: Expanding every term, repeating known content, wasting the reader's time on what they already know, the whole paragraph becomes long with no new information density — this is also high cognitive load.
- **Optimal**: Each paragraph introduces 1–2 new concepts, anchored by concepts the reader **already knows**; the next paragraph builds on this foundation. This is the writing version of Vygotsky's "zone of proximal development" — each step's new content must fall within the reader's "can absorb" range.

**Hard test for "is this piece of information appropriate here"**: Can the expected reader mentally absorb it using concepts they already know? If not, three treatments:
- **Analogy anchor**: Use something the reader knows as an anchor ("like browser view-source, that kind of local HTML").
- **Deferred expansion**: First give a conclusion sentence with no prerequisite concepts; put technical details in `<details>` or the next paragraph.
- **Simply don't say it**: If this detail doesn't affect the judgment the reader needs to make, don't mention it; keep it in engineering-layer documentation.

When writing decision tables / status cards, the "decision" column should use **business language** (what the user does, what they see), not implementation details (WKWebView, DOMPurify, data URI) — implementation details go into `<details>` or subsequent paragraphs. On the first scan pass, the reader wants "where, doing what, what status," not "what technology was used."

### Arsenal (Organized Like a UI Library)

Cognitive bandwidth optimization visual weapons are not "feels visual" forms; they are the minimal set repeatedly proven in current dogfood. Each weapon corresponds to a specific cognitive problem; don't add weapons just to "enrich the arsenal." Standard for adding weapons: only add when dogfood repeatedly proves a gap.

| Weapon | Cognitive Problem Solved | When to Use |
|--------|-------------------------|-------------|
| Short paragraphs | Default form, carries argumentation and reasoning | Almost always |
| Compact tables | Stable-dimension comparison across multiple items (triggers spatial memory) | Rows ≥ 4 and each row has the same structure |
| Status card grid | Several side-by-side items, one glance at color blocks for judgment (triggers expectation templates) | Items ≤ 4-6 and color distribution is balanced |
| chip / pill | Mark semantics of a single item (triggers parallel channels) | Same column distribution balanced ≥ 2 categories; color semantics self-contained in this document |
| `<details>` | Audit materials / rejected alternatives / long fixtures / implementation details | Content is "reader might want to verify but doesn't need to read" |
| anchor links | Let scan readers zoom into deep-read layer | Every "claim → evidence" pair should have an anchor |
| Inline SVG | Dependency network or flow with 3-7 nodes | Mermaid unavailable and form is stable |
| Code block + line number reference | Cite specific code locations | Decision depends on specific source snippets |
| Time series chart | See trends, inflection points, anomalies | Data points span time |
| Two-dimensional matrix | See tradeoffs, positioning, priorities | Comparison across two dimensions |

Detailed conditions, anti-patterns, and compound usage for each weapon are in the specific sections below.

### Form Selection: Boundaries of Tables / Card Grids / `<details>`

**First-screen one-glance scan; details into `<details>`**. The hard test for whether a visual block is truly "low cognitive load": after compressing to one table / one row of chips / one takeaway paragraph, can the reader still get the core conclusion in one glance? If "the words thrown away by compression" are words the reader wouldn't have read anyway, the original version was redundant.

- **Card grid**: Only suitable when count ≤ 4–6 and each card's takeaway genuinely needs a small space to carry an icon + short judgment (scenarios like "which path holds" — "one glance at color tells the answer").
- **Table**: Beyond this count, or when each record needs more than half a sentence of explanation, use a table. One row per decision (decision name / status / one-sentence reason), compact, scannable in one pass.
- **`<details>`**: Details, tradeoffs, process, implementation details, engineering pitfalls. Everything not needed in the first reading layer goes here.

**Anti-pattern: Status cards written like encyclopedia entries**. Each card has chip + title + 80–150 word explanatory paragraph — looks visual but still requires reading a paragraph to get the conclusion. Change to a combination of the three forms above.

Suitable diagram types:

- Time series: see trends, inflection points, anomalies
- Two-dimensional matrix: see tradeoffs, positioning, priorities
- Flowchart: see dependencies and blocking points
- Stack diagram: see system layering
- Decision tree: see next-step judgment paths

Visual forms particularly useful for mobile reading:

- **Conclusion cards**: One question, one answer, one action impact; suitable for first-screen context restoration.
- **Before / After comparison**: Suitable for explaining how a week's work changed previous judgments.
- **Path status table**: Each path marked as "holds / negated / still blocked / candidate only," replacing unstable-rendering flowcharts.
- **Evidence map**: Map key conclusions to 1-3 evidence files, avoiding readers searching through long text for sources.
- **Collapsible audit layer**: Put scripts, costs, methodology, candidate lists into `<details>`, preserving verifiability without occupying the first reading layer.

### HTML-in-Markdown Experimentation Rules

Markdown can contain small amounts of HTML/CSS for cards, side-by-side comparisons, status bars, inline SVG, but it is an enhancement layer, not a default dependency. Different renderers vary greatly in support for `<style>`, inline SVG, `class`, dark theme inheritance, and Markdown parsing within HTML blocks; mobile is especially unstable.

When using HTML-in-MD, observe the following constraints:

- **Only local enhancement**: Don't wrap the entire document in an outer `<div>`, and don't set fixed `color`, `background`, or fonts for the whole document. Only set styles for local components like cards, callouts, SVG.
- **Explicitly close every HTML block**: Missing `</div>` will swallow subsequent Markdown into the HTML container; common symptoms are body text color errors in dark themes, heading style drift, subsequent Markdown no longer parsing.
- **CSS colors use "theme variables + fallback," never hardcode a single light/dark**: This is the core rule for avoiding dark mode breakage. Card/status bar/chip colors use `var(--name, fallback)` form, e.g., `background:var(--card-bg, #f6f6f6)`, `color:var(--fg, #1a1a1a)`, `border-left:5px solid var(--ok-border, #10b981)`. Renderers supporting theme variables (OpenCode iOS Web Preview) automatically pick colors per light/dark; the same MD works in both modes. Renderers that don't support them (Cursor/VS Code, GitHub if retaining `<style>`) fall back to fallback values, visually equivalent to light mode. **Absolutely do not** write only a hardcoded light background (`background:white`, `#f8fafc`) with dark text — it will blur into a mess on a host dark background. Plain Markdown paragraphs still do not manually specify colors; leave them to the renderer theme.
  - Available theme variables (exposed by OpenCode Web Preview, fallback works in unsupported renderers): body `--fg` / background `--bg` / muted text `--fg-muted` / border `--border` / link `--link` / code `--code-bg`·`--code-fg` / card background `--card-bg`; semantic status colors each have `-border` (strong color, stroke/left bar), `-bg` (light background), `-fg` (text) three levels: `--ok-*` (holds/green), `--bad-*` (negated/red), `--warn-*` (warning/yellow), `--block-*` (blocked/gray).
  - Writing example: `.card.ok{border-left:5px solid var(--ok-border,#10b981);background:var(--card-bg,#f6f6f6);color:var(--fg,#1a1a1a)}`; chip: `.chip.ok{background:var(--ok-bg,#d1fae5);color:var(--ok-fg,#065f46)}`.
  - **Semantic classes must use compound selectors, never write bare single classes**. Decorative inline elements (chip/badge/pill) semantic colors must bind dual classes `.vx-chip.ok` / `.chip.ok`; **do not** write only `.ok{...}`. Reason: bare `.ok` specificity (0,0,1,0) equals card's `.vx-card`, will be inherited/overridden by card body `color:var(--fg)`, causing chip text to fall to `--fg` instead of `--ok-fg`, making chips nearly invisible in dark mode; dual-class specificity (0,0,2,0) exceeds card single-class and can reliably hit.
- **Every HTML visual must have a Markdown fallback**: Status cards followed by status table; inline SVG preceded/followed by equivalent text/table. When the renderer disables HTML, readers can still get equivalent judgment.
- **Avoid relying on Markdown parsing inside HTML blocks**: `## headings`, backtick code, and Markdown links inside `<div>` will not parse as Markdown in many renderers. Use HTML tags inside HTML blocks; Markdown content goes outside blocks.
- **Cross-renderer check before external distribution or long-term reuse**: At minimum check Cursor/VS Code, GitHub/GitLab preview, target mobile client. If the target end doesn't support HTML-in-MD, convert to rendered PNG/SVG images for embedding, or derive a standalone HTML artifact.

### Delta from Old Markdown-First Practice

Explicitly state "how Markdown was written before, how to write per this methodology now, why the change." If a skill item sounds like it conflicts with old practice, check this table — it's usually a direct implication of the cost structure change (reading is the new bottleneck).

| Dimension | Old Markdown-First Practice | This Skill's Advocated Practice | Why Changed |
|-----------|----------------------------|--------------------------------|-------------|
| Reading path assumption | Linear, reader reads start to finish | Multi-trajectory, scanning + deep reading coexist | AI produces more; reader budget is fixed |
| Form's role | Serves content, minimal | Independently carries value (scan layer / adaptive hooks) | Reading is the new bottleneck |
| HTML usage | Not used or freestyle | Controlled extension layer (like UI library, fixed weapon set) | Freestyle = maintenance tax source |
| Decision mechanism | Experience + style guide | Three axioms + two gates + block-level judgment | Experience doesn't scale to AI |
| Error detection | Peer review | Post-write scan (scan + threshold + fix) | AI authors don't self-review |
| Cross-document same decision | Write it in every document | Single source + anchor link | AI overproduction causes drift |

### Unresolved Matters (Live Working Items)

These are judgments still evolving; when encountered, act on current best guess and record in dogfood notes for next review:

1. **Chip boundaries**: Current rule says "same column distribution balanced ≥ 2 categories," but in practice most scenarios don't meet this. Should chips be classified as "special scenario weapon" rather than common?
2. **Cross-document single decision standard**: (a) single source + other docs link / (b) accept duplication + last-synced stamp — currently leaning toward (a), but (a) requires tool support (broken link detection).
3. **Should the HTML extension layer be concretized into reusable CSS modules** (a cross-project shared `cognitive_writing.css`), with all projects reusing the same set of chip / card / details styles?
4. **Methodology self-review cadence**: Sink new anti-patterns into the skill after each dogfood discovery, or review quarterly? Currently the former.

## Post-Write Scan (Self-Eval)

After writing one pass, execute the following **scan actions** — not asking questions before writing (AI has no answers before writing), but **scan + threshold + fix** triples after writing.

| Scan | Threshold = Trigger | Fix |
|------|---------------------|-----|
| Chip column color enum value occurrence count | Dominant color ≥ 80% | Delete chip column; annotate exception rows with end-of-row `⚠ blocked` marker |
| Grep current repo for this paragraph's core conclusion | Hits ≥ 2 | Change this paragraph to `see [path]`; don't duplicate text |
| Each `##` / `###` heading: after deleting it, can the body's first sentence stand alone as a subheading | Yes = heading is a category name | Rewrite heading as that body sentence's judgment |
| Does the text contain strikethrough + "(date)" stamp | Yes = history dumped into body | Rewrite body as latest decision; move old version to end-of-article changelog or `<details>` |
| If `<details>` content is deleted, can the reader still complete the primary judgment | No = details contain core | Move core out of details; collapsible area only keeps audit materials |
| Chip / status classification enum values — are they the same set across this document's sections | Different = semantic drift | Unify to one set across the document (recommend ok/warn/bad/block cap) |

## Common Failure Modes

| Failure Mode | Symptom | Solution |
|-------------|---------|----------|
| Written like an article | Heavy buildup and narrative; reader must finish to know the conclusion | Move bottom line, basis, and next steps to the beginning |
| Short but unclear | Few words, but judgment, evidence, and actions mixed together | Separate into conclusion, basis, constraints, next steps |
| Unverifiable | No links, file paths, or data sources next to judgments | Place evidence next to the corresponding judgment |
| Headings without information | Headings are all `Background`, `Findings`, `Notes` | Write discoveries or judgments directly in headings |
| Decorative diagrams | Diagrams look good but don't help judgment | Only keep diagrams that reduce cognitive load |
| Excessive Mermaid dependency | Doesn't render on mobile or diagram too wide; reader still must mentally reconstruct | Every Mermaid must have plain Markdown fallback; first screen doesn't use Mermaid for sole conclusions |
| HTML block leakage | Missing closing tags or global CSS affecting subsequent body; dark theme becomes dark background with dark text | HTML only local enhancement, explicitly closed; plain Markdown doesn't set colors |
| Dark mode cards fading/blurring | Cards use hardcoded light backgrounds (`white`, `#f8fafc`), nearly invisible on renderer dark background | Card colors use `var(--card-bg,#f6f6f6)`/`var(--fg,#1a1a1a)`/`var(--ok-border,#10b981)` form; theme variables + fallback, dual-mode adaptive |
| Terminology cold start failure | Opening directly uses project shorthand; reader switching back between tasks can't understand | First screen first restores minimal background, then gives conclusion |
| Chinese-English drift | Headings, headers, explanations suddenly switch to English; reading rhythm breaks | Internal defaults to Chinese; English only retains necessary terms and code/metric names |
| Evidence piled at the end | Reader must flip back and forth to find sources | Use inline links or paths adjacent to judgments |
| Cross-document duplication of same conclusion text | Same decision written in 3+ documents; inevitably drifts and conflicts after half a year | Single source of truth; other documents only `see [path]`; don't duplicate conclusion text |
| `<details>` containing core conclusions | "Expand on demand" implies non-essential reading, but content is essential; not expanding loses core information | `<details>` only holds audit materials / rejected alternatives / long fixtures; core conclusions expanded in body |
| Status table row keys using Phase/Sprint | AI defaults to engineering timeline; reader must reverse-map "Phase 1 equals what user value" | Row keys use "what the user can experience"; Phase numbers go into column names or details |
| Chip column ≥80% same color | Chips have no filtering or comparison value, purely decorative; reader instead must scan row by row for exceptions | Delete chip column; annotate exception rows with end-of-row `⚠ blocked` marker |
| Decision reversals using strikethrough + update stamp stacking | Dumping git history into body; reversal layers become unmaintained after half a year | Directly rewrite body as latest decision; move old version to end-of-article changelog or `<details>` |
| Headings write category names instead of judgments | "Security Model," "Solution Overview," "Architecture Decisions" carry no takeaway; reader scanning TOC gets no information | Headings write judgments, e.g., "WebView only runs bundle JS; sanitizer strips scripts after rendering" |
