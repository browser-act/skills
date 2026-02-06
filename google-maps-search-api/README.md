---
name: google-maps-search-api
description: This skill is designed to help users automatically extract business data from Google Maps search results. When a user asks to "find coffee shops in New York," "search for dental clinics," or "extract business leads from Google Maps," the agent should proactively apply this skill.
---

# Google Maps Search Automation Skill

## 📖 Introduction
This skill provides a one-stop business data collection service through the BrowserAct Google Maps Search API template. Obtain structured business data with just one command.

## 🔑 API Key Guidance
Before running, check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take further action; instead, request and wait for the user to provide it.
**The Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat."

## 🛠️ Input Parameters Details
The Agent should flexibly configure the following parameters when calling the script based on user needs:

1. **KeyWords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The keywords the user wants to search for on Google Maps.
   - **Example**: `coffee`, `bakery`, `coworking space`

2. **language (UI Language)**
   - **Type**: `string`
   - **Description**: Sets the UI language and the language of the returned text.
   - **Optional Values**: `en`, `de`, `fr`, `it`, `es`, `ja`, `zh-CN`, `zh-TW`
   - **Default**: `en`

3. **country (Country/Region Bias)**
   - **Type**: `string`
   - **Description**: Sets the country or region bias for search results.
   - **Example**: `us`, `gb`, `ca`, `au`, `de`, `fr`, `es`, `it`, `jp`
   - **Default**: `us`

4. **max_dates (Maximum extraction limit)**
   - **Type**: `number`
   - **Description**: The maximum number of places to extract from search results.
   - **Default**: `100`

## 🚀 Execution Method (Recommended)
The Agent should implement "one command for results" by executing the following independent script:

```bash
# Call example
python ./scripts/google_maps_search_api.py "KeyWords" "language" "country" max_dates
```

## 📊 Data Output Description
After successful execution, the script will directly parse and print the results from the API response. Results include:
- `name`: Business name
- `full address`: Business address
- `rating`: Average star rating
- `review count`: Number of reviews
- `price range`: Price level
- `cuisine type`: Business category
- `amenity tags`: Features like Wi-Fi, outdoor seating
- `review snippet`: Highlighted short review
- `service options`: Such as "Order online", "Dine-in"

## ⚠️ Error Handling & Retry
During script execution, if an error occurs (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check output content**:
   - If the output **contains** `"Invalid authorization"`, the API Key is invalid or expired. **Do not retry**; instead, guide the user to check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (e.g., output starts with `Error:` or returns an empty result), the Agent should **automatically attempt to re-execute** the script once.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.
