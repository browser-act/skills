---
name: amazon-listing-competitor-analysis-skill
description: "This skill helps users analyze Amazon competitor listings by ASIN and produce structured competitive intelligence plus strategic opportunity points for their own go-to-market. The Agent should proactively apply this skill when users want to analyze a competitor Amazon listing by ASIN, understand what a top-ranked product does right in content keywords or visuals, find market gaps and unmet buyer needs, turn competitor research into opportunity maps for their brand, identify keyword placement patterns on rival listings, extract SEO insights from Amazon product pages, reverse-engineer competitor bullet and title strategies, mine competitor reviews for buyer psychology, compare seller and A plus content patterns, run gap analysis before launching a new SKU, research why a listing wins conversion signals, synthesize whitespace you can own versus the diagnosed listing, or say just look at this ASIN with a competitive or optimization angle."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Listing Competitor Analysis

## 📖 Brief
This skill runs a two-phase workflow on a single **competitor** Amazon listing. **Phase 1** uses the BrowserAct Amazon Listing Extractor for SEO template to pull visible product data from that listing. **Phase 2** diagnoses what that competitor does well and where the market shows gaps, then closes with **your strategic opportunity points** (how you can win next to them). Do **not** end with instructions that read like editing or rewriting **this competitor's** listing; the analyzed ASIN is evidence only. Final narrative output should be grounded in extracted data, not generic claims.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to deal with regional IP restrictions or geofencing.
4. **Faster execution**: Tasks execute faster compared to purely AI-driven browser automation solutions.
5. **Extremely high cost-efficiency**: Significantly reduces data acquisition costs compared to AI solutions that consume massive amounts of tokens.

## 🔑 API Key Guide
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions first; you should ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **ASIN**
   - **Type**: `string`
   - **Description**: The ASIN (Amazon Standard Identification Number) of the Amazon product to analyze.
   - **Example**: `B0CS62LY6P`
   - **Required**: Yes

2. **Marketplace_url**
   - **Type**: `string`
   - **Description**: The base URL of the Amazon marketplace. Use the correct regional site for the listing.
   - **Example**: `https://www.amazon.com/`, `https://www.amazon.de/`
   - **Default**: `https://www.amazon.com/`

## 🚀 Invocation Method
Run Phase 1 extraction with the script below. After structured data is returned, the Agent performs Phase 2 analysis using the framework in **Competitive Analysis Framework (Phase 2)**. The closing section must synthesize **opportunity points for the user's business**, not a checklist of edits applied to the competitor page under review.

```bash
python -u ./scripts/amazon_listing_competitor_analysis.py "B0CS62LY6P" "https://www.amazon.com/"
```

When only the ASIN is needed, the marketplace argument may be omitted; the script defaults to `https://www.amazon.com/`.

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal continues to output new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, only then consider triggering the retry mechanism.

## 📊 Data Output
Upon successful execution, the script prints the API result string (or full task JSON if no string field is present). Typical fields include:
- `asin`, `title`, `product_url`, `brand`, `price`, `coupon_text`, `rating`, `review_count`, `best_sellers_rank`, `availability`, `prime_eligible`
- `description`, `short_description`, `category`, `key_features`, `bullet_points`
- `main_image_url`, `additional_image_urls`, `seller_name`, `ships_from`, `sold_by`
- `specifications`, `product_details`, `attributes`, and review-related blocks (reviewer, content, date, helpful votes, etc.)

Use this payload as the single source of truth for Phase 2; do not invent listing facts.

## ⚠️ Error Handling & Retry
During script execution, if errors occur (such as network fluctuations or task failure), the Agent should follow this logic:

1. **Check the output content**:
   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. At this point, **do not retry**, but guide the user to recheck and provide the correct API Key.
   - If the output **contains** `"concurrent"` or `"too many running tasks"` or similar concurrency limit messages, it means the concurrent task limit for the current subscription plan has been reached. **Do not retry**; guide the user to upgrade their plan.
     **Agent must inform the user**:
     > "The current task cannot be executed because your BrowserAct account has reached the limit of concurrent tasks. Please go to the [BrowserAct Plan Upgrade Page](https://www.browseract.com/reception/recharge) to upgrade your subscription plan and enjoy more concurrent task benefits."
   - If the output **does not contain** the above error keywords but the task fails (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to run the script once more**.

2. **Retry limit**:
   - Automatic retry is limited to **once**. If the second attempt still fails, stop retrying and report the specific error message to the user.

## 🌟 Typical Use Cases
1. **Competitor listing teardown**: Analyze one ASIN to see title formula, bullets, and differentiation language.
2. **Keyword placement audit**: Map where primary and long-tail terms appear across title, bullets, and description or A+ content.
3. **Visual strategy review**: Infer image narrative, infographic highlights, and video approach from extracted media data.
4. **Buyer-validated selling points**: Use high-helpful positive reviews to confirm what buyers value versus what the listing emphasizes.
5. **Unmet needs mining**: Use three-star and mixed reviews to find feature and expectation gaps.
6. **Pre-launch gap analysis**: Compare a planned positioning against a top competitor's listing structure.
7. **Cross-marketplace research**: Run the same ASIN on different regional Amazon URLs for localized copy signals.
8. **Opportunity backlog from a rival listing**: Turn extracted facts and gaps into a prioritized map of positioning, search, creative, and offer opportunities for your side of the market.
9. **SEO and conversion benchmarking**: Relate BSR, rating volume, and copy patterns without guessing unavailable metrics.
10. **Review-driven objection handling**: Surface recurring complaints to address in copy or images.

## 🧠 Competitive Analysis Framework (Phase 2)
After extraction succeeds, work through each dimension below. Every insight must be grounded in the actual extracted data.

### Layer 1 — What the Competitor Did Right

**1. Content Strategy**

- **Title formula**: Information order, primary keyword placement, brand-first vs feature-first vs use-case-first.
- **Bullet priority**: What Bullet 1 leads with; selling point order across bullets (signal of tested conversion order).
- **Differentiation language**: How generic category features are phrased to sound distinct.
- **A+ content**: Modules implied by extracted content (comparison table, brand story, lifestyle, spec callouts).

**2. Keyword Placement Strategy**

Map *where* terms appear (not only which terms exist):

- Title (first 80 chars) → primary ranking bets
- Bullets 1–2 → secondary high-weight terms
- Bullets 3–5 → long-tail and use-case terms
- Description / A+ → supplementary terms and synonyms

**3. Visual Content Strategy**

- **Image narrative arc**: Sequence story (hero, lifestyle, pain point, specs, size comparison, social proof, guarantee).
- **Infographic data**: Numbers or attributes highlighted and how they are presented.
- **Video** (if present in data): Hook length, demo vs lifestyle, subtitles.
- **Overall style**: Premium, approachable, technical, lifestyle-focused.

**4. Buyer-Validated Selling Points**

From four- to five-star reviews with high helpful votes:

- What reviewers praise that the listing underplays
- Unexpected benefits buyers mention

### Layer 2 — What the Market Lacks

**5. Unmet Buyer Needs**

From three-star reviews and recurring themes in low stars (non-defect noise):

- "I wish it had…", "Would be five stars if…", "Good but not great because…"

**6. Keyword Gaps**

- Natural search terms buyers would use that the listing does not cover
- High-traffic angles the data suggests but copy does not foreground

**7. Visual Content Gaps**

- Weak or missing context in existing images
- Absent image types (use-case, comparison, real-world scale)

### Required Output Format (Phase 2)
Produce the analysis using this structure. Be specific and quote or paraphrase extracted fields and reviews where useful. The final block is **your opportunity synthesis**; avoid imperatives that sound like "change this competitor's bullet five" or any direct edit list for the ASIN being studied.

```
Competitor ASIN: [ASIN] | Brand: [brand] | BSR: [rank] | Rating: [x.x] ([N] reviews)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ WHAT THIS COMPETITOR DOES RIGHT

Content Strategy:
  - Title formula: [describe the pattern and keyword placement]
  - Bullet priority: [what each bullet leads with and the logic behind the order]
  - Standout phrasing: [specific language worth noting or borrowing]
  - A+ modules: [which are used and what they emphasize]

Keyword Placement:
  - Primary (title, first 80 chars): [keywords]
  - High-weight (Bullets 1–2): [terms]
  - Long-tail (Bullets 3–5): [terms]
  - Supplementary (description/A+): [terms]

Visual Strategy:
  - Image sequence: [describe the narrative arc across images]
  - Infographic highlights: [what data/specs are called out]
  - Video: [approach if present, or "none"]

Buyer-Validated Selling Points:
  - "[specific insight from high-helpful reviews]"
  - "[another insight]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🕳️ MARKET GAPS (OBSERVED ON THIS COMPETITOR LISTING)

Content gap: [selling points or use cases their copy under-serves, as seen in extracted text]
Keyword gap: [search intents or terms weakly covered on their page — note buyer language from reviews where possible]
Visual gap: [image or video proof types missing or weak on their gallery or A+]
Unmet buyer needs: [recurring themes from 3-star and mixed reviews, quoted or paraphrased]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 YOUR STRATEGIC OPPORTUNITY POINTS (FOR YOUR BRAND OR ROADMAP — NOT EDITS TO THIS LISTING)

The ASIN above is the competitor under diagnosis. Below, translate gaps into **where you can win**; do not phrase outcomes as rewriting their bullets or their title.

Positioning and messaging whitespace:
  - [Claim, use case, or audience angle they under-own; why it is an opening for you]

Search and intent capture:
  - [Queries or intents implied by reviews or category that their listing weakly serves; how you could own a different slice of demand]

Trust, proof, and creative differentiation:
  - [Proof points, demos, or gallery angles they lack that you could credibly own]

Product, offer, or bundle opportunity:
  - [Unmet needs from reviews that map to a SKU, variant, bundle, warranty, or service on your side — stay factual to extracted complaints and wishes]

Competitive strengths to respect or neutralize:
  - [What this competitor does so well in copy, visuals, or social proof that you should assume as the bar before claiming superiority]
```
