---
name: google-maps-search-api-skill
description: This skill is designed to help users automatically extract business data from Google Maps search results. The Agent should proactively apply this skill when the user makes the following requests: 1. Search for coffee shops in a specific city; 2. Find dentists or medical clinics nearby; 3. Track competitors' locations in a certain area; 4. Extract business leads from Google Maps lists; 5. Gather restaurant data for market research; 6. Find hotels or accommodation options in a region; 7. Locate specific services like coworking spaces or gyms; 8. Monitor new business openings in a neighborhood; 9. Collect contact information and addresses for sales prospecting; 10. Analyze price ranges and cuisines of local eateries; 11. Get ratings and review counts for a list of businesses; 12. Export local business data into a CRM or database.
---

# Google Maps Search Automation Skill

## 📖 Introduction
This skill utilizes the BrowserAct Google Maps Search API template to provide a one-stop business data collection service. It extracts structured business results directly from Google Maps search lists. Simply provide search keywords, language, and country filters to get clean, usable business data.

## ✨ Features
1. **No Hallucinations, Ensuring Stable and Accurate Data Extraction**: Preset workflows avoid AI generative hallucinations.
2. **No Human-Machine Verification Issues**: Built-in bypass mechanisms eliminate the need to handle reCAPTCHA or other verification challenges.
3. **No IP Access Restrictions or Geofencing**: Breaks through regional IP limits to ensure stable global access.
4. **Agile Execution Speed**: Task execution is faster compared to pure AI-driven browser automation solutions.
5. **High Cost-Effectiveness**: Significantly reduces data acquisition costs compared to token-intensive AI solutions.

## 🔑 API Key Guidance Process
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take further action; instead, ask and wait for user cooperation to provide it.
**The Agent must inform the user**:
> "Since you haven't configured your BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat."

## 🛠️ Input Parameters Detail
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

## 🚀 Invocation Method (Recommended)
The Agent should execute the following independent script to achieve "one line command for results":

```bash
# Example call
python -u ./.cursor/skills/google-maps-search-api-skill/scripts/google_maps_search_api.py "search keywords" "language" "country" count
```

### ⏳ Execution Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script outputs timestamped status logs during execution (e.g., `[14:30:05] Task Status: running`).
**Agent Notes**:
- Keep an eye on the terminal output while waiting for results.
- As long as the terminal is printing new status logs, the task is running normally; do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning results, consider triggering a retry mechanism.

## 📊 Output Data Description
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

## ⚠️ Error Handling & Retry Mechanism
If an error occurs during execution, the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, the API Key is invalid or expired. **Do not retry**; guide the user to check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically attempt to re-execute once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one** time. If the second attempt still fails, stop retrying and report the specific error message to the user.

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
