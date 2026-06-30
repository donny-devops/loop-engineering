# Changelog Drafter Loop

## Schedule
- Daily at 08:30 local time (after morning triage)

## Scope
- Repo root: `C:\Users\adoni\OneDrive\Desktop\Projects\loop-engineering`
- Scan: merges since `last_tag` (currently `v0.1.0`), fallback to last 7 days
- Draft target: `RELEASE_NOTES_DRAFT.md`

## Safety Gates
- Draft only — never publish, tag, or update `CHANGELOG.md` without explicit human approval.
- Breaking changes and security items must be surfaced in `Notes` section.
- Do not overwrite existing `RELEASE_NOTES_DRAFT.md`; append or replace only with confirmation.

## Skills
- `changelog-scan` — discovers candidate changes
- `draft-release-notes` — produces polished draft

## State
- `changelog-drafter-state.md` — tracks `last_tag`, `last_scan`, `pending_drafts`
- Update `last_scan` on every run.
- Move drafts to `published_drafts` only after human approval (manual step).

## Human Handoff
- If `RELEASE_NOTES_DRAFT.md` exists and has unresolved `Notes` or `⚠️` items, flag in delivery.
- Human must approve before any GitHub release or tag push.

## Cost & Limits
- Daily cap: 50k tokens
- No auto-PRs; draft only

## Observability
- Log each run to `loop-run-log.md` when available.
