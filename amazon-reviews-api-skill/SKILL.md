---
name: amazon-reviews-api-skill
description: This skill helps users automatically extract Amazon product reviews via the Amazon Reviews API. Agent should proactively apply this skill when users express needs like: 1. Get reviews for Amazon product with ASIN B07TS6R1SF; 2. Analyze customer feedback for a specific Amazon item; 3. Get ratings and comments for a competitive product; 4. Track sentiment of recent Amazon reviews; 5. Extract verified purchase reviews for quality assessment; 6. Summarize user experiences from Amazon product pages; 7. Monitor product performance through customer reviews; 8. Collect reviewer profiles and links for market research; 9. Gather review titles and descriptions for content analysis; 10. Scrape Amazon reviews without requiring a login.
---

# Amazon Reviews Automation Extraction Skill

## 📖 Introduction
This skill provides a one-stop Amazon review collection service through BrowserAct's Amazon Reviews API template. It can directly extract structured review results from Amazon product pages. By simply providing an ASIN, you can get clean, usable review data without building crawler scripts or requiring an Amazon account login.

## ✨ Features
1. **No Hallucination, Ensuring Stable and Accurate Extraction**: Preset workflows avoid AI-generated hallucinations.
2. **No Anti-Bot Issues**: Built-in mechanisms bypass reCAPTCHA and other verification challenges.
3. **No IP Restrictions or Geofencing**: Breaks through regional IP limits to ensure stable global access.
4. **Agile Execution**: Tasks run faster than pure AI-driven browser automation solutions.
5. **High Cost-Efficiency**: Significantly reduces data acquisition costs compared to token-heavy AI schemes.

## 🔑 API Key Setup Flow
Before running, you must check for the `BROWSERACT_API_KEY` environment variable. If it's not set, do not take other actions; instead, request and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me here."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure parameters based on user needs:

1. **ASIN (Amazon Standard Identification Number)**
   - **Type**: `string`
   - **Description**: The unique identifier for the product on Amazon.
   - **Example**: `B07TS6R1SF`, `B08N5WRWJ6`

## 🚀 Usage (Recommended)
The Agent should execute the following standalone script to "get results in one line":

```bash
# Example call
python -u ./scripts/amazon_reviews_api.py "ASIN_HERE"
```

### ⏳ Runtime Monitoring
Since this task involves automated browser operations, it may take several minutes. The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Note**:
- Keep monitoring the terminal output while waiting for results.
- As long as the terminal is outputting new status logs, the task is running normally; do not misjudge it as stuck or unresponsive.
- Only consider retrying if the status remains unchanged for a long time or the script stops outputting without returning results.

## 📊 Output Data
After successful execution, the script will parse and print results directly from the API response. Each review item includes:
- `Commentator`: Reviewer's name
- `Commenter profile link`: Link to the reviewer's profile
- `Rating`: Star rating
- `reviewTitle`: Headline of the review
- `review Description`: Full text of the review
- `Published at`: Date the review was published
- `Country`: Reviewer's country
- `Variant`: Product variant info (if available)
- `Is Verified`: Whether it's a verified purchase

## ⚠️ Error Handling & Retry
If an error occurs (e.g., network issues or task failure), follow this logic:

1. **Check Output**:
   - If output contains `"Invalid authorization"`, the API Key is invalid or expired. **Do not retry**; guide the user to check and provide a correct API Key.
   - If output does **not** contain `"Invalid authorization"` but the task fails (e.g., starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute** the script once.

2. **Retry Limit**:
   - Automatic retry is limited to **once**. If the second attempt fails, stop and report the specific error to the user.

## 🌟 Typical Use Cases
1. **Competitor Analysis**: Extract reviews for competitors' products to understand their strengths and weaknesses.
2. **Product Feedback**: Summarize feedback for your own products to identify areas for improvement.
3. **Market Research**: Collect data on customer preferences and common complaints in a specific category.
4. **Sentiment Monitoring**: Monitor recent reviews to detect shifts in customer sentiment.
5. **QA Insights**: Use customer reviews to identify potential quality issues or bugs.
