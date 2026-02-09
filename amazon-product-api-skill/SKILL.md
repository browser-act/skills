---
name: amazon-product-api-skill
description: Extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications. Use this skill when users want to search for products on Amazon, find the best selling brand products, track price changes for items, get a list of categories with high ratings, compare different brand products on Amazon, extract Amazon product data for market research, look for products in a specific language or marketplace, analyze competitor pricing for keywords, find featured products for search terms, get technical specifications like material or color for product lists.
---

# Amazon Product API Skill

This skill allows you to extract structured product data from Amazon search results using a single API request, eliminating the need for complex scrapers or manual data entry.

## ✨ Features

- **One-call integration**: Send product results directly into your pricing database, BI dashboards, competitor trackers, or automation workflows via API.
- **Zero maintenance**: No scraping scripts, proxy setup, or anti-bot handling required.
- **Production-ready output**: Consistent, structured responses designed for automated processing and monitoring.
- **Built for workflows**: Perfect for competitive pricing, product research, catalog monitoring, and merchandising insights.

## 🔑 API Key Setup

This skill requires a `BROWSERACT_API_KEY`. 

### Environment Variable Check
The associated script will automatically check for the `BROWSERACT_API_KEY` environment variable.

### How to get an API Key
1. Register/Login at [BrowserAct](https://www.browseract.com/).
2. Go to the [API & Integrations](https://www.browseract.com/reception/integrations) section to get your key.
3. Set it in your environment:
   ```powershell
   $env:BROWSERACT_API_KEY = "your-api-key-here"
   ```

## 📥 Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `KeyWords` | string | Search keywords used to find products on Amazon. | `phone`, `wireless earbuds` |
| `Brand` | string | Filter products by brand name. | `Apple`, `Samsung`, `Sony` |
| `Maximum_number_of_page_turns` | number | Number of search result pages to paginate through. | `1`, `3` |
| `language` | string | UI language for the Amazon browsing session. | `en`, `de`, `zh-CN` |

## 🚀 How to Call

You can trigger this skill using the provided Python script:

```bash
python -u .cursor/skills/amazon-product-api-skill/scripts/amazon_product_api.py --keywords "laptop" --brand "Dell" --pages 1 --lang "en"
```

## 📊 Output Data

The script returns a JSON array of products with the following fields:

- `product_title`: The product name.
- `asin`: Amazon Standard Identification Number (unique ID).
- `product_url`: The product detail page URL.
- `brand`: Brand name.
- `price_current_amount`: Current selling price.
- `price_original_amount`: Original price (if available).
- `rating_average`: Average star rating.
- `rating_count`: Total number of ratings.
- `featured`: Whether it's a sponsored/featured item.
- `color`, `material`, `style`: Product attributes (if available).

## 🛠 Error Handling & Retries

- **Invalid Authorization**: If the API key is incorrect or expired, the script will catch the "Invalid authorization" error and prompt you to check your configuration.
- **Network Issues**: The script includes built-in retry logic for common network timeouts.
- **Task Failures**: If the workflow fails on the server side, the script will report the failure status and any available error details.
