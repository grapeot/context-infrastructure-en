# AI-Generated Presentation Slides Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Creating high-quality presentation decks for corporate training, tech talks, keynotes, etc.
- **Repo**: [github.com/grapeot/nbp_slides](https://github.com/grapeot/nbp_slides)
- **Created**: 2026-02-25
- **Source**: AI presentation practice summary

---

## Core Philosophy

Use AI image generation (Gemini) to "render" presentation content into a complete slide deck, rather than manually assembling. Each slide is a complete high-resolution image, with text and visual elements generated as a unified whole.

**Key distinction**:

- Old way: Drag elements in PowerPoint/Keynote, align one by one
- New way: Write Markdown prompts, render entire images with Gemini, play with Reveal.js

---

## Step 1: Clone Repo

```bash
git clone <your-slides-repo>
cd <slides-repo-dir>
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Create `.env` file:
```
GEMINI_API_KEY=your_key_here
```

---

## Step 2: Determine Visual Style

Edit `visual_guideline.md`. This is the "visual anchor" for all generation.

### Reference Style: **"Clean Ink"**

```
- Background: Cool light gray (#F0F4F8) + ultra-fine grid
- Illustration style: Deep navy lines, flat color fills, engineering-drawing precision
- Typography: Sans-serif (Inter/SF Pro), every slide must have a bold header
- Forbidden: Photorealistic photos, glossy 3D, generic clipart
- Mascot: <your-mascot> (title slide and closing slide only)
```

### Key Balance Principle (Very Important)

**The ultimate design goal of slides is Dual-Use: both a Presentation tool and a Handout.**

This is the most critical trade-off. One end is Steve Jobs style (pure visual, incomprehensible without the speaker); the other end is teacher style (pure text, Death by PowerPoint). We need to find the sweet spot in between:

- **As a Handout**: If slides are sent to people who didn't attend the talk, they can understand the core arguments by reading the slides alone, without needing additional explanation
- **As a Presentation**: Latecomers or distracted audience members can quickly catch up to the speaker's position through the current slide

This dual requirement means slide text cannot be just "labels" or "keyword hints" (that's Steve Jobs style), but must be **actual arguments and content** — yet not entire paragraphs of prose.

**Specific execution standards:**

- **Target ratio**: ~40% illustration / ~60% readable text
- **Layout model**: Left-right split — left side has diagrams/flowcharts/concept art, right side has 2-4 lines of key text
- **Text selection**: Slide text should be the slide's core argument itself, not a reference or hint to the argument. Readers should know what you're talking about just by seeing the text
- **Visual selection**: Illustrations should be concept diagrams/comparison charts/flowcharts (helping understand the argument), not decorative images (just filling space)
- Text must be clearly readable from the back row of the venue
- **Self-check method**: After writing a slide, cover the speaker notes and ask yourself — can a smart person who hasn't heard this talk understand what this slide is trying to say just by looking at it? If not, text is insufficient; if yes but it feels boring, visuals are insufficient

### Color Semantics (Especially Useful for Comparison Talks)

- **Orange (#C75B39)**: Old paradigm / problem side (e.g., ChatGPT, Before)
- **Teal (#0A6A74)**: New paradigm / solution side (e.g., Cursor, After)
- **Navy (#1C2526)**: Body text ink color

---

## Step 3: Write outline_visual.md

This is the "source code" of the slide deck. Format for each slide:

```markdown
#### Slide N: Title Name
*   **Layout**: Layout description (e.g., Left diagram + right text panel)
*   **Scene**:
    *   **Prompt**: [Detailed visual description, including:
        - Bold header text
        - Specific content and style of the illustration area
        - Actual readable text content in the text area (write out verbatim)
        - Color, line, typography instructions]
*   **Asset**: imgs/some_logo.png  ← Optional, use when there's a logo or screenshot
```

### Prompt Writing Tips

1. **Text content must be written verbatim into the prompt**; don't just say "add some explanatory text"
2. Illustration descriptions should be specific ("large circle, gap at bottom left, human silhouette standing in the gap")
3. Text area content should be complete (not placeholders, actual content)
4. Both sides' content must be clearly labeled `LEFT PANEL` / `RIGHT PANEL` in the prompt

### About "not" Phrasing

**Avoid negative sentence structures in slide text** (e.g., "you're not a user", "it doesn't know").
Use positive statements to express equivalent meaning, for example:

| Avoid | Use Instead |
|------|-------------|
| "you're not a user of the tool" | "you end up serving as a component of the tool" |
| "it doesn't know your config" | "it goes in blind: config unknown" |
| "this isn't just faster" | "this is a categorical shift" |
| "not just coding" | "brainstorming, drafting, planning, everything" |

---

## Step 4: Prepare Assets (Optional)

If slides involve brand logos, screenshots, QR codes:

1. Place files in the `imgs/` directory
2. Add a line in the corresponding slide in `outline_visual.md`: `*   **Asset**: imgs/filename.png`
3. The image will be automatically injected into the prompt during generation

**Common asset sources**:
- Company logos: Download PNG from official site or uxwing.com
- Screenshots: Capture directly and save
- QR codes: Generate using Python `qrcode` library or online tools

⚠️ AI cannot reliably generate brand logos (will hallucinate). When logos are needed, always provide real files as assets.

---

## Step 5: Generate 1K Version (Fast Iteration)

```bash
# Generate all slides (8-process parallel, fast)
python tools/generate_slides.py

# Generate only specific slides (when iterating on changes)
python tools/generate_slides.py --slides 3 5 8
```

Generated files are in `generated_slides/slide_XX_0.jpg` (1K resolution).

**Note**: `ThreadPoolExecutor(max_workers=8)` in generate_slides.py should be set to 8; the default may be 4.

---

## Step 6: Preview

```bash
python start-server.py  # or directly open index.html
```

`index.html` uses Reveal.js to display images; press `S` to open speaker notes mode.

---

## Step 7: Enlarge to 4K (Before Official Release)

**Critical: First test on a single slide to confirm it can enlarge to 4K or above, then process all.**

```bash
# Step 1: Test single slide first
python tools/generate_slides.py --enlarge --slides 1

# Verify: Check dimensions of generated_slides/slide_01_0_4k.jpg
file generated_slides/slide_01_0_4k.jpg
# Should show something like "3840 x 2160" or larger

# Step 2: After confirming enlargement works, process all in parallel
python tools/generate_slides.py --enlarge
```

⚠️ Enlarge operations re-call the Gemini API and are costly. Single-slide verification first is a required step.

---

## Step 8: Update index.html

`data-background` paths for each section in `index.html`:

- 1K version: `generated_slides/slide_XX_0.jpg`
- 4K version: `generated_slides/slide_XX_0_4k.jpg`

Speaker notes go in each section's `<aside class="notes">`.

---

## Speaker Notes Writing Principles

- English aimed at native speakers, conversational, can be read aloud directly
- ~120-150 words per slide
- **Avoid negative sentence structures** (same principle as slide text)
- First person, use "I", with warmth and viewpoint
- Specific details prioritized over abstract summaries

---

## Common Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| AI-generated logo is garbled | AI hallucination; logo is not real pixels | Provide real logo file from `imgs/` as asset |
| Inconsistent style | Too much variation between slide prompts | Strengthen "container" description in `visual_guideline.md`; or regenerate |
| Text garbled / illegible | Generated font too small or too ornate | Specify in prompt: "all text must be fully legible printed sans-serif" |
| AI draws mouse cursor as Cursor | Confuses Cursor company with cursor pointer | Provide Cursor company logo as asset; prompt explicitly says "Cursor company logo" |

---

## Project File Structure

```
slides/
├── outline_visual.md      # Source code (edit here each time)
├── visual_guideline.md    # Visual language definition
├── speak_notes.md         # Speech script (English, read aloud)
├── index.html             # Reveal.js player + speaker notes
├── imgs/                  # Assets (logos, screenshots, etc.)
├── generated_slides/      # Render output
│   ├── slide_01_0.jpg     # 1K version
│   └── slide_01_0_4k.jpg  # 4K version
├── tools/
│   ├── generate_slides.py      # Main generator (max_workers=8)
│   ├── gemini_generate_image.py # Gemini API wrapper
│   └── gemini_enlarge_image.py  # 4K upscaler
└── .env                   # GEMINI_API_KEY=...
```
