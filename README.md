# Context Infrastructure — Reference Implementation (English Version)

> Chinese version: [https://github.com/grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure)
>
> Background reading: [Why AI Only Says Correct But Useless Things — and How to Push It Out of Its Comfort Zone](https://yage.ai/context-infrastructure.html)

This is the complete structure of a context infrastructure system that has been running for a year. Its main value is as a reference implementation: you can see what the system looks like, how data flows, and how memory accumulates.

**Core positioning**: This is not a plug-and-play tool. It is a blueprint you can study. After cloning, you can immediately experience the difference between "with context" and "without context." But to make AI truly your own, you need to collect your behavioral data from scratch. There is no shortcut.

---

## Quick Start (5 minutes)

```bash
git clone https://github.com/grapeot/context-infrastructure-en
cd context-infrastructure-en
# Open this directory with Claude Code / OpenCode / Cursor
```

Then open [`rules/USER.md`](rules/USER.md) and fill in your basic information. This is the highest-ROI step: AI behavior becomes personalized immediately.

Detailed steps in [`setup_guide.md`](setup_guide.md).

If you want to extend this into a more complete working system, see [`docs/SKILL_ECOSYSTEM.md`](docs/SKILL_ECOSYSTEM.md). It lists independently installable public skill repos: web search, Google Docs, Google Maps, email/newsletter, OpenCode, PPTX, social media, payment analytics, home network analysis, and a local process launcher. `context-infrastructure-en` stays lightweight; full capabilities are installed on demand through separate repos.

---

## Directory Structure

```
context-infrastructure-en/
├── AGENTS.md                    # Root routing table (AI's starting point for every session)
├── setup_guide.md               # Setup instructions
├── .env.example                 # Environment variable template
│
├── docs/
│   ├── CRONTAB.md               # Cron job configuration guide (timeline + example crontab)
│   └── SKILL_ECOSYSTEM.md       # Directory of independently installable public skill repos
│
├── rules/
│   ├── SOUL.md                  # AI identity and behavioral baseline (template)
│   ├── USER.md                  # Your preferences and background (template)
│   ├── COMMUNICATION.md         # Communication style guide (ready to use)
│   ├── WORKSPACE.md             # Directory routing index
│   ├── axioms/                  # 43 decision axioms (demonstration layer)
│   └── skills/                  # 25+ reusable skills (demonstration layer)
│
├── contexts/
│   ├── memory/
│   │   └── OBSERVATIONS.md      # L1/L2 layers of the three-tier memory system
│   ├── survey_sessions/         # Research report storage
│   ├── daily_records/           # Daily record storage
│   └── thought_review/          # Thought review storage
│
├── periodic_jobs/
│   └── ai_heartbeat/
│       ├── docs/
│       │   ├── PRD.md           # Memory system design document
│       │   └── KNOWLEDGE_BASE.md # Observation and reflection SOP
│       └── src/v0/
│           ├── observer.py      # Daily observation script (requires cron setup)
│           └── reflector.py     # Weekly reflection script (requires cron setup)
│
├── tools/
│   └── share_report/            # Report publishing (Tier 2)
│
└── adhoc_jobs/                  # On-demand task storage
```

> Semantic search is now a standalone public skill repo: [semantic-search-skill](https://github.com/grapeot/semantic-search-skill), no longer under `tools/`.

---

## Three-Layer Structure

**Demonstration layer (study, don't copy)**: [`rules/axioms/`](rules/axioms/) and [`rules/skills/`](rules/skills/) contain what this system has accumulated over a year. The 43 axioms were distilled from concrete experiences; the skills were summarized from real projects. These represent the original author's perspective. They are useful as reference but cannot replace what you accumulate yourself.

**Reusable layer (use directly)**: [`rules/SOUL.md`](rules/SOUL.md) and [`rules/USER.md`](rules/USER.md) are templates. Fill them in and they work. [`rules/COMMUNICATION.md`](rules/COMMUNICATION.md) is a general communication style guide that most people can adopt as-is. [`periodic_jobs/ai_heartbeat/`](periodic_jobs/ai_heartbeat/) provides the memory system implementation. For cron job setup, see [`docs/CRONTAB.md`](docs/CRONTAB.md).

**Non-reusable layer**: The specific content of axioms and the concrete experiences behind skills. Understand their structure and how they were formed, then accumulate from your own data.

---

## License

MIT
