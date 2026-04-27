# Proxy Configuration

Stealth browsers support three proxy modes. Real Chrome does not support proxy configuration.

## Proxy Types

| Type | Flag | Description |
|------|------|-------------|
| **Dynamic proxy** | `--dynamic-proxy <region>` | BrowserAct-managed rotating proxy by region code (e.g. `US`, `JP`, `DE`). Simplest option — no external proxy needed |
| **Custom proxy** | `--custom-proxy <url>` | User-provided proxy with scheme. Supports `http`, `https`, `socks4`, `socks5` |
| **No proxy** | `--no-proxy` | Remove proxy from an existing browser (use with `browser update`) |

`--dynamic-proxy` and `--custom-proxy` are **mutually exclusive** — use one or the other, not both.

## Creating a Browser with Proxy

```bash
# Dynamic proxy — just specify a region code
browser-act browser create "my-browser" --dynamic-proxy US

# Custom proxy — provide full URL with scheme
browser-act browser create "my-browser" --custom-proxy http://host:port
browser-act browser create "my-browser" --custom-proxy socks5://user:pass@host:port
browser-act browser create "my-browser" --custom-proxy https://user:pass@host:port
```

## Updating Proxy on Existing Browser

```bash
# Switch to a custom proxy
browser-act browser update <browser_id> --custom-proxy http://proxy:8080

# Switch to a dynamic proxy
browser-act browser update <browser_id> --dynamic-proxy JP

# Remove proxy entirely
browser-act browser update <browser_id> --no-proxy
```

## Available Regions

```bash
browser-act browser regions    # List all available region codes for --dynamic-proxy
```

Region codes follow ISO 3166-1 alpha-2 format (e.g. `US`, `JP`, `DE`, `GB`, `SG`).

## Quick Extraction with Proxy

`stealth-extract` also supports a one-off proxy via `--proxy` (not `--custom-proxy`):

```bash
browser-act stealth-extract <url> --proxy http://host:port
browser-act stealth-extract <url> --proxy socks5://user:pass@host:port
```

This proxy is only used for the single extraction call — it does not persist.

## Custom Proxy URL Format

| Scheme | Example |
|--------|---------|
| HTTP | `http://host:port` |
| HTTPS | `https://host:port` |
| SOCKS4 | `socks4://host:port` |
| SOCKS5 | `socks5://host:port` |
| With auth | `socks5://username:password@host:port` |
