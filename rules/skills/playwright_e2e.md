# Playwright E2E Testing Methodology

## Metadata

- **Type**: Workflow
- **Applicable scenarios**: When you need to run end-to-end tests on systems with a frontend UI, especially those involving third-party SSO (Logto/Auth0 etc.), multi-step registration/login flows, email verification codes, or other complex interactions
- **Created**: 2026-06-27

## What This File Is For

Teaching AI agents how to efficiently build reliable E2E tests with Playwright. The core methodology is "walk through it manually first, then automate" — don't jump straight into writing automation scripts and brute-forcing your way through. Instead, use CDP mode to observe page behavior step by step, understand the complete flow, then reproduce it programmatically.

## Core Methodology: Manual First, Then Automate

### Why You Can't Just Write Automation Scripts Directly

The biggest pitfall in E2E testing isn't writing code — it's not knowing what the page will do next. Third-party SSO login flows are especially tricky: popups, modals, multi-step forms, redirect chains, SDK internal state — these are often poorly documented, and you only see the full picture by actually running through it once.

The problem with writing automation scripts directly: when the script gets stuck at a step, you don't know whether the selector is wrong, the page hasn't loaded yet, the flow has changed, or this step always existed but the script didn't handle it. You end up repeatedly tweaking selectors, adding waits, and guessing page state — extremely inefficient.

### CDP Manual Debugging Method

Chrome DevTools Protocol (CDP) lets Playwright connect to an already-open Chrome instance. You can operate the page step by step (goto, click, fill), and after each step use snapshot to view the complete DOM state (URL, body text, all inputs, all buttons, all links). This is far more efficient than a headless script because you can see the actual state of the page at each step.

**Launch CDP Chrome:**

```bash
pkill -f "remote-debugging-port=9222" 2>/dev/null; sleep 1
nohup "<chromium_path>" --remote-debugging-port=9222 --disable-extensions \
  --user-data-dir=/tmp/playwright_debug_profile about:blank > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:9222/json/version | head -3  # Verify CDP is ready
```

The Chromium path on macOS is typically `~/Library/Caches/ms-playwright/chromium-XXXX/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`.

**Step-by-step helper script:**

Write a single-file Python script (e.g., `/tmp/pw_step.py`) that supports subcommands like `goto`, `click`, `fill`, `snapshot`, `wait`, `reload`, `storage`, `eval`. Each invocation connects to CDP, executes one operation, prints the result, and disconnects. This lets you debug in the terminal as if you were operating the browser line by line.

**The snapshot subcommand** is the core — it prints the current page's URL, title, body text (first 1500 characters), all inputs (name/type/visible/value), all buttons (text/visible), and all links (text/href/visible). This gives you a complete view of the page state without needing screenshots.

### From Manual to Automated Flow

1. **Launch CDP Chrome**, use the helper script to walk through the entire flow step by step
2. **Record each step**: URL changes, selectors for elements that need interaction, page navigation conditions
3. **Map out all branches**: new user vs existing user, first login vs subsequent login, register vs sign-in flows for different SSO apps
4. **Reproduce programmatically**: translate manual steps into a Playwright script, using `wait_for` + selectors instead of fixed `wait_for_timeout`
5. **After it works, update this skill**: record newly discovered pitfalls in the "Known Pitfalls" section

## Acceptance Criteria

- E2E tests run completely locally without getting stuck at any intermediate step
- Tests cover the complete user journey (login + core operations for all roles)
- Each step's wait is based on element state (`wait_for` selector), not fixed timeouts
- Known limitations (e.g., uncontrollable third-party onboarding pages) are clearly documented
- On test failure, preserve the scene (don't run cleanup); on test pass, auto-cleanup

## Available Resources

- Playwright Python (`pip install playwright && python -m playwright install chromium`)
- CDP mode: `playwright.chromium.connect_over_cdp("http://localhost:9222")`
- unified_email (if you need to extract verification codes from email)
- Logto Management API (if you need to create/delete test users, assign roles)

## Known Pitfalls

### 1. SSO SDK callback not automatically handled

**Symptom:** After SSO login completes, it redirects back to the frontend callback URL (e.g., `/callback?code=...`), but the page shows a not-logged-in state — the SDK didn't handle the token exchange.

**Root cause:** Many SSO SDKs (e.g., `@logto/react`) require explicitly calling the callback handling hook (e.g., `useHandleSignInCallback`). The SDK doesn't automatically detect callback URLs and handle them.

**Fix:** Call the SDK-provided callback hook in the frontend root component. For SPAs (without routing), the callback and home page are the same component, and the hook automatically handles it when the URL matches.

### 2. JWT algorithm mismatch

**Symptom:** After the frontend gets the SSO token and calls the API, the backend returns 401 "Invalid token".

**Root cause:** The SSO provider may use a non-standard algorithm (e.g., Logto uses ES384), but the backend JWT validation is only configured for common ones like RS256/ES256.

**Fix:** Decode the token header to check the `alg` field, and ensure the backend `jwt.decode` `algorithms` parameter includes it.

### 3. JWT issuer has a suffix

**Symptom:** JWT validation throws `InvalidIssuerError`.

**Root cause:** The `issuer` returned by the SSO provider's OIDC discovery endpoint may have an `/oidc` suffix (e.g., `https://auth.example.com/oidc`), but the configured `issuer` doesn't have the suffix (e.g., `https://auth.example.com`).

**Fix:** Append `f"{settings.issuer}/oidc"` during backend JWT validation, or read the issuer value directly from the OIDC discovery endpoint.

### 4. Resource access token doesn't contain email/roles

**Symptom:** Backend JWT validation passes, but the token claims don't include email or roles — the backend can't identify the user.

**Root cause:** The SSO resource access token (audience = API URL) only contains standard JWT claims like `sub`, `iss`, `aud`, `exp` — it doesn't contain OIDC scope claims (email, profile). The OIDC userinfo endpoint also doesn't accept resource tokens.

**Fix:** Use the Management API to look up user info via `sub`. `GET /api/users/{sub}` for email/name, `GET /api/users/{sub}/roles` for roles. Requires M2M credentials (app_id + app_secret).

### 5. New user login has multiple modals

**Symptom:** After submitting the verification code, the page doesn't navigate — it appears stuck.

**Root cause:** On first login, new users see multiple modals from the SSO:
1. "No account found, Create new one?" → Need to click Continue
2. "Agree to Terms of Use and Privacy Policy" → Need to click Agree
3. Set password page → Need to fill in password and Save
4. Extra-profile page ("Tell us about yourself") → Need to fill in Name and Continue

**Fix:** After submitting the verification code, check and handle each modal/page in sequence. Use `div.ReactModalPortal` to detect modals, and use button selectors within the modal to click. Users created via Management API also go through Set password (because no password is preset), but don't get the "No account found" modal.

### 6. Register vs Sign-in flows differ

**Symptom:** When a guest registers via the signup URL, the page behavior after submitting the verification code differs from sponsor/admin login.

**Root cause:** In the sign-in flow, after submitting the verification code, a "No account found" modal may appear (if the user doesn't exist). In the register flow, this modal doesn't appear (since you're creating a new account), and after submitting the code it goes directly to Set password.

**Fix:** Use different handling logic for register and sign-in. The register flow doesn't need to check for the "No account found" modal — go directly to the Set password page.

### 7. Third-party onboarding pages are uncontrollable

**Symptom:** After SSO registration completes, it redirects to a third-party community platform (e.g., Circle.so) profile onboarding page, and form submission fails.

**Root cause:** The third-party platform's onboarding form is a Rails form (or similar), requiring a CSRF token + POST submission. Using JS `form.submit()` turns it into a GET request, causing failure.

**Fix:** If the core functionality (account creation, access group authorization) has been verified, the onboarding form is out of scope for E2E. Reaching that page means registration is complete — don't attempt to submit the third-party form.

### 8. Fixed timeout is insufficient

**Symptom:** The automation script waits 3 seconds at a step then checks for an element, but the page hasn't finished loading — reports "not found".

**Root cause:** API calls after SSO login may go through the Management API (to look up user info), with unpredictable timing. A fixed 3 seconds may be insufficient under certain network conditions.

**Fix:** Use `locator.wait_for(timeout=30000)` to wait for the target element to appear, instead of a fixed `wait_for_timeout(3000)` followed by a check. For "loading" state elements, use `wait_for(state="detached")` to wait for them to disappear.

### 9. Can't use test headers for backend verification in JWT mode

**Symptom:** The E2E test's backend verification step calls the API and returns 401.

**Root cause:** When the backend runs in JWT auth mode, it only accepts real JWT tokens — it doesn't recognize test headers (`X-Test-User-Email` etc.).

**Fix:** For backend verification steps, read the database directly or call the Service layer instead of going through the HTTP API. Alternatively, extract the token from the frontend Playwright session and use the real token to call the API.

## Relationship to Existing Skills

- `bestpractice_gui_automation.md` — General methodology for GUI automation
- `bestpractice_staged_approach.md` — Staged work approach; E2E debugging naturally fits "isolate first, then handle"
- `workflow_parallel_subagents.md` — If you need to test multiple role journeys simultaneously, use parallel subagents