# Phase 2 -Pre-flight + Stage Determination

**Load this file immediately after `browser-act-rules.md`** at the start of every Phase 2 daily run.

---

## Prerequisites -Every Run Before Anything Else

Verify `browser-act` CLI is installed and the runtime guide loads. Running without the BrowserAct runtime guide causes silent failures.

**Run these three commands in order:**

```bash
# 1. Current version (or error if not installed)
browser-act --version

# 2. Load BrowserAct runtime guide
browser-act get-skills core --skill-version 2.0.0

# 3. Confirm version after guide load
browser-act --version
```

**Decision ladder:**

| What you see | Action |
|--------------|--------|
| Step 1 returns a version AND Step 2 returns the runtime guide | Continue. Record version in first log entry's `cli_version` field |
| Step 1 errors | Stop. Tell user: "browser-act CLI is not available. Install BrowserAct CLI using the official BrowserAct install instructions, then retry." |
| Step 2 errors | Stop. Tell user: "BrowserAct runtime guide did not load. Refresh BrowserAct CLI using the official BrowserAct install instructions, then retry." |

---

## Execution Proof

Every run must produce real screenshots. Log entries are only valid when there is a fresh screenshot to back them.

**After Prerequisites passes:**

```bash
RUN_SESSION="reddit-warmup-<username>-daily-<ts>"
browser-act --session "$RUN_SESSION" browser open --headed <browser_id> https://www.reddit.com
browser-act --session "$RUN_SESSION" screenshot ~/.reddit-warmup/<username>/last_run.png
browser-act --session "$RUN_SESSION" get title
```

**Every `activity_log.jsonl` entry carries these three fields** (values from real browser-act CLI output only):

```json
{"run_session_id": "<run_session>",
 "url_confirmed": "<URL from navigate / get state>",
 "page_title": "<from get title or first heading in get markdown>"}
```

**Per-event screenshot rule:** before writing any `comment` / `post` / `upvote` / `subscribe` log entry, take a fresh screenshot to `~/.reddit-warmup/<username>/evidence/<YYYYMMDD-HHMMSS>-<event>.png`.

**Run closes with:**
```bash
browser-act --session "$RUN_SESSION" screenshot ~/.reddit-warmup/<username>/last_run.png
```
Then load that path. If loading fails ->do not send a daily report; report "browser did not open cleanly" and leave `progress.json` untouched.

**Exemption:** Phase 1 historical backfill writes entries with `"imported": true`; those don't require per-event screenshots.

---

## Publishing Rate Limit

Reddit shares one rate-limit bucket across comments + posts for the same account. Floor is 75s; we use 90s as a safety margin.

**Before any comment submit / post submit:**

1. Read `progress.json.last_publish_at` (ISO 8601; may be null on first write).
2. If `now - last_publish_at < 90s` ->sleep the remaining seconds.
3. Fetch target page markdown and grep for blocking banners (`permanently banned` / `Rate limit exceeded` / `locked` / `restricted` / `you are doing that too much`). If any ->skip and trigger Anomaly Detection full-stop.

**After successful submit:**

4. Write `progress.json.last_publish_at = now ISO 8601`.
5. If verify returned `click_failed` / `reddit_4xx` / `reddit_5xx` ->do NOT update `last_publish_at`.

Applies to: Stage 2 comments, Wednesday practice post, Stage 3 Path A/B posts, inbox replies, camping replies.

---

## Pre-flight Steps (stop at first terminating condition)

### 0a. browser-act CLI check
Run the Prerequisites sequence above. Missing CLI or missing runtime guide ->stop.

### 0b. Browser profile check
Load `~/.reddit-warmup/<username>/config.yaml`. Confirm `account.browser_id` present and non-empty.
- Missing / empty ->stop: "`<username>`'s config.yaml has no browser_id; Phase 2 refuses to run. Complete Phase 1 Step 2 first."
- Print the resolved `browser_id` in the run preview.

### 0c. Persona load
Read `config.yaml.persona_file` path (if set). If exists and has no `<...>` placeholders ->parse into working memory as `persona`. If missing / empty / has placeholders ->remember this state; Day 15 Persona Readiness Gate will hard-block comments.

### 0d. Profile-customization reminder
Read `progress.json.profile_customized`. If `false` AND `current_day >= 7`: surface in today's preview: "Warning: `<username>` profile still has default avatar + empty bio. Walk through Phase 1 Step 5.7 before Stage 2 starts." Do NOT block today's run -just surface.

### 1. Pending-batch sweep (two passes)

- **Pass A -replay_after restore.** List matching local files under `C:/Users/<system_user>/.reddit-warmup/<username>/pending_approval/*/meta.json` where `replay_after` is set. For each, if `now >= replay_after` ->clear `replay_after`. Do **not** surface the batch text in today's daily report; the Daily Report only shows the total pending count. If the batch needs renewed attention, emit a standalone Approval Batch Request with the normal batch anchor and item numbers.
- **Pass B -stale cleanup.** List matching local files under `C:/Users/<system_user>/.reddit-warmup/<username>/pending_approval/*/meta.json`. For each, if `created_at` is older than 7 days AND `replay_after` is null ->delete batch directory, append `skip("batch_stale_7d")` to log.

### 2. Idempotency

**Determine `today_scheduler`:**
- `config.yaml.account.scheduler_timezone` is set ->`today_scheduler = today's date in that timezone`
- Otherwise (blank / missing) ->`today_scheduler = today's date in account.timezone` (single-region fallback)

**Check:**
- `progress.json.last_run_scheduler_date == today_scheduler` ->show cached report, exit.
- Otherwise ->new scheduler day, continue.

**Backward compat (migration):** If `last_run_scheduler_date` is null (account predates this field):
fall back to `date(last_run, account.timezone) == today(account.timezone)`.
On the next successful run, write `last_run_scheduler_date` so the new logic takes over.

> **Why this matters:** idempotency must use the *scheduler's* local date, not the account's. When the cron fires in Shanghai at 13:14 but the account timezone is `America/Los_Angeles` (22:14 the previous night), using account.timezone would falsely report "already ran today" and skip the correct day's task.

### 2.5. Per-day flag reset (only after Idempotency confirmed a new day)
- If `progress.json.rate_limit_hit_today == true` (triggered yesterday) ->remember "today runs in light mode, Stage 1 behaviors only, no comments or posts"; then **immediately reset `rate_limit_hit_today` to `false``.
- Reset `daily_skip_reason` to `null`.
- Write back to progress.json, then continue to Step 3.

### 2.6. Persistent account-risk flag
If `progress.json.account_risk_flagged == true`, stop before opening Reddit for normal activity. Surface:

```text
<username> is currently paused by account-risk flag: <account_risk_reason>.
Manual check required: open the account, click the top-right avatar menu, and confirm no red server-error toast appears.
After manual verification, say "clear account risk for <username>" to resume on the next daily run.
```

Do not browse, upvote, subscribe, comment, post, recon, or run feedback while this flag is true. Only clear it after the user explicitly confirms the avatar menu is clean.

### 3. Paused
`paused == true` ->exit silently.

### 4. Migration
`env_migration == true` ->run the migration-day task only, exit.

### 5. Open browser + screenshot + get title
See Execution Proof above. Failure ->log `browser_open_failed` + stop.

### 5.5. Session-expiry check
Run `get markdown` and scan for session-expiry banners (case-insensitive): `"your session has expired"` / `"session timed out"` / `"please refresh"` (expiry context) / localized session-expiry equivalents.

If any match:
```bash
browser-act --session <run_session> reload
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> get markdown   # re-scan once
```
Banner gone ->continue. Banner still present ->log `session_expiry_reload_failed`, screenshot, notify user, abort writes today. **One reload only.**

### 6. Login check
Step 0 (authoritative `/user/me/` username resolution -see `browser-act-rules.md`) + four-layer verification from `login-verification.md`. Any step/layer fails ->skip write actions today. The username returned by Step 0 becomes `<current_username>` for the rest of the run.

### 6.1. Avatar Menu Health Check (hard gate before any write action)

Run this immediately after login verification and **before** Notification + Inbox Check, browsing, upvoting, subscribing, commenting, posting, recon, or feedback loops.

Why: some abnormal Reddit account states still pass `/user/me/`, profile, and prefs checks, but show a red toast such as `"We had a server error..."` only when the top-right avatar/user menu is opened. This is an account-health signal and must block write actions.

Procedure:

```bash
browser-act --session <run_session> navigate https://www.reddit.com
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-avatar-health-before.png
browser-act --session <run_session> state
# Find the top-right profile/avatar/user-menu button.
# Prefer controls whose accessible label/text contains: "user menu", "open profile menu",
# "profile", "avatar", or the current username. Do not click Settings/Log Out/menu items.
browser-act --session <run_session> click <avatar_btn_idx>
sleep 2
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-avatar-health-after.png
```

Detection sources:

- `state` output after the click.
- `get markdown` output after the click.
- screenshot evidence. If text extraction is inconclusive but the screenshot visibly shows the red account/server-error toast, treat as detected.

Detect any of these case-insensitive markers:

- `we had a server error`
- `server error`
- `we had some trouble getting to reddit`
- `something went wrong`
- `try again later`

If detected, reload and retry the full avatar-menu check **once**:

```bash
browser-act --session <run_session> reload
browser-act --session <run_session> wait stable --timeout 15000
# repeat the avatar click + state/markdown/screenshot sequence once
```

| Result | Action |
|--------|--------|
| Avatar menu opens and no marker appears | Log `account_health: "ok"`, continue |
| Marker appears first try but disappears after reload retry | Log `account_health: "ok_after_retry"`, continue |
| Marker persists after retry | Set `progress.json.account_risk_flagged = true`, `account_risk_reason = "avatar_menu_server_error"`, `account_risk_flagged_at = now`, `daily_skip_reason = "account_health_avatar_server_error"`. Log `type: "account_risk_signal"`. Notify user. Skip all write actions today. |
| Avatar button cannot be found or clicked | Treat as `uncertain`, screenshot, log `skip("avatar_menu_unavailable")`, and skip write actions today. Do not guess a different menu item. |

**Persistent flag:** if `account_risk_flagged == true` from a previous run, surface it at run start and skip write actions until the user manually verifies the account is clean. After the user confirms the avatar menu opens cleanly without the error toast, set `account_risk_flagged = false`, clear `account_risk_reason`, and resume on the next daily run.

**->After Avatar Menu Health Check passes: load `references/notification-check.md` and run the Notification + Inbox Check.**

### 6.5. Overview Scan (new day only)
After successful login and Avatar Menu Health Check, navigate to `/user/<current_username>/overview/` and scan for "Removed by Reddit" notices in the past 24 hours. If found:
- Extract subreddit names; update `sub_profiles.json[<sub>].restrictions.temp_banned_until = today + 7 days`
- Log `removed_by_reddit_detected` event; continue run (non-blocking)

### 7. CAPTCHA
Markdown contains captcha/challenge text ->use the **3-tier escalation ladder** (see `browser-act-rules.md` ->"When to Ask for Help"):

- **Tier 1 -Auto-attempt.** `browser-act --session <s> solve-captcha`. Up to 2 attempts, 10-20s between.
- **Tier 2 -Hand to user.** `browser-act --session <s> remote-assist --objective "..."`. Send URL in chat, wait for "done".
- **Tier 3 -Unavailable.** Interactive: keep waiting. Unattended (`REDDIT_WARMUP_UNATTENDED=1`): log `captcha_blocked` + `daily_skip_reason: "captcha_at_preflight"` + close + exit.

### 8. Sync karma
`browser-act navigate https://www.reddit.com/user/me/` ->`wait stable` ->`get markdown` ->parse "X karma" from profile header ->update `progress.json.comment_karma` + `post_karma`.

### 9. Audience-TZ gate
If current hour in `account.audience_tz` (or `account.timezone`) < 7 or >=23 ->log `skip("audience_night_hours")` + exit.

---

## Stage Determination

### Step A: `raw_stage` (determined by `current_day`)

```
current_day = (today - start_date).days + 1
<= 1   ->raw_stage = "setup"
<= 14  ->raw_stage = "lurk"
<= 29  ->raw_stage = "comment"
otherwise ->raw_stage = "promote"
```

### Step B: `effective_stage` (raw_stage overlaid with `stage3_user_choice`)

```
if raw_stage == "promote":
    if stage3_user_choice == "promote"  ->effective_stage = "promote"
    if stage3_user_choice == "stay"     ->effective_stage = "comment"
    if stage3_user_choice == null       ->effective_stage = "pending_stage3_decision"
else:
    effective_stage = raw_stage
```

**Flow decisions always use `effective_stage`.**

### `progress.json.stage` field

Display-only and for human audit; NOT the authority for flow decisions. Write computed `effective_stage` at end of every run alongside `last_run`.

### `setup` branch

`stage == "setup"` in Phase 2 = Phase 1 just finished the setup flow. Send: "`<username>` initialization complete. Stage 1 browsing starts on Day 2." Update `last_run = today`. Do no browser write actions. Exit.

---

## Milestone Checks

- **Day 14** -eve of Lurk ->Comment transition. Run all four checks independently:
  1. `keyword_remind_find == true` ->prompt user for `keywords.find` / `keywords.content`; flip to `false`.
  2. `persona_defer_reminder_day == current_day` ->fire persona nudge: "Stage 2 commenting starts tomorrow (Day 15) and will be hard-blocked without a filled persona." Clear `persona_defer_reminder_day = null` after firing.
  3. `profile_customized == false` ->continue surfacing the Pre-flight reminder.
  4. **Stage transition notice (always fires Day 14)**: Read `config.yaml.approval_policy` and send end-of-run message:

    ```
    Calendar: <username> -Tomorrow is Day 15: Comment Phase begins

    Your approval mode: <approval_policy>

    [If approval_policy == "manual"]
    ->You will see comment variants in chat and can reply naturally, for example
      A/B/C/D, "use D", "pick the second one", "skip", or "make it shorter".
      A clear pick immediately continues into publish + verification; the approval
      checkpoint alone is not completion.

    [If approval_policy == "auto"]
    ->Agent handles everything -comments, posts, brand-bearing included.
      Brand Exposure check logged silently. You see the daily summary report.

    [If approval_policy == "auto_stage2"]
    ->Stage 2 auto-selected. Stage 3 brand requires approval.
      You see a daily summary report.

    Wednesday (weekly): a practice post will be submitted.
    ```

- **Day 21** -log current `comment_karma` for visibility. Do not apply a global karma block; each target sub's own `karma_gate` from recon decides whether it is safe.
- **Day 29** -`account_age_days < 30` OR `comment_karma < 20` ->extend comment stage. If `keyword_remind_brand == true` ->prompt user for `brand` keywords; flip to `false` regardless.
- **Stage 3 entry** -see `stage3-promote.md ->Entry Decision Card`.

---

## After Pre-flight Completes

Based on `effective_stage`, load the stage-specific reference file:

| effective_stage | Load next |
|---|---|
| `lurk` (Days 2-14) | `references/stage1-lurk.md` |
| `comment` (Days 15-29) | `references/stage2-comment.md` + `references/approval-rules.md` |
| `promote` (Day 30+) | `references/stage3-promote.md` + `references/approval-rules.md` |
| `pending_stage3_decision` | `references/stage3-promote.md` ->Entry Decision Card |
| `setup` (Day 1) | No further reference needed; exit after setup notice |

After stage work and cross-stage tasks complete: read `references/anomaly-detection.md` for a full-stop check. If safe, run the Daily Tail (`end-of-day-recon.md` ->`comment-follow-up.md`) when its preconditions pass, then return to `references/anomaly-detection.md` for final wrap-up + Daily Report.



