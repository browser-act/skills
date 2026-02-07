---
name: google-news-api-skill
description: This skill automates the extraction of structured news data from Google News via BrowserAct API. Use this skill when the user asks for tasks such as: 1. Searching for news about a specific topic; 2. Tracking industry trends; 3. Monitoring public relations or sentiment; 4. Collecting competitor updates; 5. Getting the latest reports on specific keywords; 6. Monitoring brand exposure in media; 7. Researching market hot topics; 8. Summarizing daily industry news; 9. Tracking media activities of specific individuals; 10. Retrieving hot events from the past 24 hours; 11. Extracting structured data for market research; 12. Monitoring global breaking news.
---

# Google News Automation Skill

## 📖 Introduction
This skill provides a one-stop news collection service using BrowserAct's Google News API template. It extracts structured news results directly from Google News, including headlines, sources, publication times, and article links, providing clean and ready-to-use data without manual scraping.

## ✨ Features
1. **No Hallucinations**: Uses predefined workflows to ensure stable and accurate data extraction, avoiding AI-generated hallucinations.
2. **No CAPTCHA Issues**: Built-in mechanisms to bypass reCAPTCHA or other verification challenges automatically.
3. **No IP Restrictions**: Overcomes regional IP limitations and geofencing for stable global access.
4. **Fast Execution**: Executes tasks significantly faster than pure AI-driven browser automation.
5. **Cost-Effective**: Reduces data acquisition costs compared to token-heavy AI solutions.

## 🔑 API Key Guidance
Before running, check for the `BROWSERACT_API_KEY` environment variable. If it is not set, do not proceed with other actions. Instead, request and wait for the user to provide the key.
**Agent must inform the user**:
> "Since the BrowserAct API Key is not configured, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me here."

## 🛠️ Input Parameters Details
The Agent should configure the following parameters based on user needs when calling the script:

1. **Search_Keywords**
   - **Type**: `string`
   - **Description**: The keywords to search on Google News (e.g., company name, industry terms, competitor names).
   - **Example**: `Generative AI`, `Tesla`, `SpaceX`

2. **Publish_date**
   - **Type**: `string`
   - **Description**: Filters news based on publication time.
   - **Options**: 
     - `any time`: No time restriction.
     - `past hours`: Within the last few hours (best for breaking news).
     - `past 24 hours`: Within the last 24 hours (recommended for daily monitoring).
     - `past week`: Within the last week (short-term trend analysis).
     - `past year`: Within the last year (long-term research).
   - **Default**: `past week`

3. **Datelimit**
   - **Type**: `number`
   - **Description**: Maximum number of news items to extract in a single task.
   - **Default**: `30`
   - **Recommendation**: Use 10-30 for real-time monitoring; use larger values for deep research.

## 🚀 How to Call (Recommended)
The Agent should execute the following command to get results:

```bash
# Example call
python -u ./.cursor/skills/google-news-api-skill/scripts/google_news_api.py "search keywords" "time range" limit
```

### ⏳ Progress Monitoring
Since this task involves automated browser operations, it may take several minutes. The script will continuously output timestamped status logs (e.g., `[14:30:05] Task Status: running`).
**Agent Note**:
- Stay focused on the terminal output while waiting for the script.
- As long as new status logs are being printed, the task is running normally. Do not assume it is hung or unresponsive.
- Only consider retrying if the status remains unchanged for a long time or the script stops without returning results.

## 📊 Output Data Specification
Upon success, the script prints results parsed from the API response. Fields include:
- `headline`: Title of the news article.
- `source`: Publisher or news outlet.
- `news_link`: Resolved destination URL of the article.
- `published_time`: Timestamp displayed on Google News.
- `author`: Name of the author (if available).

## ⚠️ Error Handling & Retry Mechanism
If an error occurs (e.g., network issues or task failure), follow this logic:

1. **Check Output**:
   - If output contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**. Guide the user to provide a correct API Key.
   - If output does not contain `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or result is empty), the Agent should **automatically retry once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one** attempt. If it fails again, stop and report the error message to the user.

## 🌟 Typical Use Cases
1. **Industry Trend Tracking**: Find the latest developments in fields like "Low-altitude economy" or "Generative AI".
2. **PR Monitoring**: Monitor media exposure of a specific brand or company over the past 24 hours.
3. **Competitor Intelligence**: Collect information on new products or marketing activities from competitors over the past week.
4. **Market Research**: Get popular reports on specific keywords across different time dimensions.
5. **Individual Tracking**: Retrieve the latest news reports on industry leaders or public figures.
6. **Daily News Summary**: Automatically extract and summarize daily news in specific domains.
7. **Global Breaking News**: Get real-time updates on major global events.
8. **Structured Data Extraction**: Extract structured information like headlines, sources, and links for analysis.
9. **Media Exposure Analysis**: Evaluate the propagation heat of a project or event in mainstream news media.
10. **Long-term Research**: Retrieve all in-depth reports on a specific technical topic from the past year.
