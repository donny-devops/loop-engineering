# Workflow: Daily Triage Loop

## Flow

```
┌─────────────────┐
│  09:00 Scheduler│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Read STATE.md  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute triage  │
│   skill scan    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Append findings │
│ to STATE.md     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update "Last    │
│   run" date     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deliver output  │
│   to origin     │
└─────────────────┘
```

## Inputs
- `STATE.md` — current state, prior findings, project metadata
- `.grok/skills/loop-triage/SKILL.md` — triage procedure
- Repo files (`.git`, docs, code)

## Outputs
- Updated `STATE.md` with new `## Open Items` entries
- Updated `Last run` timestamp
- Cron delivery summary (if `deliver='all'`)

## Constraints (Week One)
- **No code changes** during triage runs
- **No auto-fix** — report-only mode
- **No pruning** of resolved items yet (introduce in week 2+)

## Next Actions After Triage
1. Human reviews `STATE.md` updates
2. Human acknowledges or dismisses items
3. Loop skill is tuned based on false positives / noise
4. After 1–2 weeks: enable `minimal-fix` + `loop-verifier`

## Failed Run Recovery
- If cron fails: manual `/loop 1d` from TUI
- If `STATE.md` is corrupted: restore from git history (`git checkout HEAD -- STATE.md`)
- If triage skill is broken: revert to previous `SKILL.md` version
