---
name: github-project-contributor-finder-api-skill
description: "This skill helps users extract GitHub repository project details and contributor contact information using keywords, stars, and update dates. Agent should proactively apply this skill when users express needs like search for GitHub projects by keywords, find top open-source contributors in specific domains, extract developer contacts from GitHub repositories, discover trending repositories with high stars, gather contributor profiles and social links for tech recruiting, retrieve GitHub project descriptions and metrics, build developer communities by finding active contributors, search for repositories updated recently, collect personal website and Twitter links of developers, generate targeted leads for developer tools, or track active open-source contributors for collaboration."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# GitHub Project & Contributor Finder API Skill

## 📖 Brief
This skill utilizes BrowserAct's GitHub Project & Contributor Finder API to extract project details and contributor contact information from GitHub. Simply provide keywords, minimum stars, and an update date filter — BrowserAct traverses the search results, extracts repository metrics, and fetches detailed contributor profiles, returning it all directly via API without building crawler scripts or dealing with rate limits.

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
The agent should flexibly configure the following parameters based on user requirements:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Keywords for searching repositories.
   - **Example**: `browser automation`, `react framework`, `machine learning`
   - **Default**: `browser automation`

2. **stars**
   - **Type**: `number`
   - **Description**: Minimum number of stars the repository should have.
   - **Example**: `100`, `1000`
   - **Default**: `100`

3. **updated**
   - **Type**: `string`
   - **Description**: Filter repositories by the date they were last updated (format: `YYYY-MM-DD`).
   - **Example**: `2026-01-01`, `2025-06-01`
   - **Default**: `2026-01-01`

4. **Page_Turns**
   - **Type**: `number`
   - **Description**: Number of search result pages to paginate through. For example, if there are 39 pages and you want the first 2, input `2`.
   - **Example**: `1`, `2`
   - **Default**: `1`

5. **date_limit_per_page**
   - **Type**: `number`
   - **Description**: Number of data items to extract per page in the search results list.
   - **Example**: `5`, `10`
   - **Default**: `5`

## 🚀 Invocation Method
Agent should execute the following command to invoke the skill:

```bash
# Example invocation (all parameters)
python -u ./scripts/github_project_contributor_finder_api.py "browser automation" 100 "2026-01-01" 1 5

# Minimal invocation (only keywords, others use defaults)
python -u ./scripts/github_project_contributor_finder_api.py "react framework"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take several minutes. The script outputs **timestamped status logs** continuously (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- Monitor the terminal output while waiting.
- As long as new status logs appear, the task is running normally; do not misjudge it as frozen.
- Only consider triggering retry if the status remains unchanged for a long time or output stops without a final result.

## 📊 Data Output
Upon successful execution, the script parses and prints the structured results from the API response.

**Project Fields**:
- `repository_name`: The name of the GitHub repository.
- `repository_url`: The URL link to the repository.
- `repository_owner_name`: The owner/creator of the repository.
- `repository_description`: A brief description of the repository.
- `star_count`: The number of stars the repository has received.

**Contributor Fields**:
- `user_name`: The GitHub username of the contributor.
- `profile_url`: The URL link to the contributor's profile.
- `bio`: The bio or short description of the contributor.
- `repositories_summary`: A summary of other repositories owned by the contributor.
- `personal_website`: The contributor's personal website link.
- `twitter`: The contributor's Twitter handle.

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
1. **Tech Recruiting**: Gather contributor profiles and social links from popular repositories to build candidate pipelines.
2. **Open-Source Discovery**: Search for trending repositories by keywords and star count to find valuable projects.
3. **Developer Outreach**: Collect personal websites and Twitter handles of active contributors for developer tool marketing.
4. **Community Building**: Identify and connect with active open-source contributors in specific domains.
5. **Competitor Analysis**: Monitor which developers contribute to competing projects.
6. **Partnership Scouting**: Find repository owners for potential collaboration or sponsorship.
7. **Market Research**: Analyze repository metrics and descriptions to understand technology trends.
8. **Lead Generation**: Generate targeted leads for developer tools by finding projects with relevant tech stacks.
9. **Academic Research**: Discover recently updated repositories in specific research areas.
10. **Talent Mapping**: Build a database of skilled developers based on their GitHub contributions and profiles.
