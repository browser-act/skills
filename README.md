# BrowserAct Skills

Comprehensive collection of AI-powered skills for browser automation and data collection using BrowserAct's API. These skills enhance AI assistants with specialized capabilities for web scraping, competitive analysis, and more.

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

### 📊 Competitive Intelligence

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [amazon-competitor-analyzer](./amazon-competitor-analyzer/SKILL.md) | Amazon product competitive analysis (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./amazon-competitor-analyzer/SKILL.md) |

### 🗺️ Local Business Data

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [google-maps-search-api](./google-maps-search-api/SKILL.md) | Google Maps business data extraction (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./google-maps-search-api/SKILL.md) |

### 📰 News & Media

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [google-news-api](./google-news-api/SKILL.md) | Google News scraping and monitoring (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./google-news-api/SKILL.md) |

### 💼 Professional Networks

| Skill | Description | Documentation |
|-------|-------------|---------------|
| [linkedin-scraper](./linkedin-scraper/SKILL.md) | LinkedIn profile, company, and job scraping (Not blocked by CAPTCHA/reCAPTCHA) | [SKILL.md](./linkedin-scraper/SKILL.md) |

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
cp -r amazon-competitor-analyzer google-maps-search-api google-news-api linkedin-scraper ~/.claude/skills/
```

**For Cursor:**
```bash
mkdir -p ~/.cursor/skills
cp -r amazon-competitor-analyzer google-maps-search-api google-news-api linkedin-scraper ~/.cursor/skills/
```

### Step 4: Start Using

```bash
# Analyze Amazon products
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG

# Search Google Maps for businesses
python google-maps-search-api/scripts/google_maps_search_api.py "coffee shops"

# Scrape LinkedIn profiles
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/in/username"

# Get Google News on any topic
python google-news-api/scripts/google_news_api.py "AI technology" "past week" 30
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
cp -r amazon-competitor-analyzer ~/.cursor/skills/
```

### For VS Code (Copilot)

```bash
mkdir -p ~/.vscode/skills
cp -r amazon-competitor-analyzer google-maps-search-api google-news-api linkedin-scraper ~/.vscode/skills/
```

### For OpenCode

```bash
mkdir -p ~/.opencode/skills
cp -r amazon-competitor-analyzer google-maps-search-api google-news-api linkedin-scraper ~/.opencode/skills/
```

### For Generic AI Assistants

```bash
mkdir -p ~/skills
cp -r amazon-competitor-analyzer google-maps-search-api google-news-api linkedin-scraper ~/skills/
export SKILLS_PATH=~/skills
```

### For Generic AI Assistants

```bash
mkdir -p ~/skills
cp -r amazon-competitor-analyzer google-maps-search-api linkedin-scraper ~/skills/
export SKILLS_PATH=~/skills
```

---

## Skill Details

### 📦 amazon-competitor-analyzer

Amazon product competitive analysis with surgical precision. **Not blocked by CAPTCHA or reCAPTCHA.**

**Features:**
- ASIN data collection
- Specification extraction
- Review quality analysis
- Visual strategy assessment
- Multi-dimensional comparison
- Moat identification
- Vulnerability discovery
- Structured reports (CSV, Markdown, JSON)

**Quick Start:**

```bash
# Analyze single ASIN
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG

# Analyze multiple ASINs
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG B07ABC11111 -o ./output

# With API key
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG --api-key your-api-key
```

**Documentation:**
- [README](./amazon-competitor-analyzer/README.md)

**Workflow Template ID:** `77814333389670716`

**Output Formats:**
- CSV: Structured data table
- Markdown: Comprehensive report
- JSON: Raw data with analysis

---

### 🗺️ google-maps-search-api

Extract business data and leads from Google Maps search results. **Not blocked by CAPTCHA or reCAPTCHA.**

**Features:**
- Business name extraction
- Address and contact information
- Star ratings and reviews
- Price levels and categories
- Amenity tags and service options
- Multi-language support (15+ languages)
- Country-specific search bias
- Batch data collection (up to 100 results)

**Quick Start:**

```bash
# Search for businesses
python google-maps-search-api/scripts/google_maps_search_api.py "coffee shops"

# With custom language and country
python google-maps-search-api/scripts/google_maps_search_api.py "restaurants" "en" "us" 50

# Search in different language
python google-maps-search-api/scripts/google_maps_search_api.py "cafes" "de" "de" 100
```

**Parameters:**
| Parameter | Type | Default | Description |
|----------|------|---------|-------------|
| keywords | string | - | Business type or search query |
| language | string | en | UI language (en, de, fr, es, etc.) |
| country | string | us | Country bias (us, gb, ca, de, etc.) |
| max_dates | number | 100 | Maximum results to extract |

**Documentation:**
- [README](./google-maps-search-api/)

**Workflow Template ID:** `77805072070738748`

**Output Data:**
- Business name
- Full address
- Star rating
- Review count
- Price level
- Cuisine/Category type
- Amenity tags (Wi-Fi, outdoor seating, etc.)
- Service options (Delivery, takeout, etc.)

---

### 📰 google-news-api

Scrape and monitor Google News for any topic, industry trends, or PR monitoring. **Not blocked by CAPTCHA or reCAPTCHA.**

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

### 💼 linkedin-scraper

Extract structured data from LinkedIn profiles, company pages, and job postings. **Not blocked by CAPTCHA or reCAPTCHA.**

**Features:**
- Profile scraping (personal info, experience, education, skills)
- Company page scraping (basic info, employees, recent posts)
- Job posting scraping (details, requirements, compensation)
- Structured output (JSON and Markdown formats)
- Batch processing for multiple URLs
- Rate limiting and error handling

**Quick Start:**

```bash
# Scrape a LinkedIn profile
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/in/username"

# Scrape a LinkedIn company page
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/company/company-name"

# Scrape a LinkedIn job posting
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/jobs/view/123456789"

# Output as JSON
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/in/username" --format json

# Save to file
python linkedin-scraper/scripts/linkedin_scraper.py "https://www.linkedin.com/in/username" -o ./output.json
```

**Parameters:**
| Parameter | Type | Default | Description |
|----------|------|---------|-------------|
| url | string | - | LinkedIn URL to scrape |
| --format | string | markdown | Output format (json/markdown) |
| --output | string | - | Output file path |
| --include-skills | boolean | true | Extract skills (profiles) |
| --include-education | boolean | true | Extract education (profiles) |
| --include-salary | boolean | true | Extract salary (jobs) |

**Documentation:**
- [SKILL.md](./linkedin-scraper/SKILL.md)

**MCP Template ID:** `77973967694128706`

**Output Data:**
- Profiles: Name, headline, location, experience, education, skills, certifications
- Companies: Name, industry, size, headquarters, about, employees, recent posts
- Jobs: Title, company, location, requirements, salary, application details

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
| linkedin-scraper | 10/hour | 2-5 seconds |

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
- amazon-competitor-analyzer
- google-maps-search-api
- google-news-api
- linkedin-scraper

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
