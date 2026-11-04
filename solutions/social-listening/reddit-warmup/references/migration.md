# Existing-account environment migration

Load after `phase2-preflight.md` browser open, authoritative login verification, and Avatar Menu Health Check succeed with `migration_only == true`. Use the configured browser and proxy. This routine replaces the ordinary stage flow and daily tail for this run; it is not a second scheduled task.

## State and one-run boundary

- Read `env_migration`, `migration_day`, `migration_clean_logins`, and `last_migration_scheduler_date` from progress. Use the `today_scheduler` already computed by preflight.
- If `last_migration_scheduler_date == today_scheduler`, show the previous result and stop without browser actions or counter changes. The normal `last_run_scheduler_date` check also applies.
- A migration day is one completed scheduled migration run, not one browser reopen. Start at 1. Repeated commands and approval replies never increment it.
- If migration counters are missing or invalid, stop for state review; do not silently turn migration off or overwrite progress from its template.

## Restricted activity

Keep the current migration day's limit throughout this run, even if the third clean login will finish migration at the end.

| migration_day | Allowed activity | Session budget |
| --- | --- | --- |
| 1-2 | Read-only browsing of configured warmup communities | 5-10 minutes |
| 3 | Browsing; up to 1-2 post upvotes | 10-15 minutes |
| 4-5 | Browsing, upvotes, and at most one eligible subscription | 15-20 minutes |
| 6+ | Stage 1 limits while migration remains active | Stage 1 budget |

Never comment, post, send DMs, or run promotional work during migration. Use `stage1-lurk.md` current-state selection for any permitted upvote/subscription and honor its already-selected checks and rules-reading gate. Day 1-2 perform only its read-only navigation/extraction steps. Account-health, rate-limit, challenge, or login failures stop activity; do not use another profile/proxy to continue.

## Record and finish

1. Classify the whole run as clean only when login and account-health checks passed and no CAPTCHA, rate-limit, or account anomaly occurred anywhere in it. Solving a challenge does not make that run clean.
2. On a completed clean run, increment `migration_clean_logins` by 1. A non-clean attempted run resets the consecutive-clean counter to 0; do not count a browser-open/network failure as a successful migration day.
3. After completed restricted activity, append a real `env_migration_day` event with screenshot evidence and the actual behavior performed. Increment `migration_day` once for the next run. Record both `last_migration_scheduler_date` and `last_run_scheduler_date` as `today_scheduler`, plus the actual `last_run` timestamp. Save all progress fields together without replacing unrelated state.
4. If the updated consecutive-clean count is at least 3, set `env_migration = false`. Preserve counters and the completion event for audit; the normal stage flow resumes only on the next scheduled run. Do not run it again today.
5. Take the final screenshot and send the normal report with the restricted actions and whether migration continues. Do not start daily recon/feedback.

If login/health fails before this routine can start, preflight still records the failed attempted run: reset `migration_clean_logins = 0`, set `last_migration_scheduler_date` and `last_run_scheduler_date` to `today_scheduler`, keep `migration_day` unchanged, and set the actual failure reason. An API/network failure without a page screenshot is a local attempt status, not a fabricated browser activity event. Surface the failure separately and wait for the next scheduled day or explicit user-directed recovery.
