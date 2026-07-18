#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import requests

DEFAULT_BASE_URL = "https://api.kit.com/v4"


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

    env_from_var = os.getenv("KIT_ENV_FILE")
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


class KitClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("KIT_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.timeout = int(os.getenv("KIT_TIMEOUT", "30"))

        self.api_key = os.getenv("KIT_API_KEY")
        if not self.api_key:
            raise ValueError("KIT_API_KEY is required in .env")

    def _headers(self) -> dict[str, str]:
        return {
            "X-Kit-Api-Key": self.api_key or "",
            "Accept": "application/json",
        }

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        if response.status_code == 429:
            raise requests.HTTPError(
                "Rate limit exceeded (120 req/60s). Please wait before retrying.",
                response=response,
            )
        response.raise_for_status()
        if not response.text.strip():
            return {}
        return response.json()

    def account(self) -> Any:
        return self._get("/account")

    def growth_stats(self, start_date: str, end_date: str) -> Any:
        return self._get("/account/growth_stats", params={"starting": start_date, "ending": end_date})

    def email_stats(self) -> Any:
        return self._get("/account/email_stats")

    def subscribers(self, per_page: int = 1) -> Any:
        return self._get(
            "/subscribers",
            params={"status": "active", "include_total_count": "true", "per_page": per_page},
        )

    def subscriber_count(self) -> int:
        data = self.subscribers(per_page=1)
        pagination = data.get("pagination") or data.get("meta") or {}
        total = pagination.get("total_count") or data.get("total_subscribers") or data.get("total")
        if total is not None:
            return int(total)
        return len(data.get("subscribers", []))

    def broadcasts(self, per_page: int = 10) -> Any:
        return self._get("/broadcasts", params={"per_page": per_page, "sort_order": "desc"})

    def broadcast_stats(self, broadcast_id: int | str) -> Any:
        return self._get(f"/broadcasts/{broadcast_id}/stats")

    def snapshot(self, start_date: str, end_date: str, broadcasts_limit: int = 10) -> dict[str, Any]:
        result: dict[str, Any] = {
            "start_date": start_date,
            "end_date": end_date,
        }

        result["growth_stats"] = self.growth_stats(start_date, end_date)
        result["email_stats"] = self.email_stats()

        bcast_data = self.broadcasts(per_page=broadcasts_limit)
        broadcasts_list = bcast_data.get("broadcasts", [])

        enriched: list[dict[str, Any]] = []
        for bcast in broadcasts_list:
            bcast_id = bcast.get("id")
            entry: dict[str, Any] = {
                "id": bcast_id,
                "subject": bcast.get("subject"),
                "published_at": bcast.get("published_at"),
                "recipients": bcast.get("recipients"),
            }
            if bcast_id:
                try:
                    stats = self.broadcast_stats(bcast_id)
                    entry["stats"] = stats
                except requests.HTTPError:
                    entry["stats"] = None
            enriched.append(entry)

        result["recent_broadcasts"] = enriched
        return result


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kit (ConvertKit) API v4 metrics CLI")
    parser.add_argument("--env-file", help="Optional .env file path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("account", help="Show account info")

    growth_parser = sub.add_parser("growth", help="Subscriber growth stats")
    growth_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    growth_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")

    sub.add_parser("email-stats", help="Aggregated open/click rates (last 90 days)")

    subscribers_parser = sub.add_parser("subscribers", help="Active subscriber info")
    subscribers_parser.add_argument("--count", action="store_true", help="Print only the count")

    broadcasts_parser = sub.add_parser("broadcasts", help="List recent broadcasts")
    broadcasts_parser.add_argument("--limit", type=int, default=10, help="Number of broadcasts (default: 10)")

    bcast_stats_parser = sub.add_parser("broadcast-stats", help="Stats for a specific broadcast")
    bcast_stats_parser.add_argument("broadcast_id", help="Broadcast ID")

    snapshot_parser = sub.add_parser("snapshot", help="Fetch everything in one shot")
    snapshot_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    snapshot_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    snapshot_parser.add_argument("--broadcasts-limit", type=int, default=10, help="Number of recent broadcasts")
    snapshot_parser.add_argument("--output", help="Write JSON output to file")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    loaded_env = load_dotenv(args.env_file)

    try:
        client = KitClient()
    except ValueError as exc:
        source_note = f" (loaded from {loaded_env})" if loaded_env else ""
        raise SystemExit(f"{exc}{source_note}")

    default_start, default_end = default_date_range()
    start_date = getattr(args, "start_date", None) or default_start
    end_date = getattr(args, "end_date", None) or default_end

    try:
        if args.cmd == "account":
            print_json(client.account())
            return 0

        if args.cmd == "growth":
            print_json(client.growth_stats(start_date, end_date))
            return 0

        if args.cmd == "email-stats":
            print_json(client.email_stats())
            return 0

        if args.cmd == "subscribers":
            if args.count:
                print(client.subscriber_count())
            else:
                print_json(client.subscribers(per_page=50))
            return 0

        if args.cmd == "broadcasts":
            data = client.broadcasts(per_page=args.limit)
            broadcasts = data.get("broadcasts", [])
            # Sort by published_at desc and show key fields
            broadcasts_sorted = sorted(
                broadcasts,
                key=lambda b: b.get("published_at") or "",
                reverse=True,
            )
            summary = [
                {
                    "id": b.get("id"),
                    "subject": b.get("subject"),
                    "published_at": b.get("published_at"),
                    "recipients": b.get("recipients"),
                }
                for b in broadcasts_sorted
            ]

            print_json(summary)
            return 0

        if args.cmd == "broadcast-stats":
            data = client.broadcast_stats(args.broadcast_id)
            stats = data.get("broadcast", data)
            summary = {
                "id": args.broadcast_id,
                "open_rate": stats.get("open_rate"),
                "click_rate": stats.get("click_rate"),
                "unsubscribes": stats.get("unsubscribes"),
            }
            if "stats" in stats:
                inner = stats["stats"]
                summary["open_rate"] = inner.get("open_rate", summary["open_rate"])
                summary["click_rate"] = inner.get("click_rate", summary["click_rate"])
                summary["unsubscribes"] = inner.get("unsubscribes", summary["unsubscribes"])
            print_json(summary)
            return 0

        if args.cmd == "snapshot":
            data = client.snapshot(
                start_date,
                end_date,
                broadcasts_limit=args.broadcasts_limit,
            )
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
