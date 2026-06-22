---
title: PDF to Markdown
category: BestPractice
tags: [pdf, markdown, docling, document-conversion]
difficulty: Easy
created: 2026-04-27
---

# PDF to Markdown

When you need to convert PDF to Markdown (for feeding to LLMs, content extraction, archiving source materials), **default to Docling**.

## Why Docling

In the OpenDataLoader benchmark of 12 PDF→Markdown engines, Docling scored the highest overall (0.882), with the best table and heading fidelity. MIT license, pure Python, runs on CPU (~3 seconds/page), faster with GPU.

Tested counterexamples to avoid:

- **MarkItDown**: underlying engine is pdfminer.six, heading hierarchy retention rate 0%, tables essentially collapse. OK for Office documents, not for PDF.
- **PyMuPDF4LLM**: fastest but AGPL, commercially restricted.
- **Marker**: quality close to Docling but GPL, commercial use requires payment.

If you want to keep engine comparison research in your own workspace, place the research notes in project docs or under `contexts/`, and link to your local report from this skill.

## Quick Usage

```bash
uv pip install --python .venv/bin/python docling
```

```python
from docling.document_converter import DocumentConverter

conv = DocumentConverter()
result = conv.convert("input.pdf")
md = result.document.export_to_markdown()
```

The first call downloads ~1 GB of model weights to the HuggingFace cache; subsequent calls reuse them. The same `DocumentConverter()` instance can convert multiple files consecutively; don't create a new one for each file.

You can also directly use the CLI bundled with this skill. It wraps Docling, LM Studio VLM OCR, and environment checks into fixed commands suitable for repeated agent invocation:

```bash
source .venv/bin/activate
python rules/skills/pdf_to_markdown_cli.py doctor --format json
python rules/skills/pdf_to_markdown_cli.py docling input.pdf --output output.md --format json
```

On macOS, especially Apple Silicon, when calling Docling's official CLI directly, prefer explicitly using CPU to avoid MPS backend crashes on `torch.float64` during layout detection:

```bash
docling input.pdf --to md --device cpu --no-ocr --output output_dir
```

## Acceptance

- Output Markdown preserves tables using standard `| ... |` syntax, columns aligned
- Heading hierarchy (`#`, `##`, `###`) matches the original PDF visual hierarchy
- Size-wise: text-only PDFs typically compress 5–10x to Markdown; pure scans won't shrink significantly

## Known Pitfalls

**Section headings swallowed**. When a heading in the PDF is emphasized text inside a table (not a true layout heading), Docling may recognize it as a regular cell. The symptom is two consecutive `## HOLDINGS` without account name differentiation. Handling: use context (account numbers, beginning balance) to cross-reference the original PDF page, manually supplement section headers if needed.

**Two PDFs with identical content but different filenames**. If two conversions produce exactly the same character count, first `md5` compare the source files — it's likely a mix-up during upload. Docling won't proactively deduplicate.

**pip missing in venv**. In a venv created by uv, pip is typically not installed; `venv/bin/python -m pip install` will error with `No module named pip`. Use `uv pip install --python .venv/bin/python <pkg>` instead.

## Known Pitfalls (continued)

**macOS MPS float64 crash**. On Apple Silicon, Docling's RT-DETR V2 model calls `torch.float64` during layout detection, which the MPS backend doesn't support, causing the entire PDF conversion to crash. The simplest workaround is to run Docling on CPU directly:

```bash
docling input.pdf --to md --device cpu --output output_dir
```

For text-only PDFs that don't need OCR, add `--no-ocr` to reduce extra model paths and false recognition:

```bash
docling input.pdf --to md --device cpu --no-ocr --output output_dir
```

Don't rely on `PYTORCH_ENABLE_MPS_FALLBACK=1` as the first option. In practice, fallback may still not take effect with certain version combinations; `--device cpu` directly is more deterministic. If the CPU path still fails, or the PDF is a Chinese-language scan, image PDF, or pitch deck, then switch to the VLM OCR path.

## Applicability Boundaries and Path Selection

| PDF Type | Preferred | Fallback | Not Recommended |
|----------|-----------|----------|-----------------|
| Text PDF (Office/WPS export, LaTeX) | Docling | — | MarkItDown |
| Scanned (primarily English) | Docling (built-in OCR) | Tesseract | — |
| Scanned/Image PDF (primarily Chinese, mixed text/images, pitch deck) | **LM Studio VLM OCR** | Tesseract (low accuracy) | Docling (MPS float64 risk) |
| Complex math formulas | Docling (export LaTeX) | Manual proofreading | — |

## CLI: PDF→Markdown

The CLI file is located at `rules/skills/pdf_to_markdown_cli.py`. It is not a standalone service and does not persist state; each run reads the input PDF, writes Markdown, and outputs a result summary to stdout. Progress and errors go to stderr.

### Prerequisites

Use `.venv` at the workspace root:

```bash
source .venv/bin/activate
uv pip install docling
```

If using the LM Studio VLM OCR fallback, also need:

```bash
uv pip install pdf2image pillow requests
```

`pdf2image` depends on system Poppler. On macOS:

```bash
brew install poppler
```

LM Studio needs to be manually opened with a vision model loaded. Default API is `http://127.0.0.1:1234/v1`, default model name is `qwen/qwen3.5-35b-a3b`.

### Doctor

Run doctor first to check whether the local environment is complete:

```bash
python rules/skills/pdf_to_markdown_cli.py doctor --format json
```

When needing to check whether LM Studio is online and the target model is loaded:

```bash
python rules/skills/pdf_to_markdown_cli.py doctor --check-lmstudio --format json
```

### Docling Path (Default Preferred)

For regular text PDFs, LaTeX PDFs, Office-exported PDFs, prefer Docling:

```bash
python rules/skills/pdf_to_markdown_cli.py docling input.pdf --output output.md --format json
```

Equivalent generic command:

```bash
python rules/skills/pdf_to_markdown_cli.py convert input.pdf --engine docling --output output.md --format json
```

### LM Studio VLM OCR Path

When Docling's OCR clearly fails on Chinese scans, image PDFs, or pitch decks, explicitly switch to VLM OCR:

```bash
python rules/skills/pdf_to_markdown_cli.py vlm-ocr input.pdf \
  --output output.md \
  --model qwen/qwen3.5-35b-a3b \
  --timeout 300 \
  --format json
```

Common tuning parameters:

- `--dpi 150`: lower DPI when images are too large, model response is slow, or output drifts
- `--start-page N --end-page M`: process only a page range, verify first then run the full document
- `--api-base http://127.0.0.1:1234/v1`: explicitly specify when LM Studio is not on the default port

VLM OCR output includes `=== PAGE N ===` page markers. Large PDFs take ~30-60 seconds per page; a 17-page pitch deck takes ~10-15 minutes, depending on model and machine load.

### CLI Acceptance

- With `--format json`, stdout must be parseable JSON
- `doctor` must accurately report missing dependencies or LM Studio offline status
- Docling output must preserve heading hierarchy and Markdown tables
- VLM OCR output must preserve the original language, not summarize or translate, and include page separators

## LM Studio VLM OCR Principles

When both Docling and Tesseract fail (Chinese pitch decks, image-dense slides), use a local vision model for OCR. The CLI is at `rules/skills/pdf_to_markdown_cli.py`:

```bash
source .venv/bin/activate
python rules/skills/pdf_to_markdown_cli.py vlm-ocr input.pdf --output output.md --timeout 300
```

Prerequisite: LM Studio running locally (default `http://127.0.0.1:1234`), with a vision model loaded. Default model is `qwen/qwen3.5-35b-a3b`, whose OCR performance on mixed Chinese-English pitch decks far exceeds Tesseract.

The script renders each PDF page as an image (200 DPI), feeds each page image through LM Studio's `/v1/chat/completions` endpoint, and outputs Markdown with `=== PAGE N ===` page separators. The prompt is generic OCR, without financial schema constraints. Large PDFs take ~30-60 seconds per page; a full 17-page pitch deck takes ~10-15 minutes.

Note: LM Studio's VLM API is OpenAI-compatible, not a dedicated OCR API. Output quality depends on model capability and prompt. If a page's OCR result clearly deviates from the original image, lower DPI (`--dpi 150`) or shorten the prompt instructions and retry.

## Scenarios Still Requiring Manual Review

- Complex math formulas: Docling can export LaTeX, but fidelity is limited
- Archival scenarios requiring preserved page numbers, headers, and footers: Docling defaults to stripping these; VLM OCR may also alter layout
- Legal, financial, medical, and other high-risk documents: must sample-check against the original PDF after conversion
