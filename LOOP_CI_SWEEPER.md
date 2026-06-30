# CI Sweeper Loop

## Schedule
- Every 15 minutes

## Scope
- CI on main branch
- Failure classification: real vs flake

## Safety Gates
- No retry-based flake silencing.
- Escalate after 3 attempts on same failure.
- Denylist paths from `safety.md`.

## Skills
- `ci-triage` — classifies failures
- `minimal-fix` — fixes self-contained failures
- `loop-verifier` — validates fix in isolated worktree

## State
- `ci-sweeper-state.md` — failures, flakes, attempt counts

## Human Handoff
- New infrastructure failures.
- Repeated failures (>3 attempts).

## Cost & Limits
- 15m cadence cap: 20k tokens per run
- Max consecutive auto-fix attempts: 3

## Observability
- Log runs to `loop-run-log.md`.
