# Dependency Sweeper Loop

## Schedule
- Every 6 hours during active sprints; daily otherwise

## Scope
- Manifests: `package.json`
- Lockfiles: `package-lock.json`
- Triage output to `dependency-sweeper-state.md`

## Safety Gates
- Patch-only auto-fix in worktree + verifier (`npm ci && npm test` or equivalent).
- Escalate majors and high-sev CVEs.
- Respect denylist packages.

## Skills
- `dependency-triage` — scans manifests/lockfiles
- `minimal-fix` — patches dependencies in worktree
- `loop-verifier` — validates install + tests

## State
- `dependency-sweeper-state.md` — in-flight updates, denylist

## Human Handoff
- Major upgrades require human approval.
- High-sev CVEs: pause and notify.

## Cost & Limits
- 6h cadence cap: 30k tokens per run
- Max auto-PRs per day: 2

## Observability
- Log runs to `loop-run-log.md`.
