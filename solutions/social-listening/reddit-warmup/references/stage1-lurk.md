# Stage 1: Lurk (Days 2-14)

**Load this file when `effective_stage == "lurk"`** (after phase2-preflight.md completes).

Browse + upvote only. No comments, no posts. Goal: 50-80 upvotes, 5 subscribed subs by Day 14 (3 warmup + 2 primary target). Full timing parameters (dwell times, upvote caps, weekly pattern) in `stages.md`.

---

## Daily Browse Flow

For each warmup sub in `subreddits.warmup` (rotate by persona alignment -see `stages.md ->Stage 1 parameters`):

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/hot/
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Read 10-15 posts. Per post to upvote (max 2/sub Days 4-7, max 3/sub Days 8+):

```bash
browser-act --session <run_session> navigate https://www.reddit.com<post_path>
browser-act --session <run_session> wait stable
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-upvote.png
browser-act --session <run_session> state
# Read the current state: locate the target POST's Upvote button, not a comment vote.
# If already pressed/selected, leave it unchanged and skip the click (do not toggle off).
browser-act --session <run_session> click <current_post_upvote_idx>
browser-act --session <run_session> state
# Count success only if that post's vote is now selected. If uncertain, log an unverified skip; do not click again.
browser-act --session <run_session> wait stable
```

Days 2-3 are browse-only. Day 4+ upvotes active.

Before upvoting in a sub the account has never touched, **read its sidebar rules once** (`navigate /r/<sub>/about/rules` ->`get markdown`) -see `browser-act-rules.md` ->Rule-Reading Gate ->"Upvoting newly-discovered subs".

---

## Subscribe Schedule (Stage 1 only)

| Days | Total subscribed subs |
|------|-----------------------|
| 1-3  | 0 |
| 4-6  | 1 |
| 7-10 | 2 |
| 11-14 | 3 |

Never subscribe to > 1 sub in a single day. Pick from `subreddits.warmup` by persona alignment.

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/
browser-act --session <run_session> state
# Locate Join/Subscribe for this subreddit in the current state.
# Joined/Leave/Unsubscribe means already subscribed: do not click it.
browser-act --session <run_session> click <current_join_idx>
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
# Confirm Joined/Leave/Unsubscribe for the same subreddit before recording success.
```

**After successful subscribe:** push `r/<sub>` to `progress.json.subscribed_subs` (if not already present), and append `type: "subscribe"` to `activity_log.jsonl`.

**Stage 2+ subscriptions (Day 15+):** Handled via End-of-Day Recon ->"Subscribe Opportunity" step. Same 1/day cap. See `end-of-day-recon.md ->Step 2`.

---

## Persona-Driven Sub Selection

Persona alignment only ranks the already-approved broad warmup subs. It must never add professional, domain-expert, career, business, technical, marketing, startup, regulated-advice, or brand-adjacent subs into the warmup set, regardless of the persona.

`stages.md ->Stage 1 parameters` covers the full persona-sub alignment logic. Brief summary:

- **Which sub to browse first today** -rotate among `subreddits.warmup`, preferring the sub whose topic matches `persona.interests` most closely today. Over a 7-day window all warmup subs should see roughly equal time; but each day's starting sub should feel intentional.
- **Which posts to upvote** -scan the first 15 posts of Hot/New/Rising. Upvote up to the per-day cap for posts that align with `persona.interests` or `persona.backstory_keywords`. If nothing aligns well, just dwell; don't force an upvote.

**Persona empty (Day 1 deferred):** fall back to dwell-only, no sub preference, upvote posts with high engagement (score > 10).

---

## End of Stage 1 Run

After the lurk loop completes:

- Run `references/anomaly-detection.md` full-stop checks on anything flagged during the session.
- Update `progress.json`: `comment_karma`, `post_karma`, `subscribed_subs`. Final `last_run` / `last_run_scheduler_date` writes happen in the run wrap-up.
- Increment `keyword_rotation.find_index` by 0 (no keyword consumption in Stage 1 -skip the increment).
- Return to `SKILL.md -> Daily Tail`; `end-of-day-recon.md` and `comment-follow-up.md` may run once as the same daily scheduled flow if their preconditions pass. The Daily Report is sent after that final wrap-up.
