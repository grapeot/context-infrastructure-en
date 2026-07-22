# Project Scaffold Skill

Upgrade a temporary directory, loose script directory, or structurally incomplete small project into a standard project form suitable for long-term maintenance.

**Trigger words**: "bootstrap a project", "scaffold a project", "organize this directory into a project", "fill in PRD/RFC/working", "create a separate git repo for this directory"

---

## 1. Applicable Scenarios

When a directory is no longer a one-off script but will be repeatedly modified, needs multiple rounds of AI handoff, needs testing, and needs frequent commits, it should be upgraded to a standard project structure.

Typical signals:

- The directory already has 2+ scripts/modules
- The user explicitly requests supplementing docs, adding tests, frequent commits
- It will continue to iterate in the future, not just a one-time task
- It needs independent git history and can't stay mixed in the workspace monorepo

---

## 2. Public/Private Repo Intake Gate

**Before touching the directory structure, one thing must be confirmed: will this repo be published to public GitHub in the future?**

Because privacy, skill splitting, `.env.example` handling, and fake fixtures all depend on this answer. If scaffolding is already complete before discovering it's a public repo, the cost of going back to fix things is much higher.

### Confirmation Method

At the start of scaffolding, ask the user:

> Will this repo be published to public GitHub in the future, or only used in your own workspace/private Git?

Options: `public (will open-source/publish to GitHub)` / `private (local use only)`.

Don't skip this step. If the user doesn't say, ask.

### Mandatory for Public Repos

If confirmed as a public repo, the following are mandatory requirements, not optional optimizations:

1. **`.gitignore` must block private files**. At minimum cover `.env`, `.env.*` (keep `!.env.example`), `__pycache__/`, `.pytest_cache/`, `*.pyc`, `dist/`, `build/`, `*.egg-info/`, local data directories, log directories. For Python projects, add `py.typed` marker.

2. **Must create `.env.example`**. All environment variables use fake placeholders, never leave them empty. Env vars required for live tests must be listed in `.env.example` with fake values, matching the form of a real `.env` so it can be copied and used directly.

3. **All public files use fake handles / domains / keys**. `README.md`, docs, tests, fixtures, scripts must not contain real email addresses, phone numbers, API keys, internal paths, server addresses, or 1Password vault references. Common fake placeholders:
   - Email: `alice@example.com`, `bob@example.net`
   - Phone: `+15555550123` (North American test number range)
   - API key: `replace-with-your-real-key`
   - 1Password: `op://your-vault/your-item/your-field`
   - Domain: `example.com`, `example.org`

4. **README must declare publishability**. In the README's Privacy section, write clearly: `This repository is designed to be publishable with only fake examples.`

5. **If the project contains skills**, they must be split into two layers. The public repo holds the technical implementation (CLI, tests, API contract, skill workflow docs); private contacts, private routes, and private handles go in the workspace global skill directory (e.g., `rules/skills/`) or private `.env`. The public repo's skill docs must state clearly "where to find private aliases." Reference the split approach of `adhoc_jobs/resend_email_skill/` (public technical skill) and `rules/skills/imessage.md` (private contact routing).

   Public skill repos should assume loose Markdown-based installation, not vendor-specific skill packaging. The README must explain how a human can hand the GitHub URL to Codex, Claude Code, Cursor, OpenCode, or another coding agent and ask it to install the skill. The AI installer should start from the target workspace's `AGENTS.md` or `CLAUDE.md`, follow any routing file such as `WORKSPACE.md`, and then add the public repo's root skill to the workspace discovery chain. If the workspace has `rules/skills/INDEX.md` or `skills/INDEX.md`, update that index; otherwise add a short pointer in `AGENTS.md` or `CLAUDE.md`.

   If the public repo contains multiple skills, expose exactly one root/router skill to the global workspace level. Use that root skill to link to focused local files inside the repo. Do not symlink every focused skill globally; that makes discovery noisy and makes private/public overlays harder to reason about.

6. **Privacy scan after completion**. In the final verification phase (Phase 4), must run a privacy scan:

   ```bash
   rg -n "real email pattern|real phone number range|internal path|op://" .
   ```

   Zero matches to pass. If matches are found, fix each one and scan again.

### Private Repo Handling

If confirmed as a private repo, fake fixtures and privacy splitting are not required. Normal `.env.example` and `.gitignore` are still recommended, but fake placeholders are not mandatory.

---

## 3. Target Structure

Minimum recommended structure:

```text
project_root/
├── AGENTS.md
├── .gitignore
├── .env.example        # mandatory for public repo; recommended for private repo
├── docs/
│   ├── prd.md
│   ├── rfc.md
│   ├── working.md
│   └── test.md
├── src/
├── scripts/
├── tests/
└── <compat wrappers / entrypoints if needed>
```

### Responsibilities of Each Directory/File

- `docs/prd.md`: covers goals, users, requirements, success criteria
- `docs/rfc.md`: covers architecture, boundaries, key design decisions, migration strategy
- `docs/working.md`: two sections
  - `## Changelog`: one date heading per day, simple bullets below recording what was changed that day
  - `## Lessons Learned`: record pitfalls, constraints, mistakes that subsequent agents should not repeat
- `docs/test.md`: testing strategy, clearly state unit / integration / e2e coverage targets
- `src/`: reusable source code, prefer modules, don't put user-facing shell entrypoints here
- `scripts/`: CLI, shell entrypoints, ops scripts that users run directly
- `tests/`: unit tests, integration tests, future e2e
- `AGENTS.md`: local rules for this project, especially reminders to update `working.md`, commit frequently, and environment requirements

### Recommended Frontend/Backend Scaffold for Current Workspace

If the project is clearly a small-to-medium web application and the goal is to **quickly produce a runnable product first, then evolve incrementally**, the current workspace default recommendation is:

- **Backend**: FastAPI
- **Frontend**: React + Vite + TypeScript
- **Local storage**: prefer SQLite (unless the user explicitly requires a heavier database)
- **Production deployment**: first have FastAPI serve the frontend build artifacts directly

Recommended directory layout:

```text
project_root/
├── AGENTS.md
├── .gitignore
├── docs/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── start_backend.sh
│   ├── start_frontend.sh
│   └── build_frontend.sh
├── src/
│   └── <python package>
├── tests/
└── pyproject.toml
```

Supplementary notes:

1. `frontend/` independently maintains the React/Vite project
2. `src/` only contains the backend Python package; don't stuff backend logic into root-level scripts
3. `scripts/` provides stable entrypoints for humans and agents, avoiding guessing commands on the spot each time
4. Production mode prefers "FastAPI same-origin hosting of frontend build," so auth, prefix, and deployment paths stay consistent more easily

### At Minimum 3 Scripts for Frontend/Backend Projects

For FastAPI + React projects, the following should be provided by default:

1. `scripts/start_backend.sh`
   - Activate `.venv`
   - Set backend environment variables
   - Start `uvicorn`
2. `scripts/start_frontend.sh`
   - Set frontend dev environment variables
   - Start `npm run start_dev_server` or equivalent command
3. `scripts/build_frontend.sh`
   - Set build-time base path / token / api base variables
   - Execute `npm run build`

Don't just write these commands in the README. The scripts themselves are the contract.

### Default Recommendation for URL Prefix / Root Path

If the project may be mounted under a sub-path in the future (e.g., `/foo/bar`), the configuration source must be unified at the scaffolding stage.

Default recommendation:

- Use **one environment variable** to drive everything uniformly, e.g., `APP_ROOT_PATH`
- Backend reads it and maps to FastAPI `root_path`
- Frontend reads it and maps to Vite `base` and React Router `basename`
- `scripts/start_backend.sh`, `scripts/start_frontend.sh`, `scripts/build_frontend.sh` all derive their respective configs from this single variable

Don't let the backend, frontend, and reverse proxy each maintain three separate prefix strings. That will almost certainly break when deploying to a sub-path.

---

## 4. Recommended Execution Order

### Phase 0: Confirm Public/Private

Execute the Section 2 intake gate: ask the user whether this repo will be published to public GitHub in the future.

If the user answers public, the entire scaffolding process must carry public repo constraints (`.env.example` fake values, `.gitignore` blocking private files, all public files using fake handles, skills split into two layers). Don't finish and then go back to fix things.

### Phase 1: Confirm Project Boundaries

First determine three things:

1. Whether this directory is already worth becoming an independent project
2. Whether the user permits reorganizing the directory structure
3. Whether a separate nested git repo is needed

If the user has not authorized reorganizing an existing project structure, don't unilaterally do a major relocation.

### Phase 2: Build the Skeleton First, Then Migrate Code

Recommended order:

1. Create `docs/ / src/ / scripts/ / tests/`
2. Write `AGENTS.md`, `.gitignore`, `.env.example`
3. Write `prd.md` / `rfc.md` / `test.md` first
4. Then migrate code into `src/`, put executable entrypoints into `scripts/`
5. Finally supplement `working.md`
6. Register the new project's quick-route in `rules/WORKSPACE.md`. Include the names readers will use, the project path, and one-line purpose, for example: `weather monitor` / `weather_monitor` → `adhoc_jobs/weather_monitor/` (home weather-data collection and alerts).

Don't restructure code and improvise the directory layout at the same time. Build the skeleton first; subsequent changes will be more stable.

### Phase 3: Preserve Compatible Entrypoints

If external cron jobs, scripts, or user habit paths already exist, don't cut them on the first pass. Prioritize keeping compatible wrappers:

- Old paths kept as thin wrappers
- New logic goes into `src/` / `scripts/`

This way you can complete the refactoring first, then gradually migrate callers.

### Phase 4: Verification and Privacy Check

After all code and tests are complete, must run a round of verification in fixed order:

1. Lint (if the project has a linter configured).
2. Tests: run default offline tests first, then opt-in integration tests (if any).
3. Public repos must run a privacy scan:

   ```bash
   rg -n "real email|real phone number|internal server|op://|private key pattern" .
   ```

   Zero matches to pass. If matches are found, fix each one and scan again.

4. Write verification results into `docs/working.md`'s daily changelog, recording xxx passed / xxx skipped / xxx found and fixed.

Only when Phase 4 fully passes is scaffolding considered delivered.

---

## 5. Git Strategy

If the directory needs long-term maintenance and its history is unrelated to the workspace monorepo, prefer a separate `git init`.

Recommended commit split:

1. **scaffold commit**
   - docs/AGENTS/.gitignore/basic directories
2. **implementation commit**
   - actual code migration, modularization, tests
3. **validation commit**
   - `working.md` records, test results, backfill or manual verification results

Don't stuff a major refactoring, doc supplementation, test fixes, and history backfill all into one commit.

---

## 6. Minimum Content for AGENTS.md

The project-local `AGENTS.md` must at minimum cover:

1. Project structure description
2. `working.md` update requirements
3. Frequent commit requirements
4. This project's Python / Node / shell environment constraints
5. Any compatibility constraints that must not be broken

If this file isn't written, subsequent agents can easily rewrite the project back into a pile of temporary scripts.

---

## 7. working.md Maintenance Requirements

### Changelog

- One date heading per day
- Each bullet records only one change
- No nested bullet points
- No empty phrases like "did some optimizations"

### Lessons Learned

Only write content that genuinely helps subsequent agents avoid pitfalls, e.g.:

- Which files are compatibility wrappers and cannot be directly deleted
- Which output formats are contracts that external dependencies rely on
- Which local data sources look like primary data sources but are actually only auxiliary indexes

---

## 8. What test.md Should Cover

At minimum, explain:

- Which pure logic unit tests cover
- Which local data or services integration tests depend on
- Whether e2e exists; if not yet, clearly state why not
- What artifacts manual verification should inspect

The value of `test.md` is not repeating pytest commands, but letting subsequent agents know "what counts as verification complete."

---

## 9. Hard Rules When Reorganizing Existing Projects

1. Without user permission, don't unilaterally do large-scale directory relocation
2. Build the skeleton first, then move code
3. Preserve compatibility first, then remove old entrypoints
4. Update `working.md` after each staged completion
5. Each phase must have a runnable or verifiable state

---

## 10. One-Sentence Judgment Criterion

If a directory will continue to be modified in the future, and you want different AIs/people to be able to take over at low cost, then it should not remain in "loose script directory" state — it should be upgraded to the project skeleton above as soon as possible.

If this repo will be published to public GitHub in the future, Phase 0 must ask the user, and Phase 4's privacy scan cannot be skipped.
