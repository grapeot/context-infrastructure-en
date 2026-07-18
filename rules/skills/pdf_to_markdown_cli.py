#!/usr/bin/env python3
"""PDF to Markdown helper CLI for AI agents.

The default path uses Docling for text PDFs. The VLM path renders pages and
calls a local LM Studio OpenAI-compatible vision model for scan-heavy PDFs.
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import io
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_API_BASE = "http://127.0.0.1:1234/v1"
DEFAULT_MODEL = "qwen/qwen3.5-35b-a3b"
DEFAULT_DPI = 200
DEFAULT_TIMEOUT = 300

OCR_SYSTEM_PROMPT = (
    "You are a precise OCR assistant. Given a PDF page image, extract ALL "
    "visible text faithfully. Output Markdown with headings, paragraphs, "
    "tables, and structured formatting when appropriate. Do NOT summarize or "
    "translate. Preserve the original language exactly. Include key numbers, "
    "labels, captions, and table structure."
)

OCR_USER_PROMPT = (
    "Extract all visible text from this PDF page as Markdown. Output only the "
    "Markdown content, no extra commentary."
)


class CliError(Exception):
    """User-facing command error."""


def has_module(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def default_output_path(pdf_path: Path, suffix: str = ".md") -> Path:
    return pdf_path.with_suffix(suffix)


def normalize_api_base(api_base: str) -> str:
    return api_base.rstrip("/")


def encode_image(image: Any) -> str:
    image_module_missing = not hasattr(image, "convert")
    if image_module_missing:
        raise CliError("Image object does not support PIL-style conversion")

    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="JPEG", quality=95)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def build_vlm_payload(image_b64: str, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": OCR_SYSTEM_PROMPT}]},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": OCR_USER_PROMPT},
                ],
            },
        ],
        "temperature": 0,
        "max_tokens": 16384,
    }


def extract_message_text(response_data: dict[str, Any]) -> str:
    choices = response_data.get("choices") or []
    if not choices:
        raise CliError(f"No choices in LM Studio response: {response_data}")

    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content

    reasoning_content = message.get("reasoning_content")
    if isinstance(reasoning_content, str) and reasoning_content.strip():
        return reasoning_content

    if isinstance(content, list):
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict)]
        joined = "".join(text_parts).strip()
        if joined:
            return joined

    raise CliError(f"LM Studio response did not contain text content: {response_data}")


def validate_page_range(start_page: int, end_page: int | None) -> None:
    if start_page < 1:
        raise CliError("--start-page must be >= 1")
    if end_page is not None and end_page < start_page:
        raise CliError("--end-page must be >= --start-page")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def convert_with_docling(pdf_path: Path) -> str:
    if not has_module("docling"):
        raise CliError("Missing dependency: docling. Install with `uv pip install docling`.")

    from docling.document_converter import DocumentConverter  # type: ignore

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    return result.document.export_to_markdown()


def render_pdf_pages(pdf_path: Path, dpi: int, start_page: int, end_page: int | None) -> list[Any]:
    if not has_module("pdf2image"):
        raise CliError("Missing dependency: pdf2image. Install with `uv pip install pdf2image`.")

    from pdf2image import convert_from_path  # type: ignore

    validate_page_range(start_page, end_page)
    kwargs: dict[str, Any] = {"dpi": dpi, "first_page": start_page}
    if end_page is not None:
        kwargs["last_page"] = end_page
    return convert_from_path(str(pdf_path), **kwargs)


def ocr_page_via_lmstudio(image: Any, api_base: str, model: str, timeout: int) -> str:
    if not has_module("requests"):
        raise CliError("Missing dependency: requests. Install with `uv pip install requests`.")

    import requests  # type: ignore

    payload = build_vlm_payload(encode_image(image), model)
    response = requests.post(
        normalize_api_base(api_base) + "/chat/completions",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return extract_message_text(response.json())


def convert_with_vlm(
    pdf_path: Path,
    api_base: str,
    model: str,
    dpi: int,
    timeout: int,
    start_page: int,
    end_page: int | None,
) -> str:
    pages = render_pdf_pages(pdf_path, dpi, start_page, end_page)
    page_count = len(pages)
    md_parts = [f"OCR_TOTAL_PAGES: {page_count}\n"]

    for index, image in enumerate(pages):
        page_num = start_page + index
        print(f"OCR page {page_num} ({index + 1}/{page_count})", file=sys.stderr, flush=True)
        text = ocr_page_via_lmstudio(image, api_base, model, timeout)
        md_parts.append(f"=== PAGE {page_num} ===\n\n{text}\n")

    return "\n\n".join(md_parts)


def lmstudio_models(api_base: str, timeout: int = 10) -> tuple[bool, list[str], str | None]:
    if not has_module("requests"):
        return False, [], "Missing dependency: requests"

    import requests  # type: ignore

    try:
        response = requests.get(normalize_api_base(api_base) + "/models", timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:  # pragma: no cover - exact exception depends on requests
        return False, [], str(exc)

    models = [item.get("id", "") for item in data.get("data", []) if item.get("id")]
    return True, models, None


def doctor(api_base: str, model: str, check_lmstudio: bool) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "python": sys.executable,
        "dependencies": {
            "docling": has_module("docling"),
            "pdf2image": has_module("pdf2image"),
            "PIL": has_module("PIL"),
            "requests": has_module("requests"),
        },
        "lmstudio": {
            "checked": check_lmstudio,
            "api_base": normalize_api_base(api_base),
            "target_model": model,
        },
    }

    if check_lmstudio:
        ok, models, error = lmstudio_models(api_base)
        checks["lmstudio"].update(
            {
                "available": ok,
                "models": models,
                "target_model_loaded": model in models,
                "error": error,
            }
        )
    return checks


def require_pdf(path_text: str) -> Path:
    pdf_path = Path(path_text).expanduser()
    if not pdf_path.exists():
        raise CliError(f"PDF not found: {pdf_path}")
    if not pdf_path.is_file():
        raise CliError(f"PDF path is not a file: {pdf_path}")
    return pdf_path


def emit_result(result: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    for key, value in result.items():
        print(f"{key}: {value}")


def add_common_convert_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("pdf", help="Input PDF path")
    parser.add_argument("--output", help="Output Markdown path")
    parser.add_argument("--format", choices=["text", "json"], default="text")


def add_vlm_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-base", default=DEFAULT_API_BASE, help="LM Studio OpenAI-compatible API base")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="LM Studio model id")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, help="PDF render DPI")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="LM Studio request timeout seconds")
    parser.add_argument("--start-page", type=int, default=1, help="First page to process, 1-indexed")
    parser.add_argument("--end-page", type=int, default=None, help="Last page to process, 1-indexed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert PDF files to Markdown for AI workflows")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Check local dependencies and optional LM Studio availability")
    doctor_parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    doctor_parser.add_argument("--model", default=DEFAULT_MODEL)
    doctor_parser.add_argument("--check-lmstudio", action="store_true")
    doctor_parser.add_argument("--format", choices=["text", "json"], default="text")

    docling_parser = subparsers.add_parser("docling", help="Convert with Docling")
    add_common_convert_args(docling_parser)

    vlm_parser = subparsers.add_parser("vlm-ocr", help="OCR with LM Studio vision model")
    add_common_convert_args(vlm_parser)
    add_vlm_args(vlm_parser)

    convert_parser = subparsers.add_parser("convert", help="Convert with selected engine")
    add_common_convert_args(convert_parser)
    convert_parser.add_argument("--engine", choices=["docling", "vlm"], default="docling")
    add_vlm_args(convert_parser)

    return parser


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "doctor":
        return doctor(args.api_base, args.model, args.check_lmstudio)

    pdf_path = require_pdf(args.pdf)
    output_path = Path(args.output).expanduser() if args.output else default_output_path(pdf_path)

    engine = args.command
    if args.command == "convert":
        engine = args.engine

    if engine == "docling":
        markdown = convert_with_docling(pdf_path)
    elif engine == "vlm-ocr" or engine == "vlm":
        markdown = convert_with_vlm(
            pdf_path=pdf_path,
            api_base=args.api_base,
            model=args.model,
            dpi=args.dpi,
            timeout=args.timeout,
            start_page=args.start_page,
            end_page=args.end_page,
        )
    else:  # pragma: no cover - argparse prevents this
        raise CliError(f"Unsupported engine: {engine}")

    write_text(output_path, markdown)
    return {
        "input": str(pdf_path),
        "output": str(output_path),
        "engine": engine,
        "chars": len(markdown),
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except CliError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    emit_result(result, getattr(args, "format", "text"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
