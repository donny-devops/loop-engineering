---
name: scan-worker
description: Parallel repo scanner for secrets, vulns, and docs.
model: inherit
tools: [terminal, file]
max_concurrency: 3
---

# scan-worker

## Role
Runs lightweight scanners against a target directory.

## Input
- Path to scan.

## Output
- Findings JSON.
- Suggested fixes.
