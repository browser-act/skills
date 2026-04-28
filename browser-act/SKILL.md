---
name: browser-act
description: "Browser automation CLI (browser-act) for AI agents. MUST trigger when: (1) user mentions 'browser-act' in any form, or user needs to: (2) open/visit/browse/check a URL or webpage, (3) scrape/extract/crawl/monitor web content, (4) fill forms, click buttons, type text, scroll, or interact with page elements, (5) take a screenshot of a webpage, (6) handle or solve a captcha, (7) use a stealth/anti-detection browser or proxy, (8) connect to or control Chrome, (9) inspect network requests or record HAR, (10) automate any browser or web interaction task. Covers: navigation, page state inspection, element interaction, data extraction, JavaScript evaluation, tab management, network inspection, dialog handling, captcha solving, parallel browser sessions, stealth browsing, and any browser automation tasks."
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "2.0.0"
  install: "uv tool install browser-act-cli --python 3.12"
  homepage: "https://www.browseract.com"
  requires:
    runtime: "Python 3.12+, uv package manager"
    binaries: "stealth: Chromium bundled by the CLI. chrome/chrome-direct: user's local Chrome/Chromium installation."
  data-paths: "macOS: ~/Library/Application Support/browseract/ | Windows: %APPDATA%\\browseract | Linux: ${XDG_DATA_HOME:-~/.local/share}/browseract"
  config-files:
    - "<data-path>/config.json — CLI credentials and settings, managed internally. No env vars required."
  permissions:
    - "Network access — required for: CLI install from PyPI, captcha solving and stealth browser management via BrowserAct cloud API"
    - "Filesystem read/write at <data-path> — required for: storing browser profiles (cookies, cache), config.json (credentials), and session logs"
    - "CDP connection to local Chrome — required for: chrome-direct type only, to control the user's running browser instance"
  data-privacy:
    local-only: "All cookies, login sessions, page content, credentials, and browser profile data are stored locally only — never uploaded."
  user-confirmation-required:
    - "First-time install (uv tool install): downloads and runs external package"
---

# browser-act

Browser automation CLI for AI agents. Runs a full browser engine for web navigation, interaction, data extraction, screenshots, captcha solving, anti-detection fingerprinting, login persistence, proxies, and multi-browser parallel operation.

## Entry Point: guide

Run this at the start of every conversation before using any other browser-act command:

```bash
browser-act guide --skill-version 2.0.0
```

This single call returns everything needed to operate: CLI compatibility status, available browsers with their descriptions, active sessions, core command list, advanced feature summary, and environment-specific directives.

If not installed: `uv tool install browser-act-cli --python 3.12`. Do not proactively upgrade — only upgrade when the user requests it or when guide reports a version error.

### What guide returns

- **CLI** — version, skill compatibility check, headed mode support
- **Browsers** — all configured browsers with id, name, type, and desc (the desc is how you identify which browser to use for a task)
- **Sessions** — currently active sessions
- **Commands** — core command list with usage (this is your command reference — do not rely on hardcoded commands)
- **Advanced** — summary of advanced capabilities (browser management, human collaboration, captcha). When you need detailed instructions, run `browser-act guide advanced` to load the full operations manual
- **Directives** — environment-specific guidance (browser selection rules, blocking version issues, confirmation requirements). Follow these with priority

## Lightweight Extraction (stealth-extract)

When the task is just "get content from a URL", use stealth-extract directly — no browser session needed. Built-in anti-detection fingerprinting reduces captcha triggers.

```bash
browser-act stealth-extract <url>                              # Extract as Markdown (default)
browser-act stealth-extract <url> --content-type html          # Extract HTML
browser-act stealth-extract <url> --dynamic-proxy <region>     # Managed proxy (US, JP, etc.)
browser-act stealth-extract <url> --custom-proxy <url>         # Custom proxy (e.g. socks5://host:port)
```

When the task requires login or page interaction, use the browser workflow below.

## Core Interaction

**Open -> State -> Interact -> Verify** loop:

```bash
# 1. Open browser (reuses if already open, navigates to URL)
browser-act --session <name> browser open <id> <url>

# 2. Inspect page elements
browser-act --session <name> state
# Output: [1] <a /> Learn more, [2] input "Search", [3] button "Go"

# 3. Interact using index numbers from state
browser-act --session <name> input 2 "search keywords" && browser-act --session <name> click 3

# 4. Wait for page to stabilize, then re-inspect (old indices become invalid after page changes)
browser-act --session <name> wait stable
browser-act --session <name> state

# 5. Extract data
#    From network requests (API responses, structured JSON — ideal for tables and lists):
browser-act --session <name> network requests --filter example --type xhr,fetch
browser-act --session <name> network request <id>
#    From DOM (rendered page content — ideal for static pages or when no API exists):
browser-act --session <name> get markdown
browser-act --session <name> get text <index>
```

**Command chaining**: Use `&&` to chain commands when you don't need intermediate output. Run commands separately when you need to parse output first (e.g., `state` to discover indices).

## Core Commands

The command list is provided dynamically by `guide` output — refer to the **Commands** block from your last `guide` call. For commands beyond that list, run `browser-act --help` to see all available commands.

## Language

Reply in the user's language when presenting task details or results.

## Error Handling

Read the error output when a command fails — it usually includes the solution. Follow the suggested fix instead of retrying blindly.

## Diagnostics

```bash
browser-act report-log              # Upload logs to help diagnose issues
browser-act feedback "message"      # Send improvement suggestions
```
