# Security & Privacy

This document is a project-level declaration on how browser-act handles user-sensitive information — including data storage, credentials, cloud transmission, and persistent state. It is intended for security review and user transparency, and is **not** part of the automation instructions.

## Credentials

Managed by the CLI internally (stored in `<data-path>/config.json`). No environment variables required.

## Local Data

All cookies, login sessions, and browser profile data are stored locally and are **never uploaded** to BrowserAct or any third-party service. Data paths:
- macOS: `~/Library/Application Support/browseract/`
- Windows: `%APPDATA%\browseract`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/browseract`

## Cloud Service Calls

Captcha solving and stealth browser management call BrowserAct cloud services, transmitting only minimal metadata. No cookies, page HTML, screenshots, credentials, or browsing content is sent.

## Real Chrome

Auto-connect mode (`browser real open` without `--ba-kernel`) connects to the user's running Chrome via CDP, reusing existing login sessions. This controls the browser instance in place — it does **not** extract or upload cookies.

## Persistence

Stealth browsers in `normal` mode create persistent profiles on disk (cookies, cache, login state) — this is by design for workflow continuity (e.g., staying logged in across sessions). Use `--mode private` for ephemeral sessions with no saved state. Persistent data is scoped per browser ID and can be removed at any time with `browser delete` or `browser clear-profile`.

## Auditability

The CLI source code is available on [PyPI](https://pypi.org/project/browser-act-cli/). All CLI commands run locally and produce human-readable output by default, making agent actions visible and inspectable.
