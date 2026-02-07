---
name: amazon-competitor-analyzer
description: Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. Compares specifications, pricing, review quality, and visual strategies to identify competitor moats and vulnerabilities.
---

# Amazon Competitor Analyzer

This skill scrapes Amazon product data from user-provided ASINs using browseract.com's browser automation API and performs deep competitive analysis. It compares specifications, pricing, review quality, and visual strategies to identify competitor moats and vulnerabilities.

## When to Use This Skill

- Competitive research: Input multiple ASINs to understand market landscape
- Pricing strategy analysis: Compare price bands across similar products
- Specification benchmarking: Deep dive into technical specs and feature differences
- Review insights: Analyze review quality, quantity, and sentiment patterns
- Visual strategy research: Evaluate main images, A+ content, and brand visuals
- Market opportunity discovery: Identify gaps and potential threats
- Product optimization: Develop optimization strategies based on competitor analysis
- New product research: Support new product development with market data

## What This Skill Does

1. **ASIN Data Collection**: Automatically extract product title, price, rating, review count, images, and core data using BrowserAct workflow templates
2. **Specification Extraction**: Deep extraction of technical specs, features, and materials
3. **Review Quality Analysis**: Analyze review patterns, keywords, and sentiment
4. **Visual Strategy Assessment**: Evaluate main images, A+ page design, and brand consistency
5. **Multi-Dimensional Comparison**: Side-by-side comparison of key metrics across products
6. **Moat Identification**: Identify core competitive advantages and barriers
7. **Vulnerability Discovery**: Find competitor weaknesses and market opportunities
8. **Structured Output**: Generate JSON and Markdown analysis reports

## Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows eliminate AI-generated hallucinations.
2.
**No CAPTCHA challenges**: Built-in bypass mechanisms eliminate the need to handle reCAPTCHA or other verification challenges.
3.
**No IP Access Restrictions or Geofencing**: Overcomes geographic IP limitations for stable global access.
4.
**Faster Execution Speed**: Tasks complete more rapidly than purely AI-driven browser automation solutions.
5. **Exceptional Cost Efficiency**: Significantly reduces data acquisition costs compared to token-intensive AI solutions.



## Prerequisites

### 1. BrowserAct.com Account Setup

You need a BrowserAct.com account and API key:

1. Visit [browseract.com](https://browseract.com)
2. Sign up for an account
3. Navigate to API settings
4. Generate an API key
5. Store your API key securely (environment variables recommended)

### 2. Environment Configuration

Set your API key as an environment variable:

```bash
export BROWSERACT_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
BROWSERACT_API_KEY=your-api-key-here
```

## How to Use

### Basic Competitor Analysis

```
Analyze the following Amazon ASIN: B09XYZ12345
```

```
Compare these three products: B07ABC11111, B07DEF22222, B07GHI33333
```

### Deep Specification Comparison

```
Analyze the technical specification differences: B09XYZ12345, B09ABC11111
```

### Review Quality Analysis

```
Analyze review quality and feedback: B09XYZ12345, B07DEF22222
```

### Visual Strategy Research

```
Research main image and visual presentation strategies: B09XYZ12345, B09ABC11111
```

### Complete Competitive Analysis

```
Analyze competitor landscape: B09XYZ12345, B07DEF22222, B07GHI33333, B09JKL44444
```

## Instructions

When a user requests Amazon competitor analysis:

### 1. ASIN Identification and Validation

Identify ASINs from user input:

- **ASIN Format**: 10-character alphanumeric (e.g., B09XYZ12345)
- **Validation**: Check format compliance with Amazon ASIN standards
- **URL Parsing**: Extract ASIN from Amazon product URLs
- **Error Handling**: Prompt user to correct invalid ASINs

### 2. BrowserAct API Implementation

```python
"""
BrowserAct API - Run Template Task and Wait for Completion
Scenarios for beginners - Synchronous task execution with official templates
"""
import os
import time
import traceback
import json
import requests

# ============ Configuration Area ============
# API Key - Get from: https://www.browseract.com/reception/integrations
API_KEY = os.getenv("BROWSERACT_API_KEY", "your-api-key-here")

# Workflow Template ID for Amazon product scraping
# You can get it from:
# - Run: python Workflow-Python/11.list_official_workflow_templates.py
# - Or visit: https://www.browseract.com/template?platformType=0
WORKFLOW_TEMPLATE_ID = "77814333389670716"

# Polling configuration
POLL_INTERVAL = 5  # Check task status every 5 seconds
MAX_WAIT_TIME = 1800  # Maximum wait time: 30 minutes (1800 seconds)

API_BASE_URL = "https://api.browseract.com/v2/workflow"


def create_input_parameters(asins):
    """Create input parameters for the workflow template"""
    return [
        {
            "name": "ASIN",
            "value": asin.strip()
        }
        for asin in asins if asin.strip()
    ]


def run_task_by_template(workflow_template_id, input_parameters):
    """Start a task using template"""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "workflow_template_id": workflow_template_id,
        "input_parameters": input_parameters,
    }
    
    api_url = f"{API_BASE_URL}/run-task-by-template"
    response = requests.post(api_url, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        task_id = result["id"]
        print(f"Task started successfully, Task ID: {task_id}")
        if "profileId" in result:
            print(f"   Profile ID: {result['profileId']}")
        return task_id
    else:
        print(f"Failed to start task: {response.json()}")
        return None


def get_task_status(task_id):
    """Get task status"""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    api_url = f"{API_BASE_URL}/get-task-status?task_id={task_id}"
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json().get("status")
        else:
            print(f"Failed to get task status: {response.json()}")
            return None
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        # Network error, will retry in next polling cycle
        return None


def get_task(task_id):
    """Get detailed task information and results"""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    api_url = f"{API_BASE_URL}/get-task?task_id={task_id}"
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get task details: {response.json()}")
            return None
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"Network error while getting task details: {type(e).__name__}")
        return None


def wait_for_task_completion(task_id):
    """Wait for task completion with progress updates"""
    start_time = time.time()
    previous_status = None
    
    print(f"Waiting for task completion (max wait time: {MAX_WAIT_TIME // 60} minutes)...")
    
    while True:
        # Check if timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > MAX_WAIT_TIME:
            print(f"Wait timeout (waited {elapsed_time:.0f} seconds)")
            return None
        
        # Get task status
        status = get_task_status(task_id)
        
        if status is None:
            # Network error or API error, continue waiting
            elapsed = int(elapsed_time)
            print(f"   Network error, retrying... (waited {elapsed} seconds)", end="\r")
        elif status == "finished":
            print(f"Task completed successfully!")
            return "finished"
        elif status == "failed":
            print(f"Task execution failed")
            return "failed"
        elif status == "canceled":
            print(f"Task canceled")
            return "canceled"
        else:
            # running, created, paused, etc.
            elapsed = int(elapsed_time)
            if status != previous_status:
                print(f"   Status: {status} (waited {elapsed} seconds)", end="\r")
                previous_status = status
            else:
                print(f"   Status: {status} (waited {elapsed} seconds)", end="\r")
        
        # Wait before checking again
        time.sleep(POLL_INTERVAL)


def scrape_amazon_products(asins):
    """
    Main function to scrape Amazon product data
    
    Args:
        asins: List of Amazon ASINs to scrape
        
    Returns:
        dict: Task result containing product data
    """
    if not asins:
        raise ValueError("No ASINs provided for scraping")
    
    # Create input parameters
    input_parameters = create_input_parameters(asins)
    
    print(f"Starting Amazon product scraping for {len(asins)} ASIN(s)...")
    print(f"ASINs: {[p['value'] for p in input_parameters]}")
    
    # Step 1: Start task using template
    task_id = run_task_by_template(WORKFLOW_TEMPLATE_ID, input_parameters)
    
    if task_id is None:
        raise Exception("Unable to start scraping task")
    
    # Step 2: Wait for task completion
    final_status = wait_for_task_completion(task_id)
    
    if final_status != "finished":
        raise Exception(f"Task did not complete successfully. Status: {final_status}")
    
    # Step 3: Get task results
    task_info = get_task(task_id)
    
    if task_info is None:
        raise Exception("Unable to retrieve task results")
    
    return task_info


def main():
    """Main execution function for testing"""
    print("=" * 60)
    print("Amazon Product Scraper - BrowserAct Integration")
    print("=" * 60)
    
    try:
        # Example: Scrape multiple ASINs
        test_asins = ["B09XYZ12345", "B07ABC11111"]
        
        print(f"\nScraping Amazon products: {test_asins}")
        results = scrape_amazon_products(test_asins)
        
        print("\n" + "=" * 60)
        print("Scraping Results (JSON):")
        print("=" * 60)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        return results
        
    except Exception as e:
        error = traceback.format_exc()
        print(f"Error occurred: {error}")
        raise


# Example usage
if __name__ == "__main__":
    main()
```

### 3. Task Output Data Structure

The BrowserAct API returns structured data in the following format:

```json
{
  "id": "task_id_12345",
  "status": "finished",
  "created_at": "2026-02-06T10:00:00Z",
  "completed_at": "2026-02-06T10:05:00Z",
  "results": {
    "products": [
      {
        "asin": "B09XYZ12345",
        "url": "https://www.amazon.com/dp/B09XYZ12345",
        "product_info": {
          "title": "Complete product title",
          "brand": "Brand name",
          "manufacturer": "Manufacturer",
          "model": "Model"
        },
        "pricing": {
          "current_price": 29.99,
          "original_price": 39.99,
          "discount_percent": 25,
          "currency": "USD"
        },
        "reviews": {
          "average_rating": 4.5,
          "total_count": 1234,
          "rating_distribution": {
            "5_star": 65,
            "4_star": 20,
            "3_star": 10,
            "2_star": 3,
            "1_star": 2
          }
        },
        "specifications": {
          "weight": "1.5 lbs",
          "dimensions": "10 x 5 x 3 inches",
          "material": "Plastic/Metal",
          "features": ["Feature 1", "Feature 2"]
        },
        "media": {
          "main_image": "https://example.com/image.jpg",
          "thumbnails": ["url1", "url2"],
          "has_video": true,
          "has_a_plus": true
        },
        "seller": {
          "type": "Amazon",
          "fulfillment": "FBA",
          "availability": "InStock"
        }
      }
    ]
  }
}
```

### 4. Workflow Template Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ASIN | string | Yes | Amazon Standard Identification Number (10 characters) |
| output_format | string | No | Output format: "json" or "markdown" (default: "json") |
| include_reviews | boolean | No | Include review analysis (default: true) |
| include_images | boolean | No | Include image URLs (default: true) |
| include_specs | boolean | No | Include specifications (default: true) |

### 5. Error Handling

```python
import requests

def safe_api_call(api_func, max_retries=3, delay=5):
    """Execute API call with retry logic"""
    for attempt in range(max_retries):
        try:
            result = api_func()
            if result is not None:
                return result
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    raise Exception(f"API call failed after {max_retries} attempts")


def handle_api_error(response):
    """Handle API error responses"""
    error_messages = {
        400: "Invalid request parameters",
        401: "Authentication failed - check API key",
        403: "Access denied - insufficient permissions",
        404: "Resource not found",
        429: "Rate limit exceeded - slow down",
        500: "Internal server error",
        503: "Service temporarily unavailable"
    }
    
    status_code = response.status_code
    message = error_messages.get(status_code, f"Unknown error (status: {status_code})")
    
    return {
        "error": message,
        "status_code": status_code,
        "details": response.json() if response.content else None
    }
```

### 6. Rate Limiting Best Practices

```python
import time
from datetime import datetime, timedelta


class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = datetime.now()
        
        # Remove requests outside the time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < timedelta(seconds=self.time_window)]
        
        if len(self.requests) >= self.max_requests:
            # Wait until oldest request expires
            oldest = min(self.requests)
            wait_time = self.time_window - (now - oldest).seconds
            if wait_time > 0:
                print(f"Rate limit reached, waiting {wait_time} seconds...")
                time.sleep(wait_time)
        
        self.requests.append(now)


# Usage
rate_limiter = RateLimiter(max_requests=10, time_window=60)

def scrape_with_rate_limiting(asins):
    """Scrape products with rate limiting"""
    results = []
    
    for asin in asins:
        rate_limiter.wait_if_needed()
        result = scrape_single_asin(asin)
        results.append(result)
    
    return results
```

## Data Extraction and Structuring

```markdown
## Product Information

### ASIN: B09XYZ12345

**Product Title**: [Complete product title]
**Status**: Success / Failed
**Scraped At**: [Timestamp]

---

#### Pricing Information

| Item | Value |
|------|-------|
| Current Price | $XX.XX |
| Original Price | $XX.XX |
| Discount | XX% OFF |
| Price Range | $XX.XX - $XX.XX (variants) |

---

#### Rating and Reviews

| Item | Value |
|------|-------|
| Average Rating | X.X / 5.0 |
| Total Reviews | X,XXX |
| Rating Distribution | 5-star XX% / 4-star XX% / 3-star XX% / 2-star XX% / 1-star XX% |

---

#### Visual Assets

| Item | Count/Status |
|------|--------------|
| Main Image | [URL / N/A] |
| Thumbnail Count | X images |
| Video Count | X videos |
| 360° View | Available / N/A |
| A+ Page | Available / N/A |
| Brand Story | Available / N/A |

---

#### Specification Parameters

| Parameter | Value |
|-----------|-------|
| Brand | [Brand name] |
| Model | [Model info] |
| Weight | [Weight] |
| Dimensions | [Dimensions] |
| Material | [Material] |
| Country of Origin | [Country] |

---

#### Seller Information

| Item | Information |
|------|-------------|
| Seller Type | Amazon / Third-Party |
| Seller Name | [Name] |
| Fulfillment | FBA / Self |
| Availability | In Stock / Out of Stock / Pre-order |

### JSON Output Format

```json
{
  "asin": "B09XYZ12345",
  "url": "https://www.amazon.com/dp/B09XYZ12345",
  "scraped_at": "2026-02-06T10:00:00Z",
  "status": "success",
  "product_info": {
    "title": "[Complete product title]",
    "brand": "[Brand name]",
    "manufacturer": "[Manufacturer]",
    "model": "[Model]"
  },
  "pricing": {
    "current_price": XX.XX,
    "original_price": XX.XX,
    "discount_percent": XX,
    "currency": "USD",
    "price_range": {
      "min": XX.XX,
      "max": XX.XX
    }
  },
  "reviews": {
    "average_rating": X.X,
    "total_count": XXXX,
    "rating_distribution": {
      "5_star": XX,
      "4_star": XX,
      "3_star": XX,
      "2_star": XX,
      "1_star": XX
    }
  },
  "specifications": {
    "weight": "[Weight]",
    "dimensions": "[Dimensions]",
    "material": "[Material]",
    "country_of_origin": "[Country]",
    "features": ["[Feature1]", "[Feature2]"]
  },
  "media": {
    "main_image": "[URL]",
    "thumbnails": ["[URL1]", "[URL2]"],
    "has_video": true,
    "has_a_plus": true
  },
  "seller": {
    "type": "[Amazon/Third-Party]",
    "name": "[Seller name]",
    "fulfillment": "[FBA/Self]",
    "availability": "[InStock/OutOfStock]"
  },
  "bestseller_rank": [
    {
      "category": "[Category]",
      "rank": XXX
    }
  ]
}
```

## LLM Deep Analysis

After collecting data from multiple products, perform surgical competitive analysis:

```markdown
## Competitive Deep Analysis

### 1. Price Dimension Analysis

#### Price Band Positioning

| Product | ASIN | Price | Position | Price Advantage |
|---------|------|-------|----------|----------------|
| [Product A] | B09XXX | $XX.XX | Premium/Mid-range/Economy | High/Medium/Low |
| [Product B] | B09YYY | $XX.XX | Premium/Mid-range/Economy | High/Medium/Low |
| [Product C] | B09ZZZ | $XX.XX | Premium/Mid-range/Economy | High/Medium/Low |

**Price Range Analysis**:
- Lowest Price: $XX.XX ([Product Name])
- Highest Price: $XX.XX ([Product Name])
- Median Price: $XX.XX
- Price Spread: XX%

**Pricing Strategy Insights**:
- [Analyze pricing strategies across products]
- [Identify price gaps]
- [Discover pricing opportunities]

#### Value Assessment

| Product | Feature Count | Cost per Feature | Feature Density | Value Index |
|---------|---------------|------------------|-----------------|-------------|
| [A] | XX | $X.XX | High/Medium/Low | X.X |
| [B] | XX | $X.XX | High/Medium/Low | X.X |
| [C] | XX | $X.XX | High/Medium/Low | X.X |

### 2. Specification Comparison

#### Core Parameter Matrix

| Parameter | [Product A] | [Product B] | [Product C] | Industry Benchmark |
|-----------|-------------|-------------|-------------|-------------------|
| [Param 1] | [Value] | [Value] | [Value] | [Value] |
| [Param 2] | [Value] | [Value] | [Value] | [Value] |
| [Param 3] | [Value] | [Value] | [Value] | [Value] |
| [Param 4] | [Value] | [Value] | [Value] | [Value] |
| [Param 5] | [Value] | [Value] | [Value] | [Value] |

#### Differentiation Analysis

**Exclusive Advantages**:
- [Product A Exclusive]: Description + User Value + Market Rarity
- [Product B Exclusive]: Description + User Value + Market Rarity
- [Product C Exclusive]: Description + User Value + Market Rarity

**Weakness Comparison**:
- [Product A Weakness]: Missing Feature + User Impact + Alternative
- [Product B Weakness]: Missing Feature + User Impact + Alternative
- [Product C Weakness]: Missing Feature + User Impact + Alternative

### 3. Review Weight Analysis

#### Review Quality Assessment

| Product | Total Reviews | Avg Rating | Positive % | Negative % | Quality Index |
|---------|---------------|------------|------------|------------|---------------|
| [A] | X,XXX | X.X | XX% | XX% | X.X |
| [B] | X,XXX | X.X | XX% | XX% | X.X |
| [C] | X,XXX | X.X | XX% | XX% | X.X |

#### Review Keyword Analysis

**Positive Keywords**:
- [Keyword 1] (XX occurrences)
- [Keyword 2] (XX occurrences)
- [Keyword 3] (XX occurrences)

**Negative Keywords**:
- [Keyword 1] (XX occurrences)
- [Keyword 2] (XX occurrences)
- [Keyword 3] (XX occurrences)

#### Sentiment Analysis

| Sentiment Dimension | [Product A] | [Product B] | [Product C] |
|--------------------|-------------|-------------|-------------|
| Positive Sentiment | XX% | XX% | XX% |
| Neutral Sentiment | XX% | XX% | XX% |
| Negative Sentiment | XX% | XX% | XX% |

**Review Insights**:
- [Product A Key Praise Points]
- [Product A Main Complaints]
- [Product B Key Praise Points]
- [Product B Main Complaints]

#### Credibility Analysis

| Product | Verified Purchase Rate | Avg Review Length | Image/Video Review % | Credibility Score |
|---------|----------------------|-------------------|---------------------|-------------------|
| [A] | XX% | XX words | XX% | X.X |
| [B] | XX% | XX words | XX% | X.X |
| [C] | XX% | XX words | XX% | X.X |

### 4. Visual Strategy Analysis

#### Main Image Assessment

| Product | Style | Background | Information Density | Visual Appeal | Conversion Potential |
|---------|-------|------------|---------------------|---------------|---------------------|
| [A] | [Description] | Solid/Scene/Transparent | High/Medium/Low | Score | High/Medium/Low |
| [B] | [Description] | Solid/Scene/Transparent | High/Medium/Low | Score | High/Medium/Low |
| [C] | [Description] | Solid/Scene/Transparent | High/Medium/Low | Score | High/Medium/Low |

**Image Strategy Insights**:
- [Analyze visual strategies across products]
- [Identify effective visual elements]
- [Discover visual optimization opportunities]

#### A+ Page Analysis

| Product | A+ Type | Module Count | Information Architecture | Brand Presentation | UX Score |
|---------|---------|-------------|-------------------------|-------------------|----------|
| [A] | Standard/Premium | XX | Excellent/Good/Poor | Strong/Medium/Weak | Score |
| [B] | Standard/Premium | XX | Excellent/Good/Poor | Strong/Medium/Weak | Score |
| [C] | Standard/Premium | XX | Excellent/Good/Poor | Strong/Medium/Weak | Score |

**A+ Page Highlights**:
- [Product A A+ Highlights]
- [Product B A+ Highlights]
- [Product C A+ Highlights]

### 5. Competitive Landscape Summary

#### Market Position Matrix

| Dimension | Leader | Challenger | Follower | Niche |
|----------|--------|------------|----------|-------|
| Volume | [Product] | [Product] | [Product] | [Product] |
| Price | [Product] | [Product] | [Product] | [Product] |
| Rating | [Product] | [Product] | [Product] | [Product] |
| Features | [Product] | [Product] | [Product] | [Product] |

#### Competitive Differentiation Map

```
                    Feature Richness
                          ↑
                          |
         [Product B]      |          [Product A]
         (High Feature)    |         (High Brand)
                          |
   ◄──────────────────────┼──────────────────────►
                          |
         [Product C]      |          [Product D]
         (Low Feature)    |         (Low Brand)
                          |
                          ↓
                    Simplified Features

   Price Band: Left Low Right High | Brand: Bottom Low Top High
```

### 6. Moat Identification

#### Competitor Core Moats

**Patent/Technology Barriers**:
- [Specific patent or tech advantage]
- [Imitation Difficulty]: High/Medium/Low
- [Defense Duration]: Long-term/Medium-term/Short-term

**Economies of Scale**:
- [Cost advantage source]
- [Pricing flexibility]
- [Competitor catch-up difficulty]

**Brand Equity**:
- [Brand awareness level]
- [Customer loyalty metrics]
- [Brand premium capability]

**Channel Advantages**:
- [Amazon ranking strength]
- [Buy Box share]
- [Review accumulation advantage]

**Supply Chain Barriers**:
- [Exclusive supplier relationships]
- [Cost structure advantage]
- [Capacity constraints]

#### Moat Strength Assessment

| Moat Type | [Product A] | [Product B] | [Product C] |
|-----------|-------------|-------------|-------------|
| Patents/Tech | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Economies of Scale | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Brand Assets | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Channel Advantage | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Customer Lock-in | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Overall Score** | **X.X/5.0** | **X.X/5.0** | **X.X/5.0** |

### 7. Vulnerabilities and Opportunities

#### Strategic Weaknesses

**Product-Level**:
- [Weakness 1]: Description + User Impact + Market Share Effect
- [Weakness 2]: Description + User Impact + Market Share Effect

**Pricing-Level**:
- [Price Disadvantage]: Analysis + Cause + Adjustment Recommendation

**Review-Level**:
- [Negative Review Pattern]: Issue + Difficulty + Exploitation Value

**Visual-Level**:
- [Visual Defect]: Issue + User Impact + Optimization Space

**Operational-Level**:
- [Operational Shortcoming]: Performance + Impact + Improvement Direction

#### Opportunity Matrix

| Opportunity Type | Description | Size | Difficulty | Priority |
|-----------------|-------------|------|------------|----------|
| [Opportunity 1] | [Description] | Large/Medium/Small | High/Medium/Low | Immediate/Planned/Watch |
| [Opportunity 2] | [Description] | Large/Medium/Small | High/Medium/Low | Immediate/Planned/Watch |
| [Opportunity 3] | [Description] | Large/Medium/Small | High/Medium/Low | Immediate/Planned/Watch |

#### Differentiation Entry Points

**Best Differentiation Directions**:
1. [Direction 1]: Recommendation + Expected Effect + Implementation Difficulty
2. [Direction 2]: Recommendation + Expected Effect + Implementation Difficulty
3. [Direction 3]: Recommendation + Expected Effect + Implementation Difficulty

**Competitive Traps to Avoid**:
- [Trap 1]: Cause + Alternative Approach
- [Trap 2]: Cause + Alternative Approach

### 8. Recommendations

#### Strategic Positioning

**Competition Strategy for [Target Product]**:
- [Core Strategy]: Actionable recommendations
- [Differentiation Focus]: Key differentiators
- [Pricing Strategy]: Pricing recommendations
- [Marketing Focus]: Promotion direction

#### Product Optimization Priority

| Optimization Item | Urgency | Impact | Difficulty | Recommendation |
|------------------|---------|--------|------------|---------------|
| [Item 1] | High/Medium/Low | High/Medium/Low | High/Medium/Low | Implement Now |
| [Item 2] | High/Medium/Low | High/Medium/Low | High/Medium/Low | Plan for Later |
| [Item 3] | High/Medium/Low | High/Medium/Low | High/Medium/Low | Long-term |

#### Risk Warnings

| Risk Type | Description | Likelihood | Impact | Mitigation |
|-----------|-------------|------------|--------|-----------|
| [Risk 1] | [Description] | High/Medium/Low | High/Medium/Low | [Measure] |
| [Risk 2] | [Description] | High/Medium/Low | High/Medium/Low | [Measure] |

### 9. Executive Summary

#### Key Findings

1. **[Finding 1]**: One-sentence summary
2. **[Finding 2]**: One-sentence summary
3. **[Finding 3]**: One-sentence summary

#### Critical Actions

1. **[Action 1]**: Specific recommendation
2. **[Action 2]**: Specific recommendation
3. **[Action 3]**: Specific recommendation

#### Competitive Position

- **Your Product vs [Competitor A]**: Advantage/Disadvantage/Tie
- **Your Product vs [Competitor B]**: Advantage/Disadvantage/Tie
- **Your Product vs [Competitor C]**: Advantage/Disadvantage/Tie

---

**Analysis Completion Time**: [Timestamp]
**Products Analyzed**: X
**Data Source**: Amazon.com
**Analysis Method**: LLM Deep Semantic Analysis
```

## Best Practices

### 1. Data Collection Optimization

- **Batch Processing**: Maximum 10 ASINs per analysis to avoid rate limits
- **Delay Strategy**: 3-5 second delay between ASIN requests
- **Retry Logic**: Automatic retry, 30-second delay on failure
- **Caching**: No duplicate collection within 24 hours for same ASIN

### 2. Analysis Quality Assurance

- **Cross-Validation**: Multi-dimensional data corroboration
- **Outlier Detection**: Identify and handle anomalous data points
- **Time Dimension**: Consider product age effects
- **Market Trends**: Combine with category trend analysis

### 3. Strategy Implementation

- **Priority Ranking**: Rank recommendations by impact and feasibility
- **Resource Assessment**: Define required resources for implementation
- **ROI Estimation**: Quantify expected benefits and costs
- **Risk Assessment**: Identify potential implementation risks

### 4. Compliance and Ethics

- **Data Use Compliance**: Only for legitimate business analysis purposes
- **Platform Rules**: Respect Amazon's Terms of Service
- **Data Security**: Protect collected data appropriately
- **Information Discretion**: Do not disclose sensitive business intelligence

## Example Usage

**User Request**:
```
Analyze Amazon competitors, compare market landscape:
B09XYZ12345, B07ABC11111, B07DEF22222, B09JKL44444
```

**Output**:
```
## Competitive Analysis Report

### Analysis Overview

| Product | ASIN | Price | Rating | Reviews | Brand |
|---------|------|-------|--------|---------|-------|
| [Product A] | B09XYZ12345 | $XX.XX | X.X | X,XXX | [Brand] |
| [Product B] | B07ABC11111 | $XX.XX | X.X | X,XXX | [Brand] |
| [Product C] | B07DEF22222 | $XX.XX | X.X | X,XXX | [Brand] |
| [Product D] | B09JKL44444 | $XX.XX | X.X | X,XXX | [Brand] |

[... Complete deep analysis report ...]
```

---

**User Request**:
```
Analyze technical specification differences: B09XYZ12345, B09ABC11111
```

**Output**:
```
## Technical Specification Deep Comparison

### Core Parameter Matrix

| Parameter | [Product A] | [Product B] | [Product C] | Assessment |
|-----------|-------------|-------------|-------------|------------|
| [Param 1] | [Value] | [Value] | [Value] | [Analysis] |
| [Param 2] | [Value] | [Value] | [Value] | [Analysis] |

[... More analysis ...]
```

---

**User Request**:
```
Research visual presentation strategies: B09XYZ12345, B09ABC11111
```

**Output**:
```
## Visual Strategy Comparison

### Main Image Assessment

| Dimension | [Product A] | [Product B] |
|-----------|-------------|-------------|
| Main Image Style | [Description] | [Description] |
| Background Type | Solid/Scene | Solid/Scene |
| Visual Appeal | XX/10 | XX/10 |

[... Complete visual analysis ...]
```

## Limitations

1. **Data Timeliness**: Amazon page data changes in real-time; analysis results have limited shelf life
2. **Anti-Scraping**: May trigger Amazon's anti-bot measures
3. **Page Structure Changes**: Amazon layout updates may invalidate selectors
4. **Regional Limitations**: Data based on specific Amazon site (e.g., US)
5. **Review Sampling**: Review analysis based on samples; may have bias
6. **A+ Page Access**: Some A+ content may require special permissions
7. **Buy Box Data**: Real-time Buy Box information may be restricted
8. **Historical Data**: Cannot directly access historical price and ranking data

## Troubleshooting

### Issue: API Call Failed

**Solution**:
- Verify API key is correctly configured
- Confirm account has sufficient API quota
- Validate ASIN format is correct
- Check network connectivity

### Issue: Task Timeout

**Solution**:
- Check MAX_WAIT_TIME setting (default 30 minutes)
- Verify BrowserAct service status
- Reduce number of ASINs per batch
- Check template availability

### Issue: Incomplete Data Extraction

**Solution**:
- Increase wait time for page load
- Check if template needs updating
- Verify target page is accessible
- Review API response for errors

### Issue: Abnormal Analysis Results

**Solution**:
- Confirm data collection completeness
- Check for anomalous data points
- Validate comparison dimensions are reasonable
- Re-run analysis process

### Issue: Amazon Anti-Scraping Triggered

**Solution**:
- Reduce request frequency
- Increase delay between requests
- Use smaller batches
- Contact BrowserAct support for rate limit adjustment

## Related Skills

- `browseract-integration` - BrowserAct API integration
- `web-scraper` - General web scraping
- `data-analyzer` - Data analysis tools
- `competitor-research` - Competitor research
- `market-researcher` - Market research tools
- `amazon-rank-tracker` - Amazon ranking tracking

## Resources

- [BrowserAct Documentation](https://browseract.com/docs)
- [BrowserAct Workflow Templates](https://www.browseract.com/template?platformType=0)
- [Amazon Product Page Best Practices](https://developer.amazon.com/docs)
- [Amazon Seller Central](https://sellercentral.amazon.com)
- [Competitive Analysis Frameworks](https://www.business.com/articles/competitive-analysis/)
- [E-commerce Data Analysis Methods](https://www.ecommerceted.com/guides/competitive-analysis/)

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-02-06
**Compatibility**: BrowserAct API v2+
**Supported Site**: Amazon.com (US)
