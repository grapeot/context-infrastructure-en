# Public Skill Ecosystem

The `rules/skills/` directory shipped with `context-infrastructure-en` is a starter set: it demonstrates how skills should be organized, indexed, and invoked. More complete capabilities should not be copied into this repo. Instead, install them through independent public skill repos. Two benefits: each skill repo keeps its own README, CLI, tests, and release cadence; and private aliases, paths, tokens, and business context in your workspace stay in a local overlay, never mixed into a public repo.

This page is for both humans and AI. Humans can use it to discover what else is installable. AI can use the install protocol below to wire a public skill repo into a target workspace.

## Install Protocol

Give this paragraph, along with the target repo URL, to your coding agent:

```text
Install this public skill repo into my workspace:
<GitHub URL>

Start from my workspace AGENTS.md or CLAUDE.md. Follow any WORKSPACE.md or skills/INDEX.md routing rules. Clone or vendor the repo under an appropriate project directory. Expose exactly one root skill to my global skill index or agent instructions. Keep private aliases, local paths, credentials, endpoint defaults, and business context in a local overlay, not in the public repo.
```

After installation, the workspace typically forms two layers: the public repo handles generic technical contracts, and the local `rules/skills/` or `.env` handles private configuration. For example, the iMessage public repo only provides a send-only CLI — the local overlay stores contact aliases. The Stripe public repo only provides read-only analysis contracts — the local overlay stores business attribution.

## Recommended Public Skill Repos

| Domain | Repo | Capability |
|---|---|---|
| Web search | [tavily-skill](https://github.com/grapeot/tavily-skill) | Tavily search/extract CLI, stable JSON output for agents |
| Documents | [gdocs-skill](https://github.com/grapeot/gdocs-skill) | Google Docs create, search, modify, share; Markdown and tab support |
| Maps / travel | [google-maps-routing-skill](https://github.com/grapeot/google-maps-routing-skill) | Google Maps Routes + Geocoding CLI; address resolution, real-time drive time, leave-by planning |
| Email | [outlook_skill](https://github.com/grapeot/outlook_skill) | Outlook.com mail download, archive, Markdown rendering, send, calendar invites |
| Email | [resend_email_skill](https://github.com/grapeot/resend_email_skill) | Resend custom-domain sending, inbox reading, Markdown export, attachment inspection |
| Email / newsletter | [kit-skill](https://github.com/grapeot/kit-skill) | Kit Broadcast CLI for Markdown newsletters, with dry-run, draft-only, web-only, and tag/segment targeting; account defaults stay in local overlays |
| Messaging | [imessage_skill](https://github.com/grapeot/imessage_skill) | macOS iMessage send-only CLI; contact aliases in local overlay |
| Agent operations | [opencode_skill](https://github.com/grapeot/opencode_skill) | OpenCode `submit` / `submit --dry-run` / batch submission, recurring cron workflow, SQLite data maintenance and archive |
| Agent operations | [process-launcher](https://github.com/grapeot/process-launcher) | Local HTTP process launcher for TCC / GUI permission bridging, durable one-shot delayed jobs, process logs and cancellation |
| Usage analytics | [ai_usage_dashboard](https://github.com/grapeot/ai_usage_dashboard) | Multi-platform AI token usage, cost estimation, local dashboard, E1002 JSON |
| Social / growth | [typefully-twitter-skill](https://github.com/grapeot/typefully-twitter-skill) | Typefully posting, account metrics, X/Twitter single-post analytics |
| Community publishing | [circle-post-skill](https://github.com/grapeot/circle-post-skill) | Circle community Markdown conversion, dry-run preflight, publish/update/delete CLI; community defaults in local overlay |
| Payments / growth | [stripe-skill](https://github.com/grapeot/stripe-skill) | Stripe read-only finance / sales analytics, live tests default opt-in |
| Media | [online-media-skill](https://github.com/grapeot/online-media-skill) | Online media download, ASR artifact, query pack, source identification workflow |
| Slides | [pptx.skill](https://github.com/grapeot/pptx.skill) | AI-first PPTX read, edit, and render |
| Images | [image-generation-skill](https://github.com/grapeot/image-generation-skill) | Gemini Flash / Gemini Pro / GPT-Image-2 text-to-image, image editing, resolution upscaling |
| Images | [tiff-icc-profile](https://github.com/grapeot/tiff-icc-profile) | Embed ICC profiles into untagged TIFFs, commonly used in DaVinci still workflows |
| Health | [health-quantification](https://github.com/grapeot/health-quantification) | Apple Health / manual records → SQLite → CLI → AI analysis |
| Home network | [firewalla-local-skill](https://github.com/grapeot/firewalla-local-skill) | Firewalla local export analysis, device/flow reports, and redacted artifact workflow; home network details stay in local overlays |
| Coffee | [roest-analysis](https://github.com/grapeot/roest-analysis) | Roest roast log capture and analysis |
| Intake | [intake-skill](https://github.com/grapeot/intake-skill) | Voice memos / intake workflow public-ready skill |
| Testing | [playwright-test-skill](https://github.com/grapeot/playwright-test-skill) | CDP step-by-step debugging CLI for AI agents writing Playwright E2E tests |

## Selection Principles

If a capability needs a full CLI, tests, fixtures, or long-term maintenance, make it an independent repo. `context-infrastructure-en` only links to it, never copies it. This lets users install on demand without turning the starter workspace into a giant tool collection.

If a capability is a general working method — deep research, parallel subagents, analytical writing, skill authoring, project scaffolding — it can stay in this repo's `rules/skills/`. These files are core to the reference implementation; they are readable and modifiable right after cloning.

If a capability depends on private data, private accounts, or business context, put the generic part in a public repo and the private part in the user's own workspace overlay. Never write real contacts, servers, paths, API keys, customer names, transaction data, or usage records into a public repo.
