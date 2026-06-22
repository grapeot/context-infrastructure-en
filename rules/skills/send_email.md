# Skill: Send Email

This skill sends email notifications from a configured workspace mailbox. Default to Resend from the custom agent identity. Gmail and Outlook remain explicit fallbacks for sender-specific cases.

## Default Route

Use Resend by default whenever the user says "send an email", "send with Resend", or asks for a notification without naming a sender.

- Default sender: configured `RESEND_FROM_EMAIL`
- Default recipient: configured workspace notification recipient
- Default transport: `adhoc_jobs/resend_email_skill/`
- Canonical Resend contract: `rules/skills/resend_email.md` and `adhoc_jobs/resend_email_skill/skills/skill_resend_email.md`

Real sends require explicit user intent and the Resend CLI `--confirm-send` flag. Always do a dry run first unless the current user message already includes clear authorization to send for real.

## Resend Usage

From `adhoc_jobs/resend_email_skill/`:

```bash
op run --env-file=.env -- .venv/bin/python -m resend_email_skill.cli send \
  --to user@example.com \
  --subject "Subject" \
  --html "<p>HTML body</p>" \
  --dry-run \
  --format json
```

After reviewing the dry-run payload and only when the user has authorized a real send:

```bash
op run --env-file=.env -- .venv/bin/python -m resend_email_skill.cli send \
  --to user@example.com \
  --subject "Subject" \
  --html "<p>HTML body</p>" \
  --confirm-send \
  --format json
```

For longer messages, write Markdown or HTML to a temporary file and pass `--body-file`. Keep message files out of git if they contain private content.

## Received Email and Markdown Export

Resend receiving can list recent inbound email, retrieve a single message, and export messages to local Markdown. Use this when an agent needs to inspect received Resend email in a file-based workflow.

```bash
op run --env-file=.env -- .venv/bin/python -m resend_email_skill.cli received list --limit 20 --format json

op run --env-file=.env -- .venv/bin/python -m resend_email_skill.cli received export-md <email_id> \
  --output-dir data/received/markdown \
  --format json

op run --env-file=.env -- .venv/bin/python -m resend_email_skill.cli received export-all-md \
  --limit 20 \
  --output-dir data/received/markdown \
  --format json
```

The default `data/` directory inside `adhoc_jobs/resend_email_skill/` is gitignored. Do not commit received email bodies, raw MIME, attachments, or local exports.

## Gmail Fallback

Use Gmail only when the user explicitly asks to send via Gmail, when Resend is unavailable, or when an old workflow specifically depends on Gmail app-password SMTP behavior.

Canonical Gmail CLI:

```bash
python3 tools/send_email_gmail.py "Subject" "<p>Body</p>" --to user@example.com --html
```

Backward-compatible wrapper:

```bash
python3 tools/send_email_to_myself.py "Subject" "<p>Body</p>" --to user@example.com --html
```

The Gmail CLI still supports Markdown files, attachments, and CC. If your private workspace uses a notification address such as Pushover, configure it locally rather than committing it to this public reference repo. Resend does not automatically CC any notification channel unless the caller adds `--cc` explicitly.

Unified Email / unified client outputs are an explicit exception to Pushover notification behavior. Self-thread notes, test emails, and local pipeline result emails should go only to the configured mailbox recipient and should not CC Pushover. This keeps email automation results in the relevant mail thread or local report instead of duplicating them into the notification channel.

## Outlook Fallback

Use Outlook only when the user explicitly asks for Outlook or both Resend and Gmail are unsuitable. Outlook sending uses `adhoc_jobs/outlook_skill/`:

```bash
cd adhoc_jobs/outlook_skill
.venv/bin/python -m outlook_skill.cli mail send --to user@example.com --subject "Subject" --body-file /path/to/body.md --body-format markdown --format json
```

## Rules

- Default to Resend and the configured `RESEND_FROM_EMAIL` identity.
- Send HTML email by default. Plain text is only for explicit user requests or tests.
- Use `--dry-run` before real Resend sends unless the user has already explicitly authorized sending.
- Use `--confirm-send` for every real Resend send.
- Keep generated email body files, received email exports, attachments, and raw MIME out of git.
