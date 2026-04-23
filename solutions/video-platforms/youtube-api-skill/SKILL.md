---
name: youtube-api-skill
description: "This skill helps users automatically extract detailed video metrics and channel information from YouTube based on keyword searches using the BrowserAct API. The Agent should proactively apply this skill when users express needs such as extract specific keyword YouTube video detailed data, monitor the latest video performance of competitor channels, collect comment and like counts for videos on a specific topic, find AI agent tutorials published this week and extract metrics, evaluate total views and subscriber info for specific videos, scrape detailed metrics of marketing campaign videos, track video trends for a tech topic periodically, get high quality video list data for specified keywords on YouTube, mine detailed information of the latest YouTube videos, collect video duration and engagement data for specific industries, or monitor YouTube content creator performance metrics."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube API Automated Extraction Skill

## 📖 Skill Introduction
This skill provides users with an automated data extraction service through BrowserAct's YouTube API template. It can directly extract structured video metrics and channel information from YouTube. By simply inputting search keywords and upload date filters, it traverses the video results list, opens each video detail page, and directly returns clean, ready-to-use data.

## ✨ Features
1. **No Hallucinations, Ensuring Stable and Accurate Data Extraction**: Pre-set workflow avoids AI-generated hallucinations.
2. **No CAPTCHA Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions and Geofencing**: No need to deal with regional IP restrictions.
4. **Faster Execution Speed**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **Extremely High Cost-Effectiveness**: Compared to AI solutions that consume a large amount of tokens, it can significantly reduce data acquisition costs.

## 🔑 API Key Guide Flow
Before running, you need to check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions first. You should request and wait for the user to provide it collaboratively.
**Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
When invoking the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords (Search Keywords)**
   - **Type**: `string`
   - **Description**: Search keywords used to find videos on YouTube.
   - **Example**: `Openclaw`, `AI agent`, `browser automation`

2. **Upload_date (Upload Date Filter)**
   - **Type**: `string`
   - **Description**: Filter videos by recency in YouTube search results.
   - **Supported values**: 
     - `Today`
     - `This week`
     - `This month`
     - `This year`
   - **Default**: `This week`

## 🚀 Invocation Method (Recommended)
The Agent should execute the following standalone script to achieve "one command to get results":

```bash
# Invocation example
python -u ./scripts/youtube_api.py "keywords" "upload_date"
```

### ⏳ Execution Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Notice for Agent**:
- While waiting for the script to return results, please keep paying attention to the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Please do not misjudge it as a deadlock or unresponsive.
- If the status remains unchanged for a long time or the script stops outputting and no result is returned, the retry mechanism can be considered.

## 📊 Data Output Description
After successful execution, the script will directly parse and print the results from the API response. The results include:
- `channel_title`: Channel name displayed on the video page
- `channel_url`: Channel URL
- `subscribers`: Subscriber count shown on the channel
- `video_title`: Video title shown on the video page
- `video_url`: Video URL
- `publish_date`: Publish date or time shown on YouTube
- `view_count`: View count shown on YouTube
- `video_duration`: Video duration
- `comment_count`: Total comment count
- `like_count`: Like count

## ⚠️ Error Handling & Retry
During the execution of the script, if an error is encountered (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, you should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the returned result is empty), the Agent should **automatically try to execute the script again once**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Content Monitoring**: Weekly track and extract detailed performance metrics of specific topics.
2. **Competitor Scanning**: Analyze the recent video details, views, and likes of competitor channels.
3. **Campaign Tracking**: Track specific promotional campaigns and evaluate their video interaction metrics.
4. **Market Research**: Collect structured data of videos in specific niches for deep research.
5. **Trend Analysis**: Analyze which types of videos have higher engagement rates in a specific industry.
6. **Creator Analytics**: Monitor specific YouTube creators' video durations, views, and comments.
7. **Engagement Evaluation**: Gather comment and like counts across multiple videos for sentiment estimation.
8. **Video Discovery**: Find top-performing tutorials or product reviews from the past week.
9. **Data Enrichment**: Build searchable video intelligence datasets for BI tools or CRM.
10. **Automated Reporting**: Extract weekly video performance metrics to feed into reporting workflows.
