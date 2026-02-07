---
name: amazon-asin-lookup-api-skill
description: This skill helps users extract structured product details from Amazon using a specific ASIN (Amazon Standard Identification Number). Use this skill when the user asks to: 1. Get Amazon product details by ASIN; 2. Lookup Amazon product title and price using ASIN; 3. Extract Amazon product ratings and reviews count for a specific ASIN; 4. Check Amazon product availability and current price; 5. Get Amazon product description and features via ASIN; 6. Enrich product catalog with Amazon data using ASIN; 7. Monitor Amazon product price changes for specific ASINs; 8. Retrieve Amazon product brand and material information; 9. Fetch Amazon product images and specifications by ASIN; 10. Validate Amazon ASIN and get product metadata.
---

# Amazon ASIN Lookup Skill

## 📖 Introduction
This skill utilizes BrowserAct's Amazon ASIN Lookup API template to provide a seamless way to retrieve comprehensive product information from Amazon. By simply providing an ASIN, you can extract structured data including title, price, ratings, brand, and detailed descriptions directly into your application without manual scraping.

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

1. **ASIN (Amazon Standard Identification Number)**
   - **Type**: `string`
   - **Description**: The unique identifier for the Amazon product.
   - **Required**: Yes
   - **Example**: `B07TS6R1SF`

## 🚀 Usage (Recommended)
The agent should execute the following script to get results in one command:

```bash
# Example Usage
python -u ./.cursor/skills/amazon-asin-lookup-api-skill/scripts/amazon_asin_lookup_api.py "ASIN_VALUE"
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

## ⚠️ Error Handling & Retry Mechanism
If an error occurs during execution, the agent should follow this logic:

1. **Check Output**:
   - If the output contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**; ask the user to provide a valid key.
   - If the output does not contain `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the agent should **automatically retry once**.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If it fails again, stop and report the error to the user.
