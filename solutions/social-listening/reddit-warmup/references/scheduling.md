# Daily Trigger Scheduling (External)

The skill itself does not schedule tasks. It only defines what happens when triggered. Wiring the daily trigger is the caller's responsibility, done once per account during onboarding.

Different runtimes have different scheduling mechanisms: system cron, Windows Task Scheduler, CI jobs, container CronJobs, hosted automation rules, or another agent-native scheduler. Embedding one named agent scheduler would lock the skill to one environment.

---

## What the scheduler must do

Once per day per account, invoke the agent with:

```text
today's task - reddit warmup <username>
```

The skill's entry-point logic detects this phrase and runs Phase 2 for that account.

### Single daily run

Schedule **one** automation trigger per account per scheduler day. Do not add a fixed second evening recon job.

The daily run owns the full sequence:

```text
Pre-flight -> Inbox/notification check -> Stage task -> Watchtower if just posted
-> Daily tail recon -> Comment Feedback Loop -> Anomaly check + Daily Report
```

The tail routines are light and conditional:
- **End-of-Day Recon**: pre-warm only the sub profiles likely needed tomorrow.
- **Comment Feedback Loop**: revisit a small capped set of older comments to update `karma_by_sub` and catch real reply opportunities.

If the account is rate-limited, logged out, near the run time budget, or has no eligible targets, skip the tail and record the reason in the daily report.

Approval replies are **not** a daily trigger. When the user later approves a pending comment/post in natural language, the agent runs only the approval publish path for that batch: open the stored `browser_id` in a fresh `<run_session>`, verify `/user/me/`, publish the stored variant, verify the result, and update logs. It does not run Phase 2 again.

Legacy note: older versions used a separate evening recon trigger. Do not wire that pattern for new accounts; it creates two automated account touches per day.

### Runtime timeout

Set the external scheduler / agent runner timeout to **at least 3600 seconds** for daily Phase 2 runs.

- Do not use a 1800-second timeout for Day 30+ or promote-stage accounts; Stage 3 has more preflight, sub verification, approval, post checks, and tail work, so runtime is less predictable.
- Stage 2 can often finish sooner, but using the same 3600-second ceiling avoids false timeout failures when Reddit UI waits, CAPTCHA handling, or post/comment verification takes longer.
- If the run approaches the timeout, skip optional tail work first (`end-of-day-recon` / `comment-follow-up`) and log `budget_approaching`; do not cut off an in-progress publish verification.
- Hot approval publish flows are separate from the daily run and may use a smaller runner timeout, but still must allow enough time for fresh browser open ->`/user/me/` check ->submit ->original-thread/permalink verification. If one user reply approves multiple items, run them sequentially and reopen a fresh browser-act session with the stored `browser_id` whenever the previous session has been closed.

### Unattended flag

Unattended runs (cron, Task Scheduler, GitHub Actions, etc. with no live user) should set:

```text
REDDIT_WARMUP_UNATTENDED=1
```

Without this, CAPTCHAs and other error-recovery prompts can hang the run waiting for a reply that never comes. With it, the CAPTCHA Tier 3 fallback switches from "keep waiting" to "log `captcha_blocked` + abort", and other non-approval interactive points similarly fail fast.

Approval timing in unattended runs:
- The flag does **not** bypass content approval.
- Manual-path comment/post batches stay in `pending_approval/<batch>/` until the user replies or the 7-day stale cleanup removes them.
- The user can reply later in natural language (`pick A`, `reply D`, `use the second one`, `skip`, `make it shorter`).
- A clear pick immediately runs the browser publish flow. Cron-only scheduling is still useful for browse / upvote / subscribe activities; content publishing waits for a clear user pick unless `approval_policy` explicitly allows auto-publish.

See `approval-rules.md` -> Rules C3/C4/C6.

---

## Picking the trigger time

"10:00 local" is not one-size-fits-all. Use three inputs:

1. **Proxy geo location**: what Reddit thinks this account's home timezone is. Pull it during Phase 1 Step 2 by visiting `https://ipinfo.io/json` and reading the `timezone` field. The account's "local" time is the proxy's time, not the user's real-world time.
2. **Target audience location**: where the subs' active users are. US-dominant subs usually peak around lunch and evening US time. UK/Europe tech subs often peak in local evening. Regional subs peak in their own evening.
3. **Account's home schedule**: a real user does not open Reddit at exactly the same second every day. Pick a window such as 09:30-11:00 or 20:00-21:30; the skill's in-loop waits add variability inside the session.

### Decision flow at onboarding

```text
Daily trigger time setup

Detected:
- Proxy geo: <proxy_timezone> (what Reddit sees as local)
- Configured target subs: <list>

Suggested candidates:
  A. Proxy local 09:30-11:00 (morning browsing)
  B. Proxy local 20:00-21:30 (evening browsing and daily tail)

Corresponding scheduler expressions converted to the scheduler machine's timezone:
  A -> <schedule>
  B -> <schedule>

Which one?
```

The skill proposes, the user picks. Record the choice in `account.schedule_profile` in `config.yaml`.

### Staggering across multiple accounts

If running multiple accounts on one machine:

- Never fire them at the same minute. Even with distinct proxies, timing correlation is a weak signal.
- Stagger at least 15 minutes apart.
- Stagger by stage: lurk accounts first, promote accounts last. If the machine hits an issue mid-batch, the lowest-risk accounts have already finished.

---

## Examples by environment

### System crontab (Linux/macOS)

```cron
# Account A (US proxy) - one trigger per day
# 20:30 US Eastern -> converts to the scheduler machine's timezone
30 1 * * * REDDIT_WARMUP_UNATTENDED=1 /usr/local/bin/claude-agent run --session isolated --message "today's task - reddit warmup <username_a>"

# Account B (UK proxy) - staggered from Account A
0 20 * * * REDDIT_WARMUP_UNATTENDED=1 /usr/local/bin/claude-agent run --session isolated --message "today's task - reddit warmup <username_b>"
```

Adjust the agent-runner CLI (`claude-agent`, `openclaw`, `codex`, or another orchestrator) to whatever your runtime provides. Do not invoke `browser-act` directly from the scheduler; `browser-act` is used internally by the skill.

### Windows Task Scheduler

Create one task per account. Trigger: Daily at the chosen local time. Action: run your agent-runner CLI (`claude-agent` / `openclaw` / `codex` / similar, not `browser-act`) with the trigger message. Set `REDDIT_WARMUP_UNATTENDED=1` as a user-level environment variable so the child process inherits it.

### GitHub Actions

```yaml
on:
  schedule:
    - cron: "30 1 * * *"   # Example only; GitHub cron is UTC
env:
  REDDIT_WARMUP_UNATTENDED: "1"
jobs:
  warmup:
    runs-on: ubuntu-latest
    steps:
      - run: <your-agent-cli> --message "today's task - reddit warmup <username>"
```

GitHub cron is UTC only. DST will drift a "local evening" schedule twice a year unless the scheduler logic accounts for it.

### Agent-native scheduling

If your agent environment has its own scheduler, use that. The payload is always the trigger message plus `REDDIT_WARMUP_UNATTENDED=1`.

---

## Pause / resume / delete

The skill supports these user commands; the scheduler honors them:

| User says | What the caller should do |
|-----------|---------------------------|
| "pause warmup `<username>`" | Disable the daily job; do not delete it. |
| "resume warmup `<username>`" | Re-enable the daily job. |
| "delete account `<username>`" | Remove the daily job entirely. |

The skill writes `paused: true` / `false` to `progress.json`; the scheduler's responsibility is to stop/start firing.

---

## Idempotency

At Phase 2 pre-flight the skill checks `progress.json.last_run_scheduler_date`:

- `last_run_scheduler_date == today_scheduler` -> already ran, show cached daily report and exit.
- Otherwise -> new scheduler day, proceed.

`today_scheduler` is computed in `config.yaml.account.scheduler_timezone` when set, otherwise `account.timezone` as a single-region fallback.

Multiple triggers on the same scheduler day are safe: the second run is a no-op. Do not rely on that as a normal pattern; the intended design is still one scheduled automation run per day.

Approval publish flows do not update `last_run_scheduler_date`, do not advance `current_day`, and do not count as the daily run.

---

## Timezone rule

Use two time concepts deliberately:

- `config.yaml.account.scheduler_timezone`: daily idempotency (`last_run_scheduler_date`) and scheduler-day boundaries.
- `config.yaml.account.timezone`: account rhythm such as `current_day`, Wednesday/Friday checks, weekly resets, post/comment timing, and user-facing account-local timestamps.

Timestamps: ISO 8601 with offset (`2026-05-08T10:15:00+08:00`). Date-only: `YYYY-MM-DD` interpreted in the relevant timezone above.

