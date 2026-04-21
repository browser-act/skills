---
name: amazon-reviews-api-skill
description: "This skill helps users automatically extract Amazon product reviews via the Amazon Reviews API. Agent should proactively apply this skill when users express needs like getting reviews for Amazon product with ASIN B07TS6R1SF, analyzing customer feedback for a specific Amazon item, getting ratings and comments for a competitive product, tracking sentiment of recent Amazon reviews, extracting verified purchase reviews for quality assessment, summarizing user experiences from Amazon product pages, monitoring product performance through customer reviews, collecting reviewer profiles and links for market research, gathering review titles and descriptions for content analysis, scraping Amazon reviews without requiring a login."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Reviews Automation Extraction Skill

## 📖 Introduction
This skill provides a one-stop Amazon review collection service through BrowserAct's Amazon Reviews API template. It can directly extract structured review results from Amazon product pages. By simply providing an ASIN, you can get clean, usable review data without building crawler scripts or requiring an Amazon account login.

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
When calling the script, the Agent should flexibly configure parameters based on user needs:

1. **ASIN (Amazon Standard Identification Number)**
   - **Type**: `string`
   - **Description**: The unique identifier for the product on Amazon.
   - **Example**: `B07TS6R1SF`, `B08N5WRWJ6`

## 🚀 Usage
The Agent should execute the following independent script to achieve "one-line command result":

```bash
# Example call
python -u ./scripts/amazon_reviews_api.py "ASIN_HERE"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
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
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Competitor Analysis**: Extract reviews for competitors' products to understand their strengths and weaknesses.
2. **Product Feedback**: Summarize feedback for your own products to identify areas for improvement.
3. **Market Research**: Collect data on customer preferences and common complaints in a specific category.
4. **Sentiment Monitoring**: Monitor recent reviews to detect shifts in customer sentiment.
5. **QA Insights**: Use customer reviews to identify potential quality issues or bugs.
6. **Sentiment Analysis Prep**: Gather review text and ratings for detailed emotion modeling.
7. **Verified Purchase Analysis**: Compare feedback from verified vs. unverified buyers.
8. **Geographic Insights**: Analyze product performance across different reviewer countries.
9. **Variant Comparison**: Understand which product variants (size/color) receive the best feedback.
10. **Historical Trend Tracking**: Retrieve and analyze review publication dates to track product lifecycle sentiment.
