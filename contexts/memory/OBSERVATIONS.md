# Memory Observations

This is the L1/L2 layer of the three-tier memory system. Daily observations are automatically written by `periodic_jobs/ai_heartbeat/src/v0/observer.py` and organized/distilled weekly by `reflector.py`.

## Format

Each date entry follows this format:

```
Date: YYYY-MM-DD

🔴 High: [methodology/constraint] description
🟡 Medium: [project status/decision] description
🟢 Low: [task log] description
```

### Priority Definitions

- **🔴 High**: Cross-project reusable lessons, hard constraints, major decisions affecting system architecture. Permanently retained. Candidate for promotion to axiom or skill.
- **🟡 Medium**: Key progress on active projects, technical decision context, information still needed for reference in the coming weeks.
- **🟢 Low**: Daily task log, transient debug records, temporary context. Periodically garbage-collected.

## How to Load Memory

Do not load this entire file (it may be large). Retrieve on demand:

```bash
# Search for a specific topic
grep -n "keyword" contexts/memory/OBSERVATIONS.md

# Search the last N days
grep -A 20 "Date: $(date -v-7d +%Y-%m-%d)" contexts/memory/OBSERVATIONS.md
```

Or use semantic search for cross-date semantic retrieval (install [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)).

---

<!-- Record area below, automatically appended by observer.py -->
