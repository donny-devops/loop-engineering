# Loop Engineering

Minimal engineering loop scaffold for daily triage, verification, and controlled auto-fix.

## Fetch / Set up the starter

If you applied the `minimal-loop` starter manually, make sure you have these files:

- `STATE.md` — current project spine (name, owner, last run frequency, open items)
- `LOOP.md` — loop config for the team
- `.grok/skills/loop-triage/SKILL.md` — triage skill

## Daily loop

1. Triage each morning using the `loop-triage` skill.
2. Review findings appended to `STATE.md`.
3. Tune `loop-triage/SKILL.md` for 1–2 weeks.
4. Once triage quality is good, add `minimal-fix` and `loop-verifier` from templates and enable small auto-wins.

## First week rule

No automated fixes. Triage and observe only.

## Prerequisites

- `git 2.x`
- `npx @cobusgreyling/loop-audit` (for readiness score)

## Readiness check

```bash
npx @cobusgreyling/loop-audit .
```

## Repo layout

```
.
├── STATE.md
├── LOOP.md
├── README.md
├── SECURITY.md
├── CHANGELOG.md
├── ARCHITECTURE.md
├── CODEOWNERS.md
├── ROADMAP.md
├── CONTRIBUTING.md
└── .grok
    └── skills
        └── loop-triage
            └── SKILL.md
```

## Security

See `SECURITY.md` for reporting vulnerabilities.

## License

See `LICENSE` (MIT).
