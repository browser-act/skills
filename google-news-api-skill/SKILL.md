---
name: google-news-api-skill
description: "This skill helps users automatically extract structured news data from Google News via BrowserAct API. Agent should proactively apply this skill when users express needs like searching for news about a specific topic, tracking industry trends, monitoring public relations or sentiment, collecting competitor updates, getting latest reports on specific keywords, monitoring brand exposure in media, researching market hot topics, summarizing daily industry news, tracking media activities of specific individuals, retrieving hot events from the past 24 hours, extracting structured data for market research, monitoring global breaking news."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Google News Automation Skill

## 📖 Introduction
This skill provides a one-stop news collection service using BrowserAct's Google News API template. It directly extracts structured news results from Google News, including headlines, sources, publication times, and article links. Simply input search keywords and time filters to get clean, usable news data.

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
Agent should flexibly configure the following parameters based on user needs:

1. **Search_Keywords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The content to search on Google News. Can be company names, industry terms, competitor names, etc.
   - **Example**: `AI Startup`, `Tesla`, `SpaceX`

2. **Publish_date (Time Range)**
   - **Type**: `string`
   - **Description**: Filter news by publication time.
   - **Options**: 
     - `any time`: No restriction
     - `past hours`: Past few hours (breaking news)
     - `past 24 hours`: Past 24 hours (daily monitoring)
     - `past week`: Past week (short-term trends)
     - `past year`: Past year (long-term research)
   - **Default**: `past week`

3. **Datelimit (Max Items)**
   - **Type**: `number`
   - **Description**: Maximum number of news items to extract per task.
   - **Default**: `30`
   - **Suggestion**: Use 10-30 for real-time monitoring; use larger values for deep research.

## 🚀 Usage
Agent should use the following independent script to achieve "one-line command result":

```bash
# Example
python -u ./scripts/google_news_api.py "Search Keywords" "Publish Date" Quantity
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script parses and prints results directly from the API response. Results include:
- `headline`: News title
- `source`: Publisher/Source
- `news_link`: Article URL
- `published_time`: Publication time
- `author`: Author (if available)

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Industry Trend Tracking**: Find the latest developments in fields like "Low-altitude economy" or "Generative AI".
2. **PR Monitoring**: Monitor media exposure of a specific brand or company over the past 24 hours.
3. **Competitor Intelligence**: Collect information on new products or marketing activities from competitors over the past week.
4. **Market Research**: Get popular reports on specific keywords across different time dimensions.
5. **Figure Tracking**: Retrieve the latest news reports on industry leaders or public figures.
6. **Daily News Summary**: Automatically extract and summarize daily news in specific domains.
7. **Global Breaking News**: Get real-time updates on major global events.
8. **Structured Data Extraction**: Extract structured information like headlines, sources, and links for analysis.
9. **Media Exposure Analysis**: Evaluate the propagation heat of a project or event in mainstream news media.
10. **Long-term Research**: Retrieve all in-depth reports on a specific technical topic from the past year.
