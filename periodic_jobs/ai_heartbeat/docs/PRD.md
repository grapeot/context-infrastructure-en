# AI Heartbeat: Progressive Disclosure Memory System — Product Requirements Document (PRD)

## 1. Product Overview

### 1.1 Vision
Build an **agentic-driven, globally unified but on-demand disclosure observation memory system**. Move away from the low-level pattern of external scripts "assembling prompts and feeding them to AI." Instead, let the AI engine (OpenCode-Builder) receive a simple "path and goal," autonomously explore the file system, assign sub-tasks, and distill observations. The system follows **Progressive Disclosure**: the memory pool is global, but the context the agent receives stays sparse and high-density.

### 1.2 Core Value Proposition
- **Agentic autonomous exploration**: Scripts only trigger tasks and provide clues (file paths). The AI handles reading, filtering (e.g., excluding blog posts that only had formatting changes), and summarizing.
- **Progressive Disclosure**: Detailed memory is not loaded by default. The agent actively retrieves only the L1/L2 observations relevant to the current task.
- **Global layered architecture**:
  - **L3**: Global hard constraints (stored in `rules/`, passively loaded globally).
  - **L1/L2**: Dynamic observation log (stored in a global memory pool, agent actively retrieves).
- **Noise-resistant design**: Uses the AI's semantic understanding to identify genuinely "new content." For example, when 300+ blog posts show file changes, the AI checks the `Date` field in metadata to identify truly new articles.

### 1.3 Target Users
- **OpenCode-Builder**: The producer and core consumer of memory.
- **Developer**: Only as the definer of system boundaries and the final auditor of the memory log.

---

## 2. Core Design Principles (The Agentic Way)

### 2.1 Reject Push, Embrace Pull
Traditional systems try to "push" all context to the model. This system requires the agent to have "pull" awareness. The script tells the agent: "These files changed. Go learn the valuable lessons." The agent decides what to read and how much.

### 2.2 Sparse Context Assumption
We assume: for any given task, truly relevant memories are very few. Therefore, the global memory pool (OBSERVATIONS.md) is allowed to grow continuously, but the agent must be able to efficiently load subsets through tags or keywords.

### 2.3 Zero-Friction Assetization
The memory log uses a plain-text append-only format. It is both the agent's runtime state machine and the developer's knowledge asset.

---

## 3. Functional Requirements: Three-Tier Hierarchy

### 3.1 L3: Global Constraints and Philosophy
- **Content**: Stored in `rules/SOUL.md` and `rules/USER.md`.
- **Hard constraints**: Must include language style constraints (no big words, no marketing terms, no quotation marks, avoid negative "not" sentence patterns as much as possible), coping strategies, etc.
- **Loading method**: Passively loaded globally at session start.

### 3.2 L1: Daily Observation and Heartbeat
- **Content**: Key events, technical decisions, and real bug-fix experiences from the past 24 hours.
- **Tagging format**: `🔴 High (methodology/constraint)`, `🟡 Medium (project status/decision)`, `🟢 Low (task log)`.
- **Generation method**: The script only provides a set of file paths found by `find`. The rest is handed to OpenCode-Builder. The agent processes autonomously (including calling sub-agents to read files and check metadata).

### 3.3 L2: Memory Distillation and Reflection (Weekly)
- **Responsibility**: Garbage collection.
- **Logic**: Runs weekly. The AI autonomously reads the L1 memory pool, deletes expired 🟢 entries, merges same-topic 🟡 entries, and promotes common patterns to 🔴.

---

## 4. Key Business Flow (User Story)

### 4.1 Agent-Initiated Heartbeat Task
1. **Trigger**: System cron job triggers the script.
2. **Input**: The script runs `find -mtime -1`, producing a long path list (potentially including 300+ changed blog posts).
3. **Dispatch**: The script starts an OpenCode-Builder session.
4. **Instruction**: "Here is the list of files changed in the past 24 hours. Your goal is to generate observation records. Note: for articles under the blog/ directory, check the Date field in their metadata. Only process content genuinely created today. Ignore formatting rearrangements."
5. **Execution**: The agent sees the task, autonomously starts sub-agents (librarian/explore) to read files in parallel, then aggregates the output.
6. **Output**: Results appended to the global `contexts/memory/OBSERVATIONS.md`.

---

## 5. Technical Constraints and Integration

- **Execution engine**: Local OpenCode Server (localhost:<your-port>).
- **Core model**: `<your-model>`.
- **Agent identity**: `<your-agent>`.
- **Memory storage**: Markdown files (supports Git version control).
