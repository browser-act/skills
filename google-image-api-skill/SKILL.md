---
name: google-image-api-skill
description: This skill helps users automatically extract structured image data from Google Images via BrowserAct API. Agent should proactively apply this skill when users express needs like finding images for specific keywords, gathering product style images for competitors, building visual datasets at scale, scanning visual search results for market research, tracking localized image trends by country, compiling related image thumbnails and links, extracting image titles and source logos, fetching click through URLs from image results, monitoring competitor visual assets, sourcing creative content for specific topics, looking up product pictures in different regions, collecting structured image metadata without opening detail pages.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["pyhon"],"env":["BROWSERACT_API_KEY"]}}}
---

# Google Image API Automation Skill

## 📖 Introduction
This skill provides users with one-click image data extraction directly from Google Images using the BrowserAct Google Image API template. It allows you to search with keywords, set country and language, control scroll depth and result limits, returning clean, structured image metadata directly via API.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid generative AI hallucinations.
2. **No CAPTCHA issues**: No need to deal with reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to handle regional IP limitations.
4. **Agile execution speed**: Faster task execution compared to pure AI-driven browser automation solutions.
5. **High cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of tokens.

## 🔑 API Key Guide
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take any further action; you should request and wait for the user to provide it collaboratively.
**The Agent must inform the user at this point**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key first."

## 🛠️ Input Parameters
The Agent should flexibly configure the following parameters according to user needs when calling the script:

1. **KeyWords (Search keywords)**
   - **Type**: `string`
   - **Description**: Search keywords used on Google Images.
   - **Example**: `flower`, `ai agent`, `tesla`

2. **Country (Country or region bias)**
   - **Type**: `string`
   - **Description**: Country or region bias for results.
   - **Supported values**: `us`, `gb`, `ca`, `au`, `de`, `fr`, `es`, `jp`, `kr`
   - **Default**: `us`

3. **Language (UI language)**
   - **Type**: `string`
   - **Description**: UI language for the Google Images session and returned text.
   - **Supported values**: `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `fr`, `de`, `es`
   - **Default**: `en`

4. **Scroll_count (Number of scroll actions)**
   - **Type**: `number`
   - **Description**: Number of scroll actions to load more image results.
   - **Default**: `5`

5. **Datelimit (Maximum items)**
   - **Type**: `number`
   - **Description**: Maximum number of items to extract from the results list.
   - **Default**: `50`

## 🚀 Invocation (Recommended)
The Agent should execute the following independent script to achieve "results with one command":

```bash
# Example invocation
python -u ./scripts/google_image_api.py "KeyWords" "Country" "Language" Scroll_count Datelimit
```

### ⏳ Execution Status Monitoring
Since this task involves automated browser operations, it may take a considerable amount of time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent Notice**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal is outputting new status logs, it means the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, then consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script will parse and print the results directly from the API response. The results include:
- `is_product`: Whether the result is detected as a product-style listing
- `link`: Click-through URL associated with the result
- `title`: Image result title or caption text
- `source_logo`: Source site logo URL
- `source`: Source site name shown in results
- `related_content_id`: Google Images related content identifier
- `thumbnail`: Thumbnail image URL
- `index`: Result index in the list

## ⚠️ Error Handling & Retry
During the execution of the script, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. In this case, **do not retry**; guide the user to check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the result is empty), the Agent should **automatically try executing the script one more time**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Visual Content Sourcing**: Finding specific imagery for creative research and design content.
2. **Competitor Asset Monitoring**: Scanning Google Images for competitor product styles and logos.
3. **Market Visual Research**: Building datasets of product listings across various countries.
4. **Localized Image Trends**: Tracking what images appear for specific terms in Japan (`jp`) or France (`fr`).
5. **E-commerce Discovery**: Extracting click-through links to track down where products are sold.
6. **Data Enrichment**: Fetching thumbnails and high-level titles associated with keywords.
7. **Brand Tracking**: Finding instances of specific brands appearing as image results.
8. **SEO Keyword Visualization**: Checking the visual results that rank for chosen SEO keywords.
9. **Automated Content Aggregation**: Delivering daily list-level visual metadata for specific topics.
10. **Global Image Search**: Finding images related to global events or personalities in their native languages.
