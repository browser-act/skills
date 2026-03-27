---
name: amazon-product-api-skill
description: "This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications. Use this skill when users want to search for products on Amazon, find the best selling brand products, track price changes for items, get a list of categories with high ratings, compare different brand products on Amazon, extract Amazon product data for market research, look for products in a specific language or marketplace, analyze competitor pricing for keywords, find featured products for search terms, get technical specifications like material or color for product lists."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Product Search Skill

## 📖 Introduction
This skill utilizes BrowserAct's Amazon Product API template to extract structured product listings from Amazon search results. It provides detailed information including titles, ASINs, prices, ratings, and product specifications, enabling efficient market research and product monitoring without manual data collection.

## ✨ Features
1. **No Hallucinations**: Pre-set workflows avoid AI generative hallucinations, ensuring stable and precise data extraction.
2. **No Captcha Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions**: No need to handle regional IP restrictions or geofencing.
4. **Faster Execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **Cost-Effective**: Significantly lowers data acquisition costs compared to high-token-consuming AI solutions.

## 🔑 API Key Setup
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other measures; ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please visit the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
The agent should configure the following parameters based on user requirements:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Search keywords used to find products on Amazon.
   - **Required**: Yes
   - **Example**: `laptop`, `wireless earbuds`

2. **Brand**
   - **Type**: `string`
   - **Description**: Filter products by brand name.
   - **Default**: `Apple`
   - **Example**: `Dell`, `Samsung`

3. **Maximum_number_of_page_turns**
   - **Type**: `number`
   - **Description**: Number of search result pages to paginate through.
   - **Default**: `1`

4. **language**
   - **Type**: `string`
   - **Description**: UI language for the Amazon browsing session.
   - **Default**: `en`
   - **Example**: `zh-CN`, `de`

## 🚀 Usage
Agent should use the following independent script to achieve "one-line command result":

```bash
# Example Usage
python -u ./scripts/amazon_product_api.py "keywords" "brand" pages "language"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
Upon success, the script parses and prints the structured product data from the API response, which includes:
- `product_title`: Full title of the product.
- `asin`: Amazon Standard Identification Number.
- `product_url`: URL of the Amazon product page.
- `brand`: Brand name.
- `price_current_amount`: Current price.
- `price_original_amount`: Original price (if applicable).
- `rating_average`: Average star rating.
- `rating_count`: Total number of ratings.
- `featured`: Badges like "Best Seller" or "Amazon's Choice".
- `color`, `material`, `style`: Product attributes (if available).

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Market Research**: Search for a specific product category to analyze top brands and pricing.
2. **Competitor Monitoring**: Track product listings and price changes for specific competitor brands.
3. **Product Catalog Enrichment**: Extract structured details like ASINs and specifications to build or update a product database.
4. **Rating Analysis**: Find high-rated products for specific keywords to identify market leaders.
5. **Localized Research**: Search Amazon in different languages to analyze international markets.
6. **Price Tracking**: Monitor current and original prices to identify discount trends.
7. **Brand Performance**: Evaluate the presence of a specific brand in search results across multiple pages.
8. **Attribute Extraction**: Gather technical specifications like material or color for a list of products.
9. **Lead Generation**: Identify popular products and their manufacturers for business outreach.
10. **Automated Data Feed**: Periodically pull Amazon search results into external BI tools or dashboards.
