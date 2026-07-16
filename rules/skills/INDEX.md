# Skills Index

This index points to reusable Skills — tools, workflows, and best practices that AI can invoke.

- **To use a capability** → browse the categories below and find the corresponding skill file
- **To add a new skill** → reference existing file formats and add to the appropriate category
- **To install more tool-type capabilities** → see [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md), which lists public skill repos that can be installed separately

## Multi-Agent Capability Notes

The current harness supports dispatching multiple `functions.task` subagents in parallel via `multi_tool_use.parallel`. Do not use by default, but when encountering large, parallelizable, research-heavy, codebase-exploration-heavy tasks that need independent cross-validation, first read [Parallel Subagent Workflow](./workflow_parallel_subagents.md).

Quick judgment: subagents are suitable for parallel reading, independent exploration, adversarial review, fact-checking, and context window isolation; not suitable for single-point small tasks, strongly sequential tasks, or multiple agents writing to the same state or files simultaneously.

---

## Component Status

### Tier 1: Core (ready after clone)
- ✅ Rules framework (SOUL/USER/COMMUNICATION/WORKSPACE) — fill in and use
- ✅ Skills framework (this directory) — fill in and use
- ✅ Three-layer memory system — requires OpenCode + cron configuration

### Tier 2: Extended (requires additional configuration)
- ⚙️ Semantic Search — requires an OpenAI-compatible embedding endpoint (local or cloud); installation options are listed in [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)
- ⚙️ Share Report — requires SSH server or GitHub Pages
- ⚙️ Google Docs — requires Google OAuth
- ⚙️ Send Email — requires Gmail App Password
- ⚙️ Delayed Execution — starter fallback; for durable/AI delayed tasks, install Process Launcher + OpenCode Skill

### Tier 3: Standalone public skill repos (install as needed)
- 🔧 AI Session Export, ChatGPT/Codex OAuth, image generation, Tavily, Google Docs, Google Maps, Outlook, Resend, OpenCode, Process Launcher, PPTX, Typefully, Circle Post, Stripe, Firewalla, Smart Home, and other capabilities — see [`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)

### Legend
✅ = Ready to use in 15 minutes or less
⚙️ = Requires additional configuration; core functionality unaffected without it
🔧 = Standalone repo, install into your workspace as needed

---

## Category Index

### API Guide

Operational manuals for calling external systems or tools.

- [AI CLI Agent Practical Guide](./ai_agent_cli_guide.md) ✅ — CLI Agent design principles, tool comparison (Claude Code / Codex / OpenCode / Antigravity), file response patterns, and AI calling AI
- [Antigravity CLI File-Based Invocation](./antigravity_cli.md) ✅ — Use `agy --print` to run a Gemini agent; covers first-run installation, keyring/App authentication, sandbox boundaries, timeouts, file-based results, and run-record acceptance checks
- [Send Email Skill](./send_email.md) ⚙️ — Send email notifications via Gmail; requires App Password configuration
- [Share Report to Web](./share_report.md) ⚙️ — Convert MD reports to HTML and publish to your own server; returns URL
- [Google Docs Operations](./google_docs.md) ⚙️ — CLI tool: publish Markdown, create/search/modify/share documents
- [Growth Analytics](./growth_analytics.md) ⚙️ — Three CLIs to query website traffic (GA4), email subscriptions (Kit), Twitter engagement (Typefully)
- [Typefully Metrics CLI](./typefully_metrics.md) ⚙️ — Query Twitter impression, engagement, and followers data via browser session credentials
- [Typefully Post CLI](./typefully_post.md) ⚙️ — Create drafts, schedule, and directly publish tweets/threads via Typefully v2 API
- [Apple Compressor Skill](./compressor.md) ⚙️ — Local Apple Compressor CLI transcoding; custom preset paths, source file write-completion detection, batch submission and monitoring

### Workflow

Complete workflows for specific tasks.

- [Parallel Subagent Workflow](./workflow_parallel_subagents.md) ✅ — Execute multiple `functions.task` subagents in parallel using `multi_tool_use.parallel`
  - **Must-read**: before using parallel subagents for the first time, read this skill first
  - **Core criteria**: suitable for parallel reading, independent exploration, cross-validation, and context isolation; not suitable for strong sequential dependencies or shared state writes
  - **Correct parallelism**: must wrap multiple `functions.task` calls in `multi_tool_use.parallel` within the same message; calling them one by one is serial
  - Judgment criteria: the task hits at least 2 of: broad information surface, independent read tasks, independent judgment, high-value uncertainty, main thread needs to retain integration capability
  - Core parameters: parallelism ≤5, research overlap 30-50%, code overlap 0-20%
- [Deep Research Workflow](./workflow_deep_research_survey.md) ✅ — Multi-agent parallel + cross-validation (Phase 1-3 information gathering)
- [External-Facing Thesis Mining](./workflow_external_thesis_mining.md) ✅ — The judgment layer between research and drafting; combines Axioms, the Thesis Catalog, historical material, independent candidates, an AGY reader, and fresh critique to return `PROCEED` or `DO_NOT_WRITE_YET`
- [External Writing Workflow](./workflow_external_writing.md) ✅ — Turn material that passed the thesis gate into an external-facing analysis: reasoning architecture → AGY IC-1 structural draft → fresh AGY IC-2 natural-explanation rewrite → fresh AGY IC-3 voice QA → Manager Voice Pass
- [Internal Writing Workflow](./workflow_internal_writing.md) ✅ — Internal document writing for the user, shared-context collaborators, and future AI agents. Core principle is low decision friction: conclusions first, skimmable, inline evidence, easy navigation and verification, use diagrams when helpful to reduce cognitive load.
- [Cognitive Profile Extraction Workflow](./workflow_cognitive_profile_extraction.md) — Extract predictable cognitive axioms from unstructured conversation data
  - Applicable to: group chats, Slack, Discord, email, podcast transcripts, and any conversation data
  - Process: broad scan → deep validation → stress testing → finalization (≥3 rounds of dynamic iteration)
  - **Requires Opus model**: writing done by Opus personally, all research delegated + parallelized
- [AI-Generated Slide Deck Workflow](./workflow_presentation_slides.md) — Gemini rendering, Clean Ink style, 8-process parallel, pre-4K upscale validation
- Semantic Search Skill → see [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md): local-text embedding + cosine similarity search with any OpenAI-compatible endpoint
- [Knowledge Flywheel Design Pattern](./workflow_knowledge_flywheel.md) — Dumb data + dumb methods + dumb models = refined knowledge
- [Video Download and Speech Recognition Workflow](./workflow_bilibili_whisper_transcription.md) — Bilibili/YouTube video processing
- [Delayed Execution Skill](./delayed_execution.md) ⚙️ — Low-risk `sleep + nohup` fallback; for durable/AI delayed tasks, see ecosystem's Process Launcher + OpenCode Skill
- [Project Scaffold](./project_scaffold.md) ✅ — Upgrade a loose directory into a standard project structure: `docs/`, `src/`, `scripts/`, `tests/`, `AGENTS.md`, and independent git
- [AI Session Search & Archive](./ai_session_search_archive.md) — Search unified OpenCode, Claude Code, Codex, Antigravity, and Second Mind Markdown archives with source routing, lexical-first retrieval, and semantic fallback

### Best Practice

General best practices and lessons learned.

- [External Article Prose and Rhetoric Guide](./bestpractice_external_prose.md) ✅ — Word-choice correction, metaphor restrictions, and long-form prose guidance for external articles and blog posts
- [Analytical Perspectives for External Articles (Thesis Catalog)](./reference_writing_thesis_catalog.md) ✅ — L1-L8 analytical perspectives and related axiom mappings
- [Internal Document Layout and Adaptive Visual Components Guide](./bestpractice_internal_visuals.md) ✅ — Adaptive HTML cards, theme variables, dark-mode compatibility, and visual component rules for internal memos, RFCs, and weekly reports
- [Core AI Programming Methodology](./bestpractice_ai_programming_mindset.md) ✅ — 70% problem, success criteria, verifiability
- [Skill Writing Guide (Meta-Skill)](./bestpractice_skill_writing.md) ✅ — Use when creating or rewriting skills; emphasizes outcome determinism, acceptance criteria, and boundary conditions
- [API Key Management](./bestpractice_api_key_management_1password_cli.md) ✅ — Securely manage keys using 1Password CLI
- [Interview Evaluation Framework](./bestpractice_interview_evaluation.md) ✅ — Trait > Skill, AI cheating detection, technical depth probing
- [Markdown to HTML Best Practice](./bestpractice_markdown_html_conversion.md) ✅
- [PDF to Markdown](./bestpractice_pdf_to_markdown.md) ✅ — Default to Docling; avoid MarkItDown / PyMuPDF4LLM / Marker for PDF scenarios due to quality or licensing issues
- [Temporal Information Verification](./bestpractice_temporal_info_verification.md) ✅ — Verify information that may exceed knowledge cutoff
- [Staged Approach](./bestpractice_staged_approach.md) ✅ — Isolate-process-verify closed loop; Dry Run before destructive operations
- [GUI Automation Methodology](./bestpractice_gui_automation.md) ✅ — Turn interfaces without APIs into programmable interfaces
- [AI-Assisted Debugging Diagnosis](./bestpractice_ai_debugging_diagnosis.md) ✅ — Root cause diagnosis decision tree for "code won't fix"
- [Mac Universal Clipboard Reset](./mac_universal_clipboard.md) ✅ — Reset `useractivityd` / `sharingd` / `pboard` when Mac and iPhone/iPad clipboard syncing breaks
- [AI Product Design Principles](./bestpractice_ai_product_design.md) ✅ — Linear chat vs knowledge work, perception-rule decoupling
- [Product/Technical Decision Reverse Engineering](./bestpractice_product_decision_analysis.md) ✅ — Analyze product or technical decisions from design space, constraints, and trade-offs
- Playwright E2E Testing Methodology → see [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md): CDP step-by-step debugging CLI + E2E methodology, CLI `pw-test`

---

## How to Add Your Own Skill

Before creating or rewriting a skill, read [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md). It explains how to define a skill using goals, acceptance criteria, available resources, and output specifications, rather than writing a skill as a mechanical step list.

File naming suggestion: use `<category>_<name>.md`, e.g., `workflow_my_process.md`, `bestpractice_my_insight.md`. After writing, add an entry under the corresponding category in this INDEX to ensure future agents can find it.

## Progressive Disclosure

Skills follow the principle of progressive disclosure:
- **INDEX.md** provides an overview for quick navigation
- **Specific skill files** contain complete operational steps and examples
