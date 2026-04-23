---
name: youtube-batch-transcript-extractor-api-skill
description: "This skill helps users automatically extract YouTube video transcripts and metadata in batch via the BrowserAct API. The Agent should proactively apply this skill when users express needs like batch extract full transcripts from YouTube videos for specific keywords, scrape YouTube subtitles for a list of videos, get batch video metadata and likes counts for analysis, automate YouTube search and subtitle extraction, collect multiple video transcripts published this week, download bulk YouTube video subtitles without writing crawler scripts, build a dataset of transcripts from top YouTube videos, extract YouTube video URLs and publisher info in batch, gather full video content for AI summarization pipelines, monitor recent YouTube videos and extract their transcripts, batch retrieve structured subtitle data for media research, extract transcripts from trending YouTube content automatically."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Batch Transcript Extractor API Skill

## 📖 Introduction
This skill uses the BrowserAct YouTube Batch Transcript Extractor API template to provide users with an automated service for extracting YouTube video transcripts and metadata in batch. Simply by providing search keywords and filters, you can batch extract full video transcripts, likes, and channel metadata without writing crawler scripts.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid generative AI hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions or geofencing**: No need to deal with regional IP restrictions.
4. **Faster execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **High cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guide Process
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you should request and wait for the user to provide it collaboratively.
**The Agent must inform the user at this time**:
> "Since you have not yet configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key first."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: The keyword to search for on YouTube.
   - **Example**: `OpenClaw`, `AI Automation`

2. **Upload_date**
   - **Type**: `string`
   - **Description**: Filter for the upload date of the videos.
   - **Optional values**: `Today`, `This week`, `This month`, `This year`.
   - **Default value**: `This week`

3. **Datelimit**
   - **Type**: `number`
   - **Description**: The number of videos to extract. Adjust as needed.
   - **Default value**: `5`
   - **Recommendation**: Set a smaller value (1-5) for quick tests and a larger value for bulk extraction.

## 🚀 Invocation Method (Recommended)
The Agent should execute the following independent script to achieve "one-line command to get results":

```bash
# Example invocation
python -u ./scripts/youtube_batch_transcript_extractor_api.py "keywords" "Upload_date" Datelimit
```

### ⏳ Execution Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output timestamped status logs** (e.g., `[14:30:05] Task Status: running`) while running.
**Agent Notes**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Please do not mistakenly judge it as a deadlock or unresponsiveness.
- Only consider triggering the retry mechanism if the status remains unchanged for a long time or the script stops outputting without returning a result.

## 📊 Data Output Description
After successful execution, the script will parse and print the results directly from the API response. The results include:
- `Video title`: The title of the YouTube video.
- `Video URL`: The direct link to the original video.
- `Publisher`: The name of the channel publishing the video.
- `Channel link`: The URL of the publisher's YouTube channel.
- `Video likes count`: The number of likes the video has received.
- `Subtitles`: The complete extracted transcript/subtitles of the videos.

## ⚠️ Error Handling & Retry
If an error is encountered during the execution of the script (such as network fluctuation or task failure), the Agent should follow the logic below:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it indicates that the API Key is invalid or expired. **Do not retry** at this time. You should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or returns an empty result), the Agent should **automatically try to execute the script once more**.

2. **Retry limits**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.
