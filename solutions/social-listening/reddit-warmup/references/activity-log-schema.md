# Activity Log Schema

`~/.reddit-warmup/<username>/activity_log.jsonl` is append-only, one JSON object per line. It is the **authoritative source** of what the skill did -daily reports, weekly post-mix proportions, historical activity plots, and shadowban checks all derive from it.

Every entry has these four common fields, plus type-specific fields below.

## Common fields (every entry -all required)

| Field | Type | Notes |
|-------|------|-------|
| `timestamp` | string | ISO 8601 with offset, in the **account's timezone** (e.g. `2026-05-08T10:15:22+08:00`) |
| `type` | string | One of the event types listed below |
| `account_day` | integer | Derived `current_day` at write time (convenience -the exact start_date-based number) |
| `ip` | string | Current session IP from `ipinfo.io`; used for IP-drift detection and shadowban triage |
| `run_session_id` | string | Temporary browser-act session used for this flow. Execution proof only; never use it as a durable workflow key |
| `url_confirmed` | string | The exact URL browser-act was on when this event happened, from `browser-act state` or browser-act navigation output. NEVER a guess or template -must be real output |
| `page_title` | string | From `browser-act get title` or the first heading in `browser-act get markdown`. NEVER a guess |
| `cli_version` | string | Output of `browser-act --version` captured at Phase 2 Pre-flight Step 0a. Only required on the **first** log entry of each daily run (subsequent entries same run can omit; the first-entry cli_version covers the whole run). Used for audit when a Reddit UI drift coincides with a browser-act release |

**Anti-hallucination rule:** `run_session_id` / `url_confirmed` / `page_title` can only come from actual browser-act output. Agents that write these fields without having run the corresponding browser-act commands are fabricating logs -this is forbidden (see `SKILL.md ->Execution Proof`). `run_session_id` is not a recovery key; use `username`, `batch_id`, and `browser_id` for recovery.

**Only exception:** the `browser_open_failed` event, which documents the failure mode when browser-act itself couldn't launch. That event has an `error` field in place of `url_confirmed` + `page_title`:

```json
{"timestamp": "...", "type": "browser_open_failed", "account_day": 3, "ip": null,
 "run_session_id": "<run_session>",
 "error": "<browser-act's actual error output>"}
```

After writing `browser_open_failed`, stop the current flow -no other events may follow from that failed `<run_session>`.

---

## Event types

### `upvote`

```json
{"timestamp": "...", "type": "upvote", "account_day": 8, "ip": "...",
 "subreddit": "r/<sub>", "post_url": "https://www.reddit.com<post_path>",
 "post_title": "<title truncated to 120 chars>"}
```

### `subscribe`

```json
{"timestamp": "...", "type": "subscribe", "account_day": 5, "ip": "...",
 "subreddit": "r/<sub>"}
```

### `comment`

```json
{"timestamp": "...", "type": "comment", "account_day": 17, "ip": "...",
 "subreddit": "r/<sub>", "post_url": "https://www.reddit.com<post_path>",
 "post_title": "<title>", "content": "<full comment text>",
 "variant": "A | B | C | D",
 "karma_before": <int>,
 "contains_brand": true | false,              // true if any config.yaml ->keywords.brand term matches content (case-insensitive)
 "brand_mention_intent": "none | accidental | deliberate",
 //   "none"       -contains_brand == false
 //   "accidental" -contains_brand == true but variant is A/B/C (brand leaked from persona, not deliberate)
 //   "deliberate" -variant == D (Problem-Solution pattern, target-sub brand insertion)
 "content_hash": "<sha256 of normalized content>",  // for duplicate-detection
 //   Structured publish-layer fields -from the /user/<me>/comments/ browser-act visibility check in comment-publishing.md
 "comment_id": "t1_xxxxxxx",                  // required on success; null on visibility != "visible"
 "permalink": "/r/<sub>/comments/<post_id>/comment/<comment_id_short>/",
 "depth": "0" | "1+",                         // "0" = top-level, "1+" = nested reply
 "parent_id": "t3_xxxxxxx" | "t1_xxxxxxx",   // t3_ for top-level (the post), t1_ for nested reply
 "visibility": "visible | pending"}
```

**comment_id / permalink / depth / parent_id semantics:**
- All four come from browser-act `state` / markdown on `/user/<current_username>/comments/` (see `comment-publishing.md ->Browser-act visibility verify`). Never guess or template them.
- On `visibility: "visible"`: all four required, `comment_id` must start with `t1_`.
- On `visibility: "pending"` (AutoMod silent filter / stale view): write `comment_id: null`, `permalink: null`, `depth: null`, `parent_id: null`. Reader code must handle null.
- Camping / feedback-loop / Inbox Reply context lookups navigate directly to `permalink` -no username-based scanning needed.

### `post`

```json
{"timestamp": "...", "type": "post", "account_day": 35, "ip": "...",
 "subreddit": "r/<sub>", "post_url": "<url>",
 "post_title": "<title>", "content": "<body text>",
 "post_kind": "help_seeking | sharing | promotional",
 "post_format": "text | link | image",
 "image_path": "~/.reddit-warmup/<username>/images/...",      // only when post_format == "image"
 "image_source": "user_provided | google_images",             // only when post_format == "image"
 "content_href": "<linked url>",                              // only when post_format == "link"
 "karma_before": <int>,
 "contains_brand": true | false,     // see comment schema above
 "content_hash": "<sha256 of normalized title + body>",
 //   Structured publish-layer fields -populated from browser-act verification, see "source attribution" below
 "post_id": "t3_xxxxxxx",                        // required on success; null on visibility != "visible"
 "permalink": "/r/<sub>/comments/<id>/<slug>/",
 "post_type_rendered": "text | link | gallery | video",  // actual type reported by browser-act verification (gallery = single-or-multi image)
 "created_timestamp": "<unix_ts>",
 "removed_by_filter": true | false,              // true = submitted but AutoMod / Reddit filter hid the detail page
 "filter_banner": "<bannerText>" | null,         // present when removed_by_filter == true; the banner text matched on the permalink
 "visibility": "visible | pending | removed_by_filter"}
```

**Source attribution for publish-layer fields:**
- `post_id` / `permalink` / `post_type_rendered` / `created_timestamp` -from browser-act `state` / markdown on `/user/<current_username>/submitted/` (the Phase 1 verify in `image-posting.md ->Verify`). Never guess.
- `removed_by_filter` / `filter_banner` -from grepping the post's permalink detail page markdown for `"removed by Reddit's filters"` / `"removed by moderators"` / `"[removed]"` / `"Sorry, this post was removed"` (the Phase 2 verify in `image-posting.md ->Verify`).
- `post_id` must start with `t3_` on success.
- `removed_by_filter: true` ->`visibility: "removed_by_filter"` (counts against the weekly post cap anyway -the attempt was made). `filter_banner` carries the truncated banner string for later audit.
- On `visibility: "pending"` (Phase 1 couldn't find the post on `/user/<me>/submitted/`): set `post_id: null`, `permalink: null`, `post_type_rendered: null`, `removed_by_filter: null`, `filter_banner: null`. Reader code must handle null.
- Camping polls `permalink` directly (skip if `removed_by_filter: true` -no replies will come).

Weekly Post Type Mix aggregates by grouping on `post_kind` within the same week-of-`account.timezone`. **imported entries do not participate** in any aggregation (see next paragraph).
9:1 brand ratio enforcement (`approval-rules.md ->Part 2 Brand Approval` + `stage3-promote.md ->Brand Exposure Target`) aggregates on `contains_brand` across both `type: "comment"` and `type: "post"`, **but excludes any entry with `imported: true`** -imported entries describe the account state **before** the skill took over, so they should not count toward the brand-exposure rhythm after takeover.

### `reply` (camping replies to our post)

Same publish mechanics as `comment` -goes through `comment-publishing.md ->Reply flow` (pure browser-act CLI: click Reply button idx for target tid ->`browser-act input <reply_lexical_idx> "<text>"` ->`browser-act click <reply_submit_idx>` ->browser-act visibility verify). Carry the structured fields:

```json
{"timestamp": "...", "type": "reply", "account_day": 35, "ip": "...",
 "our_post_url": "<url of our post>",
 "replying_to": "<parent comment id or 'op'>",   // t1_xxx of the comment we're replying to, or "op" if replying to OP thread
 "content": "<our reply text>",
 "variant": "A | B | C",
 "comment_id": "t1_xxxxxxx",                     // our reply's id -from /user/<me>/comments/ visibility check
 "permalink": "/r/<sub>/comments/<post_id>/comment/<our_reply_short>/",
 "depth": "1" | "2+",
 "parent_id": "t1_xxxxxxx",
 "visibility": "visible | pending"}
```

### `inbox_reply` (someone replied to our earlier comment -see Inbox Tracking in SKILL.md)

Our own response (when we reply) goes through the same nested-reply flow (`comment-publishing.md ->Reply flow`) and carries the `comment_id` + `permalink` from the visibility check.

```json
{"timestamp": "...", "type": "inbox_reply", "account_day": 22, "ip": "...",
 "their_comment_url": "<url of their reply>",
 "in_thread_post_url": "<post we originally commented on>",
 "their_content": "<their text>",
 "our_response_url": "<url>" | null,              // set if we replied (matches our_response_comment_id's permalink)
 "our_response": "<our text>" | null,
 "variant": "A | B | C" | null,
 "our_response_comment_id": "t1_xxxxxxx" | null,  // our reply's id -from /user/<me>/comments/ visibility check when we responded
 "our_response_parent_id": "t1_xxxxxxx" | null,   // the t1_xxx of their_comment_url
 "visibility": "visible | pending" | null}
```

### `brand_ratio_decision`

```json
{"timestamp": "...", "type": "brand_ratio_decision", "account_day": 35, "ip": "...",
 "ratio_before": {"rolling_10_brand_count": 2, "weekly_promo_posts": 1, "weekly_brand_comments": 1},
 "risk_level": "low | moderate | elevated",
 "user_choice": "rewrite | publish_anyway | skip",
 "draft_summary": "<first 80 chars of the draft, truncated>"}
```

### `replay_restored`

Fired when Pre-flight Pass B moves a batch from `drafts/` back to `pending_approval/` because its `replay_after` date has arrived (originally set by a "save-for-next-week" pick on a weekly-cap warning).

```json
{"timestamp": "...", "type": "replay_restored", "account_day": 42, "ip": "...",
 "batch_id": "<original batch id>",
 "originally_deferred_at": "<ISO when save-for-next-week was picked>",
 "replay_after": "<the target date that just matured>",
 "approval_status": "pending",
 "approval_note": "no fixed approval window; waits for user pick or 7-day stale cleanup"}
```

### `notification_check`

Fired once per daily run after the Cross-Stage Notification + Inbox Check completes (see `SKILL.md ->Cross-Stage: Notification + Inbox Check`). Records whether the account saw + acted on its inbox -part of the "responsive account" behavior pattern that counters "new-account-farm" signatures.

```json
{"timestamp": "...", "type": "notification_check", "account_day": 8, "ip": "...",
 "unread_count": <int>,                            // count of unread notifications scanned
 "mod_messages_flagged": ["r/sub1 -post removed", ...],  // mod DM subjects, empty array if none
 "admin_warnings_flagged": ["..."],                 // Reddit admin warnings, empty array if none
 "friend_requests_flagged": <int>,                  // count of inbound DMs/friend requests (we don't reply Day < 30)
 "engaged_replies": <int>                           // > 0 only on Day 15+ (Step B ran); 0 on Day 2-14 (read-only)
}
```

If `admin_warnings_flagged` is non-empty ->caller sets `progress.json.paused = true` and exits today's run after this event.

### `weekly_cap_warning`

Fired when a Path B promotional post is about to be generated but `promo_posts_this_week >= 1`. The skill shows a warning prompt (see `approval-rules.md ->Weekly Posting Cap`) and logs the user's decision here. This is a record of the advisory cap firing, NOT a skip -the actual publish (if `user_choice == yes`) is logged separately as a `post` event.

```json
{"timestamp": "...", "type": "weekly_cap_warning", "account_day": 35, "ip": "...",
 "promo_posts_this_week_before": 1,
 "user_choice": "yes | no | save-for-next-week",
 "draft_summary": "<first 80 chars of the title, truncated>",
 "replay_after": "<ISO of next Monday in account-tz>"}
```

`replay_after` is present only when `user_choice == "save-for-next-week"` -tells Pre-flight when to auto-restore the batch from `drafts/` to `pending_approval/`.

### `upvote_snapshot` (written by the Comment Feedback Loop to record an old comment's current score)

Produced by the daily-tail Comment Feedback Loop (see `comment-follow-up.md`), which revisits older comments and snapshots their score. Downstream aggregation plots score trajectories and maintains `progress.json.karma_by_sub`.

```json
{"timestamp": "<ISO+offset>", "type": "upvote_snapshot", "account_day": 25, "ip": "...",
 "comment_permalink": "<url>",
 "subreddit": "r/<sub>",
 "score": <current_score>,           // current vote total of our comment (may be negative)
 "reply_count": <int>,                // number of direct replies to our comment
 "new_replies": <int>,                // new reply count seen this pass (excluding AutoModerator / ourselves)
 "run_session_id": "<run_session>",
 "url_confirmed": "<permalink>",
 "page_title": "<from get title>",
 "evidence_screenshot": "evidence/<ts>-revisit-<comment_id>.png"}
```

### Skips and anomalies

Every time the skill **declines** to do something, log why -daily report sums these to explain gaps.

```json
{"timestamp": "...", "type": "skip", "account_day": 16, "ip": "...",
 "skipped_action": "comment | post | promo_post | subscribe | stage1_browse_sub | inbox_reply | watchtower_reply | recon_batch | feedback_revisit",
 "reason": "persona_empty | persona_placeholders | persona_missing_file | all_subs_filtered | rate_limit_today | captcha_blocked | sparse_sub_list | no_qualifying_post | commenter_karma_mismatch | watchtower_not_active | budget_approaching | low_karma_daily_cap | random_human_jitter | planned_irregular_rhythm_skip | audience_night_hours | sub_forbids_self_promo | dom_drift | batch_stale_7d | parent_post_removed | post_locked | wrong_page_submit_misdirect | click_failed | fill_verification_failed | original_thread_visibility_failed | reddit_400 | reddit_403 | reddit_429 | reddit_5xx | removed_by_filter | post_not_in_submitted_list | weekly_cap_declined | avatar_menu_unavailable | account_health_avatar_server_error",
 "detail": "<free text context>",
 // Additional fields for specific reasons:
 "elapsed_minutes": <int>,      // for budget_approaching
 "budget_minutes": <int>,       // for budget_approaching
 "skipped_actions": ["..."],    // for budget_approaching -what got deferred

 // Publish-verdict fields (comment-publishing.md / image-posting.md verdict tree):
 "http_status": <int|null>,        // for reddit_4xx / reddit_5xx -the actual response code
 "request_id": "<id>",             // for reddit_* -browser-act network requests <id> for forensics
 "banner_text": "<string>",        // for removed_by_filter -the filter banner copy
 "fill_actual_length": <int>,      // for fill_verification_failed -what the Lexical editor actually contained
 "fill_expected_length": <int>     // for fill_verification_failed -what we tried to fill
}
```

### `account_risk_signal`

Fired when a pre-write account health check detects an account-level anomaly, especially the top-right avatar menu showing a persistent Reddit server-error toast.

```json
{"timestamp": "<ISO+offset>",
 "type": "account_risk_signal",
 "account_day": <N>,
 "ip": "...",
 "trigger": "avatar_menu_server_error",
 "page_excerpt": "<first 300 chars from state/markdown>",
 "evidence_screenshot": "evidence/<ts>-avatar-health-after.png",
 "action": "blocked_write_actions_today",
 "progress_flag": "account_risk_flagged"}
```

### Environment events

```json
{"timestamp": "...", "type": "ip_drift", "account_day": 50, "ip": "<new_ip>",
 "old_ip": "<previous_ip>", "old_geo": "...", "new_geo": "..."}

{"timestamp": "...", "type": "env_migration_day", "account_day": 51, "ip": "...",
 "migration_day": 1, "behavior": "browse_only | browse_upvote | browse_upvote_subscribe | normal",
 "clean_login": true | false}

{"timestamp": "...", "type": "captcha_encountered", "account_day": 23, "ip": "...",
 "where": "preflight | registration | login | mid_task",
 "auto_solve_attempted": true | false,
 "auto_solve_succeeded": true | false,
 "handled_by": "auto | user | aborted_unattended"}

{"timestamp": "...", "type": "rate_limit_hit", "account_day": 24, "ip": "...",
 "trigger": "whoa_there | 429 | try_again_in | too_many_requests | automod_removal | mod_dm | autofilter_streak",
 "page_excerpt": "<first 200 chars>",
 "mod_dm_author": "u/..." | null,       // for mod_dm trigger
 "stopped_actions": ["comment", "post", "upvote", "inbox", "watchtower"]}

{"timestamp": "...", "type": "shadowban_check", "account_day": 28, "ip": "...",
 "source": "r_shadowban_automod | manual_user_report",
 "result": "public | shadow | suspended",
 "triggers_that_prompted_check": ["removed_by_filter_2plus_in_7d", "reddit_403_repeated", "karma_flat_14d", "user_visibility_complaint"],
 "user_reported_at": "<ISO>"}
```

### Session boundaries

```json
{"timestamp": "...", "type": "run_start", "account_day": 17, "ip": "...",
 "unattended": true | false, "stage": "lurk | comment | promote"}

{"timestamp": "...", "type": "run_end", "account_day": 17, "ip": "...",
 "duration_seconds": <int>,
 "counters": {"upvotes": 3, "comments": 1, "posts": 0, "skips": 0}}
```

---

## Rules for writers

- **Never update-in-place** -all entries append; correctness comes from time-ordering, not row edits.
- **One action = one entry** -a failed comment attempt that gets retried = 2 entries (one skip with `reason: "<why_skipped>"`, one eventual comment if it succeeds).
- **Never log secrets** -no passwords, no full proxy URLs with credentials, no CAPTCHA images, no persona file contents verbatim.
- **Content truncation** -comment/post body fields may store the full text for audit and de-dup checks. Daily reports must not render pending approval body text, variant text, titles, or batch IDs; they only show aggregate counts.
- **IP recording** -log IP for every entry so shadowban triage can correlate. If `ipinfo.io` call fails, write `"ip": null` but still emit the entry.

## Rules for readers

- Always parse line-by-line; don't try to load the whole file as one JSON object.
- Weekly aggregations: filter by `timestamp` falling inside `week_start` ->`week_start + 7d` **in `account.timezone`**.
- When computing `current_day` for historical analysis, **derive from timestamp + start_date**, don't trust `account_day` across clock changes.
- When the file doesn't exist (fresh account) or is empty, treat as "no history" -not as an error.

