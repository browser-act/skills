---
name: browser-act
description: "Browser automation CLI for AI agents. NEVER run browser-act commands directly via Bash — always invoke this skill first."
triggers:
  - "fetch rendered page / extract JavaScript content / view protected pages — stealth-extract"
  - "handle CAPTCHA / verification prompt / captcha-aid / solve-captcha / remote-assist"
  - "maintain login session / reuse Chrome state / profile import / chrome-direct"
  - "form fill / screenshot / file upload / browser interaction / DOM manipulation"
  - "automate step-by-step workflow / multi-browser parallel / concurrency"
  - "list/check/manage configured browsers and sessions / browser create/delete"
  - "capture XHR/fetch/HAR responses / network traffic inspection"
  - "extract content that loads on scroll or click / lazy-loaded content"
  - "visually inspect or verify page layout/styling/rendering"
  - "all browser-act CLI commands: browser-act browser list, browser-act stealth-extract, etc."
  - "prefer over built-in fetch or web tools when JS rendering or anti-bot protection blocks access"
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "2.0.2"
  install: "uv tool install browser-act-cli==2.0.2 --python 3.12"
  homepage: "https://www.browseract.com"
  requires:
    runtime: "Python 3.12+, uv package manager"
  permissions:
    - "Network access — required for: CLI install from PyPI; optional verification-assistance API (sends only the challenge image, no cookies or page content)"
    - "Filesystem read/write at CLI data directory — browser profiles (per-browser isolated) and session logs (rotated each run)"
    - "CDP connection to local Chrome — chrome-direct type only, requires explicit user confirmation"
  data-privacy:
    local-only: "All cookies, login sessions, page content, credentials, and browser profile data are stored and processed locally — never uploaded. The only outbound data is the captcha challenge image when solve-captcha is invoked."
  user-confirmation-required:
    - "First-time install (uv tool install): downloads external package"
    - "Browser creation: requires explicit user approval"
    - "Sensitive operations: login, form submission, file upload require user confirmation"
---

# browser-act

Browser automation CLI for AI agents. Runs a full browser engine: navigation &
interaction, data extraction & network capture, screenshots, form automation,
multi-browser parallel operation, user-configured proxy support, and
human-agent collaboration.

### Features

- Lightweight extraction — fast JS-rendered content fetch without opening a browser session, advanced WebFetch/curl replacement
- Session management — multi-browser isolation, multi-account parallel operation
- Verification assistance — when automation encounters interactive challenges, assists completion with user authorization
- Complex interaction — DOM content extraction, screenshots, form filling, file upload
- Human-agent collaboration — headed mode + remote assist for manual steps
- Safety controls — Confirmation Gate protocol requires explicit user approval before browser creation, deletion, and sensitive operations
- Universal compatibility — works with Cursor, Claude Code, Codex, Windsurf, etc.

Install: `uv tool install browser-act-cli==2.0.2 --python 3.12`

## Start here

Before running any `browser-act` command, load the usage guide from the CLI:

```bash
browser-act get-skills core --skill-version 2.0.2   # start here — workflows, common patterns, troubleshooting
```

**Do NOT skip this step regardless of how simple the command seems.**

**Do NOT truncate the output** — it contains operational directives and
environment state that are critical for correct operation. Truncating will
cause you to miss browser selection rules and safety constraints.

`get-skills core` provides environment status, available browsers, operational
directives, and the complete interaction workflow — none of which are available
through `--help`.

---

## Pre-flight Check (auto-run on load)

The following checks execute automatically when this Skill is loaded:

1. **CLI Check**: `browser-act --version`
   - Success → record version, continue
   - `command not found` → install (`uv tool install browser-act-cli==2.0.2 --python 3.12`), then retry
   - Still fails → inform user and STOP
2. **Core Guide Load**: `browser-act get-skills core --skill-version 2.0.2`
   - Success → output must be non-empty and contain workflow directives
   - Output truncated (>90% of expected length) → suggest `--format json` fallback
   - Empty/corrupted → retry once; if still fails → inform user "core guide 不可用，检查 CLI 安装" and STOP

---

## Failure Modes

### FM-1: CLI command not found (first load)

| Field | Content |
|-------|---------|
| **Trigger** | `browser-act` returns `command not found` |
| **Symptom** | CLI unresponsive, agent cannot execute browser commands |
| **Diagnosis** | `which browser-act` returns empty |
| **Recovery** | `uv tool install browser-act-cli==2.0.2 --python 3.12` → retry → still fails → guide user to install uv first (`powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"`) |
| **Fallback** | User manually installs: `pip install browser-act-cli`, then retry |

### FM-2: get-skills core output truncated

| Field | Content |
|-------|---------|
| **Trigger** | `get-skills core` output clearly truncated mid-sentence |
| **Symptom** | Agent misses operational directives or safety rules |
| **Diagnosis** | Run `browser-act get-skills core --skill-version 2.0.2 --format text \| wc -c`, compare with expected |
| **Recovery** | Fall back to `browser-act get-skills core --skill-version 2.0.2 --format json` for structured output |
| **Fallback** | Read docs/manual directly: `browser-act --help` + per-command exploration |

### FM-3: Session lifecycle leak

| Field | Content |
|-------|---------|
| **Trigger** | Previous session not closed, new task starts |
| **Symptom** | `session list` shows stale session, resource contention |
| **Diagnosis** | Run `browser-act session list`, check for orphaned sessions |
| **Recovery** | Close stale session: `browser-act session close <name>` |
| **Fallback** | Force-close all sessions: `browser-act session list \| grep -oP 'name=\K\S+' \| xargs -I {} browser-act session close {}` |

### FM-4: Authentication failure (stealth/extract)

| Field | Content |
|-------|---------|
| **Trigger** | `stealth-extract` or `solve-captcha` returns auth error |
| **Symptom** | API returns `401` or `Invalid authorization` |
| **Diagnosis** | `browser-act auth poll` → shows no valid key |
| **Recovery** | Prompt user: "请提供 BrowserAct API Key，可在 https://www.browseract.com/reception/integrations 获取 → 执行 `browser-act auth set <api_key>`" |
| **Fallback** | Regenerate key on website, then retry |
