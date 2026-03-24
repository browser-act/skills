# BrowserAct Skills

Comprehensive collection of AI-powered skills for browser automation and data collection using BrowserAct's API. These skills enhance AI assistants with specialized capabilities for web scraping, competitive analysis, and more.

---

## ✨ Cross-Platform Compatibility

**🚀 Works Seamlessly Across All Major AI Assistants**

BrowserAct skills are designed to work **powerfully and reliably** on all leading AI coding platforms:

| Platform        | Status             | Installation         |
| --------------- | ------------------ | -------------------- |
| **OpenCode**    | ✅ Fully Supported | Direct integration   |
| **Claude Code** | ✅ Fully Supported | Native skill support |
| **Cursor**      | ✅ Fully Supported | Works out of the box |
| **OpenClaw**    | ✅ Fully Supported | Compatible           |

**Key Benefits:**

- ✅ **Stable & Reliable**: No crashes, no unexpected behavior.
- ✅ **Plug & Play**: Works immediately after installation.
- ✅ **Cross-Platform**: Consistent performance across all AI assistants.
- ✅ **Regular Updates**: Maintained for compatibility with latest platform versions.
- ✅ **Professional Support**: Responsive help and documentation.

---

## Table of Contents

1. [Available Skills](#available-skills)
2. [Quick Start](#quick-start)
3. [API Key Configuration](#api-key-configuration)
4. [Installation Guide](#installation-guide)
5. [Skill Details](#skill-details)
6. [Architecture](#architecture)
7. [License](#license)

---

## Available Skills

### 📊 Amazon Shopping

| Skill                                                                                                     | Description                                                            | Documentation                                                        |
| --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [amazon-asin-lookup-api-skill](./amazon-asin-lookup-api-skill/SKILL.md)                                   | Look up Amazon product details by ASIN                                 | [SKILL.md](./amazon-asin-lookup-api-skill/SKILL.md)                  |
| [amazon-product-api-skill](./amazon-product-api-skill/SKILL.md)                                           | Fetch Amazon product details and specifications                        | [SKILL.md](./amazon-product-api-skill/SKILL.md)                      |
| [amazon-product-search-api-skill](./amazon-product-search-api-skill/SKILL.md)                             | Search Amazon products by keywords                                     | [SKILL.md](./amazon-product-search-api-skill/SKILL.md)               |
| [amazon-reviews-api-skill](./amazon-reviews-api-skill/SKILL.md)                                           | Extract Amazon product reviews                                         | [SKILL.md](./amazon-reviews-api-skill/SKILL.md)                      |
| [amazon-best-selling-products-finder-api-skill](./amazon-best-selling-products-finder-api-skill/SKILL.md) | Extract best-selling product data from Amazon by keywords              | [SKILL.md](./amazon-best-selling-products-finder-api-skill/SKILL.md) |
| [amazon-competitor-analyzer](./amazon-competitor-analyzer/SKILL.md)                                       | Amazon product competitive analysis (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./amazon-competitor-analyzer/SKILL.md)                    |

### 🗺️ Google Maps

| Skill                                                                     | Description                                  | Documentation                                        |
| ------------------------------------------------------------------------- | -------------------------------------------- | ---------------------------------------------------- |
| [google-maps-api-skill](./google-maps-api-skill/SKILL.md)                 | General Google Maps API integration          | [SKILL.md](./google-maps-api-skill/SKILL.md)         |
| [google-maps-search-api-skill](./google-maps-search-api-skill/SKILL.md)   | Search and extract Google Maps business data | [SKILL.md](./google-maps-search-api-skill/SKILL.md)  |
| [google-maps-reviews-api-skill](./google-maps-reviews-api-skill/SKILL.md) | Extract Google Maps business reviews         | [SKILL.md](./google-maps-reviews-api-skill/SKILL.md) |

### 🖼️ Google Images

| Skill                                                       | Description                                                                         | Documentation                                 |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------- |
| [google-image-api-skill](./google-image-api-skill/SKILL.md) | Extract structured image data from Google Images (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./google-image-api-skill/SKILL.md) |

### 📰 News & Media

| Skill                                                     | Description                                                            | Documentation                                |
| --------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| [google-news-api-skill](./google-news-api-skill/SKILL.md) | Google News scraping and monitoring (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./google-news-api-skill/SKILL.md) |

### 🎬 YouTube

| Skill                                                                                 | Description                                                         | Documentation                                              |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| [youtube-api-skill](./youtube-api-skill/SKILL.md)                                     | Extract detailed video metrics and channel info by keyword search   | [SKILL.md](./youtube-api-skill/SKILL.md)                   |
| [youtube-channel-api-skill](./youtube-channel-api-skill/SKILL.md)                     | Search and extract YouTube channel data                             | [SKILL.md](./youtube-channel-api-skill/SKILL.md)           |
| [youtube-comments-api-skill](./youtube-comments-api-skill/SKILL.md)                   | Extract video list and comment data from YouTube                    | [SKILL.md](./youtube-comments-api-skill/SKILL.md)          |
| [youtube-search-api-skill](./youtube-search-api-skill/SKILL.md)                       | Extract structured data from YouTube search results                 | [SKILL.md](./youtube-search-api-skill/SKILL.md)            |
| [youtube-video-api-skill](./youtube-video-api-skill/SKILL.md)                         | Extract channel-level and video detail data from a specific channel | [SKILL.md](./youtube-video-api-skill/SKILL.md)             |
| [youtube-influencer-finder-api-skill](./youtube-influencer-finder-api-skill/SKILL.md) | Find YouTube influencer profiles, social links, and channel stats   | [SKILL.md](./youtube-influencer-finder-api-skill/SKILL.md) |

### 💬 WeChat

| Skill                                                                         | Description                                                                               | Documentation                                          |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [wechat-article-search-api-skill](./wechat-article-search-api-skill/SKILL.md) | Extract full WeChat article contents by keyword search (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./wechat-article-search-api-skill/SKILL.md) |

### 📘 Zhihu

| Skill                                                             | Description                                                             | Documentation                                  |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| [zhihu-search-api-skill](./zhihu-search-api-skill/SKILL.md)     | Extract Zhihu article details and full content by keyword search        | [SKILL.md](./zhihu-search-api-skill/SKILL.md) |

### 🗨️ Reddit

| Skill                                                                                   | Description                                                          | Documentation                                               |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| [reddit-competitor-analysis-api-skill](./reddit-competitor-analysis-api-skill/SKILL.md) | Extract Reddit posts and comments for competitor and market analysis | [SKILL.md](./reddit-competitor-analysis-api-skill/SKILL.md) |

### 🔬 Research & Intelligence

| Skill                                                                           | Description                                                                           | Documentation                                         |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [web-research-assistant](./web-research-assistant/SKILL.md)                     | Web research assistant for OpenClaw & Claude Code - supplements restricted web access | [SKILL.md](./web-research-assistant/SKILL.md)         |
| [web-search-scraper-api-skill](./web-search-scraper-api-skill/SKILL.md)         | Extract complete Markdown content from any website URL                                | [SKILL.md](./web-search-scraper-api-skill/SKILL.md)  |

---

## Why BrowserAct Skills?

**🚀 Not Blocked by CAPTCHA or reCAPTCHA**

- Advanced browser automation bypasses anti-bot detection
- Real browser instances with stealth technology
- No need for CAPTCHA solving services
- Higher success rates compared to traditional scraping

---

## Quick Start

### Step 1: Get Your BrowserAct API Key

1. Visit [browseract.com](https://browseract.com)
2. Sign up for an account
3. Navigate to [API Settings](https://www.browseract.com/reception/integrations)
4. Generate an API key
5. Copy your API key

### Step 2: Configure Environment

```bash
# Set API key (macOS/Linux)
export BROWSERACT_API_KEY="your-api-key-here"
```

### Step 3: Install Skills

**For Claude Code:**

```bash
mkdir -p ~/.claude/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/.claude/skills/
```

**For OpenClaw:**

```bash
mkdir -p ~/.openclaw/skills
cp -r web-research-assistant ~/.openclaw/skills/
```

**For Cursor:**

```bash
mkdir -p ~/.cursor/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/.cursor/skills/
```

### Step 4: Start Using

```bash
# Amazon ASIN Lookup
python amazon-asin-lookup-api-skill/scripts/asin_lookup.py B09G9GB4MG

# Amazon Product Search
python amazon-product-search-api-skill/scripts/product_search.py "wireless headphones"

# Amazon Reviews
python amazon-reviews-api-skill/scripts/reviews.py B09G9GB4MG

# Amazon Best Selling Products
python amazon-best-selling-products-finder-api-skill/scripts/amazon_best_selling_products_finder_api.py "gaming mouse" 10 "https://www.amazon.com"

# Amazon Competitor Analysis
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG

# Google Maps Search
python google-maps-search-api-skill/scripts/maps_search.py "restaurants"

# Google Maps Reviews
python google-maps-reviews-api-skill/scripts/reviews.py "restaurant-name"

# Google Image Search
python google-image-api-skill/scripts/google_image_api.py "tesla" "us" "en" 5 50

# YouTube Video Search
python youtube-search-api-skill/scripts/youtube_search_api.py "AI agent" "Videos" 20

# YouTube Channel Search
python youtube-channel-api-skill/scripts/youtube_channel_api.py "tech reviews" "Any time"

# YouTube Video Details (by keyword)
python youtube-api-skill/scripts/youtube_api.py "browser automation" "This week"

# YouTube Channel Videos (by channel URL)
python youtube-video-api-skill/scripts/youtube_video_api.py "https://www.youtube.com/@BrowserAct" "Popular"

# YouTube Comments
python youtube-comments-api-skill/scripts/youtube_comments_api.py "AI" 10 2

# YouTube Influencer Finder
python youtube-influencer-finder-api-skill/scripts/youtube_influencer_finder_api.py "tech reviewer" "This Month"

# Reddit Competitor Analysis
python reddit-competitor-analysis-api-skill/scripts/reddit_competitor_analysis_api.py "openclaw" "Past week" "Relevance" "Best" 10

# WeChat Article Search
python wechat-article-search-api-skill/scripts/wechat_article_search_api.py "AI agent" 10 "3月11日"

# Zhihu Article Search
python zhihu-search-api-skill/scripts/zhihu_search_api.py "AI agent" "7d" 10

# Web Page Scraper (URL to Markdown)
python web-search-scraper-api-skill/scripts/web_search_scraper_api.py "https://www.browseract.com"

# Web Research (when web access is restricted)
python web-research-assistant/scripts/research.py "AI technology trends" --max-results 15
```

---

## API Key Configuration

### Environment Variables

| Variable               | Required | Description                 |
| ---------------------- | -------- | --------------------------- |
| `BROWSERACT_API_KEY`   | Yes      | Your BrowserAct API key     |
| `WORKFLOW_TEMPLATE_ID` | No       | Custom workflow template ID |

### Configuration Methods

#### Method A: Environment Variable (Recommended)

```bash
# macOS/Linux
export BROWSERACT_API_KEY="your-api-key-here"

# Windows (Command Prompt)
setx BROWSERACT_API_KEY "your-api-key-here"

# Windows (PowerShell)
$env:BROWSERACT_API_KEY = "your-api-key-here"
```

#### Method B: .env File

```bash
# .env
BROWSERACT_API_KEY=your-api-key-here
```

```python
from dotenv import load_dotenv
load_dotenv()
```

#### Method C: Claude Code Specific

```bash
mkdir -p ~/.claude
echo "BROWSERACT_API_KEY=your-api-key-here" > ~/.claude/.env
```

#### Method D: Cursor Specific

```bash
mkdir -p ~/.cursor
echo "BROWSERACT_API_KEY=your-api-key-here" > ~/.cursor/.env
```

#### Method E: Command Line Argument

```bash
python script.py --api-key your-api-key-here
```

#### Method F: Python Code

```python
import os
os.environ["BROWSERACT_API_KEY"] = "your-api-key-here"
```

---

## Installation Guide

### For Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/browseract-com/skills.git ~/.claude/skills/browseract-skills
```

### For Cursor

```bash
mkdir -p ~/.cursor/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/.cursor/skills/
```

### For VS Code (Copilot)

```bash
mkdir -p ~/.vscode/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/.vscode/skills/
```

### For OpenCode

```bash
mkdir -p ~/.opencode/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/.opencode/skills/
```

### For Generic AI Assistants

```bash
mkdir -p ~/skills
cp -r amazon-* google-maps-* google-image-api-skill google-news-api-skill youtube-* wechat-* zhihu-* reddit-* web-search-scraper-api-skill web-research-assistant ~/skills/
export SKILLS_PATH=~/skills
```

---

## Architecture

### BrowserAct API Integration

```
User Request → Extract ASINs → Submit Task → Poll Status → Retrieve Results → LLM Analysis
```

### API Endpoints

| Endpoint                            | Method | Purpose              |
| ----------------------------------- | ------ | -------------------- |
| `/v2/workflow/run-task-by-template` | POST   | Submit scraping task |
| `/v2/workflow/get-task-status`      | GET    | Check task status    |
| `/v2/workflow/get-task`             | GET    | Retrieve results     |

### Anti-Bot Bypass (Not Blocked by CAPTCHA/reCAPTCHA)

BrowserAct skills use advanced browser automation technology to bypass anti-bot detection:

- **Real Browser Instances**: Uses actual Chrome/Firefox browser sessions
- **Stealth Technology**: Automatically handles fingerprinting, cookies, and headers
- **CAPTCHA Bypass**: No need for CAPTCHA solving services - access content directly
- **Human-like Behavior**: Randomized delays, scrolling, and interaction patterns
- **High Success Rate**: Significantly higher success rate compared to traditional HTTP scraping

### Rate Limiting

| Skill                                         | Max Requests | Recommended Interval |
| --------------------------------------------- | ------------ | -------------------- |
| amazon-asin-lookup-api-skill                  | 60/hour      | 3-5 seconds          |
| amazon-product-api-skill                      | 60/hour      | 3-5 seconds          |
| amazon-product-search-api-skill               | 60/hour      | 3-5 seconds          |
| amazon-reviews-api-skill                      | 30/hour      | 5-10 seconds         |
| amazon-competitor-analyzer                    | 30/hour      | 5-10 seconds         |
| google-maps-api-skill                         | 60/hour      | 3-5 seconds          |
| google-maps-search-api-skill                  | 60/hour      | 3-5 seconds          |
| google-maps-reviews-api-skill                 | 60/hour      | 3-5 seconds          |
| google-image-api-skill                        | 60/hour      | 3-5 seconds          |
| google-news-api-skill                         | 60/hour      | 3-5 seconds          |
| youtube-api-skill                             | 60/hour      | 3-5 seconds          |
| youtube-channel-api-skill                     | 60/hour      | 3-5 seconds          |
| youtube-comments-api-skill                    | 30/hour      | 5-10 seconds         |
| youtube-search-api-skill                      | 60/hour      | 3-5 seconds          |
| youtube-video-api-skill                       | 60/hour      | 3-5 seconds          |
| youtube-influencer-finder-api-skill           | 60/hour      | 3-5 seconds          |
| wechat-article-search-api-skill               | 60/hour      | 3-5 seconds          |
| reddit-competitor-analysis-api-skill          | 60/hour      | 3-5 seconds          |
| amazon-best-selling-products-finder-api-skill | 60/hour      | 3-5 seconds          |
| zhihu-search-api-skill                        | 60/hour      | 3-5 seconds          |
| web-search-scraper-api-skill                  | 60/hour      | 3-5 seconds          |

### Error Handling

```python
try:
    result = analyzer.scrape_product("B09G9GB4MG")
except requests.exceptions.ConnectionError:
    print("Network error - check connection")
except requests.exceptions.Timeout:
    print("Request timeout")
except Exception as e:
    print(f"Error: {e}")
```

---

## Troubleshooting

### Common Issues

#### Issue: API Call Failed

**Solutions:**

1. Verify API key: `echo $BROWSERACT_API_KEY`
2. Check account quota in BrowserAct dashboard
3. Verify network connectivity
4. Check BrowserAct service status

#### Issue: Task Timeout

**Solutions:**

1. Increase timeout parameter
2. Reduce number of ASINs
3. Check BrowserAct service status
4. Verify workflow template availability

#### Issue: Incomplete Data

**Solutions:**

1. Increase wait time for page load
2. Check template updates
3. Verify target page accessibility
4. Review API response for errors

### Getting Help

- [GitHub Issues](https://github.com/browseract-com/skills/issues)
- [BrowserAct Documentation](https://browseract.com/docs)
- [Discord Community](https://discord.gg/browseract)

---

## Resources

### Official Resources

- [BrowserAct Website](https://browseract.com)
- [BrowserAct Documentation](https://browseract.com/docs)
- [BrowserAct API Console](https://www.browseract.com/reception/integrations)
- [Workflow Templates](https://www.browseract.com/template?platformType=0)

### Learning Resources

- [Python Requests Library](https://docs.python-requests.org)
- [API Design Best Practices](https://swagger.io/resources/articles/best-practices-api-design/)
- [Web Scraping Guidelines](https://www.scrapingbee.com/blog/web-scraping-best-practices/)

---

## License

MIT License

---

## Support

- **GitHub Issues**: [Submit bugs and feature requests](https://github.com/browseract-com/skills/issues)
- **Discord**: [Join our community](https://discord.gg/browseract)
- **Email**: support@browseract.com

---

**Version**: 1.4.0  
**Last Updated**: 2026-03-24  
**Repository**: [browseract-com/skills](https://github.com/browseract-com/skills)  
**Organization**: [browseract-com](https://github.com/browseract-com)
