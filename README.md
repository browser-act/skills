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

## 💻 Core Engine: `browser-act` CLI

The backbone of this repository is the `browser-act` CLI — a powerful browser automation tool with built-in stealth, captcha solving, and multi-browser parallel execution. It supports two browser types (Stealth and Real Chrome) and provides rapid, scriptable commands for navigation, page interaction, data extraction, and session management.

Fast, persistent browser automation from the command line:

```bash
browser-act navigate https://example.com  # Navigate to URL
browser-act state                         # See clickable elements
browser-act click 5                       # Click element by index
browser-act input 3 "Hello"               # Click and type text
browser-act screenshot page.png           # Take screenshot
```

---

## ⚡ What makes `browser-act` CLI different?

Most AI agents get blocked by Cloudflare, CAPTCHAs, or login walls. **`browser-act` CLI** provides the missing infrastructure to let your AI Agent browse like a real human.

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

## ❓ What actually happens when most agents hit a real website

* The task starts fine — then Cloudflare appears and everything stops
* The page loads, but clicks stop working halfway through
* Login works, then the session quietly dies on the next redirect
* The agent runs for minutes, then returns nothing. Sound familiar?

**If any of these have killed your workflow, these skills are for you.**

---

## 🚀 Quick Start

**One-Line Install** — Give your Agent real browser superpowers in 30 seconds.

### Step 1: Install the Skill

```bash
npx skills add browser-act/skills --skill browser-act
```

### Step 2: Run It
Tell your agent:
> *"Go to Amazon.com, find the top 10 best-selling products in the mouse category, and save them to a markdown file."*

Your agent will prompt you to register and get a **free API Key** interactively if it encounters advanced anti-bot protections.

---

## ✨ Cross-Platform Compatibility

**🚀 Works Seamlessly Across All Major AI Assistants**

BrowserAct skills are designed to work **powerfully and reliably** on all leading AI coding platforms:

| Platform | Status | Installation |
| :--- | :--- | :--- |
| **OpenCode** | ✅ Fully Supported | Direct integration |
| **Claude Code** | ✅ Fully Supported | Native skill support |
| **Cursor** | ✅ Fully Supported | Works out of the box |
| **OpenClaw** | ✅ Fully Supported | Compatible |

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
- **YouTube Transcript Extractor**: Extract transcripts and metadata from YouTube videos automatically.

[**Browse all available Skills in the `skills` directory →**](https://github.com/browser-act/skills)

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
