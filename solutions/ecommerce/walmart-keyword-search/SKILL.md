---
name: walmart-keyword-search
description: "Walmart keyword search scraper: input a search keyword and page number, navigate to walmart.com search results, extract paginated product listings with itemId, url, title, brand, image, price, wasPrice, rating, reviewCount, availability, seller info, fulfillmentBadge, classType, and shortDescription. Use when user mentions walmart search, walmart keyword search, search walmart products, scrape walmart search results, walmart search scraper, walmart product search, search items on walmart, walmart search by keyword, walmart product listing, get walmart search data, extract walmart products, walmart search results scraper, walmart shop search, walmart catalog search, walmart product list by keyword, walmart browse by keyword. Also applies to price comparison research on walmart, finding walmart product URLs in bulk, monitoring walmart search rankings, collecting walmart product data by category keyword."
---

# Walmart — Keyword Search Listing

> keyword + page → paginated product list from walmart.com search results

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract product listings from Walmart's keyword search results page, returning structured item data with pricing, rating, availability, and seller info.

## Prerequisites

- Target search page is open in the browser: `https://www.walmart.com/search?q={keyword}&page={page}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract product listing from current search page

Navigate to the target search URL first, then extract:

1. `navigate "https://www.walmart.com/search?q={keyword}&page={page}&sort={sort}"`
2. `wait stable`
3. `eval "$(python scripts/extract-listing.py)"`

Parameters in URL:
- `{keyword}`: URL-encoded search keyword (e.g., `laptop`, `apple+iphone`, `running+shoes`)
- `{page}`: page number, starting from `1`
- `{sort}`: sort order — `best_match` (default), `price_low`, `price_high`, `rating_high`, `new`

Output example:
```json
{
  "pageType": "SearchPage",
  "query": "laptop",
  "currentPage": 1,
  "totalCount": 16174,
  "maxPage": 12,
  "itemCount": 57,
  "items": [
    {
      "itemId": "18656507313",
      "url": "https://www.walmart.com/ip/HP-14-N150-4-128-Blue/18656507313",
      "title": "HP 14 inch HD Windows Laptop Intel Processor N150 4GB 128GB UFS Waterfall Blue",
      "brand": null,
      "image": "https://i5.walmartimages.com/seo/HP-14.jpeg",
      "price": 229,
      "priceString": "$229.00",
      "wasPrice": null,
      "rating": 4.2,
      "reviewCount": 274,
      "availability": "IN_STOCK",
      "availabilityText": "In stock",
      "sellerName": "Walmart.com",
      "sellerType": null,
      "fulfillmentBadge": null,
      "classType": "VARIANT",
      "shortDescription": null
    }
  ]
}
```

Error response (when extraction fails or wrong page):
```json
{"error": true, "message": "No searchResult in __NEXT_DATA__. Ensure the page is fully loaded at the correct search URL."}
```

## Enum Parameters

`sort` [collection failed]: URL parameter values observed during exploration: `best_match`, `price_low`, `price_high`, `rating_high`, `new`. Full enum list not exposed via API or DOM; additional values may exist.

## Pagination

**URL Pagination**: URL pattern `https://www.walmart.com/search?q={keyword}&page={N}&sort={sort}`. Increment `page` by 1 each iteration. Termination: `page > maxPage` (from response `maxPage` field) OR `itemCount === 0`. Note: Walmart caps search results at `maxPage` (typically 11–25 pages max regardless of `totalCount`).

## Success Criteria

`itemCount >= 1` AND `items[0].itemId` is non-null AND `items[0].url` starts with `https://www.walmart.com/ip/`

## Known Limitations

- Walmart limits search pagination to at most ~25 pages regardless of total result count
- `brand` field is null for many items in search listing (available in product detail)
- `shortDescription` is null for most non-food items in search listing
- `wasPrice` is null unless the item has an active markdown/rollback
- `sellerType` is null for Walmart.com first-party listings

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through keywords serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 1–2 second intervals between page navigations. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/walmart-scraper-walmart-keyword-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
