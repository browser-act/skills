---
name: business-contact-social-links-skill
description: "This skill helps users automatically extract official website and social media profiles. Agent should proactively apply this skill when users express needs like search for official website and social media contacts of a company, find YouTube and LinkedIn profiles by company name, extract social media links from a specific website URL, discover a company's X and Facebook presence, gather business contact details using their brand name, retrieve TikTok and Instagram links from a target website, track competitor social media strategy, extract multi-platform social links for lead generation, find official contact channels of local businesses, collect canonical profile URLs for outreach campaigns, or build a contact database from Yellow Pages leads."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Business Contact & Social Links Extractor Skill

## 📖 Brief
This skill integrates two BrowserAct templates to cover two common scenarios. When the user provides a **company name**, it searches Google to extract the company's official website and social media channels. When the user provides a **website URL**, it scrapes the site to extract social media profile links (LinkedIn, Facebook, X/Twitter, Instagram, YouTube, TikTok). The script auto-detects the input type and routes to the correct template.

## ✨ Features
1. **No Hallucinations**: Pre-set workflows avoid AI generative hallucinations, ensuring stable and precise data extraction.
2. **No Captcha Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions**: No need to handle regional IP restrictions or geofencing.
4. **Faster Execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **Cost-Effective**: Significantly lowers data acquisition costs compared to high-token-consuming AI solutions.

## 🔑 API Key Setup
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other measures; ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key yet, please visit the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
The agent should determine whether the input is a company name or a website URL and pass it to the script. The script automatically routes the request to the correct template.

1. **Target (Company Name or Website URL)**
   - **Required**: Yes
   - **Type**: `string`
   - **Description**: The name of the company to search for, or the direct website URL to scrape social links from.
   - **Example**: `OpenAI` or `https://www.rotorooter.com/`

## 🚀 Invocation Method
Agent should execute the following command to invoke the skill:

```bash
# Search by company name
python -u ./scripts/business_contact_social_links.py "OpenAI"

# Scrape by website URL
python -u ./scripts/business_contact_social_links.py "https://www.rotorooter.com/"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take several minutes. The script outputs **timestamped status logs** continuously (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- Monitor the terminal output while waiting.
- As long as new status logs appear, the task is running normally; do not misjudge it as frozen.
- Only consider triggering retry if the status remains unchanged for a long time or output stops without a final result.

## 📊 Data Output
Upon successful execution, the script prints structured JSON data extracted from the API response.

**If a Company Name was provided**, the output includes:
- `Company Name`: The official name of the company.
- `Current Page URL`: The official website URL.
- `Social Media Information`: A consolidated list of discovered social media profiles.

**If a Website URL was provided**, the output includes an array of objects:
- `platform`: Platform name (e.g., LinkedIn, YouTube).
- `url`: Canonical URL of the external profile.

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **contains** `"concurrent"` or `"too many running tasks"`, it means the concurrent task limit has been reached. **Do not retry**; guide the user to upgrade their plan.
     **Agent must inform the user**:
     > "The current task cannot be executed because your BrowserAct account has reached the concurrent task limit. Please visit the [BrowserAct Plan Upgrade Page](https://www.browseract.com/reception/recharge) to upgrade your plan."
   - If the output **does not contain the above error keywords** but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error to the user.

## 🌟 Typical Use Cases
1. **Sales Lead Enrichment**: Find the official website and social channels for a list of company names.
2. **Influencer Outreach**: Extract all social media profiles from a creator's personal website.
3. **Competitor Analysis**: Discover which social media platforms a rival company prioritizes.
4. **CRM Data Cleaning**: Verify and populate missing social links and official URLs for existing leads.
5. **Multi-Channel Marketing**: Build targeted lists of businesses with active social media presence.
6. **Social Listening Setup**: Quickly gather official handles to monitor brand mentions.
7. **B2B Prospecting**: Combine with Yellow Pages data to build complete business intelligence profiles.
8. **Partner Vetting**: Evaluate the digital footprint of a potential business partner using just their name.
9. **Directory Building**: Automate the collection of website and social links for a local business directory.
10. **Brand Tracking**: Track all official contact channels of specific brands across the web.
