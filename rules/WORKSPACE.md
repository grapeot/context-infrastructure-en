# WORKSPACE.md — Directory Routing Quick Reference

Goal: let the AI know "where to find / put what" in every session. **Check here before searching for any file.**

## Routing Rules

### Projects and Code
- Write code / run scripts / one-off projects: `adhoc_jobs/<project>/`
- Tool scripts (email, semantic search, share reports, etc.): `tools/`
- Scheduled jobs: `periodic_jobs/`

### Knowledge and Records
- General research reports: `contexts/survey_sessions/`
- Thoughts / retrospectives / methodology: `contexts/thought_review/`
- Daily logs: `contexts/daily_records/`
- AI session archive: `contexts/ai_sessions/<source>/` (generated with ai_session_export; search workflow at `rules/skills/ai_session_search_archive.md`)

### System and Rules
- Reusable technical solutions / Skills: `rules/skills/`
- Core axioms: `rules/axioms/`
- Memory system: `contexts/memory/` + `periodic_jobs/ai_heartbeat/`

## Naming Conventions
- Directory and file names: lowercase + underscores (snake_case)
- Temporary one-off projects: `tmp_<name>/`

## Python Environment
- Root `.venv/` is the workspace-level environment; manage dependencies with `uv pip install`
- When isolation is needed, create a separate environment at `adhoc_jobs/<project>/.venv/`

## Quick Reference

<!-- As your project grows, add active project quick-routes here -->
<!-- Format: - `project-name` → `adhoc_jobs/project_name/` (description) -->
