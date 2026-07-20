---
name: etsy-keyword-search
description: "Etsy keyword search scraper: given a search keyword and optional page number, returns paginated product listings with listingId, shopId, title, url, image, salePrice, originalPrice, currency, rating, reviewCount, shopName, isAd, freeShipping, badge from etsy.com search results. Use when user mentions Etsy, etsy.com, Etsy search, search Etsy by keyword, scrape Etsy listings, extract Etsy products, Etsy product search, Etsy marketplace search, find products on Etsy, Etsy handmade search, Etsy vintage search, Etsy craft search, bulk Etsy product export, Etsy price monitoring, Etsy competitor research, Etsy top listings, Etsy bestseller extraction, Etsy sales data, Etsy shop discovery via keyword. Also applies to trend research on handmade or craft niches, competitor keyword ranking on Etsy, sourcing Etsy suppliers by product type, and any paginated bulk product collection driven by a search keyword."
---

# Etsy — Keyword Search

> Input a search keyword (and optional page number) → output paginated product listings from Etsy search results.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect product listings from Etsy's public keyword search results, one page at a time, with core fields per item.

## Prerequisites

- Target page is already open in the browser: `https://www.etsy.com/search?q={keyword}` (or navigate to it during execution)
- No login required — search results are public
- Browser session must survive anti-bot verification (DataDome). Best practice: navigate to `https://www.etsy.com/` first, then to the search URL, within an established stealth browser session

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Anti-bot Warm-up

If a fresh browser session was just created, before hitting the search URL directly:

1. `navigate https://www.etsy.com/` → `wait stable`
2. Then `navigate https://www.etsy.com/search?q={keyword}` → `wait stable`

Reason: hitting `/search` cold triggers DataDome CAPTCHA more often than hitting `/` first and following the same-origin flow.

If the extraction script returns `{"error": true, "message": "blocked by anti-bot verification page"}`, treat this as a hard block: stop execution and inform the user that the page is blocked by anti-bot verification and cannot proceed automatically.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract product listings from search results page

Prerequisite: the current page must be an Etsy search results page (`https://www.etsy.com/search?q={keyword}&page={page}`), already `wait stable`.

Extract: `eval "$(python scripts/extract-listings.py)"`

Output example:
```json
{
  "error": false,
  "url": "https://www.etsy.com/search?q=leather+wallet",  // page URL
  "currentPage": 1,                        // current page number parsed from URL, defaults 1
  "count": 57,                             // number of unique listings extracted
  "nextPageUrl": "https://www.etsy.com/search?q=leather+wallet&ref=pagination&page=2",  // URL of next page, null on last page
  "listings": [
    {
      "listingId": "547491922",            // Etsy listing id
      "shopId": "15980284",                // Etsy shop id
      "title": "Leather Wallet…",          // product title
      "url": "https://www.etsy.com/listing/547491922/leather-walletwalletman-leather",  // canonical listing URL, tracking params stripped
      "image": "https://i.etsystatic.com/…/il_794xN.….jpg",  // primary product image
      "salePrice": "$32.20",               // current display price (raw text with currency symbol)
      "originalPrice": "$80.50",           // original / crossed-out price, null when no discount
      "currency": "$",                     // currency symbol as shown to user
      "rating": 4.8,                       // average star rating, null when card shows none
      "reviewCount": "7.9k",               // review count as displayed (may include k/M suffix)
      "shopName": "TexasValleyLeather",    // shop / seller display name
      "isAd": true,                        // true when card is an advertised placement
      "freeShipping": false,               // true when "Free shipping" badge shown
      "badge": "Bestseller",               // ranked badge text (Bestseller / Etsy's Pick / Popular now / null)
      "positionIndex": 0                   // 0-based position within the page
    }
  ]
}
```

Error handling:
- `{"error": true, "message": "blocked by anti-bot verification page"}` — DataDome interstitial; retry warm-up in a stealth browser
- `{"error": true, "message": "no listing cards found on page"}` — either the search returned no matches or page not fully loaded; check page state and pagination

## Pagination

**URL Pagination**: URL pattern `https://www.etsy.com/search?q={keyword}&page={N}` where `{N}` starts at 1. Termination: navigate to `{N+1}`; if `count === 0` or the previous page's `nextPageUrl` was null, stop. Practical cap: Etsy search rarely exceeds page 250 for a single query.

## Success Criteria

`result.error === false && result.count >= 1 && result.listings.every(l => l.listingId && l.title && l.url)`

## Known Limitations

- DataDome anti-bot: cold cross-page navigation into `/search` may show a CAPTCHA interstitial. Mitigate by navigating to `/` first within the same stealth session, or by rotating proxy / browser fingerprint on repeated blocks
- `reviewCount` is returned as displayed text (e.g. `7.9k`, `17.6k`) rather than an exact integer, because Etsy's search cards themselves round large counts
- Sponsored (ad) placements appear alongside organic results and are marked with `isAd: true`; the listing itself is real, but its position is paid
- Etsy Offsite Ads anonymize the seller in the card text ("Ad from Etsy seller"); for such cards `shopName` returns `null` even though `isAd: true`. Resolve the true shop by navigating to the listing URL and running the product-detail capability if the shop identity is required
- Position within a page is what search personalization returned to this browser session; results may differ across proxies / logged-in accounts
- Some cards may render without price/rating text if the listing has variations with wide price spans or is newly listed; those fields fall back to `null`

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Insert 3-8 second sleeps between page navigations to mimic human browsing. To process multiple keywords, open separate browser sessions for each keyword
- **Test before batch execution**: After writing a batch script, first test with 1-2 pages of one keyword to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: Complete the `/` → search warm-up once per session, then loop pages within the same session
- **Error resumption**: Save each page's results to a file (e.g. `results/{keyword}-p{N}.json`) as soon as extraction succeeds; on failure, resume from the missing page rather than re-scraping from page 1

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/etsy-scraper-etsy-keyword-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
