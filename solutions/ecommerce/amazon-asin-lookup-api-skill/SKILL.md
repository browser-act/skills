---
name: amazon-asin-lookup-api-skill
description: "This skill helps users extract structured product details from Amazon using a specific ASIN (Amazon Standard Identification Number). Use this skill when the user asks to get Amazon product details by ASIN, lookup Amazon product title and price using ASIN, extract Amazon product ratings and reviews count for a specific ASIN, check Amazon product availability and current price, get Amazon product description and features via ASIN, enrich product catalog with Amazon data using ASIN, monitor Amazon product price changes for specific ASINs, retrieve Amazon product brand and material information, fetch Amazon product images and specifications by ASIN, validate Amazon ASIN and get product metadata."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon ASIN Lookup Skill

## 📖 Introduction
This skill utilizes BrowserAct's Amazon ASIN Lookup API template to provide a seamless way to retrieve comprehensive product information from Amazon. By simply providing an ASIN, you can extract structured data including title, price, ratings, brand, and detailed descriptions directly into your application without manual scraping.

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

1. **ASIN (Amazon Standard Identification Number)**
   - **Type**: `string`
   - **Description**: The unique identifier for the Amazon product.
   - **Required**: Yes
   - **Example**: `B07TS6R1SF`

## 🚀 Usage
The agent should execute the following script to get results in one command:

```bash
# Example Usage
python -u ./scripts/amazon_asin_lookup_api.py "ASIN_VALUE"
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
- `ASIN`: The provided ASIN.
- `product_url`: URL of the Amazon product page.
- `brand`: Brand name.
- `price_current_amount`: Current price.
- `price_original_amount`: Original price (if applicable).
- `price_discount_amount`: Discount amount (if applicable).
- `rating_average`: Average star rating.
- `rating_count`: Total number of ratings.
- `featured`: Badges like "Amazon's Choice".
- `color`: Color variant (if applicable).
- `compatible_devices`: List of compatible devices (if applicable).
- `product_description`: Full product description.
- `special_features`: Highlighted features.
- `style`: Style attribute (if applicable).
- `material`: Material used (if applicable).

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Product Data Enrichment**: Retrieve full details for a list of ASINs to update an e-commerce database.
2. **Price Comparison**: Lookup current Amazon prices for specific ASINs to compare with other retailers.
3. **Review Monitoring**: Track changes in rating averages and review counts for key products.
4. **Availability Checks**: Automatically verify if a specific product is currently in stock on Amazon.
5. **Brand Analysis**: Identify the brand and manufacturer of products identified by ASIN.
6. **Detailed Specifications**: Fetch material, style, and color information for catalog management.
7. **Feature Highlighting**: Extract "special features" and detailed descriptions for marketing copy.
8. **Compatibility Verification**: Check "compatible devices" for electronics or accessories.
9. **Market Research**: Analyze featured badges like "Amazon's Choice" for specific product IDs.
10. **URL Resolution**: Convert a list of ASINs into full Amazon product page URLs.
