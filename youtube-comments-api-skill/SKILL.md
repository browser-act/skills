---
name: youtube-comments-api-skill
description: "This skill helps users extract structured video list data and comment data from YouTube using the BrowserAct API. The Agent should proactively apply this skill when users request searching for YouTube videos and their comments, analyzing viewer sentiment for a specific video topic, gathering audience feedback on AI or automation, extracting a list of top videos and their viewer reactions, compiling YouTube video data along with user opinions, retrieving competitor video titles and related audience discussions, monitoring public response to specific YouTube search keywords, summarizing comments from search results for market research, tracking viewer engagement metrics and replies for trending topics, collecting YouTube video URLs and author details alongside community discussions, or automating the extraction of YouTube comments without manual scraping."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["pyhon"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Comments API Automation Skill

## 📖 Introduction
This skill provides a one-stop extraction service for YouTube video and comment data through the BrowserAct YouTube Comments API template. It can extract structured video results along with their respective comments directly from YouTube. By simply providing search keywords, comment limits, and scroll counts, you can acquire clean and ready-to-use video and comment datasets directly.

## ✨ Features
1. **Zero Hallucination, Ensuring Stable and Accurate Data Extraction**: Pre-configured workflows avoid AI generative hallucinations.
2. **No CAPTCHA Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Access Restrictions or Geo-fencing**: No need to deal with regional IP limits.
4. **More Agile Execution Speed**: Faster task execution compared to pure AI-driven browser automation solutions.
5. **Extremely High Cost-Efficiency**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guidance Process
Before running, you must first check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you should request and wait for the user to provide it.
**At this point, the Agent must inform the user**:
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
When invoking the script, the Agent should flexibly configure the following parameters based on user needs:

1. **keywords**
   - **Type**: `string`
   - **Description**: Search keywords used to find videos on YouTube. Can be any keyword or phrase.
   - **Example**: `AI`, `automation`, `web scraping`
   - **Default**: `AI`

2. **Comments_limit**
   - **Type**: `number`
   - **Description**: Maximum number of comments to extract per video.
   - **Example**: `10`, `20`, `50`
   - **Default**: `10`

3. **Scroll_count**
   - **Type**: `number`
   - **Description**: Number of times to scroll in the comments section to load more comments before extraction.
   - **Example**: `1`, `2`, `5`, `10`
   - **Default**: `2`

## 🚀 Invocation Method (Recommended)
The Agent should execute the following standalone script to achieve "one command, get results":

```bash
# Example invocation
python -u ./scripts/youtube_comments_api.py "keywords" "Comments_limit" "Scroll_count"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). While running, the script will **continuously output timestamped status logs** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script to return a result, please keep monitoring the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result, should you consider triggering the retry mechanism.

## 📊 Data Output Description
Upon successful execution, the script will directly parse and print the results from the API response. The results include two linked datasets:

**Video fields:**
- `video_name`: Video title shown in the list
- `video_url`: Video URL
- `video_publication_time`: Published time
- `video_view_count`: View count

**Comment fields:**
- `commenter_name`: Comment author display name
- `commenter_url`: Comment author channel URL
- `comment_text`: Comment content
- `comment_publish_date`: Comment publish time
- `comment_likes`: Like count for the comment
- `reply_count`: Number of replies

## ⚠️ Error Handling & Retry
During the execution of the script, if an error occurs (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**; you should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (e.g., the output starts with `Error:` or returns an empty result), the Agent should **automatically try to execute the script one more time**.

2. **Retry Limit**:
   - Automatic retries are limited to **one time** only. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Audience Insight**: Turning comments into product feedback and sentiment signals based on specific keywords.
2. **Content Research**: Understanding what viewers are discussing under popular video topics.
3. **Competitive Monitoring**: Tracking comments and feedback on competitors' YouTube channels.
4. **Community Insight**: Analyzing what users care about in a specific niche like automation or AI.
5. **Topic Tracking**: Monitoring the public response and interaction for trending search terms.
6. **Sentiment Analysis**: Gathering raw text data from comments to evaluate viewer opinions.
7. **Objections and Feature Requests**: Identifying user pain points from product-related video comments.
8. **Automated Data Integration**: Sending video and comment data directly into CRM or BI tools via API.
9. **Engagement Metrics Collection**: Tracking likes and reply counts for top comments.
10. **Market Research**: Extracting a large set of video metadata combined with user discussions for market studies.