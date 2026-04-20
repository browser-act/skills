# Command Reference

Full command syntax, options, and examples for browser-act CLI. For the core workflow and browser selection, see `SKILL.md`.

## Navigation

```bash
browser-act navigate <url>              # Navigate to URL in current tab
browser-act navigate <url> --new-tab    # Navigate to URL in a new tab
browser-act back                        # Go back
browser-act forward                     # Go forward
browser-act reload                      # Reload page
```

## Page State & Interaction

```bash
# Inspect
browser-act state                                # Interactive elements with index numbers
browser-act screenshot                           # Screenshot (auto path)
browser-act screenshot --full                    # Screenshot for full page
browser-act screenshot ./page.png                # Screenshot to specific path

# Interact (use index from state)
browser-act click <index>                        # Click element
browser-act hover <index>                        # Hover over element
browser-act input <index> "text"                 # Click element, then type text
browser-act select <index> "option"              # Select dropdown option by visible text
browser-act keys "Enter"                         # Send keyboard keys
browser-act scroll down                          # Scroll down (default 500px)
browser-act scroll up --amount 1000              # Scroll up 1000px
browser-act scrollintoview <index>               # Scroll element into viewport by index
browser-act scrollintoview --selector "h1"       # Scroll element into viewport by CSS selector
browser-act upload <index> <file_path>           # Upload file to a file input element
```

## Data Extraction

```bash
browser-act get title                     # Page title
browser-act get html                      # Full page HTML
browser-act get text <index>              # Text content of element
browser-act get value <index>             # Value of input/textarea
browser-act get markdown                  # Page as markdown
browser-act stealth-extract <url>         # Standalone: extract content from URL using stealth mode (bypasses bot detection)
```

## JavaScript Evaluation

```bash
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
browser-act wait stable                                # Wait for page stable (doc ready + network idle, default 30s)
browser-act wait stable --timeout 60000                # Custom timeout (ms)
browser-act wait --selector "#spinner" --state hidden  # Wait for element to disappear
browser-act wait --selector ".content" --state visible # Wait for element to become visible
browser-act wait --selector ".btn" --state attached    # Wait for element to attach to DOM
```

| `--state` value | Description |
|-----------------|-------------|
| `visible` | Element is visible in the viewport |
| `hidden` | Element is not visible (`display:none`, `visibility:hidden`, or detached from DOM) |
| `attached` | Element is attached to the DOM |
| `detached` | Element is removed from the DOM |

## Network Inspection

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

## Dialog Management

Handle JavaScript dialogs (alert, confirm, prompt). By default, browser-act auto-accepts dialogs. Use `--no-auto-dialog` to disable this and handle them manually.

```bash
browser-act dialog status                 # Check if a dialog is currently open
browser-act dialog accept                 # Accept (OK) the current dialog
browser-act dialog accept "some text"     # Accept with text input (for prompt dialogs)
browser-act dialog dismiss                # Dismiss (Cancel) the current dialog
```

**Manual dialog flow:** Pass `--no-auto-dialog` when opening the browser, then use `dialog status` to detect dialogs and `dialog accept` / `dialog dismiss` to handle them.

## Cookies Management

Manage browser cookies independently. Cookies persist within the browser session and can be exported/imported for reuse across sessions.

```bash
browser-act cookies get                                   # Get all cookies for the current page
browser-act cookies get --url https://example.com         # Get cookies filtered by URL
browser-act cookies set <name> <value>                    # Set a cookie with name and value
browser-act cookies set sid abc123 --domain .example.com --secure --http-only --same-site Lax --expires 2026-12-31
browser-act cookies clear                                 # Clear all cookies
browser-act cookies clear --url https://example.com       # Clear cookies for a specific URL
browser-act cookies export ./cookies.json                 # Export all cookies to JSON file
browser-act cookies import ./cookies.json                 # Import cookies from JSON file
```

| Option | Applies to | Description |
|--------|-----------|-------------|
| `--url <url>` | `get`, `clear` | Filter cookies by URL |
| `--domain <domain>` | `set` | Cookie domain (e.g. `.example.com`) |
| `--secure` | `set` | Mark cookie as secure (HTTPS only) |
| `--http-only` | `set` | Mark cookie as HttpOnly (not accessible via JavaScript) |
| `--same-site <Strict\|Lax\|None>` | `set` | SameSite attribute |
| `--expires <date>` | `set` | Expiration date (ISO 8601 format, e.g. `2026-12-31`) |

**Cookie JSON format** (used by `export`, `import`, and `--cookie` on `browser create`). Note: `expires` in JSON is a Unix timestamp (seconds), while the CLI `--expires` option accepts ISO 8601 date strings.

```json
[
  {
    "name": "sid",
    "value": "abc123",
    "domain": ".example.com",
    "path": "/",
    "secure": true,
    "httpOnly": true,
    "sameSite": "Lax",
    "expires": 1798761600
  }
]
```

## Captcha Solving

When a page presents a captcha challenge, use `solve-captcha` to solve it automatically. This is a built-in capability of the browser-act service — run the command directly without hesitation.

```bash
browser-act solve-captcha                 # Solve captcha on current page
```
