---
name: instagram-hashtag-posts
description: "Scrapes Instagram posts by hashtag, returning media items with captions, like/comment counts, media URLs and user info from the hashtag explore feed. Use when user mentions Instagram hashtag scraping, get posts by hashtag, IG hashtag feed, scrape Instagram by tag, hashtag posts Instagram, search Instagram hashtag, pull posts from hashtag, Instagram topic posts, trending hashtag content, Instagram tag posts."
---

# Instagram — Hashtag Posts

> hashtag → list of posts (media, caption, counts, user info)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch posts tagged with a specific hashtag by navigating to Instagram's keyword search page and capturing the GraphQL API response.

## Prerequisites

- Browser is open on any Instagram page: `https://www.instagram.com/`
- Logged into Instagram (user avatar or username visible in top-right corner)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Instagram has been confirmed in the current session → skip this step.

Otherwise: open `https://www.instagram.com/` and observe the page login status:
- Logout/sign-out entry, user avatar, or username exists → logged in, continue execution
- Login/register entry exists with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: get hashtag posts (direct fetch from hashtag page)

Must be called while the browser is on the hashtag search page — navigate first, then call:

1. `navigate https://www.instagram.com/explore/search/keyword/?q=%23{hashtag}` (e.g., `%23travel` for `#travel`)
2. `wait stable`
3. `eval "$(python scripts/fetch-hashtag-posts.py '{hashtag}')"`

The script replays the signed GraphQL request (`PolarisKeywordSearchExplorePageRelayQuery`, doc_id `36829937936605248`) directly inside the browser, using session cookies and CSRF token already present on the page.

Error handling: If the result contains `error: true`, check whether the page loaded correctly (login prompt visible? rate-limit banner?). Re-navigate and retry once. If `items` is empty but no error, the hashtag may have no top posts at this time.

Output example:
```json
{
  "items": [
    {
      "pk": "3900557621921709539",
      "code": "DYwOA07iPmB",
      "media_type": 1,
      "taken_at": 1779686199,
      "like_count": 45230,
      "comment_count": 312,
      "caption": "Beautiful sunset #travel",
      "thumbnail_url": "https://scontent.cdninstagram.com/...",
      "video_url": null,
      "username": "traveler_jane"
    }
  ],
  "count": 20
}
```

## Pagination

**API Pagination**: `end_cursor` in `data.xdt_fbsearch__top_serp_graphql.page_info`. Check `has_next_page`; when true, the next page requires a separate GraphQL POST with the cursor value injected — this requires UI interaction (scroll to page bottom to trigger next page load) then re-reading traffic for the next `PolarisKeywordSearchExplorePageRelayQuery` request.

## Success Criteria

`items count >= 1 AND items[0].pk non-null AND items[0].username non-null`

## Known Limitations

- Results are limited to Instagram's "top posts" selection for the hashtag; full chronological feed is not available
- Login required: hashtag posts are not accessible without authentication
- Rate limiting may occur with high-frequency hashtag searches across sessions

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/instagram-scraper-instagram-hashtag-posts.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
