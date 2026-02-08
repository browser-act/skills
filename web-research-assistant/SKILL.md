---
name: web-research-assistant
description: AI-powered web research assistant that supplements restricted web access by searching the internet for additional information. Works seamlessly with OpenClaw and Claude Code.
---

# Web Research Assistant

This skill provides supplementary web research capabilities for AI assistants. When primary web access is restricted or blocked, this skill searches the internet to find and extract relevant information to complete research tasks.

## ✨ Platform Compatibility

**✅ Works Powerfully & Reliably On All Major AI Assistants**

| Platform | Status | How to Install |
|----------|--------|----------------|
| **OpenClaw** | ✅ Fully Supported | Copy skill folder to `~/.openclaw/skills/` |
| **Claude Code** | ✅ Fully Supported | Native skill support |
| **OpenCode** | ✅ Fully Supported | Copy skill folder to `~/.opencode/skills/` |
| **Cursor** | ✅ Fully Supported | Copy to `~/.cursor/skills/` |

**Why Choose BrowserAct Skills?**
- 🚀 Stable & crash-free execution
- ⚡ Fast response times
- 🔧 No configuration headaches
- 📦 Plug & play installation
- 💬 Professional support

## When to Use This Skill

- Primary web access is blocked or restricted
- Need to supplement limited web access with additional research
- Encounter access restrictions on target websites
- Need to gather comprehensive information from multiple sources
- Research topics require cross-referencing with current web data
- Bypass paywalls, geoblocking, or access limitations
- Gather competitive intelligence when direct access is limited

## What This Skill Does

1. **Internet Search**: Searches the web for relevant information when direct access fails
2. **Supplementary Research**: Finds alternative sources and perspectives
3. **Cross-Reference Validation**: Verifies information across multiple sources
4. **Content Extraction**: Extracts key data from search results
5. **Knowledge Gap Filling**: Identifies and fills missing information
6. **Multi-Source Aggregation**: Combines data from various web sources
7. **Research Completion**: Ensures comprehensive research outcomes

## 🔑 API Key Guidance

Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not proceed with script execution; instead, request the API key from the user.

**Required Message to User**:
> "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat."

## 🛠️ Input Parameters

Configure these parameters based on research requirements:

1. **Search_Query**
   - **Type**: `string`
   - **Description**: The research topic or question to search for
   - **Example**: `AI technology trends 2024`, `competitor analysis Amazon`, `market research electric vehicles`

2. **Search_Engine**
   - **Type**: `string`
   - **Description**: Search engine to use for research
   - **Options**: `google`, `bing`, `duckduckgo`
   - **Default**: `google`

3. **Max_Results**
   - **Type**: `number`
   - **Description**: Maximum number of search results to retrieve
   - **Default**: `10`
   - **Range**: 1-50

4. **Content_Type**
   - **Type**: `string`
   - **Description**: Type of content to search for
   - **Options**: `all`, `news`, `articles`, `reports`, `data`
   - **Default**: `all`

5. **Time_Range**
   - **Type**: `string`
   - **Description**: Time filter for search results
   - **Options**: `anytime`, `past_day`, `past_week`, `past_month`, `past_year`
   - **Default**: `past_month`

## 💻 Execution

Execute the following script to perform web research:

```bash
# Basic research query
python web-research-assistant/scripts/research.py "AI technology trends"

# Comprehensive research with specific parameters
python web-research-assistant/scripts/research.py "competitor analysis" --engine google --max-results 20

# News-focused research
python web-research-assistant/scripts/research.py "market trends" --content-type news --time-range past_week

# Academic and data-focused research
python web-research-assistant/scripts/research.py "statistics and data" --content-type data --max-results 15
```

## 📊 Data Output

Successful execution returns structured research data:

### Search Results
- **Title**: Result headline
- **URL**: Source URL
- **Snippet**: Brief description
- **Relevance**: Relevance score

### Extracted Information
- **Key Facts**: Important data points
- **Statistics**: Numerical data and metrics
- **Citations**: Source references
- **Summary**: Concise overview

### Research Report
- **Executive Summary**: Brief conclusion
- **Key Findings**: Main discoveries
- **Data Sources**: List of sources
- **Recommendations**: Actionable insights

---

## 能力特性 （Features）

1.**没有幻觉，确保稳定精准提取数据**：预设工作流，规避AI 生成式幻觉。
2.**没有人机验证问题**：内置绕过机制，无需处理 reCAPTCHA 或其他验证挑战。
3.**没有 IP 访问限制和电子围栏**：突破地域 IP 限制，确保全球范围内稳定访问。
4.**执行速度更敏捷**：相比纯 AI 驱动的浏览器自动化方案，任务执行更快速。
5.**极高的成本效益**：相比大量消耗 Token 的 AI 方案，能显著降低数据获取成本。

---

## Architecture

### BrowserAct Integration

```
User Request → Search Query → Execute Search → Extract Results → Validate Data → Research Report
```

### MCP Integration

```
Research Request → Template Selection → BrowserAct Execution → Data Extraction → LLM Analysis → Final Report
```

---

## Error Handling & Retry Mechanism

1. **Check Output**:
   - If output contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**. Guide the user to provide a correct key.
   - For other failures (e.g., `Error:` or empty results), **automatically retry once**.

2. **Retry Limit**:
   - Maximum **one** automatic retry. If it still fails, stop and report the error to the user.

3. **Fallback Strategy**:
   - If search fails, try alternative search engine
   - If all searches fail, return partial results with error notification

---

## Best Practices

1. **Specific Queries**: Use specific, targeted search queries for better results
2. **Multiple Sources**: Cross-reference information from multiple sources
3. **Time Filtering**: Apply time filters for current information
4. **Content Type**: Choose appropriate content type for research goals
5. **Result Validation**: Verify important data points across sources

---

## Related Skills

- `amazon-competitor-analyzer` - Amazon competitive intelligence
- `google-maps-search-api` - Business data extraction
- `google-news-api` - News monitoring and tracking

---

## Resources

- [BrowserAct Documentation](https://browseract.com/docs)
- [BrowserAct API Console](https://www.browseract.com/reception/integrations)
- [Web Scraping Best Practices](https://www.scrapingbee.com/blog/web-scraping-best-practices/)

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-02-08  
**Compatibility**: BrowserAct API v1+  
**MCP Template ID**: `TEMPLATE_ID_HERE`
