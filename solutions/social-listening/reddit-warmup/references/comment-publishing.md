# Publishing a Comment -Pure browser-act CLI Flow

All comment publishing uses **`browser-act` CLI native commands** as the only execution path. No alternate execution path is allowed. The primitives: `navigate` / `wait stable` / `scrollintoview` / `state` / `click <idx>` / `input <idx> "text"` / `network requests` / `get markdown` / `get title` / `screenshot`.

**Four browser-act behaviors to know:**
- `browser-act input <idx> "text"` **works on Reddit's Lexical contenteditable** because browser-act sends native input that Reddit accepts into its editor state.
- `browser-act click <idx>` produces the real browser click behavior Reddit expects. Do not replace it with any other click path.
- `browser-act state` **enumerates Reddit's nested controls** -including `#submit-post-button`'s inner button for posts. No alternate execution path is needed.
- **`browser-act wait stable` frequently times out on Reddit's SPA** (exit code 1, "Timed out waiting for page readiness"). This is **non-fatal** -Reddit's new UI never fires a clean load-complete signal. Always proceed to the next command regardless of the exit code.
- Every action shows up in the headed browser window; UI drift is easy to spot.

**Agent-driven idx selection:** Reddit's UI varies across subs / A/B tests. Don't write regex to extract indices -read `state` output and pick the right idx by semantic match. Examples below show what the state lines typically look like; treat them as descriptions, not locked-in patterns.

---

## Inputs

- `<username>` -Reddit account
- `<browser_id>` -persistent browser profile from `config.yaml`
- `<run_session>` -temporary browser-act session for this browser flow; never use it as durable state
- `<current_username>` -logged-in username (from Phase 2 login-verification)
- `<post_url>` -canonical `/r/<sub>/comments/<id>/<slug>/` form; never a `/submit/` URL
- `<text>` -the picked comment variant
- `<parent_comment_id>` -optional `t1_xxxx` for nested reply

---

## Standard flow -top-level comment

### 1. Navigate + real-reader dwell

Every independent comment-publishing flow starts from a fresh `<run_session>` unless `approval-rules.md` Step 3 has already opened and verified one in the same active flow.

```bash
browser-act --session <run_session> browser open --headed <browser_id> <post_url>
browser-act --session <run_session> wait stable --timeout 10000
```

If `approval-rules.md` Step 3 already opened and verified `<run_session>`, use `navigate <post_url>` inside that same active flow instead of opening a second tab. Never depend on a previous flow's session still existing. The durable recovery key is `browser_id`.

Continue from here regardless of entry form:
```bash
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-before-comment.png

# Dwell 4-7s "reading title + body" on the target page.
sleep $((RANDOM % 4 + 4))
browser-act --session <run_session> scroll down --amount 2
sleep $((RANDOM % 4 + 3))    # 3-6s reading top comments
```

`wait stable` is advisory on Reddit's SPA. If it times out, continue to `state` / markdown instead of retrying long waits.

### 1a. Thread-page guard -never comment from `/submit/`

Before opening the composer, prove the browser is still on the target Reddit thread:

```bash
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
```

Read the current URL from the `state` page header / current-page line.

Proceed only when all hold:
- Current URL is a Reddit comments thread matching `/r/<sub>/comments/<post_id>/...` or a comment permalink under that same post.
- Current URL does **not** contain `/submit/`.
- Page title / markdown belongs to the target post, not a "Create post" / submission form page.
- State shows a comment composer path, not a post composer path.

If the browser is on `/submit/`, a Create Post page, or any non-thread page:
1. Navigate back to the original `<post_url>`.
2. Run a short `wait stable --timeout 10000` once, then re-run this guard.
3. If it still does not resolve to the target thread, stop and log `skip("wrong_page_submit_misdirect")`.

Do not click any submit button until this guard passes. A write action on `/submit/` is a post attempt, not a comment attempt.

### 2. Pre-flight -is the post commentable?

```bash
browser-act --session <run_session> get markdown
```

**Agent: read the markdown.** If any of these specific Reddit banners are present, log skip and stop:

- `"Sorry, this post was removed by Reddit's filters"` ->`skip("parent_post_removed")`
- `"This post was removed by moderators"` ->`skip("parent_post_removed")`
- `"This post is locked"` / `"Comments are locked"` ->`skip("post_locked")`
- `"you are doing that too much"` / `"Rate limit exceeded"` ->`skip("rate_limit_today")`
- `"your session has expired"` / `"session has expired"` / `"session timed out"` / localized session-expiry equivalents ->**do NOT skip** -`browser-act reload` + `wait stable --timeout 15000`, then re-run Step 2 once. If the banner persists after reload ->`skip("session_expiry")`. This is a frontend hydration issue, not a rate-limit or removal signal; reloading recovers it without losing the target post.

Match whole phrases -don't match loose `"removed by"` or `"locked"` that appear in sidebar rules text.

### 3. Rate-limit floor

Read `progress.json.last_publish_at`. If `now - last_publish_at < 90s`, sleep the remainder.

### 4. Open the composer

```bash
browser-act --session <run_session> scrollintoview --selector "comment-composer-host"
sleep 2
browser-act --session <run_session> state
```

**Agent: find the composer trigger in state.** It's a collapsed textarea, typically:

```
*[33]<textarea id=innerTextArea placeholder=Join the conversation ...>
```

Click it to expand ->the Lexical editor mounts:

```bash
browser-act --session <run_session> click <trigger_idx>
sleep $((RANDOM % 3 + 2))   # 2-5s for Lexical to mount
browser-act --session <run_session> state
```

**Agent: now find the Lexical editor idx.** It's a `<div>` with `role=textbox`, `name=body`, `data-lexical-editor=true`:

```
*[35]<div name=body role=textbox aria-placeholder=Join the conversation ...>
```

> Warning: **`innerTextArea` is only the trigger; the Lexical div is the actual fill target, and the two idx values differ after expansion. Never use `type` on the `innerTextArea` idx or jump directly to submit. Find the `role=textbox data-lexical-editor=true` div in the current `state`, then call `input <lexical_idx>` on that div.**

### 5. Fill via `browser-act input` (Lexical accepts real keystrokes)

```bash
browser-act --session <run_session> input <lexical_idx> "<text>"
sleep 2
```

**Hard gate -verify the fill committed before proceeding to submit:**

```bash
browser-act --session <run_session> state
```

Only take the filled-state screenshot when `state` does not clearly show the inserted text:

```bash
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-comment-filled.png
```

**Agent: verify from `state` that the expanded Lexical editor contains the expected text or a clear prefix of it. Use only browser-act output for this verification.**

If the state output does not show the filled text, use the screenshot as the second source. If neither source proves the text landed ->**STOP. Do not proceed to submit.** Input landed in the wrong element (likely `innerTextArea` instead of the Lexical div). Go back to step 4, re-read state, find the correct `role=textbox data-lexical-editor=true` idx, re-run `input` once. If verification is still impossible, log `skip("fill_verification_failed")`. Skipping this gate = likely empty-comment submission.

### 6. Pre-submit "checking wording" dwell

```bash
sleep $((RANDOM % 4 + 4))   # 4-7s
```

### 7. Submit

```bash
browser-act --session <run_session> network clear
browser-act --session <run_session> scrollintoview --selector "#comment-composer-submit-button"
sleep 1
browser-act --session <run_session> state
```

> **`scrollintoview` may return "Node does not have a layout object"** on comment permalink pages where the submit button lives inside a nested Reddit control. This error is non-fatal -ignore it and proceed to `state`. The button is present regardless.

**Agent: find the submit button in state.** Typically:

```
*[37]<button id=comment-composer-submit-button type=submit ...>
    Comment
```

If not present ->composer may have collapsed (re-do step 4). If `pressed=true` or disabled ->verify fill committed.

**Pre-submit page guard:** before clicking, re-read the current URL and state. It must still be the target comments thread. If URL contains `/submit/`, title/markdown says Create Post, or state shows `inner-post-submit-button` / post title/body fields instead of `comment-composer-submit-button`, **do not click**. Navigate back to `<post_url>` once and restart from Step 1a. If the second guard fails, log `skip("wrong_page_submit_misdirect")`.

If `state` alone is ambiguous, call `get markdown` and `get title` before deciding. Do not run those extra reads on the normal path when the URL and composer controls are already clear.

Click:

```bash
browser-act --session <run_session> click <submit_btn_idx>
sleep 8
```

### 8. Verdict tree via network capture

```bash
browser-act --session <run_session> network requests --method POST
```

Look for a POST to `/svc/shreddit/t3_<postid>/create-comment`. Three branches:

**Branch A -No matching POST captured (or `network requests` returns empty):**
- browser-act's network buffer sometimes clears on `scrollintoview`/navigate. Fall through to step 9 browser-act visibility verify; don't immediately fail.
- If visibility verify also shows no comment ->retry click once. Still nothing ->`skip("click_failed")`.

**Branch B -POST status 400 / 403 / 429 / 5xx:**
- `400` ->fill likely didn't commit. Check step 5 verify return value. `skip("reddit_400")`.
- `403` ->permission or account-level block. `skip("reddit_403")`.
- `429` ->rate limit. `skip("reddit_429")`.

**Branch C -POST status 200:**
- Server accepted. Continue to step 9.

### 9. Browser-act visibility verify + success path

After submitting, go back to the original post thread before judging success. A click action, a 200 response, or a disappeared composer is not enough.

```bash
browser-act --session <run_session> wait stable --timeout 5000
browser-act --session <run_session> navigate <post_url>
browser-act --session <run_session> wait stable --timeout 10000
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
```

**Top-level comment** (depth = 0): in `state`, find the newest visible `shreddit-comment` / comment block authored by `<current_username>` whose text matches the submitted `<text>` prefix. Capture `thingid`, `permalink`, and `depth` from the state line or nearby link if present.

**Reply** (depth >=1): on a comment permalink page where the same account has an existing depth-0 comment, do not take the first matching author block. Find the newest matching comment/reply block under the target thread whose text matches `<text>` and whose state context shows reply depth >=1 or parent context matching `<parent_comment_id>`.

If the original post page does not expose a reliable match, use the user's comment history only as a permalink discovery fallback:

```bash
browser-act --session <run_session> navigate "https://www.reddit.com/user/<current_username>/comments/"
browser-act --session <run_session> wait stable --timeout 20000
browser-act --session <run_session> state
browser-act --session <run_session> get markdown
```

- History match found ->capture its permalink, navigate that permalink, and verify the submitted text is visible there. For top-level comments, also return to `<post_url>` once and confirm the original thread can surface the comment or link to that permalink.
- Only after the original thread or the verified permalink shows the submitted comment body ->update `progress.json.last_publish_at = now`, log `comment` event with `comment_id`, `permalink`, `depth`, and save an after-comment screenshot. Derive `comment_id` from the captured `t1_...` thingid or the permalink's `/comment/<id>/` segment; never guess.
- No body/permalink match after 10s ->reload `<post_url>` + retry once. Still nothing ->log `skip("original_thread_visibility_failed")` or surface `click_succeeded_but_no_comment_in_visibility_verify`; do not write a normal successful `comment` log entry.

Success definition: the actual comment body, or a permalink that resolves to that body, must be visible after post-submit verification. "Submit button clicked" and "network accepted" are intermediate signals, not success.

> Warning: **Shadow-ban detection is NOT in this flow.** Found in the account's own logged-in session does not prove public visibility (shadow accounts see their own content in their own session). For shadow verification, run manual weekly `r/ShadowBan` checks.

---

## Reply flow -nested reply to an existing comment

Same primitives; the difference is **precise target-comment Reply-button selection**.

### Navigate to the comment's permalink (no-slug format)

```
https://www.reddit.com/r/<sub>/comments/<post_id>/comment/<cid_without_t1_prefix>/
```

NOT `/comments/<post_id>/<title_slug>/comment/<cid>/`. The slug-less form is canonical; Reddit generates it on the `shreddit-comment` element's `permalink` attribute.

### Find the target's Reply button via tid-anchored state

On a permalink page, many Reply buttons appear (one per visible comment). In `state` output, each comment's rendered body has an id like `t1_<cid>-comment-rtjson-content`. The Reply button for that comment is the next `Reply`-labeled button after this content line. Example:

```
[46]<div id=t1_okxnlak-comment-rtjson-content />
    Only talks about themself...
|SHADOW(open)|[47]<shreddit-comment-action-row class=block />
    [48]<button class=button shrink-0 ...>
        Reply                ->idx 48 is the target's Reply button
```

**Agent: read state, find the line with `id=t1_<target_cid>-comment-rtjson-content`, then find the first `Reply` text below it and grab the button idx on the line above that `Reply`.**

### Click Reply ->the nested composer opens

```bash
browser-act --session <run_session> click <reply_btn_idx>
sleep 3
browser-act --session <run_session> state
```

Find the nested composer's Lexical editor idx (now there will be two -top-level composer's and this reply composer's). The reply composer's host has `parent-id="t1_<target_cid>"` attribute. Pick the Lexical editor whose nearby `comment-composer-host` context has that parent-id. In state output these appear in mounting order; the newly-mounted reply composer's editor is typically the LAST `[role=textbox][name=body]` block.

Fill:

```bash
browser-act --session <run_session> input <reply_lexical_idx> "<text>"
```

**Warning: Submit -multiple submit buttons trap:** after a reply composer opens, `state` will show **two** `comment-composer-submit-button` entries -one for the top-level composer (first in state, lower idx) and one for this reply composer (last in state, higher idx). **Always pick the highest idx.** Clicking the first one submits the empty top-level composer and silently does nothing.

```bash
browser-act --session <run_session> state
# Two submit buttons will appear -pick the LAST (highest idx) one
browser-act --session <run_session> click <reply_submit_idx_highest>
```

Log with `depth >= "1"`, `parent_id = t1_<target_cid>` (not `t3_`).

---

## progress.json fields used

| Field | Purpose |
|---|---|
| `last_publish_at` | Rate-limit floor (90s shared bucket across comments + posts + replies) |

---

## Common failure modes

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `fill didn't commit` (verify fails after input) | `browser-act input` went to the wrong element (e.g., the trigger textarea instead of the expanded Lexical editor) | Re-read state after the click-trigger step; the Lexical editor idx is DIFFERENT from the trigger idx and only appears post-expand |
| Submit button idx missing from state | Composer collapsed (maybe after a slow fill) | Re-scrollintoview + wait stable + re-read state; re-click the trigger if still missing |
| `reddit_400` | Lexical state empty at submit despite visible text | Step 5 verify didn't match -re-do the fill |
| `reddit_429` on fresh account | Low-karma rate limit (~5 writes/hour) | Back off aggressively, 15-min gaps |
| `reddit_403` repeating | Account-level block or shadow-adjacent | Manual r/ShadowBan verification; retire account if shadow |
| Reply flow: opened wrong composer | State search found the wrong Reply button | Verify via the `t1_<cid>-comment-rtjson-content` anchor; if the anchor isn't in state, `scrollintoview` on `shreddit-comment[thingid="t1_<cid>"]` first |

