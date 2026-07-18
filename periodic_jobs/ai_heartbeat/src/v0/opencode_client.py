import base64
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

module_dir = Path(__file__).resolve().parent
project_env_path = module_dir.parent.parent / ".env"
legacy_env_path = module_dir.parent / ".env"
if project_env_path.exists():
    load_dotenv(project_env_path)
else:
    load_dotenv(legacy_env_path)

# Message timeout: agentic tasks can run 10–60+ min. Default 1 hour.
MESSAGE_TIMEOUT = int(os.getenv("OPENCODE_MESSAGE_TIMEOUT", "3600"))

class OpenCodeClient:
    def __init__(self):
        self.base_url = os.getenv("OPENCODE_BASE_URL", "http://localhost:4096")
        self.username = os.getenv("OPENCODE_USERNAME", "opencode")
        self.password = os.getenv("OPENCODE_PASSWORD")

        if not self.password:
            raise ValueError("OPENCODE_PASSWORD not found in environment variables.")

        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.headers = {"Authorization": f"Basic {encoded}"}

    def list_sessions(self):
        """GET /session - list all sessions."""
        try:
            response = requests.get(
                f"{self.base_url}/session",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []

    def create_session(self, title):
        try:
            response = requests.post(
                f"{self.base_url}/session",
                json={"title": title},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()['id']
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    def _suggest_models(self, provider_id, requested_model_id, limit=5):
        try:
            response = requests.get(
                f"{self.base_url}/provider",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            providers = payload.get("all", [])
            provider = next((p for p in providers if p.get("id") == provider_id), None)
            if not provider:
                return []
            model_ids = list((provider.get("models") or {}).keys())
            if requested_model_id in model_ids:
                return [requested_model_id]

            related = [m for m in model_ids if requested_model_id in m or m in requested_model_id]
            if related:
                return related[:limit]

            stem = requested_model_id.rsplit("-", 1)[0] if "-" in requested_model_id else requested_model_id
            related = [m for m in model_ids if stem and stem in m]
            return related[:limit]
        except Exception:
            return []

    def _wait_for_first_assistant_message(self, session_id, max_wait=45, poll_interval=3):
        started = time.time()
        while (time.time() - started) < max_wait:
            messages = self.get_session_messages(session_id) or []
            if any((m.get("info") or {}).get("role") == "assistant" for m in messages):
                return True
            time.sleep(poll_interval)
        return False

    def send_message(self, session_id, message, model_id="antigravity-gemini-3-flash", provider_id=None, agent="OpenCode-Builder"):
        try:
            # Auto-detect provider from model_id if not specified
            if provider_id is None:
                provider_id = "google"
                if model_id == "glm-5":
                    provider_id = "zai-coding-plan"
                elif model_id.startswith("anthropic") or "/" in model_id:
                    # Handle format like "anthropic/claude-sonnet-4-6"
                    if "/" in model_id:
                        provider_id, model_id = model_id.split("/", 1)
                    else:
                        provider_id = "anthropic"

            payload = {
                "parts": [{"type": "text", "text": message}],
                "model": {
                    "modelID": model_id,
                    "providerID": provider_id
                },
                "agent": agent
            }

            response = requests.post(
                f"{self.base_url}/session/{session_id}/message",
                json=payload,
                headers=self.headers,
                timeout=MESSAGE_TIMEOUT,
            )

            if response.status_code != 200:
                print(f"Server returned {response.status_code} Error: {response.text}")

            response.raise_for_status()

            if not response.text.strip():
                has_assistant_reply = self._wait_for_first_assistant_message(session_id)
                if has_assistant_reply:
                    return {
                        "status": "accepted_empty_response",
                        "session_id": session_id,
                    }

                suggestions = self._suggest_models(provider_id, model_id)
                print("Server returned 200 with empty response body; request was likely rejected before agent reply.")
                print(f"Model/provider used: {provider_id}/{model_id}")
                if suggestions and suggestions[0] != model_id:
                    print(f"Try one of these models for provider '{provider_id}': {', '.join(suggestions)}")
                return None

            try:
                return response.json()
            except ValueError as e:
                suggestions = self._suggest_models(provider_id, model_id)
                print(f"Response JSON parse failed: {e}")
                print(f"Model/provider used: {provider_id}/{model_id}")
                print(f"Raw response prefix: {response.text[:200]!r}")
                if suggestions and suggestions[0] != model_id:
                    print(f"Try one of these models for provider '{provider_id}': {', '.join(suggestions)}")
                return None
        except requests.exceptions.RequestException as e:
            if "Read timed out" not in str(e):
                print(f"Request Exception: {e}")
            return None

    def get_session_messages(self, session_id):
        try:
            response = requests.get(
                f"{self.base_url}/session/{session_id}/message",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting messages: {e}")
            return None

    def delete_session(self, session_id):
        """DELETE /session/:id - remove session from storage (e.g. after ephemeral task completes)."""
        try:
            response = requests.delete(
                f"{self.base_url}/session/{session_id}",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def get_session_info(self, session_id):
        """GET /session/:id - session metadata (e.g. status, running)."""
        try:
            response = requests.get(
                f"{self.base_url}/session/{session_id}",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None

    def wait_for_session_complete(
        self,
        session_id,
        poll_interval=15,
        max_wait=7200,
    ):
        """
        Poll until session is idle. Ensures we don't start the next task before this one finishes.
        Used when send_message times out but the agent is still running.
        """
        start = time.time()
        while (time.time() - start) < max_wait:
            info = self.get_session_info(session_id)
            if not info:
                time.sleep(poll_interval)
                continue
            # OpenCode may use "running", "status", "busy" etc.
            running = info.get("running") or info.get("busy")
            status = info.get("status", "")
            if not running and status not in ("running", "busy"):
                return True
            elapsed = int(time.time() - start)
            print(f"  ... session still running ({elapsed}s elapsed), polling in {poll_interval}s")
            time.sleep(poll_interval)
        print(f"  wait_for_session_complete: max_wait {max_wait}s exceeded")
        return False
