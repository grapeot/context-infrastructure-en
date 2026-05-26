---
title: PDF 转 Markdown
category: BestPractice
tags: [pdf, markdown, docling, document-conversion]
difficulty: Easy
created: 2026-04-27
---

# PDF 转 Markdown

需要把 PDF 转成 Markdown（喂给 LLM、做内容提取、归档原始资料）时，**默认用 Docling**。

## 为什么是 Docling

OpenDataLoader benchmark 12 个 PDF→Markdown 引擎里 Docling 综合得分最高（0.882），表格和标题保真都最好。MIT 许可证，纯 Python，CPU 也能跑（约 3 秒/页），有 GPU 更快。

实测过的几类反例不要用：

- **MarkItDown**：底层是 pdfminer.six，标题层级保留率 0%，表格基本崩溃。Office 文档 OK，PDF 不行。
- **PyMuPDF4LLM**：速度最快但 AGPL，商用受限。
- **Marker**：质量接近 Docling 但 GPL，商用要付费。

如果你要在自己的 workspace 里保留引擎对比调研，把调研记录放在项目文档或 `contexts/` 下，并在本 skill 里链接到你的本地报告。

## 怎么用

```bash
uv pip install --python .venv/bin/python docling
```

```python
from docling.document_converter import DocumentConverter

conv = DocumentConverter()
result = conv.convert("input.pdf")
md = result.document.export_to_markdown()
```

首次调用会下载约 1 GB 模型权重到 HuggingFace 缓存，之后复用。同一个 `DocumentConverter()` 实例可以连续转多份，不要每份都新建。

## 验收

- 输出 Markdown 中表格用标准 `| ... |` 语法保留，列对齐
- 标题层级（`#`、`##`、`###`）和原 PDF 视觉层级一致
- 体积上：纯文字 PDF 一般 5–10x 压缩到 Markdown，纯扫描件不会显著变小

## 已知陷阱

**Section 标题被吞掉**。当 PDF 里某个标题是表格内的强调文字（不是真正的 layout heading），docling 可能识别成普通单元格。表现是连续两个 `## HOLDINGS` 中间没有账户名区分。处理方法：用上下文（账户编号、beginning balance）回查原 PDF 对应页，必要时手动补 section header。

**两份 PDF 内容相同但文件名不同**。如果两份转出来字符数完全相等，先 `md5` 比较原文件——很可能是上传时弄错了。docling 不会主动 dedupe。

**venv 里 pip 不存在**。在用 uv 创建的 venv 里通常没装 pip，`venv/bin/python -m pip install` 会报 `No module named pip`。改用 `uv pip install --python .venv/bin/python <pkg>`。

## 适用边界

不适用：

- 扫描件 / 图片 PDF：docling 自带 OCR 但精度不如专用 OCR。如果纯扫描件，先评估 Tesseract 或商业 API
- 复杂数学公式：导出 LaTeX 但保真度有限
- 需要保留页码、页眉页脚的归档场景：docling 默认会清掉这些
