---
name: amazon-competitor-analyzer
description: Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. Compares specifications, pricing, review quality, and visual strategies to identify competitor moats and vulnerabilities.
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Competitor Analyzer

This skill scrapes Amazon product data from user-provided ASINs using browseract.com's browser automation API and performs deep competitive analysis.

## When to Use This Skill

- Competitive research: Input multiple ASINs to understand market landscape
- Pricing strategy analysis: Compare price bands across similar products
- Specification benchmarking: Deep dive into technical specs and feature differences
- Review insights: Analyze review quality, quantity, and sentiment patterns
- Market opportunity discovery: Identify gaps and potential threats

## What This Skill Does

1. **ASIN Data Collection**: Extract product title, price, rating, review count, images
2. **Specification Extraction**: Deep extraction of technical specs, features, and materials
3. **Review Quality Analysis**: Analyze review patterns, keywords, and sentiment
4. **Multi-Dimensional Comparison**: Side-by-side comparison of key metrics
5. **Moat Identification**: Identify core competitive advantages and barriers
6. **Vulnerability Discovery**: Find competitor weaknesses and market opportunities

## Features

1. **Stable and accurate data extraction**: Pre-set workflows ensure consistent results.
2. **Browser automation**: Uses BrowserAct's automated browser instances for reliable data collection.
3. **Global accessibility**: BrowserAct provides servers in multiple regions.
4. **Fast execution**: Optimized workflow templates complete tasks quickly.
5. **Cost efficient**: Reduces manual research time and associated costs.

## Prerequisites

### BrowserAct.com Account Setup

You need a BrowserAct.com account and API key:

1. Visit [browseract.com](https://browseract.com)
2. Sign up for an account
3. Navigate to [API Settings](https://www.browseract.com/reception/integrations)
4. Generate an API key

### Environment Configuration

Copy the `.env.example` file to `.env` and add your API key:

```bash
cp .env.example .env
# Edit .env and replace YOUR_API_KEY_HERE with your actual API key
```

Or set as environment variable:

```bash
export BROWSERACT_API_KEY="your-api-key-here"
```

## Usage

### Basic Analysis

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG
```

### Multiple Products

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG B07ABC11111 B08N5WRWNW
```

### With Output Directory

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG -o ./output
```

### Output Formats

- **CSV**: Structured data table
- **Markdown**: Comprehensive report
- **JSON**: Raw data with analysis

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| asins | string | - | One or more Amazon ASINs to analyze |
| --output, -o | string | ./output | Output directory |
| --format | string | all | Output format (csv/markdown/json/all) |
| --api-key | string | env | BrowserAct API key |

## Dependencies

This skill requires the following Python packages:

```bash
pip install requests
```

Optional (for automatic .env loading):
```bash
pip install python-dotenv
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| BROWSERACT_API_KEY | Yes | Your BrowserAct API key. Get it from [BrowserAct Console](https://www.browseract.com/reception/integrations) |

## Error Handling

- **Invalid API Key**: Check BROWSERACT_API_KEY environment variable
- **Network Error**: Verify internet connection
- **Rate Limit**: Wait and retry with exponential backoff
- **Invalid ASIN**: Verify ASIN format (10 alphanumeric characters)

---

**Version**: 1.0.0  
**Updated**: 2026-02-09  
**Template ID**: `77814333389670716`
