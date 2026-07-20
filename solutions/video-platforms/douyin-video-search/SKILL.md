---
name: douyin-video-search
description: "Searches Douyin (douyin.com) for videos by keyword and returns structured video data including author info, stats, cover, description, hashtags, and download URL. Supports date range filtering and sorting by relevance, likes, or recency. Use when user mentions Douyin search, scrape Douyin videos, collect TikTok China videos, extract douyin video data, grab douyin results, fetch douyin keyword videos, douyin video list, douyin content mining, search douyin by keyword, douyin likes filter, douyin date filter, douyin video download links, douyin creator info, douyin hashtag extraction, douyin video scraper, douyin KOL research, douyin content analysis."
---

# Douyin — Video Search

> Keyword → paginated list of videos with author, stats, cover, description, hashtags, download URL

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch Douyin video search results for a given keyword, with optional sort order and date filters, returning complete structured data for each video.

## Prerequisites

- Browser is open and navigated to any Douyin page (douyin.com) with an active logged-in session
- User is logged in to Douyin (avatar visible in top-right corner)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Douyin has been confirmed in the current session → skip this step.

Otherwise: navigate to `https://www.douyin.com` and check the top-right corner:
- User avatar or account name visible → logged in, continue
- "登录" button visible → not logged in; inform the user and assist them in completing login via `remote-assist`

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already visible to the logged-in user, never bypassing authentication or access controls. JS code is in `scripts/` and invoked via `eval "$(python scripts/xxx.py {params})"`. Use the bash tool for execution.

### API: Search videos by keyword

Navigate to the Douyin search page first to establish cookie context, then call the search API directly.

**Step 1 — Navigate to search page:**

```
navigate https://www.douyin.com/search/{keyword}?type=video
wait stable
```

Replace `{keyword}` with the URL-encoded search term (e.g., `AI%E5%88%9B%E4%B8%9A`).

**Step 2 — Fetch search results:**

```bash
eval "$(python scripts/search-videos.py '{keyword}' --offset {offset} --count 20 --sort-type {sort_type} --publish-time {publish_time} --search-id '{search_id}')"
```

Parameters:
- `keyword`: search term (plain text, script handles URL encoding)
- `--offset`: pagination offset; start at `0`, then use `next_offset` from previous response (default: `0`)
- `--count`: results per page (default: `20`, max: `20`)
- `--sort-type`: sort order — `0`=综合排序/comprehensive (default), `1`=最多点赞/most liked, `2`=最新发布/latest
- `--publish-time`: date filter in days — `0`=不限/all time (default), `1`=一天内/1 day, `7`=一周内/7 days, `180`=六个月内/6 months, `365`=一年内/1 year
- `--search-id`: leave empty for first page; use `next_search_id` from previous response for page 2+

Output example:
```json
{
  "items": [
    {
      "aweme_id": "7656392146064639419",
      "title": "深度还原7姐妹创业 #ai #搞笑视频 #热门",
      "author_name": "楠楠AI小剧场",
      "author_profile_url": "https://www.douyin.com/user/MS4wLjABAAAAY4eph...",
      "video_url": "https://www.douyin.com/video/7656392146064639419",
      "cover_url": "https://p3-pc-sign.douyinpic.com/image-cut-tos-priv/...",
      "description": "深度还原7姐妹创业 #ai #搞笑视频 #热门 #逆天 #宝妈创业",
      "hashtags": ["#ai", "#搞笑视频", "#热门", "#逆天", "#宝妈创业"],
      "download_url": "https://www.douyin.com/aweme/v1/play/?video_id=v2700f...",
      "digg_count": 188184,
      "comment_count": 3346,
      "publish_time": 1782642711
    }
  ],
  "count": 20,
  "has_more": 1,
  "next_offset": 20,
  "next_search_id": "20260709115250C6DC5EE42A6DC2D6B48D"
}
```

**Error handling:**
- `status_code: 2483` → session cookie is invalid or expired; re-verify login and retry navigation step before calling again
- `error: true` in output → check `message` field; most common cause is session expiry, retry after navigating to `https://www.douyin.com` once
- If `count` in response is 0 with `has_more: 0` → no more results, pagination complete

## Enum Parameters

[AI] `sort_type` — UI filter panel options (read from 筛选 dropdown):
- `0`: 综合排序 (comprehensive, default)
- `1`: 最多点赞 (most liked)
- `2`: 最新发布 (latest/newest)

[AI] `publish_time` — UI filter panel options (read from 筛选 dropdown):
- `0`: 不限 (all time, default)
- `1`: 一天内 (within 1 day)
- `7`: 一周内 (within 7 days)
- `180`: 六个月内 (within 6 months)
- `365`: 一年内 (within 1 year)

## Pagination

**API Pagination**: parameter `offset`, type: page-number-style increment. Start value: `0`. Next page: use `next_offset` from response. Also pass `next_search_id` from first response as `--search-id` for all subsequent pages. Termination: `has_more == 0` or `count == 0` in response.

## Success Criteria

`count >= 1` AND `items[0].aweme_id` is non-null AND `items[0].digg_count` is non-null

## Known Limitations

- Requires an active Douyin login session; API returns `status_code: 2483` when unauthenticated or session expires
- `download_url` is a redirect URL (`/aweme/v1/play/`); the actual MP4 is at the final CDN redirect destination. Follow the redirect to obtain the direct file URL
- Filter parameter values for `sort_type` and `publish_time` are based on observed API behavior; edge-case values beyond the listed options are untested
- Douyin may impose rate limits on repeated search requests from the same session; add a 1–2 second delay between paginated requests in batch scripts

## Execution Efficiency

- **Batch orchestration**: Write a bash loop to iterate through pages serially within a single session; add 1–2 second sleep between requests to avoid rate-limit triggers
- **Test before batch**: Run with `--count 5` for 1–2 pages first to confirm the script works before executing the full batch
- **Error resumption**: Save `next_offset` and `next_search_id` after each page so batch can resume from the last successful page on failure
- **Multiple keywords**: For multiple keywords, loop through them sequentially in one session; re-navigate to each keyword's search URL before calling the API

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/douyin-video-search-douyin-video-search.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations from past runs (e.g., API parameter changes, session handling quirks); adjust strategy accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record task inputs or result counts — those are task outputs, not experience.
