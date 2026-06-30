# STATE

Project: loop-engineering
Repo: C:\Users\adoni\OneDrive\Desktop\Projects\loop-engineering
Primary Owner: adoni

Last run: 2026-06-29
Frequency: daily (1d)

## Project Name
Loop Engineering

## Daily Triage Loop
Goal: Start each day with a prioritized, actionable picture of what needs attention — without manually checking CI, issues, PRs, and chat.

Scheduling
- `/loop 1d` for morning triage (report-only recommended for first 1–2 weeks)
- `/loop 2h` during active sprints for faster signal
- GitHub Actions: `0 8 * * 1-5` for teams without a TUI

Required Skills
- `loop-triage` — reads CI, issues, commits, chat; produces prioritized findings
- `minimal-fix` (optional, phase 2) — drafts small fixes for obvious failures
- Reviewer sub-agent or skill (optional, phase 2) — verifies proposed fixes

State
- Use `STATE.md` as the memory spine; update only the triage skill appending findings here
- Fields to update every run:
  - `Last run` timestamp
  - Item status + last action taken
  - Human decisions that overrode the loop

How the Loop Runs (Typical Cycle)
1. Scheduler fires (morning or interval).
2. Triage skill ingests: CI failures (24h), open issues/tickets, recent commits, prior `STATE.md`.
3. High-priority items appended to state with suggested next action.
4. (Phase 2) For small, self-contained failures: open worktree → implementer → verifier.
5. (Phase 3) Connectors update PRs/tickets; ambiguous items flagged for human.
6. Prune resolved/merged items from state.
7. Record post-run critique in state: false positives, repeated items, re-prioritized or dropped items, and one adjustment for next run.

Post-Run Critique
- High-noise items
- False positives
- Items that should be deprioritized
- Human-review friction
- One change to improve the next cycle

Verification Strategy
- Phase 1 (report-only): Human reads `STATE.md` — no auto-action verification needed.
- Phase 2+: Never let implementer mark work done; verifier confirms fix scope and tests.
- Triage skill must not invent architectural work — signal only.

Human Handoff Points
- Design decisions or multi-file refactors
- Security, auth, payments, infrastructure
- Items flagged "needs discussion" in triage output
- Anything the loop has surfaced 3+ days without resolution

Failure Modes & Mitigations
- Triage creates noise: tighten skill rules; add "Noise / Ignore" section
- State file grows unbounded: prune merged/closed items every run
- Auto-fix on wrong priority: start report-only; add explicit effort/risk gates
- Missed overnight failures: add fireImmediately: true or run at start of day + mid-day
- Stale critique / never reviewed: add human handoff when critique entries accumulate without resolution across N runs

Success Metrics
- Time from "something broke" to "human knows about it"
- % of mornings where `STATE.md` matched what you'd have found manually
- Reduction in ad-hoc "what's on fire?" messages

Current Phase: Week one — report-only. Do not auto-fix.

## Open Items
- [High] Add `LICENSE` file
- [Watch] `triage-loop.txt` purpose — confirm if linker/archival or duplicate content
- [Watch] Expand triage skill sources after initial quality is validated

## Completed
- [x] Initialize `.git` repo and push initial commit
