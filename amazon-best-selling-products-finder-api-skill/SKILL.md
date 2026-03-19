---
name: amazon-best-selling-products-finder-api-skill
description: "This skill helps users extract structured best-selling product data from Amazon via the BrowserAct API. Agent should proactively apply this skill when users express needs like search for best selling products on Amazon, extract Amazon product data based on keywords, find top rated Amazon products, monitor Amazon competitor prices and sales, discover trending products on Amazon marketplace, extract Amazon product titles prices and ratings, gather Amazon product sales volume for market research, search Amazon best sellers in specific region, collect Amazon product reviews and promotion details, analyze Amazon product availability and badges, get Amazon product data for market analysis."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Best Selling Products Finder API Skill

## 📖 Skill Introduction
This skill provides users with a one-stop product data extraction service using the BrowserAct Amazon Best Selling Products Finder API template. It can directly extract structured best-selling product data from Amazon. By inputting search keywords, data limit, and marketplace URL, you can easily get clean and usable product data including titles, prices, ratings, reviews, sales volume, and promotional details.

## ✨ Features
1. **No hallucinations, ensuring stable and precise data extraction**: Preset workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP access restrictions and geofencing**: No need to handle regional IP restrictions.
4. **More agile execution speed**: Compared to pure AI-driven browser automation solutions, task execution is faster.
5. **Extremely high cost-effectiveness**: Significantly reduces data acquisition costs compared to AI solutions that consume a large number of Tokens.

## 🔑 API Key Guide Flow
Before running, first check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions; require and wait for the user to collaborate to provide it.
**The Agent must inform the user at this time**:
> "Since you have not configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Search keywords used to find Amazon products.
   - **Example**: `iphone 17 pro max`, `gaming mouse`, `running shoes`

2. **Date_limit**
   - **Type**: `number`
   - **Description**: Maximum number of products to extract.
   - **Default**: `10`
   - **Recommendation**: Set to a lower number for quick checks, or higher for comprehensive analysis.

3. **Marketplace_url**
   - **Type**: `string`
   - **Description**: Amazon marketplace URL for region-specific searches.
   - **Default**: `https://www.amazon.com`
   - **Example**: `https://www.amazon.co.uk`, `https://www.amazon.de`

## 🚀 Call Method (Recommended)
The Agent should execute the following standalone script to achieve "one command to get results":

```bash
# Call example
python -u ./scripts/amazon_best_selling_products_finder_api.py "search keywords" limit "marketplace_url"
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** (e.g. `[14:30:05] Task Status: running`) during execution.
**Agent notice**:
- While waiting for the script to return the result, please keep an eye on the terminal output.
- As long as the terminal is still outputting new status logs, it means the task is running normally. Please do not mistakenly judge it as a deadlock or unresponsive.
- If the status remains unchanged for a long time or the script stops outputting and no result is returned, the retry mechanism can be triggered.

## 📊 Data Output Description
After successful execution, the script will parse and print the result directly from the API response. The result contains:
- `title`: Product title
- `brand`: Brand name
- `list_price`: Original list price
- `current_price`: Current selling price
- `star_rating`: Average star rating
- `review_count`: Total review count
- `past_month_sales`: Sales volume in the past month
- `availability`: Stock status
- `promotion`: Promotional offers
- `asin`: Amazon Standard Identification Number
- `category`: Product category
- `badge`: Badges like Amazon's Choice
- `product_url`: Direct link to the product

## ⚠️ Error Handling & Retry Mechanism
During the execution of the script, if an error occurs (such as network fluctuation or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this time, **do not retry**, and guide the user to recheck and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task execution fails (for example, the output starts with `Error:` or the returned result is empty), the Agent should **automatically try to execute the script again once**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Market Research**: Extract product listings and ratings to analyze the current market for specific keywords.
2. **Competitor Analysis**: Monitor competitor pricing, discounts, and sales volume over time.
3. **Trending Products Discovery**: Find the best-selling and highly rated products within a specific category.
4. **Price Monitoring**: Track current prices and list prices to optimize purchasing strategies.
5. **Cross-Region Analysis**: Compare product availability and pricing across different Amazon marketplaces.
