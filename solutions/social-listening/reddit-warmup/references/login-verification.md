# Login Verification -Step 0 + Four Layers

**Run at the start of every Phase 2 run, before any write action (comment / post / upvote / subscribe).** Session cookies expire (7-14 days typical), and "homepage loads" is not the same as "logged in" -Reddit serves most home-page content to anonymous users, so single-point checks mislead the agent.

**Rule:** Step 0 (authoritative username resolution) must run first, then all four layers must pass. If Step 0 or any layer fails or is uncertain, skip all write actions for the run.

Step 0 is the prerequisite for Layer 4 -Layer 4's "username matches" check consumes what Step 0 returned. The four layers keep their names (no renumbering) so daily reports / log fields stay backward-compatible.

---

## Why four layers (past mistakes)

| Wrong judgment | Reality | Fix |
|---|---|---|
| "Home page has posts = logged in" | Home feed serves anonymous users too | Must verify notifications and account settings; home feed alone does not count |
| "Page has 'Log In' button = logged out" | Logged-in users also see a "Switch account" link that markdown-dumps to "Log in" | Four-layer check, ignore home button text |
| "Last task succeeded, session must still be good" | Cookies expire mid-week | Every run re-verifies, never cache |
| "Can visit /user/\<username\> = logged in" | User profiles are public | User profile is NOT a login signal |
| "get markdown returned content = page is fine" | Login walls are also markdown content | Must check both "logged-in element present" AND "login wall absent" |
| "Username appears in inbox = logged in" | New accounts have empty inboxes with no username displayed | Username check uses the resolved self-profile URL, not inbox text |

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

First read both the current URL and page text. If Reddit shows “blocked by network security” or a challenge/interstitial, classify the result as blocked/inconclusive before accepting any user URL. A login/register page or login wall without a security block is logged_out and uses the re-login flow below. A URL still ending in `/user/me/` is the unresolved self alias, not a logged-in username. Never accept `me` as `current_username`, even when the generic user-path pattern matches. Retry once after checking the page; persistent blockage stops all account write actions and requires the user to restore access. Do not create a replacement account or change the proxy as an automatic recovery.

Parse the resolved URL shown by `browser-act state` into one of:

| URL pattern | Meaning |
|---|---|
| Matches `^https?://(?:www|old|new)\.reddit\.com/user/([a-zA-Z0-9_-]+)/?` | Reddit redirected to `/user/<captured_name>/` -authoritative, `current_username = <captured_name>` |
| Contains `/login` or `/register` | Not authenticated. Skip Steps 1-, go directly to re-login flow |
| Anything else (interstitial / 503 / ad wall / age-gate) | `inconclusive`. Retry navigate once; still inconclusive ->`uncertain`, abort writes |

**Carry the resolved `username` forward as `<current_username>` for the rest of this run** -this is the value used by `/user/<current_username>/comments/` and `/user/<current_username>/submitted/` navigation in `comment-publishing.md` + `image-posting.md`. Do not re-derive it later from home-page links or profile snippets.

### Step 1 -Visit two auth-gated pages

Use the notifications page and the current account-settings page. Waits are advisory on Reddit's SPA: if `wait stable` times out, inspect `state` before deciding; a timeout alone does not mean logged_out.

```bash
browser-act --session <run_session> navigate https://www.reddit.com/notifications/
browser-act --session <run_session> wait stable --timeout 10000
browser-act --session <run_session> state
browser-act --session <run_session> get markdown

browser-act --session <run_session> navigate https://www.reddit.com/settings/account
browser-act --session <run_session> wait stable --timeout 10000
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
```

Keep the observed URLs, visible states, and relevant page content in working memory. Do not copy email addresses, phone numbers, birthday, or other settings values into logs. The legacy `/message/inbox/` is an archived private-message view, not the current notification source; its iframe content may appear in `state` but be absent from top-document markdown.

### Step 2 -Evaluate the four layers

**Layer 1 -Correct resolved page, no security block.** Confirm each current URL remains the intended notifications/settings page after redirects. A concrete login/register URL is logged_out; a network-security block, challenge, inaccessible page, or unexpected redirect is uncertain. Never accept a navigation shell by itself.

**Layer 2 -No visible authentication wall.** Inspect current visible `state` for an actual login form or auth-required page, such as username/password inputs plus a login submit action, or an auth-required main heading. A login wall must belong to the active page, not hidden modal/template content. Do not run a global substring test over all markdown: account settings can legitimately say “Connect to log in to Reddit with your Google account”, and global navigation/templates can contain login words while authenticated. Such help text is not a login wall. If page visibility is ambiguous, use a screenshot/current main content once; unresolved ambiguity means uncertain, never success.

**Layer 3 -Account-specific page content is present.**
- Notifications: visible Notifications heading plus actual activity rows or an explicit empty state such as “You don't have any activity yet”. The global “Open inbox” header link alone does not pass.
- Account settings: visible Settings/Account page with actual account-setting controls, such as the Email address/Password change buttons. Do not count generic sidebar/navigation “Email” or “Notifications” text as settings content. Do not change any setting during verification.

If either page lacks its own expected content after one state refresh, mark uncertain and stop writes.

**Layer 4 -Step 0 username matches the expected account.** Compare the `<captured_name>` parsed from `/user/me/` redirect URL (Step 0) against the expected account -in Phase 2 this is `config.yaml ->account.username`; in Phase 1 Step 3B (old-account takeover) this is the username the user just told us.

- Match ->`logged_in`
- Mismatch ->`uncertain` ("browser profile is logged into a DIFFERENT account than expected; refuse to proceed -writing under the wrong account is worse than not writing at all")
- Step 0's URL did not match a `/user/<name>/` pattern ->already short-circuited in Step 0 (login/register ->re-login flow; inconclusive ->retry once ->uncertain). Layer 4 only runs when Step 0 resolved a concrete username.

Do not scan settings markdown for the username literal; the rendered settings page may not expose it. `/user/me/` redirect is the only tamper-proof signal.

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
 "url_confirmed": "<account-settings URL observed after navigate>",
 "page_title": "<account-settings page title>",
 "result": "logged_in | logged_out | uncertain",
 "layers_passed": ["url_ok", "no_visible_login_wall", "notifications_content_ok", "account_settings_content_ok", "username_match"]}
```

Update `progress.json.last_login_verified_at` on every `logged_in` result. If > 7 days since the last successful verification (every recent run failed), warn the user that stored credentials may be stale.



