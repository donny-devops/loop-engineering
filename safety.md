# Safety

## Denylist

Never auto-edit, auto-fix, or auto-merge changes touching:
- Authentication, authorization, session management
- Payments, billing, invoicing
- Secret storage, credentials, tokens, environment files
- Infrastructure / deployment / networking
- Data deletion or retention logic
- Legal / compliance wording

## Auto-Merge Policy

- Do not enable auto-merge by default.
- If enabled, restrict to docs-only and chore-only paths with an explicit allowlist.

## Flake Policy

- Do not “fix” intermittent failures by adding retries or disabling tests.
- Require a human decision before changing timeouts or thresholds.

## Secrets Policy

- Never commit secrets or `.env` files.
- Rotate any secret accidentally exposed.
