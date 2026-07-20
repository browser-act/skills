---
name: 1688-product-detail
description: "Extracts comprehensive wholesale product data from 1688.com product detail pages: title, tiered pricing, SKU variants with dimensions/weight, product images, seller info, shop scores, buyer protection, cross-border flags, product attributes, coupon/promotion data, and review stats. Use when user mentions 1688, 1688.com, wholesale China, alibaba wholesale, B2B China sourcing, Chinese wholesale scraper, 1688 product scrape, 1688 offer, 1688 detail, extract 1688 data, pull 1688 listings, get wholesale price, 1688 supplier info, factory stats 1688, 1688 SKU variants, 1688 product attributes, 1688 shop score, DSR score 1688, 1688 buyer protection, 1688 cross-border, 1688 dropship. Also applies to: scraping bulk product data from 1688 by offer ID list, monitoring 1688 supplier metrics, extracting 1688 pricing tiers for resale analysis."
---

# 1688.com — Product Detail Extraction

> Navigate to a 1688 product page → extract 50+ fields including pricing tiers, SKU variants, seller stats, attributes, promotions

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete wholesale product data from a 1688.com offer detail page using embedded page data and network capture for supplier metrics.

## Prerequisites

- Target product detail page is open in the browser: `https://detail.1688.com/offer/{offer_id}.html`
- No login required for product detail pages (data is publicly accessible)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: Extract core product data (title, pricing, images, seller, flags)

After navigating to the product page and waiting for page load:

`eval "$(python scripts/extract-product-detail.py '{offer_id}')"`

Parameters:
- offer_id: Numeric 1688 offer/product ID (e.g., `927875250705`)

Output example:
```json
{
  "offerId": "927875250705",
  "title": "新款苹果18promax手机壳磁吸...",
  "unit": "个",
  "category": { "topCategoryId": 7, "postCategoryId": 132918005 },
  "pricing": {
    "tiers": [
      { "minQty": "30", "price": "7.99" },
      { "minQty": "100", "price": "7.79" }
    ],
    "priceDisplayType": "range",
    "minOrderQty": 30,
    "currency": "CNY"
  },
  "sales": {
    "totalSold": 308417,
    "displaySaleNum": "10万+",
    "saleCountLabel": "全网销量"
  },
  "images": ["https://cbu01.alicdn.com/img/ibank/...jpg"],
  "attributes": {
    "材质": "优质TPU",
    "款式": "后盖款",
    "功能": "防震,磁吸,防磨,防摔",
    "适用型号": "iPhone17,iphone17pro..."
  },
  "skuCount": 339,
  "skuWeightData": [
    { "weight": 40, "length": 17, "width": 7, "height": 1, "volume": 119 }
  ],
  "seller": {
    "companyName": "佛山市南海区三丰手机配件有限公司",
    "loginId": "fssf06",
    "memberId": "b2b-2850655109d72ea",
    "userId": 2850655109,
    "shopUrl": "https://shop1460393846166.1688.com",
    "cardType": "cjgc",
    "isPmPlus": true,
    "serviceScore": "4.5分",
    "buyerRepeatRate": "65.82%"
  },
  "offerFlags": {
    "isSkuOffer": true,
    "isPreSell": false,
    "isConsignMarketOffer": true,
    "isDistribution": true,
    "isChtOffer": true,
    "isBuyerProtection": true
  },
  "crossBorder": {
    "foreignLanguagePackageAvailable": true,
    "boxMarkAvailable": true,
    "fbaLabelAvailable": true
  },
  "guarantees": ["买家保障", "正品保障"],
  "descriptionUrl": "https://detail.1688.com/...",
  "offerMemberTags": [4336705, 519170],
  "sellerWinportUrlMap": {}
}
```

### DOM: Extract SKU variants (color/model combinations with weight/dimensions)

`eval "$(python scripts/extract-sku-details.py '{offer_id}')"`

Parameters:
- offer_id: Numeric 1688 offer/product ID

Output example:
```json
{
  "offerId": "927875250705",
  "skuCount": 339,
  "skuRangePrices": [
    { "price": "7.99", "beginAmount": "30" },
    { "price": "7.79", "beginAmount": "100" }
  ],
  "skus": [
    {
      "skuId": 5833485852524,
      "specId": "...",
      "attrs": { "颜色": "黑色", "适用型号": "iPhone17" },
      "saleCount": 0,
      "canBookCount": 9999,
      "isPromotionSku": false,
      "packInfo": { "weight": 40, "length": 17, "width": 7, "height": 1, "volume": 119 }
    }
  ],
  "skuImageMap": {}
}
```

### DOM: Extract coupon and promotion data

`eval "$(python scripts/extract-promotions.py '{offer_id}')"`

Parameters:
- offer_id: Numeric 1688 offer/product ID

Output example:
```json
{
  "offerId": "927875250705",
  "coupons": [
    { "couponType": "INTERACT", "couponContent": "满100减5券" }
  ],
  "promotionModel": {
    "buttonName": "领券",
    "promotionList": [
      {
        "type": "INTERACT",
        "name": "互动优惠券",
        "summary": "入会有礼券",
        "promotionItems": [
          {
            "label": "满100减5券",
            "availablePeriod": "有效期：2026.05.28 00:00:00-2026.11.24 23:59:59",
            "canApply": true
          }
        ]
      }
    ]
  },
  "activity": {
    "activityType": null,
    "activityName": null,
    "activityUrl": null,
    "countdown": null,
    "activityId": null
  },
  "bannerImage": ""
}
```

### DOM: Extract seller params (for shopcard network capture)

`eval "$(python scripts/extract-seller-params.py '{offer_id}')"`

Parameters:
- offer_id: Numeric 1688 offer/product ID

Output example:
```json
{
  "offerId": "927875250705",
  "seller": {
    "companyName": "佛山市南海区三丰手机配件有限公司",
    "loginId": "fssf06",
    "memberId": "b2b-2850655109d72ea",
    "userId": 2850655109,
    "shopUrl": "https://shop1460393846166.1688.com",
    "cardType": "cjgc",
    "serviceScore": "4.5分",
    "buyerRepeatRate3m": "65.82%"
  },
  "shopcardParams": {
    "offerId": "927875250705",
    "userId": 0,
    "offerMemberTags": [4336705, 519170, "..."],
    "sellerUserId": 2850655109,
    "sellerMemberId": "b2b-2850655109d72ea",
    "topCategoryId": 7,
    "offerModelSign": { "isBuyerProtection": true, "isDistribution": true },
    "sellerIdentity": "cjgc",
    "sellerWinportUrlMap": { "indexUrl": "...", "defaultUrl": "..." },
    "winportUrl": "https://shop1460393846166.1688.com"
  }
}
```

### Network Capture: Get shop scores and metrics (shopcard API)

The shopcard API uses dynamic `sign` tokens — let the page JS handle it, read from network traffic.

After the product detail page loads fully (wait stable), the shopcard request fires automatically:

1. `wait stable`
2. `network requests --type xhr,fetch --filter h5api.m.1688.com`
3. Find request with URL containing `mtop.1688.moga.pc.shopcard`
4. `network request <id>`

Endpoint characteristic: URL contains `mtop.1688.moga.pc.shopcard`

If the shopcard request is not in traffic (navigated away or cleared), reload the product page:
1. `navigate https://detail.1688.com/offer/{offer_id}.html`
2. `wait stable`
3. Repeat steps 2–4 above

Error handling: If request not found after page reload, check if the product page loaded correctly (screenshot), then retry once. If still unavailable, shopcard data is unavailable for this offer.

Output example:
```json
{
  "api": "mtop.1688.moga.pc.shopcard",
  "data": {
    "model": {
      "shopName": "佛山市南海区三丰手机配件有限公司",
      "shopType": "cjgc",
      "iconType": "cjgc",
      "mainCategoryName": "手机配件",
      "shopUrl": "https://shop1460393846166.1688.com",
      "tpYear": 11,
      "shopData": [
        { "dataKey": "店铺回头率", "dataValue": "66%" },
        { "dataKey": "店铺服务分", "dataValue": "4.5", "unit": "分" },
        { "dataKey": "准时发货率", "dataValue": "- %" },
        { "dataKey": "店铺好评率", "dataValue": "99.9%" }
      ],
      "shopButton": {
        "fuzzyFavCount": "8.6k粉丝",
        "attentionRelation": false
      }
    }
  }
}
```

### Network Capture: Get DSR review summary (queryDsrRateDataV2 API)

After page load, the DSR scores request fires automatically alongside shopcard:

1. `wait stable`
2. `network requests --type xhr,fetch --filter h5api.m.1688.com`
3. Find request with URL containing `querydsrratedatav2`
4. `network request <id>`

Endpoint characteristic: URL contains `mtoprateservice.querydsrratedatav2`

Error handling: Same as shopcard — if not found, navigate to the product page and retry. The DSR API fires with the POST param `loginId` = seller loginId and `offerId`; both come from `extract-seller-params.py` output.

Output example:
```json
{
  "data": {
    "model": {
      "goodRates": 99.9,
      "goodsGrade": 5.0,
      "fulfillmentDataList": [
        { "name": "商品好评", "value": "100%" },
        { "name": "按时发货" },
        { "name": "商品退款" }
      ],
      "commonTagNodeList": [
        { "name": "全部", "count": 2497 },
        { "name": "有图", "count": 6 },
        { "name": "好评", "count": 2494 }
      ],
      "impressionTagNodeList": [
        { "name": "价格很便宜", "count": 6 },
        { "name": "质量很好", "count": 5 }
      ]
    }
  }
}
```

### Composite: Full product data extraction

Combines DOM extraction with network capture for complete data. For each offer ID:

1. `navigate https://detail.1688.com/offer/{offer_id}.html`
2. `wait stable`
3. `eval "$(python scripts/extract-product-detail.py '{offer_id}')"` → core data
4. `eval "$(python scripts/extract-sku-details.py '{offer_id}')"` → SKU variants
5. `eval "$(python scripts/extract-promotions.py '{offer_id}')"` → coupons/activity
6. `network requests --type xhr,fetch --filter h5api.m.1688.com` → locate shopcard and DSR requests
7. `network request <shopcard_request_id>` → shop scores
8. `network request <dsr_request_id>` → review stats
9. Merge all results by offerId

## Enum Parameters

shop type [collection failed]: `cardType` values (e.g., `cjgc`, `cht`) come from page data but no separate enumeration API found; values depend on seller registration type

## Pagination

Not applicable — this is a single-product detail extraction capability. For bulk processing, see Execution Efficiency below.

## Success Criteria

`extract-product-detail.py` output has no `error` field AND `title` is non-null AND `pricing.tiers` length >= 1

## Known Limitations

- Search functionality (`s.1688.com`) requires login/CN IP — this Skill covers detail pages only (publicly accessible by offer ID)
- Shopcard API (`mtop.1688.moga.pc.shopcard`) may return empty `shopData` for some offer types or if the session has expired; navigate to the product page to refresh
- `productAttributes` DOM module has a server-side rendering bug (JSONArray cast error in page metadata) — attributes are extracted from DOM fallback selectors instead
- `freightInfo.totalCost` (shipping cost) comes from the freight API which requires `sendAddressCode` and `receiveAddressCode`; defaults to sender's registered address; not included in composite extraction due to address dependency
- Review list detail (`queryItemRatedListV2`) returns paginated individual reviews but is not included in composite — use the DSR summary instead

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through offer IDs serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 2–3 second intervals between products. To increase throughput, open multiple stealth browser sessions and distribute offers across them.
- **Test before batch execution**: After writing a batch script, first test with 1–2 offer IDs to verify script runs correctly; only then run the full batch.
- **Reduce redundant pre-operations**: When processing multiple offers, keep the session open; don't re-launch browser-act for each offer.
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over.

## Experience Notes

Path: `{working_directory}/browser-act-skill-forge-memories/1688-wholesale-scraper-1688-product-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
