# Setup Guide: Context Infrastructure

This is an AI-guided setup guide. Follow the steps in order; you'll feel the difference after each one.

---

## Step 1: Fill in identity files (required, 5 minutes)

**Value**: Once this step is done, AI behavior becomes personalized immediately. This is the highest-ROI step.

### 1a. Fill in USER.md

Open `rules/USER.md` and replace the template content with your own information.

At minimum, fill in these items:
- **Name**: What you want the AI to call you
- **Timezone**: Avoid time-related confusion
- **Background**: Who you are, what you do
- **Technical interests**: The more specific, the better
- **What annoys you**: Help the AI avoid communication styles you dislike

**Verify**: After filling it in, ask the AI "Tell me what you know about me" and check whether it describes you accurately.

### 1b. Customize SOUL.md (optional but recommended)

Open `rules/SOUL.md` and adjust the AI's core behavioral baseline.

The default content is already a solid general foundation (direct, opinionated, no fluff). If you have specific needs, add your preferences in the "Vibe" and "Core Truths" sections.

---

## Step 2: Explore and extend skills (recommended, 15 minutes)

**Value**: Understand the skill format and start accumulating your own reusable workflows.

### 2a. Browse existing skills

Open `rules/skills/INDEX.md` and scan the existing skill categories:

- **BestPractice**: Ready to use, independent of your tools and projects
- **Workflow**: Research, slide creation, cognitive profile extraction. Understand first, then adapt.
- **API Guide**: ⚙️ marked items need configuration, ✅ marked items are ready to use

### 2b. Create your first skill

Pick something you do often (calling an API, processing a type of data, running a workflow) and create `rules/skills/<category>_<name>.md` using this format:

```markdown
# Skill: Name

## When to Use
What situation triggers this skill

## Prerequisites
What tools/config are needed

## Steps
1. Step one
2. Step two

## Example
Concrete commands or code
```

Add the new skill to the appropriate category in `rules/skills/INDEX.md`.

### 2c. Install external public skill repos

The content in `rules/skills/` is a starter set — you don't need to copy every capability into it. When you need more complete capabilities, check [`docs/SKILL_ECOSYSTEM.md`](docs/SKILL_ECOSYSTEM.md) first. It lists a set of independently maintained public skill repos: Tavily, Google Docs, Google Maps, Outlook, Resend, OpenCode, Process Launcher, PPTX, Typefully, and Stripe.

To install, give the target repo URL to your AI agent and have it start from the current workspace's `AGENTS.md` / `WORKSPACE.md`, exposing only one root skill. Generic technical contracts stay in the public repo; contact aliases, local paths, endpoints, tokens, and business context stay in a local overlay.

### 2d. About axioms

`rules/axioms/` contains 43 decision principles distilled from real experience. These represent the original author's perspective and cognitive patterns. Use them as reference, but do not let them replace your own axioms.

Suggestions:
- Browse `rules/axioms/INDEX.md` first to understand the categories and core meanings
- Mark axioms that resonate with you
- Over time, accumulate your own axioms from your project experience (using the same format)

---

## Step 3: Set up the memory system (optional, 30 minutes)

**Value**: Let the AI automatically accumulate your work experience. The more you use it, the better it understands you.

### 3a. Understand the three-tier architecture

```
L3 (global constraints): All files under rules/ → passively loaded every session
L1/L2 (dynamic memory): contexts/memory/OBSERVATIONS.md → agent actively retrieves
```

L3 is already configured (Step 1). L1/L2 requires cron setup for automatic execution.

### 3b. Configure OpenCode Server

The scripts in `periodic_jobs/ai_heartbeat/` depend on the OpenCode Server API.

1. Confirm your local OpenCode Server is running (or configure the connection)
2. Check `opencode_client.py` in `periodic_jobs/ai_heartbeat/src/v0/` (you need to provide this yourself; see OpenCode docs for the source)
3. Test connectivity: `python3 observer.py --help`

### 3c. Configure cron

```bash
# Daily 8:00 AM — run observer (scan today's changes)
0 8 * * * cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# Weekly Monday 9:00 AM — run reflector (distill and promote)
0 9 * * 1 cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1
```

Adjust paths and times to your actual setup.

### 3d. Verify

Run the observer once:

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/observer.py 2024-01-15
```

Check whether `contexts/memory/OBSERVATIONS.md` has new entries.

---

## Step 4: Extend Tier 2 components (on demand, 30–60 minutes)

These components work independently. Configure them as needed; skipping them does not affect core functionality.

### Semantic search (⚙️)

Once your `contexts/` directory has accumulated enough content, semantic search lets you retrieve historical records by meaning rather than keywords.

**Requires**: Any OpenAI-compatible embedding endpoint (local or cloud)
**Configuration**: Install the ecosystem [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)

### Share reports to the web (⚙️)

Convert research reports to HTML and publish them to your own server.

**Requires**: A server with SSH access
**Configuration**: See `rules/skills/share_report.md`, replace `<your-domain>` and `<your-server>`

### Send email notifications (⚙️)

Have the AI send you an email when a task completes.

**Requires**: Gmail App Password
**Configuration**: See `rules/skills/send_email.md`

---

## When you'll feel the system's value

**After filling in USER.md (immediately)**: AI responses become targeted rather than generic.

**After 2–3 weeks of use**: Your `contexts/` directory starts accumulating work records. The AI can reference context.

**After 1–2 months of running the memory system**: The observer begins identifying your work patterns. The reflector promotes high-value experiences into skills or axioms.

**After 6+ months of accumulation**: The system starts to genuinely understand your judgment logic and decision patterns. You'll notice the AI's suggestions getting closer to what you would decide yourself.

---

## FAQ

**Q: Can I use the axioms directly?**
A: You can use them to understand the system's structure, but the core content represents the original author's perspective. Your axioms need to be distilled from your own experience. See `rules/skills/workflow_cognitive_profile_extraction.md` for the extraction method.

**Q: Can I use the skills directly?**
A: ✅ marked ones are ready to use. ⚙️ marked ones need configuration replacement (endpoints, API keys, domains, etc.). BestPractice category items are mostly ready to use. More complete tool-type capabilities live in independent public repos; see [`docs/SKILL_ECOSYSTEM.md`](docs/SKILL_ECOSYSTEM.md).

**Q: What dependencies does observer.py need?**
A: It depends on `opencode_client.py` (a client wrapper for OpenCode Server). You need to implement or adapt this based on the AI agent framework you use.

**Q: Can I use a different AI agent (not OpenCode)?**
A: Yes. The core logic of `observer.py` is constructing a prompt and calling an AI. You can replace `opencode_client` with the Claude API, OpenAI API, or any AI interface that supports long conversations.

---

## Next steps

Once the system is set up, the real accumulation begins. The key is consistent use: put your work in this workspace, let the AI participate in your daily work. Over time, the system will understand you better and better.
