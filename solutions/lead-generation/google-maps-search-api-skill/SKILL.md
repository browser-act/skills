---
name: google-maps-search-api-skill
description: "This skill is designed to help users automatically extract business data from Google Maps search results. The Agent should proactively apply this skill when the user makes the following requests searching for coffee shops in a specific city, finding dentists or medical clinics nearby, tracking competitors' locations in a certain area, extracting business leads from Google Maps lists, gathering restaurant data for market research, finding hotels or accommodation options in a region, locating specific services like coworking spaces or gyms, monitoring new business openings in a neighborhood, collecting contact information and addresses for sales prospecting, analyzing price ranges and cuisines of local eateries, getting ratings and review counts for a list of businesses, exporting local business data into a CRM or database."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Google Maps Search Automation Skill

## 📖 Introduction
This skill utilizes the BrowserAct Google Maps Search API template to provide a one-stop business data collection service. It extracts structured business results directly from Google Maps search lists. Simply provide search keywords, language, and country filters to get clean, usable business data.

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
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: The content you want to search on Google Maps. Can be business names, categories, or specific keywords.
   - **Example**: `coffee shop`, `dental clinic`, `coworking space`

2. **language**
   - **Type**: `string`
   - **Description**: Sets the UI language and the language of returned text fields.
   - **Common Values**: `en`, `de`, `fr`, `it`, `es`, `ja`, `zh-CN`, `zh-TW`
   - **Default**: `en`

3. **country**
   - **Type**: `string`
   - **Description**: Sets the country or region bias for search results.
   - **Example**: `us`, `gb`, `ca`, `au`, `de`, `fr`, `jp`
   - **Default**: `us`

4. **max_dates**
   - **Type**: `number`
   - **Description**: The maximum number of places to extract from the search results list.
   - **Default**: `100`

## 🚀 Usage
The Agent should execute the following independent script to achieve "one-line command result":

```bash
# Example call
python -u ./scripts/google_maps_search_api.py "search keywords" "language" "country" count
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script parses and prints results directly from the API response. Fields include:
- `name`: Business name
- `full address`: Full address
- `rating`: Star rating
- `review count`: Number of reviews
- `price range`: Price level
- `cuisine type`: Business category
- `amenity tags`: Features like Wi-Fi
- `review snippet`: Short review text
- `service options`: Service indicators (e.g., "Order online")

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Local Business Discovery**: Find all "Italian restaurants" in Manhattan.
2. **Sales Lead Generation**: Extract a list of "real estate agencies" in London for prospecting.
3. **Competitor Mapping**: Locate all "Starbucks" branches in a specific city to map competition.
4. **Market Research**: Analyze "boutique hotels" in Paris, including their ratings and price ranges.
5. **Contact Collection**: Gather addresses and names of "dental clinics" in Sydney.
6. **Service Search**: Find "24-hour pharmacies" or "emergency plumbers" in a certain area.
7. **Neighborhood Monitoring**: Track new "gyms" or "yoga studios" opening in a community.
8. **Structured Data Export**: Export structured data of "car dealerships" for CRM integration.
9. **Sentiment Analysis Prep**: Get review snippets and ratings for "popular tourist attractions".
10. **Global Search Localization**: Use different language and country settings to research "tech hubs" globally.
