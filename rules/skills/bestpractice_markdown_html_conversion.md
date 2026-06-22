---
title: Markdown to HTML Best Practice
category: BestPractice
tags: [markdown, html, pandoc, document-conversion]
difficulty: Easy
related_projects: []
created: 2025-02-12
updated: 2025-02-12
---

# Markdown to HTML Best Practice and Lessons Learned

When converting carefully authored Markdown documents to HTML (especially using tools like Pandoc), we have summarized the following core lessons to ensure formatting accuracy and professionalism.

## 1. Strict Requirements for List Formatting

### Must Leave Blank Lines
Markdown converters (such as Pandoc) typically require a **complete blank line** between a list (unordered or ordered) and the paragraph above it.

- **Wrong approach**:
  ```markdown
  Applications of physiognomy in relationships:
  * Strength matching
  * Fortune matching
  ```
  *Result: the list may be recognized as plain text, causing bullet points to not display in HTML.*

- **Correct approach**:
  ```markdown
  Applications of physiognomy in relationships:

  * Strength matching
  * Fortune matching
  ```

## 2. Structural Integrity When Merging Chapters

### Line Breaks Between Chapters
When merging multiple Markdown files into one large document, you must insert **at least two line breaks** (i.e., one blank line) between files.

- **Reason**: if the previous file ends with text and the next file starts with a `#` heading without a blank line in between, the parser may confuse the heading logic.
- **Best practice**: explicitly add `\n\n` when merging with `cat` or scripts.

## 3. Logical Reorganization of Headings and Introductions

### Remove Redundant Headings
In ebooks or long tutorials, if each chapter has a separate `## Introduction` heading, it adds burden to the table of contents and appears visually fragmented.

- **Improvement suggestion**: remove the `## Introduction` text and place the introduction text directly after the chapter heading (`#`). This makes the reading experience smoother and more aligned with modern book typography.

## 4. CSS Details for Mobile Adaptation

### Spacing Management
Ensure the HTML `body` or main container has sufficient `padding` (recommended 24px or more) to prevent text from hugging the screen edge on mobile devices.

## 5. Standardization of Symbols and Brackets

### Heading Purity
In the final aggregated document, try to remove unnecessary brackets or special symbols from headings (such as `## 【Chapter Summary】`). Using concise `## Chapter Summary` is not only visually more professional but also helps the auto-generated table of contents (TOC) appear clean.
