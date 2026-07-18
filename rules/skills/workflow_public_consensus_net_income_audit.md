# Skill: Public Consensus Net Income Audit Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Auditing FY / CY consensus net income for a set of stocks using public web sources, especially when mixing MarketScreener, Yahoo Finance, MarketWatch, and similar pages.
- **Created**: 2026-05-06
- **Recommended model**: GPT series. Do not delegate core extraction or QA to GLM / DeepSeek.

## Goal

Organize "what current public web sources can trace back to as consensus net income" into an auditable table, and explicitly distinguish current source availability, historical baseline availability, revision comparability, direct value, and derived value.

This skill does not provide investment advice, does not derive market sentiment from estimates, and does not substitute EPS or revenue trends for net income consensus.

## Acceptance Criteria

The task is complete only when all of these conditions are met:

1. Every ticker has one row in the audit table; when no public net income can be found, write `Current Source Status = Unavailable` explicitly rather than leaving the cell blank.
2. Current value, six-month-ago baseline, and revision direction are expressed separately. `Not Comparable` can only indicate revision not comparable; it must not mislead readers into thinking the current consensus is missing.
3. Every non-`N/A` current value carries a source URL, retrieved-at timestamp, source provider, source field, currency, unit, and fiscal period.
4. Direct and derived are labeled separately. Direct means the page explicitly exposes a target-year value named `Net income` / `Net income 1` / `Net income Million <currency>`. Derived means a value recomputed from page-exposed fields such as net sales × net margin, or summing semi-annual net income.
5. All source URLs are reviewed link-by-link before final delivery. The review does not stop at HTTP reachability; it also verifies that the extracted page text locates the fiscal period, currency unit, source field, and target year column.
6. The QA record must list corrected values, especially corrections to column mapping, currency, and direct/derived status.
7. Notes outside the table use the user's preferred natural language. If the user asks for a Chinese explanation with an English table, keep the column names and values copyable, and write the prose notes in Chinese.

## Available Resources

Prefer the Tavily CLI for web search and extraction. Common command shapes:

```bash
cd <tavily_skill_dir> && .venv/bin/python -m tavily_skill search "<query>" --max-results 6 --search-depth advanced --answer advanced --stdout
cd <tavily_skill_dir> && .venv/bin/python -m tavily_skill extract <url1> <url2> --query "Projected Income Statement Net income 1 Fiscal Period 2026 currency" --chunks-per-source 2 --output tmp/<session>/qa_extract.json
```

If using Python to process files, confirm the workspace root `.venv/` exists and use `.venv/bin/python`. Generate reports under `tmp/<session_slug>/`; when publishing, sync to the share-report archive directory per `share_report.md`.

## Table Semantics

The recommended audit table includes at least these columns:

| Column | Meaning |
|---|---|
| `Current Source Status` | Whether the current public source has a verifiable value; allowed values: `Available (direct)`, `Available (derived)`, `Available (semiannual direct sum)`, `Unavailable`, `Not live FY2026E` |
| `Current Consensus Estimate` | The value currently adopted. Write current value `N/A` only when this column is missing |
| `Baseline Status` | Whether the same field, same methodology, same provider baseline from six months ago is traceable |
| `Direction` | Revision direction. Write Up / Down / Flat only when both current and baseline are comparable; otherwise write `Not Comparable` |
| `Source Field Name` | Page field name, e.g., `Net income 1`, `Net income Million CNY`, `Net sales 1 / Net margin (%)` |
| `Calculation Notes` | Why this page was adopted; direct/derived logic; fiscal-year and currency caveats |

The working sheet should preserve the adoption logic for the provider aggregate. Public web pages usually lack firm-level analyst detail, so do not fabricate broker averages.

## Workflow Suggestions

First define the universe and target fiscal period, then search source URLs by ticker in parallel. The search phase can be batched to subagents, but core extraction, column mapping, and final QA require a GPT-series model review. This task is very sensitive to table column position, fiscal-year convention, and currency; GLM / DeepSeek tend to confuse 2026/2027 columns, USD/CNY, and direct/derived in this task, so do not use them for core judgment.

After collection, do not publish immediately. First run one pass of link-by-link QA: batch-extract all URLs, confirm `failed_count=0`, then check item by item whether the target value actually appears in the current extracted text. When the search answer, subagent summary, and live extract conflict, defer to the live extract and page field. If the live extract does not expose a direct row but the search snippet does, annotate the evidence level clearly in the table.

## Known Pitfalls

**MarketScreener year columns are easily misaligned.** The annual table is usually 2021-2028; the search summary may treat the last column as 2026, or misread the 2027 column as 2026. The fix is to check the `Fiscal Period` header, announcement dates, and the target year column together.

**Calendar and finances pages may give different granularities.** The calendar page often exposes an annual `Net income Million CNY` row; the finances page often exposes `Net income 1` plus quarterly / halfyear tables. When a direct calendar annual row is available, prefer it; do not pass Q4 or semi-annual values off as full-year.

**Regional mirrors may carry stale data or different page states.** `marketscreener.com`, `in.marketscreener.com`, and other mirrors may expose different data. The final table must specify the exact URL used; do not average across mirrors.

**Do not default currency to CNY.** SMIC, Lenovo, Hua Hong, etc. may report in USD million. Preserve the original MarketScreener currency unless the report explicitly requires conversion and provides an FX source/date.

**Derived values must be downgraded.** If the page does not expose an annual net income row directly and you can only use net sales × net margin or summing semi-annual net income, set `Current Source Status` to derived / semiannual direct sum, and write the formula in notes. Do not disguise derived as direct consensus.

**The meaning of `N/A` must be column-scoped.** Baseline = `N/A` only means there is no point-in-time snapshot from six months ago; when the current source is available, the current value must still be shown. Otherwise readers will think the entire row has no data.

## Output Spec

Recommended three categories of files:

1. `tmp/<session>/...audit.md`: working draft, containing audit table, working sheet, QA record, and caveats.
2. `tmp/<session>/qa_extract_*.json`: link-by-link QA extraction results, preserving the evidence chain.
3. If publishing, copy the final MD to the share-report archive directory and generate HTML per `share_report.md`.

If new real pitfalls are discovered after the task, update this skill and `INDEX.md`.