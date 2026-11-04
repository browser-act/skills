# Cross-Stage: Notification + Inbox Check

**Load this file from `phase2-preflight.md` Step 6** (right after login check, before stage-specific main work). Runs every daily invocation on Day 2+, all stages.

A real user who opens Reddit checks their notification bell / inbox almost first thing. Leaving the notification counter at ">9+" for 14 days is a strong bot signal.

---

## Step A: Read-only Notification Check (ALL stages, Day 2+)

```bash
browser-act --session <run_session> navigate https://www.reddit.com/notifications/
browser-act --session <run_session> wait stable --timeout 20000
sleep $((RANDOM % 6 + 5))   # 5-11s dwell -"scrolling through what I missed"
browser-act --session <run_session> scroll down --amount 2
sleep $((RANDOM % 4 + 3))

# Visit the messages inbox (separate panel on Reddit)
browser-act --session <run_session> navigate https://www.reddit.com/message/inbox/
browser-act --session <run_session> wait stable --timeout 20000
sleep $((RANDOM % 5 + 5))
browser-act --session <run_session> get markdown
```

**Scan the markdown for:**

- **Moderator messages / modmail** (keywords: "from the mods of r/<sub>", "moderator", "automoderator") ->surface to user IMMEDIATELY; most are sub-removal notices or community warnings. Do NOT auto-reply.
- **Warning from Reddit admin** (keywords: "Reddit admin", "suspension warning", "site-wide rule", "your account has been flagged") ->CRITICAL. Surface to user, set `progress.json.paused = true` pending user review.
- **Friend request / DM** (Day < 30: no DMs from us; but we may receive them) ->log, don't open, surface to user for review.
- **Trophy / achievement unlock / Reddit premium ad** ->ignore; just visiting the page marks them "seen".
- **Unread comment/post reply** ->Day < 15: log count but don't engage yet. Day >=15: proceed to Step B.

Screenshot the inbox page to evidence folder as proof the check happened.

---

## Step B: Inbox Reply Engagement (Day 15+ only)

```bash
browser-act --session <run_session> navigate https://www.reddit.com/message/unread/
browser-act --session <run_session> wait stable --timeout 20000
browser-act --session <run_session> get markdown
```

For each unread reply (not modmail, not trophy, not username mention from an old thread):

1. `navigate <reply_permalink>`, `get markdown` for full thread context.
2. Generate 3 drafts (A/B/C), using thread context as `[post_body]` and last 3 comments as `[top-3 existing comments]`.
3. `approval-rules.md` ->Part 2 Brand Approval applies if any variant is brand-bearing.
4. Show to user ->user picks ->publish via `comment-publishing.md` ->Reply flow.
5. Mark read (navigate permalink once -Reddit flips "unread" automatically on view).
6. Log `type: "inbox_reply"`.

Cap: 3 inbox replies per run, oldest first. Reactive timing floor: >=2 min between replies. Skip if persona gate failed, `rate_limit_hit_today == true`, or reply is a bare emoji / single word.

---

## Step C: Stage-specific Reactions (always)

Regardless of Step B, always:

- If Step A flagged a **moderator / mod removal notice** for any sub in `subreddits.warmup + target` ->update `sub_profiles.json[<sub>].last_mod_action_date = today`.
- If Step A flagged an **admin warning** ->end today's run after this step; don't proceed to stage-specific writes.

---

## Logging

Every invocation appends a `notification_check` event to `activity_log.jsonl`:

```json
{"timestamp": "...", "type": "notification_check", "account_day": 8, "ip": "...",
 "unread_count": 3,
 "mod_messages_flagged": ["r/sub1 -post removed"],
 "admin_warnings_flagged": [],
 "friend_requests_flagged": 1,
 "engaged_replies": 0}
```

Day 14 report: if `notification_check` hasn't fired for 2+ consecutive days, surface "notification check was skipped N days in a row".

---

## After Notification Check Completes

Return to `phase2-preflight.md` execution flow -continue to Step 6.5 (Overview Scan) and the rest of the pre-flight sequence, then proceed to stage-specific work.

