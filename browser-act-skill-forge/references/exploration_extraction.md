# Extraction Capability Exploration

This file is read during Phase 2 execution (extraction capabilities only).

**Goal**: Prioritize discovering API endpoints and confirming data accessibility; when requests cannot be independently constructed, use UI triggers + Network capture to obtain structured responses; fall back to DOM extraction only when both approaches are infeasible.

**Pass Criteria** (API path):
- `fetch()` reproduction verification passes, returned data matches page display (item count, key field values)
- List data pagination works (page 2 data does not duplicate page 1)
- Enumeration parameter acquisition methods are determined (passes even if some are marked `[collection failed]`)

**Pass Criteria** (UI trigger + Network capture path):
- Target API requests can be stably triggered via URL navigation or UI operations
- Response data read from `network request` is structured with complete field coverage
- Parameters can be injected via URL query string or UI controls
- List data pagination works

**Pass Criteria** (DOM path):
- Target data can be stably extracted from DOM with complete field coverage
- List data pagination works (different data is extracted after pagination)

---

## Exploration Decision Tree

```
Navigate → Read traffic → Found API with target data?
  ├── Yes → Can request be independently constructed?
  │     ├── Yes → Parameters complete?
  │     │     ├── Yes ──────────────→ [API Verification]
  │     │     └── No → [UI Completion] → [API Verification]
  │     └── No ──────────────────→ [UI Trigger + Network Capture]
  └── No → [DOM Extraction]

Verification failure fallback: [API Verification] → [UI Trigger + Network Capture] → [DOM Extraction] → [AI Workflow] → Report obstacle

List type → [Pagination Verification]
All paths ultimately → [Enumeration Collection]
```

---

## Navigation and Endpoint Discovery

Navigate to the target page, wait for loading to complete, then read traffic:

```
network requests --type xhr,fetch --filter {domain keyword}
```

Extract the most distinctive keyword from the target URL (e.g., `github`, `notion`, `jira`) to cover both the main domain and API subdomains while excluding third-party tracking noise. If no match, remove `--filter` to see all traffic.

When page load traffic yields no match (SPA scenarios), perform one target interaction (search, toggle filter, scroll to load), then read newly added traffic.

After finding candidate endpoints:
```
network request <id>
```
Record request information: URL, method, response structure. Also note whether the initial traffic contains **enumeration prefetch requests** (returning dropdown options, category lists, etc.) for priority use in subsequent enumeration collection. Browser extensions also make requests in the page context — filtering traffic by extension keywords can reveal API data provided by extensions.

---

## Endpoint Evaluation

After obtaining an endpoint, determine two things:

**Transparency**: Can request parameters be independently constructed?
- Parameter names are clear and parameterizable → Transparent, proceed to evaluate parameter completeness
- Contains opaque encoding, dynamic tokens, serialized structures → Opaque, but response data is still structured → Enter **[UI Trigger + Network Capture]** (let the site's own JS handle signing, inject parameters via URL navigation or UI operations, read responses from network)

**Parameter Completeness** (only needs evaluation for transparent endpoints): Do the currently observed parameters cover all settable options in the UI?
- URL contains filter parameters (e.g., `?minPrice=10&maxPrice=50`) → Read directly, usually complete
- **Check page URL and Referer header**: After the first interaction, the current page URL or request's Referer header may already contain the complete parameter name mapping (query string) — decoding it is faster than analyzing the request body
- Endpoint parameters clearly don't match the number of visible controls on the page → Parameters incomplete, enter **[UI Completion]**

Both criteria satisfied → Proceed directly to **[API Verification]**.

---

## UI Completion

Let the page UI help you complete all unknown parameters at once. Goal: **Set all controls to non-default values before triggering search, exposing all parameters in one search.**

1. One eval to scan all form controls, returning a structured map (including checkbox/radio label text and checked state, all select options — for associating enumeration values in step 6):
   ```javascript
   JSON.stringify(Array.from(document.querySelectorAll('input, select, textarea, [role="combobox"]')).map(el => {
     const b = { tag: el.tagName, type: el.type, name: el.name, id: el.id, ph: el.placeholder, val: el.value };
     if (el.type === 'checkbox' || el.type === 'radio') {
       b.checked = el.checked;
       b.label = (el.labels?.[0] || el.closest('label') || el.parentElement)?.textContent?.trim()?.slice(0, 50) || '';
     }
     if (el.tagName === 'SELECT')
       b.opts = Array.from(el.options).map(o => ({ t: o.textContent.trim(), v: o.value }));
     return b;
   }))
   ```
   When control purpose is hard to determine from returned information, supplement with a `screenshot`. Unclear labels don't block progress — proceed directly to step 2; step 6's unique value mapping will automatically associate controls with API parameters.
2. One eval to batch-fill all text/number inputs, **filling each control with a unique value** (e.g., incrementing numbers 1001, 1002, 1003...) to enable precise reverse lookup of which POST parameter corresponds to which control in step 6:
   ```javascript
   const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
   const fills = [ ['{selector1}', '1001'], ['{selector2}', '1002'] /* ...one unique value per control */ ];
   fills.forEach(([sel, val]) => {
     const el = document.querySelector(sel);
     if (el) { setter.call(el, val); el.dispatchEvent(new Event('input', {bubbles: true})); }
   });
   'filled: ' + fills.length
   ```
3. Select non-default options for remaining controls:
   - checkbox / radio: one eval to batch-check (`querySelectorAll('input[type=checkbox]:not(:checked)').forEach(el => el.click())`)
   - Native `<select>`: eval to set `.value` + trigger `change` event
   - Component library dropdowns: try one eval to set value via component instance; **if it fails, use `click` interaction**
   - Range sliders (noUiSlider etc.): eval to batch-set values (e.g., `slider.noUiSlider.set([min, max])`), complete together with other controls in the same round, don't test each slider individually
4. Trigger one complete request (click search / apply / confirm)
5. Read newly added network requests to get the complete parameter structure:
   ```
   network requests --type xhr,fetch --filter {domain keyword}
   network request <id>
   ```
6. Compare requests before and after completion, confirm all parameters are covered; simultaneously use step 1's DOM label/value mapping to associate enumeration values in the POST body (checkbox `val` attribute <-> POST array elements, select option `v` <-> POST field values), producing a "control label -> API parameter name:value" mapping table for direct use in enumeration collection

---

## API Verification

### fetch() Reproduction

Use `eval` in the browser console to directly call the discovered endpoint, confirming data accessibility:

```javascript
const res = await fetch('https://example.com/api/v1/items?page=1&limit=20');
const data = await res.json();
JSON.stringify({ total: data.total, count: data.items?.length, sample: data.items?.[0] })
```

Batch similar verification actions (validity of multiple parameters, reachability of multiple endpoints) into a single eval, drawing conclusions by comparing return differences.

> **DOM Supplement**: If the API response cannot cover all target fields, supplement with DOM extraction for missing fields, combining with the API approach in the capability component.

> **Verification failure fallback**: fetch() returns unexpected results (HTTP error, CORS rejection, response structure doesn't match traffic observation, empty data) → fall back to [UI Trigger + Network Capture].

---

## UI Trigger + Network Capture

Enter this path when API response data is structured and usable, but the request contains dynamic signatures, tokens, or other parameters that cannot be independently constructed. Core idea: let the site's own JS handle signing and authentication, inject business parameters via URL or UI, and read structured responses from network traffic.

### Determine Parameter Injection Method

From requests already observed during the endpoint discovery phase, identify which parameters are business parameters (keywords, page numbers, filter conditions, etc.):

1. **Check page URL**: Does the current page URL's query string contain business parameters? e.g., `?q=keyword&page=2`. Yes → Parameters can be injected via URL navigation
2. **URL doesn't contain business parameters**: Parameters are in the request body, need to be injected via UI control operations (fill search box, select filter conditions, click search)

Both methods may coexist (URL carries some parameters, UI operations supplement the rest).

### Verification: URL Navigation Injection

Construct a URL with business parameters, navigate to it, then read the response from traffic:

```
navigate {target URL with parameters}
```

Wait for loading to complete, then read traffic:

```
network requests --type xhr,fetch --filter {endpoint keyword}
network request <id>
```

Confirm response data matches expectations (field structure, data count). Repeat with modified URL parameters to confirm parameter changes are reflected in the response.

### Verification: UI Operation Injection

Set parameters via UI controls, use HAR recording to precisely capture requests generated by interactions (avoiding filtering from existing traffic):

1. `network har start`
2. Operate UI controls to inject parameters (fill input boxes, select dropdowns, click filters)
3. Trigger request (click search / submit)
4. `network har stop {path}` → Extract the target request's response from HAR
5. Confirm response contains target data

### Record

Record the following information for Skill generation:
- Endpoint URL characteristics (for locating target requests in traffic)
- Parameter injection method (URL pattern / UI operation steps)
- Response structure (field names, types, nesting relationships)

> **Verification failure fallback**: Cannot stably trigger target requests, or response data is incomplete/unusable → fall back to [DOM Extraction].

---

## DOM Extraction

Enter this path when no API endpoint for target data is found, or when API exists but UI Trigger + Network Capture also cannot stably obtain structured data.

When target data is absent from the current DOM, means to make it appear (try in order):
1. Use navigate to open a sub-page/detail page URL containing the data
2. Click a "Show all" / "See more" link that navigates to the data
3. Tab or section navigation within the page
4. Keyboard-driven scroll (e.g., End key) to trigger lazy loading
5. UI scroll commands

Before entering selector extraction, first check whether the page already has embedded structured data (SSR frameworks often embed complete page data as JSON in HTML). When found, extract directly — more stable than selectors and with more complete fields.

### Locate Target Data Elements

Use one eval to batch-test candidate selectors, returning a JSON summary (match count, key attributes of first element, uniqueness) — do not eval them individually:

```javascript
const selectors = ['{candidate1}', '{candidate2}', '{candidate3}'];
JSON.stringify(selectors.map(sel => {
  const els = document.querySelectorAll(sel);
  return { sel, count: els.length, sample: els[0]?.textContent?.slice(0, 50) };
}))
```

Refresh the page and re-test all selectors, comparing before and after results to confirm stability.

### Write Static Extraction Script

After determining selectors, write one eval to complete all field extraction:

```javascript
// [Script] Extract list data
// Extraction selector: '{list item selector}' (batch match + result check: items.length > 0)
const items = Array.from(document.querySelectorAll('{list item selector}')).map(el => ({
  '{field name}': el.querySelector('{sub-selector}')?.textContent.trim(),
  '{field name}': el.querySelector('{sub-selector}')?.getAttribute('{attribute}')
}));
JSON.stringify(items)
```

When encountering steps requiring real-time judgment (dynamic loading, conditional rendering) → mark as **[AI Intervention]**, Agent performs visual operations before extraction.

### AI Workflow Alternative (When Static Script Cannot Cover)

If interaction is too complex (CAPTCHA, complex dynamic rendering, visual judgment), organize as AI Workflow.

**Writing Standards**:
1. Each step uses browser-act subcommands in abstract form (no `browser-act` prefix — Agent adds session/flags at runtime), followed by supplementary context, ending with `→ expected result`
2. Element references use only visual descriptions, **CSS selectors and DOM characteristics are forbidden**
   - ✗ `click input[placeholder="搜索"]`
   - ✓ `state` to locate the input box at the top of the page with "Search" placeholder text → `click <index>`
3. Record state checkpoints after key steps (URL, page title, visible element characteristics)
4. Data extraction steps specify which command to use and explain which fields to extract from it: `get markdown` / `eval "{extraction script}"`

> **Verification failure**: DOM selectors are unstable, data cannot be fully extracted, AI Workflow also cannot cover → Report current obstacles and attempted paths to the user, ask about next steps.

---

## Cross-Origin iframe

Enter this sub-path when the target data is rendered inside a cross-origin iframe — identifiable by: `eval` returning a cross-origin access error (`Blocked a frame with origin...`), `iframe.contentDocument` returning `null`, or `state` showing the target elements but `eval` unable to reach them.

**browser-act capability boundary in this context**:

| Command | Works in cross-origin iframe? | Notes |
|---------|-------------------------------|-------|
| `state` | Yes | Reads accessibility tree at OS level; same-origin policy does not apply |
| `click <index>` | Yes | Uses the index returned by `state`; no JS execution required |
| `eval` | No | Blocked by the browser's same-origin policy at the JS layer |

When `state` + `click` cover the full task (purely visual navigation, clicking buttons, reading text already visible in the a11y tree) → use them directly, no CDP connection needed.

When JS execution inside the iframe is required (virtual scroll, DOM querying, reading non-accessible attributes, triggering programmatic events) → use the CDP WebSocket direct-connect path below.

### CDP WebSocket Direct Connect

Chrome exposes every frame as an independent debugging target. Connecting directly to the iframe's target bypasses the browser's cross-origin policy entirely, allowing arbitrary JS execution inside the iframe.

**Step 1 — Enumerate targets and locate the iframe's WebSocket URL**:

```python
import urllib.request, json

targets = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
# Match by a known substring of the iframe's origin or URL
iframe_target = next(t for t in targets if "expected-iframe-domain.com" in t.get("url", ""))
ws_url = iframe_target["webSocketDebuggerUrl"]
```

**Step 2 — Connect and execute JS inside the iframe**:

```python
import asyncio, json, websockets

async def eval_in_iframe(ws_url: str, expression: str):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": expression, "returnByValue": True}
        }))
        resp = json.loads(await ws.recv())
        return resp["result"]["result"]["value"]

result = asyncio.run(eval_in_iframe(ws_url, """
(function() {
    try {
        const items = Array.from(document.querySelectorAll('.item-row')).map(el => ({
            title: el.querySelector('.title')?.textContent?.trim(),
            value: el.querySelector('.value')?.textContent?.trim()
        }));
        return JSON.stringify(items);
    } catch(e) {
        return JSON.stringify({ error: true, message: e.message });
    }
})()
"""))
```

**Decision rule**:
- Use `state` + `click` when: data is already readable from the a11y tree, no JS execution needed.
- Use CDP WebSocket when: data requires JS to extract (virtual scrolling, non-accessible DOM attributes, programmatic event triggers).

**For Skill generation**: encapsulate the CDP connection logic into a standalone `scripts/*.py` file. The script connects to CDP and prints the result directly — it does **not** output a JS string for `eval`. Label the component `CDP Direct` in SKILL.md (see output template) and invoke it with `python scripts/{name}.py {params}` without `eval "$(...)"` wrapping. Requires `websockets` Python package.

> **Verification failure**: CDP target not found at `localhost:9222` → confirm Chrome was started with `--remote-debugging-port=9222`. iframe URL changed between page loads (dynamic token) → re-discover the target via `/json` on each run, never hardcode the WebSocket URL.

---

## Pagination Verification (Required for List Data)

Skip this section for non-list types.

### API Pagination

Check pagination parameters in existing traffic (`page` / `offset` / `cursor` / `next_token`). Can be combined with API verification's fetch reproduction into one compound eval, simultaneously verifying endpoint reachability + pagination effectiveness:

```javascript
// Request pages 1 and 2, confirm data differs
// Page number: page=1 → page=2; Cursor: get {cursor field} from r1 response for second request
const r1 = await (await fetch('{endpoint page 1}')).json();
const r2 = await (await fetch('{endpoint page 2}')).json();
JSON.stringify({
  p1_count: r1.{list field}?.length,
  p2_count: r2.{list field}?.length,
  different: r1.{list field}?.[0]?.{unique identifier} !== r2.{list field}?.[0]?.{unique identifier}
})
```

### URL Pagination

Data is server-rendered in HTML, pagination implemented by navigating to a new URL (common in traditional SSR sites, SEO-friendly sites). Construct a page 2 URL and navigate, confirm different data is extracted:

```javascript
// Extract pagination URL pattern from current page URL or next page link
const next = document.querySelector('{next page link selector}')?.href;  // Element assertion: a tag with href containing pagination parameter
JSON.stringify({ nextUrl: next })
```

Navigate to the next page and re-execute the extraction script, comparing whether data differs.

### DOM Pagination

In-page click controls or scrolling triggers pagination (no navigation to new URL), confirm page 2 data does not duplicate page 1:

```javascript
const btn = document.querySelector('{next page selector}');  // Element assertion: btn exists and text contains "Next"
btn?.click();
// Wait for loading then re-execute extraction script, compare whether data differs
```

### AI Pagination

When scripts cannot reliably determine pagination timing or termination conditions (infinite scroll requiring visual judgment of load completion, inconsistent pagination trigger methods, CAPTCHA interruption, etc.), Agent uses visual operations to drive pagination, confirming page 2 data does not duplicate page 1.

### Record

| Pagination Type | Characteristics / Trigger Method | Record |
|---------|----------------|------|
| API Pagination | `?page=2`, `?cursor=xxx` and other request parameters | Pagination parameter name + type (page number/cursor) + next page value source + termination condition |
| URL Pagination | Pagination navigates to new URL, data in HTML | URL pattern + next page link selector + termination condition |
| DOM Pagination | Click button / `scrollTo()`, no navigation | Trigger method + selector + termination condition |
| AI Pagination | Script cannot determine pagination timing or termination | Visual operation step description + termination signal |

> Network capture path pagination reuses the above mechanisms — pagination trigger method is the same (URL navigation / UI click), only data is read from network traffic instead of DOM or fetch.

---

## Enumeration Collection

During verification, you **must proactively explore** every enumeration control on the page (dropdowns, selectors, radio groups) to determine the **data source and acquisition method** for their options. Don't record specific values — values change, recording acquisition methods is more durable.

Try in order of priority `API > DOM > AI`:

1. **Independently read current page traffic**: `network requests --filter {domain keyword}` to check if there are requests returning enumeration lists. If traffic is empty (page has been navigated away), navigate back to the target page first
2. **Expand/interact with controls**, observe whether async requests are triggered → if new API requests appear, record as above. If the control supports search (input box + dropdown linked), enter keywords to trigger the search API
3. **API endpoint exists** (step 1 or 2 matched) → Record endpoint URL + request method + response structure (field names, value formats), verify whether independent invocation is feasible. When verifying enumeration values: first trigger once from the UI to get real values, then batch-verify with the API — don't guess values first then confirm via UI
4. **Independent invocation not feasible** → Record as hybrid method: which prerequisites need to be obtained from the page + how to obtain them + then how to call the API
5. **No API endpoint** → eval to read option values from DOM (native `<select>` reads `.options`, component library controls try reading instance properties, if fails then expand and read rendered results), record selectors and method
6. **DOM also cannot stably obtain** (multiple attempts failed or controls are highly dynamic) → **[AI] approach**: describe the visual interaction operations the Agent needs to perform

#### Conditional Enumeration (Cascading Linkage)

When cascading relationships are discovered between enumeration controls (options for B only appear/change after selecting A), record the dependency chain (A→B→C) and the acquisition method for each level.

#### Writing to Generated Skill

In the generated SKILL.md's "Enum Parameters" section, provide acquisition approaches for each enumeration layered by `[API]` > `[DOM]` > `[AI]`. `[API]` and `[DOM]` must provide executable JS code; `[AI]` describes the interaction operations the Agent needs to perform (used when code cannot obtain values). Must cover: acquisition method for each enumeration + dependency order when cascading exists. Operation steps also retain inline comments `// {parameter name} enumeration acquisition: ...` to provide in-place context.

Mark uncollectable enumerations with `[collection failed]` (always lowercase) and continue — do not block exploration.
