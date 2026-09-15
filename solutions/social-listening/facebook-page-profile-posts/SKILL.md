---
name: facebook-page-profile-posts
description: "Scrapes posts from any public Facebook Page or personal Profile timeline, returning structured data including post text, author info with profile picture, engagement metrics (likes/comments/shares), full reaction breakdown (Like/Love/Wow/Haha/Sad/Angry/Care as both array and flat counts), hashtags and external links, media assets with full thumbnail URLs and dimensions, page ad library status, and collaborators. Use when user wants to scrape Facebook posts, extract Facebook page content, get Facebook post data, collect Facebook engagement stats, download Facebook posts, monitor a Facebook page, crawl Facebook timeline, get Facebook reactions, get like count comment count share count from Facebook, Facebook post bulk export, Facebook social media analytics, get profile picture, get page ad library status, fetch Facebook collaborators. Supports date range filtering (afterTime/beforeTime) and cursor-based pagination for bulk collection."
---

# Facebook — Page / Profile Posts Scraper

> Facebook page or profile URL → list of posts with full fields including media thumbnails, author profile pics, page ad library status, and flat reaction counts

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract posts from a public Facebook Page or personal Profile timeline, including post content, engagement counts, full reaction breakdown, media thumbnails, author profile picture, page ad library status, and text references (hashtags/links).

## Prerequisites

- The target Facebook page or profile is open in the browser (e.g., `https://www.facebook.com/cern`)
- User is logged into Facebook (user avatar visible in the top right)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Facebook has been confirmed in the current session → skip this step.

Otherwise: navigate to `https://www.facebook.com` and check:
- User avatar or name visible in top right → logged in, continue
- Login button visible → not logged in, inform the user and assist with login

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### API: Resolve Facebook page URL to numeric page ID

`eval "$(python scripts/get-page-id.py '{page_url}')"`

Parameters:
- `page_url`: Full Facebook page or profile URL, e.g. `https://www.facebook.com/cern`

**Must run while the target page is open** (or any Facebook page is open) so the browser has Facebook cookies.

Output example:
```json
{
  "pageId": "100064792144187",
  "pageUrl": "https://www.facebook.com/cern"
}
```

Error handling: If `pageId` is not found (page not found or not logged in), verify login status and that the URL is a valid Facebook page.

### API: Fetch posts from page/profile timeline

`eval "$(python scripts/get-page-posts.py '{page_id}' --page-url '{page_url}' --cursor '{cursor}' --after-time {after_time} --before-time {before_time} --count {count})"`

Parameters:
- `page_id`: Numeric Facebook page/profile ID (from get-page-id above)
- `--page-url`: Original input URL (used for `facebookUrl`, `inputUrl`, `pageName` fields); omit if not needed
- `--cursor`: Pagination cursor string from previous response `pagination.endCursor`; omit or pass `null` for first page
- `--after-time`: Unix timestamp (seconds); only return posts after this time; omit or pass `null` for no filter
- `--before-time`: Unix timestamp (seconds); only return posts before this time; omit or pass `null` for no filter
- `--count`: Number of posts per batch, default `5`, max recommended `10`

Output example:
```json
{
  "posts": [
    {
      "facebookUrl": "https://www.facebook.com/cern",
      "postId": "1417704873732571",
      "pageName": "cern",
      "url": "https://www.facebook.com/cern/posts/pfbid0n87...",
      "time": "2026-05-22T14:30:18.000Z",
      "timestamp": 1779460218,
      "user": {
        "id": "100064792144187",
        "name": "CERN",
        "profileUrl": "https://www.facebook.com/cern",
        "profilePic": "https://scontent-lax3-1.xx.fbcdn.net/v/t39.30808-1/..."
      },
      "collaborators": [],
      "text": "Post text content here...",
      "textReferences": [
        { "type": "ExternalUrl", "url": "https://home.cern/...", "offset": 731, "length": 96 },
        { "type": "Hashtag", "url": "https://www.facebook.com/hashtag/espp", "offset": 296, "length": 5 }
      ],
      "link": "https://home.cern/...",
      "likes": 1285,
      "comments": 45,
      "shares": 125,
      "topReactions": [
        { "name": "Like", "count": 1167 },
        { "name": "Love", "count": 98 },
        { "name": "Care", "count": 9 },
        { "name": "Wow", "count": 8 },
        { "name": "Haha", "count": 1 },
        { "name": "Sad", "count": 1 },
        { "name": "Angry", "count": 1 }
      ],
      "topReactionsCount": 1285,
      "reactionLikeCount": 1167,
      "reactionLoveCount": 98,
      "reactionCareCount": 9,
      "reactionWowCount": 8,
      "reactionHahaCount": 1,
      "reactionSadCount": 1,
      "reactionAngryCount": 1,
      "media": [
        {
          "__typename": "Photo",
          "id": "1417649567071435",
          "thumbnail": "https://scontent-lax3-1.xx.fbcdn.net/v/t39.30808-6/...",
          "photo_image": { "uri": "https://scontent-lax3-1.xx.fbcdn.net/...", "width": 960, "height": 540 },
          "url": "https://www.facebook.com/photo.php?fbid=1417649567071435&...",
          "ocrText": "Artistic representation of the Future Circular Collider",
          "feedback": { "can_viewer_comment": true, "id": "ZmVlZGJhY2s6..." }
        }
      ],
      "feedbackId": "ZmVlZGJhY2s6MTQxNzcwNDg3...",
      "facebookId": "100064792144187",
      "topLevelUrl": "https://www.facebook.com/100064792144187/posts/1417704873732571",
      "pageAdLibrary": {
        "is_business_page_active": false,
        "id": "169005736520113"
      },
      "inputUrl": "https://www.facebook.com/cern"
    }
  ],
  "pagination": {
    "endCursor": "Cg8Ob3JnYW5pY19j...",
    "hasNextPage": true
  }
}
```

For **video/reel posts**, `media[0]` has these fields instead of `photo_image`:
```json
{
  "__typename": "Video",
  "id": "1540366350780488",
  "thumbnail": "https://scontent-lax3-1.xx.fbcdn.net/v/t15.5256-10/...",
  "url": "https://www.facebook.com/reel/2188342222016401/",
  "playableUrlSd": "https://video.xx.fbcdn.net/...",
  "playableUrlHd": "https://video.xx.fbcdn.net/...",
  "viewsCount": null
}
```

Error handling: If response contains `"error": true`, check that the target page is open and the user is logged in, then retry once. If the error persists, the `doc_id` may have expired — see Known Limitations for recapture steps.

## Pagination

**API Pagination**: cursor-based. Pass `pagination.endCursor` from each response as `--cursor` in the next call. Start value: omit `--cursor` (first page). Termination: `pagination.hasNextPage === false`.

## Success Criteria

`posts.length >= 1` AND `posts[0].postId` is non-null AND `posts[0].user.id` is non-null AND `posts[0].user.profilePic` is non-null

## Known Limitations

- `viewsCount` for video posts is always `null` — Facebook does not include video view counts in the timeline feed GraphQL response; this field requires a separate video-specific API call not covered by this Skill
- `media.playableUrlSd/Hd` requires the user to be logged in; unauthenticated sessions may return null
- `collaborators` is an empty array for most posts (only populated when the post has tagged co-authors)
- The persisted query `doc_id` and its `__relay_internal__pv__*` provided variables change when Facebook deploys updates (a stale set fails with `missing_required_variable_value`). `scripts/get-page-posts.py` reads both at runtime from the page's own Relay modules, so no manual recapture is normally needed:
  - `require('ProfileCometTimelineFeedRefetchQuery_facebookRelayOperation')` → current `doc_id` string
  - `require('ProfileCometTimelineFeedRefetchQuery.graphql').params.providedVariables` → provider objects; call `.get()` on each for its value
  - The hard-coded `doc_id` in the script is only a fallback for when those modules aren't loaded — open the target page (not a bare facebook.com tab) before calling
- If the query succeeds but fields come back `null` (e.g. likes/comments/shares, media), Facebook changed the response shape rather than the query — inspect a raw node and re-map the paths in `extractPost`
- `pageName` is derived from the URL path and may be incorrect for profile pages with numeric IDs (e.g., `https://www.facebook.com/100012345` → pageName = `100012345`)
- Requires an active Facebook login session; public/unauthenticated access is not supported
- Date filtering (`afterTime`/`beforeTime`) applies to the timeline cursor position, not a strict server-side filter; posts near the boundary may occasionally appear outside the specified range

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through paginated calls serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add a 1–2 second delay between paginated calls to avoid rate limiting. To increase throughput, open multiple browser sessions and distribute pages across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, test with 1-2 items first to verify the script runs correctly; only then run the full batch
- **Reduce redundant pre-operations**: Run `get-page-id` once per page URL and reuse the result for all paginated calls
- **Error resumption**: Save results page by page during batch processing; on failure, resume from the last successful `endCursor` rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/facebook-posts-scraper-facebook-page-profile-posts.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what pages were scraped or how many posts were returned — those are task outputs, not experience.
