---
name: wechat-article-search-api-skill
description: "This skill helps users extract full article contents from WeChat using the BrowserAct API. The Agent should proactively apply this skill when users express needs like finding full WeChat articles for specific keywords, tracking WeChat public accounts for industry trends, extracting WeChat article contents for media research, monitoring public relations on WeChat platforms, collecting competitor updates from WeChat, getting full article body from WeChat links, monitoring brand exposure on WeChat articles, retrieving structured WeChat data for sentiment analysis, summarizing daily news from WeChat, getting author and publication date for WeChat articles, or automating WeChat content extraction without scraping."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# WeChat Article Search API

## 📖 Introduction
This skill provides users with automated WeChat article extraction through the BrowserAct WeChat Article Search API template. It allows for the direct extraction of full-content, structured WeChat articles based on keyword searches. Simply provide search keywords and optional date filters, and you can obtain comprehensive article data including the full body text.

## ✨ Features
1. **No hallucinations, ensuring stable and precise data extraction**: Pre-configured workflows avoid AI-generated hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to handle regional IP limitations.
4. **Faster execution**: Task execution is faster compared to pure AI-driven browser automation solutions.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guidance Flow
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other actions; request and wait for the user to provide it.
**The Agent must inform the user**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
When invoking the script, the Agent should flexibly configure the following parameters based on user needs:

1. **keywords (Search Keywords)**
   - **Type**: `string`
   - **Description**: Search keywords used to find WeChat articles. Can be an industry term, topic, or specific phrase.
   - **Example**: `openclaw`, `AI agent`, `browser automation`

2. **Date_limit (Extraction Limit)**
   - **Type**: `number`
   - **Description**: Maximum number of articles to extract. For the first run, a smaller default value is recommended.
   - **Default Value**: `10`
   - **Suggestions**: Use `5` to `10` for quick testing, larger numbers for batch research.

3. **publication_date (Publication Date Filter)**
   - **Type**: `string`
   - **Description**: Filter articles by their publication date.
   - **Example**: `3月11日`, `March 10`, `2026-03-11`

## 🚀 Invocation Method
The Agent should execute the following independent script to achieve "one command, direct results":

```bash
# Example invocation
python -u ./scripts/wechat_article_search_api.py "keywords" limit "publication_date"
```

### ⏳ Run Status Monitoring
Because this task involves automated browser operations, it may take a long time (several minutes). While running, the script will **continuously output timestamped status logs** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- Keep monitoring the terminal output while waiting for the script to return results.
- As long as the terminal continues to output new status logs, it means the task is running normally; do not misjudge it as deadlocked or unresponsive.
- Only consider triggering the retry mechanism if the status remains unchanged for a long time, or the script stops outputting without returning results.

## 📊 Output Data Explanation
Upon successful execution, the script will parse and print the results directly from the API response. The results include:
- `url_link`: Original article URL
- `publication_date`: Article publication date
- `author`: Article author or publishing account name
- `image_url`: Main image URL or article cover image URL
- `body_content`: Full body content of the article
- `title`: Full article title

## ⚠️ Error Handling & Retry
During script execution, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. In this case, **do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns an empty result), the Agent should **automatically try to execute the script one more time**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Content Monitoring**: Track mentions of specific brands or topics across WeChat articles.
2. **Media Research**: Analyze full text of articles published by top WeChat accounts.
3. **Trend Tracking**: Collect articles about rising industry trends (e.g., AI agents) for comprehensive reading.
4. **Knowledge Base Building**: Extract deep-dive articles into an internal repository.
5. **Competitor Analysis**: Review full-length posts released by competitor accounts.