# Anomaly Detection + Daily Report

**Load this file at the end of every daily run**, after the daily tail finishes and before sending the Daily Report.

---

## Full-Stop Signals (check after every browser action)

If any of:
- `get markdown` on the target page contains:
  - `"permanently banned"` / `"suspended"` / `"Rate limit exceeded"` / `"locked post"` / `"restricted community"`
  - `"Removed by Reddit"` (admin removal)
  - `"you are doing that too much"`
  - `"whoa there, pardner"`
  - `"Too Many Requests"` / `"ratelimit"` / `"try again in"` / `"429"`
- `network requests` shows the submit POST returning 429 or 403
- AutoMod removal notice in inbox
- Any moderator DM in the inbox
- Avatar Menu Health Check shows a persistent red account/server-error toast such as `"We had a server error..."`
- Two consecutive `visibility: pending` in one run
- Submit POST returns 200 but comment/post fails browser-act visibility verification or `/user/<me>/submitted/` even after retry

**Then:**
1. Log `rate_limit_hit` (or specific reason code, including `removed_by_reddit`) to `activity_log.jsonl`.
2. If reason is `removed_by_reddit`, extract the subreddit name and:
   - Update `sub_profiles.json[<sub>].restrictions.temp_banned_until = today + 7 days`
   - Skip all activity in that sub for the next 7 days
3. Set `progress.json.rate_limit_hit_today = true` + `daily_skip_reason = "<reason>"`.
4. Treat the current `<run_session>` as finished; do not schedule more browser-act commands in it.
5. Exit. No more actions today.
6. Tomorrow's Pre-flight Step 2.5 will see the flag, run Stage 1 only, then clear it.
7. **>=2 `rate_limit_hit`-class events in 3 days** ->notify user. Detection: scan `activity_log.jsonl` for `type == "rate_limit_hit"` entries in the last 3 days; **don't maintain a separate counter**.

---

## Weekly Shadowban Check (Mondays, manual / user-driven)

See `stage3-promote.md ->Weekly Shadowban Check` for full routine. Summary: automatic detection was removed because in-session logged-in checks are unreliable (shadow-user-sees-own-content means false-negatives). The authoritative check is **manual, user-driven, on r/ShadowBan** -user posts the template, AutoMod replies `public` / `shadow` / `suspended`.

Agent surfaces the "run r/ShadowBan verification" prompt in the daily report when:
- 2+ `removed_by_filter` events in 7 days
- Repeated `reddit_403` returns
- Karma flat for 14 days despite activity
- User reports visibility issues

---

## Daily Report

### Before sending the report

1. Update `progress.json`: `last_run = today(account timezone)`, `last_run_scheduler_date = today_scheduler`, `comment_karma`, `post_karma`, `stage` (effective_stage cache). **Do not write `current_day`** -it's derived from `start_date` on read. Per-day activity counters are NOT stored in progress.json; compute from `activity_log.jsonl`.
2. Final screenshot to `last_run.png`; load it to verify. If loading fails ->**do not send the report**; tell user "browser failed to produce evidence".

### Counter sources

All computed from today's rows in `activity_log.jsonl`, filtered by `timestamp` falling inside today's account-tz date boundary:

| Report field | Source |
|---|---|
| `browsed <N> min` | Sum of dwell-time estimates across today's `upvote` / `subscribe` / recon entries (~1 min per event) |
| `upvoted <N>` | Count of `type: "upvote"` today |
| `commented <N>` | Count of `type: "comment"` today with `visibility in {"visible","pending"}`; `reply` and `inbox_reply` count in same bucket |
| `posted <N>` | Count of `type: "post"` today with `visibility == "visible"`; `removed_by_filter` does NOT count |
| `Skipped` | Count + distinct reasons from `type: "skip"` today |
| `age <N>d` | Actual Reddit profile age, or `account_age_days_at_onboarding + (today - onboarding_date).days`. Never use the backdated workflow start_date; if baseline age is missing, re-read the profile or report unknown. |
| `comment_karma` / `post_karma` | `progress.json` (updated by Pre-flight Step 8) |
| `subscribed <N> subs` | `progress.json.subscribed_subs.length` |

### Report format

```
Daily Report: <username>
<YYYY-MM-DD account-local> -Day <N> -<stage>
skill: reddit-warmup  browser: <browser_id>
Done: browsed <N> min, upvoted <N>, commented <N>, posted <N>
Warning: Skipped: <count> (list reasons if > 0)
Account: age <N>d -comment_karma <N> -post_karma <N> -subscribed <N> subs
Calendar: Tomorrow (Day <N+1>): <plain-English description>
```

**If any approval batches are still open** in `pending_approval/` when the daily report fires, append a count-only pending approvals section **after** the main report block:

```
---
Pending approvals: <N> item(s) awaiting review
```

Daily reports are **not actionable approval requests**. Do not include batch IDs, subreddit names, post titles, post/comment body text, variant text, or A/B/C/D letters in the Daily Report. Those details only belong in the standalone Approval Batch Request emitted when drafts are created/restored, because that request carries the batch anchor and item numbers needed for reliable Hot Approval execution. Batches are cleaned up after 7 days (Rule C4).

Skip-line examples:
- `persona_placeholders` -persona file has unresolved `<...>`
- `sub_forbids_self_promo` -target sub blocks promo; Path B deferred
- `karma_gate` -candidate sub's karma_gate > own karma
- `sparse_sub_list` -only 2 warmup subs configured
- `audience_night_hours` -fired during audience timezone's deep night
- `batch_stale_7d` -batch sat in pending_approval/ for 7+ days without a pick; deleted (post almost certainly dead)
- `persona_placeholders` -persona file has unresolved `<...>`
