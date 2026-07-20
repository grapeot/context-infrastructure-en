# Working Log

## 2026-07-20

- Updated the Antigravity CLI guide and quick reference for AGY 1.1.4: documented the top-level `agy --print` interface, rejected nonexistent `agy run` and JSON event flags, and added the new headless inheritance of persisted `settings.json` policies.
- Added `apple-photos-skill` to the public ecosystem for metadata inspection, retrieval, backup, guarded imports, and default-dry-run deletion workflows.
- Added `bright-horizons-photo-sync-skill` for resumable My Bright Day event and media backup with verified, deduplicated Apple Photos imports.
- Added `ai-session-profanity-rate` to the public ecosystem for cached sub-agent profanity-unit analysis over local AI-session user messages, with private local artifacts and redacted JSON/chart outputs.

## 2026-07-16

- Added `chat-gpt-oauth-skill` to the public ecosystem as an opt-in local ChatGPT Plus/Pro OAuth compatibility reference; documented that its private endpoint is unstable and not recommended for production.

## 2026-07-15

- Added the English AI Session Search & Archive workflow with source routing, lexical-first retrieval, fresh semantic-search file lists, freshness checks, and privacy-safe result rules.
- Added `ai_session_export` to the public ecosystem and documented a daily multi-source Session Sync covering OpenCode, Claude Code, Codex, Antigravity, and Second Mind.
- Added the private `contexts/ai_sessions/<source>/` route to the starter workspace map.

## 2026-07-12

- Added `genai_portrait_skill` to the public skill ecosystem for identity-preserving portrait, headshot, and ID-photo editing with photographic coherence.

## 2026-07-10

- Added `innovation-assistant-skill` to the public skill ecosystem as the Innovation capability for structured innovation pipelines (SIT + Think Bigger).

## 2026-06-06

- Added `google-maps-routing-skill` to the public skill ecosystem as the Maps / travel capability for Google Maps Routes + Geocoding CLI workflows.
- Updated README, setup guide, and starter skill index examples so Google Maps appears alongside other standalone public skill repos.

## 2026-05-25

- Moved image generation from built-in skill (`rules/skills/generate_image.md`, `tools/generate_image.py`) to independent public repo [`image-generation-skill`](https://github.com/grapeot/image-generation-skill). The starter repo now references it via `docs/SKILL_ECOSYSTEM.md` instead of shipping its own implementation.
- Removed `rules/skills/generate_image.md`, `tools/generate_image.py`, and `tools/tests/test_generate_image.py` from the starter set.
- Updated `rules/skills/INDEX.md` to point users to the ecosystem index for image generation.
- Added image-generation-skill row to `docs/SKILL_ECOSYSTEM.md`.

- Added three generic best-practice skills to the starter set: PDF-to-Markdown with Docling, GUI automation methodology, and product/technical decision reverse engineering.
- Redacted the PDF conversion skill's local report path so the public version stays workspace-neutral.

- Added a human- and agent-readable public skill ecosystem index at `docs/SKILL_ECOSYSTEM.md`.
- Linked the ecosystem index from `README.md`, `setup_guide.md`, and `rules/skills/INDEX.md` so users can discover standalone skill repos without loading every repo into the starter skill index.
- Kept the model as public repo + private workspace overlay: public repos hold generic CLI contracts and tests; local workspaces hold aliases, paths, endpoints, credentials, and business context.
- Updated `rules/skills/project_scaffold.md` with the public skill repo installation convention: loose Markdown-based install, one root/router skill per repo, and private overlays outside the public repo.
