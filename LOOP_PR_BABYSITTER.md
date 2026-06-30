# PR Babysitter Loop

## Schedule
- Every 5 minutes during active sprints; every 15 minutes otherwise

## Scope
- Open PRs targeting main branch
- Allowlist: non-auth, non-payments, non-secrets, non-infra PRs only

## Safety Gates
- No auto-merge by default.
- Denylist: auth, payments, secrets, infra (see `safety.md`).
- Escalate after 3 attempts per PR.

## Skills
- `pr-review-triage` — scans PRs
- `minimal-fix` — applies small fixes in worktree
- `loop-verifier` — validates fix before proposal

## State
- `pr-babysitter-state.md` — watched PRs, attempt counts, escalations

## Bot Identity
- PR comments must be signed: `🤖 Loop Engineering — PR Babysitter`

## Human Handoff
- New infrastructure or security-related PRs.
- Repeated failures (>3 attempts).
- Any PR modifying denylist paths.

## Cost & Limits
- 5m cadence cap: 25k tokens per run
- Max auto-fix attempts per PR: 3

## Observability
- Log runs to `loop-run-log.md`.
