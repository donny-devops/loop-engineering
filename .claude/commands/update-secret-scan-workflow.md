---
name: update-secret-scan-workflow
description: Workflow command scaffold for update-secret-scan-workflow in loop-engineering.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-secret-scan-workflow

Use this workflow when working on **update-secret-scan-workflow** in `loop-engineering`.

## Goal

Update or trigger the GitHub Actions workflow for secret scanning, typically to fix configuration, update inputs, or trigger a scan.

## Common Files

- `.github/workflows/secret-scan.yml`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit .github/workflows/secret-scan.yml to update configuration or trigger a run
- Commit changes with a message referencing secret scan or gitleaks
- Optionally, update related documentation or agent files if the workflow logic changes

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.