# Login Verification -Step 0 + Four Layers

**Run at the start of every Phase 2 run, before any write action (comment / post / upvote / subscribe).** Session cookies expire (7-14 days typical), and "homepage loads" is not the same as "logged in" -Reddit serves most home-page content to anonymous users, so single-point checks mislead the agent.

**Rule:** Step 0 (authoritative username resolution) must run first, then all four layers must pass. If Step 0 or any layer fails or is uncertain, skip all write actions for the run.

Step 0 is the prerequisite for Layer 4 -Layer 4's "username matches" check consumes what Step 0 returned. The four layers keep their names (no renumbering) so daily reports / log fields stay backward-compatible.

---

## Why four layers (past mistakes)

| Wrong judgment | Reality | Fix |
|---|---|---|
| "Home page has posts = logged in" | Home feed serves anonymous users too | Must visit inbox or prefs; home feed doesn't count |
| "Page has 'Log In' button = logged out" | Logged-in users also see a "Switch account" link that markdown-dumps to "Log in" | Four-layer check, ignore home button text |
| "Last task succeeded, session must still be good" | Cookies expire mid-week | Every run re-verifies, never cache |
| "Can visit /user/\<username\> = logged in" | User profiles are public | User profile is NOT a login signal |
| "get markdown returned content = page is fine" | Login walls are also markdown content | Must check both "logged-in element present" AND "login wall absent" |
| "Username appears in inbox = logged in" | New accounts have empty inboxes with no username displayed | Username check uses prefs page, not inbox |

---

## Step 0 + four layers -via `browser-act`

### Step 0 -Resolve the logged-in username authoritatively

**Non-negotiable:** the ONLY authoritative source of "who is this browser logged in as" is Reddit's `/user/me/` 302 redirect. Do NOT infer from:
- `/user/<name>/` anchors on the home feed (those are recommended-post authors, not the viewer)
- component attributes on arbitrary pages
- Avatar `alt` text or tooltip
- Old-reddit username header (not all profiles use it)

```bash
browser-act --session <run_session> navigate https://www.reddit.com/user/me/
browser-act --session <run_session> wait stable --timeout 30000
browser-act --session <run_session> state       # read the current URL from the state page header/current-page line
PAGE_TITLE=$(browser-act --session <run_session> get title 2>&1 | tail -1)
```

Parse the resolved URL shown by `browser-act state` into one of:

| URL pattern | Meaning |
|---|---|
| Matches `^https?://(?:www|old|new)\.reddit\.com/user/([a-zA-Z0-9_-]+)/?` | Reddit redirected to `/user/<captured_name>/` -authoritative, `current_username = <captured_name>` |
| Contains `/login` or `/register` | Not authenticated. Skip Steps 1-, go directly to re-login flow |
| Anything else (interstitial / 503 / ad wall / age-gate) | `inconclusive`. Retry navigate once; still inconclusive ->`uncertain`, abort writes |

**Carry the resolved `username` forward as `<current_username>` for the rest of this run** -this is the value used by `/user/<current_username>/comments/` and `/user/<current_username>/submitted/` navigation in `comment-publishing.md` + `image-posting.md`. Do not re-derive it later from home-page links or profile snippets.

### Step 1 -Visit two auth-gated endpoints

```bash
browser-act --session <run_session> navigate https://www.reddit.com/message/inbox/
browser-act --session <run_session> wait stable --timeout 30000
browser-act --session <run_session> get title       # record as inbox_title
browser-act --session <run_session> get markdown    # record as inbox_md

browser-act --session <run_session> navigate https://www.reddit.com/prefs/
browser-act --session <run_session> wait stable --timeout 30000
browser-act --session <run_session> get title       # record as prefs_title
browser-act --session <run_session> get markdown    # record as prefs_md
```

The agent keeps the outputs in its working memory (no `/tmp` files).

### Step 2 -Evaluate the four layers against the two markdowns

The agent checks, in order:

**Layer 1 -URL not redirected to login.** After each `navigate`, if `get title` returns "Log In" / "Sign Up" / "Reddit -Log In", OR the markdown's first heading is the login form, the page was redirected. ->`logged_out`.

**Layer 2 -Login-wall phrases absent.** Scan both `inbox_md` and `prefs_md` (case-insensitive) for any of:
- "log in to reddit"
- "sign up to reddit"
- "log in to continue"
- "please log in"
- "you need to be logged in"

Any match ->`logged_out` with reason naming which page and marker.

**Layer 3 -Logged-in element present on each page.**
- `inbox_md` must contain one of: "inbox", "messages", "no new messages"
- `prefs_md` must contain one of: "preferences", "content preferences", "email", "notifications"

Missing ->`uncertain` (page didn't load fully, not necessarily logged out).

**Layer 4 -Step 0 username matches the expected account.** Compare the `<captured_name>` parsed from `/user/me/` redirect URL (Step 0) against the expected account -in Phase 2 this is `config.yaml ->account.username`; in Phase 1 Step 3B (old-account takeover) this is the username the user just told us.

- Match ->`logged_in`
- Mismatch ->`uncertain` ("browser profile is logged into a DIFFERENT account than expected; refuse to proceed -writing under the wrong account is worse than not writing at all")
- Step 0's URL did not match a `/user/<name>/` pattern ->already short-circuited in Step 0 (login/register ->re-login flow; inconclusive ->retry once ->uncertain). Layer 4 only runs when Step 0 resolved a concrete username.

This replaces the old "scan prefs_md for username literal" approach -that text-search was unreliable on new-reddit UI where prefs doesn't always surface the username in markdown. `/user/me/` redirect is the only tamper-proof signal.

Only when all four pass ->`logged_in`.

---

## Handling each outcome

| Result | Action |
|--------|--------|
| `logged_in` | Continue the run |
| `logged_out` | Attempt re-login (next section). If re-login fails, abort the run; daily report flags `login_failed` |
| `uncertain` | **Never** continue to write actions. Take a screenshot to `~/.reddit-warmup/<username>/evidence/<ts>-login-uncertain.png`, notify user for manual check. Common causes: Reddit 503, network blip, browser profile loaded the wrong account |

---

## Re-login flow (logged_out case)

```bash
browser-act --session <run_session> navigate https://www.reddit.com/login/
browser-act --session <run_session> wait stable
browser-act --session <run_session> remote-assist --objective "Log in to Reddit as <username>. Do not change accounts."
```

After sending the assist link, do not run browser-act commands while the user is operating the page. Wait until the user replies "done", then continue:

```bash
browser-act --session <run_session> wait stable
browser-act --session <run_session> get markdown
```

Scan the markdown:
- Contains "incorrect" / "wrong password" / "locked" ->stop, tell the user credentials are bad.
- Contains "captcha" / "prove your humanity" / "unusual activity" / "verify" ->use the unified 3-tier ladder (Tier 1: auto-solve via current browser-act CAPTCHA command -e.g. `solve-captcha` -up to 2 attempts; Tier 2: browser handover via current browser-act user-assist command -e.g. `remote-assist --objective "..."`; Tier 3: interactive wait / unattended abort + `daily_skip_reason: "captcha_on_relogin"`). Full rules + command-name fallback in `stages.md ->Rate Limit & CAPTCHA Rules`; decision tree in `SKILL.md ->When to ask the user for help`.

Otherwise re-run the full verification (Step 0 + four layers). If all pass now, continue the run.

---

## Log entry

Every verification run writes:

```json
{"timestamp": "<ISO+offset>",
 "type": "login_check",
 "account_day": <N>,
 "ip": "<from ipinfo if recorded this run>",
 "run_session_id": "<run_session>",
 "url_confirmed": "<prefs URL observed after navigate>",
 "page_title": "<prefs get title>",
 "result": "logged_in | logged_out | uncertain",
 "layers_passed": ["url_ok", "no_login_wall", "inbox_content_ok", "prefs_content_ok", "username_match"]}
```

Update `progress.json.last_login_verified_at` on every `logged_in` result. If > 7 days since the last successful verification (every recent run failed), warn the user that stored credentials may be stale.



