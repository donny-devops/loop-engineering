# Post-Merge Cleanup Loop

## Schedule
- Daily at 10:00 local time

## Scope
- Branch: main
- Window: last 7 days
- Fix type: doc/link/typo/formatting only

## Safety Gates
- No refactors without human ticket.
- Denylist paths: feature flags, auth paths (see `safety.md`).

## Skills
- `post-merge-scan` — identifies candidates
- `minimal-fix` — applies small fixes in isolated worktree where applicable
- `loop-verifier` — validates fixes

## State
- `post-merge-state.md` — cleanup backlog

## Human Handoff
- Escalate refactors.
- Pause on denylist hits.

## Cost & Limits
- Daily cap: 40k tokens
- No auto-PRs

## Observability
- Log runs to `loop-run-log.md`.
