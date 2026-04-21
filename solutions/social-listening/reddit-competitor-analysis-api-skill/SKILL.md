---
name: reddit-competitor-analysis-api-skill
description: "This skill helps users extract structured data from Reddit posts and comments via BrowserAct API. Agent should proactively apply this skill when users express needs like analyzing competitor mentions on Reddit, tracking brand sentiment in Reddit comments, extracting Reddit discussions for market research, finding popular Reddit posts by keywords, monitoring community feedback on specific topics, gathering user reviews from Reddit threads, searching for Reddit posts within a specific date range, sorting Reddit discussions by relevance or hotness, compiling nested Reddit comments for deep analysis, building a structured dataset of Reddit conversations, discovering trending topics in specific subreddits, or monitoring social media activity for specific brands on Reddit."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Reddit Competitor Analysis API Skill

## 📖 Introduction
This skill uses the BrowserAct Reddit Competitor Analysis API template to provide users with a one-stop Reddit data collection service. It can extract full post details and comments from Reddit search results. Just input search keywords and filtering conditions to directly get clean and usable Reddit data.

## ✨ Features
1. **No hallucinations, ensuring stable and precise data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions or geofencing**: No need to handle regional IP limitations.
4. **Faster execution**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to highly token-consuming AI solutions.

## 🔑 API Key Guide
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you should request and wait for the user to provide it collaboratively.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key first."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **Keywords (Search keywords)**
   - **Type**: `string`
   - **Description**: Search keywords for Reddit posts.
   - **Example**: `openclaw`

2. **Publication_date (Publication date)**
   - **Type**: `string`
   - **Description**: Filter posts by publication date range.
   - **Options**: `All time`, `Past year`, `Past month`, `Past week`, `Today`, `Past hour`
   - **Default**: `Past week`

3. **Post_sort_by (Search sort)**
   - **Type**: `string`
   - **Description**: Sort Reddit post search results by selected criteria.
   - **Options**: `Relevance`, `Hot`, `Top`, `New`, `Comment count`
   - **Default**: `Relevance`

4. **Comment_sort_by (Comment sort)**
   - **Type**: `string`
   - **Description**: Sort extracted comments by.
   - **Options**: `Best`, `Top`, `New`, `Controversial`, `Q&A`
   - **Default**: `Best`

5. **Data_limit (Comments per post)**
   - **Type**: `number`
   - **Description**: Maximum number of comments to extract per post.
   - **Default**: `10`

## 🚀 Usage (Recommended)
The Agent should execute the following independent script to achieve "one-line command to get results". Note that the script path `./scripts/...` is relative to this skill's directory:

```bash
# Example invocation
python3 -u ./scripts/reddit_competitor_analysis_api.py "keywords" "publication_date" "post_sort_by" "comment_sort_by" data_limit
```

### ⏳ Task Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Agent Must Know**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Please do not mistakenly judge it as a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting and no result is returned, you can consider triggering the retry mechanism.

## 🔧 OpenClaw Adaptation Guide
Since BrowserAct tasks may take a long time to run (5-20 minutes), when the Agent executes in the OpenClaw environment, it needs to:

1. **Run in background mode (using JSON parameters for `exec` tool):**
   - `command`: `"python3 -u ./scripts/reddit_competitor_analysis_api.py ..."`
   - `background`: `true`
   - `timeout`: `1800`

2. **Or increase yieldMs:**
   - `command`: `"python3 -u ./scripts/reddit_competitor_analysis_api.py ..."`
   - `yieldMs`: `600000`
   - `timeout`: `1800`

3. **Use process poll to monitor:**
   - `action`: `"poll"`
   - `sessionId`: `"xxx"`
   - `timeout`: `300000`

## 📊 Data Output Description
After successful execution, the script will directly parse and print the results from the API response. The results include:
- `post_title`: Full post title
- `publish_time`: Post publication time
- `like_count`: Number of upvotes on the post
- `comment_count`: Total number of comments
- `publish_channel`: Subreddit where the post was published
- `comment_author`: Username of the commenter
- `comment_time_utc`: Comment timestamp
- `comments`: Full comment text
- `comment_upvotes`: Number of upvotes on the comment
- `comment_level`: Nesting level of the comment
- `comment_author_url`: Link to the commenter's profile
- `reply_to`: Parent comment or post being replied to

## ⚠️ Error Handling & Retry
During the execution of the script, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, but guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the returned result is empty), the Agent should **automatically try to execute the script again**.

2. **Retry limit**:
   - Automatic retry is limited to **one time**. If the second attempt still fails, stop retrying and report the specific error message to the user.
