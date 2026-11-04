# Phase 1: Account Onboarding

Runs once per account. Triggered when the user says "reddit warmup" / "start warmup" / "30-day warmup" etc., AND `~/.reddit-warmup/<username>/config.yaml` does not exist locally (otherwise go straight to Phase 2).

**Key principle:** regardless of new registration or existing-account takeover, **browser profile creation + proxy binding** is a mandatory step, and must be done BEFORE registration / login -both the register and login pages require an already-proxy-bound headed browser to open.

## Runtime prerequisites

Before any browser/proxy operation, load the BrowserAct entry skill, then the current core and advanced guides. Confirm the CLI is callable and authenticated. Use current lifecycle instructions; a returned purchase page link is not a created browser. When `config.yaml` is absent, keep all account state in pending variables until Step 6/7.5; do not rewrite an existing completed configuration.

## Step 1 -Account type + proxy setup

### 1.1 -Account type

Ask the user:

```
Is this a fresh new Reddit account, or an existing one you're taking over?
  A. New registration
  B. Existing account
```

No credentials are collected here -registration and login are both handled via browser remote collaboration in Step 3. The username is confirmed via `/user/me/` after Step 3 completes (both paths).

New accounts land at Day 1; existing accounts go through login ->Day is determined in Step 4 based on Reddit-side karma/age.

### 1.2 -Proxy setup

Reddit account nurturing requires a **fixed, persistent IP** -static proxy is strongly recommended over dynamic rotation. Check for available purchased proxies first:

```bash
browser-act proxy list
```

**Case A -list has active proxies:** show the available proxies (exclude EXPIRED / ALLOCATION_FAILED) and offer these options:
- Select one of the purchased proxies ->note `<proxy_id>`, use `--static-proxy <proxy_id>` in Step 2.
- "I have my own proxy URL" ->collect `<proxy_url>`, use `--custom-proxy <proxy_url>` in Step 2.
- "Purchase a new one" ->follow the same flow as Case B Option B below.

**Case B -list is empty:** ask the user:

```
No purchased static proxy is available. Choose one:
  A. I have my own proxy URL (socks5://user:pass@host:port or http://...)
  B. Purchase a browser-act static residential proxy (generate purchase link now)
```

- **Option A:** collect `<proxy_url>`. Use `--custom-proxy <proxy_url>` in Step 2.

- **Option B:** if the user picks B, treat it as consent and run:

  ```bash
  browser-act proxy buy-request
  # Returns: purchase_url + request_id
  ```

  Send `purchase_url` to the chat:

  > "Purchase link: `<purchase_url>`
  > Complete the purchase in the browser, then reply **'done'**."

  **Wait for user to say "done".** Then:

  ```bash
  browser-act proxy buy-status --request-id <request_id>
  browser-act proxy list
  ```

  Find the newly added active proxy entry, note its `<proxy_id>`. Use `--static-proxy <proxy_id>` in Step 2.

---

## Step 2 -Create browser profile + bind proxy + verify IP

Use a unique profile name `reddit-setup-<ts>` and a temporary run session `reddit-warmup-setup-<ts>`. The name is not the persistent browser ID.

Show the selected fixed proxy and the proposed profile purpose. Explain that a new profile starts without login state and that stealth creation completes on the returned page. Follow the current BrowserAct advanced guide for user authorization; do not repeat a confirmation the user has already supplied.

```bash
SETUP_BROWSER_NAME="reddit-setup-<ts>"

# Choose exactly ONE proxy option, using the user's selected proxy.
browser-act browser create --name "$SETUP_BROWSER_NAME" --type stealth --desc "Reddit warmup account setup" --objective "Create a persistent fixed-proxy browser for the requested Reddit account warmup" --static-proxy <proxy_id>
# Alternative for a user-provided fixed proxy:
browser-act browser create --name "$SETUP_BROWSER_NAME" --type stealth --desc "Reddit warmup account setup" --objective "Create a persistent fixed-proxy browser for the requested Reddit account warmup" --custom-proxy <proxy_url>
```

If the result contains `purchase_url` and `request_id`, show both and wait for the user to finish on that page. Do not open a guessed name/ID, assume completion, or issue another create request. After the user confirms completion:

```bash
browser-act browser create-status --request-id <request_id>
```

Continue only after status reports creation completed. Read the actual persistent browser ID from the returned result; use `browser-act browser list` to resolve the completed profile if necessary. Save that ID in the onboarding variable `SETUP_BROWSER_ID`. If pending/failed/cancelled, remain in onboarding and do not write final account config.

```bash
# SETUP_BROWSER_ID is the actual ID returned after completed creation, not SETUP_BROWSER_NAME.
browser-act --session <run_session> browser open --headed "$SETUP_BROWSER_ID" https://ipinfo.io/json
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> get markdown
```

Read IP + `timezone` from markdown:

- **If using `--static-proxy` (browser-act purchased):** store the displayed IP as onboarding variable `baseline_ip_pending`. No leak check needed -browser-act guarantees the proxy is bound. Step 6 writes it to `progress.json.baseline_ip`. On every subsequent session open, compare the current IP against `baseline_ip`; if they differ, warn the user (proxy may have been reassigned or expired).
- **If using `--custom-proxy`:** verify the displayed IP is not the machine's real IP -if it matches the real IP, **stop immediately** and have the user check the proxy config. If correct, store `baseline_ip_pending` and `baseline_timezone_pending`; Step 5 uses the timezone as the suggested default for `account.timezone` (user can override), and Step 6 writes the baseline IP fields.

**Proxy conflict check:**

List matching local files under `~/.reddit-warmup/*/config.yaml`, then read each file and compare `account.proxy` against the selected proxy identifier:
- purchased static proxy ->compare `static-proxy:<proxy_id>`
- custom proxy ->compare the exact proxy URL or the redacted host/port fingerprint recorded in config

If any match ->warn: "Warning: This proxy is already bound to `<conflicting_username>`. Sharing one proxy between two accounts risks both being flagged. Please use a separate proxy." Require explicit confirmation before continuing. Store `proxy_conflict_note_pending` and carry it into `config_pending`; write it into the final `config.yaml` only in Step 7.5.

---

## Step 3 -Register / Login via remote collaboration

Open the right page and hand control to the user. **Send no browser-act commands while the user is operating the page.**

### Step 3A -New account registration

```bash
browser-act --session <run_session> navigate https://www.reddit.com/register/
browser-act --session <run_session> wait stable --timeout 20000
ASSIST_URL=$(browser-act --session <run_session> remote-assist \
    --objective "Complete Reddit registration: enter email ->Continue ->enter username + password ->Sign Up. Tell me 'done' when you see the Reddit home page.")
```

Tell the user:

> "Reddit registration page is open: `<ASSIST_URL>`
>
> 1. Enter your email ->click **Continue**
> 2. Enter your desired username and password
> 3. Click **Sign Up**
>
> Reply **'done'** when complete."

After "done":

```bash
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> get markdown
```

**Post-registration (run in order):**

1. **Email verification** -Ask: "Please click the verification link in your inbox. Reply **'done'** when complete." (Unverified accounts are silently filtered by AutoMod in Stage 2.)

2. **Confirm actual username via `/user/me/`** (only authoritative source):
   ```bash
   browser-act --session <run_session> navigate https://www.reddit.com/user/me/
   browser-act --session <run_session> wait stable --timeout 30000
   browser-act --session <run_session> state
   # Read the current URL from state and extract <actual_username>: ^https?://(www|old|new)\.reddit\.com/user/([a-zA-Z0-9_-]+)/
   ```
   Redirects to `/login/`, stays on `/user/me/`, or displays a network-security block/challenge ->stop; registration/login identity has not been confirmed. Do not initialize a username directory named `me`.

3. **Session formalization:**
   ```bash
   browser-act session close <run_session>
   # Create ~/.reddit-warmup/<actual_username>/evidence/ with the agent's filesystem tools before screenshot.
   browser-act --session <run_session> browser open --headed "$SETUP_BROWSER_ID" https://www.reddit.com/user/me/
   browser-act --session <run_session> wait stable --timeout 15000
   browser-act --session <run_session> screenshot ~/.reddit-warmup/<actual_username>/evidence/ip-verify.png
   ```
   From this point: `<username> = <actual_username>`, `<browser_id> = "$SETUP_BROWSER_ID"`. Future browser-act commands use fresh per-flow `<run_session>` values; do not rely on this setup session surviving.

4. **Interest selection** ("What are you interested in?"): read `browser-act --session <run_session> state`, identify an appropriate visible topic from the user-provided interests, then `click <current_topic_idx>`. Refresh `state` after each click; use its current indices for the next choice. If interests are not yet supplied, skip optional selection rather than inventing a persona.

5. **Profile completion** (birthday / gender / region) ->auto-fill required fields from persona or proxy geo; skip optional fields.

New account ->`start_date = today`, `current_day = 1`, `stage = "setup"`. Jump to Step 5.

### Step 3B -Existing account login

```bash
browser-act --session <run_session> navigate https://www.reddit.com/login/
browser-act --session <run_session> wait stable --timeout 20000
ASSIST_URL=$(browser-act --session <run_session> remote-assist \
    --objective "Log in to Reddit with your username and password. Tell me 'done' when you can see your Reddit home page.")
```

Tell the user:

> "Reddit login page is open: `<ASSIST_URL>`
>
> Enter your username and password, then click **Log In**.
> Complete any CAPTCHA or 2FA if prompted. Reply **'done'** when you see your home page."

After "done":

```bash
browser-act --session <run_session> wait stable --timeout 15000
browser-act --session <run_session> get markdown
```

Still on `/login/` or `/register/` after "done" ->ask user to retry. "incorrect" / "wrong password" / "locked" in page ->tell user credentials failed, ask them to check and try again.

**Post-login (run in order):**

1. **Confirm username via `/user/me/`** (only authoritative source):
   ```bash
   browser-act --session <run_session> navigate https://www.reddit.com/user/me/
   browser-act --session <run_session> wait stable --timeout 30000
   browser-act --session <run_session> state
   # Read the current URL from state and extract <actual_username>: ^https?://(www|old|new)\.reddit\.com/user/([a-zA-Z0-9_-]+)/
   ```
   Redirects back to `/login/`, stays on `/user/me/`, or displays a network-security block/challenge ->login identity was not confirmed; do not write final state or infer a username from the self alias. Use the current page for user-directed login/access recovery.

2. **Session formalization:**
   ```bash
   browser-act session close <run_session>
   # Create ~/.reddit-warmup/<actual_username>/evidence/ with the agent's filesystem tools before screenshot.
   browser-act --session <run_session> browser open --headed "$SETUP_BROWSER_ID" https://www.reddit.com/user/me/
   browser-act --session <run_session> wait stable --timeout 15000
   browser-act --session <run_session> screenshot ~/.reddit-warmup/<actual_username>/evidence/ip-verify.png
   ```
   From this point: `<username> = <actual_username>`, `<browser_id> = "$SETUP_BROWSER_ID"`. Future browser-act commands use fresh per-flow `<run_session>` values.

Run login verification (four-layer check; details in `login-verification.md`). Then ->Step 4 for Reddit-side status detection.

## Step 4 -Existing account only: detect Reddit-side current status

Only runs when Step 1 chose existing account; skip for new accounts.

**4.1 Read the account profile, extract age + karma:**

```bash
browser-act --session <run_session> navigate https://www.reddit.com/user/<username>/
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Parse `account_age_days` and `comment_karma` from markdown; determine starting Day per this table:

| Condition | Starting Day |
|------|----------|
| Age > 30d AND karma >=50 | Day 30 (promote) |
| Age > 30d AND karma 10-49 | Day 15 (comment) |
| Age > 30d AND karma < 10 | Day 8 |
| Age 15-29d | Day 15 |
| Age < 15d | Day 1 |

> **Why is the karma threshold here (50) higher than the Stage 3 entry hard gate (20)?** The two thresholds serve different scenarios:
> - **50 (Phase 1 starting-day jump)**: an existing account is jumped straight to Day 30, **skipping the skill's own 30 days of lurk + comment work**. Reddit hasn't seen this warm-up history, so more karma buffer is needed to make "suddenly starting to post promotions" look less abrupt.
> - **20 (Stage 3 hard gate)**: the account has gone through the skill's own 30-day rhythm -systematically done lurk + comment under the skill -so Reddit has seen a complete activity trace, and 20 karma is enough. But **this is a hard limit** -accounts that finished 30 days without hitting 20 karma still can't enter Stage 3, and must continue commenting to accumulate karma.
>
> So an age 45d + karma 25 existing account will land on Day 15 (comment stage), not straight on Day 30 -even though it literally meets both conditions of the Stage 3 entry gate. This is **intentional** extra buffer, not a typo.

**4.2 Historical content backfill:** open `/user/<username>/submitted/` and `/user/<username>/comments/`, `get markdown`, parse up to 100 posts + 100 comments each, append to `activity_log.jsonl` with `"imported": true` on each. This baseline supports downstream de-dup and shadowban checks.

**4.3 Migration-transition determination:** if the user is taking over an existing account onto a **new** browser profile / new proxy (the one created in Step 2), treat this as "device change":

| Migration day | Allowed behaviors | Session duration |
|--------|----------|--------------|
| Day 1-2 | Browse only | 5-10 min |
| Day 3 | Browse + 1-2 upvotes | 10-15 min |
| Day 4-5 | Browse + upvotes + subscribe | 15-20 min |
| Day 6+ | Normal rhythm | Normal |

Keep `env_migration_pending = true`, `migration_day_pending = 1`, and `migration_clean_logins_pending = 0` in memory. Do not write `progress.json` here. Step 6 copies these values after loading the template, so template defaults cannot overwrite them. Daily migration execution is defined in `migration.md`; three consecutive clean daily runs complete migration for subsequent runs.

If an explicitly reused profile+proxy is unchanged and this has been verified, set pending migration values to false/0/0. A newly created profile is always a changed environment. Initialize new-account migration values to false/0/0.

## Step 5 -Collect remaining config.yaml fields (pending only)

Use `assets/config.yaml.template` as the schema for the final config, but **do not write `~/.reddit-warmup/<username>/config.yaml` yet**. During Phase 1, collect values into an in-memory `config_pending` object. The official `config.yaml` is written only after Step 7.5 approval-policy selection, so an interrupted onboarding cannot be mistaken for a runnable Phase 2 account.

Agent fills these known pending fields automatically before asking the user for the rest:

| Field | Value |
|------|------|
| `account.username` | `<actual_username>` from Step 3 `/user/me/` |
| `account.browser_id` | `$SETUP_BROWSER_ID` from Step 2 |
| `account.proxy` | `static-proxy:<proxy_id>` for purchased BrowserAct proxy, or the custom proxy URL / redacted host:port fingerprint for user-provided proxy |
| `account.timezone` | Default suggestion from Step 2 `baseline_timezone_pending`; user can override |
| `account.audience_tz` | Defaults to `account.timezone` if user leaves blank |
| `approval_policy` | Leave unset in `config_pending` until Step 7.5 records the user's selected policy |

If `proxy_conflict_note_pending` exists, carry it in `config_pending` and write it as a comment near `account.proxy` when the final config is created in Step 7.5.

Ask the user to fill or confirm these remaining fields:

| Field | Description |
|------|------|
| `subreddits.warmup` | 2-3 large, non-brand-related, non-professional practice subs optimized for easy karma |
| `subreddits.target.primary` | **Required: at least 2, hard cap 5.** Core target subs where you want to build influence. Subscribed by the main flow on Days 12-14 so the account has 7-10 days of passive lurk history before Day 22 commenting begins. If you supply fewer than 2, onboarding will not complete. |
| `subreddits.target.secondary` | Optional at start, hard cap 7. Fallback / monitoring / karma-building subs. Leave blank now -add them gradually via daily-tail discovery or by manually appending entries after Day 21. Total across primary + secondary must not exceed 12. |
| `keywords.find` | Keywords for searching candidate posts (can be left blank; re-prompted on Day 14) |
| `keywords.content` | Persona keywords (identity / background / experience) |
| `keywords.brand` | Brand terms (used from Day 30+; can be left blank; re-prompted on Day 29) |
| `account.timezone` | The "local" timezone for the account. The proxy timezone grabbed from ipinfo in Step 2 is only a **suggested default** -the user can accept it, or change to any other timezone (e.g., based on the operator's own schedule, target audience timezone, or proxy geography). Account-rhythm comparisons (Wednesday check, 07:00-23:00 gate, weekly reset, content timing) use this value; daily idempotency uses `account.scheduler_timezone` when set |
| `account.audience_tz` | Target audience timezone. May differ from `account.timezone` (e.g., the account's proxy shows US East but target users are in US West). Defaults to `account.timezone` if blank |

## Step 5.5 -Sub auto-discovery (optional; also triggered by the "refresh subreddit pool" command)

User doesn't know which subs to configure ->run auto-discovery: do a Reddit sub search for terms in `keywords.find + brand + content`, classify candidates, show shortlist, user picks ->patch into config.

**Classification rules:**

| Signal | Assign to |
|--------|-----------|
| Large + generic, high-interaction, low-expertise topic (>500k members) | `warmup` |
| Medium + brand-adjacent + active (10k-100k, members online ratio > 1:5000) | `target.primary` |
| Small/niche + brand-adjacent, OR low activity, OR uncertain fit | `target.secondary` |

Show the user three columns: proposed tier, sub name, member count + online count + one-line description. User can override any tier assignment before confirming.

**Warmup sub hard rule:** do not place professional, domain-expert, career, business, technical, marketing, startup, regulated-advice, or brand-adjacent communities into `subreddits.warmup`, regardless of the user's persona. The warmup phase is for earning low-friction karma and creating a normal browsing footprint, not proving expertise in the account's eventual niche. Put professional or brand-adjacent subs into `target.primary` / `target.secondary` and use them only after the account has enough karma and recon says the gate is safe.

**Validation gate before exiting Step 5.5:**
- `subreddits.target.primary` must have >=2 entries. If fewer, prompt the user to add more or accept suggestions. Do not proceed to Step 5.6 until this is satisfied.
- Total `target.primary + target.secondary` must not exceed 12. If auto-discovery produces more, surface the top-ranked ones and let the user curate.

This step is also re-triggered post-onboarding in two ways:

1. **Manual command** -user says "refresh subreddit pool `<username>`"
2. **Auto-trigger from stall detection** -`comment-follow-up.md Step 3.5` fires this when >=50% of warmup subs are marked `warmup_stall = true`. The agent surfaces the alert in the daily report and asks the user to confirm before running discovery. Discovery does NOT run automatically without user confirmation.

In both cases: runs the same discovery logic against the current `keywords.find + brand + content` and proposes updates to `subreddits.warmup / target.primary / target.secondary`. Changes to primary take effect in the next Day 12-14 main-flow subscribe window; changes to secondary are picked up by the next daily-tail recon run.

**Stall-triggered refresh behavior:** when proposing replacement subs, first check `sub_profiles.json` -subs already marked `warmup_stall = true` should NOT be re-proposed unless the stall flag has been cleared. The Tier 1 / Tier 2 shortlist below is the fallback pool for replacements.

### Newbie-friendly warmup sub shortlist (fallback when auto-discovery can't find good matches)

Use these as fallback candidates for `subreddits.warmup` when the user has no strong preference. They are broad, generically themed, and easier to participate in without specialist context. Rules still change, so the skill must run live recon before any write action.

**Tier 1 -Broad default communities (good first candidates for any persona):**

| Sub | Why it's newbie-friendly |
|---|---|
| `r/CasualConversation` | Explicit "be welcoming to new accounts" rule; short text posts; easy to find something to comment on |
| `r/NoStupidQuestions` | Q&A format = natural comment opportunities; low-context answers can fit naturally |
| `r/AskReddit` | Largest sub, generic questions, 100+ top-of-hot posts per day; comments under low-score threads avoid AutoMod scrutiny |
| `r/Showerthoughts` | Short single-sentence posts; engagement opportunities are "agree / riff / related observation" one-liners |
| `r/mildlyinteresting` | Visual content, short captions; comments are usually just "cool / never noticed that / same thing happened to me" |
| `r/LifeProTips` | Advice format; commenting "I've done this for years, also works for..." fits naturally |
| `r/todayilearned` | Historical / factual posts; comments extend or correct the fact |

**Tier 2 -Social-resonance karma builders (pick for easy reactions, not professional fit):**

| Social lane | Candidate subs (run recon before writing) |
|---|---|
| Any / general | `r/CasualConversation`, `r/NoStupidQuestions`, `r/AskReddit`, `r/mildlyinteresting` |
| Humor / relatable life | `r/funny`, `r/MadeMeSmile`, `r/wholesomememes`, `r/meirl`, `r/mildlyinteresting` |
| Fashion / style / trends | `r/Outfits`, `r/fashion`, `r/streetwear` |
| Pop culture / entertainment | `r/popculturechat`, `r/entertainment`, `r/movies`, `r/television`, `r/Music` |
| Food / home / plants | `r/cooking`, `r/food`, `r/MealPrepSunday`, `r/houseplants` |
| Pets / visual | `r/cats`, `r/dogs`, `r/aww` |
| Gaming / hobbies | `r/gaming`, `r/patientgamers`, `r/books` |

**Do not use as warmup for any professional persona:** `r/learnprogramming`, `r/webdev`, `r/SideProject`, `r/selfhosted`, `r/programming`, `r/MachineLearning`, `r/devops`, `r/sysadmin`, language-specific expert subs, `r/marketing`, `r/socialmedia`, `r/SEO`, `r/PPC`, `r/advertising`, `r/sales`, `r/startups`, `r/indiehackers`, `r/Entrepreneur`, `r/smallbusiness`, or any expert/professional sub where good comments require specialized context. These can be target or secondary subs after recon and karma growth, not early karma-building warmup subs.

**Avoid during Days 2-14 warmup (strict AutoMod / high karma gate):**

| Sub | Why to avoid as warmup |
|---|---|
| `r/programming` / `r/MachineLearning` / `r/devops` / `r/sysadmin` | Technical expert communities; good comments require domain context and fresh accounts are easy to filter |
| `r/learnprogramming` / `r/webdev` / `r/SideProject` | Treat these as strict professional-context communities; use later as target/secondary, not as early karma warmup |
| `r/marketing` / `r/socialmedia` / `r/SEO` / `r/PPC` / `r/advertising` / `r/sales` | Professional marketing / growth communities; fresh-account comments can look like lead-gen or self-promo |
| `r/startups` / `r/indiehackers` / `r/Entrepreneur` / `r/smallbusiness` | Business and founder communities attract promotional behavior; treat as target/secondary after recon |
| `r/Technology` | Active automod catches new accounts in threads about any specific company |
| `r/science` | Explicit karma + account-age gate; verified-expert only for top-level comments in some threads |
| `r/news` / `r/worldnews` | Politically sensitive; new accounts' political takes silently auto-flagged |
| Anything with "no new accounts" in the sidebar | Literally says no |

### Picking 2-3 warmup subs (Phase 1 Step 5)

Pick **2 from Tier 1** (broad, high-volume defaults) + **0-1 from Tier 2** social-resonance karma builders. Do not pick professional/domain subs for warmup, even when the persona is a developer, founder, marketer, operator, consultant, finance person, medical/legal professional, or AI user. This way:

- Daily browsing has guaranteed content (Tier 1 never runs dry)
- Comment opportunities are easy, low-context, and karma-friendly
- Zero subs are on the avoid list

Example for a professional persona (developer, marketer, founder, consultant, etc.):
```yaml
subreddits:
  warmup:
    - r/CasualConversation   # Tier 1, broad default
    - r/NoStupidQuestions    # Tier 1, easy Q&A comments
    - r/Outfits              # style / trend lane; broad social reactions
  target:
    primary:
      - r/<professional-sub> # professional context starts after karma/recon
      - r/<brand-adjacent-sub>
```

**Extra step for existing accounts:** for each sub in `subreddits.warmup + target`, **run recon immediately** (see `stage2-comment.md ->Subreddit Risk Profiling`) and write `sub_profiles.json`. Subs where `karma_gate > own karma` must be flagged to the user during onboarding, not silently swallowed.

## Step 5.6 -Create persona.json (mandatory before Day 15; strongly advised on Day 1)

The skill does NOT auto-generate persona content -all voice / backstory / brand_story must come from the user. Without persona, Day 15+ comments get skipped daily and Day 30+ Path B brand posts can't fire. **Best practice: fill it on Day 1 while context is fresh.**

Copy `assets/persona.json.template` to `~/.reddit-ops/personas/<username>.json` and walk the user through each field **in chat**:

| Field | What to ask the user |
|---|---|
| `identity` | "In one sentence, who is this account? Job title, years of experience, relevant expertise." |
| `tone` | "How does this person sound when writing online? (casual / blunt / dry / self-deprecating / etc.)" |
| `interests` | "3-5 topics this person genuinely follows -not brand-related, just personal interest" |
| `backstory_keywords` | "3-5 concrete past experiences the account can reference authentically (e.g., 'got burned by a $500 agency bill in 2023')" |
| `brand_story` | **"1-3 sentences, first-person, describing your / their experience building or using the product you plan to promote. This is the anchor for Day 30+ Path B posts. Keep it specific and believable -stock marketing copy reads like an ad and gets auto-filtered."** |
| `never_say` | "Any phrases this account should never use (e.g. 'as an AI', 'I hope this helps', stock Reddit cliches)" |

Then set `config.yaml ->persona_file: ~/.reddit-ops/personas/<username>.json` (top-level field, not under `account:`).

**If the user says "I'll fill it later":**
- Accept and proceed (Day 2-14 is lurk-only, doesn't need persona)
- BUT explicitly warn: "Day 15 comments and Day 30 brand posts will be blocked until this file exists with real content. You'll get a reminder on Day 14."
- Leave `config.yaml ->persona_file` empty; set onboarding variable `persona_defer_reminder_day_pending = 14`. Step 6 writes this into `progress.json ->persona_defer_reminder_day` so the Day 14 Milestone fires the dedicated persona nudge. (Do **not** reuse `keyword_remind_find` -that flag is for `keywords.find / content` prompts, not persona; conflating them was a past bug.)

**If the user wants help drafting:**
- Agent drafts based on `config.yaml ->keywords.content + brand + subreddits.target.primary + subreddits.target.secondary` + proxy geo + the user's stated product
- Show side-by-side with the template, user approves field-by-field (same pattern as `stage2-comment.md ->Placeholder auto-draft`)
- Agent NEVER silently writes persona values; every replacement needs explicit user ack

**brand_story is the highest-leverage field** -it's what makes or breaks Path B promo posts in Stage 3. Spending 10 minutes on this at Day 1 saves the user from scrambling at Day 29.

## Step 5.7 -Profile customization (avatar + bio)

**Why this matters**: a fresh Reddit profile with (a) the default generic avatar and (b) an empty bio is an instant "bot farm" signal -new-account farms don't bother customizing these because it takes 30 seconds per account and they cut corners. Real users ALWAYS set at least one of them within a few days of registering. Spending 2 minutes here on Day 1 significantly reduces "new-account-suspicious" AutoMod triggers in Days 15-29 when commenting starts.

Do these right after persona is written. Use the current `<run_session>` only if it is still active; otherwise open the same `browser_id` in a fresh `<run_session>`.

### 5.7a -Pick an avatar (free built-in)

Reddit lets you pick a free default avatar that's customizable. Navigate to the avatar editor:

```bash
browser-act --session <run_session> navigate https://www.reddit.com/user/<username>/avatar
browser-act --session <run_session> wait stable --timeout 20000
```

**Agent: read `browser-act state` to find the "Save" / "Apply" button** (the exact label varies per Reddit release). The page shows a builder UI with presets. Any non-default pick is better than the default. Options:

- **Quick path**: agent picks a preset style at random (if state output lists presets with idx), clicks it, then clicks Save
- **User-involved path**: tell the user "go pick an avatar in the open browser window, then reply 'done'"; on "done" continue

Either works. Just don't skip.

**Post-save error check**: same pattern as bio (5.7b) -after the Save click, `get markdown` and look for `"We had some issues saving your changes"` / similar. Settings modals on Reddit share one error banner; a rejected bio save or avatar save shows the same red banner at page top. If present ->shadow suspect or reCAPTCHA miss, handle per the bio flow above.

### 5.7b -Write a profile bio (persona-derived, 1-2 sentences)

Navigate to settings:

```bash
browser-act --session <run_session> navigate https://www.reddit.com/settings/profile
browser-act --session <run_session> wait stable --timeout 20000
browser-act --session <run_session> state
```

**Agent: find the "About description" button idx** (a row button with aria-label `Open modal to change setting: About description`). Click it to open the modal.

```bash
browser-act --session <run_session> click <about_btn_idx>
sleep 3
browser-act --session <run_session> state
```

**In the opened modal, state re-numbers to a small local range**; expect something like:

```
[1]<textarea id=innerTextArea maxlength=200 invalid=false required=false />
[2]<span class=character-count />   0/200
[3]<button class=button-primary invalid=false />   Save
[4]<button class=button-secondary invalid=false />   Cancel
```

**Critical: stay inside browser-act native commands.** The bio textarea is inside a modal, and a single combined fill can sometimes focus the modal backdrop. Use `state` ->`click <textarea_idx>` ->`input <textarea_idx> "..."` and verify visually. If browser-act cannot fill the field after one retry, use browser-act `remote-assist` or stop with a clear log.

```bash
browser-act --session <run_session> state
browser-act --session <run_session> click 1     # focus the textarea
sleep 1
browser-act --session <run_session> input 1 "<1-2 sentence bio>"
sleep 1
browser-act --session <run_session> state
# Verify visually: the character count should show N/200 matching the text length
browser-act --session <run_session> screenshot "<evidence>/bio-filled.png"
```

If the field still does not contain the text after one retry, hand the page to the user with `browser-act remote-assist --objective "Type the approved profile bio and click Save"` and continue after the user says "done". Do not use any alternate execution path.

Then click Save and **check for a server-side error banner** right afterwards:

```bash
browser-act --session <run_session> click 3     # Save
sleep 4
browser-act --session <run_session> get markdown
```

If markdown contains `"We had some issues saving your changes"` or similar error text ->the save was rejected by Reddit's server. Common causes:
- **Shadow-banned account**: Reddit silently rejects profile updates from shadow accounts. Surface to user: "Reddit refused to save bio -run r/ShadowBan verification (see `stage3-promote.md ->Weekly Shadowban Check`); if confirmed shadow, retire the account"
- **reCAPTCHA failure**: save requires a fresh token; try once more with 30s dwell in between
- **Connection / rate-limit**: retry after 60s; persistent ->`skip("profile_update_rejected")`

If no error banner ->save succeeded; navigate to `/user/<username>/` and verify the bio renders in the right sidebar.

Bio content rules:
- **1-2 short sentences max.** Long bios are suspicious on new accounts.
- **Use `persona.identity` as the anchor**; don't mention brand.
- **Casual lowercase / sentence fragments are fine.** Real Reddit bios are rarely polished.
- **Do NOT** include links, emojis, or self-promotion.

Agent drafts ->shows to user ->user confirms or edits ->agent types the final version via `browser-act input <bio_textarea_idx> "<text>"` ->click Save.

### 5.7c -Pick user flair in the target subs (optional, Stage 3 prep)

Some target subs require or reward user flair (e.g., `r/Entrepreneur` uses flair for role tags like "Solo" / "Founder"). For each sub in `subreddits.target.primary + subreddits.target.secondary` that supports flair:

```bash
browser-act --session <run_session> navigate https://www.reddit.com/r/<sub>/
# Find "Add user flair" / pencil-icon button via state ->click ->pick appropriate flair ->Save
```

Skip any sub that doesn't expose a flair picker. This is advisory, not mandatory.

### 5.7d -Mark the Profile Customization achievement as done

Record onboarding variables for Step 6:

```json
{
  "profile_customized_pending": true,
  "profile_customized_at_pending": "<ISO timestamp>"
}
```

Phase 2 pre-flight reads this field. If `false` after Day 7, surface a reminder ("This account still has the default avatar and an empty bio. Take 10 seconds to customize the profile; it significantly lowers the chance that Days 15+ comments get filtered."). After Day 14 still not done ->add `profile_customized == false` to the Stage 2 Persona Readiness Gate's soft-block list (not a hard stop; just include in the nudge).

### What this skill deliberately does NOT chase

These achievements require money / other-user action / artificial behavior -skill stays out:

- Reddit Premium / Gold purchase ($)
- Receiving awards (other-user dependent)
- NFT / Collectible Avatars ($)
- "Top 1% commenter" in a sub (requires heavy volume that trips anti-spam)
- Any achievement that asks the user to "share to social" externally

Stick to auto-unlocks from normal activity + Step 5.7a/b/c. Nothing more.

## Step 6 -Initialize progress.json

Copy `assets/progress.json.template` to `~/.reddit-warmup/<username>/progress.json`, fill based on Step 3/4 conclusions:

- `onboarding_date = today (account tz)`; `initial_day = 1` for a new account or the starting Day chosen in Step 4.1 for an existing account.
- `start_date = onboarding_date - (initial_day - 1) calendar days`. This is the workflow calendar anchor, not the Reddit registration date. For example, onboarding at Day 30 on 2026-11-04 stores 2026-10-06, so the next date computes Day 31.
- `current_day = initial_day` and `stage = <corresponding stage>` are initialization/display values only; later runs derive the day from the anchor.
- Also initialize `account_age_days` and `account_age_checked_on` from the real profile/registration evidence; the checked date is onboarding_date. Store `account_age_days_at_onboarding = 0` for an account just registered here; for an existing account, use the age actually read in Step 4.1. Do not infer Reddit age from the backdated workflow anchor. If age is unavailable, store null and re-read the profile before any age-gated action.
- Copy `env_migration_pending`, `migration_day_pending`, and `migration_clean_logins_pending` into their matching progress fields **after** loading template defaults; set `last_migration_scheduler_date = null`. Missing pending migration values for an existing account mean onboarding is incomplete, not a reason to assume migration is disabled.
- `week_start = this Monday (account tz)`
- `baseline_ip = baseline_ip_pending` and `baseline_ip_checked_at = now` if Step 2 captured an IP
- `baseline_timezone = baseline_timezone_pending` if Step 2 captured a proxy timezone
- `persona_defer_reminder_day = persona_defer_reminder_day_pending` if the user deferred persona setup
- `profile_customized = profile_customized_pending`, `profile_customized_at = profile_customized_at_pending` if Step 5.7 succeeded; otherwise leave template defaults
- Preserve all values collected above when applying the remaining template defaults. Never recopy the template over the populated progress object.

BrowserAct may close the runtime session after the flow. Do not store or depend on this setup `<run_session>`; the durable state is the configured `browser_id`.

`config.yaml` is still intentionally absent after Step 6. This prevents a half-finished onboarding from being routed into Phase 2 if the thread stops before approval policy and scheduler settings are collected.

## Step 7 -Detect scheduler timezone + tell user to wire the external scheduler

**Step 7.1 -Auto-detect and record `scheduler_timezone`:**

Detect the current machine's local timezone:
- Windows: `powershell -c "[TimeZoneInfo]::Local.Id"` ->map Windows ID to IANA (e.g. "China Standard Time" ->"Asia/Shanghai")
- macOS: read the `/etc/localtime` symlink and take the IANA name after `/zoneinfo/` (for example Asia/Shanghai). If unavailable, ask for the scheduler IANA timezone.
- Linux: `timedatectl show -p Timezone --value` when available, otherwise read `/etc/timezone`; validate the result as an IANA timezone.

Store the detected IANA zone as `config_pending.account.scheduler_timezone`. Then confirm in chat:

> Scheduler timezone auto-detected: **`<detected_tz>`**
> This is the machine timezone used for daily idempotency (has today's job already run?).
> **Different from `account.timezone` (`<account_tz>`) -that still controls account rhythm (current_day, Wednesday, week resets).**
> If the detected timezone is wrong, reply: `set scheduler_timezone <correct_tz> for <username>`

If detection fails, prompt: "Could not auto-detect machine timezone. Please provide the IANA timezone of the machine that will run the scheduler (e.g. Asia/Shanghai, America/New_York)." Store the user-provided value as `config_pending.account.scheduler_timezone`.

---

> Scheduler timezone recorded for `<username>`. State directory: `~/.reddit-warmup/<username>/`.
>
> One final initialization choice remains: approval policy (Step 7.5 below). After that, the account setup is complete.
>
> Scheduler preview: after Step 7.5 completes and `config.yaml` exists, wire an external scheduler (cron / Windows Task Scheduler / any scheduler) to trigger once per day with the message:
>
> `today's task - reddit warmup <username>`
>
> Recommended trigger time: once per day in the account's normal browsing window (avoid on-the-hour). Scheduler wiring details, timezone picking by proxy geo, and staggering across multiple accounts: see `scheduling.md`.
>
> For unattended schedulers, still set `REDDIT_WARMUP_UNATTENDED=1` so CAPTCHAs and other error-recovery prompts fail fast instead of hanging. Note: the flag does **not** bypass comment/brand approval. Manual-path batches stay in `pending_approval/` until the user replies or the 7-day stale cleanup removes them. The user can approve later with natural language such as `pick A`, `reply D`, `use the second one`, `skip`, or `make it shorter`; a clear pick immediately runs the browser publish flow. See `scheduling.md ->Unattended flag` and `approval-rules.md` ->Rules C3/C4/C6.

## Step 7.5 -30-Day Plan Preview + Approval Policy Selection

Show the complete plan and collect the approval policy choice before wrapping up.

### 30-Day Plan Preview

Send this to the user in chat:

```
Calendar: <username> -30-Day Warmup Plan
Start date: <today>

Phase 1 -Lurk (Day 2-14)
Browse + upvote only, no comments or posts.
Goals: 50-80 upvotes, 3 warmup subreddits plus 2 primary target subreddits by Day 14.
  Day 2-3: Browse only (no upvotes yet)
  Day 4+:  Start upvoting (max 2-3 posts/sub/day, 20-45s gaps)
  Day 4+:  Gradually subscribe to warmup subs (1 sub by Day 6, 2 by Day 10, 3 by Day 14)

Warning:  Day 14 reminder: You'll receive a notification before entering the Comment Phase.

Phase 2 -Comment (Day 15-29)
AI-generated natural comments + 1 practice post/week. No brand mentions yet.
Goals: Build comment karma, reach account age >=30 days.
  Day 15-19: 1 comment/day (skip Day 17 + 19 -irregular rhythm)
  Day 20-21: 2 comments/day in warmup subs
  Day 22-25: 3 comments/day (2 warmup + 1 target)
  Day 26-29: 4 comments/day (2 warmup + 2 target)
  Every Wednesday: 1 practice post (text-only, Path A, no brand terms)

Phase 3 -Brand Promotion (Day 30+)
Entry gate: account age >=30 days AND comment karma >=20 (both required).
  2-4 comments/day, up to 2 posts/week (1 help/share + 1 promotional)
  Brand-bearing content (D variants, Path B posts) always requires your explicit approval.

Warning:  Day 29 reminder: You'll be offered the choice to enter brand phase.
```

### Approval Policy Choice

```
How would you like comments and posts to be handled?

A. Manual Approval (all require your review)
   Every comment/post shows you A/B/C variants. You can reply naturally with
   A / B / C / D / skip, "use D", "pick the second one", or a revision request.
   A clear pick immediately continues into publish + verification; the approval
   checkpoint alone is not completion. You have full control.
   Best for: users who want to review every piece of content.

B. Agent Auto-Execute (fully hands-off)
   Agent handles everything -comments, posts, and brand-bearing content alike.
   Brand Exposure check runs but is logged silently (no chat interruption).
   Sub verification for promotional posts still runs (blocked sub = no post).
   You see only the daily summary report.
   Best for: fully hands-off operation; no approvals required.

C. Stage 2 Auto + Stage 3 Brand Manual (hybrid)
   Stage 2 (Days 15-29) comments are auto-selected by the agent.
   When Stage 3 starts, brand-bearing content (D variants, Path B posts) requires
   your approval. Non-brand comments in Stage 3 continue auto.
   Best for: automated warmup with hands-on control when promotion begins.

Reply A, B, or C.
(You can change this any time: "set approval to manual/auto/auto_stage2 for <username>")
```

**Agent: wait for the user's reply (A / B / C), then set `config_pending.approval_policy`:**

| User picks | Pending value |
|---|---|
| A | `approval_policy: "manual"` |
| B | `approval_policy: "auto"` |
| C | `approval_policy: "auto_stage2"` |

**Important -Day 14 notification preview (tell the user what to expect):**

If the user chose A or C (any manual approval mode), add this note:

> "When Phase 2 comments are generated (starting Day 15), you'll see comment variants in this chat window. There is no fixed approval window. You can reply naturally at any time with A / B / C / D / skip, and a clear pick immediately runs the browser publish flow for that stored batch. Old pending batches are only cleaned by the 7-day stale cleanup."

After setting the pending approval policy, write the final `~/.reddit-warmup/<username>/config.yaml` in one pass using `assets/config.yaml.template` and all collected `config_pending` values:

- `account.username`
- `account.browser_id`
- `account.proxy`
- `account.timezone`
- `account.audience_tz`
- `account.schedule_profile` if collected
- `account.scheduler_timezone`
- `subreddits.warmup`
- `subreddits.target.primary`
- `subreddits.target.secondary`
- `keywords.find`
- `keywords.content`
- `keywords.brand`
- `persona_file`
- `post_options`
- `approval_policy`

If the final write fails, onboarding is **not complete**. Tell the user the config write failed and do not instruct them to start the scheduler. Only after the final `config.yaml` exists should future triggers route to Phase 2.

After writing the final config, send the final setup confirmation:

```text
<username> initialization complete.
State directory: ~/.reddit-warmup/<username>/
Browser profile: <browser_id>
Approval policy: <approval_policy>

Next daily trigger:
today's task - reddit warmup <username>
```
