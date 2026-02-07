---
name: google-maps-reviews-api-skill
description: This skill is designed to help users automatically extract reviews from Google Maps via the Google Maps Reviews API. Agent should proactively apply this skill when users request to: 1. Find reviews for local businesses (e.g., coffee shops, clinics); 2. Monitor customer feedback for a specific brand or location; 3. Analyze sentiment of reviews for competitors; 4. Extract reviews for a chain of stores or services; 5. Track reputation of a local restaurant; 6. Gather user testimonials for a specific venue; 7. Conduct market research on service quality of local businesses; 8. Monitor reviews for a new retail location; 9. Collect feedback on public attractions or parks; 10. Identify common complaints for a specific service provider; 11. Research the best-rated places in a city; 12. Analyze recurring themes in reviews for a specific industry.
---

# Google Maps Reviews Automation Skill

## 📖 Introduction
This skill provides a one-stop review collection service using BrowserAct's Google Maps Reviews API template. It can extract structured review data directly from Google Maps search results. Simply provide the search keywords, language, and country to get clean, usable review data.

## ✨ Capability Features
1. **No Hallucination, Precision Data Extraction**: Uses preset workflows to avoid AI-generated hallucinations.
2. **No CAPTCHA Issues**: Built-in mechanisms to bypass reCAPTCHA or other verification challenges.
3. **No IP Restrictions or Geo-fencing**: Breaks through regional IP limits to ensure stable access worldwide.
4. **Agile Execution**: Faster task execution compared to pure AI-driven browser automation solutions.
5. **High Cost-Effectiveness**: Significantly reduces data acquisition costs compared to high-token-consumption AI solutions.

## 🔑 API Key Guidance
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other measures; instead, request the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat."

## 🛠️ Input Parameters Details
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

## 🚀 Invocation Method (Recommended)
The Agent should execute the following script to get results:

```bash
# Example call
python -u ./.cursor/skills/google-maps-reviews-api-skill/scripts/google_maps_reviews_api.py "Keywords" "Language" "Country"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take several minutes. The script will continuously output status logs with timestamps (e.g., `[14:30:05] Task Status: running`).
**Agent Notes**:
- Stay focused on the terminal output while waiting for results.
- As long as the terminal is outputting new status logs, the task is running normally; do not misjudge it as hung or non-responsive.
- If the status remains unchanged for a long time or the script stops outputting without returning results, consider a retry.

## 📊 Output Data Description
After successful execution, the script parses and prints results from the API response:
- `author_name`: Display name of the reviewer
- `author_profile_url`: Profile URL of the reviewer
- `rating`: Star rating
- `text`: Review text content
- `comment_date`: Human-readable date
- `likes_count`: Number of likes
- `author_image_url`: Reviewer's avatar URL

## ⚠️ Exception Handling & Retry Mechanism
If an error occurs (e.g., network fluctuations or task failure), follow this logic:

1. **Check Output Content**:
   - If output contains `"Invalid authorization"`, the API Key is invalid or expired. **Do not retry**; guide the user to provide a correct Key.
   - If output does not contain `"Invalid authorization"` but the task fails (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-run the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If the second attempt fails, stop and report the error to the user.

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
