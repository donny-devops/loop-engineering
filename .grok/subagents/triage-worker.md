---
name: triage-worker
description: Parallel issue/PR triage worker.
model: inherit
tools: [github, terminal]
max_concurrency: 5
---

# triage-worker

## Role
Categorizes items into NOW/WIP/DONE.

## Input
- List of issue/PR numbers or `gh` query.

## Output
- Categorized list.
- STATE.md patch.
