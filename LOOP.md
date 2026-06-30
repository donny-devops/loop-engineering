# LOOP.md

This file is the source of truth for loop configuration. `loop-audit` reads it
to compute readiness level; loops themselves read it to know their gate
thresholds, schedule, and escalation path. Keep it in version control —
changes to gate thresholds should go through the same review as code.

```yaml
# ──────────────────────────────────────────────────────────────
# 1. LOOP DEFINITIONS
# Each loop declares its readiness level, what triggers it, and
# where its skill/config lives. Fill in the 4 unnamed loops.
# ──────────────────────────────────────────────────────────────
loops:
  - id: loop-triage
    level: L0
    enabled: true
    skill: .grok/skills/loop-triage/SKILL.md
    trigger:
      type: schedule
      cron: "0 8 * * 1-5"          # 08:00 weekdays, repo-local timezone
      on_demand: true               # can also be run manually
    timeout_minutes: 10
    output: appended to STATE.md under `## Triage Log`

  - id: loop-verifier
    level: L1
    enabled: false                  # flips true once L1 gate is cleared
    skill: .grok/skills/loop-verifier/SKILL.md
    trigger:
      type: event
      on: [triage_completed]        # runs immediately after triage, not on its own schedule
    timeout_minutes: 15
    output: pass/fail verdict appended to STATE.md, see Verifier Contract below

  - id: minimal-fix
    level: L2
    enabled: false
    skill: .grok/skills/minimal-fix/SKILL.md
    trigger:
      type: event
      on: [verifier_passed]
    timeout_minutes: 20
    output: proposed diff, opened as draft PR — never auto-merged at L2

  - id: [loop-name-5]
    level: [L_]
    enabled: false
    skill: .grok/skills/[loop-name-5]/SKILL.md
    trigger:
      type: [schedule|event]
      cron: [if schedule]
      on: [if event]
    timeout_minutes: [N]
    output: [what it writes and where]

  - id: [loop-name-6]
    level: [L_]
    enabled: false
    skill: .grok/skills/[loop-name-6]/SKILL.md
    trigger: {}
    output: []

  - id: [loop-name-7]
    level: [L_]
    enabled: false
    skill: .grok/skills/[loop-name-7]/SKILL.md
    trigger: {}
    output: []

# ──────────────────────────────────────────────────────────────
# 2. READINESS GATES
# Numeric thresholds an audit checks against to recommend the
# next level. loop-audit reads these directly — don't hardcode
# thresholds anywhere else.
# ──────────────────────────────────────────────────────────────
gates:
  L0_to_L1:
    require: consecutive_clean_triage_runs >= 10
    false_positive_rate_max: 0.05   # over the same window

  L1_to_L2:
    require: consecutive_verified_runs >= 10
    verifier_false_negative_rate_max: 0.0   # zero tolerance — a missed failure here is the riskiest failure mode

  L2_to_L3:
    require: human_approved_fix_proposals >= 15
    rollback_count_max: 0           # any rollback resets this counter to 0
    scope: per_fix_category          # L3 is granted per category, not globally — see rollback rules

# ──────────────────────────────────────────────────────────────
# 3. VERIFIER CONTRACT
# What loop-verifier must guarantee to be trusted as a gate.
# If you swap in a different verifier, it must still satisfy this.
# ──────────────────────────────────────────────────────────────
verifier_contract:
  input: triage findings from the immediately preceding loop-triage run (STATE.md `## Triage Log`, latest entry)
  output:
    format: structured verdict, one of [pass, fail, inconclusive]
    must_include:
      - verdict
      - reasoning (why pass/fail — not just the label)
      - confidence_score (0.0–1.0)
      - timestamp
  idempotency: running the verifier twice on the same triage output must produce the same verdict
  inconclusive_handling: treated as fail for gate-counting purposes — never silently dropped
  on_fail: loop chain stops here; minimal-fix does not run; STATE.md open item created automatically

# ──────────────────────────────────────────────────────────────
# 4. ROLLBACK RULES (L3 auto-fix stage)
# These apply once a fix category has cleared the L2→L3 gate and
# auto-merge is live for that category.
# ──────────────────────────────────────────────────────────────
rollback:
  triggers:
    - post_merge_test_failure        # CI red on main after an auto-merged fix
    - error_rate_spike_pct: 5         # >5% increase in monitored error rate within rollback_window
    - manual_revert_requested         # any owner can force this, no quorum needed
  rollback_window_minutes: 30         # how long after merge a spike/failure counts as caused by the fix
  mechanism: git revert (not force-push) — preserves history and triggers a fresh CI run
  on_rollback:
    - immediately disable auto-merge for the affected fix_category
    - reset that category's L3 counter (see gates.L2_to_L3.rollback_count_max) to 0
    - require [N] re-cleared L2 cycles before that category is eligible for L3 again
    - log to STATE.md under `## Rollback Log` with: timestamp, fix_category, trigger, who/what reverted it
  cool_down_minutes: 60               # no new auto-merges for the same category during this window post-rollback

# ──────────────────────────────────────────────────────────────
# 5. OWNERSHIP & ESCALATION
# CODEOWNERS routes PR review. This section defines what happens
# when a loop itself fails, times out, or needs a human decision —
# distinct from normal code review.
# ──────────────────────────────────────────────────────────────
escalation:
  primary_owner: [@github-handle or team]
  secondary_owner: [@github-handle or team]   # paged if primary doesn't respond within SLA

  on_loop_timeout:
    notify: primary_owner
    sla_minutes: 30
    if_unack: escalate to secondary_owner

  on_verifier_fail:
    notify: primary_owner
    sla_minutes: 1440                # 24h — non-urgent, becomes an open item in STATE.md
    if_unack: surfaced in next daily triage as a stale open item

  on_rollback:
    notify: [primary_owner, secondary_owner]   # always both — rollback is the highest-severity event
    sla_minutes: 15
    if_unack: escalate to [team lead / on-call rotation]
    channel: [Slack channel / PagerDuty service / etc.]

  on_l3_category_disabled:           # i.e. auto-merge was turned off for a fix category after rollback
    notify: primary_owner
    requires_manual_reenable: true   # never auto-re-enables, even after cool-down
```
