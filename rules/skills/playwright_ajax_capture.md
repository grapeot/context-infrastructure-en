# Playwright Ajax Capture Skill

## Metadata

- **Type**: Workflow
- **Use case**: Reverse-engineer a logged-in web app's internal API by capturing its ajax/XHR calls (URL, method, headers, payload, response), then replay them with plain HTTP — bypassing Admin API restrictions or enabling E2E automation
- **Created**: 2026-08-06
- **Battle-tested**: Used to reverse-engineer 9 Circle community internal API endpoints (notifications, post CRUD, comments, chat, image upload), all replayed successfully with plain requests + cookie + CSRF

## Goal

Let an AI agent intercept and record all fetch/XHR calls from a logged-in Playwright/CDP browser session, reverse-engineer the full internal API contract (endpoint, method, params, body, auth headers), and replay the same calls with plain `requests` — no Admin API key, no ad-hoc raw JS.

## When to Use

- You want to call a web app's internal API as a regular member, but there's no official API documentation
- Admin API key is too dangerous or unavailable, and browser session auth (cookie + CSRF) can substitute
- You need to turn a web UI operation (list posts, create post, delete post) into a reproducible HTTP call

## When Not to Use

- The target app has public REST API docs — read docs instead
- You only need to read a public page without auth — use webfetch
- The operation is pure client-side computation with no ajax — capturing ajax is pointless

## Available Resources

- **`pw-test` CLI**: at `/Users/grapeot/co/knowledge_working/adhoc_jobs/playwright_test_skill/.venv/bin/pw-test`, provides `goto`/`click`/`eval`/`snapshot`/`storage` CDP primitives (see `rules/skills/playwright_e2e.md`)
- **CDP Chrome**: `--remote-debugging-port=9222 --user-data-dir=/tmp/pw_<purpose>_profile`, user logs in manually
- **Playwright Python**: same venv, `from playwright.async_api import async_playwright` — for CDP-level HttpOnly cookie extraction and persistent network monitoring

## Methodology

### 1. Start CDP Chrome and let the user log in

```bash
rm -rf /tmp/pw_<purpose>_profile
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 --user-data-dir=/tmp/pw_<purpose>_profile \
  --no-first-run --no-default-browser-check > /dev/null 2>&1 &
```

Navigate to the target site and let the user log in manually. SSO/OTP flows are a black box to the agent — do not attempt to automate login.

### 2. Persistent network monitoring (preferred approach)

**Do not use `window.fetch` monkey-patching** — page refreshes reset `window.__captured`, losing all intercepted records. Instead, use Playwright Python's `page.on("request")` / `page.on("response")`, which operates at the CDP protocol level and survives page refreshes:

```python
import asyncio, json
from playwright.async_api import async_playwright

NOISE = ("segment", "sentry", "amplitude", "google-analytics", "googletagmanager",
         "pendo", "vwo", "stripe", "facebook", "doubleclick", "hotjar", "cookieyes",
         "bugsnag", "packs/", "analytics/track", "active_storage", "assets-v2")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        page = ctx.pages[0]

        captured = []

        def on_request(req):
            if any(n in req.url for n in NOISE):
                return
            entry = {"url": req.url, "method": req.method}
            try:
                pd = req.post_data
                entry["reqBody"] = pd[:5000] if pd else None
            except Exception:
                entry["reqBody"] = "[binary]"
            captured.append(entry)

        def on_response(resp):
            for entry in reversed(captured):
                if entry["url"] == resp.url and entry["method"] == resp.request.method and "status" not in entry:
                    entry["status"] = resp.status
                    break

        page.on("request", on_request)
        page.on("response", on_response)

        # ... perform UI actions: page.goto(), page.click(), page.fill(), etc.
        await page.goto("https://target-domain.com/feed", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        await page.click("button:has-text('New post')")
        # ... fill and submit

        print(json.dumps(captured, indent=2, ensure_ascii=False))

asyncio.run(main())
```

### 3. fetch monkey-patch (fallback, SPA-internal navigation only)

If you only need to capture ajax during SPA-internal navigation (no page refresh), you can inject a fetch hook via `pw-test eval`:

```javascript
(function(){
  window.__captured = window.__captured || [];
  if (window.__fetchHooked) return "already hooked";
  window.__fetchHooked = true;
  const orig = window.fetch;
  window.fetch = function(...args){
    const url = typeof args[0]==="string" ? args[0] : (args[0] && args[0].url);
    const init = args[1] || {};
    let bodyDesc = null;
    if (init.body) {
      if (typeof init.body === "string") bodyDesc = {type:"string", value: init.body.slice(0,2000)};
      else if (init.body instanceof FormData) {
        bodyDesc = {type:"FormData", entries: {}};
        for (const [k,v] of init.body.entries()) {
          if (v instanceof File) bodyDesc.entries[k] = {type:"File", name:v.name, size:v.size, mime:v.type};
          else bodyDesc.entries[k] = String(v).slice(0,500);
        }
      } else bodyDesc = {type: init.body.constructor.name};
    }
    const rec = {url, method: init.method||"GET", reqBody: bodyDesc, t: Date.now()};
    window.__captured.push(rec);
    return orig.apply(this, args).then(async resp=>{
      try { const c = resp.clone(); if ((resp.headers.get("content-type")||"").includes("json")) rec.resBody = (await c.text()).slice(0,1000); } catch(e){}
      rec.status = resp.status;
      return resp;
    });
  };
  return "hooked";
})()
```

**But note**: if the operation triggers a page refresh (e.g., form submit), `window.__captured` is lost. In practice, "Save" buttons in some SPAs trigger full-page reloads. If this happens, switch immediately to approach 2 (CDP `page.on`).

### 4. Export HttpOnly cookies for plain HTTP replay

`document.cookie` cannot access HttpOnly cookies (e.g., `remember_user_token`, `_circle_session`). Use Playwright Python's CDP `context.cookies()` to export the full cookie header:

```python
import asyncio, json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        cookies = await ctx.cookies()
        relevant = [c for c in cookies if "target-domain.com" in c.get("domain","")]
        cookie_header = "; ".join(f'{c["name"]}={c["value"]}' for c in relevant)
        csrf = next((c for c in relevant if c["name"]=="csrf_token"), None)
        print(json.dumps({"cookie_header": cookie_header, "csrf_token": csrf["value"] if csrf else None}))

asyncio.run(main())
```

### 5. Determine the auth mechanism

Common internal API auth combinations:

- **Cookie + CSRF**: Most common. GET requests only need the cookie; POST/PUT/DELETE also need an `X-CSRF-Token` header (value usually from a cookie named `csrf_token` or `<meta name="csrf-token">`). Verify: send a GET with `fetch` + `credentials:"include"` without an explicit Authorization header — if it returns 200, cookie-only is sufficient.
- **Bearer JWT**: `Authorization: Bearer <jwt>` header. JWT is usually in localStorage or exchanged from a cookie by the frontend. If cookie-only GET fails and Authorization is needed, find the JWT from `pw-test storage` or intercepted request headers.
- **Both required**: Cookie for session, JWT for API auth. Rare but exists. In practice, Circle's GET works with cookie-only — JWT is redundant.

Verify the minimum auth combination first: if cookie-only GET works, don't add JWT; if mutation fails, add CSRF; if that still fails, check Authorization.

### 6. Verify with plain requests

After extracting cookie + CSRF, replay one call with `requests` to confirm it works outside the browser:

```python
import requests
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cookie": cookie_header,
    "X-CSRF-Token": csrf_token,  # only for mutations
    "Referer": "https://target-domain.com/",
    "User-Agent": "Mozilla/5.0 ...",
}
r = requests.get("https://target-domain.com/internal_api/...", headers=headers)
```

Only after `requests` verification passes should you write it into a CLI. Write an end-to-end verification script covering all reverse-engineered endpoints (create → update → reply → list → delete) and run it in one shot.

## Known Pitfalls

### 1. Page refresh resets window.__captured

**Symptom**: Injected fetch hook, clicked Save, but `__captured` is empty.

**Cause**: Save triggered a full-page reload (form submit), resetting the JS context. `window.__captured` and `window.__fetchHooked` are gone.

**Fix**: Don't rely on `window.__captured`. Use Playwright Python's `page.on("request")` / `page.on("response")`, which operates at the CDP protocol level and survives page refreshes.

### 2. SSO direct URLs get blocked

**Symptom**: `pw-test goto "https://app/.../space/123"` returns "We were unable to process your request".

**Cause**: SSO validates referer/origin; deep-link jumps are blocked.

**Fix**: `goto` the feed/home page first, then click through UI navigation to the target space, letting the referer chain build naturally.

### 3. document.cookie can't access HttpOnly cookies

**Symptom**: `pw-test eval 'document.cookie'` is missing `remember_user_token`, `_circle_session`, and other critical session cookies.

**Cause**: HttpOnly cookies are invisible to JS by design.

**Fix**: Use Playwright Python `context.cookies()` (via CDP protocol, can access HttpOnly), not `document.cookie`.

### 4. set_key duplicates cause repeated .env keys

**Symptom**: `.env` has the same key on multiple lines (e.g., two `CIRCLE_CLIENT_COOKIE=` lines).

**Cause**: python-dotenv's `set_key` appends instead of overwriting in some modes.

**Fix**: Dedup by key (keep last occurrence) before updating `.env`, or clear the target key before setting.

### 5. Analytics noise drowns out business APIs

**Symptom**: 90% of captured records are segment/pendo/google-analytics/sentry/googletagmanager requests.

**Fix**: Hardcode an exclusion list: `segment`, `sentry`, `amplitude`, `google-analytics`, `googletagmanager`, `pendo`, `hotjar`, `vwo`, `doubleclick`, `facebook.com`, `stripe.com` (unless the business is payments), `bugsnag`, `packs/js`, `analytics/track`, `active_storage`, `assets-v2`.

### 6. TipTap/ProseMirror editors: innerHTML doesn't trigger React state

**Symptom**: Set editor content via `el.innerHTML = '<p>content</p>'`, click Post button, but no network request fires.

**Cause**: TipTap/ProseMirror uses React state management. Setting `innerHTML` directly doesn't trigger React's `onChange`/`input` state update — React thinks the editor is empty, so the submit button doesn't fire.

**Fix**: Use `page.keyboard.type(text, delay=30)` to type via the keyboard, which triggers React state properly. First `page.click(editor)` to focus, then `keyboard.type`. To clear existing content: `keyboard.press("Meta+A")` + `keyboard.press("Backspace")`.

### 7. POST response may not include an id field

**Symptom**: After POSTing a resource, the response has no `id` field — only `creation_uuid` or similar. If you then use this non-existent `id` as a parameter in a subsequent request (e.g., `parent_message_id`), the parameter becomes None and the request behaves unexpectedly (e.g., thread reply becomes a standalone message).

**Cause**: Some internal APIs return an async processing token (`creation_uuid`), not the resource ID. The resource ID is generated after server-side processing completes.

**Fix**: Don't use the response's `id` directly after POST. If you need the new resource's ID, send a GET (fetch list) after POST and find the just-created resource by content match. Or follow the pattern from existing projects (like translation bots): after sending a message, immediately fetch messages and find the new message's numeric ID by content matching.

### 8. CSRF token changes after page refresh

**Symptom**: CSRF token saved in `.env` suddenly stops working; mutation requests return 403.

**Cause**: The `csrf_token` cookie may regenerate on page refresh.

**Fix**: Periodically update the CSRF value in `.env`. If mutation fails with 403, re-export cookies + CSRF via CDP.

### 9. Wrong parent message ID makes thread reply invisible

**Symptom**: API returns 202 and `parent_message_id` is echoed correctly, `fetch_replies` can find the reply, but the browser UI's thread panel doesn't show it.

**Cause**: You sent the thread reply to the wrong parent message ID. The API succeeded (the reply is indeed linked to that parent), but you opened a different message's thread panel in the UI.

**Fix**: Before sending a thread reply, confirm the parent message's real ID via API. Don't infer the ID from the POST response's `creation_uuid`. When verifying in the UI, make sure you open the thread panel for the same message you replied to.

## Acceptance Criteria

- [ ] CDP Chrome is running and the user is logged in (`pw-test url` returns a logged-in URL, not a login page)
- [ ] Using CDP `page.on("request"/"response")` for persistent network monitoring (not `window.__captured`)
- [ ] After triggering the target operation, captured records contain business API calls (not analytics noise)
- [ ] Extracted endpoint URL, method, key params, request body schema, and response schema highlights
- [ ] HttpOnly cookies exported via Playwright Python CDP
- [ ] Plain `requests` replay succeeds (status 200/201/202, response body structure matches the browser's)
- [ ] If a newly created resource's ID is needed, POST then GET to confirm the ID (don't use `creation_uuid` as ID)
- [ ] Credentials updated to `.env` (if applicable), requests mode works

## Relationship to other skills

- **`playwright_e2e.md`**: This skill is a specialization — the E2E skill focuses on "reproduce a UI flow as a test", while this skill focuses on "reverse-engineer the ajax contract and replay with plain HTTP". They share CDP Chrome startup, pw-test CLI, and stale-profile avoidance pitfalls.
- **`bestpractice_gui_automation.md`**: General GUI automation methodology. This skill is the concrete implementation of its "turn interfaces without APIs into programmable interfaces" principle.