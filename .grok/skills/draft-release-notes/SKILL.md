# Draft Release Notes Skill

name: draft-release-notes
description: Reads a structured changelog scan and produces polished, user-facing release notes draft. Inserts into RELEASE_NOTES_DRAFT.md or returns markdown ready for human review.
user_invocable: true

## Draft Release Notes Skill

You are an expert technical writer. Your job is to turn a structured `changelog-scan` output into a clean, user-friendly release notes draft.

### Inputs
- Structured scan output from `changelog-scan` skill
- Existing `RELEASE_NOTES_DRAFT.md` (optional)
- Project's release voice / style guide (if present in `AGENTS.md` or a project skill)

### Output Format
If `RELEASE_NOTES_DRAFT.md` exists, append a new section titled `## Draft: YYYY-MM-DD` (date of latest merge in window). Otherwise, create the file.

Use this structure:
```
## Draft: YYYY-MM-DD

### Highlights
- 1–3 bullets summarizing the user-facing impact

### Added
- ...

### Changed
- ...

### Deprecated
- ...

### Removed
- ...

### Fixed
- ...

### Security
- ...

### Notes
- Anything that needs human sign-off (breaking changes, deprecations, security items)
```

### Rules
- Keep language clear and non-internal.
- Convert PR titles to user benefit where possible.
- Breaking changes must be prefixed with `⚠️ ` and explicitly called out in `Notes`.
- Do not publish or update `CHANGELOG.md` — draft only.
- If the scan output is empty, write a minimal placeholder and stop.
