---
title: GitHub Actions to Koyeb Deployment Guide
category: Deployment
tags: [github-actions, koyeb, docker, ci-cd]
difficulty: Medium
related_projects: []
created: 2025-02-12
updated: 2025-02-12
---

# GitHub Actions to Koyeb Deployment Guide

Automate deployment to Koyeb via GitHub Actions after tests pass. Applicable to any Dockerized application.

## Core Principles

1. **Disable Koyeb Autodeploy** — deployment timing is controlled by GitHub Actions
2. **`needs` gating** — deploy only after all tests pass
3. **Explicitly specify `git-builder: "docker"`** — otherwise Koyeb detects Python/Node files and falls back to buildpack

## Prerequisites

- An app and service created in the Koyeb console, with **Autodeploy disabled** (Settings → Source → Autodeploy)
- A `Dockerfile` at the project root containing `EXPOSE` and `CMD`
- The `Dockerfile` `CMD` uses `${PORT:-8000}` to adapt to Koyeb's dynamic port

## Configuration Steps

### 1. GitHub Secret

In the GitHub repo Settings → Secrets and variables → Actions, add:

| Name | Value |
|------|-------|
| `KOYEB_API_TOKEN` | From Koyeb console Settings → API Tokens |

### 2. Get App Name and Service Name

Via the console URL (`https://app.koyeb.com/apps/<app-name>`) or the CLI:

```bash
koyeb apps list
koyeb services list --app <app-name>
```

### 3. Workflow Configuration

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # ... your test steps

  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t test-image .

  deploy:
    needs: [test, docker]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/master'
    steps:
      - uses: actions/checkout@v4

      - name: Install Koyeb CLI
        uses: koyeb-community/koyeb-actions@v2
        with:
          api_token: "${{ secrets.KOYEB_API_TOKEN }}"

      - name: Deploy
        uses: koyeb/action-git-deploy@v1
        with:
          app-name: "<app-name>"                # ← replace
          service-name: "<service-name>"         # ← replace
          git-branch: "master"
          git-builder: "docker"                  # ⚠️ must be explicit
          git-docker-dockerfile: "Dockerfile"    # ⚠️ must be explicit
          service-regions: "na"                  # na / eu / ap
          service-ports: "8000:http"             # container port:protocol
          service-routes: "/:8000"               # route path:port
```

## Parameter Quick Reference

| Parameter | Format | Notes |
|-----------|--------|-------|
| `git-builder` | `"docker"` | Must be `docker`; otherwise buildpack may be used |
| `git-docker-dockerfile` | `"Dockerfile"` | Dockerfile path (relative to repo root) |
| `service-regions` | `"na"` | `na` / `eu` / `ap`; cannot mix continental and metropolitan regions |
| `service-ports` | `"8000:http"` | `port:protocol`; protocol is `http` or `tcp` |
| `service-routes` | `"/:8000"` | `path:port`; subpaths like `"/api:8000"` |

## Dockerfile Examples

```dockerfile
# Python FastAPI
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"
```

```dockerfile
# Node.js
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD sh -c "node server.js --port ${PORT:-3000}"
```

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Logs show `Installing Python 3.x` instead of Docker build | `git-builder: "docker"` not specified | Add `git-builder: "docker"` |
| `cannot mix continental and metropolitan regions` | Mixed `na` with `fra`, etc. | Use only continental regions (`na`/`eu`/`ap`) |
| `no command to run your application` | Dockerfile missing `CMD` | Add a `CMD` instruction |
| 502 errors | Port or route config mismatch | Confirm `service-ports` matches `EXPOSE`; app listens on `0.0.0.0` |
| Deploy job not triggered | Autodeploy not disabled / not a push to main branch | Disable Autodeploy; check the `if` condition |

## References

- [koyeb/action-git-deploy](https://github.com/koyeb/action-git-deploy)
- [koyeb-community/koyeb-actions](https://github.com/koyeb-community/koyeb-actions)
- [Koyeb Build & Deploy docs](https://www.koyeb.com/docs/build-and-deploy)