---
name: x-tweet-by-conversation
description: "Collects every tweet in an X (Twitter) conversation thread given a conversation id (root tweet id) — the focal tweet plus all replies, sub-replies, and quote chains — and returns normalized per-tweet data with text, author, engagement counts, media, hashtags, mentions, in_reply_to mapping, and cursor for pagination. Use when user mentions Twitter conversation, X conversation thread, conversation_id, thread scraper, scrape Twitter replies, all replies to a tweet, replies under a tweet, sub-replies, nested replies, thread harvester, get replies of a tweet, scrape comments on Twitter, scrape comments on X, full thread extraction, conversation export, conversation tree, reply chain, thread dump, X tweet thread, twitter thread scrape, comment scraping twitter, comment scraping x, focal tweet plus context, root tweet plus replies. Also applies to sentiment analysis on a single viral tweet, controversy mapping, harvesting community Q&A threads, capturing AMA threads, recovering long-running discussions, and any paginated bulk reply collection driven by a conversation id."
---

# X — Tweets by Conversation

> Conversation id (root tweet id) → normalized list of every tweet in the thread (focal tweet + replies + sub-replies), with author, engagement, media, cursor.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given an X conversation id (which equals the root tweet id), collect the focal tweet and every reply / sub-reply visible to the logged-in session, returning structured per-tweet data with pagination cursors.

## Prerequisites

- Active X session in the browser (left sidebar shows logged-in avatar / @handle).
- Network capture is enabled in the browser-act session.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for X has been confirmed in the current session → skip this step.

Otherwise: open `https://x.com` and observe the left sidebar:
- User avatar or @handle visible → logged in, continue
- "Sign in" / "Log in" prompt visible → not logged in, inform the user and assist the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads tweet data already shown to the user, never bypassing authentication. The browser's own JS signs the GraphQL request; the Skill triggers it via URL navigation and reads the response from network traffic. Python scripts under `scripts/` only build URLs and parse responses — they do not call X directly. Run them through the bash tool.

### Network Capture: full conversation thread

Step 1 — build the tweet-detail URL for the conversation root:

`URL=$(python scripts/build-conversation-url.py '{conversation_id}' [--handle {handle}])`

Parameters:
- `conversation_id` (positional): the X conversation id, which equals the root tweet id (the same number you would see in `https://x.com/i/status/<conversation_id>`).
- `--handle`: the root tweet's author handle if known; if unknown, leave the default — `x.com/i/status/<id>` resolves to the same focal tweet because X canonicalises the URL.

Step 2 — navigate and capture the first page:

1. `network requests --clear`
2. `navigate "$URL"`
3. `wait stable --timeout 25000` (timeout is normal on X; proceed)
4. `network requests --type xhr,fetch --filter TweetDetail` → take the latest entry's `request_id`
5. `network request <request_id>` → save full output to a file (e.g. `tmp/x-conversation-page-1.txt`)
6. `python scripts/parse-tweets.py --json-file tmp/x-conversation-page-1.txt --source tweet_detail` → emits JSON `{tweets, count, cursor_top, cursor_bottom}`. The focal tweet is the first element; subsequent elements are replies (in display order). Each reply carries `is_reply: true`, `in_reply_to_id`, `in_reply_to_user`, and `conversation_id == <root tweet id>`, which makes the reply tree reconstructable downstream.

Endpoint characteristic: URL contains `/i/api/graphql/<hash>/TweetDetail`. The query hash rotates; always filter by name.

Step 3 — paginate via scroll to load deeper replies and sub-replies:

1. `network requests --clear`
2. `scroll down --amount 5000`
3. `wait stable --timeout 10000`
4. `network requests --type xhr,fetch --filter TweetDetail` → newest entry's `request_id`
5. `network request <request_id>` → save to `tmp/x-conversation-page-N.txt`
6. `python scripts/parse-tweets.py --json-file tmp/x-conversation-page-N.txt --source tweet_detail`

Repeat Step 3 until any termination condition is met:
- Accumulated unique reply count reaches the user's target.
- `count == 0` on the current page.
- `cursor_bottom` is unchanged across two consecutive pages.
- The page shows a "Show more replies" button gated by visibility filters — `state` reveals it; the Agent may `click <index>` to expand more, then resume scrolling.

Error handling:
- If the focal tweet is deleted or protected, the response carries a `TweetTombstone` entry; `parse-tweets.py` filters tombstones, so the result will be `count: 0` — report to the user and stop.
- If no `TweetDetail` request appears after a scroll, wait 3 s and retry once. Persistent absence after two scrolls means the thread has been fully loaded.
- If a captcha challenge appears (visible in `state` as an authorization prompt), pause and ask the user.

Output example:
```json
{
  "tweets": [
    {
      "type": "tweet",
      "id": "2069990565530214798",
      "url": "https://x.com/Rothmus/status/2069990565530214798",
      "twitter_url": "https://twitter.com/Rothmus/status/2069990565530214798",
      "text": "\"We are going to have a multi-racial nation in Singapore. ...\"",
      "created_at": "Tue Jun 24 23:01:50 +0000 2026",
      "lang": "en",
      "source": "Twitter Web App",
      "retweet_count": 91,
      "reply_count": 84,
      "like_count": 567,
      "quote_count": 12,
      "bookmark_count": 50,
      "view_count": 64140,
      "is_reply": false,
      "is_retweet": false,
      "is_quote": false,
      "quote_id": null,
      "quote_url": null,
      "in_reply_to_id": null,
      "in_reply_to_user": null,
      "in_reply_to_user_id": null,
      "conversation_id": "2069990565530214798",
      "hashtags": [],
      "mentions": [],
      "urls": [],
      "media": [],
      "card": null,
      "place": null,
      "author": {
        "id": "987654321",
        "user_name": "Rothmus",
        "name": "Rothmus",
        "url": "https://x.com/Rothmus",
        "is_verified": false,
        "is_blue_verified": true,
        "verified_type": null,
        "profile_picture": "https://pbs.twimg.com/profile_images/.../photo.jpg",
        "description": "Singapore observer ...",
        "location": "Singapore",
        "followers": 12345,
        "following": 678,
        "created_at": "Wed Jun 16 10:00:00 +0000 2021"
      }
    },
    {
      "type": "tweet",
      "id": "2070027327409655973",
      "url": "https://x.com/DinoLeadingNews/status/2070027327409655973",
      "text": "@Rothmus @elonmusk Singapore proves that identity ...",
      "is_reply": true,
      "in_reply_to_id": "2069990565530214798",
      "in_reply_to_user": "Rothmus",
      "in_reply_to_user_id": "987654321",
      "conversation_id": "2069990565530214798",
      "like_count": 0,
      "reply_count": 0,
      "retweet_count": 0,
      "quote_count": 0,
      "bookmark_count": 0,
      "view_count": 19,
      "author": {"user_name": "DinoLeadingNews", "name": "Dino Leading News", "...": "..."},
      "...": "..."
    }
  ],
  "count": 40,
  "cursor_top": null,
  "cursor_bottom": "DAACCgABHLoz..."
}
```

## Pagination

**Network Capture Pagination**: triggered by `scroll down`. X's page JS inserts the previous response's `cursor_bottom` into the next `TweetDetail` request's `variables.cursor`. Some sub-reply branches require clicking an in-page "Show replies" expander (`state` to locate, `click <index>`) before the next scroll surfaces them. Termination: `count == 0`, `cursor_bottom` does not advance across two consecutive pages, or user target reached.

## Success Criteria

`count >= 1 on the first page` (the focal tweet must be present unless the conversation root is deleted) AND `every tweet has non-null id, text, created_at, author.user_name, like_count, retweet_count, reply_count, conversation_id` AND `each reply tweet has is_reply == true and in_reply_to_id pointing to a tweet inside the thread`.

## Known Limitations

- Only replies visible to the logged-in session are returned; X enforces visibility filters (blocked accounts, soft-blocked replies, "Show additional replies, including those that may contain offensive content").
- Deleted root tweets return a tombstone; the Skill terminates with `count: 0`.
- Quote tweets that reference this conversation are NOT included — they live in a separate timeline; collect them via `x-tweet-search-by-query` with `filter:quote conversation_id:<id>` if needed.
- `view_count` is `null` for very new replies where X has not emitted `views.count`.
- Sustained polling triggers per-session throttling; stay under ~150 timeline calls per 15-minute window per session.
- The page may never reach `network-idle`; `wait stable` will frequently time out — proceed to read network anyway.

## Execution Efficiency

- **Batch orchestration**: write a bash script that iterates conversation ids serially in one session. For parallelism, fan out across multiple stealth browsers each with its own login.
- **Test before batch execution**: run one conversation end-to-end (page 1 + at least one paginated page) first.
- **Reduce redundant pre-operations**: keep the same session for many sequential conversations.
- **Error resumption**: persist `cursor_bottom` and accumulated reply IDs per conversation after every page.
- **De-duplicate by `id`**: the focal tweet may appear in multiple paginated responses (some endpoints repeat the focal tweet at the top of every page); merge by `id`.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-tweet-scraper-x-tweet-by-conversation.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record which conversation was scraped or how many replies were returned — those are task outputs, not experience.
