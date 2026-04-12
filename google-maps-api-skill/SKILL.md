---
name: google-maps-api-skill
description: "This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API. Agent should proactively trigger this skill for needs like finding restaurants in a specific city, extracting contact info of dental clinics, researching local competitors, collecting addresses of coffee shops, generating lead lists for specific industries, monitoring business ratings and reviews, getting opening hours of local services, finding specialized stores (e.g., Turkish-style restaurants), analyzing business categories in a region, extracting website links from local businesses, gathering phone numbers for sales outreach, mapping out service providers in a specific country."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Google Maps Automation Scraper Skill

## 📖 Introduction
This skill leverages BrowserAct's Google Maps API template to provide a one-stop business data collection service. It extracts structured details directly from Google Maps, including business names, categories, contact info, ratings, and more. Simply provide the search keywords and location bias to get clean, actionable data.

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
Configure the following parameters based on user requirements:

1. **keywords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The query you would search for on Google Maps.
   - **Example**: `coffee shop`, `dental clinic`, `Turkish-style restaurant`

2. **language (UI Language)**
   - **Type**: `string`
   - **Description**: Defines the UI language and returned text language (e.g., en, zh-CN).
   - **Default**: `en`

3. **country (Country Bias)**
   - **Type**: `string`
   - **Description**: Specifies the country or region bias (e.g., us, gb, ca).
   - **Default**: `us`

## 🚀 Usage
Execute the following script to get results in one command:

```bash
# Example call
python -u ./scripts/google_maps_api.py "keywords" "language" "country"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
Upon success, the script parses and prints the following fields from the API:
- `Title Name`: Official business name
- `Category_primary`: Main business category
- `Address`: Full street address
- `Phone number`: Contact phone number
- `Website link`: Official URL
- `Rating`: Average star rating
- `reviews_count`: Total number of reviews
- `business_status`: Operational status (e.g., operational)

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Lead Generation**: Find "SaaS companies" in "us" for sales outreach.
2. **Competitor Research**: Extract data on "coffee shops" in a specific neighborhood.
3. **Market Analysis**: Identify the density of "dental clinics" in a region.
4. **Contact Info Retrieval**: Get phone numbers and websites for "real estate agencies".
5. **Local Service Discovery**: Find "Turkish-style restaurants" with high ratings.
6. **Business Status Monitoring**: Check if specific stores are "operational".
7. **Directory Building**: Gather addresses and categories for a local business directory.
8. **Rating Benchmarking**: Compare ratings of various "luxury hotels".
9. **Global Scouting**: Research "tech startups" in different countries like "gb" or "au".
10. **Automated Data Sync**: Periodically pull local business data into a CRM.
