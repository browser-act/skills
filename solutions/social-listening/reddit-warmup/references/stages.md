# Stage Behavior Reference

Detailed parameters for each of the three stages. The main SKILL.md points here for specifics.

---

## Stage 1: Lurk (Days 2-14)

**Goal:** Let the account "exist" naturally. Accumulate 50-80 upvotes, subscribe to 5 subreddits by Day 14 (3 warmup + 2 primary target).

### Upvote Parameters

| Rule | Value |
|------|-------|
| Start upvoting | Day 4 (Days 2-3 = browse only) |
| Gap between upvotes | 20-45 seconds (random) -**never below 15s** |
| Posts to browse per sub | First 10-15 posts (vary randomly, don't always use 15) |
| Upvotes per subreddit per session | Max 2 (Days 4-7) / Max 3 (Days 8+) |
| Post dwell time | 30-75 seconds (Days 4-9) / 75-150 seconds (Days 10+) |
| Sort order rotation | Hot only (Days 2-9) / Hot + New + Rising random (Days 10+) |
| Sessions per day | **1 session only** -do NOT re-enter within 4 hours if session already ran |
| Target total upvotes by Day 14 | 50-80 |

### Rate Limit & CAPTCHA Rules (MUST follow)

Any CAPTCHA encountered in any scenario goes through the same **3-tier ladder**. No exceptions for Phase / login / re-login. The ladder is described by intent -when browser-act CLI command names change in future versions, replace the example commands with whatever the current CLI exposes (run `browser-act --help` to check).

| Situation | Handling |
|------|---------|
| CAPTCHA / bot challenge encountered after any navigate / click | **Tier 1 (agent auto-attempt)**: call browser-act's CAPTCHA auto-solve command (currently `browser-act --session <s> solve-captcha`) -**try at most 2 consecutive times** (wait 10-20s between). Any success ->wait 45-60s + scan for rate-limit signals ->continue.<br>**Tier 2 (hand page control to user)**: both auto-solve attempts failed ->request a human-assist URL from browser-act. Use: `browser-act --session <s> remote-assist --objective "<describe the problem to solve>"`. Send the returned URL to the user in chat with a clear "what to do" description. **No browser-act commands from the agent while the user is operating the page** (not even `get markdown` / `screenshot` -that breaks the assist flow). Wait for the user to say "done" in chat ->wait 45-60s ->continue.<br>**Tier 3 (fallback)**: Neither user-assist command is available, OR the user doesn't respond within a reasonable window ->interactive mode keeps waiting; unattended mode logs `captcha_blocked` + `daily_skip_reason: "captcha_at_preflight"` + closes session and exits. |
| "whoa there, pardner!" / "Too Many Requests" / "ratelimit" / "try again in" appears | **Not CAPTCHA, this is rate-limiting**. Enter full-stop immediately: close session + log `rate_limit_hit` + `progress.json.rate_limit_hit_today = true` + no more write actions today |
| `rate_limit_hit_today == true` today | Skip all write actions for the day; Stage 1 behavior only; note the reason in the daily report |
| `rate_limit_hit` hit >=2 times in 3 days | Notify user; proxy/account may be flagged; recommend investigation |

**Inter-tier pacing**: after a Tier 1 success, enforce a 45-60s wait (see the "after solving CAPTCHA" row of the Between-Action Timing table) -Reddit stays in a high-sensitivity state right after CAPTCHA; writing immediately significantly raises the chance of re-triggering. Same for Tier 2 (Human Assist) success -wait 45-60s.

### Reference -Tier 1 ladder

```bash
# First solve-captcha attempt
browser-act --session <run_session> solve-captcha
# If returns solved: False ->wait 10-20s, then second attempt
sleep 15
browser-act --session <run_session> solve-captcha
# Both fail ->enter Tier 2

# Mandatory wait after either succeeds (45-60s random)
sleep 50

# After waiting, scan the page once to confirm no rate-limit signals before running the next action
browser-act --session <run_session> get markdown
```

### Reference -Tier 2 (page handover to user)

```bash
# Use browser-act remote-assist for page handover.

# Browser handover (works for CAPTCHA and any page-level block)
ASSIST_URL=$(browser-act --session <run_session> remote-assist \
    --objective "Please solve the CAPTCHA that appeared on Reddit")

# 2. Tell the user in chat what they need to do. Example:
#    "A CAPTCHA appeared, auto-solve failed. Please open this link
#     to complete verification: <ASSIST_URL>
#     Tell me 'done' when complete."

# 3. CRITICAL: during the assist, the agent sends NO browser-act commands
#    (no navigate, click, get markdown, screenshot -nothing) while
#    the user is on the assist URL. That's a documented browser-act rule:
#    sending commands mid-assist invalidates the assist flow.
#    Only wait in chat for the user to reply "done" / "completed".

# 4. After user confirms done, wait 45-60s for the page to settle
sleep 50

# 5. Scan the page once to confirm CAPTCHA is cleared and no rate-limit signals
browser-act --session <run_session> get markdown
# Clean ->continue main flow

# 6. Fallback if remote-assist is missing in a
#    future browser-act version:
#    - Tell the user in chat: "browser-act remote-assist is unavailable;
#      please open the browser yourself and solve the CAPTCHA, then reply 'done'"
#    - Still wait 45-60s after "done", then re-scan the page
```

### When browser handover is needed vs chat confirmation

Rule from the browser-act docs (paraphrased):

- **When the user needs to see or interact with content on the current browser page** (e.g. CAPTCHA / email verification redirect / checkout summary / settings change confirmation) ->**must hand over the browser via browser-act's user-assist mechanism** (currently `remote-assist`). Extracting the page content to chat for the user to read is **wrong**, because it bypasses the assist flow.
- **When the content is not yet in the browser, still being assembled by the agent** (e.g. comment drafts / post drafts / persona placeholder auto-draft / subscribe-sub shortlist / Brand Exposure warning / Stage 3 entry decision card) ->use the normal chat-display-and-user-pick flow; no browser handover needed.

Corresponding scenarios in this skill:

Page interactions fall into three types: **agent fills itself**, **browser handover to user**, **chat confirmation**.

| Scenario | Which path |
|------|-------|
| CAPTCHA / bot challenge appears in the browser-act-controlled browser | Browser handover (`remote-assist`) |
| Suspicious / "unusual activity" login challenge page | Browser handover (remote-assist) |
| Mid-task unexpected "verify phone" / "enter 2FA" challenge page | Browser handover (remote-assist) |
| **Post-registration interest-selection page** | **Agent auto-selects based on persona** -reads `persona_file.interests` / `config.yaml ->subreddits.warmup + target` / `keywords.content`, uses `browser-act state` to identify matching topic controls, then `browser-act click <idx>` to select them. No persona ->Skip |
| **Post-registration info-completion page (birthday / gender / region and other non-sensitive fields)** | **Agent auto-fills based on persona** -use persona values when available; otherwise approximate from proxy geo (fill required fields only, Skip all optional) |
| Email verification link click (happens in the **user's own default browser**, not the browser-act session) | Ask user to say "done" in chat |
| Comment Approval -show A/B/C/D drafts | Chat display |
| Path A / Path B post approval | Chat display |
| Persona placeholder auto-draft confirmation | Chat display |
| Stage 3 entry decision card A/B | Chat display |
| Subscribe-sub shortlist for user to pick | Chat display |

Do not use free-form action commands in any of the cases above. For interest selection or other non-sensitive forms, read `browser-act state`, identify the matching control indices, then use `browser-act click <idx>` / `browser-act input <idx> "..."`.

Core judgment:
1. **Does the agent have enough info to auto-fill?** (interests / birthday / gender and other non-verification forms) ->agent fills directly via `browser-act input <idx> "..."` / `click <idx>`
2. **Does this require direct user interaction with the browser page?** (CAPTCHA / challenge / 2FA / email-confirm-click-in-browser) ->browser handover via current browser-act user-assist command
3. **Is the content still in the agent's hands, not yet in the browser?** (drafts / decisions / shortlists) ->chat confirmation

### Persona-driven sub + post selection (Day 2+)

**Pre-flight loads `persona_file`** (or falls back to `config.yaml.keywords.content` if persona_file is empty) into working memory. Even in pure-lurk mode, persona drives two decisions:

Persona alignment is a ranking rule inside `subreddits.warmup`, not a license to add domain-expert communities. The warmup set must stay broad, low-context, and easy-karma; professional, career, business, technical, marketing, startup, regulated-advice, and brand-adjacent subs wait until target/secondary stages after recon and karma growth.

1. **Which sub to browse first today** -rotate among `subreddits.warmup`, preferring the sub whose topic matches `persona.interests` most closely today. Over a 7-day window all warmup subs should see roughly equal time; but each day's starting sub should feel intentional to the persona, not round-robin mechanical.
2. **Which posts to upvote within a sub** -scan the first 15 posts of Hot/New/Rising. Upvote up to the per-day cap for posts that align with `persona.interests` or `persona.backstory_keywords`. If nothing aligns well, just dwell (don't force an upvote -a persona with no interest in today's post slate reads more authentic than one that upvotes anything).

**Persona empty (Day 1 deferred)**: fall back to dwell-only, no sub preference, upvote deferred to posts with high engagement (score > 10) to look like a reader who "liked the comment section". Subscription schedule still fires on cadence.

### Daily Browse Sequence

1. Open the persona-preferred warmup sub ->browse and upvote posts matching persona interests
2. Wait **10-20 minutes** (simulates leaving to do something else)
3. Open the next warmup sub in rotation ->same
4. (Add more subs as subscriptions grow)
5. After all subs are done, **wait 3-5 minutes** before taking the screenshot and closing the session

### Subscription Schedule (persona-aware)

Subscribe to one new subreddit per day maximum -never subscribe to multiple on the same day (looks automated). The schedule below is a target cadence, not a rigid day-counter; the main flow checks whether the threshold has been reached each run and subscribes if not.

| Day | Target total subscriptions | What to subscribe |
|-----|---------------------------|-------------------|
| Day 1-3 | 0 | Browse only |
| Day 4-6 | 1 | 1st warmup sub |
| Day 7-10 | 2 | 2nd warmup sub |
| Day 11 | 3 | 3rd warmup sub -completes warmup set |
| **Day 12-13** | **4** | **1st primary target sub** (main flow, see below) |
| **Day 14** | **5** | **2nd primary target sub** (main flow, see below) |
| Day 15-20 | up to 8 | 3rd-5th primary target -main flow + daily tail (1/day max) |
| Day 21+ | up to 12 | Secondary target subs -main flow + daily tail (ongoing, 1/day max) |

**Hard caps:** `subreddits.target.primary` <=5; `subreddits.target.secondary` <=7; total across all tiers <=15.

**Which sub to subscribe to when the schedule ticks up (warmup phase):** among unsubscribed warmup subs, pick the one whose topic matches `persona.interests` most strongly. If persona is empty, go in config order. This selection happens only inside the already-vetted broad warmup list; do not subscribe to professional/domain subs as warmup substitutes.

**Day 12-14 primary target subscription (main flow -runs regardless of whether daily tail runs):**

On Day 12, 13, and 14, the main flow checks at the end of the daily session:

```
if current_day in [12, 13, 14]:
    unsubscribed_primary = [s for s in subreddits.target.primary
                            if s not in progress.json.subscribed_subs]
    if unsubscribed_primary and today_subscribe_count == 0:
        subscribe the first unsubscribed primary sub (same subscribe flow as Stage 1)
```

This is intentionally in the **main flow** (not daily-tail only) so that accounts with a single daily trigger still subscribe to primary targets before Day 22 commenting begins. One primary sub per day, never same day as a warmup sub.

**Day 15-20 remaining primary targets (main flow):**

```
if current_day in range(15, 21):
    unsubscribed_primary = [s for s in subreddits.target.primary
                            if s not in progress.json.subscribed_subs]
    if unsubscribed_primary and today_subscribe_count == 0:
        subscribe the first unsubscribed primary sub
```

**Day 21+ secondary targets (main flow -runs regardless of whether daily tail runs):**

```
if current_day >= 21:
    unsubscribed_secondary = [s for s in subreddits.target.secondary
                              if s not in progress.json.subscribed_subs]
    total_subscribed = len(progress.json.subscribed_subs)
    if unsubscribed_secondary and today_subscribe_count == 0 and total_subscribed < 15:
        subscribe the first unsubscribed secondary sub
```

Daily-tail Subscribe Opportunity still runs when available -it provides the same logic with richer recon data (karma gate, automod filter rate). Because it runs inside the same daily scheduled flow after the main flow, `today_subscribe_count == 0` prevents a second subscription that day.

**Why subscribe target subs during Stage 1 lurk (not just before Day 22)?**
Subscribing a sub at least 7-10 days before commenting gives the account a passive browsing history in that sub. A profile that subscribes to a sub on Monday and posts a comment on Tuesday is a weak bot signal; one that subscribed two weeks ago and lurked reads as a genuine member.

### Stage 1 End State

Before advancing to Stage 2, verify:
- Subscribed to >=5 subreddits (3 warmup + 2 primary target)
- Total upvotes >=50
- Account age >=14 days
---

## Stage 2: Comment (Days 15-29)

**Goal:** Build comment karma organically while reaching account age >=30 days. **Both `account_age_days >=30` AND `comment_karma >=20` are hard gates to Stage 3** -neither can be bypassed (manual "enter brand phase" also not allowed). Karma also governs which subs are safe to comment in within Stage 2 (see Day 21 check and **Subreddit Risk Profiling** in SKILL.md).

**Karma-first subreddit posture:** Stage 2 is not where the account proves professional expertise. Regardless of whether the persona is technical, marketing, founder, finance, legal, medical, or another professional profile, comments should start in broad, low-context, high-interaction warmup subs where lightweight personal reactions can earn karma. Professional/domain communities are target/secondary subs for later, after recon and karma growth.

### Subscription Gate (hard rule -no exceptions)

**Never comment in any subreddit that is not in `progress.json.subscribed_subs`.** Commenting in a sub the account hasn't joined is a bot-farm fingerprint -real users follow a sub before engaging in it.

- The sub must appear in `subscribed_subs` **before** the run that comments in it. Subscribing and commenting in the same session is not acceptable.
- **Primary target subs** are subscribed via the main flow on Days 12-14 (see Subscription Schedule above) -this guarantees they're subscribed at least 7 days before Day 22 commenting begins, regardless of whether daily-tail recon runs.
- **Secondary target subs** are added gradually via daily-tail Subscribe Opportunity (see `end-of-day-recon.md`), starting from Day 21 onward.
- **Fallback rule:** if all subscribed primary subs are blocked on a given run (karma gate / automod hostile / banned), the candidate pool automatically expands to include subscribed secondary subs. If secondary pool is also empty or all blocked, skip commenting today and log `skip("all_target_subs_blocked")`.

### Comment Schedule

| Phase | Days | Comments/day | Target subs | Notes |
|-------|------|-------------|-------------|-------|
| Initial commenting | Day 15-19 | 1/day (but skip comments on Day 17 and 19, browse/upvote only) | Warmup subs only | Create irregular rhythm to avoid bot detection |
| Increase frequency | Day 20-21 | 2/day | Warmup subs only | -|
| Start transition | Day 22-25 | 3/day (2 warmup + 1 target) | Mixed | Build more karma while testing target subs gradually |
| Target-focused | Day 26-29 | 4/day (2 warmup + 2 target) | Mixed | Stronger karma-building pace before Stage 3 gate |

**Rhythm notes:** Days 15-19 comment once per day, but Days 17 and 19 deliberately skip commenting (browse + upvote only) to create an irregular activity pattern. Accounts that comment at the same time every day trigger Reddit's automation detection.

Day 17 / Day 19 zero-publish counters are expected. If the run reports `comments_done: 0`, `replies_done: 0`, or no approval batch on those days, treat it as the designed irregular-rhythm skip, not a failure. Daily reports may mention "planned comment-skip day"; anomaly detection must not flag it.

### Karma Milestone Checks

**Day 21 check:**
- Transition to target subs proceeds regardless of karma -each sub's own `karma_gate` (from recon) is the deciding factor per `stage2-comment.md ->Filter Step 1`.
- Log current `comment_karma` in progress.json for visibility, but do NOT block the transition.

**Day 29 check (gate to Stage 3):**
- `account age < 30 days` ->Do NOT advance to Stage 3; extend this stage
- Notify user: "Account `<username>` isn't ready for brand promotion yet -account age: <N> days (need 30). Continuing the comment stage. Estimated ready date: <date>."
- `account age >=30 days AND comment_karma >=20` ->entry decision card auto-fires; on user's choice B, advance to Stage 3.
- `account age >=30 days AND comment_karma < 20` ->**stay in Stage 2**. Both gates are hard -below 20 karma, the entry card does not fire AND manual "enter brand phase `<username>`" command is refused with a karma-gap message (promo posts with near-zero karma look planted, and skill-level hard gate removes the decision burden from the user). The account keeps commenting in Stage 2 until it hits 20; then next run's Day-29-style check auto-fires the entry card.

### Between-Comment Timing

Real multi-hour waits can't happen within a single Agent session. The skill enforces gaps across invocations using `last_comment_time` in progress.json. Full policy + distinction between proactive and reactive comments lives in the table below.

| Situation | Rule |
|-----------|------|
| Absolute safety floor | **>=2 minutes** since `last_comment_time` -below this, Reddit rate-limits the account. Hard block, no exceptions |
| Between proactive comments (Stage 2 scheduled) | Target >=30 minutes (ideal >=60) |
| Between reactive comments (inbox reply / camping) | >=2 min is enough -real users do burst-reply |
| Before typing a comment | Browse the post for 30-90s first ("read" before commenting) |
| After submitting a comment | Wait 10-25s before any other action (simulate reading replies) |
| Between upvoting different posts | 20-45 seconds (no rapid consecutive upvotes) |
| Switching between subreddits | 10-20 minutes (realistic switching interval) |
| After the user solves a CAPTCHA manually and says "done" | **Wait at least 45-60s before the next action** (the user just solved a CAPTCHA, Reddit remains in high-sensitivity state; immediate write actions significantly raise re-trigger probability) |
| If "whoa there" / any warning detected | Stop commenting AND posting for the day; log `rate_limit_hit: true` -see `SKILL.md ->Anomaly Detection` |
| If rate limit hit twice in 3 days | Notify user -IP might be flagged, consider checking proxy quality |

**Check for rate limit after EVERY action:**
```bash
# After every click/act/navigate, read page markdown and scan for rate-limit signals
browser-act --session <run_session> get markdown
```
Scan the returned markdown (case-insensitive) for any of:
- `whoa there`
- `too many requests`
- `you are doing that too much`
- `ratelimit` / `try again in`
- `429`

Any hit ->immediately enter the SKILL.md ->Anomaly Detection full-stop flow.

**Practical flow:** The scheduled daily run executes the day's allowed proactive comment quota inside one account session, respecting `last_comment_time` and the timing table above. Manual hot approvals and inbox/watchtower replies may happen later, but they are reactive publish flows only; they must not re-run the daily Stage 2 task or create a second scheduled account-warmup session.

---

## Stage 3: Promote (Day 30+)

**Goal:** Organic promotion of the user's brand through natural-looking posts. Max 1 promotional post per week per account.

Full promotional-post flow (conditions, sub selection, recon, prompt, approval, publish) lives in `stage3-promote.md ->Path B`. This file only holds the extra timing/rhythm parameters not covered there.

### Weekly Activity Pattern & Posting Schedule

Spread the week so activity doesn't look bot-regular. **Applies to both Stage 2 and Stage 3** (on top of each stage's base daily comment count: 1-4/day in Stage 2, 2-4/day in Stage 3). Stage 1 is too low-volume for this pattern to matter; just follow the per-day upvote schedule.

| Day of week | Comment activity | Path A post (Help/Share) | Path B post (Promo/Brand) | Notes |
|-------------|-------------------|------------------------|--------------------------|-------|
| Monday | Normal | Possible | -| Good day to draft weekly posts |
| Tuesday | Light (~50%) | -| -| ~50% fewer comments, no new posts |
| Wednesday | Normal | -| **Preferred day** | Mid-week; promotional/brand posts fire on Wednesday |
| Thursday | Light (~50%) | -| -| ~50% fewer comments |
| Friday | **Preferred day** | **Yes (Path A only)** | -| High engagement; non-promotional posts land well here |
| Saturday | Normal | Possible | -| Casual posts land well |
| Sunday | Rest | -| -| Browse only, or skip the run entirely |

**Rationale**: Path A (Help-seeking / Sharing, non-promotional) lands best on Friday when Reddit traffic peaks. Path B (Promotional / brand-bearing) uses Wednesday mid-week engagement curve. This keeps promotional visibility natural (spread) rather than clustered (bot-like).

**Stage 2 Wednesday practice post**: follows Path A rules; fires on Wednesday with non-brand intent. Path A rules apply (no promotional language).

### Post Type Mix (per week)

Balance the week's posts across three shapes. **Do not add a counter field** -proportions are derived at read-time by grouping `activity_log.jsonl` entries where `type == "post"` within the current week.

| Type | Target share | Shape | Preferred day |
|------|-------------:|-------|---|
| Help-seeking | ~40% | "Has anyone dealt with X?" -invites discussion, looks genuine | Friday |
| Sharing | ~40% | "Here's how I solved Y" -value-first, no brand mention needed | Friday |
| Promotional | >=0% | Brand-adjacent story -**advisory** 1/week per account; exceeding triggers an extra warning prompt (see `approval-rules.md ->Weekly Posting Cap`), user can override with explicit ack | Wednesday |

Help-seeking and Sharing posts are Path A in SKILL.md; Promotional is Path B.

### Upvoting in Stage 3

Continue upvoting as in earlier stages (10-20/day), now spread across both warmup and target subs.



