---
name: ebay-search-listing
description: "Extracts product listings from any eBay search or category page URL, returning per-item cards (itemNumber, url, title, subtitle, caption, price, priceWithCurrency, currency, wasPrice, bids, shipping, seller, sellerFeedbackCount, sellerPositiveRating, reviewsCount, starRating, image) plus pagination state (currentPage, nextPageUrl, hasNextPage, totalResultsApprox). Works across all eBay regional TLDs. Use when user mentions eBay, ebay.com, eBay scraper, eBay search results, eBay category page, eBay SRP, eBay product list, eBay item cards, scrape eBay listings, extract eBay items, eBay bulk products, eBay keyword search, eBay category scraper, eBay pagination, eBay startUrls, eBay items scraper, eBay marketplace scraping. Also applies to price comparison across marketplaces, competitive listing monitoring, category catalog audits, brand keyword tracking on eBay, and paginated bulk extraction of eBay item cards from a search or category URL."
---

# eBay — Search & Category Listing Extraction

> Input: any eBay search or category page URL → Output: paginated array of item cards (itemNumber, url, title, price, seller, image, etc.) plus pagination state (currentPage, nextPageUrl, hasNextPage, totalResultsApprox).

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given any eBay search results URL (SRP) or category URL, extract the visible product cards on the current page with their key surface fields, and expose pagination state so a caller can loop pages until an item cap or the last page is reached.

## Prerequisites

- Target page is already open in the browser: `https://www.ebay.{tld}/sch/i.html?_nkw={keyword}` (search) or `https://www.ebay.{tld}/b/{category-slug}/{category-id}/bn_...` (category), where `{tld}` is any eBay regional TLD (`com`, `co.uk`, `de`, `fr`, `it`, `es`, `com.au`, `ca`, `co.jp`, `com.hk`, `in`, `ph`, `pl`, `nl`, `ie`, `at`, `be`).
- No login is required for public listings. Extraction runs against whatever the anonymous browser session sees.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting.

### DOM: extract item cards from the current search or category page

Precondition: `navigate {search or category URL}` → `wait stable` first.

Extract: `eval "$(python scripts/extract-listing.py --max-items 0)"`

Parameters:
- `--max-items`: Cap on cards returned from the current page. `0` (default) returns every card on the page. Use a positive integer when the caller only wants the top-N of the current page (does not affect pagination state).

Output example:
```json
{
  "currentUrl": "https://www.ebay.com/sch/i.html?_nkw=headphones&LH_BIN=1",  // page URL as observed
  "hostname": "www.ebay.com",                       // regional domain of the current page
  "currentPage": 1,                                 // 1 when the URL has no _pgn param
  "nextPageUrl": "https://www.ebay.com/sch/i.html?_nkw=headphones&LH_BIN=1&_pgn=2",  // null when on last page
  "hasNextPage": true,                              // false = last page reached
  "totalResultsApprox": 250000,                     // parsed from the results-count heading; null if not shown
  "totalResultsRaw": "250,000+ results for headphones",  // original heading text
  "itemsOnPage": 60,                                // eBay default is 60 per page; can be overridden by _ipg URL param
  "returnedCount": 3,                               // number of items in the "items" array below (respects --max-items)
  "items": [
    {
      "itemNumber": "195486024424",                 // eBay listing id (also from data-listingid on the card)
      "url": "https://www.ebay.com/itm/195486024424",  // canonical item URL, query params stripped
      "title": "Plugfones Guardian OSHA Certified earplug with audio Work Headphones earbuds",
      "subtitle": "Brand New",                      // condition / seller-type badge; null when absent
      "caption": null,                              // e.g. "New Listing", "Sold Jul 7, 2026"; null when absent
      "price": 24.99,                               // parsed numeric price
      "priceWithCurrency": "$24.99",                // original price string
      "currency": "USD",                            // ISO code detected from price prefix
      "wasPrice": null,                             // original / strikethrough price if shown
      "wasPriceWithCurrency": null,
      "bids": null,                                 // auction bid count; null for BIN listings
      "shipping": "+$12.99 delivery",               // shipping-row text as displayed; null when absent
      "seller": "plugfones",                        // seller username
      "sellerRawText": "plugfones 99.7% positive (15.9K)",  // original seller badge text
      "sellerFeedbackCount": 159000,                // parsed from (15.9K); handles K suffix
      "sellerPositiveRating": 99.7,                 // percentage as float
      "reviewsCount": null,                         // product-review count when displayed on the card
      "starRating": null,                           // 0-5 star rating when displayed
      "image": "https://i.ebayimg.com/images/g/PbYAAOSwuHdjcqCX/s-l1600.webp"  // upgraded to s-l1600 for the largest available crop
    }
  ]
}
```

Error handling:
- When `.srp-results > li.s-card` matches zero elements, the script returns `{"error": true, "message": "no item cards found ..."}`. Root causes: the page navigated to an item detail (URL contains `/itm/`), an anti-bot interstitial is shown, or eBay changed the class prefix. Take a `screenshot` first, verify the URL is still an SRP or category page, then retry.
- When the browser is fingerprinted and eBay serves a captcha page, follow the standard captcha escalation (`solve-captcha`, headed handoff, `remote-assist`).

## Pagination

**URL Pagination**: URL pattern `?_pgn={page}` (append `&_pgn=N` to any search or category URL; page 1 = no param, or `_pgn=1`). eBay's default page size is 60 items; add `&_ipg={size}` (accepted values include `60`, `120`, `240`) to change it. Next-page detection selector: `a.pagination__next`, exposed by the extractor as `nextPageUrl` / `hasNextPage`. Termination: `hasNextPage === false`, or the caller-supplied item cap is reached, or a page returns zero items.

Loop skeleton (bash pseudocode):
```
url="{startUrl}"
collected=0
maxItems={caller-cap}
while [ -n "$url" ]; do
  browser-act --session {name} navigate "$url"
  browser-act --session {name} wait stable
  page=$(browser-act --session {name} eval "$(python scripts/extract-listing.py --max-items 0)")
  # append page.items to output, respecting maxItems
  next=$(echo "$page" | jq -r '.nextPageUrl // empty')
  hasNext=$(echo "$page" | jq -r '.hasNextPage')
  [ "$hasNext" = "true" ] || break
  [ "$collected" -ge "$maxItems" ] && break
  url="$next"
done
```

## Success Criteria

`returnedCount >= 1` on any non-empty search / category page, and `error` field is absent. Card-level: `itemNumber` and `url` are non-null for every returned card (title is normally non-null but can be empty for restricted or ended listings — that is a page-side condition, not a scraper failure).

## Known Limitations

- eBay regional geo-redirection: navigating to `ebay.com` from a non-US IP may land on the local domain (e.g., `ebay.de`, `ebay.co.uk`). The extractor is locale-agnostic (selectors are the same across TLDs, currency and text-suffix cleanup handle multiple languages), but the `hostname` field will reflect the final URL — inspect `hostname` and `currentUrl` when the target domain matters.
- Filters like `LH_Sold=1&LH_Complete=1` (sold / completed listings), `LH_BIN=1` (Buy It Now), `LH_Auction=1`, `_udhi` / `_udlo` (price range), `_sop` (sort order) etc. are passed through the URL — the caller sets them on the input URL; the extractor does not enumerate them.
- Promoted / "you may also like" carousels that appear outside `.srp-results` are intentionally excluded to keep the returned list aligned with the main SRP feed.
- Product-review count and star rating on cards depend on eBay attaching a matching product page to the listing; many listings have neither and return `null`.
- `bids` is parsed from the card's attribute row when present; auction-type listings expose it, BIN listings do not.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop pages serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Between pages, insert a `wait stable` before extracting; a small sleep (1–3s) between page fetches keeps the traffic pattern natural. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session.
- **Test before batch execution**: After writing a batch script, first test with 1–2 pages to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: Reuse the same browser session across many pages of the same query; do not re-open the browser per page.
- **Error resumption**: Save results page by page during batch processing (e.g., `tmp/pages/{query}-p{n}.json`); on failure, resume from the next page rather than starting over.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ebay-scraper-ebay-search-listing.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
