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

Browser automation CLI built for AI agents. Get past anti-bot walls, hand off to humans across platforms when stuck, run parallel tasks without cross-contamination, and isolate multiple accounts in independent browsers.

## Why BrowserAct

The browser an AI agent needs has to reach places standard tools can't, let a human seamlessly take over when the agent is stuck, keep parallel tasks from cross-contaminating, and be designed for LLM reasoning — not human-written scripts. **A browser for agents must get four things right.**

**1. Break through blocks — three progressive layers**

1. **Environment layer** — stealth fingerprint spoofing, TLS rotation, proxy switching. The vast majority of blocks never trigger.
2. **Execution layer** — `solve-captcha` auto-solves CAPTCHAs; `stealth-extract` pulls protected pages in one command.
3. **Human layer** — `remote-assist` generates a live URL; the user takes over from any device, and the agent continues seamlessly when done.

**2. Three browser modes — by real-world scenario**

| Mode | Scenario | Key trait |
|------|----------|-----------|
| `chrome` | Reuse local Chrome login state | Profile import or CDP attach |
| `stealth` privacy mode | Frictionless batch scraping without login | Fresh fingerprint per session + proxy rotation, zero residue |
| `stealth` fixed identity | Logged-in accounts · multi-browser parallel | Stable fingerprint + stable IP, stable account identity, not flagged as bots |

**3. Zero-interference concurrency — every agent in its own lane**

- Cross-browser parallel — independent cookies, fingerprints, proxies. Sites cannot correlate them.
- Same-browser multi-session — shared login state, independent execution, tasks don't block each other.
- Privacy mode — fresh fingerprint and empty profile per session, zero residue when done.

**4. Designed for agent reasoning — not human scripts**

- **Compact text output** — indexed text format, several times more token-efficient than JSON or HTML.
- **Indexed interaction** — `state` returns an indexed list; `click 3` / `input 2 "..."`. No DOM parsing required.
- **Semantic memory** — every browser carries a `desc`, matched to tasks by meaning.
- **Concurrency-safe** — session ownership + explicit naming. Multi-agent operation never conflicts.

**Security: confirmation gating** — sensitive operations (browser create / delete, Profile import, proxy changes, security and privacy toggles) require explicit user approval. Prior approvals do not carry over. Enforced at the Skill layer, not a configuration toggle.

---

## And More

- **Better headless** — Default headless without disrupting users; stealth headless that isn't detected.
- **Cross-platform remote handoff** — Any device opens the link to take over, and the agent continues seamlessly.

---

## Install

Tell your AI agent:

> Install browser-act. Skill source: https://github.com/browser-act/skills/tree/main/browser-act . Verify it works after installation.

[Installation details →](docs/installation.md)

---

## Quick Start

```bash
# Extract protected page content (zero config)
browser-act stealth-extract https://example.com

# Full browser automation
browser-act --session my-task browser open <id> https://example.com
browser-act --session my-task state          # See clickable elements
browser-act --session my-task click 3        # Click by index
browser-act --session my-task input 2 "hi"   # Type into a field
```

[More examples and workflows →](docs/quick-start.md)

The agent runs `get-skills` at the start of each session — gets environment state, browser list, and commands in one call:

```bash
browser-act get-skills core --skill-version 2.0.2
```

[How agents discover and use BrowserAct →](docs/skills.md)

---

## Compatibility

**OS:** Windows, macOS, Linux

**Agents:** Claude Code · Cursor · VS Code · OpenCode · OpenClaw · Codex · Gemini CLI — works with any agent that can execute shell commands and load Skills.

---

## What's Free

Almost everything is free. Only two features require payment: managed proxies (Dynamic / Static), and stealth browsers beyond the first 5.

| Feature | Free<br>(No&nbsp;Signup) | Free<br>(Login&nbsp;Only) | Paid |
|---------|:----------------:|:-----------------:|:----:|
| Browser automation, Chrome / Chrome-direct | ✓ | ✓ | ✓ |
| Stealth browser (≤ 5), stealth-extract, solve-captcha, remote-assist, privacy mode, Skill Forge | — | ✓ | ✓ |
| Stealth browser (> 5), Dynamic / Static proxy | — | — | ✓ |

---

## Documentation

Full documentation covers anti-blocking, browser modes, sessions and concurrency, headless and remote handoff, agent design, the Skills system, and the complete command reference.

[Read the full documentation →](docs/README.md)

---

## Also From BrowserAct

### Skill Forge — Your Personal Scraping Engineer

Need to extract data from the same website repeatedly at scale? Don't write scrapers by hand. **Skill Forge** explores a site once, discovers its APIs and data patterns, generates a deploy-ready Skill package, then runs reliably without re-exploration — 500 or 5,000 records through the same stable path.

**Any website. Any data. One command to start:**

> Install browser-act-skill-forge. Skill source: https://github.com/browser-act/skills/tree/main/browser-act-skill-forge . Verify it works after installation.

Then tell your agent what you need:

> *"Forge a Skill that extracts job listings from LinkedIn — title, company, salary, URL. I'll run 300 keywords later."*

[Skill Forge documentation →](docs/skill-forge.md)

### Solutions Catalog

30+ pre-built Skills already generated by Skill Forge, ready to install and run. Covers Amazon, Google Maps, YouTube, Reddit, WeChat, Zhihu, and more.

[Browse the full Solutions Catalog →](solutions/README.md)

### Build Your Own

Can't find what you need above? Generate a custom Skill for **any website** in minutes — no coding required. Just describe what data you want or what action to perform, and Skill Forge handles the rest.

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

## Star History

<a href="https://www.star-history.com/?repos=browser-act%2Fskills&type=date&logscale=&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=browser-act/skills&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=browser-act/skills&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=browser-act/skills&type=date&legend=top-left" />
 </picture>
</a>
