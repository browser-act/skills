---
name: youtube-video-api-skill
description: This skill helps users automatically extract channel-level and video detail data from a specific YouTube channel via BrowserAct API. Agent should proactively apply this skill when users express needs like extracting channel video data, getting latest or popular videos from a YouTube channel, tracking competitor channel content, extracting video metrics such as views likes comments, retrieving subscriber count and channel info, monitoring posting cadence of a YouTube channel, gathering video data for content strategy analysis, getting earliest videos of a YouTube creator, analyzing engagement signals across a full channel, and downloading structured YouTube video details without manual scraping.
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Video API Skill

## 📖 Introduction
This skill provides users with a one-stop YouTube video data extraction service using BrowserAct's YouTube Video API template. It can directly extract structured channel-level data plus video detail data from a specific YouTube channel through a single API request. Just input the YouTube channel URL and video type (Latest, Popular, or Earliest), and you can get clean, ready-to-use video metrics.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid generative AI hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions and geo-blocking**: No need to deal with regional IP restrictions.
4. **More agile execution speed**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of Tokens.

## 🔑 API Key Guidance Flow
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions first. You should request and wait for the user to provide it collaboratively.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **YouTube_channel_url**
   - **Type**: `string`
   - **Description**: Target YouTube channel URL used to load the channel video list.
   - **Example**: `https://www.youtube.com/@BrowserAct`

2. **Video_type**
   - **Type**: `string`
   - **Description**: Which ordering mode to use when traversing the channel video list.
   - **Optional Values**:
     - `Latest`
     - `Popular`
     - `Earliest`
   - **Default**: `Popular`

## 🚀 Invocation Method
The Agent should implement "one command gets results" by executing the following independent script:

```bash
# Invocation example
python -u ./scripts/youtube_video_api.py "YouTube_channel_url" "Video_type"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Agent Instructions**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting and no result is returned, the retry mechanism can be considered.

## 📊 Data Output Description
After successful execution, the script will parse and print the results directly from the API response. The results include:
### Channel fields
- `channel_title`: Channel name displayed on the channel page
- `channel_url`: Channel URL
- `subscribers`: Subscriber count shown on the channel page
### Video fields
- `video_title`: Video title shown on the video page
- `video_url`: Video URL
- `publish_date`: Published date or time shown on YouTube
- `view_count`: View count shown on YouTube
- `video_duration`: Video duration
- `comment_count`: Total number of comments (if available)
- `like_count`: Like count (if available)

## ⚠️ Error Handling & Retry
During script execution, if an error occurs (such as network fluctuation or task failure), the Agent should follow the logic below:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, but guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the return result is empty), the Agent should **automatically try to execute the script once more**.

2. **Retry limits**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Competitor Tracking**: Track performance trends and posting cadence of a competitor's channel.
2. **Creator Research**: Analyze engagement signals and popular videos of content creators.
3. **Content Ops Reporting**: Monitor channel videos and performance metrics for reporting.
4. **Growth Analytics**: Understand what video types (Latest/Popular) drive growth.
5. **Database Automation**: Send channel videos directly into CRM or databases without manual export.
6. **Market Research**: Aggregate video metrics across different channels in a specific industry.
7. **Trend Spotting**: Identify the most popular videos on specific tech or gaming channels.
8. **Audience Engagement Analysis**: Correlate subscriber counts with video views and likes.
9. **Content Strategy**: Review a channel's earliest videos to understand their origin and growth path.
10. **Automated Social Monitoring**: Keep tabs on new content released by key industry leaders.