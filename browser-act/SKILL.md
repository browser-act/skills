---
name: browser-act-cli
description: "Guide for installing and using the browser-act CLI tool — a Python command-line interface for browser automation with stealth browsing, captcha bypass, and multi-browser support. Use this skill whenever the user wants to automate browsers via CLI, control web pages programmatically, scrape websites with anti-detection, manage stealth browser sessions, or interact with page elements from the terminal. Also trigger when users mention browser-act, browser-act-cli, or ask about headless browser automation with Python CLI tools."
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      bins: ["uv"]
      env: ["BROWSERACT_API_KEY"]
env:
  - BROWSERACT_API_KEY
---

# browser-act CLI

`browser-act` is a CLI for browser automation with stealth and captcha bypass capabilities. It supports two browser types (Stealth and Real Chrome) and provides commands for navigation, page interaction, data extraction, tab/session management, and more.

All commands output human-readable text by default. Use `--format json` for structured JSON output, ideal for AI agent integration and scripting.

## Pre-flight: Upgrade Check

Before using browser-act, always ensure the latest version is installed. Run this at the start of every session:

```bash
uv tool upgrade browser-act-cli || uv tool install browser-act-cli --python 3.12
```

This upgrades if already installed, or installs fresh if not yet present.

## Installation

Install via `uv tool install` with Python 3.12:

```bash
uv tool install browser-act-cli --python 3.12
```

After installation, the `browser-act` command is available globally.

## Authentication

Some features require a BrowserAct API key (stealth browsers, captcha bypass, human-assist, etc.). Other features like Real Chrome and basic page operations work without one.

You do **not** need to set up the API key upfront. When a command requires authentication, the CLI will automatically detect the missing key and return a structured error with registration URLs and setup instructions. Simply follow the prompts at that point.

If you want to set up the API key in advance, there are three ways:

**Option 1: Quick setup (interactive)**
```bash
browser-act auth login
# Returns registration URL and session_id
browser-act auth poll <session_id>
# Polls until registration completes, saves API key automatically
```

**Option 2: Manual set**
```bash
browser-act auth set <your_api_key>
```

**Option 3: Environment variable**
```bash
export BROWSERACT_API_KEY=your_api_key
```

Get your API key at: https://www.browseract.com

To verify setup:
```bash
browser-act doctor
```

## Global Options

Every command accepts these options:

| Option | Default | Description |
|--------|---------|-------------|
| `--session <name>` | `default` | Session name (isolates browser state) |
| `--format <text\|json>` | `text` | Output format |
| `--intent <desc>` | none | Caller intent for analytics |
| `--version` | | Show version |
| `-h, --help` | | Show help |

## Browser Types

### Stealth Browser (requires API key)

Cloud-hosted browsers with anti-detection fingerprinting. Ideal for sites with bot detection.

```bash
# List your stealth browsers
browser-act browser list

# Create a stealth browser
browser-act browser create "my-browser" --desc "For scraping"

# Open a URL in stealth browser
browser-act browser open <browser_id> https://example.com

# Open with visible UI (headed mode)
browser-act browser open <browser_id> https://example.com --headed

# Delete a stealth browser
browser-act browser delete <browser_id>
```

### Real Chrome

Connect to your local Chrome instance (uses your existing login sessions).

```bash
# Open URL in real Chrome
browser-act browser real open https://example.com

# Connect via CDP endpoint
browser-act browser real open https://example.com --cdp 9222
browser-act browser real open https://example.com --cdp http://127.0.0.1:9222
```

## Core Workflow

1. **Open**: `browser-act browser open <browser_id> <url>` — opens page in stealth browser
2. **Inspect**: `browser-act state` — returns interactive elements with index numbers
3. **Interact**: use indices from `state` (`browser-act click 5`, `browser-act input 3 "text"`)
4. **Verify**: `browser-act state` or `browser-act screenshot` to confirm result
5. **Repeat**: browser stays open between commands — inspect and interact as needed
6. **Cleanup**: `browser-act session close` when done

```bash
browser-act browser open <browser_id> https://example.com/login
browser-act state
# Output: [3] input "Email", [4] input "Password", [5] button "Sign In"

browser-act input 3 "user@example.com"
browser-act input 4 "password123"
browser-act click 5
browser-act wait stable
browser-act state    # Check result — always re-inspect after page changes
```

After any action that changes the page (click, navigation, form submit), run `wait stable` then `state` to get fresh element indices before further interaction.

## Navigation

```bash
browser-act navigate <url>      # Navigate to URL
browser-act back                # Go back in history
browser-act forward             # Go forward in history
browser-act reload              # Reload current page
```

## Page State & Screenshot

```bash
# Get current URL, title, and interactive elements (with index numbers)
browser-act state

# Take screenshot
browser-act screenshot                    # Save to auto-generated path
browser-act screenshot ./page.png         # Save to specific path
browser-act screenshot --full             # Full page screenshot
```

The `state` command returns a list of interactive elements, each with an **index number**. Use these index numbers with interaction commands below.

## Page Interaction

All interaction commands use the element index from `browser-act state`:

```bash
browser-act click <index>                 # Click element
browser-act hover <index>                 # Hover over element
browser-act type "search text"            # Type into focused element
browser-act input <index> "text"          # Click element then type
browser-act keys "Enter"                  # Send keyboard keys
browser-act select <index> "option"       # Select dropdown option
browser-act scroll down                   # Scroll down (default 500px)
browser-act scroll up --amount 1000       # Scroll up 1000px
```

## Data Extraction

```bash
browser-act get title                     # Page title
browser-act get html                      # Full page HTML
browser-act get html --selector "div.main"  # HTML of specific element
browser-act get text <index>              # Text content of element
browser-act get value <index>             # Value of input/textarea
browser-act get markdown                  # Page content as markdown
browser-act get bbox <index>              # Element bounding box (x, y, w, h)
browser-act eval "document.title"         # Execute JavaScript
```

## Tab Management

```bash
browser-act tab list                      # List open tabs
browser-act tab switch <tab_id>           # Switch to tab
browser-act tab close                     # Close current tab
browser-act tab close <tab_id>            # Close specific tab
```

## Wait

```bash
browser-act wait stable                   # Wait for page stable (doc ready + network idle)
browser-act wait stable --timeout 60000   # Custom timeout (ms)
```

## Captcha Bypass

When a page presents a captcha challenge, use `bypass-captcha` to attempt automatic resolution. This requires an API key.

```bash
browser-act bypass-captcha
```

## Session Management

Sessions isolate browser state. Each session runs its own background server, enabling **parallel browser automation** — multiple sessions can operate simultaneously without interfering with each other.

```bash
# Use a named session
browser-act --session scraper navigate https://example.com
browser-act --session scraper state

# List active sessions
browser-act session list

# Close a session
browser-act session close
browser-act session close my-session
browser-act session close --all
```

### Parallel Automation with Sessions

Use separate sessions to run multiple stealth browsers in parallel. Each session maintains its own browser instance and state independently.

**Example: Scrape 2 sites simultaneously using stealth browsers**

```bash
# Step 1: Create stealth browsers for each task
browser-act browser create "site-a" --desc "Scraper for site A"
browser-act browser create "site-b" --desc "Scraper for site B"

# Step 2: Open each browser in its own session (run these in parallel)
browser-act --session site-a browser open <browser_id_a> https://site-a.com
browser-act --session site-b browser open <browser_id_b> https://site-b.com

# Step 3: Interact with each session independently (can run in parallel)
browser-act --session site-a state
browser-act --session site-a click 3
browser-act --session site-a get markdown

browser-act --session site-b state
browser-act --session site-b click 5
browser-act --session site-b get markdown

# Step 4: Clean up all sessions when done
browser-act session close --all
```

Key points for parallel usage:
- Each `--session <name>` creates an isolated browser context
- Commands to different sessions can execute concurrently without conflicts
- Use descriptive session names to keep track of parallel tasks
- Always close sessions when done to free resources


## System Commands

```bash
browser-act doctor                        # Run diagnostic checks
browser-act report-log                    # Upload logs to help the browser-act team diagnose issues
browser-act feedback "message"            # Send feedback
```

## Error Handling

- If API key is missing for stealth commands, the CLI prints instructions to set it up
- On failure, commands output error messages in text by default (use `--format json` for structured `{"error": "..."}` responses)
- Session server auto-shuts down after 30 minutes of inactivity (configurable)
- Use `browser-act doctor` to diagnose configuration issues

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `browser-act: command not found` | Run `uv tool install browser-act-cli --python 3.12` |
| `API Key is missing` | Run `browser-act auth set <key>` or set `BROWSERACT_API_KEY` |
| Session server unreachable | Run `browser-act session close --all` and retry |
| Timeout on commands | Increase with `browser-act wait stable --timeout 60000` |
