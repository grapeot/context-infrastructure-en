# External Writing: Visuals, Verification, and Delivery Guide

> [!NOTE]
> **Applicable Phase**: To be read and used by the **Manager** during the **Image Freeze**, **Acceptance**, and **Delivery** phases.
> The permission boundaries and delivery contracts involved in this document are always governed by Section 0 of the [External Writing and Drafting Workflow](./workflow_external_writing.md). This guide only provides specific stage execution details and does not grant the Manager any authority to modify the final text.

## Image Contract and Specifications

Images in the article must actively reduce the reader's cognitive burden, rather than serving merely decorative purposes. Articles shorter than 2,000 words must contain at least one image; articles of 2,000 words or longer typically require 2 to 3 images.

- **Formats and Sources**: Final images embedded in the text must be generated or redrawn using image generation or redrawing tools available in the current workspace, and must use PNG, JPG, or WebP formats supported by the target channel.
- **Draft Redrawing**: Structural sketches exported from coding tools, flowchart tools, or presentation tools may only serve as inputs for redrawing; they must never be directly referenced in the final Markdown delivery file.
- **Data Compliance**: Quantitative charts must first establish their data structure through verifiable data processing methods before being handed over to workspace image generation or redrawing tools for visual redraw, ensuring data accuracy.
- **Visual Style**: The default style uses a light background, low saturation, and a clean research report design. Avoid neon effects, glowing shadows, and purely decorative elements containing no actual information.
- **Dimensions and Size**: Images must be compressed to JPG or WebP formats, with the long edge restricted to a maximum of 1024 pixels, and the file size kept under 200 KB. Embedding images in base64 format in the text is prohibited.
- **Workflow Milestones**: Image filenames, relative paths, placement in the text, and the semantic intent of each image must be frozen before IC-3 starts. IC-3 writes the final alt text and image references from that intent. Afterward, the Manager may only copy the image files to the target directory and must never modify the Markdown image paths or alt text.

## Deterministic Regression Checks

**Deterministic scans are diagnostic only: regex matches do not automatically equal errors and never authorize the Manager to modify the text.** When a match occurs, the Manager should make a semantic judgment based on context. If the match indeed represents a comprehension or quality issue, the Manager should record it in the audit report as a blocking issue (BLOCKER) and trigger the next round of IC-3.

Example commands for regression scanning are as follows:

```bash
# Internal scaffolding or metadata leaks
rg -n 'L[0-8]|axiom|Phase [A-Z]|Thesis Catalog' <candidate>

# Em dashes prohibited by the prose guide
rg -n '—' <candidate>

# Evaluative intensifiers and meta-commentary; review each hit in context
rg -ni '\b(very|clearly|obviously|notably|importantly)\b|specifically|next we|it is important to note|clearly shows' <candidate>

# Image references and alt text format
rg -n '!\[[^\]]+\]\([^\)]+\)' <candidate>

# Unexpected Chinese output in an English article
rg -n '[\x{3400}-\x{4DBF}\x{4E00}-\x{9FFF}]' <candidate>

# Mechanical adjective stacks that hide actors and sequence
rg -ni '\b(waitable|rejectable|resumable|recoverable|traceable|verifiable)(,| and)\s*(waitable|rejectable|resumable|recoverable|traceable|verifiable)' <candidate>
```

In addition, the Manager must mechanically check the consistency of numbers, links, image paths, and the sequence of subheadings (H2) between the candidate text and the source pack. Under no circumstances should text that has not passed the regression checks be considered accepted.

## Archiving Protocol

Archiving operations must strictly adhere to the following steps:

1. **Select Candidate Version**: Select a complete candidate text from historical drafts that has passed all gate inspections.
2. **Execute Direct Copy**: Copy the file directly to the final delivery path. During this copy, no template replacement, path correction, or formatting adjustments are permitted.
3. **Verify Consistency**: Run `cmp -s <agy_candidate> <final_md>` in the terminal to compare the files, or calculate their SHA-256 hashes to ensure they are byte-for-byte identical.
4. **Handle Discrepancies**: If there is any discrepancy, the delivery is deemed a failure. You must re-execute the direct copy and are strictly prohibited from manually modifying or patching the differences.
5. **Verify Visuals**: Verify that the final image files exist in the target directory, are correctly formatted, conform to size and dimension specifications, and that all relative Markdown image paths resolve correctly.
6. **Trigger Client Rendering**: Use the `read` tool to read enough content from the beginning of the final Markdown file to cover the entire text, ensuring a successful render is triggered in the client.

## Final Delivery Checklist

Before announcing that delivery is complete, the Manager must confirm that all of the following conditions are met:

- The final Markdown file is byte-for-byte identical to the accepted candidate text.
- All links, image paths, and local paths in the text resolve correctly.
- The latest audit report status is PASS, and no unresolved blocking issues remain.
- All temporary prompts, session logs, source packs, and audit reports are retained in the temporary directory and not uploaded to the public directory.
- The final response to the user provides the specific file paths and lists any known residual risks.
- No publication actions (such as blog deployment, social media posting, or email distribution) are executed without new, explicit user authorization.
