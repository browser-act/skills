---
name: google-maps-reviews-api-skill
description: "This skill is designed to help users automatically extract reviews from Google Maps via the Google Maps Reviews API. Agent should proactively apply this skill when users request to find reviews for local businesses (e.g., coffee shops, clinics), monitor customer feedback for a specific brand or location, analyze sentiment of reviews for competitors, extract reviews for a chain of stores or services, track reputation of a local restaurant, gather user testimonials for a specific venue, conduct market research on service quality of local businesses, monitor reviews for a new retail location, collect feedback on public attractions or parks, identify common complaints for a specific service provider, research the best-rated places in a city, analyze recurring themes in reviews for a specific industry."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Google Maps Reviews Automation Skill

## 📖 Introduction
This skill provides a one-stop review collection service using BrowserAct's Google Maps Reviews API template. It can extract structured review data directly from Google Maps search results. Simply provide the search keywords, language, and country to get clean, usable review data.

## ✨ Features
1. **No Hallucinations**: Pre-set workflows avoid AI generative hallucinations, ensuring stable and precise data extraction.
2. **No Captcha Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions**: No need to handle regional IP restrictions or geofencing.
4. **Faster Execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **Cost-Effective**: Significantly lowers data acquisition costs compared to high-token-consuming AI solutions.

## 🔑 API Key Setup
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other measures; ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please visit the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
The Agent should flexibly configure the following parameters when calling the script:

1. **KeyWords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The query used to find places on Google Maps (e.g., business names, categories).
   - **Example**: `coffee shop`, `dental clinic`, `Tesla showroom`

2. **language (Language)**
   - **Type**: `string`
   - **Description**: Sets the UI language and the language of the returned text.
   - **Supported values**: `en`, `zh-CN`, `es`, `fr`, etc.
   - **Default**: `en`

3. **country (Country)**
   - **Type**: `string`
   - **Description**: Country or region bias for search results.
   - **Supported values**: `us`, `gb`, `ca`, `au`, `jp`, etc.
   - **Default**: `us`

## 🚀 Usage
Agent should use the following independent script to achieve "one-line command result":

```bash
# Example call
python -u ./scripts/google_maps_reviews_api.py "Keywords" "Language" "Country"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script parses and prints results from the API response:
- `author_name`: Display name of the reviewer
- `author_profile_url`: Profile URL of the reviewer
- `rating`: Star rating
- `text`: Review text content
- `comment_date`: Human-readable date
- `likes_count`: Number of likes
- `author_image_url`: Reviewer's avatar URL

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Local Business Analysis**: Find reviews for cafes or clinics in a specific area.
2. **Reputation Monitoring**: Track feedback for a specific brand location.
3. **Competitive Benchmarking**: Analyze reviews of competitor stores.
4. **Sentiment Analysis**: Gather review text for emotion and topic modeling.
5. **Market Research**: Evaluate service quality across different regions.
6. **Lead Qualification**: Use review data to identify high-quality service providers.
7. **Customer Insight**: Understand recurring complaints or praises.
8. **Venue Research**: Collect testimonials for parks, museums, or attractions.
9. **Retail Monitoring**: Gather feedback for newly opened stores.
10. **Service Quality Audit**: Analyze ratings and comments for a specific service chain.
