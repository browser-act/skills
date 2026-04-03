---
name: browser-act
description: "Browser automation CLI for AI agents with anti-detection stealth browsing, captcha solving, and parallel multi-browser support. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, scraping sites with bot detection, or automating any browser task. Also use when the user needs to connect to their existing Chrome session, configure proxy-based stealth browsing, or run parallel browser sessions. Triggers on requests to open a website, fill out a form, click a button, take a screenshot, scrape data from a page, login to a site, automate browser actions, handle captcha challenges, or any task requiring programmatic web interaction."
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "1.0.1"
---

# Browser Automation with browser-act CLI

`browser-act` is a CLI for browser automation with stealth and captcha solving capabilities. It supports two browser types (Stealth and Real Chrome) and provides commands for navigation, page interaction, data extraction, tab/session management, and more.

All commands output human-readable text by default. Use `--format json` for structured JSON output, ideal for AI agent integration and scripting.

## Installation

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
| `--version` | | Show version |
| `-h, --help` | | Show help |

## Authentication

Some features require a BrowserAct API key (stealth browsers, captcha solving, etc.). Real Chrome and basic page operations work without one.

**Option 1: Interactive registration (recommended)**

```bash
# Step 1: Get registration URL
browser-act auth login
# Output: registration URL + instructions

# Step 2: Check registration status (single check, not a loop)
browser-act auth poll
# Returns API key on success, or pending status if not yet completed
```

**AI agent flow:** Call `auth login`, present the registration URL to the user, then loop `auth poll` every few seconds until it returns success. When the response indicates less than 10 minutes remaining before expiry, warn the user to complete registration promptly.

```bash
browser-act auth login
# → show URL to user, ask them to register
browser-act auth poll  # check
browser-act auth poll  # retry after a few seconds
browser-act auth poll  # ... until success, expiry, or give up
# ⚠ if remaining time < 10 min, warn the user
```

**Option 2: Direct set**

```bash
browser-act auth set <your_api_key>
```

Get your API key at: https://www.browseract.com

You do **not** need to set up the API key upfront. When a command requires authentication, the CLI returns a structured error with setup instructions.

## Browser Selection

browser-act supports two browser types. Choose based on the task:

| Scenario | Use | Why |
|----------|-----|-----|
| Target site has bot detection / anti-scraping | **Stealth** | Anti-detection fingerprinting bypasses bot checks |
| Need proxy or privacy mode | **Stealth** | Real Chrome does not support `--proxy` / `--mode` |
| Need multiple browsers in parallel | **Stealth** | Each Stealth browser is independent; create multiple and run in parallel sessions |
| Need user's existing login sessions from their daily browser | **Real Chrome** | Connects directly to user's Chrome with existing cookies |
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
browser-act browser list
browser-act browser delete <browser_id>
browser-act browser clear-profile <browser_id>
```

| Option | Description |
|--------|-------------|
| `--desc` | Browser description |
| `--proxy <url>` | Proxy with scheme (`http`, `https`, `socks4`, `socks5`), e.g. `socks5://host:port` |
| `--mode <normal\|private>` | `normal` (default): persists cache, cookies, login across launches. `private`: fresh environment every launch, no saved state |

Stealth browsers in `normal` mode (default) persist cookies, cache, and login sessions across launches — you can log in once and reuse the session, similar to a regular browser profile.

### Real Chrome

Connect to your local Chrome instance (auto-discovers running Chrome with CDP enabled).

```bash
browser-act browser real open https://example.com                  # Auto-connect to your real Chrome with Default profile (existing logins/cookies)
browser-act browser real open https://example.com --ba-kernel      # Use BrowserAct-provided browser kernel
```

Both browser types support `--headed` to show the browser UI. Use for debugging to see what the browser is doing:

```bash
browser-act browser open <browser_id> https://example.com --headed
browser-act browser real open https://example.com  --ba-kernel --headed
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
browser-act input <index> "text"          # Click element then type
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
browser-act wait stable                   # Wait for page stable (doc ready + network idle)
browser-act wait stable --timeout 60000   # Custom timeout (ms)
```

### Network Inspection

Inspect captured network requests across all open tabs and iframes in the browser session. Requests are tracked globally — switching tabs does not reset or filter the captured data. Use `--filter` to narrow results to a specific page or API.

```bash
browser-act network requests                          # List all captured requests (all tabs)
browser-act network requests --filter api.example.com # Filter by URL substring
browser-act network requests --type xhr,fetch         # Filter by resource type
browser-act network requests --method POST            # Filter by HTTP method
browser-act network requests --status 2xx             # Filter by status (200, 2xx, 400-499)
browser-act network request <request_id>              # Full detail with response body
browser-act network clear                             # Clear tracked requests
```

| Option | Description |
|--------|-------------|
| `--filter <url>` | Filter by URL substring |
| `--type <types>` | Resource type, comma-separated (`xhr`, `fetch`, `document`, `script`, `stylesheet`, `image`, `font`, `media`, `websocket`, `ping`, `preflight`, `other`) |
| `--method <method>` | HTTP method (`GET`, `POST`, etc.) |
| `--status <code>` | Status code (`200`), category (`2xx`), or range (`400-499`) |
| `--clear` | Clear all tracked requests (on `network requests` command) |

Use `network request <request_id>` to get full detail for a single request. The detail view includes: request headers, post data (for POST/PUT), response headers, and response body. Binary responses show a `[base64, N chars]` placeholder instead of raw content.

**Scope notes:**
- Requests from **all tabs and iframes** flow into a single tracker (up to 1,000 entries).
- Closing a tab does **not** remove its previously captured requests. Use `network clear` to reset.
- When working with multiple tabs, use `--filter` with a domain or path to isolate the tab you care about.

### Network Simulation

Simulate network disconnection to test offline behavior, error handling, and recovery flows. 

```bash
browser-act network offline on                # Simulate disconnect (all requests fail)
browser-act network offline off               # Restore network connection
```

When offline mode is enabled:
- All network requests fail with `ERR_INTERNET_DISCONNECTED`
- `navigator.onLine` returns `false`
- The browser fires the `offline` event
- Service Worker cached responses and Cache API reads still work (they bypass the network layer)

When offline mode is disabled:
- Network is fully restored
- `navigator.onLine` returns `true`
- The browser fires the `online` event

**Verification example:**

```bash
browser-act eval "navigator.onLine"       # true
browser-act network offline on
browser-act eval "navigator.onLine"       # false
browser-act network offline off
browser-act eval "navigator.onLine"       # true
```

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
