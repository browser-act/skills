# End-of-Day Recon (daily tail)

**Purpose:** pre-warm `sub_profiles.json` for the subs likely needed in tomorrow's run. The next day's main flow can then use cached rules, AutoMod filter rate, and typical poster karma instead of doing live recon before every interaction.

Risk posture: this is not a second automated session. It runs only as a light tail of the same once-per-day scheduled flow. If the daily run is already heavy, the account is rate-limited, or the browser state is unstable, skip recon and report the skip reason.

---

## Trigger conditions

Runs only from `SKILL.md -> Daily Tail` after the main stage flow has completed.

Do not schedule a separate recon cron/task. Older versions used an evening recon trigger; new accounts should use one daily scheduled run and let this file run conditionally at the end of that run.

Order:

```text
main flow + inbox + optional watchtower -> End-of-Day Recon -> Comment Feedback Loop -> final report
```

---

## Preconditions for running

Any failure means skip recon and record the reason in the daily report:

- Main flow has reached the daily-tail step.
- `progress.json.rate_limit_hit_today != true`.
- Login state is still valid.
- A fresh `<run_session>` can be opened with the configured `browser_id` if the main flow's browser-act session has already closed.
- Daily run has enough remaining time budget for a light tail.
- There is at least one eligible target from Step 1.

Missing active browser-act session is expected and is not a failure. Open the same `browser_id` in a fresh `<run_session>`; do not create a new browser profile and do not switch accounts.

---

## Step 0 - Next-Day Sub Planning

Before picking recon targets, determine which subs are likely needed tomorrow and flag subscription gaps.

```text
tomorrow_day = progress.json.current_day + 1
if tomorrow_day <= 21:
    tomorrow_candidates = config.yaml.subreddits.warmup
else:
    tomorrow_candidates = config.yaml.subreddits.warmup + subreddits.target.primary + subreddits.target.secondary
```

Subscription gap priority:

| Sub tier | Condition | Priority | Action |
|----------|-----------|----------|--------|
| `target.primary` | needed tomorrow (`day > 21`) and unsubscribed | P0 | Put at the front of the recon queue; subscribe opportunity may fire if quota is unused |
| `target.primary` | not yet needed but unsubscribed | P0.5 | High priority; subscribe if no P0 sub consumed today's quota |
| `target.secondary` | unsubscribed | P1 | Normal first-contact priority |

Target sub subscriptions are still handled by the main flow first. Recon's Subscribe Opportunity is an enhancement layer that adds richer recon data before subscribing and acts as a fallback if the main flow missed a safe sub. `today_subscribe_count == 0` prevents more than one subscription per day.

After Step 2 and Step 3.5, write:

```json
"tomorrow_planned_subs": ["r/<sub_a>", "r/<sub_b>"]
```

The next day's pre-flight can use this list to pick the first sub to inspect.

---

## Step 1 - Pick target subs

Keep recon light. Default cap: **3 subs**. Allow up to **5** only when at least one P0/P0.5 subscription gap exists or tomorrow would otherwise have no valid sub.

Priority ladder, shuffled randomly within each tier:

| Priority | Source | Reason |
|----------|--------|--------|
| P1 | Configured warmup/target subs with no `sub_profiles.json` entry | First contact needs a profile |
| P2 | Subs whose `recon_at` is older than 14 days | Rules/filter rate may have changed |
| P3 | Subs with `last_verdict == "warm-up-first"` and `retry_when_comment_karma <= current comment_karma` | Previously blocked sub may now be eligible |
| P4 | Potential subs from accepted discovery output | Optional, low priority |

If all tiers combined return fewer than 3, run fewer than 3. Do not invent work.

---

## Step 2 - Run recon on each target sub

Use the current `<run_session>` only if it is still active inside the same browser-act flow. Otherwise open a fresh `<run_session>` with the configured `browser_id`.

Action skeleton:

```bash
# Rules
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/about/rules
browser-act --session <run_session> wait stable
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-recon-rules-<sub>.png
browser-act --session <run_session> get markdown

# Wiki, optional
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/wiki/index
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown

# /new for AutoMod filter rate
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/new/
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown

# /top for typical poster karma
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/top/?t=week
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Parse and merge into `sub_profiles.json`:

- `rules_summary`
- `karma_gate`
- `age_gate_days`
- `forbids_self_promo`
- post shape restrictions
- `automod_filter_rate`
- `median_recent_poster_karma`
- `recon_at = today(account timezone)`

Write a `sub_recon` event to `activity_log.jsonl`:

```json
{
  "timestamp": "<ISO+offset>",
  "type": "sub_recon",
  "subreddit": "r/<sub>",
  "trigger": "daily_tail",
  "cached_before": false,
  "fields_updated": ["rules_summary", "karma_gate", "automod_filter_rate"],
  "run_session_id": "<run_session>",
  "url_confirmed": "<last navigate URL>",
  "page_title": "<last get title>",
  "evidence_screenshot": "evidence/<ts>-recon-rules-<sub>.png"
}
```

### Subscribe Opportunity

Immediately after writing the `sub_recon` event, run a subscribe eligibility check.

All gates must pass:

1. Sub is not already in `progress.json.subscribed_subs`.
2. `recon_result.karma_gate <= own comment_karma`.
3. `recon_result.age_gate_days <= own account_age_days`.
4. `recon_result.automod_filter_rate != "high"`.
5. Today's `activity_log.jsonl` has zero `type: "subscribe"` entries.

If all gates pass:

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-subscribe-<sub>.png
browser-act --session <run_session> state
# Read the current state and locate this subreddit's Join/Subscribe button.
# If already Joined/Leave/Unsubscribe, skip the click; do not unsubscribe.
browser-act --session <run_session> click <current_join_idx>
browser-act --session <run_session> state
browser-act --session <run_session> wait stable --timeout 10000
browser-act --session <run_session> get markdown
```

Confirm by scanning for label change to "Unsubscribe" / "Joined" / "Leave". On success, append `r/<sub>` to `progress.json.subscribed_subs` and log:

```json
{
  "timestamp": "<ISO+offset>",
  "type": "subscribe",
  "subreddit": "r/<sub>",
  "trigger": "daily_tail_recon_subscribe",
  "account_day": <N>,
  "run_session_id": "<run_session>",
  "url_confirmed": "https://www.reddit.com/r/<sub>/",
  "page_title": "<from get title>",
  "evidence_screenshot": "evidence/<ts>-subscribe-<sub>.png"
}
```

If the label is unchanged or the button is missing, log `skip("subscribe_confirm_failed")` and do not add to `subscribed_subs`.

Either success or failure consumes today's subscribe quota. Skip subscribe checks for remaining subs in this recon batch.

---

## Step 3 - Pacing and limits

- Wait 90-180 seconds after finishing recon on one sub before starting the next.
- The entire recon tail has a hard 10-minute cap.
- On time cap, stop and defer remaining targets to the next daily run. Log `skip("recon_batch_time_cap")` with the deferred subs.
- If any page returns rate-limit signals ("whoa there", "too many requests", similar), enter the anomaly full-stop path and abandon remaining recon.

---

## Step 3.5 - Next-Day Sub Preview

For each sub in `tomorrow_candidates` that has a fresh enough profile, run a brief preview:

### Pass A - Rules confirmation

If the profile was just written/refreshed in Step 2, reuse it. Otherwise read `/about/rules` and confirm any day-of-week or time-of-day restrictions that could block tomorrow's interaction.

If restrictions block tomorrow, set:

```json
"rule_conflict_tomorrow": true
```

and exclude the sub from `tomorrow_planned_subs`.

### Pass B - Hot feed scan

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/hot/
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> get markdown
```

Extract up to 5 non-pinned posts: title, short body snippet or post type, score, and comment count. Store:

```json
"tomorrow_hot_context": [
  {"title": "...", "snippet": "...", "score": 0, "comment_count": 0}
],
"tomorrow_note": "Hot topic: X. Tone: casual/humor/relatable. Avoid: Y."
```

Time budget: 30-60 seconds per sub. If the recon tail is near the 10-minute cap, skip Pass B for the last sub and mention it in the daily report.

### Confirm or reject each sub for tomorrow

Include a sub in `tomorrow_planned_subs` only when:

- subscribed,
- no rule conflict tomorrow,
- recon profile is valid,
- `automod_filter_rate` is not high for this account's current karma.

Log exclusions. If `tomorrow_planned_subs` is empty, surface a warning in the daily report.

Write `next_day_preview` events:

```json
{
  "timestamp": "<ISO+offset>",
  "type": "next_day_preview",
  "subreddit": "r/<sub>",
  "trigger": "daily_tail",
  "rule_conflict_tomorrow": false,
  "tomorrow_note": "<one-line note>",
  "posts_scanned": <N>,
  "included_in_tomorrow_plan": true,
  "run_session_id": "<run_session>"
}
```

---

## Step 4 - Handoff back to main flow

After recon finishes, continue to the Comment Feedback Loop, then final wrap-up and daily report.

Daily report snippet:

```text
End-of-Day Recon: refreshed r/<a>, r/<b> (cache valid 14d)
Subscribed: r/<b> (now <N> total subs)
Tomorrow's plan: r/<a>, r/<b>
Deferred: r/<d> due to time cap
No subs confirmed for tomorrow - check subscription status and karma gates
```

Only include lines that apply. If no recon target was picked, omit the recon section but still include `Tomorrow's plan` if it was already known.

---

## Relationship with Comment Feedback Loop

Both routines run inside the same daily tail, with End-of-Day Recon first and Comment Feedback Loop second:

- Recon operates at the subreddit level.
- Feedback Loop operates at the comment/post level.
- Recon first ensures the feedback loop reads fresh `sub_profiles.json` data.

Insert a 90-180 second pause between the two. If recon used most of the time budget, skip Feedback Loop and record the reason.
