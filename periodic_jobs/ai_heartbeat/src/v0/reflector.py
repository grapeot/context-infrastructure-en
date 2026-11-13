#!/usr/bin/env python3
"""
L2 Reflector Agent (Trigger Script)

Two stages, so that no rule changes without a human saying yes:

1. propose (default, safe to run from cron at night):
   the agent reads OBSERVATIONS.md and writes rule *candidates* to contexts/memory/RULE_CANDIDATES.md,
   each with its target file, the exact change, the reason, and the source entries it came from.
   It does not touch rules/ or OBSERVATIONS.md. The script snapshots rules/ before and after and
   exits non-zero if anything under rules/ changed.
2. apply (run by hand after review, `--apply`):
   the human ticks `- [x] Approve` on the candidates they accept; the agent merges only those into rules/,
   moves them to the archive section of the candidates file, and garbage-collects OBSERVATIONS.md.
"""
import hashlib
import os
import sys
from datetime import datetime

from opencode_client import OpenCodeClient

KNOWLEDGE_BASE = "/path/to/your/workspace/periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KNOWLEDGE_BASE))))
RULES_DIR = os.path.join(ROOT_DIR, "rules")
CANDIDATES_PATH = os.path.join(ROOT_DIR, "contexts", "memory", "RULE_CANDIDATES.md")

PROPOSE_TEMPLATE = """
Run the memory system's "reflection" task (propose stage: write candidates only, do not change rules).

SOP: {kb_path}
Date: {target_date}

Steps:
1. Read contexts/memory/OBSERVATIONS.md and analyse the 🔴 and high-priority 🟡 entries; when you need to check one, find the original conversation in the session history directory or with local search.
2. Find patterns worth promoting, and rules under rules/ that contradict each other and need a clearer boundary.
3. Write each suggestion as a candidate and append it to the "Pending review" section of contexts/memory/RULE_CANDIDATES.md (create the file if it does not exist: a title line "# Rule candidates", then the sections "## Pending review" and "## Done"). Use this format for every candidate:

### {target_date} · <one-line title>
- [ ] Approve
- Target file: rules/... (full relative path)
- Change: add / modify / delete, with the new text; for modify and delete also quote the old lines
- Reason: why the change is needed, and where it does and does not apply
- Sources: the observation entry dates, or the full relative paths of the original conversation files, that support it (at least one)

Hard constraints:
- Do not modify any file under rules/, and do not modify OBSERVATIONS.md. In this stage you may only write RULE_CANDIDATES.md.
- Do not repeat a suggestion that is already under "Pending review".
- Promotion bar: general across projects + confirmed more than once + a clear scope; a problem seen only once is not proposed as a global rule.

When done, reply with a short report: how many candidates you added and their target files.
"""

APPLY_TEMPLATE = """
Run the memory system's "promotion" task (apply stage: a human has reviewed the candidates).

SOP: {kb_path}

Steps:
1. Read the "Pending review" section of contexts/memory/RULE_CANDIDATES.md.
2. Handle only the candidates ticked "- [x] Approve": change rules/ exactly as each candidate's target file and change say. Leave every unticked candidate alone.
3. Move each merged candidate to the "## Done" section and append "(merged YYYY-MM-DD)" to its title.
4. GC: rewrite contexts/memory/OBSERVATIONS.md, deleting content that has been merged into rules and expired 🟢 entries.

When done, reply with a short report: which candidates you merged and which file each one changed.
"""


def snapshot(path):
    """sha256 of every file under path, keyed by relative path."""
    out = {}
    for base, _, files in os.walk(path):
        for name in files:
            full = os.path.join(base, name)
            with open(full, "rb") as f:
                out[os.path.relpath(full, path)] = hashlib.sha256(f.read()).hexdigest()
    return out


def changed(before, after):
    keys = set(before) | set(after)
    return sorted(k for k in keys if before.get(k) != after.get(k))


def run(client, title, prompt, model_id):
    session_id = client.create_session(title)
    if not session_id:
        return None
    client.send_message(session_id, prompt, model_id=model_id)
    # If send_message timed out, agent may still be running; poll until done
    print("Waiting for session to complete (sync mode)...")
    client.wait_for_session_complete(session_id)
    return session_id


def main():
    import argparse
    parser = argparse.ArgumentParser(description='L2 Reflector Agent')
    parser.add_argument('--model', default='<your-model-id>',
                        choices=['<your-model-id>'],
                        help='Model ID to use')
    parser.add_argument('--apply', action='store_true',
                        help='Merge the candidates a human has ticked into rules/ (default: only propose candidates)')
    args = parser.parse_args()

    model_id = args.model
    target_date = datetime.now().strftime("%Y-%m-%d")
    client = OpenCodeClient()

    if args.apply:
        print(f"Applying approved candidates from {CANDIDATES_PATH} using model: {model_id}...")
        session_id = run(client, f"Heartbeat L2 Reflector Apply - {target_date}",
                         APPLY_TEMPLATE.format(kb_path=KNOWLEDGE_BASE), model_id)
        print(f"Task complete (Session: {session_id}).")
        return

    print(f"Proposing rule candidates using model: {model_id}...")
    before = snapshot(RULES_DIR)
    session_id = run(client, f"Heartbeat L2 Reflector Propose - {target_date}",
                     PROPOSE_TEMPLATE.format(kb_path=KNOWLEDGE_BASE, target_date=target_date), model_id)
    touched = changed(before, snapshot(RULES_DIR))
    if touched:
        print("ERROR: rules/ changed during the propose stage, which is not allowed:", file=sys.stderr)
        for path in touched:
            print(f"  rules/{path}", file=sys.stderr)
        print("Review with `git diff -- rules/` and revert what you did not approve.", file=sys.stderr)
        sys.exit(1)
    print(f"Candidates written to {CANDIDATES_PATH}. Review them, tick `- [x] Approve`, then run with --apply.")
    print(f"Task complete (Session: {session_id}).")


if __name__ == "__main__":
    main()
