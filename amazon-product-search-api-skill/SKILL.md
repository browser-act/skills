---
name: amazon-product-search-api-skill
description: This skill is designed to help users automatically extract product data from Amazon search results. The Agent should proactively apply this skill when users request: 1. Search for products related to [keyword]; 2. Find best-selling items from [brand]; 3. Monitor product prices and availability on Amazon; 4. Extract product listings for market research; 5. Collect product ratings and review counts for competitive analysis; 6. Find specific products with a maximum count of [number]; 7. Search Amazon in [language] for localized results; 8. Track monthly sales estimates for [brand] products; 9. Gather product URLs and titles for a product catalog; 10. Scan Amazon for "Best Seller" tags in a specific category; 11. Monitor shipping and delivery information for [brand] items; 12. Build a structured dataset of Amazon search results.
---

# Amazon Product Search Automation Skill

## 📖 Introduction
This skill provides a one-stop product data collection service through BrowserAct's Amazon Product Search API template. It directly extracts structured product results from Amazon search lists. Simply input search keywords, brand filters, and quantity limits to get clean, usable product data.

## ✨ Features
1. **No Hallucinations, Ensuring Stable and Accurate Data Extraction**: Preset workflows avoid AI generative hallucinations.
2. **No CAPTCHA Issues**: Built-in bypass mechanisms, no need to handle reCAPTCHA or other verification challenges.
3. **No IP Access Restrictions or Geofencing**: Breaks through regional IP restrictions to ensure stable global access.
4. **Faster Execution Speed**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **High Cost-Efficiency**: Significantly reduces data acquisition costs compared to high-token-consuming AI solutions.

## 🔑 API Key Guidance
Before running, check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other measures; instead, request and wait for the user to provide it.
**The Agent must inform the user at this point**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this dialog."

## 🛠️ Input Parameters Detail
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The keywords the user wants to search for on Amazon.
   - **Example**: `phone`, `wireless earbuds`, `laptop stand`

2. **Brand (Brand Filter)**
   - **Type**: `string`
   - **Description**: Filter products by brand name shown in the listing.
   - **Example**: `Apple`, `Samsung`, `Sony`

3. **Maximum_date (Maximum Products)**
   - **Type**: `number`
   - **Description**: The maximum number of products to extract across paginated search results.
   - **Default**: `50`

4. **language (UI Language)**
   - **Type**: `string`
   - **Description**: UI language for the Amazon browsing session.
   - **Options**: `en`, `de`, `fr`, `it`, `es`, `ja`, `zh-CN`, `zh-TW`
   - **Default**: `en`

## 🚀 Call Method (Recommended)
The Agent should execute the following independent script to achieve "one-line command for results":

```bash
# Example Call
python -u ./.cursor/skills/amazon-product-search-api-skill/scripts/amazon_product_search_api.py "Keywords" "Brand" Quantity "language"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent Notes**:
- Keep an eye on the terminal output while waiting for the script to return results.
- As long as the terminal is outputting new status logs, the task is running normally; do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning results, consider triggering a retry mechanism.

## 📊 Output Data Description
After successful execution, the script will parse and print results directly from the API response. Results include:
- `product_title`: Product name
- `product_url`: Detail page URL
- `rating_score`: Average star rating
- `review_count`: Total number of reviews
- `monthly_sales`: Estimated monthly sales (if available)
- `current_price`: Current selling price
- `list_price`: Original list price (if available)
- `delivery_info`: Delivery or fulfillment information
- `shipping_location`: Shipping origin or location
- `is_best_seller`: Whether marked as Best Seller
- `is_available`: Whether available for purchase

## ⚠️ Error Handling & Retry Mechanism
If an error is encountered during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, the API Key is invalid or expired. **Do not retry**; instead, guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute** the script once.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Market Research**: Search for "wireless earbuds" from "Sony" to analyze the current market.
2. **Competitive Monitoring**: Track "Samsung" phone prices and availability on Amazon.
3. **Catalog Discovery**: Gather product titles and URLs for a new product catalog in the "laptop stand" category.
4. **Localized Analysis**: Search Amazon in "ja" (Japanese) to understand products available in the Japan region.
5. **Best Seller Tracking**: Identify products marked as "Best Seller" for a specific brand.
6. **Pricing Intelligence**: Compare `current_price` and `list_price` to monitor discounts.
7. **Sales Trend Estimation**: Use `monthly_sales` data to estimate market demand for certain items.
8. **Shipping Efficiency Study**: Analyze `delivery_info` and `shipping_location` for various brands.
9. **Large-scale Data Extraction**: Collect up to 100 products for a comprehensive dataset.
10. **Product Availability Check**: Verify if specific brand products are currently `is_available` for purchase.
