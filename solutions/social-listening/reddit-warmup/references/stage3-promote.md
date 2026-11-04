# Stage 3 -Promote (Day 30+)

SKILL.md's Stage 3 section is intentionally short. All operational detail lives here.

Stage 3 **auto-entry** is gated by two hard requirements: `account_age_days >=30` AND `comment_karma >=20` -both must hold for the entry decision card to auto-fire. Manual command `enter brand phase <username>` is a separate bypass path that shows a risk warning when gates aren't met and lets the user override with explicit confirmation. See Entry Decision below.

Once in promote mode, commenting continues (same flow as Stage 2 -see `stage2-comment.md`, the A/B/C/D generator, duplicate check, approval gate all apply unchanged). Posts gain two new paths: A (normal) and B (promotional). Both require explicit human approval -see `approval-rules.md` ->Part 2 Brand Approval.

---

## Entry Decision Card

Two flags in `progress.json`:
- `stage3_entry_offered_day`: day the card last fired, or `null`
- `stage3_user_choice`: `null | "stay" | "promote"`

### When to fire

Fire when ALL hold:
- `account_age_days >=30`
- `comment_karma >=20`
- `stage3_user_choice == null`
- `stage3_entry_offered_day == null` OR `current_day - stage3_entry_offered_day >=7` (re-ask weekly if ignored)

Set `stage3_entry_offered_day = current_day` on fire. Leave `stage3_user_choice` alone.

**The two auto-fire gates only control whether the card auto-pops**; they don't block manual override -manual path below.

### Handling the manual command `enter brand phase <username>`

1. **Read the current `account_age_days` / `comment_karma`** (Pre-flight Step 8 just synced them; read directly from progress.json).
2. **Both gates met** ->equivalent to picking B on the card: `stage3_user_choice = "promote"`, `progress.json.stage = "promote"`, log `stage3_entry: {"source": "manual", "forced": false}`.
3. **Either gate not met** ->**show the risk notification card**:
   ```
   Warning: `<username>` does not meet Stage 3 auto-entry conditions
      Account age: <N>d (gate 30d, short by <gap_age>d)
      comment_karma: <K> (gate 20, short by <gap_karma>)

   Stage 3 allows soft brand mentions / Path B promotional posts. When karma / age
   reserves are insufficient, promo content is easily judged as planted by Reddit
   and may trigger shadow-filter.

   Type "override" or "continue"
     ->proceed to Stage 3 (audit record kept)
   Type anything else ->cancel, stay in Stage 2 and keep building karma
   ```
4. **User explicitly overrides** ->`stage3_user_choice = "promote"`, `progress.json.stage = "promote"`, log `stage3_entry: {"source": "manual", "forced": true, "age_at_entry": <N>, "karma_at_entry": <K>, "gap_age": <gap_age>, "gap_karma": <gap_karma>}`.
5. **User does not confirm** ->leave all fields untouched; Stage 2 continues.

### Card text

```
Stage 3 entry: <username> meets brand-period entry conditions: account <N> days -karma <K>

A. Continue regular warm-up (safe karma accumulation)
B. Enter soft-promo period Warning: Allows soft brand mentions

Pick A / B
```

### On user response

- **A** ->`stage3_user_choice = "stay"`. Per SKILL.md ->Stage Determination's two-step rule, the effective_stage will be mapped by Step B to `"comment"`, so all flows behave like Stage 2 (even though `current_day >= 30`). `progress.json.stage` field is written as `"comment"` on the next run's wrap-up. The card will not re-fire. User changes their mind ->say "enter brand phase `<username>`" ->go through the "Handling the manual command" branch above (gate met ->go to promote; not met ->risk notification override flow).
- **B** ->`stage3_user_choice = "promote"`, `progress.json.stage = "promote"`, effective_stage = `"promote"`, full Stage 3 behavior unlocked. log `stage3_entry: {"source": "card", "forced": false, "age_at_entry": <N>, "karma_at_entry": <K>, "gap_age": 0, "gap_karma": 0}`.

### On silence

`stage3_user_choice` stays `null`. Card quietly re-fires 7 days later. **No auto-default to either choice** -the promote decision feels irreversible enough that silent auto-opt-in is the wrong behavior.

---

## Brand Exposure Target -9:1 (advisory, user decides)

Target: for every 10 units of published content, at most 1 mentions the brand. This is Reddit's community-accepted self-promo guideline and protects young accounts from site-wide shadowban. **Advisory, not a hard ceiling** -mature accounts with established karma history can exceed it with lower risk; user decides case-by-case.

### Check (runs every time a brand-bearing draft is about to be published)

A draft is "brand-bearing" if ANY of:
- Variant letter is D (deliberate intent -always counts, regardless of whether rendered text mentions the brand)
- Any token from `config.yaml ->keywords.brand` appears in the rendered text (case-insensitive substring)
- For posts: topic is directly related to the brand (caller's judgment), or the draft's body contains a brand keyword

Compute:
1. Load the rolling last 10 entries where `type in {"comment", "post"}` **AND `imported != true`** (only entries produced **after** skill takeover count -imported backfill describes the account before takeover and doesn't participate in the current 9:1 ratio judgment).
2. Count entries with `contains_brand: true` (flag set at write time -see `activity-log-schema.md`).
3. Also compute last-7-days count of promotional posts and brand-mention comments (**also excluding `imported: true`**).
4. Classify risk:

| Account state | Risk level |
|---------------|-----------|
| `account_age_days < 30` OR `comment_karma < 50` | **elevated** |
| `account_age_days >=30` AND `comment_karma >=50 AND <200` | **moderate** |
| `account_age_days >=90` AND `comment_karma >=200` | **low** |

### Warning UI

```
Warning: Brand exposure ratio check -<username>
----------------------------------------
  Last 10 entries: <N> brand (target <=1)
  Last 7 days: <M1> promo posts / <M2> brand comments
  Account age: <age>d -comment_karma: <K>
  9:1 soft-rule risk: <low | moderate | elevated>

  Risk level basis:
   -age < 30d or karma < 50 ->elevated
   -age >=30d and karma 50-199 ->moderate
   -age >=90d and karma >=200 ->low

Publish options:
  A. Rewrite as a non-brand version first (recommended for elevated)
  B. Publish as-is (accept risk)
  C. Skip this one
```

Log the decision as a `brand_ratio_decision` entry with `ratio_before`, `risk_level`, `user_choice`.

---

## Stage 3 Daily Flow

Apply **Weekly Activity Pattern** (`stages.md`): Mon/Wed/Fri/Sat normal, Tue/Thu light (~50% fewer comments, no new posts), Sun rest.

Baseline post mix (informational, not hard):
- Help-seeking ~40%
- Sharing ~40%
- Promotional >=0%

Mature accounts may override. Weekly targets: `posts_this_week >=2` (hard cap) and `promo_posts_this_week >=1` (**advisory -exceeding triggers the Weekly Cap Warning prompt**, see `approval-rules.md ->Weekly Posting Cap`; user can ack and proceed, or save for next Monday, or cancel).

---

## Path A -Normal Post (Help-seeking / Sharing)

### Preconditions (verify before generating draft)

**Hard preconditions (ALL must hold, otherwise skip and pick another sub or defer Path A this week):**

- Target sub is already subscribed (check `progress.json.subscribed_subs` contains the target sub)
- Target sub has post history (check `activity_log.jsonl` for ANY successful `type: "post"` or `type: "comment"` entries in that sub; must have >=1 prior success to prove it's safe)

If either fails, log with reason (`skip("sub_not_subscribed")` or `skip("no_sub_history")`) and pick another target sub or defer Path A.

### Publishing Path A

1. Generate draft: title + 50-80 word body, first-person, grounded in persona.
2. Write draft to `~/.reddit-warmup/<username>/pending_approval/<ts>/post_A.txt` + `meta.json` (`kind: "post"` for Path A normal posts; `kind: "brand"` for Path B promotional posts -see Path B below). Include `platform: "reddit"`, `skill: "reddit-warmup"`, `batch_id`, `browser_id`, `username`, target subreddit, exact title/body, path, recommended/default variant, and queue fields (`queue_status`, `queue_position`, `queue_total`, `approval_item_index`, `display_group_id`, `displayed_at`, `retired_at`). Manual-path batches stay in `pending_approval/` until picked or cleaned by the 7-day stale sweep; see `approval-rules.md` ->Approval Queue and Rules C3/C4/B4.
3. Enqueue the draft. Show it to the user as one item in the account's Approval Batch Request:
   ```
   Approval Batch: reddit-warmup / <username>
   platform: reddit  browser: <browser_id>  pending: <N>

   [<approval_item_index>] kind: <post>  batch: <batch_id>
   Post draft -r/<sub>
   Title: <title>
   Body: <body>
   ---
   You can reply naturally: <item_number> confirm / <item_number> publish / <item_number> modify / <item_number> revise it / <item_number> cancel
   Canonical command: approve <username> <batch_id> confirm
   Revise command: revise <username> <batch_id> <instruction>
   Skip command: skip <username> <batch_id>
   On clear confirmation, publish immediately; do not only record the choice.
   ```
4. On item-scoped `confirm` ->publish via Post Publishing Steps below. On item-scoped `modify` / `revise it` / a concrete edit instruction ->run `approval-rules.md ->Revision Execution Flow`, update the same pending batch, and immediately display the revised Approval Batch Request for unresolved items.

Stage 2 Wednesday practice post reuses Path A unchanged (text-only, no image, no brand in body).

---

## Path B -Promotional Post

### Preconditions

**Hard preconditions (ALL must hold, otherwise defer):**

- Topic directly related to `config.yaml ->keywords.brand`
- Target sub's `sub_profiles.json[<sub>].restrictions.forbids_self_promo != true` (sub rule, non-negotiable)
- `posts_this_week < 2` (total weekly post cap -still hard)
- **Target sub is already subscribed** (check `progress.json.subscribed_subs` contains the target sub)
- **Target sub has post history** (check `activity_log.jsonl` for ANY successful `type: "post"` or `type: "comment"` entries in that sub; must have >=1 prior success to prove it's safe) -if no history, pick another sub or defer Path B this week

> Account age / karma gates are enforced by the Stage 3 entry gate (including the manual override path); no double check here.
> **Note on new gate-checking flow:** Before writing any Path B draft, verify both conditions above by scanning `activity_log.jsonl` and `progress.json`; log with reason if skipped (`skip("sub_not_subscribed")` or `skip("no_sub_history")`).

**Advisory precondition (warning + user choice, not a hard stop):**

- `promo_posts_this_week < 1` -if already at 1, generate the draft anyway but trigger the Weekly Cap Warning prompt described in `approval-rules.md ->Weekly Posting Cap`. User can:
  - Override and proceed to normal Path B approval
  - Save for next Monday (batch written to `drafts/` with `replay_after`)
  - Cancel (log `skip("weekly_cap_declined")`)

### Flow: pick sub ->verify sub ->generate ->approve ->publish

Verifying the sub **before** writing the draft means we never write copy for a sub that will reject us.

#### Step 1 -Pick target sub (karma-guided, non-blocking)

Pick from `config.yaml ->subreddits.warmup + subreddits.target.primary + subreddits.target.secondary`, ranked by `sub_profiles.json`:

| Own comment_karma | Prefer |
|-------------------|--------|
| 0-9 | Only `warmup` subs with `automod_filter_rate: low` AND `median_recent_poster_karma >=20`. Defer promo this week if none qualify. |
| 10-49 | All warmup + `target.primary` where `median_recent_poster_karma >=own x 5` AND `automod_filter_rate in {low, medium}` |
| 50-99 | All configured subs except `karma_gate > 50` or `automod_filter_rate: high` |
| >=100 | Any configured sub, subject to its individual profile |

Rule derives entirely from user config + per-sub cache. Skill never names subs.

#### Step 2 -Specialized-sub check (before writing anything)

"Specialized" is defined by the sub's profile, not name. Treat as specialized if ANY of:
- `karma_gate >=50`
- `automod_filter_rate == "high"`
- `median_recent_poster_karma >=100`

If none hold ->skip to Step 3 (basic risk filter was sufficient).

For specialized subs, compute verdict:

| Own comment_karma vs `median_recent_poster_karma` | Verdict |
|----------|---------|
| own >=50% of median | post |
| own < 30% of median | Skip this sub this week; pick another target or fall back to Path A |
| in between | Warning: comment 2-3 times in this sub first, post next week |

Write back to the profile entry in `sub_profiles.json` using the host agent's local file capability:
```json
"r/<sub>": {
  // ...existing fields...
  "last_verdict": "post | blocked | warm-up-first",
  "verdict_at": "<YYYY-MM-DD>",
  "retry_when_comment_karma": <int>
}
```

TTL: 7 days. If `last_verdict == "blocked"` and `own comment_karma < retry_when_comment_karma`, skip this sub without re-scraping.

#### Step 3 -Scan top posts + generate draft

Only proceed if Step 2 gave OK

**First take today's rotated brand angle** (see SKILL.md ->Keyword Rotation). Read from `progress.json.keyword_rotation.brand_index` and compute `today_brand_angle = keywords.brand[brand_index % len(keywords.brand)]`. This is the brand dimension to emphasize in this post.

Entries in the `keywords.brand` list should be **different angles / selling points**, not multiple names for the same product. For example:
- NOOne account: `["MyProduct", "my-product", "my product"]` (just spelling variants; rotation is meaningless)
- One account: `["MyProduct for use case X", "MyProduct vs Y advantages", "MyProduct's Z feature"]` (genuinely different entry points)

If the user gave only 1 term ->same angle every time (rotation has no effect but doesn't error).

```bash
browser-act --session <run_session> navigate "https://www.reddit.com/r/<sub>/top/?t=month"
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Extract top 20 text posts from the markdown. Based on the angle implied by `today_brand_angle`, find a **recurring pain point mentioned in at least 3 of them** that credibly matches both `today_brand_angle` AND `persona's brand_story`. If no pain point recurs ->fall back to Path A this week (**don't force it** -forcing a brand angle produces an ad-like post, which defeats the whole Reddit warm-up strategy).

Prompt:

```
You are a real Redditor writing a first-person post.

Identity:            [identity from persona_file]
Tone and voice:      [tone]
Phrases to avoid:    [never_say]

Today's brand angle (not to be written literally, just shapes the story
 you tell):
  [today_brand_angle]

The community's recurring pain point: [core_pain_point]
Your relevant experience: [brand_story]

Write a 50-80 word text post:
- First-person throughout ("I" / "my")
- Title format, length, emotional register should follow Tone above.
  Reddit-native self-deprecating formats (e.g. "TIFU: ...", "I tried to ...
  and", "So I thought ... boy was I wrong") are acceptable -pick whichever
  fits Tone, don't force any.
- Body: specific, concrete, sounds lived -not a summary.
- End with an open question that invites replies.
- DO NOT name any brand. Brand should be implied only through the
  experience described in brand_story. Direct brand mentions belong in
  follow-up comments, not the post body.
- The brand angle above is a framing hint -let it color what ASPECT of your
  experience you share; don't paste it verbatim into the post.
- No AI-smell vocabulary -see comment-rules.md ->Forbidden Patterns.
  Rewrite or skip any draft using those phrases.
```

All style signals (tone, register, title format, language/locale) come from `persona_file`. The skill imposes only structural constraints (first person, length, open question, no brand in body).

**After draft generation** (regardless of whether the user later confirms or cancels), increment `brand_index += 1` -draft generation itself consumes a rotation value, and next Path B uses the following angle. Write back to `progress.json` during the final daily wrap-up.

#### Step 3.5 (optional) -Image attachment

Text posts are default. If BOTH hold, optionally ask user:
- `config.yaml ->post_options.allow_images: true`
- Target sub's profile has `prefers_image: true`, OR the post is show-and-tell / self-deprecating-mishap style

Full flow (sourcing, Google Lens reverse-check for popularity, Reddit image submit URL) in `image-posting.md`. Text-only unless user opts in.

#### Step 4 -Approval

Enqueue the Path B batch using the Approval Queue fields from `approval-rules.md`. Show this approval request as one item in the account's Approval Batch Request; comments/replies appear before posts in the batch order.

```
Approval Batch: reddit-warmup / <username>
platform: reddit  browser: <browser_id>  pending: <N>

[<approval_item_index>] kind: <brand>  batch: <batch_id>
Post draft -r/<target_sub>
Title: <title>
Body: <body>
<if image attached>: Image: <image_path> (source: user / google_images)
---
Publish? (<item_number> confirm / <item_number> modify / <item_number> revise it / <item_number> cancel)
Canonical command: approve <username> <batch_id> confirm
Revise command: revise <username> <batch_id> <instruction>
Skip command: skip <username> <batch_id>
Warning: No publish without confirmation.
```

Clear item-scoped natural-language confirmation (`confirm`, `publish`, `go ahead`, `approved`) must proceed immediately to Post Publishing Steps. `modify` / `revise it` / a concrete edit instruction must run `approval-rules.md ->Revision Execution Flow`, update the same pending batch, and redisplay the Approval Batch Request for unresolved items. `cancel` / `skip` skips. Do not only write a choice marker.

**This approval is unskippable.** See `approval-rules.md` ->Part 2 Brand Approval for the hard rule: Path B posts never auto-publish, in any mode.

---

## Post Publishing Steps

After user confirms (both Path A and Path B):

->**Follow `references/image-posting.md` -Common flow ->TEXT post branch ->Submit ->Verify (2-phase).**

All browser-act commands (navigate, dwell, state, title fill, body fill, submit button click, network verdict, 2-phase verify via submitted list + permalink filter check) live in that file. **Do not use the `act` command -it is not in the approved CLI command set and produces unreliable fills on Reddit's Lexical composer.**

Key points from image-posting.md to keep in mind:
- Use `?type=text` URL param for text posts.
- Title is a native `<textarea name=title>` (fill via `input <idx>`); body is a Lexical `<div role=textbox name=body>` (same `input` command).
- Submit button is `#inner-post-submit-button` inside Reddit's nested controls -`browser-act state` enumerates it.
- **2-phase verify**: Phase 1 checks `/user/<username>/submitted/` for the post; Phase 2 navigates the permalink and checks for `"removed by Reddit's filters"` / `"removed by moderators"` banners.
- `removed_by_filter` is the expected outcome for fresh accounts with no prior sub history -this is why the "prior sub activity" hard precondition exists.

Visibility outcomes:
- `visible` -post accessible and not filtered
- `removed_by_filter` -Reddit-level or sub-level AutoMod filter (still update `last_publish_at`)
- `pending` -404 or empty body (rare; treat same as `removed_by_filter`)

### Log + update

Activity log:
```json
{
  "timestamp": "<ISO+offset>",
  "type": "post",
  "subreddit": "r/<sub>",
  "post_url": "<url>",
  "post_title": "<title>",
  "content": "<body>",
  "post_kind": "help_seeking | sharing | promotional",
  "post_format": "text | image",
  "path": "A | B",
  "karma_before": <int>,
  "contains_brand": <bool>,
  "content_hash": "<sha256 of title+body>",
  "visibility": "visible | removed_by_filter | pending",
  "run_session_id": "<run_session>",
  "url_confirmed": "<url>",
  "page_title": "<title>",
  "evidence_screenshot": "evidence/<ts>-after-post.png"
}
```

Patch `progress.json`:
- `last_post_url = <url>`
- `last_post_time = now`
- `posts_this_week += 1`
- `promo_posts_this_week += 1` if Path B
- `post_watchtower_deadline = now + 30 min`
- `seen_reply_ids = []`

---

## Watchtower (every successful post -Path A, Path B, Stage 2 practice)

**First 30 minutes after publishing** determine whether the post makes Rising. Every new comment in that window should get a timely, persona-consistent reply -that's what pushes the post onto more feeds. After 30 min the pattern plateaus; 1h and 2h checks catch late replies.

### After post publishes

Set deadline and notify user:

```
Post published: <post_url>

Camping window open (until <deadline account-local time>, ~30 min)
- Poll every 5 min (recommended): /loop 5m camp <username>
- Manual single check: camp <username>
- Auto-stops after window closes; manually check once at 1h and 2h afterward.
```

### Watchtower Entry Point

Triggered by user saying "camp `<username>`" or `/loop 5m` calling the same phrase.

Each invocation:

1. Read `progress.json` -`last_post_url`, `seen_reply_ids`, `post_watchtower_deadline`, `last_post_time`.
2. Window check:
   - `now > deadline` AND `now - last_post_time > 3h` ->fully closed. Report "no active watch" and exit.
   - `now > deadline` AND `now - last_post_time >=3h` ->past the active window but in long-tail range. Do one pass, no auto-continue.
   - Otherwise inside 30-min window ->do a pass, tell user next `/loop` tick time.
3. Diff replies:
   ```bash
   browser-act --session <run_session> navigate <last_post_url>
   browser-act --session <run_session> wait stable
   browser-act --session <run_session> get markdown
   ```
   Parse reply IDs. Compute `new_replies = all_reply_ids - seen_reply_ids`.
4. For each new reply -> generate 3 drafts (A/B/C using same template as Stage 2, `[post_body]` -> full thread context, `[top 3 comments]` -> last 3 in this reply chain). Write each reply batch to `pending_approval/` with queue fields including `queue_status`, `queue_position`, `queue_total`, `approval_item_index`, `display_group_id`, `displayed_at`, and `retired_at`. Show all same-account reply/comment/post items together in one Approval Batch Request. On clear natural-language picks, publish each selected item sequentially via `comment-publishing.md` -> Reply flow (same browser-act click/input/verify flow with `parent_id` set to the `t1_xxx` of the reply we are answering). On clear revision requests, update the targeted pending items and redisplay one anchored Approval Batch Request for unresolved items. Do not only record the pick or revision.
5. Update `seen_reply_ids` with everything seen (including skipped -don't re-prompt on same reply).
6. Stop conditions (any one ends the watchtower):
   - 2 consecutive invocations with 0 new replies inside the 30-min window ->clear `post_watchtower_deadline`
   - `now > last_post_time + 3h` ->clear deadline
   - User says "stop camping `<username>`" ->clear deadline

This lets the first 30 min produce near-real-time replies via `/loop 5m` while the long tail stays manual. No scheduler-side logic required beyond the 5-min trigger.

---

## Weekly Shadowban Check (Mondays) -manual / user-driven

In-session logged-in profile checks cannot distinguish "visible to me" from "visible to everyone" -Reddit deliberately shows shadow-banned accounts their own content in their own logged-in session. The authoritative shadow check is **manual, user-driven, on [r/ShadowBan](https://www.reddit.com/r/ShadowBan/)**:

1. User opens r/ShadowBan in their everyday browser, posts the subreddit's standard template
2. AutoMod replies within ~1 minute with the verdict (`public` / `shadow` / `suspended`)
3. User reports the verdict back in chat

**When to trigger this check** (agent surfaces the suggestion in the daily report):

- 2+ `removed_by_filter` events on the same account within 7 days
- Repeated `reddit_403` on submit in a short window
- Karma hasn't moved in 14 days despite daily comment activity
- User directly reports "nobody seems to see my comments"

**After the verdict:**
- `public` ->no action needed; continue normal flow. Append a `shadowban_check` event to `activity_log.jsonl` with `source: "r_shadowban_automod"`, `result: "public"`, `triggers_that_prompted_check: [<which signals fired>]`, `user_reported_at: <ISO now>`. Full schema in `activity-log-schema.md ->shadowban_check`.
- `shadow` or `suspended` ->write the same event with `result: "shadow"` or `"suspended"`; then set `progress.json.paused = true`, notify user to create a replacement account. Do not resume this account without a fresh AutoMod `public` verdict.

**Why not open `/user/<username>/comments/` anonymously?** Shadow-banned profiles still render *some* content to logged-out visitors in certain views, and Reddit's cache layer often bypasses the logged-out-vs-logged-in delta. The r/ShadowBan AutoMod check is the only authoritative signal.

