# Staged Approach

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: AI-assisted automation, batch processing, destructive operations
- **Created**: 2026-02-21
- **Source**: Observation record from 2026-01-07

---

## Core Framework

Decompose complex automation tasks into three stages:

```
Stage 1: Data Collection → Stage 2: Batch Processing → Stage 3: Review and Publish
```

### Stage 1: Data Collection

- Fully pull source data to local
- Isolate from the online system
- Data must be written to disk before entering the next stage
- Goal: ensure subsequent processing has a stable data foundation

### Stage 2: Batch Processing

- Invoke AI in the local environment
- Completely isolated from the online system
- Repeatable and rollback-able
- Goal: complete AI non-deterministic operations in a safe sandbox

### Stage 3: Review and Publish

- Human review of processing results
- One-click publish or batch apply
- Record changelog
- Goal: human gatekeeping as the final defense

---

## Core Principles

### Isolate-Process-Verify Closed Loop

```
Online Environment ←→ Local Sandbox ←→ Human Confirmation
       ↓                  ↓                ↓
    Read-only          AI Operations    Publish Decision
```

### Dry Run First

**Always Dry Run before any destructive operation.**

Destructive operations include:
- File overwrite/delete
- Database writes
- API POST/PUT/DELETE
- Email/message sending
- Any irreversible operation

Dry Run checklist:
- [ ] Confirm operation scope (which files/records are affected)
- [ ] Confirm operation content (what specific changes)
- [ ] Confirm rollback capability (backup or version control exists)
- [ ] Confirm execution environment (not production)

---

## Typical Application Scenarios

### Content Translation and Publishing

1. Stage 1: Pull content to be translated to local
2. Stage 2: Invoke AI for batch translation, generate preview
3. Stage 3: Human review then one-click publish

### Data Processing Pipeline

1. Stage 1: Export source data (CSV/JSON)
2. Stage 2: AI processing + validation
3. Stage 3: Import into target system after confirmation

### Batch Code Modification

1. Stage 1: Create an independent branch
2. Stage 2: AI executes modifications + local testing
3. Stage 3: Merge after review

---

## Relationship with Other Skills

- Works with `bestpractice_ai_programming_mindset.md`'s "outcome determinism" principle
- Works with `workflow_parallel_subagents.md`'s parallel processing
- Works with `bestpractice_temporal_info_verification.md`'s verification mechanism

## Changelog

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from 2026-01-07 observation record |
