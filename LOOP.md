# LOOP

Loop config for loop-engineering.

## Workflow
1. Read `STATE.md` each morning.
2. Run the `loop-triage` skill.
3. Append high-priority and watch items to `STATE.md`.
4. Update `Last run` timestamp.
5. Do not auto-fix anything in week one.

## Mode
Triage-only for week one. No automated fixes.

## Schedule
Daily at 09:00 local time.

## Safety Gates
- Do not auto-fix without human approval after triage quality is validated.
- Do not auto-merge PRs.
- Do not touch paths related to auth, payments, secrets, or infrastructure.

See `safety.md` for the full denylist and policies.

## Human Handoff
- Surface items flagged "needs discussion" or that have persisted 3+ days.
- Pause loops before acting on anything ambiguous.

## Cost & Limits
- Daily token cap: 60,000
- Kill switch: if daily spend exceeds cap, pause further loop jobs and notify human.
- Log spend per run in `loop-run-log.md`.

## State
- `STATE.md` is the memory spine.
- Update `Last run`, item status, and human overrides on every run.

## Skills
- `loop-triage` — prioritizes signals
- `loop-verifier` — validates proposed fixes before approval
- `loop-budget` — checks cap before and after each run

## Connectors (MCP)
- MCP not required for this pattern.
- No GitHub/GitLab/Linear connector is configured by default.
- If connectors are added later, they must use minimum permissions: read access for triage, write only for explicit allowlisted paths after verifier approval.

## Worktree Isolation
- When phase 2 auto-fixes are enabled, use git worktrees for fix isolation.
- Implementer and verifier must operate in separate worktrees.
- Implementer cannot mark its own work "done"; verifier confirms scope and tests.
