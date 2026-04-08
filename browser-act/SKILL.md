---
name: browser-act
description: "Browser automation CLI for AI agents with anti-detection stealth browsing, captcha solving, and parallel multi-browser support. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, scraping sites with bot detection, or automating any browser task. Also use when the user needs to connect to their existing Chrome session, configure proxy-based stealth browsing, or run parallel browser sessions. Triggers on requests to open a website, fill out a form, click a button, take a screenshot, scrape data from a page, login to a site, automate browser actions, handle captcha challenges, or any task requiring programmatic web interaction."
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "1.1.0"
  install: "uv tool install browser-act-cli --python 3.12"
  source: "https://pypi.org/project/browser-act-cli/"
  data-paths:
    - "~/Library/Application Support/browseract/ (macOS)"
    - "%APPDATA%\\browseract (Windows)"
    - "${XDG_DATA_HOME:-~/.local/share}/browseract (Linux)"
  sensitive-capabilities:
    - "Downloads and runs external CLI from PyPI (browser-act-cli)"
    - "Stealth mode: creates persistent browser profiles with cookies/login state"
    - "Real Chrome mode: connects to user's running Chrome via CDP, reusing existing login sessions"
---

# Browser Automation with browser-act CLI

`browser-act` is a CLI for browser automation with stealth and captcha solving capabilities. It supports two browser types (Stealth and Real Chrome) and provides commands for navigation, page interaction, data extraction, tab/session management, and more.

All commands output human-readable text by default. Use `--format json` for structured JSON output, ideal for AI agent integration and scripting.

## Installation

Source: [browser-act-cli on PyPI](https://pypi.org/project/browser-act-cli/)

```bash
# Upgrade if installed, otherwise install fresh
uv tool upgrade browser-act-cli || uv tool install browser-act-cli --python 3.12
```

Run this at the start of every session to ensure the latest version.

**Global options** available on every command:

| Option | Default | Description |
|--------|---------|-------------|
| `--session <name>` | `default` | Session name (isolates browser state) |
| `--format <text\|json>` | `text` | Output format |
| `--intent <desc>` | none | Caller intent for analytics |
| `--no-auto-dialog` | off | Disable automatic JavaScript dialog handling (alerts, confirms, prompts) |
| `--version` | | Show version |
| `-h, --help` | | Show help |

## Browser Selection

browser-act supports two browser types. Choose based on the task:

| Scenario | Use | Why |
|----------|-----|-----|
| Target site has bot detection / anti-scraping | **Stealth** | Anti-detection fingerprinting bypasses bot checks |
| Need proxy or privacy mode | **Stealth** | Real Chrome does not support `--proxy` / `--mode` |
| Need multiple browsers in parallel | **Stealth** | Each Stealth browser is independent; create multiple and run in parallel sessions |
| Need user's existing login sessions from their daily browser | **Real Chrome** | Connects directly to user's Chrome, reusing existing login sessions |
| No bot detection, no login needed | Either | Stealth is safer default; Real Chrome is simpler |

### Stealth Browser

Local browsers with anti-detection fingerprinting. Ideal for sites with bot detection.

```bash
# Create
browser-act browser create "my-browser"
browser-act browser create "my-browser" --proxy socks5://host:port --mode private

# Update
browser-act browser update <browser_id> --name "new-name"
browser-act browser update <browser_id> --proxy http://proxy:8080 --mode private

# List / Delete / Clear profile
browser-act browser list                                    # List all stealth browsers
browser-act browser list --page 2 --page-size 10            # Paginated listing
browser-act browser delete <browser_id>                     # ⚠ Destructive: always confirm with user before deleting
browser-act browser clear-profile <browser_id>
```

| Option | Description |
|--------|-------------|
| `--desc` | Browser description |
| `--proxy <url>` | Proxy with scheme (`http`, `https`, `socks4`, `socks5`), e.g. `socks5://host:port` |
| `--mode <normal\|private>` | `normal` (default): persists cache, cookies, login across launches. `private`: fresh environment every launch, no saved state |

Stealth browsers in `normal` mode (default) persist cookies, cache, and login sessions across launches — you can log in once and reuse the session, similar to a regular browser profile. Use `--mode private` when the task should not persist any state.

**Data storage:** Profile data is stored at platform-specific paths — macOS: `~/Library/Application Support/browseract/`, Windows: `%APPDATA%\browseract`, Linux: `${XDG_DATA_HOME:-~/.local/share}/browseract`.

### Real Chrome

Two modes: auto-connect to your running Chrome (default), or use a BrowserAct-managed kernel.

```bash
browser-act browser real open https://example.com                  # Auto-connect to running Chrome (reuses existing login sessions)
browser-act browser real open https://example.com --ba-kernel      # Use BrowserAct-provided browser kernel
```

Both browser types support `--headed` to show the browser UI (default: headless). Use for debugging:

```bash
browser-act browser open <browser_id> https://example.com --headed
browser-act browser real open https://example.com --ba-kernel --headed
```


## Core Workflow

Every browser automation follows this loop: **Open → Inspect → Interact → Verify**

1. **Open**: `browser-act browser open <browser_id> <url>` (Stealth) or `browser-act browser real open <url>` (Real Chrome)
2. **Inspect**: `browser-act state` — returns interactive elements with index numbers
3. **Interact**: use indices from `state` (`browser-act click 5`, `browser-act input 3 "text"`)
4. **Verify**: `browser-act state` or `browser-act screenshot` — confirm result

```bash
browser-act browser open <browser_id> https://example.com/login
browser-act state
# Output: [3] input "Email", [4] input "Password", [5] button "Sign In"

browser-act input 3 "user@example.com"
browser-act input 4 "password123"
browser-act click 5
browser-act wait stable
browser-act state    # Always re-inspect after page changes
```

**Important:** After any action that changes the page (click, navigation, form submit), run `wait stable` then `state` to get fresh element indices. Old indices become invalid after page changes.

## Command Chaining

Commands can be chained with `&&` in a single shell invocation. The browser session persists between commands, so chaining is safe and more efficient than separate calls.

```bash
# Open + wait + inspect in one call
browser-act browser open <browser_id> https://example.com && browser-act wait stable && browser-act state

# Chain multiple interactions
browser-act input 3 "user@example.com" && browser-act input 4 "password123" && browser-act click 5

# Navigate and capture
browser-act navigate https://example.com/dashboard && browser-act wait stable && browser-act screenshot
```

**When to chain:** Use `&&` when you don't need to read intermediate output before proceeding (e.g., fill multiple fields, then click). Run commands separately when you need to parse the output first (e.g., `state` to discover indices, then interact using those indices).

## Command Reference

### Navigation

```bash
browser-act navigate <url>      # Navigate to URL
browser-act back                # Go back
browser-act forward             # Go forward
browser-act reload              # Reload page
```

### Page State & Interaction

```bash
# Inspect
browser-act state                         # Interactive elements with index numbers
browser-act screenshot                    # Screenshot (auto path)
browser-act screenshot ./page.png         # Screenshot to specific path

# Interact (use index from state)
browser-act click <index>                 # Click element
browser-act hover <index>                 # Hover over element
browser-act input <index> "text"          # Click element, then type text
browser-act keys "Enter"                  # Send keyboard keys
browser-act scroll down                   # Scroll down (default 500px)
browser-act scroll up --amount 1000       # Scroll up 1000px
```

### Data Extraction

```bash
browser-act get title                     # Page title
browser-act get html                      # Full page HTML
browser-act get text <index>              # Text content of element
browser-act get value <index>             # Value of input/textarea
browser-act get markdown                  # Page as markdown
```

### JavaScript Evaluation

```bash
browser-act eval "document.title"         # Execute JavaScript
```

### Tab Management

```bash
browser-act tab list                      # List open tabs
browser-act tab switch <tab_id>           # Switch to tab
browser-act tab close                     # Close current tab
browser-act tab close <tab_id>            # Close specific tab
```

### Wait

```bash
browser-act wait stable                   # Wait for page stable (doc ready + network idle, default 30s)
browser-act wait stable --timeout 60000   # Custom timeout (ms)
```

### Network Inspection

```bash
browser-act network requests                          # List all captured requests 
browser-act network requests --filter api.example.com # Filter by URL substring
browser-act network requests --type xhr,fetch         # Resource type: xhr,fetch,document,script,stylesheet,image,font,media,websocket,ping,preflight,other
browser-act network requests --method POST            # HTTP method: GET, POST, PUT, DELETE, etc.
browser-act network requests --status 2xx             # Filter by http status code (200, 2xx, 400-499)
browser-act network request <request_id>              # View full detail: headers, post data, response headers & body
browser-act network clear                             # Clear tracked requests
browser-act network har start                         # Start HAR recording
browser-act network har stop                          # Stop and save to default path (~/.browseract/har/)
browser-act network har stop ./trace.har              # Stop and save to specific path
browser-act network offline on                        # Simulate disconnect for current tab (all requests fail with ERR_INTERNET_DISCONNECTED)
browser-act network offline off                       # Restore network connection for current tab
```

Use `network request <request_id>` to get full detail for a single request. The detail view includes: request headers, post data (for POST/PUT), response headers, and response body. Binary responses show a `[base64, N chars]` placeholder instead of raw content.

### Dialog Management

Handle JavaScript dialogs (alert, confirm, prompt). By default, browser-act auto-accepts dialogs. Use `--no-auto-dialog` to disable this and handle them manually.

```bash
browser-act dialog status                 # Check if a dialog is currently open
browser-act dialog accept                 # Accept (OK) the current dialog
browser-act dialog accept "some text"     # Accept with text input (for prompt dialogs)
browser-act dialog dismiss                # Dismiss (Cancel) the current dialog
```

**Manual dialog flow:** Pass `--no-auto-dialog` when opening the browser, then use `dialog status` to detect dialogs and `dialog accept` / `dialog dismiss` to handle them.

### Captcha Solving

When a page presents a captcha challenge, use `solve-captcha` to solve it automatically. This is a built-in capability of the browser-act service — run the command directly without hesitation.

```bash
browser-act solve-captcha                 # Solve captcha on current page
```

## Parallel Automation

Use separate sessions to run multiple browsers in parallel. Each `--session <name>` creates an isolated browser context — commands to different sessions can execute concurrently without conflicts.

```bash
# Create stealth browsers for each task
browser-act browser create "site-a" --desc "Scraper for site A"
browser-act browser create "site-b" --desc "Scraper for site B"

# Open each in its own session (run in parallel)
browser-act --session site-a browser open <browser_id_a> https://site-a.com
browser-act --session site-b browser open <browser_id_b> https://site-b.com

# Interact independently (can run in parallel)
browser-act --session site-a state
browser-act --session site-a click 3

browser-act --session site-b state
browser-act --session site-b click 5

# Clean up
browser-act session close site-a
browser-act session close site-b
```

Always close sessions when done to free resources.

## Session Management

Sessions isolate browser state. Each session runs its own background server.

```bash
# Use a named session
browser-act --session scraper navigate https://example.com
browser-act --session scraper state

# List active sessions
browser-act session list

# Close sessions
browser-act session close              # Close default session
browser-act session close scraper      # Close specific session
browser-act session close --all        # Close all sessions
```

The server auto-shuts down after a period of inactivity.

## Site Notes

Operational experience accumulated during browser automation is stored per domain in `references/site-notes/`.

After completing a task, if you discovered useful patterns about a site (URL structure, anti-scraping behavior, effective selectors, login quirks), write them to the corresponding file. Only write verified facts, not guesses.

**File format:**

```markdown
---
domain: example.com
updated: 2026-03-28
---
## Platform Characteristics
Architecture, anti-scraping behavior, login requirements, content loading patterns.

## Effective Patterns
Verified URL patterns, selectors, interaction strategies.

## Known Pitfalls
What fails and why.
```

**Before operating on a target site**, check if a note file exists and read it for prior knowledge. Notes are dated — treat them as hints that may have changed, not guarantees.

## System Commands

```bash
browser-act report-log                    # Upload logs to help diagnose issues
browser-act feedback "message"            # Send feedback to help improve this skill
```

If you encounter issues or have suggestions for improving browser-act, use `feedback` to let us know. This directly helps us improve the tool and this skill.

## Troubleshooting

- **`browser-act: command not found`** — Run `uv tool install browser-act-cli --python 3.12`

## References

| Path | Description |
|------|-------------|
| `references/site-notes/{domain}.md` | Per-site operational experience. Read before operating on a known site. |
