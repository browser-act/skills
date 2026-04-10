---
name: zhihu-search-api-skill
description: "This skill helps users automatically extract structured article details and full content from Zhihu via the BrowserAct API. Agent should proactively apply this skill when users express needs like: searching for Zhihu articles on a specific topic, tracking industry trends on Zhihu, monitoring public relations or sentiment on Zhihu, collecting competitor updates, getting the latest reports on specific keywords, monitoring brand exposure in Zhihu media, researching market hot topics, summarizing daily Zhihu industry news, retrieving hot events from the past week, extracting structured data for market research, finding full Zhihu articles for AI agents, extracting full article body from Zhihu links."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Zhihu Search API Automated Extraction Skill

## 📖 Brief
This skill uses BrowserAct's Zhihu Search API template to provide a one-stop article extraction service. It extracts structured article details and full content from Zhihu article search results based on keywords and publication date filters.

## ✨ Features
1. **No hallucinations, ensuring stable and precise data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions and geo-fencing**: No need to deal with regional IP limits.
4. **Faster execution speed**: Compared to pure AI-driven browser automation solutions, task execution is much faster.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guide
Before running, you need to check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions; wait for the user to provide it.
**The Agent must inform the user at this time:**
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
The Agent should flexibly configure the following parameters according to user needs when calling the script:

1. **keyword (Search Keywords)**
   - **Type**: `string`
   - **Description**: Search keywords used to find Zhihu articles. Can be company name, industry term, etc.
   - **Example**: `AI agent`, `openclaw`

2. **Publish_date (Publication Date Range)**
   - **Type**: `string`
   - **Description**: Filter articles by publication date.
   - **Options**:
     - `7d`: Past 7 days
     - `30d`: Past 30 days
     - `90d`: Past 90 days
     - `1y`: Past year
     - `all`: Any time
   - **Default**: `7d`

3. **Date_limit (Extraction Limit)**
   - **Type**: `number`
   - **Description**: Maximum number of articles to extract.
   - **Default**: `10`

## 🚀 Recommended Usage
The Agent should execute the following independent script to achieve "one command gets results":

```bash
# Example call
python -u ./scripts/zhihu_search_api.py "keyword" "Publish_date" limit
```

### ⏳ Execution Status Monitoring
Because this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Agent Must Know:**
- While waiting for the script to return a result, keep monitoring the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally, do not mistake it for a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, then consider triggering the retry mechanism.

## 📊 Data Output
Upon successful execution, the script will directly parse and print the result from the API response. The result includes:
- `title`: Full article title
- `body_content`: Full body content of the article
- `image_url`: Main image URL or article cover image URL
- `author`: Article author or publishing account name
- `publication_date`: Article publication date
- `url_link`: Original article URL

## ⚠️ Error Handling & Retry
During the execution of the script, if an error is encountered (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. Do **not retry** at this time, and guide the user to check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the return result is empty), the Agent should **automatically try to execute the script once more**.

2. **Retry limits**:
   - Automatic retry is limited to **one time**. If the second attempt still fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Industry Trend Tracking**: Find the latest industry dynamics on specific topics like "low-altitude economy" or "generative AI" on Zhihu.
2. **Public Relations Monitoring**: Monitor the media exposure of a specific brand or company on Zhihu over the past 30 days.
3. **Competitor Intelligence Gathering**: Collect recent product information or market activities published by competitors on Zhihu.
4. **Market Hotspot Research**: Get popular Zhihu reports on specific keywords across different time dimensions.
5. **Character Dynamics Tracking**: Retrieve the latest Zhihu articles and interviews of industry leaders or public figures.
6. **Daily Briefing Summary**: Automatically extract and summarize daily industry news briefings from Zhihu.
7. **Global Event Monitoring**: Real-time access to major breaking news and discussions on Zhihu.
8. **Structured Data Extraction**: Extract structured information such as article titles, authors, and links from Zhihu for market research analysis.
9. **Media Exposure Analysis**: Evaluate the spread and popularity of a specific project or event on Zhihu.
10. **Long-term Thematic Research**: Retrieve in-depth reports and discussions on a specific technical topic from the past year.