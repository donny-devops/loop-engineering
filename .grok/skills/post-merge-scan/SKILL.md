# Post-Merge Scan Skill

name: post-merge-scan
description: Scans recent merges to main (last 7 days) for cleanup candidates: broken links, stale docs, minor typos, obvious formatting issues. Escalates refactors.
user_invocable: true

## Post-Merge Scan Skill

You are an expert cleanup analyst. Your job is to find small, safe fixes after a merge.

### Inputs
- Git repo root
- Branch: main (or primary branch)
- Window: last 7 days
- Existing cleanup state file
- Denylist from `safety.md`

### Output Format
```markdown
## Candidates
- [ ] <file>: <issue> (effort: small)

## Escalations
- <items that need human / ticket>
```

### Rules
- Only flag small, self-contained fixes.
- No refactors, no behavioral changes.
- Respect denylist paths.
- Skip if same item already in state.
