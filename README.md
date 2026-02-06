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

| Skill | Description | Version |
|-------|-------------|---------|
| [amazon-competitor-analyzer](./amazon-competitor-analyzer/) | Amazon product competitive analysis with surgical precision | v1.0.0 |

### 🔧 Browser Automation

| Skill | Description | Version |
|-------|-------------|---------|
| [browser-use](https://github.com/browser-use/browser-use) | General browser automation | - |

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
cp -r amazon-competitor-analyzer ~/.claude/skills/
```

**For Cursor:**
```bash
mkdir -p ~/.cursor/skills
cp -r amazon-competitor-analyzer ~/.cursor/skills/
```

### Step 4: Start Using

```bash
# Analyze Amazon products
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG
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
cp -r amazon-competitor-analyzer ~/.vscode/skills/
```

### For OpenCode

```bash
mkdir -p ~/.opencode/skills
cp -r amazon-competitor-analyzer ~/.opencode/skills/
```

### For Generic AI Assistants

```bash
mkdir -p ~/skills
cp -r amazon-competitor-analyzer ~/skills/
export SKILLS_PATH=~/skills
```

---

## Skill Details

### 📦 amazon-competitor-analyzer

Amazon product competitive analysis with surgical precision.

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

### Rate Limiting

| Skill | Max Requests | Recommended Interval |
|-------|-------------|---------------------|
| amazon-competitor-analyzer | 30/hour | 5-10 seconds |

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

- [browser-use](https://github.com/browser-use/browser-use) - Browser automation
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
