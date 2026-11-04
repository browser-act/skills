# Comment Feedback Loop (daily tail)

**Purpose:** revisit a small capped set of older comments to learn which subreddits produce karma for this persona and to catch genuine reply opportunities.

1. **Data flywheel:** update `progress.json.karma_by_sub` so later Stage 2/3 sub selection can use weighted random instead of uniform random.
2. **Reply opportunity:** if an older comment received a new meaningful reply, generate A/B/C drafts and route them through `approval-rules.md`. A clear user pick later publishes that single reply; it does not re-run the daily task.

Risk posture: this loop runs only as a light tail of the once-per-day scheduled flow. Do not schedule a separate pm follow-up job.

---

## Trigger conditions

Runs only after End-of-Day Recon inside `SKILL.md -> Daily Tail`.

Order:

```text
main flow + inbox + optional watchtower -> End-of-Day Recon -> Comment Feedback Loop -> final report
```

Preconditions for running; any failure means skip and report the reason:

- Main flow completed.
- `progress.json.rate_limit_hit_today != true`.
- Login state is still valid.
- A current `<run_session>` is active, or a fresh `<run_session>` can be opened with the configured `browser_id`.
- Daily run has enough remaining time budget.
- At least one eligible comment target exists.

Missing active browser-act session is expected. Reopen the same `browser_id` in a fresh `<run_session>`; do not create a new browser profile and do not switch accounts.

---

## Step 1 - Pick revisit targets

`progress.json.comment_metrics` stores metadata for published comments. Treat it as an empty array if missing:

```json
{
  "comment_metrics": [
    {
      "permalink": "https://www.reddit.com/r/<sub>/comments/<post_id>/<slug>/<comment_id>/",
      "sub": "r/<sub>",
      "published_at": "<ISO+offset>",
      "content_hash": "<sha256>",
      "score_history": [["<ISO>", 0]],
      "reply_count": 0,
      "seen_reply_ids": [],
      "last_checked_at": null
    }
  ]
}
```

Filter:

- `published_at` is in the 6-18 hour window. Too new has not matured; too old has usually sunk.
- `last_checked_at` is null or at least 18 hours ago.
- Exclude comments whose parent post was already marked removed/deleted.

Sort by `published_at` ascending and take the first **3**. Scanning more in one pass looks crawler-like.

If there are no matches, skip the loop and omit this section from the report.

---

## Step 2 - Revisit each target

For each target comment:

```bash
browser-act --session <run_session> navigate <comment_permalink>
browser-act --session <run_session> wait stable
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-revisit-<comment_id>.png
browser-act --session <run_session> get markdown
```

Parse:

| Field | Source |
|-------|--------|
| `current_score` | Current score of the account's comment |
| `reply_count` | Direct replies under the account's comment |
| `new_reply_ids` | Current reply ids minus `seen_reply_ids`, excluding AutoModerator and the account itself |

Write an `upvote_snapshot` event:

```json
{
  "timestamp": "<ISO+offset>",
  "type": "upvote_snapshot",
  "comment_permalink": "<url>",
  "subreddit": "r/<sub>",
  "score": <current_score>,
  "reply_count": <reply_count>,
  "new_replies": <len(new_reply_ids)>,
  "run_session_id": "<run_session>",
  "url_confirmed": "<permalink>",
  "page_title": "<from get title>",
  "evidence_screenshot": "evidence/<ts>-revisit-<comment_id>.png"
}
```

---

## Step 3 - Write back metrics

For this comment's `comment_metrics` entry:

```json
{
  "last_checked_at": "<now>",
  "score_history": [["<previous>", 0], ["<now>", <current_score>]],
  "reply_count": <new reply_count>,
  "seen_reply_ids": ["<union of old and new>"]
}
```

Update `karma_by_sub[<sub>]`:

```json
{
  "karma_by_sub": {
    "r/<sub>": {
      "comments": <int>,
      "upvotes": <int>,
      "latest_checked_at": "<ISO>",
      "latest_delta_at": "<ISO>",
      "consecutive_zero_runs": <int>
    }
  }
}
```

Computation:

- `prev_score = score_history[-2][1]`; use 0 if absent.
- `delta = current_score - prev_score`.
- `karma_by_sub[<sub>].upvotes += delta`.
- `latest_checked_at = now`.
- If `delta > 0`: set `latest_delta_at = now` and reset `consecutive_zero_runs = 0`.
- If `delta <= 0`: increment `consecutive_zero_runs`.

`comments` is incremented when the original comment is first published, not here.

---

## Step 3.5 - Stall detection and sub rotation alert

A sub is stalling when all hold:

1. `karma_by_sub[<sub>].comments >= 3`.
2. `karma_by_sub[<sub>].consecutive_zero_runs >= 3`.

When true:

- Set `sub_profiles.json[<sub>].warmup_stall = true`.
- Set `warmup_stall_since = <now>`.
- Log `sub_stall`.

Pool-level check:

| `stall_ratio` | Action |
|----------------|--------|
| `< 0.5` | Log silently. |
| `>= 0.5` | Surface a pool rotation alert in the daily report and suggest `refresh subreddit pool <username>`. |

Clear `warmup_stall` when a later positive delta resets `consecutive_zero_runs` to 0.

---

## Step 4 - New reply handling

For comments with non-empty `new_reply_ids`, generate 3 A/B/C drafts per reply only when all hold:

- Original comment's `current_score >= 5`.
- New reply is not AutoMod.
- New reply is not a single emoji or single word.
- `progress.json.rate_limit_hit_today != true`.

Prompt inputs follow `stage2-comment.md -> Generate Variants`, with:

- `[post_body]` = original post + the account's comment + conversation context up to the new reply.
- `[top 3 existing comments]` = last 3 messages in this reply chain.

Then run `approval-rules.md -> Part 1 Comment Approval`:

- Write all variants to `pending_approval/<ts>/` with full `meta.json`, `platform: "reddit"`, `skill: "reddit-warmup"`, `batch_id`, `browser_id`, `username`, parent reply id, and exact variant text.
- If any variant contains brand keywords, pre-gate with the Brand Exposure warning.
- Show variants to the user when possible.
- User can reply naturally at any time: `pick A`, `use the second one`, `skip`, `make it shorter`.
- A clear revision request immediately updates the same pending batch and redisplays the Approval Batch Request for unresolved items; do not only acknowledge the edit request.
- A clear pick immediately publishes via `comment-publishing.md -> Reply flow` in a fresh verified `<run_session>`.
- No pick leaves the batch in `pending_approval/` until picked or cleaned by the 7-day stale sweep.

Replies count as reactive comments. The `last_comment_time` gap only needs to be at least 2 minutes; real users can reply in bursts.

Log reply drafts/publishes with `"source": "followup_loop"` and `"parent_comment_id": "<id>"`.

---

## Step 5 - Downstream use of `karma_by_sub`

When Stage 2/3 chooses a sub after Rule-Reading Gate checks pass, use weighted random:

```text
base weight = 1
Every 10 cumulative net upvotes -> weight += 1, cap at 5
Negative karma -> keep weight 1
No karma_by_sub entry -> keep weight 1
warmup_stall == true -> weight = 0
```

Effect:

- Strong historical subs get higher probability.
- New and neutral subs still have a chance.
- Stalling subs are excluded from auto-pick until recovery.

---

## Step 6 - Session throttling

- Wait 60-120 seconds between revisits.
- The whole Feedback Loop has a hard 10-minute cap.
- If the cap is hit, stop and defer unprocessed targets to the next daily run.
- Any rate-limit signal during the loop triggers the same full-stop rule as End-of-Day Recon.

---

## Compared to Watchtower

| Dimension | Feedback Loop | Watchtower |
|-----------|---------------|------------|
| Target | Comments the account posted | The post the account most recently submitted |
| Trigger | Daily tail only | 30-minute window after publishing + manual `camp <username>` |
| Age window | 6-18h | Immediate active window |
| Cap per run | 3 comments | 1 post |
| New-reply handling | A/B/C -> approval -> publish | Same approval path |

No conflict: Watchtower handles the immediate post window; Feedback Loop handles the long tail of older comments.

---

## Daily report output

After the Feedback Loop finishes, add only the lines that apply:

```text
Comment Feedback: revisited 3 (r/<a>: +5, r/<b>: 0, r/<c>: -1)
Top sub ROI (past 7d): r/<a> (+18 karma) -r/<b> (+7) -r/<c> (+3)
Stalling subs (>=50% of pool): r/<x>, r/<y> - run "refresh subreddit pool <username>" to refresh
```

Line 2 comes from the 7-day delta of `karma_by_sub[*].upvotes`, filtered by `latest_delta_at`. For the first 10 days after onboarding, omit line 2 because there is not enough data.

