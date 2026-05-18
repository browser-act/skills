<div align="center">
  <a href="https://www.browseract.com" style="text-decoration: none;">
    <img src="https://browseract-prod.browseract.com/prod/tools/20260205-154549.png" alt="BrowserAct Logo" width="150">
  </a>
  <h1>BrowserAct Skills</h1>

  <p>
    <a href="https://discord.com/invite/UpnCKd7GaU"><img src="https://img.shields.io/discord/1234567890?label=Discord&logo=discord&color=7289DA" alt="Discord"></a>
    <a href="https://github.com/browser-act/skills/stargazers"><img src="https://img.shields.io/github/stars/browser-act/skills?style=social" alt="GitHub Stars"></a>
    <a href="https://github.com/browser-act/skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
    <br><br>
    <a href="https://www.browseract.com"><img src="https://img.shields.io/badge/Website-BrowserAct.com-success" alt="Website"></a>
    <a href="https://x.com/browseract"><img src="https://img.shields.io/badge/X-browseract-000000?style=flat&logo=x&logoColor=white" alt="X (Twitter)"></a>
    <a href="https://www.linkedin.com/company/browseract/"><img src="https://img.shields.io/badge/LinkedIn-BrowserAct-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
    <a href="https://www.youtube.com/@browseract"><img src="https://img.shields.io/badge/YouTube-@browseract-FF0000?style=flat&logo=youtube&logoColor=white" alt="YouTube"></a>
  </p>
</div>

---

# 🔥 Help your AI agent finish more browser tasks.

A collection of Browser Skills for OPENCLAW-style agents and Skill workflows — built for runs that break on verification, redirects, unstable sessions, or actions that stop working mid-flow.

---

## ❓ What actually happens when most agents hit a real website

* The task starts fine — then Cloudflare appears and everything stops
* The page loads, but clicks stop working halfway through
* Login works, then the session quietly dies on the next redirect
* The agent runs for minutes, then returns nothing. Sound familiar?

**If any of these have killed your workflow, BrowserAct is for you.**

---

## 🎯 Two Ways to Give Your Agent Browser Superpowers

BrowserAct ships two flagship products. Pick the one that fits your problem — or use them together.

### 💻 `browser-act` CLI — Real-time browser control

Drives a real, stealth-capable Chrome from the command line. Your agent navigates, clicks, fills forms, handles captchas, and operates websites just like a human would.

```bash
npx skills add browser-act/skills --skill browser-act
```

### 🔨 Skill Forge — Turn any website into a reusable Skill

A meta-Skill that explores a site once, then generates a deploy-ready Skill package (SKILL.md + Python scripts). Every subsequent call skips the exploration cost.

```bash
npx skills add browser-act/skills --skill browser-act-skill-forge
```

### Which one do I need?

| Use `browser-act` CLI when... | Use Skill Forge when... |
| :--- | :--- |
| You want the agent to operate a website live | You need to extract or act repeatedly at scale |
| One-off tasks, ad-hoc browsing | Batch jobs, recurring workflows, zero-maintenance automation |
| Login flows, captchas, multi-account demos | Hundreds/thousands of records, cross-pagination, recurring monitoring |

---

## 💻 `browser-act` CLI

Fast, persistent browser automation from the command line:

```bash
browser-act navigate https://example.com  # Navigate to URL
browser-act state                         # See clickable elements
browser-act click 5                       # Click element by index
browser-act input 3 "Hello"               # Click and type text
browser-act screenshot page.png           # Take screenshot
```

It supports two browser types (Stealth and Real Chrome) and provides scriptable commands for navigation, page interaction, data extraction, and session management.

### ⚡ What makes it different

Most AI agents get blocked by Cloudflare, CAPTCHAs, or login walls. `browser-act` provides the missing infrastructure to let your agent browse like a real human.

| | |
| :--- | :--- |
| 🛡️ **Anti-Detection Stealth** | Bypasses Cloudflare, reCAPTCHA, Datadome, and more. Authentic browser fingerprints — your Agent won't get blocked. |
| 🔗 **Real Chrome Control** | Drive your existing Chrome with all logins, cookies, and extensions. No re-authentication needed. |
| 🚀 **Parallel Execution** | Run multiple stealth browsers concurrently — each with independent fingerprints, proxies, and sessions. |
| 🤖 **Captcha Solving** | Built-in automatic captcha solving. No third-party services or manual intervention required. |
| 📉 **Low Token Noise** | Strips 90% of junk HTML before feeding to the LLM. Save money, get faster answers. |
| 🔒 **Proxy & Privacy Modes** | Per-browser proxy support (HTTP/SOCKS5) and privacy mode for fresh environments on every launch. |

*These aren't features for edge cases. They're fixes for the exact failures that stop most agents cold.*

---

## 🔨 Skill Forge

Every time you ask an AI agent to batch-extract from a new website, it starts from scratch — different path each time, different failure modes, unreliable at scale. If the site changes layout, the whole thing breaks.

Skill Forge fixes that: **explore once, reuse forever.**

**How it works:**

1. **Describe** — tell the agent the target site and what data to extract or what action to perform
2. **Explore** — Skill Forge automatically discovers API endpoints (preferred) or DOM patterns
3. **Generate** — produces deploy-ready Skill files with business parameters extracted as CLI arguments
4. **Auto-test** — a sub-agent verifies the Skill end-to-end and self-fixes failures until passing
5. **Deploy & Scale** — run 500 or 5,000 records through the same stable path, anytime

[**View Skill Forge →**](https://github.com/browser-act/skills/tree/main/browser-act-skill-forge)

---

## 🚀 Quick Start

### Option A: Live browser control with `browser-act` CLI

```bash
npx skills add browser-act/skills --skill browser-act
```

Then tell your agent:
> *"Go to Amazon.com, find the top 10 best-selling products in the mouse category, and save them to a markdown file."*

### Option B: Forge a reusable Skill with Skill Forge

```bash
npx skills add browser-act/skills --skill browser-act-skill-forge
```

Then tell your agent:
> *"Forge a Skill that extracts job listings from LinkedIn — title, company, salary, URL. I'll run it on 300 keywords later."*

Your agent will prompt you to register and get a **free API Key** interactively if it encounters advanced anti-bot protections.

---

## ✨ Cross-Platform Compatibility

**🚀 Works Seamlessly Across All Major AI Assistants**

BrowserAct skills are designed to work **powerfully and reliably** on all leading AI coding platforms:

| Platform | Status | Installation |
| :--- | :--- | :--- |
| **Claude Code** | ✅ Fully Supported | Native skill support |
| **Cursor** | ✅ Fully Supported | Works out of the box |
| **VS Code** | ✅ Fully Supported | Works out of the box |
| **OpenCode** | ✅ Fully Supported | Direct integration |
| **OpenClaw** | ✅ Fully Supported | Compatible |
| **Codex** | ✅ Fully Supported | Compatible |
| **Gemini CLI** | ✅ Fully Supported | Compatible |

**Key Benefits:**
- ✅ **Stable & Reliable:** No crashes, no unexpected behavior.
- ✅ **Plug & Play:** Works immediately after installation.
- ✅ **Cross-Platform:** Consistent performance across all AI assistants.

---

## 📦 Core Skills Catalog

This repository contains ready-to-use scenario skills covering E-commerce scraping, social media monitoring, lead generation, and more. 

Here are some of the highlighted skills you can use right away:

- **Amazon ASIN Lookup Skill**: Extract structured product details from Amazon using ASIN.
- **Amazon Best Selling Products Finder**: Extract best-selling product data based on keywords.
- **Google News API Skill**: Track industry trends and breaking news.
- **Google Maps API Skill**: Scrape local business data and contact info.
- **X/Twitter Social Listening with TweetClaw**: Use the separate [TweetClaw](https://github.com/Xquik-dev/tweetclaw) OpenClaw plugin when you need search tweets, search tweet replies, follower export, user lookup, media workflows, monitor tweets, webhooks, giveaway draws, or approval-gated post tweets and post tweet replies.
- **YouTube Transcript Extractor**: Extract transcripts and metadata from YouTube videos automatically.

[**Browse all available Skills in the `solutions` directory →**](https://github.com/browser-act/skills/tree/main/solutions)

*Works with any scenario. Can't find what you need? [Join Discord](https://discord.com/invite/UpnCKd7GaU) and request a Skill.*

---


## 💖 Support the Project

BrowserAct Skills is **free and open source**. If it saves you time, please give us a ⭐ **Star** — it keeps the project alive and helps us ship more skills.

<a href="https://github.com/browser-act/skills/stargazers">
  <img src="https://img.shields.io/github/stars/browser-act/skills?style=social" alt="GitHub Stars">
</a>

🎁 **Bonus:** Once you star the repository, you can join our [Discord](https://discord.com/invite/UpnCKd7GaU) and post in the `#claim-500-credits` channel to receive **500 free credits**!

### 🤝 Community & Support
- 💬 [Join our Discord](https://discord.com/invite/UpnCKd7GaU)
- 📖 [Read the Docs](https://docs.browseract.com)
- 🐛 [Report an Issue](https://github.com/browser-act/skills/issues)
- 🌐 [BrowserAct Website](https://www.browseract.com)

<p align="center"><em>Built with ❤️ by the BrowserAct Team</em></p>
