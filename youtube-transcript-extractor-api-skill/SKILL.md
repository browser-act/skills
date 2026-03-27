---
name: youtube-transcript-extractor-api-skill
description: "This skill helps users automatically extract YouTube video transcripts and metadata via the BrowserAct API. The Agent should proactively apply this skill when users express needs like extracting full transcript from a specific YouTube video, getting subtitles and metadata for video content analysis, gathering video titles and likes counts, summarizing YouTube videos without watching them, collecting channel details from a video URL, tracking transcript automation for specific videos, scraping YouTube subtitles for internal knowledge bases, fetching full video content for AI summarization pipelines, downloading structured transcripts from YouTube links, analyzing video text content for media research, monitoring video publisher information and channel links, or building datasets from YouTube video transcripts."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Transcript Extractor API Skill

## 📖 Introduction
This skill provides a one-stop video transcript extraction service using BrowserAct's YouTube Transcript Extractor API template. It can directly extract full video transcripts and metadata from any YouTube video. By simply providing the TargetURL, you can get clean, ready-to-use transcript and metadata.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid generative AI hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions or geofencing**: No need to deal with regional IP limits.
4. **Faster execution**: Compared to pure AI-driven browser automation solutions, task execution is much faster.
5. **High cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume large amounts of tokens.

## 🔑 API Key Setup
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you must request and wait for the user to provide it.
**The Agent must inform the user at this point**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key first."

## 🛠️ Input Parameters
The Agent should configure the following parameter based on the user's needs when calling the script:

1. **TargetURL (Target URL)**
   - **Type**: `string`
   - **Description**: The URL of the YouTube video you want to extract the transcript and metadata from.
   - **Example**: `https://www.youtube.com/watch?v=st534T7-mdE`

## 🚀 Usage (Recommended)
The Agent should execute the following independent script to achieve "one command, get results":

```bash
# Example Call
python -u ./scripts/youtube_transcript_extractor_api.py "TargetURL"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). While running, the script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal continues to output new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result, should you consider triggering the retry mechanism.

## 📊 Data Output Description
After successful execution, the script will parse and print the results directly from the API response. The results include:
- `video_title`: The title of the YouTube video
- `video_url`: The direct link to the original video
- `publisher`: The name of the channel publishing the video
- `channel_link`: The URL of the publisher's YouTube channel
- `video_likes_count`: The number of likes the video has received
- `transcript`: The complete extracted transcript/subtitles of the video

## ⚠️ Error Handling & Retry
During script execution, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. In this case, **do not retry**, and guide the user to check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or returns an empty result), the Agent should **automatically try to execute the script one more time**.

2. **Retry limits**:
   - Automatic retry is limited to **only once**. If the second attempt still fails, stop retrying and report the specific error message to the user.
