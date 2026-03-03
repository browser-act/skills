---
name: youtube-channel-api-skill
description: "This skill helps users automatically extract structured channel data from YouTube search results via BrowserAct API. Agent should proactively apply this skill when users express needs like finding YouTube channels about specific topics, collecting data on YouTube content creators, tracking YouTube influencers in specific industries, getting YouTube channel information for competitor analysis, searching for YouTube channels related to keywords, monitoring YouTube channel updates for specific keywords, finding YouTube channels that recently published videos, extracting YouTube channel subscriber counts, discovering YouTube vloggers in specific niches, building a YouTube channel database for market research, batch extracting YouTube channel links and descriptions, or monitoring competitor channel growth."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["pyhon"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Channel API Skill

## 📖 Introduction
This skill provides users with a one-stop channel data extraction service through BrowserAct's YouTube Channel API template. It can directly extract structured channel results from YouTube search. By simply entering search keywords and optional upload date filters, you can get clean, usable channel data directly.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows to avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to handle regional IP restrictions.
4. **Faster execution**: Faster task execution compared to purely AI-driven browser automation solutions.
5. **High cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guide
Before running, you must first check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you should request and wait for the user to provide it.
**The Agent must inform the user at this point**:
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
Agent should flexibly configure the following parameters according to user needs when calling the script:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Search keywords used to find YouTube channels.
   - **Example**: `AI`, `automation`, `tech reviews`

2. **Upload_date**
   - **Type**: `string`
   - **Description**: Filter channels that have published content within a defined time window.
   - **Optional Values**: `This week`, `Any time`, etc.
   - **Default**: `Any time`

## 🚀 Usage
Agent should execute the following standalone script to achieve "one command gets results":

```bash
# Example call
python -u ./scripts/youtube_channel_api.py "Search Keywords" "Upload date"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Agent Notes**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal continues to output new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, then consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script will directly parse and print the results from the API response. The results include:
- `channel_title`: Channel name displayed on YouTube
- `channel_link`: Channel page URL
- `verified`: Whether the channel is verified
- `handle`: Channel handle
- `subscribers`: Subscriber count
- `description`: Channel description text
- `thumbnail`: Channel avatar or thumbnail image URL

## ⚠️ Error Handling & Retry
During the execution of the script, if an error occurs (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this point, **do not retry**; you should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or returns empty results), the Agent should **automatically try to execute the script one more time**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Creator Discovery**: Find channels related to specific topics for outreach.
2. **Influencer Sourcing**: Identify potential influencers in specific industries.
3. **Competitive Landscape Mapping**: Track competitors' channel growth and updates.
4. **Channel Database Building**: Extract structured data for building creator databases.
5. **Content Trend Tracking**: Monitor new channels popping up around a specific keyword.
6. **Market Research**: Collect data on leading YouTube channels in a target niche.
7. **Brand Monitoring**: Track unofficial or related channels discussing your brand.
8. **Audience Analysis**: Assess the size of audiences in specific fields via subscriber counts.
9. **Partnership Campaigns**: Find active channels that uploaded videos recently.
10. **Automated Data Enrichment**: Pipe YouTube channel details into CRMs or internal tools.