---
name: google-maps-api-skill
description: This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API. Agent should proactively trigger this skill for needs like: 1. Find restaurants in a specific city; 2. Extract contact info of dental clinics; 3. Research local competitors; 4. Collect addresses of coffee shops; 5. Generate lead lists for specific industries; 6. Monitor business ratings and reviews; 7. Get opening hours of local services; 8. Find specialized stores (e.g., Turkish-style restaurants); 9. Analyze business categories in a region; 10. Extract website links from local businesses; 11. Gather phone numbers for sales outreach; 12. Map out service providers in a specific country.
---

# Google Maps Automation Scraper Skill

## 📖 Introduction
This skill leverages BrowserAct's Google Maps API template to provide a one-stop business data collection service. It extracts structured details directly from Google Maps, including business names, categories, contact info, ratings, and more. Simply provide the search keywords and location bias to get clean, actionable data.

## ✨ Features
1. **No Hallucinations, Stable & Precise Data Extraction**: Preset workflows avoid AI-generated hallucinations.
2. **No CAPTCHA Issues**: Built-in mechanisms bypass reCAPTCHA and other verification challenges.
3. **No IP Access Restrictions or Geo-fencing**: Overcomes regional IP limits for global access.
4. **Faster Execution**: Tasks run more quickly than pure AI-driven browser automation.
5. **High Cost-Effectiveness**: Significantly reduces data acquisition costs compared to high-token AI solutions.

## 🔑 API Key Setup
Before running, ensure the `BROWSERACT_API_KEY` environment variable is set. If missing, do not proceed; request the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it in this chat."

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

## 🚀 How to Call
Execute the following script to get results in one command:

```bash
# Example call
python -u ./scripts/google_maps_api.py "keywords" "language" "country"
```

### ⏳ Execution Monitoring
As this involves automated browser operations, it may take several minutes. The script will output timestamped status logs (e.g., `[14:30:05] Task Status: running`).
**Agent Note**:
- Monitor the terminal output while waiting.
- New status logs mean the task is running; do not assume it is hung.
- Retry only if the status stops updating or the script exits without results.

## 📊 Output Data
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
If an error occurs (network issues or task failure), follow this logic:

1. **Check Output**:
   - If it contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**; ask the user for a correct Key.
   - Otherwise, if it starts with `Error:` or returns no results, **automatically retry once**.

2. **Retry Limit**:
   - Only one automatic retry. If it fails again, report the specific error to the user.

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
