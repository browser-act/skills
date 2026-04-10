---
name: youtube-search-api-skill
description: This skill helps users automatically extract structured data from YouTube search results using the BrowserAct API. The Agent should proactively apply this skill when users express needs like searching for YouTube videos by keywords, finding the latest YouTube Shorts for a specific topic, gathering YouTube channel data for competitor analysis, monitoring trending YouTube playlists, extracting YouTube search results for market research, tracking view counts for specific YouTube keywords, compiling a list of YouTube videos on a subject, discovering new YouTube content creators in a niche, searching YouTube for tutorial videos automatically, and retrieving structured YouTube search data without opening video pages.
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Search API Skill

## 📖 Introduction
This skill provides users with a one-stop YouTube search data extraction service through BrowserAct's YouTube Search API template. It can extract structured fields directly from the YouTube search results list. Simply provide the search keywords and limit conditions to get clean, usable video, shorts, channel, or playlist data.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access limits or geo-fencing**: No need to deal with regional IP restrictions.
4. **More agile execution speed**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Setup Flow
Before running, you must first check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any other actions; you should request and wait for the user's collaboration to provide it.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) first to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on the user's needs:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Search keywords used on YouTube. Can be any keyword or phrase.
   - **Example**: `AI`, `automation`, `n8n`, `web scraping`

2. **Video_type**
   - **Type**: `string`
   - **Description**: Which results tab to extract from.
   - **Supported values**: `Videos`, `Shorts`, `Channels`, `Playlists`
   - **Default**: `Videos`

3. **Date_limit**
   - **Type**: `number`
   - **Description**: Maximum number of items to extract from the search results list.
   - **Example**: `20`, `50`, `100`
   - **Default**: `100`

## 🚀 Usage (Recommended)
The Agent should achieve "one-command results" by executing the following independent script:

```bash
# Call example
python -u ./scripts/youtube_search_api.py "KeyWords" "Video_type" Date_limit
```

### ⏳ Execution Status Monitoring
Because this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`) while running.
**Notice to Agent**:
- While waiting for the script to return results, please keep paying attention to the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Please do not mistakenly judge it as a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting and no result is returned, can you consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script will parse and print the result directly from the API response. The extracted data includes:
- `title`: Title shown in search results
- `description`: Short description snippet (when available)
- `view_count`: View count displayed in results
- `published_at`: Publish time displayed in results
- `url`: Result item URL

## ⚠️ Error Handling & Retry Mechanism
During the execution of the script, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, and you should guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the returned result is empty), the Agent should **automatically try to execute the script again**.

2. **Retry limit**:
   - Automatic retry is limited to **only once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Keyword-first discovery**: Build topic pools and content datasets directly from search intent.
2. **Competitor scanning**: Search for competitor brand names and extract top related videos.
3. **Content monitoring**: Regularly extract search results for specific industry keywords to see what's trending.
4. **Channel research**: Search for channels within a specific niche and gather their URLs.
5. **Tutorial aggregation**: Find and extract educational videos for specific software or tools.
6. **Shorts tracking**: Monitor YouTube Shorts for trending hashtags or topics.
7. **Playlist extraction**: Find curated playlists for specific subjects.
8. **Market research**: Build structured datasets of search results for market analysis.
9. **Creator outreach**: Find emerging creators in a particular field for collaboration.
10. **View count analysis**: Compare view counts of the top videos for various keywords.
