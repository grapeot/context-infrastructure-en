#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import requests

DEFAULT_BASE_URL = "https://typefully.com"
DEFAULT_REFERER = "https://typefully.com/grow"
DEFAULT_USER_AGENT = "Mozilla/5.0"

METRIC_ENDPOINTS = {
    "published_tweets": "published-tweets-count",
    "impressions": "impressions",
    "profile_clicks": "user-profile-clicks",
    "followers": "followers-count",
    "engagements": "engagements",
    "engagement_rate": "engagement-rate",
    "engagement_heatmap": "engagement-heatmap",
}


def _load_env_file(env_file: Path) -> bool:
    if not env_file.exists():
        return False
    with env_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if key and key not in os.environ:
                os.environ[key] = value
    return True


def load_dotenv(explicit_env_file: str | None = None) -> Path | None:
    candidates: list[Path] = []

    if explicit_env_file:
        candidates.append(Path(explicit_env_file).expanduser().resolve())

    env_from_var = os.getenv("TYPEFULLY_ENV_FILE")
    if env_from_var:
        candidates.append(Path(env_from_var).expanduser().resolve())

    cwd = Path.cwd()
    candidates.extend((parent / ".env") for parent in [cwd] + list(cwd.parents))

    script_dir = Path(__file__).resolve().parent
    candidates.extend((parent / ".env") for parent in [script_dir] + list(script_dir.parents))

    seen: set[Path] = set()
    for env_file in candidates:
        if env_file in seen:
            continue
        seen.add(env_file)
        if _load_env_file(env_file):
            return env_file
    return None


def default_date_range() -> tuple[str, str]:
    end = date.today()
    start = end - timedelta(days=14)
    return start.isoformat(), end.isoformat()


class TypefullyClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("TYPEFULLY_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.timeout = int(os.getenv("TYPEFULLY_TIMEOUT", "30"))

        self.authorization = os.getenv("TYPEFULLY_AUTHORIZATION")
        self.account = os.getenv("TYPEFULLY_ACCOUNT")
        self.session = os.getenv("TYPEFULLY_SESSION")
        self.cookie = os.getenv("TYPEFULLY_COOKIE", "")

        if not self.authorization:
            raise ValueError("TYPEFULLY_AUTHORIZATION is required in .env")
        if not self.account:
            raise ValueError("TYPEFULLY_ACCOUNT is required in .env")
        if not self.session:
            raise ValueError("TYPEFULLY_SESSION is required in .env")

    def _headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": os.getenv("TYPEFULLY_USER_AGENT", DEFAULT_USER_AGENT),
            "Accept": "application/json, text/plain, */*",
            "Referer": os.getenv("TYPEFULLY_REFERER", DEFAULT_REFERER),
            "Session": self.session,
            "Account": self.account,
            "Authorization": self.authorization,
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie
        return headers

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        response.raise_for_status()
        if not response.text.strip():
            return {}
        return response.json()

    def accounts_v2(self) -> Any:
        return self._get("/api/backend/accounts-v2")

    def metric(self, metric_endpoint: str, start_date: str, end_date: str) -> Any:
        return self._get(
            f"/api/backend-alt/metric/{metric_endpoint}",
            params={"start_date": start_date, "end_date": end_date},
        )

    def metric_by_name(self, metric_name: str, start_date: str, end_date: str) -> Any:
        endpoint = METRIC_ENDPOINTS.get(metric_name)
        if not endpoint:
            valid = ", ".join(sorted(METRIC_ENDPOINTS.keys()))
            raise ValueError(f"Unknown metric '{metric_name}'. Valid metrics: {valid}")
        return self.metric(endpoint, start_date, end_date)

    def snapshot(self, start_date: str, end_date: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for metric_name in METRIC_ENDPOINTS:
            result[metric_name] = self.metric_by_name(metric_name, start_date, end_date)
        return result


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Private Typefully metrics CLI")
    parser.add_argument("--env-file", help="Optional .env file path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("accounts", help="GET /api/backend/accounts-v2")

    metric_parser = sub.add_parser("metric", help="Fetch one metric")
    metric_parser.add_argument("name", choices=sorted(METRIC_ENDPOINTS.keys()))
    metric_parser.add_argument("--start-date")
    metric_parser.add_argument("--end-date")

    snapshot_parser = sub.add_parser("snapshot", help="Fetch all metrics")
    snapshot_parser.add_argument("--start-date")
    snapshot_parser.add_argument("--end-date")
    snapshot_parser.add_argument("--output", help="Write JSON output to file")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    loaded_env = load_dotenv(args.env_file)

    try:
        client = TypefullyClient()
    except ValueError as exc:
        source_note = f" (loaded from {loaded_env})" if loaded_env else ""
        raise SystemExit(f"{exc}{source_note}")

    default_start, default_end = default_date_range()
    start_date = getattr(args, "start_date", None) or default_start
    end_date = getattr(args, "end_date", None) or default_end

    try:
        if args.cmd == "accounts":
            print_json(client.accounts_v2())
            return 0

        if args.cmd == "metric":
            print_json(client.metric_by_name(args.name, start_date, end_date))
            return 0

        if args.cmd == "snapshot":
            data = {
                "start_date": start_date,
                "end_date": end_date,
                "metrics": client.snapshot(start_date, end_date),
            }
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"Saved to {output_path}")
            else:
                print_json(data)
            return 0

        parser.print_help()
        return 1
    except requests.HTTPError as exc:
        response = exc.response
        if response is not None:
            print(f"HTTP {response.status_code}: {response.text}")
        else:
            print(f"HTTP error: {exc}")
        return 1
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
