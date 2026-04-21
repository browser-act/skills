---
name: web-search-scraper-api-skill
description: "This skill helps users automatically extract complete Markdown content from any website via the BrowserAct Web Search Scraper API. The Agent should proactively apply this skill when users express needs like extract complete markdown from a specific website, scrape the content of an article link, get the text from a target url, convert a webpage to markdown format, fetch the main content of a blog post, extract data from a given web page, parse the html of a website into markdown, download the readable text from a news article, obtain the content of a tutorial page, extract all the markdown text from any http or https url, scrape documentation from a web link, or grab the text of a single webpage."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Web Search Scraper API Skill

## 📖 Introduction
This skill provides users with a one-stop web page extraction service through the BrowserAct Web Search Scraper API template. It can directly extract structured markdown content from any given URL. By simply inputting the target URL, you can get clean and usable markdown data.

## ✨ Features
1. **No hallucinations, ensuring stable and precise data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No human-machine verification issues**: No need to deal with reCAPTCHA or other verification challenges.
3. **No IP access restrictions or geofencing**: No need to handle regional IP limitations.
4. **More agile execution speed**: Compared to purely AI-driven browser automation solutions, task execution is faster.
5. **Extremely high cost-effectiveness**: Compared to AI solutions that consume a lot of Tokens, it can significantly reduce the cost of data acquisition.

## 🔑 API Key Guidance Process
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions first; you should ask and wait for the user to provide it cooperatively.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters Details
Agent should flexibly configure the following parameters based on user needs when calling the script:

1. **target_url**
   - **Type**: `string`
   - **Description**: The website URL to extract content from. Supports any HTTP/HTTPS URL.
   - **Example**: `https://www.browseract.com`

## 🚀 Invocation Method (Recommended)
Agent should execute the following independent script to achieve "one command gets the result":

```bash
# Example invocation
python -u ./scripts/web_search_scraper_api.py "target_url"
```

### ⏳ Execution Status Monitoring
Since the task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Notice for Agent**:
- While waiting for the script to return results, please keep paying attention to the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting and no result is returned, the retry mechanism can be triggered.

## 📊 Data Output Description
Upon successful execution, the script will directly parse and print the result from the API response. The result contains:
- `content`: The complete markdown content of the webpage.

## ⚠️ Error Handling & Retry Mechanism
During the execution of the script, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, and you should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the returned result is empty), the Agent should **automatically try to re-execute the script once**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Article Extraction**: Scrape the main content of a news article link into markdown.
2. **Blog Post Parsing**: Download the readable text from a target blog post URL.
3. **Webpage to Markdown**: Convert any given website URL into clean markdown format.
4. **Documentation Scraping**: Fetch the contents of a tutorial or documentation page for offline reading.
5. **Content Monitoring**: Automatically extract the text from a specific webpage for updates.
6. **Data Processing**: Parse the HTML of an arbitrary HTTP/HTTPS URL to structure its content.
