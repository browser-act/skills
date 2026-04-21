---
name: youtube-transcript-analysis-api-skill
description: "This skill helps users extract YouTube video transcripts and perform deep competitive analysis on the content. Agent should proactively apply this skill when users express needs like analyze YouTube video content strategy, perform competitive video content analysis, extract and analyze YouTube subtitles for marketing insights, understand competitor value propositions from their videos, identify target audience from YouTube video content, analyze pain points and needs mentioned in YouTube videos, evaluate competitor CTA strategies in video content, find content gaps in competitor YouTube videos, analyze video narrative structure and hooks, extract key messaging and positioning from YouTube content, benchmark competitor video content quality, research competitor marketing angles through video analysis, identify audience signals and terminology level in videos, analyze emotional tone and persuasion techniques in YouTube content."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# YouTube Transcript Analysis API Skill

## 📖 Brief
This skill provides an end-to-end YouTube video transcript extraction and deep content analysis service. By extracting video transcripts and then systematically analyzing them, users can understand competitors' core value propositions, target audience profiles, pain point strategies, and content gaps — all without manually watching hours of video.

**This skill works in two phases:**
1. **Phase 1 — Transcript Extraction**: Uses BrowserAct API to extract raw transcript data (supports single video and batch modes).
2. **Phase 2 — Deep Analysis**: The Agent performs structured 8-dimension analysis on the extracted transcripts.

## ✨ Features
1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows avoid AI generative hallucinations.
2. **No CAPTCHA issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP restrictions or geo-blocking**: No need to handle regional IP restrictions or geofencing.
4. **Faster execution**: Tasks execute faster compared to purely AI-driven browser automation solutions.
5. **Extremely high cost-efficiency**: Significantly reduces data acquisition costs compared to AI solutions that consume massive amounts of tokens.

## 🔑 API Key Guide
Before running, you must check the `BROWSERACT_API_KEY` environment variable. If it is not set, do not take other actions first; you should ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key yet, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
The Agent should determine the extraction mode based on the user's needs:

### Mode A: Single Video Analysis
Use when the user provides a specific YouTube video URL.

1. **TargetURL**
   - **Type**: `string`
   - **Description**: The URL of the YouTube video to extract and analyze.
   - **Example**: `https://www.youtube.com/watch?v=st534T7-mdE`
   - **Required**: Yes

### Mode B: Batch Video Analysis
Use when the user wants to search and analyze multiple videos by keyword.

1. **KeyWords**
   - **Type**: `string`
   - **Description**: The keyword to search for on YouTube.
   - **Example**: `AI Automation`, `SaaS Marketing`
   - **Required**: Yes

2. **Upload_date**
   - **Type**: `string`
   - **Description**: Filter for the upload date of the videos.
   - **Example**: `This week`
   - **Default**: `This week`

3. **Datelimit**
   - **Type**: `number`
   - **Description**: The number of videos to extract and analyze.
   - **Example**: `3`
   - **Default**: `3`

### Optional Analysis Parameters
These parameters are set by the user's intent, not script arguments:

4. **Analysis Language**
   - **Type**: `string`
   - **Description**: The language the analysis report should be written in. Defaults to the same language as the user's request.
   - **Example**: `Chinese`, `English`

5. **Analysis Focus**
   - **Type**: `string`
   - **Description**: The user may specify an analysis focus. The Agent must dynamically adjust the depth of specific dimensions based on this focus. For example:
     - *Competitor Analysis* -> Deep dive into Dim 7 (Business Model) and Dim 8 (Gaps).
     - *Viral Deconstruction* -> Deep dive into Dim 1 (Hook), Dim 4 (Emotional Arc), and Dim 5 (Viral Drivers).
     - *Audience Research* -> Deep dive into Dim 3 (Persona & Intent) and Dim 4 (Pain Points).
   - **Default**: All 8 dimensions balanced.
   - **Example**: `Competitor Analysis`, `Viral Deconstruction`, `Audience Research`

## 🚀 Invocation Method
The Agent should execute the unified extraction script based on the mode:

**Mode A — Single Video:**
```bash
python -u ./scripts/youtube_transcript_analysis_api.py single "TargetURL"
```

**Mode B — Batch Videos:**
```bash
python -u ./scripts/youtube_transcript_analysis_api.py batch "keywords" "Upload_date" Datelimit
```

### ⏳ Running Status Monitoring
Since this task involves automated browser operations, it may take a long time (several minutes). The script will **continuously output status logs with timestamps** while running (e.g., `[14:30:05] Task Status: running`).
**Agent guidelines**:
- While waiting for the script to return results, please keep an eye on the terminal output.
- As long as the terminal continues to output new status logs, it means the task is running normally. Do not misjudge it as a deadlock or unresponsiveness.
- If the status remains unchanged for a long time or the script stops outputting without returning a result, only then consider triggering the retry mechanism.

### Post-Extraction Workflow
After the script completes and returns transcript data, the Agent must proceed with two additional steps:

**Step 1: Present Video Metadata** — Display the extracted metadata to the user. *(Note: Do NOT output the full raw transcript text in your response, as it is too long. Use it internally for your analysis.)*

**Step 2: Perform Concise 8-Dimension Analysis** — Analyze the transcript across the 8 dimensions. ⚠️ **CRITICAL: The analysis MUST be extremely concise, bullet-point driven, and free of filler words.** Directly state the facts, evidence, and actionable insights without verbose explanations. Use the same language as the user's request.

## 📊 Data Output
After successful execution, the output includes two parts:

### Part 1: Video Metadata
The script returns the following fields for each video:
- `video_title`: The title of the YouTube video
- `video_url`: The direct link to the original video
- `publisher`: The name of the channel publishing the video
- `channel_link`: The URL of the publisher's YouTube channel
- `video_likes_count`: The number of likes the video has received
- `transcript`: The complete extracted transcript/subtitles of the video (used internally for analysis, do not display full text)

### Part 2: 8-Dimension Analysis
After presenting raw data, the Agent must produce structured analysis on the transcript content across the following 8 dimensions:

#### Dimension 1: Content Structure & Hook
Analyze the video's narrative architecture:
- **Opening Hook**: What is the core hook in the first 30 seconds? Quote it and explain the hook logic (e.g., curiosity gap, bold claim).
- **Narrative Framework**: Identify the overall structure (e.g., Problem-Agitate-Solve, Hero's Journey, Listicle).
- **Pacing & Time Allocation**: Proportion of intro vs. core content vs. pitch/CTA.

#### Dimension 2: Core Messaging
Extract the central message:
- **Single Core Viewpoint**: What is the ONE key thesis the video conveys?
- **Supporting Arguments**: How is the viewpoint supported? (Data, analogies, personal experience).
- **Conclusion Clarity**: Is the conclusion clear and memorable?

#### Dimension 3: Audience Persona & Intent
Identify the intended viewer and their mindset:
- **Target Viewer Profile & Level**: Who is this for? (Beginner, Expert) What prior knowledge is assumed?
- **Viewer Intent**: Why are they watching? (To learn a skill, be entertained, make a buying decision, or validate existing beliefs?)

#### Dimension 4: Pain Points & Emotional Arc
Map the emotional journey and problems addressed:
- **Explicit & Implicit Pain Points**: What specific problems are stated or implied? Quote exact words.
- **Emotional Arc**: How does the content shift the viewer's emotion? (e.g., from anxiety/confusion to clarity/relief/empowerment). This emotional shift drives retention and sharing.

#### Dimension 5: Viral & Engagement Drivers
Analyze the spreading mechanism:
- **Shareability Factors**: Why is this video shared? (Controversial takes, highly relatable scenarios, title/thumbnail alignment inferred from script).
- **Memorable/Quotable Phrasing**: Extract unique expressions, catchy concepts, or "aha" moments that stick in the mind.

#### Dimension 6: Evidence & Credibility
Evaluate trust-building elements:
- **Authority Signals**: Data cited, expert references, or professional background mentioned.
- **Social Proof & Empathy**: Real user stories, case studies, or the creator sharing their own past struggles to build rapport.

#### Dimension 7: Business Model & Conversion
Deconstruct the monetization and CTA strategy:
- **Primary Monetization Goal**: What is the underlying business purpose? (Ad revenue, selling a course, affiliate marketing, brand sponsorship, lead generation).
- **CTA Strategy**: What actions are requested? How is urgency or value constructed to drive this action?

#### Dimension 8: Categorized Content Gaps
Identify strategic opportunities by splitting gaps into three layers:
- **Creator's Weaknesses**: Arguments that lack evidence, logical flaws, or poorly explained concepts.
- **Unresolved Viewer Questions**: What specific questions would the audience still have after watching?
- **Industry Whitespace**: What related angles or broader perspectives did the video entirely miss that you could cover?

### Output Format

**For Single Video Analysis:**
```
## Video Metadata
[Present video metadata. DO NOT print full transcript]

## Concise Deep Analysis
*(Output in extremely brief bullet points, max 1-2 short sentences per point)*

### 1. Content Structure & Hook
[Concise bullets]

### 2. Core Messaging
[Concise bullets]

### 3. Audience Persona & Intent
[Concise bullets]

### 4. Pain Points & Emotional Arc
[Concise bullets]

### 5. Viral & Engagement Drivers
[Concise bullets]

### 6. Evidence & Credibility
[Concise bullets]

### 7. Business Model & Conversion
[Concise bullets]

### 8. Categorized Content Gaps
[Concise bullets]

### Key Takeaways
[3 short, actionable strategic insights]
```

**For Batch Video Analysis:**
```
## Video Metadata
[Present all video metadata. DO NOT print full transcripts]

## Concise Individual Analysis
[Repeat the concise 8-dimension analysis for EACH video using brief bullet points]

## Cross-Video Comparative Analysis
[After analyzing all videos individually, provide a comparative summary]:
- Common value propositions: What themes appear across multiple videos?
- Shared target audience: Is there a consistent audience profile?
- Recurring pain points: Which problems are mentioned most frequently?
- Dominant content strategies: What narrative structures and CTA patterns are most common?
- Competitive differentiation: How do different creators/brands position themselves differently?
- Industry content gaps: What topics are consistently missing across all analyzed videos?
```

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

3. **Analysis phase notes**:
   - If the transcript is too short (fewer than 50 words), note this and provide analysis only on available content.
   - If the transcript appears to be auto-generated and contains many errors, note this caveat at the beginning of the analysis.

## 🌟 Typical Use Cases
1. **Competitive content strategy analysis**: Analyze competitors' top-performing videos to understand their messaging and positioning.
2. **Target audience research**: Identify who competitors are targeting and how they speak to them.
3. **Pain point discovery**: Extract customer pain points mentioned in competitor videos for product development insights.
4. **Content gap identification**: Find topics competitors haven't covered well to create differentiated content.
5. **CTA strategy benchmarking**: Understand how competitors drive conversions through their video content.
6. **Value proposition mapping**: Map out what value propositions competitors emphasize most.
7. **Messaging framework extraction**: Learn from competitors' narrative structures and persuasion techniques.
8. **Market trend analysis**: Batch analyze recent videos in a niche to identify emerging themes and shifts.
9. **Content quality benchmarking**: Evaluate the depth and credibility of competitor content.
10. **Marketing copy inspiration**: Extract memorable phrases and emotional hooks for your own content creation.
