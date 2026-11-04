# Post Publishing (TEXT / LINK / IMAGE) -Pure browser-act CLI Flow

**All three post flows use pure `browser-act` CLI as the only execution path.** Title / link URL / body (Lexical) / image upload / submit button all go through `browser-act` subcommands.

Three browser-act CLI behaviors that aren't always obvious:

- `browser-act input <idx> "text"` **commits to Lexical contenteditable state** using browser-act native input.
- `browser-act state` **enumerates Reddit's nested controls**, including `#submit-post-button ->inner-post-submit-button` and `shreddit-composer`'s internal fields.
- `browser-act upload <btn_idx> <path>` **handles Reddit's drop zone through browser-act** -no need for the file input to be visible in state; the file is supplied through the browser-act command.

---

## Inputs

- `<username>` / `<browser_id>` / `<current_username>` / `<run_session>` -as in comment-publishing.md
- `<subreddit>` -target sub, no `r/` prefix
- `<post_type>` -`TEXT` / `LINK` / `IMAGE` (written into URL `?type=` param)
- `<title>`, plus `<body>` (TEXT) / `<url>` (LINK) / `<image_path>` (IMAGE)

---

## Common flow (all three post types)

### 1. Pre-flight -navigate + dwell

```bash
PARAM_TYPE=$(echo "$POST_TYPE" | tr '[:upper:]' '[:lower:]')
SUBMIT_URL="https://www.reddit.com/r/$SUB/submit/?type=$PARAM_TYPE"

browser-act --session <run_session> browser open --headed <browser_id> "$SUBMIT_URL"
browser-act --session <run_session> wait stable --timeout 10000

sleep $((RANDOM % 4 + 4))   # 4-7s dwell reading sub rules

TS=$(date +%s)
browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/${TS}-before-post.png
```

If `approval-rules.md` Step 3 already opened and verified `<run_session>`, navigate to `$SUBMIT_URL` in that same active flow instead of opening a second tab. Across separate flows, always start fresh from `browser open --headed <browser_id>`; never rely on an old browser-act session.

`wait stable` is advisory on Reddit's SPA. If it times out, continue to `state` / markdown instead of repeating long waits.

### 2. Front-gate check

```bash
browser-act --session <run_session> get markdown
```

**Agent: read markdown. Skip if any of these specific banners are present:**

- `"This community has been banned"` / `"has been banned from Reddit"` ->`skip("sub_access")`
- `"You must be a member of this community"` / `"restricted community"` ->`skip("sub_access")`
- `"you are doing that too much"` / `"Rate limit exceeded"` ->`skip("rate_limit_banner")`

Don't match loose `"banned"` / `"locked"` -sidebar rules use those words too.

Confirm the requested post type from the active composer's actual controls, not the `?type=` URL alone. LINK requires a visible URL field; IMAGE requires an upload control. If a type tab is available, select the requested type and refresh `state`. If Reddit shows a page-load error or the required controls are absent, reload once and inspect again; if still unavailable, stop with `skip("post_type_unavailable")`. Hidden Add Link/media templates in markdown are not usable controls. Never silently submit a TEXT post in place of the approved LINK/IMAGE type.

---

### TEXT post branch

```bash
browser-act --session <run_session> state
```

**Agent: read current state and find the title/body inside the active post composer. Current UI may use `r-post-composer-form`; older UI may use `shreddit-composer`. Do not require one host tag:**

1. **Title** -`<textarea>` with `name=title` (typically idx around 30-40), example:
   ```
   *[33]<textarea id=innerTextArea name=title maxlength=300 ...>
   ```
2. **Body** -`<div>` with `role=textbox`, `name=body`, `data-lexical-editor=true`:
   ```
   *[35]<div name=body role=textbox aria-placeholder=Body text (optional) ...>
   ```

Fill both via `browser-act input`:

```bash
browser-act --session <run_session> input <title_idx> "$TITLE"
sleep $((RANDOM % 3 + 2))   # 2-5s between fields
browser-act --session <run_session> input <body_idx> "$BODY"
sleep 2
```

Verify with browser-act native output. Read current `state`, then use `get value <current_title_idx>` for the title when its value is not echoed in state. Use `get text <current_body_idx>` for Lexical text, or `get value <current_link_idx>` for a link field. Global CSS queries do not automatically cross shadow boundaries, so prefer the current indices for shadow-root fields. Compare the actual readback with the intended title/body/URL before submission; do not accept a successful input command alone. Production mode reads `state` first. Only take the filled-state screenshot when `state` cannot prove the title/body/link fill.


```bash
browser-act --session <run_session> state
```

Read `state` first. If `state` is inconclusive, take the filled-state screenshot and read it as the second source. The available browser-act evidence must match what was input. If the title/body/link is empty or cannot be verified, the wrong idx was targeted; re-read state and retry once. Use only browser-act output for this verification.

```bash
sleep $((RANDOM % 4 + 4))   # 4-7s "checking wording"
```

In normal production mode, the filled-state screenshot may not exist; `state` alone is sufficient when it clearly shows the expected fill.

If `state` is inconclusive, run `browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-post-filled.png` and read that screenshot as the second source.

### LINK post branch

Same as TEXT but use URL input instead of body:

**Agent: in state, find the title idx + URL idx.** URL field is an `<input type=url>` or has `name=link`:

```bash
browser-act --session <run_session> input <title_idx> "$TITLE"
sleep 2
browser-act --session <run_session> input <url_idx> "$LINK_URL"
sleep $((RANDOM % 4 + 4))
```

### IMAGE post branch

```bash
browser-act --session <run_session> state
```

**Agent: find the device-upload-button in state.** Inside `#fileInputInnerWrapper` / `#r-image-upload-field-input-file`:

```
[35]<div id=fileInputInnerWrapper />
    Drag and Drop or upload media
    [36]<button id=device-upload-button type=button invalid=false />
```

Pass the button idx to `browser-act upload` with the image file path. The browser-act CLI handles the browser file chooser internally, so the native OS dialog never appears and the file is supplied through the browser-act command:

```bash
browser-act --session <run_session> upload <device_upload_btn_idx> "$IMAGE_PATH"
```

Wait for thumbnail generation -the composer re-renders and title textarea idx may shift:

```bash
browser-act --session <run_session> wait stable --timeout 20000
sleep 3
browser-act --session <run_session> state
```

**Agent: re-find the title idx (may have shifted after upload re-render), then fill:**

```bash
browser-act --session <run_session> input <title_idx_after_upload> "$TITLE"
sleep $((RANDOM % 4 + 4))
```

---

## Submit (all three branches converge)

```bash
browser-act --session <run_session> network clear
# If the current Post button is outside the viewport, scroll to the observed composer/button.
# The legacy #submit-post-button wrapper is optional; use current state when it is absent.
sleep 2
browser-act --session <run_session> state
```

**Agent: find the active composer's enabled Post submit button in current state.** It may be an `inner-post-submit-button` inside a shadow root; the old outer wrapper is not required. Distinguish Post from Save Draft:

```
[81]<button id=inner-post-submit-button type=button invalid=false />
    Post
```

Click via browser-act CLI (produces trusted events, trips reCAPTCHA, Reddit accepts):

```bash
browser-act --session <run_session> click <inner_submit_idx>
sleep 10   # media posts take longer; wait generously
```

### Verdict tree

```bash
browser-act --session <run_session> state
browser-act --session <run_session> get title
```

Read the current URL from the `state` output.

**Branch A -URL redirected to `r/<sub>/` or the new post's permalink:**
- Post submitted successfully. Reddit's standard post-submit redirect. Continue to verify.

**Branch B -URL still on `/submit/`:**
- Inspect `network requests --method POST` for the actual submission initiated by this click. Reddit may use a GraphQL mutation (`/svc/shreddit/graphql`) or a submit endpoint; do not require only the legacy `/svc/shreddit/submit` URL. A 200 response is not sufficient if the JSON contains a business error. Do not mistake analytics/recaptcha requests for post submission.
- Non-2xx ->handle by code (`reddit_400/403/429/5xx`).
- No matching submission captured ->check the intended post in the account submitted list before any retry. If it already exists, verify that permalink and do not click again. Retry once only when no submission/body match exists; otherwise report an uncertain result without risking a duplicate.

---

## Verify (2-phase)

### Phase 1 -post in submitted list

```bash
browser-act --session <run_session> wait stable --timeout 10000
sleep 8   # short replication lag; retry below if needed
browser-act --session <run_session> navigate "https://www.reddit.com/user/$CURRENT_USER/submitted/"
browser-act --session <run_session> wait stable --timeout 10000

browser-act --session <run_session> state
browser-act --session <run_session> get markdown
```

Read the first 10 submitted items from `state` / markdown. Find the post whose title starts with our title prefix. Capture `thingid` / `post_id`, `permalink`, title, and rendered post type from state if present; otherwise capture the visible permalink from markdown. If not found, wait 10s and refresh the submitted list once. Still not found ->`skip("post_not_in_submitted_list")` (possible shadow-adjacent issue; run manual r/ShadowBan check).

### Phase 2 -permalink filter check


```bash
browser-act --session <run_session> navigate "https://www.reddit.com<permalink>"
browser-act --session <run_session> wait stable --timeout 10000
browser-act --session <run_session> get markdown
```

**Agent: check markdown for filter banners:** Normalize curly/straight apostrophes and whitespace before comparing phrases (for example Reddit’s and Reddit's); read the current post's banner, not unrelated navigation or quoted content.

- `"removed by Reddit's filters"` ->sub-level or Reddit-level filter. `visibility: "removed_by_filter"`, `filter_banner: "<copy>"`. Still update `last_publish_at` (attempt consumed the bucket).
- `"removed by moderators"` / `"[removed]"` ->mod removal. Same handling.
- None of the above ->`visibility: "visible"`. Success.

### On success

- Take an after-post evidence screenshot from the verified permalink page:
  ```bash
  browser-act --session <run_session> screenshot ~/.reddit-warmup/<username>/evidence/<ts>-after-post.png
  ```
- If the screenshot fails or times out, record that evidence limitation and retain the native state/readback and permalink. Do not retry submission or omit the accepted attempt from the rate-limit state because a screenshot failed.
- Update `progress.json.last_publish_at = now`.
- Log `post` event with `post_id`, `permalink`, `post_type_rendered`, `title`, `created_timestamp`.
- For Stage 3: set `progress.json.post_watchtower_deadline = now + 30min`.

---

## progress.json fields used

Same as comment flow:

| Field | Purpose |
|---|---|
| `last_publish_at` | Rate-limit floor (shared bucket with comments) |
| `post_watchtower_deadline` | Stage 3 only; tells watchtower to poll replies for 30 min |

---

# IMAGE posts -provenance & safety (opt-in only)

Text-only posts are the safe default. **Image posts often get ~2-3x engagement** in visual subs (r/DIY, r/cooking, r/gardening, etc.), so "show-and-tell" or "mishap" posts benefit from a rough, real-looking image.

This section only fires when all three are true:

- Sub is visual (`sub_profiles.json[<sub>].prefers_image == true`)
- Draft is "show-and-tell" or "mishap" in nature
- `config.yaml ->post_options.allow_images: true` (opt-in per account)

Any false ->ship text-only.

## Image sourcing

The skill **never auto-publishes an image it found itself.** Two paths:

### Option 1 (recommended): user provides the image

> Image note: This post would read better with a rough phone-shot image. Have one? Give me a local path. Otherwise I can find candidates on Google Images for you to pick + reverse-check.

User gives path ->go to Pre-publish safety checks below.

### Option 2: skill searches, user picks + reverse-checks

1. Derive 2-3 search terms from the post topic (NOT from the brand).
2. Search Google Images:
   ```bash
   browser-act --session <run_session> navigate "https://www.google.com/search?q=<term>&tbm=isch&tbs=isz:m"
   browser-act --session <run_session> wait stable
   browser-act --session <run_session> get markdown
   ```
   `tbs=isz:m` filters to medium-res (phone-shot vibe beats 4k stock).
3. Show top ~10 candidates with thumbnails + source URLs. User picks.
4. Google Lens reverse-check on the picked image:
   ```bash
   browser-act --session <run_session> navigate "https://lens.google.com/uploadbyurl?url=<image_url>"
   browser-act --session <run_session> wait stable
   browser-act --session <run_session> get markdown
   ```
   Reject if:
   - On Shutterstock / Getty / iStock / Adobe Stock (commercial stock = guaranteed downvotes + copyright)
   - >=20 distinct domains using it (too famous)
   - Top hit for a specific named product/person (wrong connotation)
5. Failed pick ->loop back to step 3.
6. Download to `~/.reddit-warmup/<username>/images/<timestamp>.jpg`.

## Pre-publish safety checks (both options)

| Check | Action if failed |
|-------|------------------|
| File exists | Abort; ask user for another path |
| Extension `.jpg/.jpeg/.png/.webp/.gif/.mp4/.mov` | Convert or pick another |
| File size 50KB-10MB | Too small = thumbnail/corrupt; too big ->Reddit rejects upload (no thumbnail appears, `browser-act upload` returns but no re-render) |
| EXIF GPS strip | Ask user to run `exiftool -gps:all= <path>`; warn if they don't |
| Reverse-search passes (Option 2 only) | Already handled above |

Then proceed to the IMAGE post branch above.

## Activity log -image-specific fields

```json
{"image_path": "~/.reddit-warmup/<username>/images/<ts>.jpg",
 "image_source": "user_provided|google_images"}
```

## Config hook

```yaml
post_options:
  allow_images: false            # Set true to let Stage 3 suggest image attachment
  image_source: "ask"            # "ask" (default) | "user_only" (never search Google) | "search_ok"
```

---

## Common failure modes

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `body_fill_failed` / empty body at verify | `browser-act input` went to the wrong element | Re-read state post-expand; pick the `[role=textbox][name=body]` idx, not the trigger textarea |
| Submit button idx missing from state | Page loading incomplete | `scrollintoview` on `#submit-post-button` + `wait stable` + re-read state |
| `image_upload_rejected` `validity:invalid` | File > 20MB / unsupported / corrupt | Re-source per safety checks; never retry same file |
| `post_not_in_submitted_list` after 200 OK | Shadow-adjacent OR replication lag > 15s | Retry verify once after another 15s; persistent ->manual r/ShadowBan |
| `removed_by_filter` 2+/week on same account | Sub AutoMod rejecting this account | Manual r/ShadowBan check; pause Stage 3 writes |


