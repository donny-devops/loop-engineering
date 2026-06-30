# Release Notes Draft

## Draft: 2026-06-29

### Highlights
- Scoped daily triage loop scaffolded and tested
- Changelog drafter loop scaffolded with scan + draft skills

### Added
- Daily triage loop with `.grok/skills/loop-triage/SKILL.md` and `STATE.md`
- Changelog drafter loop with `.grok/skills/changelog-scan` and `.grok/skills/draft-release-notes`
- `LOOP_DESIGN_CHECKLIST.md` and `WORKFLOW.md` to document loop design and execution flow

### Changed
- Loop cron delivery switched to `all` for in-session visibility

### Deprecated
- n/a

### Removed
- n/a

### Fixed
- n/a

### Security
- `SECURITY.md` scaffolded with vulnerability reporting workflow

### Notes
- Mock draft seeded from initial repo state. No real scan candidates exist yet.
- Human must approve publication; do not tag or update `CHANGELOG.md` without sign-off.
