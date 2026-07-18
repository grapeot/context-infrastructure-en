# Skill: OpenReview API

Query paper metadata and author profiles for AI academic conferences hosted on OpenReview (ICLR, NeurIPS, ICML, etc.).

## When to Use

- Get the accepted paper list for a conference (title, authors, authorids)
- Look up an author's profile: institution history, position, start/end years
- Search authors by name to find their tilde ID
- Batch-query profiles for a set of tilde IDs

## CLI Tool

Path: `tools/openreview_cli.py`

Dependency: `openreview-py` (installed in the workspace `.venv`)

Authentication: `openreview_email` / `openreview_password` in `.env`, or environment variables `OPENREVIEW_EMAIL` / `OPENREVIEW_PASSWORD`. Token is cached to a temp file (e.g., `tmp/openreview_token.json`) to avoid repeated logins hitting the rate limit (3 logins per window).

### Subcommands

```bash
# Get conference accepted papers
python tools/openreview_cli.py papers ICLR.cc/2024/Conference
python tools/openreview_cli.py papers NeurIPS.cc/2024/Conference -o papers.json

# Look up a single profile
python tools/openreview_cli.py profile ~Bohan_Lyu1
python tools/openreview_cli.py profile ~Bohan_Lyu1 --publications --relations

# Search by name
python tools/openreview_cli.py search "Bohan Lyu"
python tools/openreview_cli.py search "Chen Zhang" --institution "Peking University"

# Batch-query profiles
python tools/openreview_cli.py profiles --ids "~A1,~B2,~C3"
python tools/openreview_cli.py profiles --ids-file author_ids.txt
```

### Output Format

Default is JSON to stdout. Add `-o path.json` to write a file (stdout then returns only `{"status":"ok","file":"...","summary":"..."}`).

Profile JSON structure:

```json
{
  "id": "~Bohan_Lyu1",
  "preferred_name": "Bohan Lyu",
  "all_names": ["Bohan Lyu"],
  "history": [
    {
      "position": "Undergrad student",
      "start": 2022, "end": 2026,
      "institution": "Tsinghua University",
      "domain": "tsinghua.edu.cn",
      "country": "CN",
      "city": null, "department": null
    }
  ],
  "emails": ["****@mails.tsinghua.edu.cn", "****@gmail.com"],
  "homepage": "",
  "dblp": "", "google_scholar": "", "semantic_scholar": ""
}
```

Paper JSON structure:

```json
{
  "id": "rhgIgTSSxW",
  "title": "TabR: Tabular Deep Learning Meets Nearest Neighbors",
  "authors": ["Yury Gorishniy", "Ivan Rubachev"],
  "authorids": ["~Yury_Gorishniy1", "~Ivan_Rubachev1"],
  "venue": "ICLR 2024 poster",
  "venueid": "ICLR.cc/2024/Conference",
  "abstract": "...",
  "keywords": ["tabular", "deep learning"],
  "primary_area": "...",
  "pdf": "/pdf/..."
}
```

## Confirmed Venue IDs

| Conference | Venue ID |
|------------|----------|
| ICLR 2024 | `ICLR.cc/2024/Conference` |
| ICLR 2025 | `ICLR.cc/2025/Conference` |
| NeurIPS 2024 | `NeurIPS.cc/2024/Conference` |
| NeurIPS 2023 | `NeurIPS.cc/2023/Conference` |
| ICML 2024 | `ICML.cc/2024/Conference` |

CVPR 2023+ may be available; AAAI/ACL coverage is limited and must be confirmed one by one.

## Known Limitations

1. **Affiliation is not on the paper.** Papers only carry authorids; institution info is in the profile. Flow: papers → extract authorids → batch-query profiles → read history.
2. **Emails are masked.** The public API only returns the domain part (`****@tsinghua.edu.cn`); full emails are not available.
3. **History is self-reported.** In practice the ICLR author cohort has a high fill rate (100% history, 85% country), but this is not guaranteed for all users. Use institution-name matching + email domain (`.edu.cn`) as a fallback for identifying Chinese institutions.
4. **Login rate limit.** At most 3 logins per time window. The CLI already does token caching; normal use will not trigger it. If a 403 occurs due to an expired token, delete `tmp/openreview_token.json` and retry once.
5. **Common-name search is noisy.** `search "Chen Zhang"` returns 247 results. Use `--institution` to filter, or prefer querying profiles directly from paper authorids rather than searching by name.

## Typical Workflows

### Batch-extract student paper authors from a conference

```bash
# 1. Get papers
python tools/openreview_cli.py papers ICLR.cc/2024/Conference -o tmp/iclr2024_papers.json

# 2. Extract all authorids
cat tmp/iclr2024_papers.json | python -c "
import sys,json
papers = json.load(sys.stdin)
ids = set()
for p in papers:
    ids.update(p['authorids'])
print('\n'.join(sorted(ids)))
" > tmp/iclr2024_authorids.txt

# 3. Batch-query profiles
python tools/openreview_cli.py profiles --ids-file tmp/iclr2024_authorids.txt -o tmp/iclr2024_profiles.json
```

### Look up a known candidate's OpenReview profile

```bash
# Search by name + institution filter
python tools/openreview_cli.py search "Xiaohu Huang" --institution "Hong Kong"

# If the tilde ID is known, query directly
python tools/openreview_cli.py profile ~Xiaohu_Huang1
```

## Tests

```bash
cd <project_dir>
source .venv/bin/activate
python -m pytest tests/test_openreview_cli.py -v
```

The integration tests cover all 4 subcommands. They call the live API and require valid credentials.