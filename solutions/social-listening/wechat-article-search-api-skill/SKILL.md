---
name: wechat-article-search-api-skill
description: Search public WeChat articles by keyword through the BrowserAct API, with an article limit and a publication-date value or explicit unrestricted value, returning article metadata, source links and available full text. Use for WeChat article discovery, content research and monitoring.
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# WeChat Article Search API

Use the user's keyword, requested quantity (default 10), and publication-date choice. All three Workflow API parameters are required. The literal hyphen `-` is the template's unrestricted-date sentinel. When the user does not restrict dates, send the explicit non-empty value `-`; do not omit publication_date or send an empty value, which may activate the template's historical date default. Ask for the keyword when it is missing; never invent a keyword or date.

## Credentials and runtime

Read `BROWSERACT_API_KEY` from the execution environment. If the user has an existing local BrowserAct credential source, load it securely into this process's environment without printing or copying the secret. Ask the user to configure a local credential only when no authorized source is available; never ask them to paste the key in chat.

The script requires Python and requests. If requests is not installed in the selected Python, invoke it with `uv run --with requests python` without modifying a managed system Python.

## Execute

From this Skill directory:

```bash
# Required date parameter: explicit non-empty unrestricted value.
uv run --with requests python -u scripts/wechat_article_search_api.py "ai 选品" 10 "-"
# Explicit date filter:
uv run --with requests python -u scripts/wechat_article_search_api.py "your keyword" 10 "2026-11-04"
```

The client starts one task and prints its ID, then waits up to 30 minutes. Continue observing while the server reports created/running. Client wait expiration does not mean that the server task failed and does not authorize another POST. Resume the same task:

```bash
uv run --with requests python -u scripts/wechat_article_search_api.py "ai 选品" 10 "-" --task-id "EXISTING_TASK_ID" --timeout 1800
```

Failed, canceled, paused, HTTP errors, an unverified query, absent output or too few usable records produce a nonzero exit. Inspect the existing task before deciding on a new run. Do not retry authentication errors or uncertain task creation automatically. A definite failed task may be retried once for a demonstrated transient cause; a known wrong query or input mapping must be corrected before another run.

## Verify and deliver

A terminal finished status alone is insufficient. Compare requested inputs, the task's actual search step, and the returned records. Parameter echo alone does not prove that the template used those parameters. Verify the keyword and date restriction were applied. The workflow processes whole result pages and can return more than Date_limit, which is a target count rather than a strict server-side ceiling. The client validates records, removes duplicate articles and records missing any whitespace-separated keyword term in the title/body (case-insensitive), and selects the first requested number in server order. It prints a run summary to stderr with server, usable, selected and rejected counts; stdout contains only the selected article JSON. This literal term check does not interpret search operators or prove topic relevance; review article coverage before delivery. Always disclose over-fetching instead of describing a larger server response as exactly the requested size. Do not accept placeholder URLs or present a verification page as article text. Report partial results honestly when the source is exhausted or inaccessible; do not label them a full pass.

Expected article fields are title, full body, publisher/author, publication date, source URL and optional image URL. The legacy template may return `Title`, `Body Content`, `Author`, `Publication Date`, `URL Link`, and `Image URL`; preserve the actual response field names when saving raw output.

Save the task ID, requested inputs, observed execution steps and acceptance result locally without credentials or temporary private access URLs. Return useful article links and a concise description of the verified coverage. Site verification, access restrictions and missing source fields remain possible; this Skill does not guarantee uninterrupted access.
