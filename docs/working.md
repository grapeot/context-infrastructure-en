# Working Log

## 2026-05-25

- Added three generic best-practice skills to the starter set: PDF-to-Markdown with Docling, GUI automation methodology, and product/technical decision reverse engineering.
- Redacted the PDF conversion skill's local report path so the public version stays workspace-neutral.

- Added a human- and agent-readable public skill ecosystem index at `docs/SKILL_ECOSYSTEM.md`.
- Linked the ecosystem index from `README.md`, `setup_guide.md`, and `rules/skills/INDEX.md` so users can discover standalone skill repos without loading every repo into the starter skill index.
- Kept the model as public repo + private workspace overlay: public repos hold generic CLI contracts and tests; local workspaces hold aliases, paths, endpoints, credentials, and business context.
- Updated `rules/skills/project_scaffold.md` with the public skill repo installation convention: loose Markdown-based install, one root/router skill per repo, and private overlays outside the public repo.
