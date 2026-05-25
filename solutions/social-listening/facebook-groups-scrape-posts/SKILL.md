---
name: facebook-groups-scrape-posts
description: "Scrapes posts from a Facebook group given a group URL, sort order, and desired count — returns structured post metadata including post_id, permalink, author, timestamp, body text, images/videos, reaction counts, reaction type breakdown, comment count, and share count. Use when: user wants to scrape/extract Facebook group posts, collect FB group content, harvest group data, get posts from a Facebook group, monitor Facebook group activity, bulk export group posts, facebook groups scraping, facebook-groups-scrape-posts, fetch FB group feed."
---

# Facebook Groups — Scrape Posts

> Input: Facebook group URL + sort order + desired count → Output: post list with full metadata (JSON).

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given a Facebook group URL, scrape N posts sorted by the specified order and return structured metadata for each post.

## Prerequisites

- Target group page is already open in the browser: `https://www.facebook.com/groups/{group_slug_or_id}`
- Already logged into Facebook (user avatar, Messenger icon, and notification bell visible in the top-right corner)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If Facebook login status has been confirmed in the current session → skip this step.

Otherwise, navigate to `https://www.facebook.com/` and verify login status programmatically:

```
browser-act navigate 'https://www.facebook.com/'
browser-act wait stable --timeout 15000
browser-act eval "JSON.stringify({user_id: document.cookie.match(/c_user=(\d+)/)?.[1] || '0', USER_ID: (()=>{try{return require('CurrentUserInitialData').USER_ID;}catch(e){return '0';}})()})"
```

Verdict:
- `user_id` is a non-empty numeric string (e.g., `"61560817072276"`), or `USER_ID !== "0"` → logged in, continue
- `user_id === null` or `USER_ID === "0"` → not logged in; assist user: run `browser-act browser open {browser_id} https://www.facebook.com/login --headed` to open a headed window so the user can sign in manually (Stealth `normal` mode persists cookies — one login is reusable)

**Facebook may clear `c_user` mid-session**: if GraphQL errors such as `field_exception` or `missing_required_variable_value` occur during execution, re-run this login check before assuming the script is broken.

User refuses or cannot log in → terminate execution. Facebook enforces strict restrictions on unauthenticated group access (login modal blocks pagination, feed returns partial data + `field_exception`); login is a hard prerequisite.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the authenticated user, never bypassing authentication or access controls — equivalent to copy-pasting on the user's behalf. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; use the bash tool for execution.

### API: Scrape group posts (with auto-pagination)

Navigate to the target group page first, then invoke the scrape script (it auto-resolves the numeric group ID from the current page):

```
browser-act navigate 'https://www.facebook.com/groups/{group_slug_or_id}'
browser-act wait stable --timeout 20000
browser-act eval "$(python scripts/scrape-posts.py --sort CHRONOLOGICAL --count 20)"
```

Parameters:
- `--sort`: Sort order, default `CHRONOLOGICAL`. See "Enum Parameters" below
- `--count`: Desired number of posts, default `20`. Script auto-paginates until count is met or feed is exhausted
- `--max-pages`: Pagination safety cap, default `100`
- `--doc-id`: GraphQL persisted query `doc_id` for `GroupsCometFeedRegularStoriesPaginationQuery`, default `26577462205242925`. Update via this flag if Facebook rotates the version (see "Known Limitations")

Output example:
```json
{
  "ok": true,
  "group_id": "2580640642080467",
  "group_name": "Programmer Humor",
  "sort": "CHRONOLOGICAL",
  "total": 20,
  "posts": [
    {
      "post_id": "4052937798184070",
      "cache_id": "6790541484885792441",
      "id": "UzpfSTEwMDA4ODY4MzIx...",
      "permalink_url": "https://www.facebook.com/groups/programmerhumor/posts/4052937798184070/",
      "creation_time": 1772941518,
      "message": "Those were the days my friend ...",
      "author": {
        "id": "100088683215191",
        "name": "Jeff Bramlett",
        "profile_picture": null,
        "url": "https://www.facebook.com/JeffieB56"
      },
      "group": {
        "id": "2580640642080467",
        "name": "Programmer Humor",
        "url": "https://www.facebook.com/groups/programmerhumor/"
      },
      "reactions": {
        "total": 1,
        "total_formatted": "1",
        "breakdown": [
          { "name": "Haha", "reaction_id": "115940658764963", "count": 1 }
        ]
      },
      "share_count": 0,
      "share_count_formatted": "0",
      "comment_count": 0,
      "media": [
        {
          "__typename": "Photo",
          "id": "938454962453936",
          "photo_image": "https://scontent-...fbcdn.net/v/t39...jpg"
        }
      ]
    }
  ],
  "diagnostics": {
    "pages": [
      { "pageIdx": 0, "httpStatus": 200, "edgeCount": 4, "err": null, "hasNext": true }
    ]
  }
}
```

Video posts include additional fields in `media`: `playable_url` (mp4 direct link), `playable_url_hd`, and `thumbnail`.

## Enum Parameters

[AI] `--sort` sort order — Facebook accepts the following three values:

- `TOP_POSTS` — most relevant (default web sort)
- `CHRONOLOGICAL` — newest first (reverse chronological by post time)
- `RECENT_ACTIVITY` — most recently active (reverse chronological by latest comment/reaction time)

Values are fixed and validated by `argparse choices`; no runtime query needed.

## Pagination

**API Pagination**: handled automatically by the script.

- Pagination parameter: `cursor` (embedded in GraphQL `variables`)
- Type: opaque cursor (server-side state, base64-encoded)
- Initial value: `null` (first request)
- Next page value: `data.node.group_feed.page_info.end_cursor`
- Each response returns 3 edges (FB streaming mode ignores client-provided `count`)
- Termination: `has_next_page === false`, or `--count` / `--max-pages` limit reached

## Success Criteria

- `ok === true` and `total >= 1`
- `posts[*].post_id` non-null rate = 100% (non-post units such as Section Headers are filtered out by the script)
- `posts[*].permalink_url` and `posts[*].creation_time` non-null rate = 100%
- When using `CHRONOLOGICAL` sort, `creation_time` is strictly monotonically decreasing

## Known Limitations

- **Public groups only**: private groups require membership; returns empty or permission error when not a member
- **No comment body**: `comment_count` returns total count but the group feed GraphQL does not include `top_comments` content or authors. Facebook places comment data in a separate `CommentsRenderer` query triggered only when the user clicks "Comments" — fetching comment bodies requires additional per-`post_id` GraphQL requests (out of scope)
- **`doc_id` rotates with Facebook frontend versions**: when the default `26577462205242925` expires (`PersistedQueryNotFound` or HTTP 404), retrieve a fresh one:
  1. Open any group page while logged in
  2. Scroll down to trigger a new batch of posts
  3. `browser-act network requests --filter api/graphql --method POST`
  4. Check `X-FB-Friendly-Name` header on each request; find `GroupsCometFeedRegularStoriesPaginationQuery`
  5. Extract `doc_id` from that request's POST body and pass it via `--doc-id`
- **`group_name` can be null**: parsed from page HTML via heuristic regex; prefer `posts[*].group.name` (more reliable)
- **Localized count fields**: `reactions.total_formatted` and `share_count_formatted` format depends on Facebook's UI language (e.g., Chinese locale returns `"1.2万"` instead of `"12K"`)
- **Rapid requests trigger temporary throttling**: paginating too fast or calling multiple groups concurrently may return empty responses or temporary bans. Serialize group requests with a 2–5 s sleep between each
- **GraphQL `field_exception` / partial edges + errors**: almost always caused by session cookie being cleared. Check `c_user` cookie and `require('CurrentUserInitialData').USER_ID` — if `0` / `null`, return to "Login Verification" and re-login; do not attempt to extract data from error responses
- **Author avatar often null**: `author.profile_picture` is frequently unloaded in the group feed default response (Facebook lazy-loads avatars); a separate query is required if avatars are needed

## Execution Efficiency

- **Batch orchestration**: for small counts, call each group directly; for large counts, write a bash script to loop serially — do not parallelize (prone to anti-scraping triggers). Test with a minimal sample before running the full batch. Add appropriate intervals per rate guidance in "Known Limitations" above
- **Test before batch execution**: always test with 1–2 items to verify the script runs correctly before running the full batch
- **Reduce redundant pre-operations**: when multiple steps share the same prerequisite state, complete them in batch under that state to avoid repeatedly re-establishing it
- **Error resumption**: save results item by item during batch processing; resume from the breakpoint on failure rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/facebook-groups-scrape-posts-facebook-groups-scrape-posts.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record which groups were used or how many posts were returned — those are task outputs, not experience.
