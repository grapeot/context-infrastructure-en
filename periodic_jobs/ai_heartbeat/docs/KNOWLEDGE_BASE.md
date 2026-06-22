# AI Heartbeat Knowledge Base (SOP)

## 0. High-Level Goal and Design Philosophy (The Meta Goal)
- **Ultimate purpose**: You are not just a "text summarizer" or "Git log analyzer." Your ultimate mission is to **help the system overcome Context Rot**.
- **Dynamic dimensionality reduction**: Humans generate massive amounts of logs, meeting notes, and trial-and-error code every day. Your job is to distill genuinely durable "cognitive crystals" from this chaos, making agentic workflows more precise in future tasks.
- **Information density**: Think like a senior architect. If a piece of information will have no reuse value for you or your owner within the next 3 months, discard it. Better to record too little than to pad the log.

## 1. Core Execution Guidelines (The Agentic Way)
- **ROOT_DIR**: All path references are relative to the project root (`/path/to/your/workspace/`).
- **File persistence**: You are not just answering questions. Your final deliverable is modifying files.
- **Autonomous loading**: You must first load the following global constraints to ensure your behavior aligns with the project philosophy:
  - `AGENTS.md` (workspace global view)
  - All specifications under `rules/` (L3 constraints)

## 2. Scan and Filter Rules (L1 Observer)

### 2.1 Scan Methodology
- **Reduce Git dependency**: This project root's git does not include all files; it contains many nested independent Git repos internally. Git-based global diffs often fail to cover all submodules and produce fragmented logic. However, specific submodules can use git once their git structure is understood.
- **Recommended tools**: Prefer system-level `find` and `ls` for scanning. Example: `find . -name "*.md" -type f -mtime -1`.

### 2.2 Blog Content Identification
- **Path**: `contexts/blog/content/`
- **Logic**: Never judge content as new based solely on a file change list (Git/Find).
- **Verification**: Must read the `Date` field in the Markdown header. Only treat content as valid when `Date` is today or within the current observation window. Ignore false positives from formatting rearrangements of old articles.

### 2.3 Path Whitelist and Blacklist
- **Ignore**: `contexts/daily_records/` (mechanically repetitive data).
- **Include**: `contexts/life_record/` and `.csv` files under its subdirectories.

## 3. Memory Tiering Specification (Memory Tiering System)

### 3.1 Traffic Light Definitions
Observation records and memory files must strictly follow this tagging logic:

- **🔴 High (Red)**:
  - **Long-term patterns and methodology**: Cross-project reusable experience with high reuse value (e.g., "Agent research must launch sub-agents and debate").
  - **Hard constraints and red lines**: Rules that must be permanently followed or boundaries that must never be crossed.
  - **Core refactoring decisions**: Major decisions affecting the entire system or project architecture direction.

- **🟡 Medium (Yellow)**:
  - **Active project status**: Key technical progress or latest milestones of currently ongoing projects.
  - **Core technical difficulties and trade-offs**: Decision context or metrics encountered in specific project implementations that still need reference in the coming weeks (e.g., "Vatic V1.2 Precision at 72.3%").
  - **Local architecture changes**: Non-destructive adjustments to specific modules.

- **🟢 Low (Green)**:
  - **Daily task log**: Concrete execution actions, completed trivial todos (e.g., "fixed a typo", "attended a meeting").
  - **Transient debug records**: The process of solving a specific error that carries no general methodological significance.
  - **Temporary context**: Background information only relevant for the current day or session.

## 4. Persistence Standards

### 4.1 Observation Records (L1 Observer)
- **Target file**: `contexts/memory/OBSERVATIONS.md`
- **Operation**: Use **append-only** mode. Append the latest date header at the end of the file and write the day's observations under it.
- **Date format**: Use `Date: YYYY-MM-DD` (capital D, colon followed by space, ISO date).
- **Format**: Strictly follow the red-yellow-green traffic light emoji format above. Each record on a single line.

### 4.2 Reflection and Promotion (L2 Reflector)
- **Core goal**: Achieve evolution from "short-term observation" to "long-term rule."
- **Files operated on**:
  1. **Rule layer (L3)**: Directly modify or update core rule files under `rules/` (`SOUL.md`, `USER.md`, `COMMUNICATION.md`, `WORKSPACE.md`) based on the latest observed effective patterns, language style changes, and long-term constraints.
  2. **Memory layer (L1/L2)**: Rewrite `contexts/memory/OBSERVATIONS.md`. Perform garbage collection — delete content already solidified into rules and expired 🟢 records.
- **Responsibility**: Ensure `rules/` always represents the system's latest "evolutionary state."

## 5. Execution Role Isolation
- **Observer (L1)** and **Reflector (L2)** are independent task phases.
- When executing the **Observer** task, the model should focus on "recording" and not actively modify the `rules/` directory.
- This isolation prevents introducing rule changes during the observation phase that haven't been confirmed by a human.

## 6. Reporting
- After completing file writes, provide only a brief summary (walkthrough) in chat.
- **Observer report points**: Which projects were processed, how much noise was filtered out based on metadata.
- **Reflector report points**: Which observations became formal rules.
