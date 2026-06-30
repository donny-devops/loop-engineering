# Contributing

This repo is a practical engineering reference, not a hype collection. We welcome patterns, stories, tool mappings, and honest failure reports.

## Ways to Contribute

| Contribution | Where |
| --- | --- |
| New loop pattern | `patterns/` + `patterns/registry.yaml` |
| Production story | `stories/` |
| Tool example | `examples/{grok,claude-code,codex,openclaw,github-actions}/` |
| Skill template | `templates/` |
| Starter kit | `starters/` |
| Doc improvement | `docs/` |

## Pattern Requirements

Every new pattern must include all sections from `templates/pattern-template.md`:

- Goal (one sentence)
- Scheduling (per-tool commands)
- Required skills
- State schema (with example)
- Typical cycle (numbered steps)
- Verification strategy (maker/checker)
- Human handoff points
- Tool-specific notes (at least 2 tools)
- Failure modes table
- Success metrics

Also add an entry to `patterns/registry.yaml`.

## Story Requirements

- Real experience (anonymize if needed)
- Name the pattern used
- Include at least one failure or surprise
- Actionable lesson in one paragraph

## Pull Request Checklist

- Links work from README or relevant index
- No secrets, tokens, or internal URLs
- `STATE.md` examples use `.example` suffix (gitignored live state)
- Safety-sensitive patterns reference `safety.md`

## Code of Conduct

- Engineering over hype
- Failures are first-class content
- Tool-agnostic by default; tool-specific in labeled sections

## Community

Questions: GitHub Discussions (preferred) or issue with label `question`
Show your loop: Add Adopter issue, Discussions, or a row in `docs/adopters.md`
Loop Ready badge: `npx @cobusgreyling/loop-audit . --badge` — paste into your README
Good first issues: look for label `good first issue`
Security: see `SECURITY.md` — do not file public issues for exploitable vulnerabilities

Thank you for helping make this the go-to reference for loop engineering.
