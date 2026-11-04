# browser-act Rules + Interaction Patterns

## Execution Tool Boundary

All Reddit-facing execution must stay inside `browser-act` CLI.

Allowed browser/page/network primitives are only browser-act subcommands such as `browser open`, `navigate`, `wait stable`, `state`, `get markdown`, `get title`, `click`, `input`, `upload`, `scrollintoview`, `network`, `screenshot`, `solve-captcha`, and `remote-assist`.

If command usage or availability is uncertain, refresh the BrowserAct runtime guide with `browser-act get-skills core --skill-version 2.0.2`. Do not inspect, install, or try another browser execution tool.

Do not use any alternate execution method. If browser-act returns an error, times out, or cannot find an element, re-read browser-act `state`, retry with browser-act primitives, use browser-act `remote-assist`, skip, or stop with a clear log.

Local state files are the only non-browser exception: use the host agent's normal local file read/write/list capabilities for `~/.reddit-warmup/<username>/` files. These file operations do not replace browser verification.

**Load this file at the start of every Phase 2 run** (the first thing after Phase Router confirms a Phase 2 context).

---

## Important: No Screenshot = No Execution

**Every write to `activity_log.jsonl` must be preceded by actually opening the browser and taking a screenshot.**

**It is FORBIDDEN** to skip actual browser operations based on historical `activity_log`, IP type, proxy geo, or any "I'll infer what the result would be" guess -and then fabricate log entries.

- Agent sees `ip_blocked` in historical logs ->does NOT mean today is also blocked; must actually open the browser and try
- Agent sees the proxy is Cogent / AWS / DigitalOcean ->does NOT mean Reddit will reject it; must actually load a page once
- Previous run succeeded ->does NOT mean login will work this time; re-run the four-layer login verification every time (see `login-verification.md`)
- Before writing any log entry, there must be a corresponding `browser-act screenshot` output, `browser-act get markdown/title` real response

---

## Must Use Configured Browser Profile + Headed Mode

**Before any browser operation, read `account.browser_id` from `~/.reddit-warmup/<username>/config.yaml` and open a fresh runtime session in headed mode with that browser profile.**

```bash
# Correct way to start a browser flow (must include --headed)
RUN_SESSION="reddit-warmup-<username>-<purpose>-<ts>"
browser-act --session "$RUN_SESSION" browser open --headed <browser_id_from_config> <url>
```

`<run_session>` is a temporary command channel for the current browser-act flow. It is not durable state and must not be used as the way to find pending approvals later.

### Headed mode requirements

- Must include the `--headed` flag
- NOMust NOT use headless mode -headless has detectable fingerprint characteristics

### Browser ID requirements

- NOMust NOT use any other browser_id
- NOMust NOT create a new browser profile on the fly (except during Phase 1 Step 2 initialization)
- NOMust NOT open the browser without specifying a browser_id

### Runtime session rule

`account.browser_id` is the persistent browser profile. The browser-act `--session` value is per-flow runtime state; browser-act may close it after a flow completes. Therefore all durable workflow state must be stored in local files and keyed by `username`, `batch_id`, and `browser_id`, never by browser-act session.

- Start every independent flow by creating a fresh `<run_session>` and opening the same configured browser profile:
  ```bash
  browser-act --session "$RUN_SESSION" browser open --headed <browser_id_from_config> <target_url>
  ```
- Reuse `<run_session>` only inside the same active browser-act flow.
- Do not try to recover approval context from `session_id`; recover it from `pending_approval/<batch_id>/meta.json`, `config.yaml`, and the Approval Batch anchor plus item number shown in chat.
- Do not create a new browser profile, switch `browser_id`, or skip the approved publish just because a previous session is gone.
- After opening the profile in the fresh runtime session, run the authoritative `/user/me/` login verification before any comment/post submission.
- If `/user/me/` redirects to `/login` or a different account, stop and ask the user to log in; this is an authentication failure, not a session-recovery failure.
- Do not run the Avatar Menu Health Check inside Hot Approval / approval-publish execution. That check belongs to the scheduled daily preflight only; a user-approved publish resumes from the stored batch and should not become a second account-health audit.

### Mandatory verification before starting a task

Agent reads `~/.reddit-warmup/<username>/config.yaml` with its normal local-file capability and retrieves `account.browser_id`.
- Field empty / missing ->**stop immediately and notify the user**; don't create or pick a browser on your own.
- Field populated ->clearly tell the user which `browser_id` will be used this run, create a fresh `<run_session>`, then run `browser-act browser open`.

### Account-to-browser binding

One account is permanently bound to one browser profile + one proxy. Changing either counts as "device switch" and must go through the restricted migration runs in `references/migration.md` until three consecutive clean daily runs have completed; cannot enter the normal schedule directly.

---

##  Authoritative Source for Logged-in Username

**The only authoritative source for Reddit's currently logged-in username is the `/user/me/` 302 redirect.**

```bash
browser-act --session <run_session> navigate https://www.reddit.com/user/me/
browser-act --session <run_session> wait stable --timeout 30000
browser-act --session <run_session> state
PAGE_TITLE=$(browser-act --session <run_session> get title 2>&1 | tail -1)
```

Before accepting a user URL, inspect the page text: Reddit network-security blocks or challenges mean blocked/inconclusive; an ordinary login/register page or login wall means logged_out and uses login-verification.md re-login flow. None proves authentication. The unresolved `/user/me/` alias is not a username: explicitly reject captured `me` (case-insensitive). If the route does not resolve to a concrete account, retry once and then stop writes for user-directed recovery; do not switch account/profile/proxy automatically.

Read the current URL from the `browser-act state` page header / current-page line. Parse that resolved URL:
- Matches `^https?://(?:www|old|new)\.reddit\.com/user/([a-zA-Z0-9_-]+)/?` ->authenticated as captured name
- Contains `/login` or `/register` ->not logged in
- Anything else ->inconclusive; do NOT proceed, fail login-verification

**Forbidden inference methods (all known to be unreliable):**
- Any `/user/<name>/` link in the home-page state output -contaminated by recommended-post author bylines
- component attributes -only appear on specific components, unstable
- Avatar `alt` / `title` / nearby tooltips
- Top-right "Expand user menu" button's child text -often empty or hidden
- Searching for `u/<name>` literals in `get markdown` output -new prefs pages may not render it

**Why:** Reddit's home feed renders `/user/<author>/` links in every post card byline. Profile-link searches return random recommended-post authors -you cannot distinguish the logged-in account. `/user/me/` is Reddit's official "who is logged in" route.

**Only exception:** When `config.yaml ->account.username` is explicit, you can use it directly, but you **must** verify once via this authoritative source.

---

##  Rule-Reading Gate

**Many subs have karma / account-age / no-self-promo / flair / length restrictions. AutoMod silently removes rule-breaking content and accumulates strikes toward shadowban. Verify rules before any write action.**

### Per-action requirements

| Action | Requirement |
|--------|-------------|
| **Subscribe** | None. Low-risk signal |
| **Upvote** | None for individual upvotes. See "Upvoting newly-discovered subs" below |
| **Comment** / **Reply** / **Inbox reply** / **Camping reply** | Valid `sub_profiles.json[<sub>]` entry with `recon_at` within 14 days, ALL gate checks pass |
| **Post (Path A)** | Same as comment + sub's `restrictions` match post shape (text/image/length/flair/weekday) |
| **Post (Path B promotional)** | Same as Path A + `restrictions.forbids_self_promo != true` + specialized-sub verdict passes |

### Gate checks (all must pass before any comment/post)

For the target sub, load `sub_profiles.json[<sub>]` and verify in order:

1. **Recon fresh** -`recon_at` within 14 days. Stale or missing ->run recon first (`stage2-comment.md` ->Subreddit Risk Profiling).
2. **Rules non-empty** -`rules_summary` and `restrictions` must be populated. Empty ->re-run recon, don't guess.
3. **Karma gate** -`karma_gate <= own comment_karma`. Violated ->pick another sub; log `skip("karma_gate")`.
4. **Age gate** -`age_gate_days <= own account_age_days`. Violated ->pick another sub; log `skip("age_gate")`.
5. **Content-shape restrictions** -action must match the sub's `restrictions` table:
   - Promotional + `forbids_self_promo: true` ->skip; log `skip("sub_forbids_self_promo")`
   - Text post + `forbids_text_posts: true` ->skip
   - Image post + `forbids_image_posts: true` ->fall back to text
   - URL in post body + `forbids_urls_in_posts: true` ->rewrite without URL or skip
   - `requires_post_flair: true` AND no flair picked ->ask user first
   - Draft length outside `minimum_post_length_words` / `maximum_post_length_words` ->regenerate
6. **De-facto floor** -`median_recent_poster_karma`. For promotional actions, apply Stage 3 Specialized-sub check. For regular comments, informational only.

**If any mandatory gate fails ->pick another sub or skip today. Never write under a failed gate.**

### Recon routine (run on demand)

Full procedure in `stage2-comment.md` ->Subreddit Risk Profiling. Summary: `navigate /r/<sub>/about/rules + /wiki/index + /new + /top + /about/moderators` via browser-act, parse into `sub_profiles.json` schema.

### Upvoting newly-discovered subs

Stage 1 upvotes don't need the full gate check, BUT before upvoting in a new sub, **read the sidebar rules once** (`navigate /r/<sub>/about/rules` ->`get markdown`) to catch obvious red flags. On the first day the account plans to **comment** in that sub, run the full recon routine above.

---

## How browser-act CLI Interaction Works -Agent-driven idx Selection

**Reddit's UI varies across subs / post types / A/B tests.** Do NOT write rigid regex patterns to extract element indices from `browser-act state` output.

1. Run `browser-act state`.
2. **Read the output yourself** -find the element by its visible label + surrounding context.
3. Call `browser-act click <idx>`.

Example -`Upvote` button:
```
*[31]<button class=group button invalid=false pressed=false />
    Upvote
```
The idx is `31`. On another post it might be `32` or `45`. **Your job is to recognize "the button labeled Upvote inside the post's action bar"** and emit its idx.

Each reference file describes elements in semantic terms; you read state and pick the right idx. When a reference gives an example state line, treat it as a **description of what to look for**, not a locked-in pattern.

### When `browser-act input <idx>` silently fails

For fields inside Reddit's settings modals (About description / Display name / Banner link URL / social link fields), the combined `input` command's internal click step sometimes focuses the modal backdrop. The command returns success but text never lands.

**Workaround**: stay inside browser-act native controls. Re-read the modal state, click the field itself, then use `input`; verify with state, screenshot, or the visible character-count/save-state. If browser-act cannot fill the field, use browser-act `remote-assist` or stop with a clear log.

```bash
browser-act --session <s> state
browser-act --session <s> click <field_idx>
sleep 1
browser-act --session <s> input <field_idx> "<text>"
sleep 1
browser-act --session <s> state
browser-act --session <s> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-field-filled.png
```

`input <idx> "<text>"` is the correct typing primitive. If the value still does not land after one click+input retry, use `browser-act remote-assist --objective "Type the profile field and click Save"` or skip with a clear reason. This split is NOT needed for Lexical contenteditable, title textarea, or URL/Link fields on `/submit`.

---

## When to Ask the User for Help

**Intent-based policy: describe the intent, pick the right browser-act command at runtime, fall back to chat if the command doesn't exist.**

```
Agent encounters something it can't resolve alone
- Page-level block (CAPTCHA / login challenge / 2FA / verification)?
  - CAPTCHA specifically:
    - Tier 1: try `browser-act solve-captcha` (auto)
    - Tier 2: hand over via `browser-act remote-assist --objective "..."`
  - Login / 2FA / email return / other verification:
    - Skip Tier 1. Go directly to `browser-act remote-assist --objective "..."`
- Content decision in agent memory?
  - Examples: comment draft, persona fill-in, sub shortlist.
  - Show it in chat and ask for A/B/C/confirm/skip.
  - No browser handover needed.
- Operational question the agent cannot answer?
  - Examples: unexpected UI change, unknown sub rule, ambiguous mod message.
  - Describe the situation and options in chat, then ask how to proceed.
  - Agent waits; it does not improvise.
```

### Robustness when commands rename

browser-act CLI commands may be renamed in future versions. The skill does NOT hard-depend on any specific command name:

1. All user-assist references describe the **intent** ("hand page control to the user").
2. Current command names are listed as **examples**, not contracts.
3. **Fallback hierarchy when a named command is missing**: check `browser-act --help` for a semantic match; if nothing matches, explain in chat and ask user to operate manually + reply "done".

---

## UI Drift Fallback

Reddit's frontend changes often. When a selector stops working:

1. Retry once after `browser-act wait stable` + a short delay.
2. Fall back to `browser-act state` -find the target by role / aria-label / visible text.
3. Fall back to `browser-act get markdown` for read-only ops.
4. All three fail ->log `skip` entry with `reason: "dom_drift"` + `detail: "<operation>"`, close session, move on.

Don't retry beyond this -drift is a skill-level issue, not recoverable mid-run.



