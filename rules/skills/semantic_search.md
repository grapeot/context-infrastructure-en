# Semantic Search Skill

## 1. Skill Overview

`semantic-search` is a general-purpose semantic search tool that indexes local text files and supports natural language queries. It goes beyond keyword matching to understand semantic relationships, suitable for any scenario requiring meaning-based retrieval from large text collections.

The most typical use case is searching grapeot's personal knowledge base (blog posts, daily records, survey reports), but the tool is not limited to this. `--file-list` can point to any text file collection: chat logs, third-party documents, research materials, code comments, etc.

For grapeot's knowledge base, this is the core tool for retrieving deep preferences and personal philosophy — the key infrastructure for AI Heartbeat Step 2 (Reflection Layer).

### 1.1 When to Use

**Scenario A: Search grapeot's knowledge base (most common)**
- **Deep background mining**: Understand grapeot's evolving views on a topic (e.g. "Agentic AI", "astrophotography").
- **Associative thinking**: Find historical experiments, essays, or reflections relevant to the current task, even when keywords don't match exactly.
- **Decision support**: Retrieve past postmortems or design discussions to inform current architecture decisions.
- **Disambiguation**: When grapeot mentions an ambiguous concept, find the most relevant historical definition.
- **Building Axioms / Digital Twin**: When crystallizing axioms or deep reflections, semantic search must run first to align with historical understanding.

**Scenario B: Analyze arbitrary text collections**
- **Third-party content analysis**: Search chat logs, interview transcripts, meeting notes by topic (e.g. "find all discussions by person X about AI").
- **Research material mining**: Run semantic search across a batch of downloaded documents/reports to find relevant passages that keyword search would miss.
- **Cognitive profile extraction**: Extract patterns from large conversation datasets by dimension (technical views, values, methodology).
- **Cross-document theme discovery**: Find semantically related but differently worded content across heterogeneous text collections.

### 1.2 Trigger Recommendations

**Proactive triggers (must execute)**:
- When building axiom documents under `rules/axioms/`
- When a task involves the user's core values, methodology, or philosophical framework
- When you need to understand the user's "intellectual evolution" in a domain
- When doing reflection-layer work (crystallizing axioms, deep postmortems)
- When you need to extract information by topic or semantic dimension from large text collections (not limited to grapeot's content)

**Passive triggers (user explicitly requests)**:
- "Search my previous thoughts on X"
- "Find any relevant background material"
- "Summarize my thinking on topic Y"
- "How did I solve similar problems before?"
- "Find X-related content in this batch of chat logs / documents"
- "Analyze person Y's views on topic Z"

---

## 2. Usage

### 2.1 Core Command

```bash
python tools/semantic_search/main.py \
    --file-list tmp/search_files.txt \
    --query "<natural language query>" \
    --top-k 10 \
    --cache-dir .knowledge_cache
```

### 2.2 Parameter Conventions

- `--file-list`: Required. Points to a text file containing paths to search. Place in `tmp/`.
- `--query`: Required. A complete, descriptive sentence. For example, "grapeot's latest thinking on the core tension in Agentic AI" is better than "Agentic AI".
- `--top-k`: Optional. Number of relevant snippets to return. Default 5; recommend 10 for broader context.
- `--cache-dir`: Must specify `.knowledge_cache` (workspace root) to reuse precomputed embeddings for faster response.

### 2.3 Cache Warmup

To pre-index yage.ai/share archived articles and Outlook email Markdown into `.knowledge_cache`, use the wrapper to generate a file-list and submit it to Process Launcher. This wrapper calls the existing `tools/semantic_search/main.py` without rewriting index logic, so it reuses the same 50-file batch save and mtime-based skip mechanism.

Dry-run first to see source counts, file-list path, and the JSON payload for the launcher:

```bash
.venv/bin/python tools/semantic_search/warmup_cache.py --mode dry-run
```

After confirming, submit the background job:

```bash
.venv/bin/python tools/semantic_search/warmup_cache.py --mode submit
```

Default scan targets three explicit directories, not the entire workspace:

- `adhoc_jobs/yage_share/md_archived/*.md`
- `adhoc_jobs/outlook_skill/data/mail/markdown/*.md` (`mail export-md` output)
- `adhoc_jobs/outlook_skill/data/mail/markdowns/*.md` (`mail render-markdown` output)

Generated file-lists go to `tmp/semantic_search_warmup/`, containing only paths, not email bodies. `tmp/`, `.knowledge_cache/`, and Outlook `data/` are all gitignored. Outlook local email Markdown, SQLite, and token caches are treated as sensitive data — do not commit to git or copy to public directories.

After submission, check status and logs via Process Launcher:

```bash
curl -sf http://localhost:7997/processes/<pid>
curl -sf 'http://localhost:7997/processes/<pid>/output?tail=80'
curl -sf 'http://localhost:7997/logs/heartbeat?label=semantic_search_warmup&limit=20'
```

Use `--path-style absolute` if absolute paths are needed as cache keys. Default is relative paths, consistent with the common `find contexts/... > tmp/search_files.txt` usage in this skill.

---

## 3. Standard Workflow

1. **Prepare file list**: Filter knowledge base areas based on need (reference `rules/WORKSPACE.md`).
   ```bash
   mkdir -p tmp
   # Example: search blog posts and survey reports
   find contexts/blog/content contexts/survey_sessions -name "*.md" > tmp/search_files.txt
   ```
2. **Run semantic search**:
   ```bash
   source .venv/bin/activate
   export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
   python tools/semantic_search/main.py --file-list tmp/search_files.txt --query "..." --top-k 10 --cache-dir .knowledge_cache
   ```
3. **Analyze and synthesize**: Read search results (typically containing score, source_file, text), combine with metadata (date, category) for comprehensive analysis.
4. **Clean up**: Delete `tmp/search_files.txt` after the task.

---

## 4. Common Search Paths

When searching grapeot's knowledge base, prioritize these paths:
- `contexts/blog/content/`: In-depth technical articles and core thinking.
- `contexts/daily_records/`: Daily logs capturing the most authentic thought evolution.
- `contexts/survey_sessions/`: Deep research conclusions.
- `contexts/life_record/data/`: Life recording transcripts (daily summaries and meeting notes).
  - 2026 data: `contexts/life_record/data/<YYYYMMDD>/`
  - 2025 data: `contexts/life_record/data/2025/<YYYYMMDD>/`
  - Both daily summary `.md` and raw transcript `.csv` are searchable.
- `rules/skills/`: Methodology documentation.

These are common shortcut paths. `--file-list` can point to any text file collection, for example:

```bash
# Search life transcripts (2025 and 2026)
find contexts/life_record/data -name "*.md" -not -path "*/.venv/*" > tmp/search_files.txt

# Search WeChat chat logs
find contexts/wechat -name "*.csv" > tmp/search_files.txt

# Search all materials for a research project
find contexts/people/magong -name "*.md" > tmp/search_files.txt

# Search arbitrary temporary documents
ls adhoc_jobs/some_project/*.txt > tmp/search_files.txt
```

---
**Version**: 1.2.0
**Last updated**: 2026-03-15
