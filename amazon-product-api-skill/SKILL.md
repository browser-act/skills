---
name: amazon-product-api-skill
description: "This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications. Use this skill when users want to search for products on Amazon, find the best selling brand products, track price changes for items, get a list of categories with high ratings, compare different brand products on Amazon, extract Amazon product data for market research, look for products in a specific language or marketplace, analyze competitor pricing for keywords, find featured products for search terms, get technical specifications like material or color for product lists."
---

# Amazon Product Search Skill

## 📖 Introduction
This skill utilizes BrowserAct's Amazon Product API template to extract structured product listings from Amazon search results. It provides detailed information including titles, ASINs, prices, ratings, and product specifications, enabling efficient market research and product monitoring without manual data collection.

## ✨ Features
1. **No Hallucinations, Reliable Data**: Uses a pre-defined workflow to ensure accurate data extraction without AI-generated errors.
2. **No CAPTCHA Challenges**: Built-in mechanisms bypass reCAPTCHA and other bot detection systems.
3. **Global Access, No Geo-fencing**: Overcomes IP restrictions to ensure stable access from any location.
4. **Fast Execution**: More efficient than general-purpose AI browser automation.
5. **Cost-Effective**: Reduces data acquisition costs compared to high-token consumption AI models.

## 🔑 API Key Workflow
Before running the skill, the `BROWSERACT_API_KEY` environment variable must be checked. If it is not set, do not proceed; instead, request the key from the user.
**Agent Instruction**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it here."

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

## 🚀 Usage (Recommended)
The agent should execute the following script to get results in one command:

```bash
# Example Usage
python -u ./scripts/amazon_product_api.py "keywords" "brand" pages "language"
```

### ⏳ Progress Monitoring
Since this task involves automated browser operations, it may take a few minutes. The script outputs real-time timestamped status logs (e.g., `[14:30:05] Task Status: running`).
**Agent Note**:
- Monitor the terminal output while waiting for results.
- As long as new status logs are appearing, the task is running normally.
- Only consider retrying if the status remains unchanged for a long period or the script stops without output.

## 📊 Output Data Description
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

## ⚠️ Error Handling & Retry Mechanism
If an error occurs during execution, the agent should follow this logic:

1. **Check Output**:
   - If the output contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**; ask the user to provide a valid key.
   - If the output does not contain `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the agent should **automatically retry once**.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If it fails again, stop and report the error to the user.

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
