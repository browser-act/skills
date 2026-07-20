---
name: amazon-bestseller-listing
description: "Amazon Best Sellers listing scraper: extract product cards from any Amazon Best Sellers (zgbs) or /gp/bestsellers/ category page — returns rank (position on chart), asin, title, url, image, imageAlt, price, stars, reviewCount, ratingRaw per item, plus category metadata (categoryName, categoryFullName, categoryUrl) and pagination state (currentPage, hasNextPage, nextPageUrl). Works across all Amazon regional TLDs (amazon.com, amazon.co.uk, amazon.de, amazon.co.jp, amazon.fr, amazon.it, amazon.es, amazon.ca, amazon.com.au, amazon.in, etc.). Use when user mentions Amazon Best Sellers, Amazon bestsellers, Amazon top 100, Amazon zgbs, Amazon /zgbs/, Amazon /gp/bestsellers/, Amazon Best Sellers Rank, Amazon BSR, Amazon top ranked products, Amazon top-selling products, Amazon chart, Amazon category ranking, Amazon best sellers by category, Amazon best sellers electronics, Amazon best sellers kitchen, Amazon best sellers toys, scrape Amazon bestsellers, extract Amazon top 100, Amazon rank scraper, Amazon best seller list, Amazon leaderboard, Amazon trending products, discover trending Amazon products, Amazon niche discovery, Amazon top ranked ASINs. Also applies to competitive intelligence via ranking snapshots, spotting up-and-coming products, sourcing bestseller ASINs for further enrichment, tracking rank changes over time, and building bestseller-per-category datasets."
---

# Amazon — Best Sellers Listing

> Input any Amazon Best Sellers (/zgbs/ or /gp/bestsellers/) URL → output ranked product list (position 1..N) + category info + pagination.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract the ranked product list from any Amazon Best Sellers page for any category or sub-category, across all Amazon regional TLDs, with pagination to walk beyond the first 50 items.

## Prerequisites

- Target page is already open in the browser: any Amazon Best Sellers URL (e.g. `https://www.amazon.com/gp/bestsellers/{category-slug}`, `https://www.amazon.com/Best-Sellers/zgbs/{category-slug}`, `https://www.amazon.com/Best-Sellers/zgbs/{category-slug}/{node-id}`, or the paginated variant `?pg={pageNumber}`)
- No login required

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `browser-act --session {name} eval "$(python scripts/xxx.py {params})"`. The `$(...)` is bash command substitution — it runs the python script, captures its printed JS text, and hands that JS string as a single argument to `browser-act eval`. Do not run `eval "$(python ...)"` as a bare shell command; that would ask bash to execute the JS as shell, which fails.

### DOM: extract bestseller cards from current best-sellers page

Bestseller pages are server-rendered — no XHR/fetch API for chart data. Cards use the stable `#gridItemRoot` container (30 cards per page, 2 pages up to top 50).

1. `navigate {any Amazon bestseller URL, e.g. https://www.amazon.com/gp/bestsellers/{category}, https://www.amazon.com/Best-Sellers/zgbs/{category}?pg=2}`
2. `wait stable`
3. Extract: `browser-act --session {name} eval "$(python scripts/extract-bestseller.py)"`

On error path, the script returns:
- `{"error": true, "message": "no bestseller cards found - is this a /bestsellers/, /gp/bestsellers/ or /zgbs/ page?"}` when `#gridItemRoot` selectors match zero cards (possibly wrong URL, or Amazon returned an interstitial)

Output example:
```json
{
  "categoryName": "Electronics",                       // parsed from document.title
  "categoryFullName": "Best Electronics",              // full title
  "categoryUrl": "https://www.amazon.com/gp/bestsellers/electronics",  // origin + pathname
  "currentPage": 1,                                    // page from .a-pagination .a-selected, defaults 1
  "hasNextPage": true,                                 // true when 'Next page' pagination link exists
  "nextPageUrl": "https://www.amazon.com/Best-Sellers/zgbs/electronics/?pg=2",  // absolute URL, null when last page
  "itemCount": 30,                                     // typically 30 per page
  "items": [
    {
      "rank": 1,                                       // extracted from .zg-bdg-text (e.g. "#1"), falls back to grid index
      "asin": "B08JHCVHTY",                            // 10-char ASIN from data-asin
      "title": "blink plus plan with monthly auto-renewal",  // truncated title from p13n-sc-css-line-clamp
      "url": "https://www.amazon.com/Blink-Plus-Plan-monthly-auto-renewal/dp/B08JHCVHTY/...",  // absolute product URL
      "image": "https://images-na.ssl-images-amazon.com/images/I/31...png",  // thumbnail
      "imageAlt": "blink plus plan with monthly auto-renewal",  // img alt
      "price": {"value": 11.99, "currencyRaw": "$", "raw": "$11.99"},  // null when not shown
      "stars": 4.4,                                    // 0-5 rating, null when no reviews
      "reviewCount": 277638,                           // total ratings, null when absent
      "ratingRaw": "4.4 out of 5 stars"                // full a11y text
    }
  ]
}
```

## Pagination

**URL Pagination**: Amazon bestseller pages use `?pg={N}` (starting at 1, typically pages 1-2 with 30 cards each = top 50). To iterate:

1. Read `nextPageUrl` from the output (already absolute) OR append/replace `?pg={N+1}` in the URL
2. `navigate {nextPageUrl}` → `wait stable` → re-run extraction script
3. Termination: `hasNextPage == false` in output, OR extracted ranks stop advancing beyond top 50 (Amazon caps bestseller lists at top 100 for most categories with pages 1 and 2)

## Success Criteria

`response.itemCount >= 1 AND response.items[0].asin matches /^[A-Z0-9]{10}$/ AND response.items[0].rank >= 1`

## Known Limitations

- Amazon bestseller lists cap at top 100 products (page 1: ranks 1-30 on ~/gp/bestsellers/, page 2: ranks 31-50; for /zgbs/ deeper pages up to 100). Beyond that no more data is available.
- Rank number is the current-moment position; capturing it repeatedly over time yields a rank history.
- `stars` and `reviewCount` on bestseller cards reflect the same snapshot Amazon shows in the chart, but Amazon updates chart data with a lag.
- Prices reflect the browsing session's country; use proxies for country-specific chart data.
- When Amazon shows a chart interstitial or gate (rare, region-dependent), the extractor returns `error: no bestseller cards found` — check the page state before retrying.

## Execution Efficiency

- **Batch orchestration**: Iterate categories serially in one browser session with 3-6 second delays between navigations. For higher throughput, open multiple stealth sessions with different fingerprints/proxies and shard categories across them.
- **Test before batch execution**: Test with 1-2 categories before running against many. Never skip testing.
- **Reduce redundant pre-operations**: Reuse the browser session across categories — no need to re-open.
- **Error resumption**: Persist per-category JSON as it completes so partial crashes resume from the failed category.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/amazon-scraper-amazon-bestseller-listing.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
