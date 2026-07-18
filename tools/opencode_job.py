#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path


def load_dotenv():
    """Load environment variables from .env file."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v
            break

# Add the client directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "periodic_jobs", "ai_heartbeat", "src", "v0"))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Please check the path.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Submit a job to OpenCode.')
    parser.add_argument('prompt', help='The task description/prompt for the agent.')
    parser.add_argument('--title', default='Automated Job', help='Session title.')
    parser.add_argument('--model', default='glm-5',
                        choices=['glm-5', 'antigravity-gemini-3-flash'],
                        help='Model ID (default: glm-5).')
    parser.add_argument('--agent', default='OpenCode-Builder', help='Agent name (default: OpenCode-Builder).')
    parser.add_argument('--no-wait', action='store_true', help='Do not wait for completion.')
    parser.add_argument('--keep-session', action='store_true', help='Do not delete the session after completion.')

    args = parser.parse_args()

    # Load environment variables before creating client
    load_dotenv()

    client = OpenCodeClient()

    print(f"Creating session: {args.title}...")
    session_id = client.create_session(args.title)
    if not session_id:
        print("Error: Failed to create session.")
        sys.exit(1)

    print(f"Sending message using model {args.model} and agent {args.agent}...")
    result = client.send_message(session_id, args.prompt, model_id=args.model, agent=args.agent)

    if not result:
        print("Warning: Initial request timed out or failed, but the agent might still be running.")

    if not args.no_wait:
        print("Waiting for session to complete...")
        client.wait_for_session_complete(session_id)
        print("Job finished.")

    if not args.keep_session:
        print(f"Deleting session {session_id}...")
        client.delete_session(session_id)
    else:
        print(f"Session {session_id} preserved.")

if __name__ == "__main__":
    main()
