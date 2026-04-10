---
name: amazon-buy-box-monitor-api-skill
description: "This skill helps users extract basic product details other sellers prices and seller ratings from Amazon via ASIN automatically using the BrowserAct API. Agent should proactively apply this skill when users express needs like query Amazon buy box information, monitor Amazon product prices, extract Amazon product details by ASIN, check other sellers prices on Amazon, get Amazon seller ratings and feedback count, monitor buy box ownership for a specific ASIN, track Amazon fulfillment methods for competitors, compare Amazon product prices across different sellers, retrieve Amazon buy box availability status, analyze Amazon seller profile details."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Buy Box Monitor API Skill

## 📖 Introduction
This skill provides users with an automated Amazon Buy Box monitoring service using the BrowserAct API template. It can directly extract structured data including basic product details, other sellers' prices, and seller ratings from Amazon via a specific ASIN. No coding or proxies are required, and users only need to provide the ASIN and an optional marketplace URL to retrieve clean and usable data.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions or geo-fencing**: No need to handle regional IP restrictions.
4. **More agile execution speed**: Faster task execution compared to purely AI-driven browser automation solutions.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume massive amounts of tokens.

## 🔑 API Key Guidance
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you must prompt and wait for the user to provide it.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on the user's needs:

1. **ASIN**
   - **Type**: `string`
   - **Description**: The Amazon Standard Identification Number. This is the unique identifier for the product on Amazon.
   - **Example**: `B005O2ZU68`
   - **Required**: Yes

2. **Marketplace_url**
   - **Type**: `string`
   - **Description**: The Amazon marketplace URL indicating the region.
   - **Default value**: `https://amazon.com/`
   - **Example**: `https://amazon.co.uk/`
   - **Required**: Yes

## 🚀 Invocation Method (Recommended)
The Agent should execute the following standalone script to achieve "one command to get results":

```bash
# Example invocation
python -u ./scripts/amazon_buy_box_monitor_api.py "ASIN" "Marketplace_url"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script to return results, please keep paying attention to the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Do not misjudge it as deadlocked or unresponsive.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, then consider triggering the retry mechanism.

## 📊 Data Output Description
After successful execution, the script will parse and print the result directly from the API response. The result includes:
- `asin`: The Amazon Standard Identification Number
- `product_title`: The title of the product
- `buy_box_owner`: The owner of the buy box
- `buy_box_price`: The current buy box price
- `currency`: The currency of the price
- `fulfillment_method`: The fulfillment method (e.g., FBA, FBM)
- `availability_status`: Stock availability status
- `other_sellers`: An array of other sellers including their name, price, shipping fee, and seller rating
- `seller_info`: Detailed information about the main seller including rating and feedback count

## ⚠️ Error Handling & Retry
If an error is encountered during the execution of the script (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. In this case, **do not retry**, but guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically attempt to execute the script once more**.

2. **Retry limits**:
   - Automatic retry is limited to **only once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Query Amazon buy box information**: Find out who currently owns the buy box for a specific ASIN.
2. **Monitor Amazon product prices**: Track the current price and buy box price changes.
3. **Extract Amazon product details by ASIN**: Get basic product information like title and brand.
4. **Check other sellers prices on Amazon**: Analyze pricing strategies of competitors for the same product.
5. **Get Amazon seller ratings and feedback count**: Evaluate the reputation of sellers on the listing.
6. **Monitor buy box ownership for a specific ASIN**: Check if a particular seller maintains the buy box.
7. **Track Amazon fulfillment methods for competitors**: Determine whether competitors are using FBA or FBM.
8. **Compare Amazon product prices across different sellers**: View shipping fees and total prices from multiple sellers.
9. **Retrieve Amazon buy box availability status**: Check if the product is in stock or backordered.
10. **Analyze Amazon seller profile details**: Extract detailed seller info and recent feedback summaries.