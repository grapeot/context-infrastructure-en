#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_PROPERTY_ID = "393442232"


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


def setup_credentials() -> None:
    creds_path = os.getenv("GA4_CREDENTIALS_PATH")
    if creds_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path


def date_range_str(days: int) -> tuple[str, str]:
    return f"{days}daysAgo", "today"


def rows_to_dicts(response: Any) -> list[dict[str, str]]:
    dim_headers = [h.name for h in response.dimension_headers]
    met_headers = [h.name for h in response.metric_headers]
    rows = []
    for row in response.rows:
        entry: dict[str, str] = {}
        for i, dh in enumerate(dim_headers):
            entry[dh] = row.dimension_values[i].value
        for i, mh in enumerate(met_headers):
            entry[mh] = row.metric_values[i].value
        rows.append(entry)
    return rows


class GA4Client:
    def __init__(self, property_id: str = DEFAULT_PROPERTY_ID) -> None:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient

        self.property = f"properties/{property_id}"
        self.client = BetaAnalyticsDataClient()

    def _run(self, request: Any) -> list[dict[str, str]]:
        response = self.client.run_report(request)
        return rows_to_dicts(response)

    def daily(self, days: int = 30) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
        ))

    def weekly(self, days: int = 90) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[Dimension(name="isoYearIsoWeek")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="isoYearIsoWeek"))],
        ))

    def top_pages(self, limit: int = 20, days: int = 90) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="pageTitle"),
            ],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
            limit=limit,
        ))

    def sources(self, days: int = 90) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
            ],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=50,
        ))

    def channels(self, days: int = 90) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        ))

    def campaigns(self, days: int = 30) -> list[dict[str, str]]:
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )
        start, end = date_range_str(days)
        return self._run(RunReportRequest(
            property=self.property,
            dimensions=[
                Dimension(name="sessionCampaignName"),
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
            ],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            date_ranges=[DateRange(start_date=start, end_date=end)],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=50,
        ))

    def snapshot(self, days_daily: int = 30, days_wide: int = 90) -> dict[str, Any]:
        return {
            "daily": self.daily(days=days_daily),
            "weekly": self.weekly(days=days_wide),
            "top_pages": self.top_pages(days=days_wide),
            "sources": self.sources(days=days_wide),
            "channels": self.channels(days=days_wide),
            "campaigns": self.campaigns(days=days_daily),
        }


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Analytics 4 metrics CLI")
    parser.add_argument("--env-file", help="Optional .env file path")
    parser.add_argument("--property", default=DEFAULT_PROPERTY_ID, help="GA4 property ID")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("daily", help="Daily traffic: active users, sessions, PV, duration, bounce")
    p.add_argument("--days", type=int, default=30)

    p = sub.add_parser("weekly", help="Weekly aggregated traffic")
    p.add_argument("--days", type=int, default=90)

    p = sub.add_parser("top-pages", help="Top pages by pageviews")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--days", type=int, default=90)

    p = sub.add_parser("sources", help="Traffic sources breakdown")
    p.add_argument("--days", type=int, default=90)

    p = sub.add_parser("channels", help="Channel group breakdown")
    p.add_argument("--days", type=int, default=90)

    p = sub.add_parser("campaigns", help="UTM campaign tracking (Twitter/social attribution)")
    p.add_argument("--days", type=int, default=30)

    p = sub.add_parser("snapshot", help="Fetch all reports, save to JSON")
    p.add_argument("--days", type=int, default=90, help="Days window for weekly/pages/sources/channels")
    p.add_argument("--output", help="Write JSON to file instead of stdout")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    load_dotenv(args.env_file)
    setup_credentials()

    try:
        client = GA4Client(property_id=args.property)
    except Exception as exc:
        raise SystemExit(f"Failed to initialize GA4 client: {exc}")

    try:
        if args.cmd == "daily":
            print_json(client.daily(days=args.days))

        elif args.cmd == "weekly":
            print_json(client.weekly(days=args.days))

        elif args.cmd == "top-pages":
            print_json(client.top_pages(limit=args.limit, days=args.days))

        elif args.cmd == "sources":
            print_json(client.sources(days=args.days))

        elif args.cmd == "channels":
            print_json(client.channels(days=args.days))

        elif args.cmd == "campaigns":
            print_json(client.campaigns(days=args.days))

        elif args.cmd == "snapshot":
            data = client.snapshot(days_daily=min(args.days, 30), days_wide=args.days)
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"Saved to {output_path}")
            else:
                print_json(data)

        else:
            parser.print_help()
            return 1

        return 0

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
