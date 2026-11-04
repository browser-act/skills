# Stage 2 -Commenting (Days 15-29)

SKILL.md's Stage 2 section is intentionally short. All operational detail lives here.

Daily commenting volumes + irregular-rhythm rules (Day 17/19 skip) are in `stages.md`. The Wednesday practice post gate + mechanism are below. This file mainly covers the **mechanics** of commenting: finding posts / generating variants / de-dup / approval / publishing.

---

## Wednesday Practice Post (once a week, Stage 2 only)

Stage 2 is comment-heavy, but **every Wednesday** the account additionally submits **1** non-brand practice post. Purpose: let the account accumulate post_karma as well, establish a "this account not only comments but also posts" pattern, paving the way for Stage 3's first promotional post. This practice post is a karma-building social post, not a professional proof-of-expertise post.

### Strict trigger conditions (all 5 must hold)

```
1. current_day >= 15            ->Stage 2 officially started
2. current_day <= 29            ->upper bound; Day 30+ is Stage 3, handled by Path A
3. Today is Wednesday (by account timezone, see scheduling.md timezone rule)
4. progress.json.posts_this_week < 1   ->no post yet this week
5. Persona readiness gate == "ok"      ->no persona = no practice post
```

Any one fails ->no practice post today, continue normal comment flow.

### What to post

Use a high-activity warmup / broad-interest sub and post something easy to react to. Favor style, pop-culture, food, pets, hobbies, light trends, and everyday-life communities over any professional niche. The best shapes are:
- funny or lightly self-deprecating everyday observation
- relatable small frustration / "does anyone else do this?"
- lifestyle, fashion/style, pop-culture, food, pets, hobby, or mild trend-adjacent prompt
- short visual/observation style when the sub supports it

Avoid professional/domain posts during the comment stage, regardless of persona. Do not use Stage 2 practice posts to discuss software tooling, marketing strategy, SEO, ads, growth tactics, startup lessons, sales funnels, finance/legal/medical advice, AI agents, developer workflows, or the brand category. Those topics belong to target subs later.

Reuse **Stage 3 ->Path A** mechanics (approval + post publishing), with these hard constraints:
- **Must NEVER contain any `keywords.brand` terms** (Stage 2's red line -brand exposure must wait for Day 30+)
- **Text-only post, does NOT go through the image-posting flow** (even if `post_options.allow_images: true`)
- **Must target `subreddits.warmup` or another broad-interest high-activity sub found by recon**, not `target.primary` professional/domain subs.
- **Must be resonance-first**: title/body should invite low-effort replies from many users, not require domain expertise.

Approval flow is identical to Path A: `confirm / modify / revise it / cancel`, though it follows `approval-rules.md` ->Part 1 Comment Approval (which is also in-flight approval). Clear edit requests must run Revision Execution Flow and redisplay the anchored draft.

### What to do if Wednesday's practice post fails

- Pre-flight skipped due to paused / rate_limit_hit / migration ->skip this week, **do NOT retry** -wait for next Wednesday.
- User picked "cancel" ->skip this week, no retry.
- User didn't trigger the daily on Wednesday ->skip this week.

**Do NOT** retry on Thursday/Friday. Fixing the practice post to Wednesday itself is what gives the account a regular behavior pattern (one post per week); retrying disrupts the rhythm.

### Relationship with Day 17 / 19 skip-day rules

- Day 17 / 19 are comment-skip days (browse + upvote only, no comments)
- If Day 17 or 19 happens to be a Wednesday, **the practice post still goes out** (comment-skip >=post-skip). Skipping comments on those two days is about breaking comment regularity; posting is independent.
- `comments_done: 0` / `replies_done: 0` on Day 17 or Day 19 is expected. Do not mark the run failed, anomalous, or timed out just because no comment/reply was published on these planned irregular-rhythm days. Log or report the skip as planned rhythm, not as a publishing failure.

---

## Persona Readiness Gate (run before commenting on Day 15+)

Four persona states + one profile-customization soft-block. Compute at the start of the run:

1. **`ok`** -either `persona_file` is set and the file exists and contains no `<...>` placeholder strings, OR `keywords.content` has >=2 non-empty entries.
2. **`empty`** -no persona file configured AND `keywords.content` is empty or < 2 entries.
3. **`placeholders`** -persona file exists but raw template tokens (`<role / identity>`, `<concrete past experience 1>`, etc.) survive unreplaced.
4. **`missing_file`** -`persona_file` is set but the path doesn't resolve.

**Soft-block layered on top** (even when persona state == `ok`):

- If `progress.json.profile_customized == false` AND `current_day >= 15`, **still allow commenting** (don't block comments outright just for a missing avatar/bio), but **surface the reminder every run** in today's preview until the user runs Phase 1 Step 5.7. Empty-bio + default-avatar is the #1 new-account-farm signal, and the user is now actively commenting -every day this stays uncustomized is a day Reddit's ML gets a cleaner "bot" signature from the account's activity-to-profile mismatch.

Response per state:

| State | Action |
|-------|--------|
| `ok` | Proceed with comment path |
| `empty` | Skip today's comment path (browse + upvote still runs). Remind user every 3 days via `last_persona_reminder_day` in progress.json. Tell them: "Comments generated without a persona read very AI-smelly. Please fill `config.yaml ->keywords.content` with at least 2 entries, or point to a persona file. Template at `assets/persona.json.template`" |
| `placeholders` | Auto-draft from config + proxy geo + subscribed subs + recent activity, show side-by-side with the placeholder file, ask user "accept / I'll edit myself / only change some fields" (see below) |
| `missing_file` | Tell user the path doesn't resolve; ask them to fix or clear `persona_file`. Skip comment path |

### Placeholder auto-draft

Agent inputs when drafting:
- `config.yaml` ->`keywords.find` / `content` / `brand` -topical hints
- `config.yaml` ->`subreddits.warmup` / `target` -implied interests
- `sub_profiles.json` -what the account has already touched
- Proxy geo from `https://ipinfo.io/json` -plausible location/accent for the persona
- `activity_log.jsonl` -any past activity

Present the current placeholder file + the proposed filled version side-by-side:

```
Persona file for <username> still has template placeholders:

  identity:       <role / identity>         ->unfilled
  tone:           <how the account sounds>  ->unfilled
  interests:      ["<topic 1>", ...]        ->unfilled
  backstory_keywords: ["<concrete past experience 1>", ...]
  brand_story:    <1-3 sentence first-person anecdote ...>

I drafted a suggested persona based on your config.yaml + proxy geo + subscribed subs:

  identity:       <AI-drafted value>
  tone:           <AI-drafted value>
  interests:      [...]
  backstory_keywords: [...]
  brand_story:    <AI-drafted value>

Accept? (accept / I'll edit myself / only change some fields)
```

- **Accept** ->agent writes the filled JSON to `persona_file` (preserving any non-placeholder field the user had filled). Comment path resumes this run.
- **Edit myself** ->skip today's comment path; reminder cadence resumes; re-detect next run.
- **Change some fields** ->walk field-by-field, accepting draft or user-supplied value per field.

Agent never silently auto-writes. Every replacement needs explicit ack.

---

## Subreddit Risk Profiling

Before commenting in any sub, ensure `sub_profiles.json[<sub>]` is present and `recon_at` within 14 days. If missing or stale ->recon first.

### Hard rule: read rules before every interaction

Every sub has its own rules (flair requirements, self-promo bans, weekday-only topics, etc.). AutoMod silently removes rule-violating content and accumulates strikes. Before any comment/post:

1. Sub must have a valid profile entry (`recon_at` within 14 days).
2. Entry's `rules_summary` + `restrictions` must be non-empty. Empty means recon didn't capture rules -re-run, don't guess.
3. Evaluate the rules against the intended action. If the sub forbids the action type (e.g., no self-posts on weekdays and today is Tuesday, or no URL submissions and the post has a link), **abort this interaction** and pick another sub or skip.

Applies equally to comments, practice posts, promotional posts, and camping replies. No exceptions.

### Recon routine (via browser-act)

```bash
# 1. Rules page
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/about/rules
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
# Parse into: karma_gate, age_gate_days, forbids_self_promo, requires_post_flair, flair_options,
#             forbids_urls_in_posts, forbids_image_posts, forbids_text_posts,
#             weekday_only_topics, min/max post length, rules_summary

# 2. Wiki (often richer)
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/wiki/index
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown

# 3. /new -observe AutoMod filter rate
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/new/
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
# Sample the first 20 posts' age + comment count.
# >=40% of /new posts have 0 comments and are > 1h old  ->automod_filter_rate: high
# 20-40% ->medium
# < 20% ->low

# 4. Sample successful posters' karma + post-format distribution
# Pull 5 recent non-stickied posts with >=20 upvotes.
# For each, navigate to /user/<author>/, get markdown, read comment_karma.
# Median ->median_recent_poster_karma
# Also count how many of the 5 are image/gallery/video type (checked on the post cards' post-type attribute).
# >=3 of 5 are visual ->prefers_image: true; otherwise false.

# 5. Moderator list -Bot Bouncer reconnaissance
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/about/moderators
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
# Parse the moderator usernames out of the markdown. Record every bot-looking
# account (suffix "Bot", known bot-moderator names) in `moderator_bots`.
# Flag `has_strict_bot_bouncer: true` if any specialized anti-circumvention bot
# is in the list, including but not limited to:
#   BotBouncer, Bot-Bouncer, BotDefender, AntiBot, safestbot, BotSentinel,
#   RepostSleuth, RepostSleuthBot (treat any "*Bouncer" / "*Defender" / "AntiBot*"
#   username as a match).
# AutoModerator appears in nearly every sub and is NOT a specialized anti-bot
# moderator -record it in `moderator_bots` but do NOT set `has_strict_bot_bouncer`
# on AutoModerator alone.
# Otherwise ->has_strict_bot_bouncer: false
```

Write profile to `sub_profiles.json` using the host agent's local file capability. Include `recon_at = today`. Write `prefers_image` based on the sampling above -Stage 3 image-posting flow reads this flag.

### Pre-action rule check (every time, O(1) lookup)

Load `sub_profiles.json[sub]` before each action. Verify:

| Condition | If violated |
|-----------|-------------|
| `recon_at` within 14 days | Re-run recon first |
| Promotional action AND `forbids_self_promo == true` | Pick another sub; log `skip("sub_forbids_self_promo")` |
| Image post AND `forbids_image_posts == true` | Fall back to text post |
| Text post AND `forbids_text_posts == true` | Pick another sub |
| `requires_post_flair == true` AND no flair chosen | Ask user to pick from `flair_options` before approval |
| Day-of-week matches a `weekday_only_topics` restriction | Wait or pick another sub |
| Draft length outside `minimum_post_length_words`/`maximum_post_length_words` | Regenerate with length constraint |

All violations logged as `skip` entries with specific reason codes.

### Filter before searching for posts

Build the candidate pool in priority order:

```
if day <= 21:
    pool = warmup_subs
else:
    pool = warmup_subs + target.primary_subs
    # fallback: if primary pool ends up empty after filtering below,
    # expand to include target.secondary_subs
```

**Karma-building priority:** during Days 15-29, warmup subs are the default comment pool because they are broad, low-context, and easier for new accounts to earn karma in. Do not prioritize professional/domain target subs merely because the persona is a marketer, developer, founder, consultant, operator, finance person, legal/medical professional, or other specialist. Target subs may enter after Day 22 only when recon gates pass, but they are secondary to the account's immediate karma-building goal.

**Step 0 -Subscription pre-check (runs first, before any other gate):**

Verify `sub in progress.json.subscribed_subs`. If NOT subscribed:

- Remove from today's candidates immediately.
- Log `skip("not_subscribed", subreddit: "r/<sub>")`.
- Enqueue for tonight's End-of-Day Recon subscribe opportunity.
- Do NOT comment in the sub today under any circumstances.

**Step 1 -Profile + drop checks (only for subs that passed Step 0):**

- No cached profile, or `recon_at > 14d ago` ->run recon now (~60s per sub)
- Drop if ANY of:
  - `karma_gate > own comment_karma`
  - `age_gate_days > own account_age_days`

Log each drop with reason. `automod_filter_rate` is recorded in `sub_profiles.json` for reference but does NOT block candidates -Reddit's own AutoMod will silently filter if needed.

**Step 2 -Primary ->Secondary fallback:**

```
if all target.primary_subs filtered out AND day > 21:
    expand pool with target.secondary_subs (subscribed only)
    re-run Step 0 + Step 1 on secondary subs
    log "primary_pool_exhausted, falling_back_to_secondary"
```

If the expanded pool also filters out entirely ->skip commenting today, keep upvoting. Log `skip("all_target_subs_blocked")`.

---

## Finding Posts (comment-hijack first)

Stop at the first good fit.

Prefer posts with high social resonance over professional depth:
- relatable questions, funny/rant-style observations, everyday tradeoffs, fashion/lifestyle/food/pet/hobby prompts, or trending low-stakes topics
- posts where a short personal comment can earn agreement or follow-up replies
- avoid threads where a good answer requires expert technical knowledge, marketing/growth tactics, code review, specialized tool familiarity, legal/medical/financial expertise, or brand/product disclosure

### Priority 1 -Rising

Good Rising targets are actively climbing, not just recently posted. Reddit's Rising list includes stalled posts that briefly trended and fell off -those are worse than a quiet /new post.

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/rising/
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Keep posts where:
- Age < 2h
- Upvotes >=5 (some early traction; 0-4 = dead on arrival)
- Comments < 50 (room for visible reply)
- Not pinned / locked / NSFW

To confirm the post is still rising (not stalled), re-check upvote count ~30 seconds later. If unchanged AND > 30 min old, pick the next candidate.

### Priority 2 -Search by find keyword

**Use today's rotated keyword** (see SKILL.md ->Keyword Rotation). At the start of the run, read `progress.json.keyword_rotation.find_index` and compute `today_find = keywords.find[find_index % len(keywords.find)]`. All Priority 2 searches within one run across all subs use this same `today_find` -don't change keywords per sub.

```bash
browser-act --session <run_session> navigate "https://www.reddit.com/r/<sub>/search/?q=<today_find>&sort=new&restrict_sr=1&t=day"
```

Keep: < 6h old, < 50 comments.

**Before this run ends** (during the final daily wrap-up), increment `find_index += 1` -regardless of whether Priority 2 actually ran (using only Rising is fine; each run counts once). Tomorrow's `today_find` will be the next item in the list.

**Edge cases:**
- `keywords.find` is empty ->ignore rotation, skip Priority 2, go straight to Priority 3
- `keywords.find` has only 1 item ->`today_find` is always that one; still +1 with no side effects (modulo pulls it back to 0)
- User changes `keywords.find` length mid-stream ->modulo handles it naturally; next run picks some entry in the new list

### Priority 3 -/new fallback

Take the newest qualifying post.

---

## Commenter Profile Check (log-only, non-blocking)

Sample karma of the first 3-5 non-AutoModerator commenters in the thread. Record `median_thread_karma` in the activity log for analysis, but **do not skip the post regardless of the result** -Reddit decides whether the comment survives, not us.

| Sample state | Action |
|--------------|--------|
| Thread has < 3 comments OR sample median >=10 | Log `median_thread_karma: low`, continue |
| Own comment_karma >=sample median x 20% | Log `karma_ratio: ok`, continue |
| Own < median x 20% AND median > 50 | Log `karma_ratio: low_risk`, continue (Reddit AutoMod handles filtering) |

---

## Generate Variants

Open the post sorted by top:
```bash
browser-act --session <run_session> navigate "<post_url>?sort=top"
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

From the markdown: extract post title, body, top 3 comments.

### D variant generation (brand insertion)

D is always generated alongside A/B/C -no conditional gates.

### Prompt template

```
You are a real Redditor replying in r/<sub>.

Identity:            [identity from persona_file]
Tone and voice:      [tone]
Phrases to avoid:    [never_say]

You've personally used: [brand keyword(s) + one-line what it is]
Your related experience: [brand_story]

The post you are replying to:
  Title: [post_title]
  Body:  [post_body]

The thread's top 3 existing comments:
  #1 [score]: [text]
  #2 [score]: [text]
  #3 [score]: [text]

Produce N variants, each 15-50 words
(length appropriate to sub type -see comment-rules.md):

A. Punchline         -short, sharp reaction; reversal, observation, or
                       dry humor consistent with Tone
B. Nerd Out          -use the Identity's knowledge area to surface a
                       concrete detail, mechanism, or explanation that
                       actually teaches the reader something
C. Riff              -extend or reverse top comment #1's angle without
                       restating it
D. Problem-Solution  -open with a specific detail from the post or a top
                       comment that naturally connects to your brand_story
                       (line 1); describe a related experience of your own
                       (1 sentence, grounded in brand_story); mention the
                       brand naturally as what ended up working (1 sentence);
                       end with outcome or invitation for follow-up. No CTA,
                       no link, no superlatives. Brand name appears exactly
                       once, mid-comment, not at the opener.

                       CRITICAL: Must NOT sound like an ad. Strictly use the
                       Voice and Tone specified above. Use first-person ("I").
                       The brand name must be a casual, passing mention in the
                       middle of a personal anecdote, never capitalized like
                       a slogan. No CTA, no link, no superlatives.

Hard rules for every variant:
- First sentence must respond to a specific detail from the post or a top comment.
  No generic openers.
- No "Great post!", "This is amazing!", "Thanks for sharing" or equivalents.
- No URLs.
- No AI-smell vocabulary -see comment-rules.md ->Forbidden Patterns.
- No brand name in any variant before Day 30 (including D).
- Must sound like the Identity above, not a generic assistant.
```

### D variant policy

- D is **always brand-bearing regardless of whether the rendered text mentions the brand** -it carries deliberate promotion intent. Log it with `brand_mention_intent: "deliberate"`.
- Whenever D is generated, the **Brand Exposure Target check** (`approval-rules.md` ->Part 2 Brand Approval) fires before approval or auto-pick handling.
- D follows `approval_policy` exactly like other brand-bearing content. Manual paths require explicit human pick; auto paths follow the auto behavior in `approval-rules.md` and write audit records.
- **Bot Bouncer gate:** if the sub's `sub_profiles.json[<sub>].has_strict_bot_bouncer == true`, surface the flag in manual approval items (e.g., "Warning: r/<sub> has BotBouncer moderating -this D variant is at higher takedown/ban risk."). For auto paths, log the flag in the audit record instead of creating a manual prompt.

### Picking which variant to publish (advisory default)

| Reply target | Prefer |
|-------------|--------|
| OP top-level post, short/funny/rant-style | A (Punchline) |
| OP asking a question / describing a problem, generic sub | B (Nerd Out) |
| OP in target sub, post connects to `brand_story` | **D** (if available) else B |
| An existing comment | C (Riff) |

User still gets shown all variants and picks.

Full length tables, AI-smell blacklist, and quality checklist in `comment-rules.md`.

---

## Duplicate Content Check (pre-approval, hard block)

Run **before** showing variants to user.

1. **Normalize** each variant and each past `activity_log.jsonl` entry's `content`:
   - Lowercase, strip URLs, strip `@mentions` and `r/subs`, strip punctuation (keep apostrophes), collapse whitespace.
2. **Compute jaccard similarity** between the variant's normalized token set and each past comment/post (pull last 200 entries from activity log where `type in {"comment", "post", "reply"}`).
3. **Reject thresholds:**
   - Exact `content_hash` match ->always reject
   - jaccard >=0.80 ->reject (too similar)
   - jaccard 0.60-0.80 ->warn user at approval ("this variant is 67% similar to your reply on `<post_url>` from `<date>`, okay to proceed?")
4. **On reject**, regenerate with instruction: `Do NOT use phrasing similar to: "<offending past content, first 200 chars>"`. Keep other variants that passed.
5. **Cross-account** (multi-account mode): also check against `~/.reddit-warmup/*/activity_log.jsonl` for last 7 days. Identical text from the same persona across two accounts = both flagged.

Persist `content_hash` (SHA-256 of normalized text) in every new comment/post entry -it's the fast-path exact-match gate.

---

## Approval + Publishing

**Write drafts to pending_approval:** `~/.reddit-warmup/<username>/pending_approval/<YYYYMMDDTHHMMSS>/`

- `comment_A.txt`, `comment_B.txt`, `comment_C.txt`, `comment_D.txt`
- `meta.json` -must include `platform`, `skill`, `batch_id`, `browser_id`, `username`, and full `variants` text (required for Hot Approval Rule C6 to work without re-running the daily task):
  ```json
  {"kind": "comment",
   "platform": "reddit",
   "skill": "reddit-warmup",
   "batch_id": "<YYYYMMDDTHHMMSS>",
   "post_url": "<url>", "subreddit": "r/<sub>", "post_title": "<title>",
   "post_body": "<complete post body text>",
   "stage": "<comment|promote>", "created_at": "<ISO>",
   "brand_bearing": <bool>,
   "browser_id": "<from config.yaml account.browser_id>",
   "username": "<reddit account username>",
   "approval_status": "pending",
   "queue_status": "queued",
   "queue_position": <int>,
   "queue_total": <int>,
   "approval_item_index": <int|null>,
   "display_group_id": "<account-scoped display batch id|null>",
   "displayed_at": null,
   "retired_at": null,
   "selected_variant": null,
   "approved_at": null,
   "approved_text_hash": null,
   "variants": {
     "A": "<full rendered text of variant A>",
     "B": "<full rendered text of variant B>",
     "C": "<full rendered text of variant C>",
     "D": "<full rendered text of variant D, omit key if not generated>"
   }}
  ```

There is no approval window - the batch stays in `pending_approval/` until the user replies or the 7-day stale cleanup removes it. If multiple comment/post batches are generated for the same account, show them together in one Approval Batch Request with stable item numbers. Reply `all A` applies to all displayed items that have variant A; item-specific replies like `1 B, 2 skip` apply to the numbered items. Full rules: `approval-rules.md` -> Approval Queue and Rules C3/C4/C6.

Do not rely on an active browser-act session while waiting for approval. Browser-act may close the session after the draft-generation flow. Hot Approval later starts a fresh `<run_session>` with the same stored `browser_id`.

**Brand-bearing variants trigger the Brand Exposure warning first** -see `approval-rules.md` ->Part 2 Brand Approval. The warning pre-gates the variant list; user sees the ratio + risk level before picking.

When this batch is included in an Approval Batch Request, show its variants in chat as one item block:
```
Approval Batch: reddit-warmup / <username>
platform: reddit  browser: <browser_id>  pending: <N>

[<approval_item_index>] kind: <comment|reply>  batch: <batch_id>
Target: r/<sub> -"<post title>"
<complete post body>

---
A. <full text of A>
B. <full text of B>
C. <full text of C>
(D. <full text of D>   OKbrand)

You can reply naturally: `all A`, `1 B`, `use the second one for 1`, `2 skip`, `1 make it shorter`, `remove the brand mention from 1`
Canonical command: `approve <username> <batch_id> A|B|C|D`
Skip command: `skip <username> <batch_id>`
Revise command: `revise <username> <batch_id> <instruction>`
```

The **approval batch anchor** and each **item line** are mandatory. They let the agent look up the right batch and browser profile metadata in any subsequent conversation turn, even after context compaction, while making clear which item a natural-language reply applies to. The active browser-act session may be gone; `browser_id` is enough to open the configured profile in a fresh `<run_session>`.

- `<username>` = Reddit account username (same as in `progress.json`)
- `platform` = `reddit`
- `skill` = `reddit-warmup`
- `<browser_id>` = value from `config.yaml.browser_id` (used verbatim in `browser open --headed`; not a session id)
- `<batch_id>` = the `pending_approval/<batch_id>/` directory name (ISO timestamp slug)

Tag any A/B/C that accidentally contains a brand keyword with `OKbrand` so the user sees it clearly.

**After the user picks, immediately echo back the selected item(s) before publishing:**
```
Picked: item <N> -> <A/B/C/D> -Publishing now...
  r/<sub> -"<post title>"
  > <first 120 chars of picked variant>...
```

This confirms to the user exactly which item and variant are being published. It is not a stopping point. Do not only write a `choice` file, marker, or local note; continue directly into Publish on user pick.

### Publish on user pick

**->Follow `comment-publishing.md` Steps 1a- in full.**

`act` does not exist in browser-act CLI. All comment publishing uses `scrollintoview` / `state` / `click <idx>` / `input <idx> "<text>"` primitives -exact sequence, fallback ladder, and verify logic are all in `comment-publishing.md`.

### Verify visibility

Use `comment-publishing.md ->Step 9` as the source of truth. The publish is successful only when the original post thread or the resolved comment permalink shows the submitted comment body.

- Body/permalink verified on the original thread or permalink ->`visibility: "visible"`.
- Body not found after original-thread reload + one retry ->`visibility: "pending"` or skip with `original_thread_visibility_failed`; do **not** treat the submit click as success.
- Markdown contains a rate-limit phrase ->trigger the anomaly stop (SKILL.md ->Anomaly Detection). **Do NOT write a normal successful `comment` log entry.**

### Log entry

```json
{
  "timestamp": "<ISO+offset>",
  "type": "comment",
  "subreddit": "r/<sub>",
  "post_url": "<url>",
  "post_title": "<title>",
  "content": "<published text>",
  "variant": "A|B|C|D",
  "contains_brand": <bool>,
  "brand_mention_intent": "none|accidental|deliberate",
  "content_hash": "<sha256>",
  "karma_before": <int>,
  "visibility": "visible|pending",
  "run_session_id": "<run_session>",
  "url_confirmed": "<url>",
  "page_title": "<title>",
  "evidence_screenshot": "evidence/<ts>-after-comment.png"
}
```

Update `progress.json.last_comment_time = now`.

---

## Between-Comment Timing

Enforced against `progress.json.last_comment_time`.

| Gap since `last_comment_time` | Behavior |
|------------------------------|----------|
| < 2 min | **Hard block.** Reddit's per-user comment rate limit triggers here. Don't publish; sleep until >=2 min |
| 2-30 min | Allowed, log as `soft_timing`. Acceptable for inbox reply bursts and camping within the watchtower window |
| >=30 min | Free to publish next proactive comment |
| >=60 min | Ideal for routine proactive comments |

**Default for proactive Stage 2 comments:** >=30 min since `last_comment_time` (not the old 60). Lets a natural run do 2-4 comments without forcing a 3-hour session.

**Reactive comments** (inbox reply processing, camping during the post's 30-min window): >=2 min is enough. Real users do burst-reply when catching up.

---

## Daily Comment Volume

Daily comment volume is governed solely by the Comment Schedule in `stages.md` (1-4/day depending on stage and day). No additional karma-based cap is applied -Reddit's own rate limiting and AutoMod filtering are the natural ceiling.

