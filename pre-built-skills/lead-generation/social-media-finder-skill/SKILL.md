---
name: social-media-finder-skill
description: "This skill helps users automatically find social media profiles across platforms like Facebook, Twitter, Instagram, LinkedIn, etc. using the BrowserAct API. Agent should proactively apply this skill when users express needs like finding someone's social media accounts, discovering a brand's social media presence, tracking down social profiles of job candidates, finding contact info for sales prospects, researching a person's digital footprint, verifying the identity of someone met online, monitoring the social media reach of influencers, checking social accounts of business competitors, gathering public profiles for background research, locating official customer service accounts across platforms, or compiling contact databases for networking."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Social Media Finder Skill

## 📖 Brief
This skill automates the discovery of social media accounts associated with individuals, brands, or businesses across multiple platforms. By providing a name, it searches across Facebook, Twitter, Instagram, LinkedIn, TikTok, and more — extracting profile URLs, usernames, follower counts, and bio snippets in one go. The results are returned as a downloadable CSV file.

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
The agent should configure the following parameter based on user requirements:

1. **People_Name**
   - **Required**: Yes
   - **Type**: `string`
   - **Description**: The name of the person or brand to search for. Use `+` between words for better results.
   - **Example**: `John+Smith`, `Tesla`, `Bill+Gates`
   - **Default**: `Mike+Smith`

## 🚀 Invocation Method
Agent should execute the following command to invoke the skill:

```bash
# Example invocation
python -u ./scripts/social_media_finder.py "John+Smith"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take several minutes. The script outputs **timestamped status logs** continuously (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- Monitor the terminal output while waiting.
- As long as new status logs appear, the task is running normally; do not misjudge it as frozen.
- Only consider triggering retry if the status remains unchanged for a long time or output stops without a final result.

## 📊 Data Output
Upon successful execution, the script retrieves a JSON object containing a `files` array with a download link to a CSV file. The CSV includes the following structured profile data:
- `Platform name`: The social media platform (e.g., LinkedIn, Twitter).
- `Followers count`: The number of followers.
- `Page title`: The title of the profile page.
- `Description snippet`: The bio or description snippet.
- `Profile URL`: The direct link to the social media profile.

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
1. **Background Research**: Find social media profiles of job candidates or new connections.
2. **Lead Generation**: Gather contact information and social profiles for sales prospects.
3. **Competitive Intelligence**: Discover the social media footprint of competitors.
4. **Influencer Discovery**: Locate content creators across various platforms.
5. **Brand Monitoring**: Check a brand's presence across different social networks.
6. **Reconnecting**: Find old friends or colleagues online.
7. **Identity Verification**: Cross-reference profiles of people met online.
8. **Customer Support**: Find official brand accounts for reaching out.
9. **Networking**: Research event attendees or potential business partners.
10. **Digital Footprint Audit**: Monitor one's own public social media presence.
