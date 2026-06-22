---
title: API Key Management Best Practice (1Password CLI)
category: BestPractice
tags: [security, api-key, 1password, op-cli, environment-variables]
difficulty: Medium
related_projects: [dotfiles, debianinit]
created: 2026-02-13
updated: 2026-02-13
---

# API Key Management Best Practice (1Password CLI)

This document summarizes how to securely manage and inject API keys using the 1Password CLI (`op`) in local development and production environments, avoiding plaintext leaks and long-term persistence risks.

## 1. Core Principles

1. Do not store plaintext keys in `.zshrc`, repository files, or script parameters.
2. In local development, use `op run --env-file ... -- <command>` for on-demand injection.
3. In production, use machine identities (Service Accounts); do not rely on desktop app fingerprint prompts.
4. Keys should have least privilege, be rotatable, and be revocable; prioritize rotation after a leak.

## 2. Recommended Pattern for Local Development (Mac)

### 2.1 Use Secret References Instead of Plaintext

Store references in the local file `~/.config/op/env.secrets`:

```dotenv
OPENAI_API_KEY=op://dev/dev-api-keys/openai_api_key
TAVILY_API_KEY=op://dev/dev-api-keys/tavily_api_key
GEMINI_API_KEY=op://dev/dev-api-keys/gemini_api_key
```

This file contains no plaintext keys and can be safely stored locally (recommended permissions `600`).

### 2.2 Command-Level Injection

```bash
op run --env-file ~/.config/op/env.secrets -- python app.py
op run --env-file ~/.config/op/env.secrets -- nvim
```

Advantage: only affects the target process, does not pollute the current shell's global environment variables.

### 2.3 About Fingerprint/Password Authorization

A 1Password authorization prompt appearing locally is normal security behavior. It typically triggers only when 1Password is locked, not on every command. Frequency is determined by the auto-lock policy.

## 3. Recommended Pattern for Production (Non-Interactive)

The production goal is "auto-restartable, unattended" and should not depend on desktop authorization.

Recommended approach:

1. Create a 1Password Service Account (read-only, scoped to a specific vault).
2. Securely store `OP_SERVICE_ACCOUNT_TOKEN` on the server (e.g., systemd EnvironmentFile).
3. In the startup script, use `op read` to pull keys, then start the process manager (e.g., PM2).

Illustration:

```bash
export OPENAI_API_KEY="$(op read 'op://dev/dev-api-keys/openai_api_key')"
pm2 start ecosystem.config.js --env production --update-env
pm2 save
```

## 4. Anti-Patterns to Avoid

1. `export API_KEY=...` in plaintext in `.zshrc`.
2. Passing keys directly in command-line arguments (will land in history, can be inspected by other processes).
3. Mixing the same set of keys across dev/staging/prod.
4. Only doing "import" without "rotation," making historical leaks permanently valid.

## 5. Minimum Implementation Checklist

1. Clean plaintext keys from dotfiles.
2. Create a `dev-api-keys` item with unified field naming (snake_case).
3. Use `~/.config/op/env.secrets` + `op run`.
4. Configure Service Account token injection chain for production.
5. Establish a regular key rotation process and a leak emergency procedure.

## 6. Calling API Keys in Code

In Python/Node scripts, do not hardcode or read `.env`; instead, retrieve via `op read`:

```python
import subprocess
import os

def get_api_key(service: str) -> str:
    """Retrieve API key from 1Password.
    
    Args:
        service: e.g., 'tavily_api_key', 'openai_api_key'
    """
    # Prefer environment variable (CI/CD scenario)
    env_key = os.environ.get(service.upper())
    if env_key:
        return env_key
    
    # Read from 1Password
    result = subprocess.run(
        ["op", "read", f"op://dev/dev-api-keys/{service}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

# Usage
api_key = get_api_key("tavily_api_key")
```

**Key points**:
1. Check environment variables first (CI/CD compatibility)
2. Local development uses `op read`
3. Vault path unified as `op://dev/dev-api-keys/<service>`
