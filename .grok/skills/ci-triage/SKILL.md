# CI Triage Skill

name: ci-triage
description: Scans CI status on main for new, actionable failures. Classifies flakes vs real failures. Proposes minimal fixes with verifier.
user_invocable: true

## CI Triage Skill

You are an expert CI analyst.

### Inputs
- CI provider output (GitHub Actions, etc.) for main branch
- Last N hours (typically 24h)
- Existing `ci-sweeper-state.md`
- `safety.md` denylist

### Output Format
```markdown
## New Failures
- <workflow/job>: <failure summary> (effort: small | escalate)

## Flakes
- <test name>: passed on retry / no code change → Watch

## Escalations
- <items beyond loop scope>
```

### Rules
- "Fix" only real, reproducible failures.
- Do not disable tests or add retries to silence flakes.
- Escalate after 3 attempts on same failure.
