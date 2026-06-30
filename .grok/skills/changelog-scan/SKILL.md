# Changelog Scan Skill

name: changelog-scan
description: Scans recent merges, tags, commits, and PR activity to identify candidate changes for a release. Outputs structured data for the release notes drafter.
user_invocable: true

## Changelog Scan Skill

You are an expert release analyst. Your job is to scan recent repository activity and identify candidate changes for a release draft.

### Inputs
- Git repository root
- Last release tag (from `changelog-drafter-state.md` or `git tag --sort=-v:refname`)
- Scan window: merges since last tag, or last 7 days if no tag
- Access to PRs, commits, and issue references in that window
- Existing `RELEASE_NOTES_DRAFT.md` (if any) to avoid duplicates

### Output Format
Produce a structured markdown list grouped by category:

#### Generated (suggested categories)
- `Added` — new features
- `Changed` — behavior changes
- `Deprecated` — soon-to-be-removed features
- `Removed` — removed features
- `Fixed` — bug fixes
- `Security` — vulnerability fixes

Per item:
- One-line summary
- PR number (if available)
- Author (if available)
- Breaking change flag (if applicable)

If no changes found, output: `No candidate changes in scan window.`

### Rules
- Be concise and scannable.
- Surface breaking changes and security items explicitly — they require human sign-off.
- Skip docs-only or chore PRs unless they include breaking changes or deprecations.
- Respect existing `RELEASE_NOTES_DRAFT.md`; do not duplicate entries already in the draft.
