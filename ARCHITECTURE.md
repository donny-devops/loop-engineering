# Architecture

## Overview

`loop-engineering` is a minimal repo that houses an engineering loop scaffold: a state spine, a loop config, and a triage skill.

## Components

- `STATE.md` — single source of truth for project status, owner, last run, and open items.
- `LOOP.md` — team-facing workflow definition.
- `.grok/skills/loop-triage/SKILL.md` — triage procedure executed by the daily cron job.

## Data Flow

```
morning 09:00
   │
   ▼
 cron job (f472a7a0fdf5)
   │
   ▼
 read STATE.md
   │
   ▼
 execute loop-triage skill
   │
   ▼
 append findings to STATE.md
   │
   ▼
 update "Last run"
```

## Constraints (Week One)

- No code or repository changes during triage.
- No auto-fix pipeline enabled until triage quality is verified.

## Future Expansion

- `minimal-fix` skill
- `loop-verifier` skill
- Optional GitHub Actions workflow for readiness score
- Optional `readiness-badge` in README.md
