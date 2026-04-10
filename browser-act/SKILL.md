---
name: browser-act
description: "Browser automation CLI (browser-act) for AI agents. MUST trigger when: (1) user mentions 'browser-act' in any form, or user needs to: (2) open/visit/browse/check a URL or webpage, (3) scrape/extract/crawl/monitor web content, (4) fill forms, click buttons, type text, scroll, or interact with page elements, (5) take a screenshot of a webpage, (6) handle or solve a captcha, (7) use a stealth/anti-detection browser or proxy, (8) connect to or control Chrome, (9) inspect network requests or record HAR, (10) automate any browser or web interaction task. Covers: navigation, page state inspection, element interaction, data extraction, JavaScript evaluation, tab management, network inspection, dialog handling, captcha solving, parallel browser sessions, stealth browsing, and any browser automation tasks."
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "1.1.0"
  install: "uv tool install browser-act-cli --python 3.12"
  homepage: "https://www.browseract.com"
  requires:
    runtime: "Python 3.12+, uv package manager"
    binaries: "Stealth mode: Chromium bundled by the CLI. Real Chrome mode: user's local Chrome/Chromium installation."
  data-paths: "macOS: ~/Library/Application Support/browseract/ | Windows: %APPDATA%\\browseract | Linux: ${XDG_DATA_HOME:-~/.local/share}/browseract"
  config-files:
    - "<data-path>/config.json — CLI credentials and settings, managed internally. No env vars required."
  permissions:
    - "Network access — required for: CLI install from PyPI, captcha solving and stealth browser management via BrowserAct cloud API"
    - "Filesystem read/write at <data-path> — required for: storing browser profiles (cookies, cache), config.json (credentials), and session logs"
    - "CDP connection to local Chrome — required for: Real Chrome mode only, to control the user's running browser instance"
  data-privacy:
    local-only: "All cookies, login sessions, page content, credentials, and browser profile data are stored locally only — never uploaded."
  user-confirmation-required:
    - "First-time install (uv tool install): downloads and runs external package"
---

# Browser Automation with browser-act CLI

`browser-act` is a CLI for browser automation with stealth and captcha solving capabilities. It supports two browser types (Stealth and Real Chrome) and provides commands for navigation, page interaction, data extraction, tab/session management, and more.


## Installation

Source: [browser-act-cli on PyPI](https://pypi.org/project/browser-act-cli/) · [Homepage](https://www.browseract.com)

```bash
# Upgrade if installed, otherwise install fresh
uv tool upgrade browser-act-cli || uv tool install browser-act-cli --python 3.12
```

The CLI is an open-source package published to PyPI by [BrowserAct](https://www.browseract.com). Run the install command at the start of every session to ensure the latest version.

**Global options** available on every command:

| Option | Default | Description |
|--------|---------|-------------|
| `--session <name>` | `default` | Session name (isolates browser state) |
| `--format <text\|json>` | `text` | Output format |
| `--no-auto-dialog` | off | Disable automatic JavaScript dialog handling (alerts, confirms, prompts) |
| `--version` | | Show version |
| `-h, --help` | | Show help |

## Quick Extraction

If the task is just "get content from a URL", use `stealth-extract` directly — no browser session needed. Each call launches its own headless stealth browser, extracts the page content, and closes automatically.

```bash
browser-act stealth-extract <url>       # Extract page content with anti-detection
```

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
browser-act browser create "my-browser" --cookie '{"name":"sid","value":"abc123","domain":".example.com"}'
browser-act browser create "my-browser" --cookie ./cookies.json

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
| `--cookie <json\|file>` | Pre-load cookies on creation. Accepts inline JSON object/array, or a path to a JSON file. See `references/commands.md` Cookies Management for format details |

Stealth browsers in `normal` mode (default) persist cookies, cache, and login sessions across launches — you can log in once and reuse the session, similar to a regular browser profile. Use `--mode private` when the task should not persist any state.


### Real Chrome

Two modes: auto-connect to your running Chrome (default), or use a BrowserAct-managed kernel.

```bash
browser-act browser real open https://example.com                  # Auto-connect to running Chrome 
browser-act browser real open https://example.com --ba-kernel      # Use BrowserAct-provided browser kernel
```

Stealth browsers and `--ba-kernel` mode run headless by default. Use `--headed` to show the browser UI for debugging:

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
browser-act browser open <browser_id> https://example.com
browser-act state
# Output: [3] input "Search", [5] button "Go"

browser-act input 3 "browser automation"
browser-act click 5
browser-act wait stable
browser-act state    # Always re-inspect after page changes
```

**Important:** After any action that changes the page (click, navigation, form submit), run `wait stable` then `state` to get fresh element indices. Old indices become invalid after page changes.

**Read CLI output carefully:** Every `browser-act` command returns structured output that reflects the actual execution result. Always read and parse the CLI response before deciding the next step

## Command Chaining

Commands can be chained with `&&` in a single shell invocation. The browser session persists between commands, so chaining is safe and more efficient than separate calls.

```bash
# Open + wait + inspect in one call
browser-act browser open <browser_id> https://example.com && browser-act wait stable && browser-act state

# Chain multiple interactions
browser-act input 3 "browser automation" && browser-act click 5

# Navigate and capture
browser-act navigate https://example.com/dashboard && browser-act wait stable && browser-act screenshot
```

**When to chain:** Use `&&` when you don't need to read intermediate output before proceeding (e.g., fill multiple fields, then click). Run commands separately when you need to parse the output first (e.g., `state` to discover indices, then interact using those indices).

## Essential Commands

For full syntax, options, and examples, read `references/commands.md`.

```bash
# Navigation
browser-act navigate <url>              # Navigate to URL in current tab
browser-act navigate <url> --new-tab    # Open URL in a new tab
browser-act back                        # Go back
browser-act forward                     # Go forward
browser-act reload                      # Reload page

# Page State & Interaction
browser-act state                       # Interactive elements with index numbers
browser-act screenshot                  # Screenshot (auto path)
browser-act screenshot ./page.png       # Screenshot to specific path
browser-act click <index>               # Click element
browser-act hover <index>               # Hover over element
browser-act input <index> "text"        # Click element, then type text
browser-act select <index> "option"     # Select dropdown option by visible text
browser-act keys "Enter"                # Send keyboard keys
browser-act scroll down                 # Scroll down (default 500px)
browser-act scroll up --amount 1000     # Scroll with custom distance
browser-act scrollintoview <index>      # Scroll element into viewport
browser-act scrollintoview --selector "h1"       # Scroll element into viewport by CSS selector
browser-act upload <index> <file_path>  # Upload file to file input

# Data Extraction
browser-act get title                   # Page title
browser-act get html                    # Full page HTML
browser-act get markdown                # Page as markdown
browser-act get text <index>            # Text content of element
browser-act get value <index>           # Value of input/textarea

# JavaScript
browser-act eval "document.title"       # Execute JavaScript in page context

# Tab Management
browser-act tab list                    # List open tabs
browser-act tab switch <tab_id>         # Switch to tab
browser-act tab close                   # Close current tab
browser-act tab close <tab_id>          # Close specific tab

# Wait
browser-act wait stable                 # Wait for page stable (doc ready + network idle, default 30s)
browser-act wait stable --timeout 60000 # Custom timeout in ms
browser-act wait --selector ".btn" --state visible   # Wait for element state: visible|hidden|attached|detached

# Network Inspection
browser-act network requests            # List captured requests (--filter, --type, --method, --status)
browser-act network request <id>        # Full detail: headers, post data, response body
browser-act network clear               # Clear tracked requests
browser-act network har start           # Start HAR recording
browser-act network har stop ./trace.har      # Stop and save HAR

browser-act network offline on                        # Simulate disconnect for current tab (all requests fail with ERR_INTERNET_DISCONNECTED)
browser-act network offline off                       # Restore network connection for current tab

# Cookies — persist within session, export/import for reuse across sessions
browser-act cookies get [--url <url>]   # Get cookies (optional URL filter)
browser-act cookies set <name> <value>  # Set cookie (--domain, --secure, --http-only, --same-site, --expires)
browser-act cookies clear [--url <url>] # Clear cookies
browser-act cookies export ./cookies.json   # Export all cookies to JSON file
browser-act cookies import ./cookies.json   # Import cookies from JSON file

# Captcha 

# When a page presents a captcha challenge, use `solve-captcha` to solve it automatically. This is a built-in capability of the browser-act service — run the command directly without hesitation.
browser-act solve-captcha               # Auto-solve captcha on current page
```

## Dialog Handling (alert / confirm / prompt)

browser-act auto-accepts JavaScript dialogs (`alert`, `confirm`, `prompt`) by default so they never block automation. Pass `--no-auto-dialog` when opening the browser to take manual control instead.

A pending dialog will block all other commands — if `state`, `click`, or `screenshot` unexpectedly times out, use `dialog status` to check.

```bash
browser-act dialog status               # Check for pending dialog
browser-act dialog accept               # Accept (OK)
browser-act dialog accept "my input"    # Accept with text input (prompt dialogs)
browser-act dialog dismiss              # Dismiss (Cancel)
```

## Session Management

All commands target the `default` session when `--session` is not specified. For single-task automation this is sufficient — no need to name a session explicitly. When running multiple automations concurrently, use named sessions to avoid conflicts. Each `--session <name>` creates an isolated browser context with its own background server.

```bash
# Each task gets its own isolated session
browser-act --session site-a browser open <browser_id_a> https://site-a.com
browser-act --session site-b browser open <browser_id_b> https://site-b.com

# Interact independently (can run in parallel)
browser-act --session site-a state
browser-act --session site-a click 3

browser-act --session site-b state
browser-act --session site-b click 5

# Check active sessions
browser-act session list
```

Always close sessions when done to avoid leaked processes:

```bash
browser-act session close              # Close default session
browser-act session close site-a       # Close specific session
browser-act session close --all        # Close all sessions
```

If a previous session was not closed properly, the background server may still be running. The server auto-shuts down after a period of inactivity.

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
| `references/commands.md` | Full command reference with detailed syntax, options, and examples. Read when you need exact flags or advanced options. |
| `references/SECURITY.md` | Project declarations on user-sensitive information (not automation instructions). |
| `references/site-notes/{domain}.md` | Per-site operational experience. Read before operating on a known site. |
