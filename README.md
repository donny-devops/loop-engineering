# Loop Engineering

Minimal engineering loop scaffold for daily triage, verification, and controlled auto-fix — built around a readiness ladder (L0–L3) that gates how much autonomy the loop is allowed before a human has to sign off.

## Get started

```bash
npx degit your-org/loop-engineering-starter my-loop
cd my-loop
git init
```

If you applied the `minimal-loop` starter manually instead, confirm you have these files before continuing:

- `STATE.md` — current project spine (name, owner, last run frequency, open items)
- `LOOP.md` — loop config for the team
- `.grok/skills/loop-triage/SKILL.md` — triage skill

## Readiness ladder

The scaffold ships 7 loops, gated into 4 readiness levels. You don't enable all of them at once — each level unlocks the next loop only after the prior one has run clean for a defined period.

| Level | Unlocks | Gate to advance |
|---|---|---|
| L0 — Observe | `loop-triage` only | N/A — always on from day one |
| L1 — Verify | `loop-verifier` | [N] consecutive clean triage runs with no false positives |
| L2 — Assist | `minimal-fix` (proposes diffs, doesn't merge) | [N] verified runs, fix proposals reviewed by a human |
| L3 — Auto-fix | Auto-merge for [whitelisted fix categories] | [N] consecutive human-approved fixes of that category, zero rollbacks |

> Fill in the bracketed thresholds (`[N]`, fix categories) with your team's actual gate values — these are config, not fixed rules, and should live in `LOOP.md` so they're versioned alongside the loops themselves.

The other 3 loops in the set of 7 — `[loop-name-5]`, `[loop-name-6]`, `[loop-name-7]` — slot into this ladder at `[L_]`; document what each does and where it sits before publishing, since the ladder is the whole pitch of this repo.

## Daily loop

1. Triage each morning using the `loop-triage` skill.
2. Review findings appended to `STATE.md`.
3. Tune `loop-triage/SKILL.md` for 1–2 weeks before trusting its output.
4. Once you've cleared the L1 gate above, add `loop-verifier`.
5. Once you've cleared the L2 gate, add `minimal-fix` and start reviewing (not merging) its proposals.
6. Only after the L3 gate is cleared for a given fix category should auto-merge be turned on for that category — never globally.

## First week rule

No automated fixes. Triage and observe only. This is L0, and it's mandatory regardless of how confident the audit score looks.

## Prerequisites

- `git` (any reasonably current version — no sparse-checkout, worktrees, or other 2.x-specific features are used)
- `npx @cobusgreyling/loop-audit` (for readiness score, see below)

## Readiness check

```bash
npx @cobusgreyling/loop-audit .
```

Example output:

```
loop-audit v[x.y.z] — scanning .

✔ STATE.md found, last updated [N] days ago
✔ loop-triage/SKILL.md present
✔ 14 consecutive clean triage runs
✘ loop-verifier not yet enabled

Readiness: L1 (Verify) — eligible for L2
Next gate: enable loop-verifier, accumulate [N] verified runs
```

> Replace this block with real output from a run against this repo. A reviewer should be able to see what "ready" looks like without running the tool themselves.

## Repo layout

```
.
├── STATE.md          — project spine: owner, run cadence, open items, triage log
├── LOOP.md            — loop config: which loops are enabled, gate thresholds per level
├── README.md          — this file
├── SECURITY.md        — vulnerability reporting process
├── CHANGELOG.md        — version history of the scaffold itself
├── ARCHITECTURE.md     — loop state machine and fix-gating logic
├── CODEOWNERS          — review routing (no extension — GitHub only recognizes this exact filename)
├── ROADMAP.md          — planned loops and readiness-ladder changes
├── CONTRIBUTING.md      — how to propose a new loop or skill
└── .grok
    └── skills
        └── loop-triage
            └── SKILL.md
```

## Security

See `SECURITY.md` for reporting vulnerabilities.

## License

See `LICENSE` (MIT).
