# Google Docs Skill

Canonical skill: read `adhoc_jobs/gdocs_skill/docs/skill_google_docs.md` for the full CLI contract, commands, defaults, output format, and known caveats. This file contains only workspace-specific additions.

## Project location

`adhoc_jobs/gdocs_skill/` — work from this directory.

## Voice Recognition Contact Aliases

When sharing Google Docs or resolving spoken recipient names, voice input may produce homophone errors. Keep workspace-specific contact aliases here, not in the public `gdocs-skill` repo.

| Voice input variants | Email |
|---|---|
| `example teammate`, `example team mate` | `teammate@example.com` |
| `core team`, `project team` | `person-a@example.com`, `person-b@example.com` |

Replace these placeholders with your own contacts in your private workspace. Do not commit real personal contacts to a public reference repo.
