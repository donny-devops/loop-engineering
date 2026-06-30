# Loop Triage (L1 readiness)

Read `STATE.md` first, then run this triage script against the repo at `C:\Users\adoni\OneDrive\Desktop\Projects\loop-engineering`.

## Steps
1. Read `STATE.md`.
2. Check repo health: `git status`, recent commits, open branches.
3. Scan for loose ends: open TODOs, broken links, stale docs, missing `README.md`.
4. Classify findings:
   - **High Priority**: blocking or security-relevant.
   - **Watch**: non-blocking, should be tracked.
5. Append findings to `STATE.md` under `## Open Items` (create the section if absent).
6. Update `Last run` date in `STATE.md`.
7. Do NOT write any code or make repository changes in week one.

## Output Format
Append only:
```
## Open Items
- [High] <item>
- [Watch] <item>
```

Keep additions concise.
