# BrowserAct Skills

Comprehensive collection of AI-powered skills for browser automation and data collection using BrowserAct's API. These skills enhance AI assistants with specialized capabilities for web scraping, competitive analysis, and more.

---

## ✨ Cross-Platform Compatibility

**🚀 Works Seamlessly Across All Major AI Assistants**

BrowserAct skills are designed to work **powerfully and reliably** on all leading AI coding platforms:

| Platform | Status | Installation |
|----------|--------|--------------|
| **OpenCode** | ✅ Fully Supported | Direct integration |
| **Claude Code** | ✅ Fully Supported | Native skill support |
| **Cursor** | ✅ Fully Supported | Works out of the box |
| **OpenClaw** | ✅ Fully Supported | Compatible |

**Key Benefits:**
- ✅ **Stable & Reliable**: No crashes, no unexpected behavior
- ✅ **Plug & Play**: Works immediately after installation
- ✅ **Cross-Platform**: Consistent performance across all AI assistants
- ✅ **Regular Updates**: Maintained for compatibility with latest platform versions
- ✅ **Professional Support**: Responsive help and documentation

---

## Table of Contents

1. [Available Skills](#available-skills)
2. [Quick Start](#quick-start)
3. [API Key Configuration](#api-key-configuration)
4. [Installation Guide](#installation-guide)
5. [Skill Details](#skill-details)
6. [Architecture](#architecture)
7. [Contributing](#contributing)
8. [License](#license)

---

## Available Skills

### 📊 Amazon Shopping

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [amazon-asin-lookup-api-skill](./amazon-asin-lookup-api-skill/SKILL.md) | Look up Amazon product details by ASIN | [SKILL.md](./amazon-asin-lookup-api-skill/SKILL.md) |
| [amazon-product-api-skill](./amazon-product-api-skill/SKILL.md) | Fetch Amazon product details and specifications | [SKILL.md](./amazon-product-api-skill/SKILL.md) |
| [amazon-product-search-api-skill](./amazon-product-search-api-skill/SKILL.md) | Search Amazon products by keywords | [SKILL.md](./amazon-product-search-api-skill/SKILL.md) |
| [amazon-reviews-api-skill](./amazon-reviews-api-skill/SKILL.md) | Extract Amazon product reviews | [SKILL.md](./amazon-reviews-api-skill/SKILL.md) |
| [amazon-competitor-analyzer](./amazon-competitor-analyzer/SKILL.md) | Amazon product competitive analysis (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./amazon-competitor-analyzer/SKILL.md) |

### 🗺️ Google Maps

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [google-maps-api-skill](./google-maps-api-skill/SKILL.md) | General Google Maps API integration | [SKILL.md](./google-maps-api-skill/SKILL.md) |
| [google-maps-search-api-skill](./google-maps-search-api-skill/SKILL.md) | Search and extract Google Maps business data | [SKILL.md](./google-maps-search-api-skill/SKILL.md) |
| [google-maps-reviews-api-skill](./google-maps-reviews-api-skill/SKILL.md) | Extract Google Maps business reviews | [SKILL.md](./google-maps-reviews-api-skill/SKILL.md) |

### 📰 News & Media

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [google-news-api-skill](./google-news-api-skill/SKILL.md) | Google News scraping and monitoring (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./google-news-api-skill/SKILL.md) |

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
cp -r amazon-* google-maps-* google-news-api-skill ~/.claude/skills/
```

**For Cursor:**
```bash
mkdir -p ~/.cursor/skills
cp -r amazon-* google-maps-* google-news-api-skill ~/.cursor/skills/
```

### Step 4: Start Using

```bash
# Amazon ASIN Lookup
python amazon-asin-lookup-api-skill/scripts/asin_lookup.py B09G9GB4MG

# Amazon Product Search
python amazon-product-search-api-skill/scripts/product_search.py "wireless headphones"

# Amazon Reviews
python amazon-reviews-api-skill/scripts/reviews.py B09G9GB4MG

# Amazon Competitor Analysis
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG

# Google Maps Search
python google-maps-search-api-skill/scripts/maps_search.py "restaurants"

# Google Maps Reviews
python google-maps-reviews-api-skill/scripts/reviews.py "restaurant-name"

# Google News
python google-news-api-skill/scripts/google_news.py "AI technology" "past week" 30
```

---

## API Key Configuration

### Environment Variables

| Variable | Required | Description |
|----------|-----------|-------------|
| `BROWSERACT_API_KEY` | Yes | Your BrowserAct API key |
| `WORKFLOW_TEMPLATE_ID` | No | Custom workflow template ID |

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
cp -r amazon-* google-maps-* google-news-api-skill 【ZH】comprehensive-seo-analyzer ~/.cursor/skills/
```

### For VS Code (Copilot)

```bash
mkdir -p ~/.vscode/skills
cp -r amazon-* google-maps-* google-news-api-skill ~/.vscode/skills/
```

### For OpenCode

```bash
mkdir -p ~/.opencode/skills
cp -r amazon-* google-maps-* google-news-api-skill ~/.opencode/skills/
```

### For Generic AI Assistants

```bash
mkdir -p ~/skills
cp -r amazon-* google-maps-* google-news-api-skill ~/skills/
export SKILLS_PATH=~/skills
```

---

## Skill Details

Click on any skill above to view its detailed documentation in the SKILL.md file.

### 📊 Amazon Shopping Skills

| Skill | Template ID |
|-------|-------------|
| amazon-asin-lookup-api-skill | [View SKILL.md](./amazon-asin-lookup-api-skill/SKILL.md) |
| amazon-product-api-skill | [View SKILL.md](./amazon-product-api-skill/SKILL.md) |
| amazon-product-search-api-skill | [View SKILL.md](./amazon-product-search-api-skill/SKILL.md) |
| amazon-reviews-api-skill | [View SKILL.md](./amazon-reviews-api-skill/SKILL.md) |
| amazon-competitor-analyzer | [View SKILL.md](./amazon-competitor-analyzer/SKILL.md) |

### 🗺️ Google Maps Skills

| Skill | Template ID |
|-------|-------------|
| google-maps-api-skill | [View SKILL.md](./google-maps-api-skill/SKILL.md) |
| google-maps-search-api-skill | [View SKILL.md](./google-maps-search-api-skill/SKILL.md) |
| google-maps-reviews-api-skill | [View SKILL.md](./google-maps-reviews-api-skill/SKILL.md) |

### 📰 News & Media

| Skill | Template ID |
|-------|-------------|
| google-news-api-skill | [View SKILL.md](./google-news-api-skill/SKILL.md) |

---

## Rate Limiting

**Features:**
- Keyword-based news search
- Time range filtering (past hour, 24 hours, week, year)
- Batch extraction (up to 100+ articles)
- Multi-language support (15+ languages)
- Author and source information extraction
- Real-time news monitoring
- Structured data output (JSON)

**Quick Start:**

```bash
# Get latest news on a topic
python google-news-api/scripts/google_news_api.py "AI technology" "past week" 30

# Breaking news (past 24 hours)
python google-news-api/scripts/google_news_api.py "Tesla" "past 24 hours" 20

# Long-term research (past year)
python google-news-api/scripts/google_news_api.py "climate change" "past year" 100
```

**Parameters:**
| Parameter | Type | Default | Description |
|----------|------|---------|-------------|
| keywords | string | - | Search keywords or topic |
| publish_date | string | past week | Time range (past hours, past 24 hours, past week, past year, any time) |
| datelimit | number | 30 | Maximum articles to extract |

**Documentation:**
- [SKILL.md](./google-news-api/SKILL.md)

**Workflow Template ID:** `77638424152140851`

**Output Data:**
- Headline/Title
- Source publisher
- Article URL
- Published time
- Author name
- Full article content

---


## Architecture

### BrowserAct API Integration

```
User Request → Extract ASINs → Submit Task → Poll Status → Retrieve Results → LLM Analysis
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v2/workflow/run-task-by-template` | POST | Submit scraping task |
| `/v2/workflow/get-task-status` | GET | Check task status |
| `/v2/workflow/get-task` | GET | Retrieve results |

### Anti-Bot Bypass (Not Blocked by CAPTCHA/reCAPTCHA)

BrowserAct skills use advanced browser automation technology to bypass anti-bot detection:

- **Real Browser Instances**: Uses actual Chrome/Firefox browser sessions
- **Stealth Technology**: Automatically handles fingerprinting, cookies, and headers
- **CAPTCHA Bypass**: No need for CAPTCHA solving services - access content directly
- **Human-like Behavior**: Randomized delays, scrolling, and interaction patterns
- **High Success Rate**: Significantly higher success rate compared to traditional HTTP scraping

### Rate Limiting

| Skill | Max Requests | Recommended Interval |
|-------|-------------|---------------------|
| amazon-competitor-analyzer | 30/hour | 5-10 seconds |
| google-maps-search-api | 60/hour | 3-5 seconds |
| google-news-api | 60/hour | 3-5 seconds |

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

## Contributing

### Adding New Skills

1. Create a new directory for your skill
2. Add `SKILL.md` with full documentation
3. Add implementation files
4. Update this README
5. Submit via Pull Request

### Skill Structure

```
skill-name/
├── README.md
├── SKILL.md
└── implementation.py
```

**Current Skills:**
- amazon-asin-lookup-api-skill
- amazon-product-api-skill
- amazon-product-search-api-skill
- amazon-reviews-api-skill
- amazon-competitor-analyzer
- google-maps-api-skill
- google-maps-search-api-skill
- google-maps-reviews-api-skill
- google-news-api-skill

### Documentation Requirements

All skills must include:

- YAML frontmatter with name and description
- Input parameters documentation
- Output format specification
- Usage examples
- API key setup instructions
- Troubleshooting section

---

## Resources

### Official Resources

- [BrowserAct Website](https://browseract.com)
- [BrowserAct Documentation](https://browseract.com/docs)
- [BrowserAct API Console](https://www.browseract.com/reception/integrations)
- [Workflow Templates](https://www.browseract.com/template?platformType=0)

### Related Repositories

- [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) - SEO and GEO skills

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

**Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Repository**: [browseract-com/skills](https://github.com/browseract-com/skills)  
**Organization**: [browseract-com](https://github.com/browseract-com)
