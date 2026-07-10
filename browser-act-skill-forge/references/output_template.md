# Generated Skill File Template

This file is read during Phase 3 execution. Create the output Skill directory according to this specification.

---

## Directory Structure

```
output/{skill-name}/{site-slug}-{capability-slug}/
├── SKILL.md
└── scripts/
    └── {capability-name}.py
```

**Naming Rules**:
- `site-slug`: Target site's primary domain, lowercase, without `www.` and TLD (e.g., `github`, `notion`, `jira`)
- `capability-slug`: Short English description of the capability, kebab-case (e.g., `list-issues`, `create-task`, `search-users`)
- `scripts/*.py` filenames also use kebab-case (e.g., `search-products.py`)
- Only lowercase letters, digits, and hyphens are allowed; no underscores

JS code is encapsulated in Python files under `scripts/`; SKILL.md invokes them via command line. Non-JS content (Network capture steps, AI Workflow, text descriptions) remains inline in SKILL.md.

---

## SKILL.md Template

````markdown
---
name: {site-slug}-{capability-slug}
description: "{Function statement — site name + capability + input/output overview}. Use when user mentions {site name variants}, {data type keywords}, or says {trigger phrases covering casual/formal/abbreviated expressions — as many as needed for full coverage}. Also applies to {adjacent scenarios that aren't obvious but should trigger}."
---

# {site-name} — {capability-name}

> {one-line description: input → output}

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

{what this capability aims to achieve, one sentence}

## Prerequisites

- Target page is already open in the browser: `{full URL of the target page}`
- {e.g., already logged in, user avatar or username is visible on the page} (when login is required)

<!-- Assembly guidance: Prerequisites only describe website state (page opened, logged in, etc.) and dependencies (e.g., browser extensions), not connection methods or browser types — the generation environment ≠ the runtime environment; these are decided by the caller. -->

## Pre-execution Checks

<!-- Assembly guidance: Pre-execution checks only include the following fixed items; do not add custom check steps for browser connection, extension detection, etc. — those are handled by the caller based on prerequisites. -->

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification (when prerequisites include login requirement)

If login status for the target site has been confirmed in the current session → skip this step.

Otherwise: open the target site and observe the page login status:
- Logout/sign-out entry, user avatar, or username exists → logged in, continue execution
- Login/register entry exists with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: {capability description, e.g., "get product list"}

`eval "$(python scripts/{capability-name}.py '{param1}' --param2 {param2})"`

Parameters:
- {param1}: {description}
- --param2: {description}, default {default-value}

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

### API: {capability description, e.g., "submit order"}

`eval "$(python scripts/{capability-name}.py '{param1}' --field1 '{value1}' --field2 '{value2}')"`

Parameters:
- {param1}: {description}
- --field1: {description}
- --field2: {description}

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

### Network Capture: {capability description, e.g., "get search results"} (when parameters are injected via URL navigation)

Parameters are injected via URL; API responses are read from traffic (requests contain dynamic signatures, cannot be fetched directly):

1. `navigate {URL pattern, e.g., https://example.com/search?q={keyword}&page={page}}`
2. `wait stable`
3. `network requests --type xhr,fetch --filter {endpoint keyword}`
4. `network request <id>`

Endpoint characteristic: URL contains `{characteristic path, e.g., /api/search}`

Error handling: When no matching target request is found, check page status (whether blocked by anti-scraping, whether login is needed, whether navigation reached the correct page), then retry once after ruling out issues.

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

### Network Capture: {capability description, e.g., "get filtered results"} (when parameters are injected via UI operations)

Parameters are injected via UI operations; API responses are read from traffic (requests contain dynamic signatures, cannot be fetched directly):

1. {UI operation steps, e.g., fill search box, select filter criteria}
2. Trigger request ({trigger method, e.g., click search button})
3. `wait stable`
4. `network requests --type xhr,fetch --filter {endpoint keyword}`
5. `network request <id>`

Endpoint characteristic: URL contains `{characteristic path}`

Error handling: When no matching target request is found, check page status (whether blocked by anti-scraping, whether login is needed, whether navigation reached the correct page), then retry once after ruling out issues.

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

### DOM: {data area description, e.g., "product list"} (data extraction type)

<!-- Assembly guidance: If the target data is asynchronously injected (browser extensions, lazy loading, etc.), add `wait --selector "{target-selector}" --state attached --timeout {milliseconds}` before the extraction command to wait for target elements to appear before extracting. -->

Extract: `eval "$(python scripts/{extraction-capability-name}.py)"`

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

Pagination: `eval "$(python scripts/{pagination-capability-name}.py)"`

[AI Intervention] {step requiring visual judgment, e.g., "confirm new data has loaded"}:
`screenshot` confirm page change → re-run extraction script

### DOM: {control description, e.g., "submit form"} (operation type)

<!-- Assembly guidance: If form controls are asynchronously rendered (component libraries, extension injection, etc.), add `wait --selector "{control-selector}" --state attached --timeout {milliseconds}` before the fill command to ensure controls are ready. -->

Fill and submit: `eval "$(python scripts/{operation-capability-name}.py '{param1}' --field '{value}')"`

Parameters:
- {param1}: {description}
- --field: {description}

[AI Intervention] {step requiring dynamic judgment, e.g., selecting a dynamic dropdown item}:
{judgment basis: what signal on the page determines the operation}
→ `state` get element index then `click <index>`

### AI Workflow: {capability description, e.g., "browse products and extract prices"} (pure visual, used when static scripts cannot cover)

Each step uses browser-act subcommands (abstract form, Agent adds session/flags at runtime); element references use only visual descriptions, **no** CSS selectors or DOM characteristics; record state checkpoints after key steps:

1. `navigate {url}` → page loaded, title is "{expected-title}"
2. `state` locate {visual description, e.g., "product card area with price labels in the middle of the page"} → `get text <index>`, extract `{field-name}`
3. `scroll down` → wait for more products to load (checkpoint: new products appear)
4. `get markdown` extract `{field-list}` from returned content

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

### Composite: {full capability description, e.g., "get complete product data (API + DOM supplement)"}

<!-- Assembly guidance: Used when a single atomic component cannot provide complete data; can combine across pages (e.g., list page capture + detail page extraction + merge). Combinations that are entirely same-page JS should be merged into one Python script; when navigation or non-JS steps are involved, list steps sequentially, which may include page navigation and loops. Atomic components are still retained for individual invocation. -->

{When all-JS combination}:

`eval "$(python scripts/{composite-capability-name}.py '{param1}' --param2 {param2})"`

Parameters:
- {param1}: {description}
- --param2: {description}

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

{When cross-page / contains non-JS steps combination}:

1. `navigate {page-A URL}` → `wait stable` → `eval "$(python scripts/{capability-A}.py '{param}')"`
2. `network requests --filter {keyword}` → `network request <id>`
3. For each `{item}` from step 1/2:
   a. `navigate {page-B URL pattern}` → `eval "$(python scripts/{capability-B}.py '{item}')"`
4. Merge: associate by `{association-field}`

Output example:
```json
{
  "{field-name}": "{example-value}",  // {description}
  "{field-name}": 0,            // {description}
  "{field-name}": null           // {description}, null when no data
}
```

## Enum Parameters

<!-- Assembly guidance: Group by parameter; priority: API > DOM > AI. What can be obtained via code should not be left to AI. When a single endpoint can cover multiple parameters, merge into one block. -->

[API] {param-name} — `eval "$(python scripts/enum_{param-name}.py)"`

[DOM] {param-name} — `eval "$(python scripts/enum_{param-name}.py)"`

[AI] {param-name}: {description of what requires Agent interaction to obtain, no JS, not encapsulated}

Cascade dependency: {param A} → {param B} (obtain A's value first, then obtain B)

{param-name} [collection failed]: {failure reason}

## Pagination

<!-- Assembly guidance: Required for list-type data; delete this section for non-list types. Only keep types verified during the exploration phase; delete the rest. -->

**API Pagination**: `{pagination-param-name}`, type: `{page-number / cursor}`, start value: `{start-value}`. Next page value source: `{increment / response field path}`. Termination: `{termination-condition}`.

**URL Pagination**: URL pattern `{URL pattern}`, next page link selector: `{selector}`. Termination: `{termination-condition}`.

**DOM Pagination**: Click "{control description}" (`{selector}`), wait for loading then re-extract. Termination: `{termination-condition}`.

**AI Pagination**: Pagination driven by Agent visual operations. Each page: `screenshot` judge status → pagination operation → wait for loading → re-extract. Termination signal: `{termination-signal}`.

## Success Criteria

`{quantifiable condition expression; purely descriptive criteria are prohibited}`

Quantifiable dimension references:
- Data count: `result count >= 1`
- Field completeness: `core field non-null rate = 100%`
- Data consistency: `matches the first N items displayed on the page`
- Operation result: `response status 200 with no error field`

## Session Cleanup

After completing the workflow (normal completion, user abort, or error), close the session to release resources:

```bash
browser-act session close $SESSION
```

Do not close if the user explicitly requests to keep the session open for manual inspection.

---

## Known Limitations

- {e.g., rate limited to 60 requests per minute}
- {e.g., can only query data under own account}

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

<!-- Assembly guidance: Required universal section; output in the current language, only replace {skill-name} and {site}-{capability} in the path -->

Path: `{working-directory}/browser-act-skill-forge-memories/{skill-name}-{site-slug}-{capability-slug}.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
````
<!-- Assembly guidance: The Experience Notes section is a universal template; output in the current language during assembly and replace path variables without modifying semantics. Strategy implementation details (API parameters, pagination methods, etc.) should be inline in their corresponding strategy reference files, not in experience notes. -->


---

## Python Wrapper File Template

Each `scripts/*.py` file follows this structure:

```python
import argparse
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('{positional-param}')                          # {description}
    parser.add_argument('--{named-param}', default='{default-value}')    # {description}
    args = parser.parse_args()

    js = f"""
    (function() {{
      try {{
        // Original JS verified during exploration phase
        // Business parameters injected via f-string: {args.positional_param}, {args.named_param}
        return JSON.stringify({{ /* normal result */ }});
      }} catch(e) {{
        return JSON.stringify({{ error: true, message: e.message }});
      }}
    }})()
    """
    print(js)

if __name__ == '__main__':
    main()
```

<!-- Assembly guidance: Python files only handle parameterized assembly of JS strings. Verified JS goes into the f-string as-is; only business parameters (keywords, page numbers, sort order, etc.) are replaced with argparse parameters. Selectors, field mappings, endpoint URLs, and other fixed values are hardcoded directly in the JS. -->

---

## Filling Specifications

1. **No placeholders left behind**: All `{...}` are replaced with real values; leaving blanks is not allowed
2. **Code must be runnable**: JS strings in `scripts/*.py` must be executable directly in the browser console; Python file execution stdout must be valid JS
3. **Use placeholders for runtime variables**: Keywords, business parameters, pagination offsets, etc. use `{param-name}` and are not hardcoded with specific values. If demonstrating typical usage, provide a separate "Usage Example" block outside the code block with a note, separate from the strategy code itself
4. **Description must be entirely in English** (every word — function statement, trigger phrases, scenarios — even when target users speak Chinese / Japanese / other languages; never embed non-English keywords or phrases). Three parts: function statement (site + capability + I/O), trigger scenarios (keyword-rich English phrases covering site name variants, data keywords; think from the user's perspective: what English words would a user use to mention this capability? Casual, formal, abbreviated — include all real-world phrasings), and scope expansion (adjacent non-obvious triggers). Site name goes first for matching priority; be concise but don't sacrifice keyword coverage — aim for under 1024 characters (the platform limit); no markdown formatting. Write in third person, err toward being "pushy" (Claude tends to under-trigger)
5. **Limitations must be real**: Only document limitations actually encountered during exploration; do not speculate
6. **Add/remove components as needed**: Each API / Network Capture / DOM entry under "Capability Components" is added or removed based on actual exploration results; no fixed quantity is required
7. **Enum priority order**: For the same parameter, list `[API]` first then `[DOM]`; if only one exists, list only that one
8. **Mark collection failures**: Enums that cannot be collected are marked with `{param-name} [collection failed]: {reason}`; do not leave blank
9. **Delete sections as needed**: Delete "Enum Parameters" when there are no enums; delete "Pagination" when not a list type
10. **Enums do not duplicate capability components**: If an enum's retrieval method already exists as a capability component, the Enum Parameters section directly references that component (e.g., "retrieval method: see API component above: {component-name}"); do not duplicate code
11. **Do not include task-specific instance data or origin references**: A Skill is a reusable template; it must not contain specific inputs from this exploration task (search keywords, specific URL lists, usernames, etc.) or reference materials provided by the user (competitor links, third-party tool descriptions, requirement background). When the request was to reproduce capabilities of an existing scraper / SaaS / data extraction platform (e.g. Apify, Octoparse, Bright Data, ScrapingBee, Phantombuster, Diffbot, etc.), the generated Skill must NOT mention the source platform anywhere — no "reproduces X actor", no "equivalent to Y scraper", no source platform name in description / objective / capability titles / comments / examples. The Skill describes the target site capability as a standalone reusable template, as if the source platform was never referenced.
12. **Strip assembly guidance**: All HTML comments (`<!-- ... -->`) in the template are generation guidance and must not appear in the generated Skill output
13. **One JS snippet per .py file**: Each independent `eval` JS snippet is encapsulated as one `scripts/*.py` file, with the filename in kebab-case describing the function
14. **Python only does assembly**: `.py` files do not make network requests, do not operate the filesystem, do not call browser-act; they only output JS strings via `print()`
15. **Parameter names align with business semantics**: argparse parameter names use business terms (keyword, page, sort), not technical terms (selector, xpath)
16. **Output format must be defined**: All components that return data must provide annotated JSON examples, ensuring consistent output format across executions
17. **Component titles accurately reflect implementation method**: API = fetch call; Network Capture = read from browser traffic; DOM = obtained via DOM API; AI Workflow = visual operations; Composite = multi-component orchestration. Labels must match the actual retrieval method; do not mix them up just because the invocation format is the same
18. **JSON output should be compact and efficient**: Key-value pairs are preferred over name/value arrays — e.g., use `{"Brand": "xxx", "Weight": "30 lbs"}` for specifications instead of `[{"name": "Brand", "value": "xxx"}]`, reducing redundant structure
19. **JS code must include error handling**: All JS is wrapped in try/catch, with structural-level validation (selector hits empty, data source unreachable, results empty, page structure does not match expectations, etc.). On error, uniformly return `{"error": true, "message": "..."}` format. Individual field values being null is a normal data characteristic and does not count as an error
20. **Network Capture must guide error handling**: Network Capture steps in the Skill must explain: how to handle when the target request is not found (e.g., wait and retry, check page status), and the basis for judging response anomalies
