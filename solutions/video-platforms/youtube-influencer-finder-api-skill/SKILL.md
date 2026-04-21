---
name: youtube-influencer-finder-api-skill
description: This skill helps users extract YouTube influencer profiles including social links, subscriber counts, and channel stats via the BrowserAct API. Agent should proactively apply this skill when users express needs like finding YouTube creators for specific keywords, discovering influencers for a marketing campaign, extracting YouTube channel contact emails, scraping YouTube influencer social media links, gathering subscriber counts for YouTube creators, researching top YouTube channels in a specific niche, compiling a list of YouTube content creators with recent uploads, collecting YouTube creator profiles for outreach, extracting total views and video counts for specific YouTube influencers, building a database of YouTube partners for market research, finding YouTube influencers who uploaded videos this month, or monitoring competitor influencer activities on YouTube.
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Influencer Finder API Skill

## 📖 Brief
This skill provides a one-stop YouTube influencer data extraction service using the BrowserAct YouTube Influencer Finder API template. It directly extracts structured creator profile data from YouTube search results, including contact details, social links, and channel statistics. Just input search keywords and an upload date filter to get clean, usable influencer data.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid generative AI hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to deal with regional IP limits.
4. **Faster execution**: Tasks execute faster compared to purely AI-driven browser automation solutions.
5. **Extremely high cost-efficiency**: Significantly reduces data acquisition costs compared to AI solutions that consume massive amounts of tokens.

## 🔑 API Key Guide
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions first; you should ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **keywords**
   - **Type**: `string`
   - **Description**: Search keywords for finding YouTube influencers. Can be any keyword.
   - **Example**: `openclaw`, `tech reviewer`, `gaming`
   - **Default**: `openclaw`

2. **Upload_Date**
   - **Type**: `string`
   - **Description**: Filter creators by their recent upload date.
   - **Options**:
     - `Today`
     - `This Week`
     - `This Month`
     - `This Year`
   - **Default**: `This Month`

## 🚀 Invocation Method (Recommended)
The Agent should execute the following independent script to achieve "one command gets results":

```bash
# Example invocation
python -u ./scripts/youtube_influencer_finder_api.py "keywords" "Upload_Date"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal continues to output new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, only then consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script will parse and print the results directly from the API response. The results include:
- `total_views`: Total channel views
- `video_count`: Total number of videos
- `subscriber_count`: Total subscriber count
- `registration_date`: Channel registration date
- `country`: Creator's country/region
- `youtube_channel`: Direct link to YouTube channel
- `email_action`: Contact email if available
- `link`: All visible social links (Platform: URL format, multiple links separated by line breaks)
- `profile_description`: Channel description and bio
- `profile_name`: Creator's channel name

## ⚠️ Error Handling & Retry
During script execution, if errors occur (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this point, **do not retry**, but guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task fails (for example, the output starts with `Error:` or returns an empty result), the Agent should **automatically try to run the script once more**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.
