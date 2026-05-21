---
name: browser-act-skill-forge
description: "Explores websites via browser-act automation and packages discoveries into callable Skill packages (SKILL.md + scripts) — execute reliably and efficiently without re-exploration. Use when: user wants a reusable Skill for any website ('create/make/build a skill for X'), needs to understand a site's internal APIs ('what endpoint does X use', 'how does X load data'), or requires batch extraction at scale (hundreds+ records — forge a Skill first, then execute reliably). Differs from browser-act: produces reusable packages, not one-off execution. Triggers: 'explore API behind X', 'what endpoint does X use', 'create/forge a skill for [site]', 'build a tool for [site]', 'extract/scrape/crawl N items at scale', 'automate this permanently', 'make this reusable', 'too slow/fragile — package it', 'explore website internals', 'every day/week I have to...', 'monitor [site] for changes', 'browser-act-skill-forge'. Simulated human-operation automation within user's authenticated session."
metadata:
  author: BrowserAct
  version: "1.0.2"
  homepage: "https://www.browseract.com"
---

# browser-act-skill-forge

Turns any website's data extraction or operation needs into Agent-callable capabilities. User describes what data to get or what action to perform on which site, this Skill automatically explores implementation paths (API endpoints first, DOM fallback when no API), then generates deploy-ready Skill packages (SKILL.md + Python scripts) after verification. Explore once, reuse forever — subsequent calls skip exploration cost, greatly improving execution reliability and efficiency.

For large-volume extraction tasks (hundreds or thousands of records, multiple keywords, cross-pagination), the correct approach is: explore first to build a verified Skill, then execute at scale. Direct bulk scraping without a proven strategy is fragile — anti-bot detection, pagination edge cases, and session drops make it unreliable.

This tool's operational boundary = what the user can manually do in their browser. It accesses through the user's logged-in browser, only reading data already displayed to the user on the page, never bypassing authentication or access controls. Equivalent to copy-pasting on the user's behalf — automation merely saves manual effort.

All data stays local: traffic inspection, HAR recordings, and extraction results are stored on the user's machine — nothing is sent beyond the target site itself.

## Language

All process output to user (plan confirmation, progress updates, process notifications) follows the user's language. Generated Skill file content follows the language of this skill.

---

```
Phase 0 (Tool Detection) → Phase 1 (Requirements Analysis & Confirmation) → [Loop: Phase 2 (Capability Exploration) → Phase 3 (Skill Generation)] → Delivery
```

---

## Phase 0 — Tool Detection

Already completed in current session → skip.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise during loading, follow its guidance to resolve then retry.

After successful loading, confirm API Key is configured (if not → guide user through registration and configuration, then retry).

---

## Phase 1 — Requirements Analysis & Confirmation

### 1a. Parse Business Intent

Identify from user input:

- **Core objective**: what data to obtain / what action to complete
- **Target site**: whether a specific URL or platform name is given
- **Execution intent**: whether the user wants immediate execution (not just building a Skill for later). Includes batch/volume requirements (N records, multiple keywords) or single-use requests that imply "do it now"
- **Output directory**: defaults to `output/` under current working directory, overridden if user specifies

| Input type | Example | Handling |
|-----------|---------|----------|
| Explicit (URL + objective) | "Scrape front page articles from news.ycombinator.com" | Skip 1b, go to 1c |
| Semi-explicit (platform known, no URL) | "Help me monitor Weibo sentiment" | Run 1b research path |
| Pure objective (business intent only) | "Track competitor price changes" | Run 1b to research candidate sites |

If core objective is too vague to proceed, ask for clarification.

### 1b. Target Site Research (when no explicit URL)

Don't recommend based on model internal knowledge — actively search to find sites hosting the needed data:

1. Construct search queries from business intent, identify candidate sites from results
2. Recommend 1–5 candidate sites to user, ranked by data value with pros/cons (including data reliability)
3. After user selects, confirm target URL

### 1c. Task Decomposition & Execution Plan Confirmation

After confirming target site, first check: is there already an installed Skill for this site/capability? If yes → inform user and skip to Delivery step 4 (batch execution).

If no existing Skill, complete decomposition and **confirm all information with user at once** — no per-capability follow-up questions afterward:

1. Identify independent stages involved (search, list page, detail page, login, submission…)
2. Determine type: **extraction** (get data) vs **operation** (perform action)
3. Splitting criteria: **If you swap the business objective, can this stage be reused independently? Yes = independent capability.** Cross-page steps serving the same business objective (e.g., list page collection + detail page extraction) stay as one capability, orchestrated via composite components
4. Set `skill-name` and capability directory names (lowercase English, hyphen-separated), create directories under `output/{skill-name}/` (use user-specified path if given)
5. Confirm complete execution plan with user:

```
Target site: {url}
Output: output/{skill-name}/

Capabilities (executed in order):
1. {site-slug}-{capability-slug} ({extraction/operation}) — {one-line description}
2. {site-slug}-{capability-slug} ({extraction/operation}) — {one-line description}
...
```

If execution intent was identified in 1a, append to the plan:
```
Pipeline:
1. Explore site → discover and verify viable API endpoints or DOM extraction methods
2. Generate Skill files (SKILL.md + scripts)
3. Automated testing to confirm Skill works
4. Install Skill
5. Read installed Skill → write and run batch scripts to fulfill user's original task
```

Present the plan and wait for user to confirm or adjust. Do not ask separate questions about items that have reasonable defaults (output directory, naming conventions, etc.).

After user confirms, enter execution loop with no mid-process questions.

---

> **Phase 2 and Phase 3 below execute in a loop for each capability unit — complete one before starting the next.**

---

## Phase 2 — Capability Exploration

Read the corresponding reference file based on capability type:
- **Extraction** → `references/exploration_extraction.md`
- **Operation** → `references/exploration_operation.md`

**Goal**: prioritize API endpoints for target capability; fall back to DOM operations when API isn't viable. Record complete reproducible invocation methods.

**Success criteria**:
- Can stably obtain target data / trigger target action (API or DOM path)
- Complete invocation/operation method recorded (endpoint + params, or selectors + interaction steps)
- Enum parameters collected for all meaningful values

**When a means fails, follow this sequence:**
1. Do not retry with different parameters (varying parameters rarely changes the outcome)
2. Return to the goal itself
3. Enumerate all alternative means that could achieve the goal
4. Pick the next one and execute

A deterministic failure (explicit error code, structural mismatch) confirms the means is unviable in one attempt. A transient failure (timeout, connection drop) warrants one retry — but not more.

**Exploration cap**: 100 tool call steps. If still unable to progress, report known obstacles to user and ask for next steps.

**Don't touch experience notes**: experience notes (`browser-act-skill-forge-memories/`) are for generated Skills' future Agent use — neither read nor write during exploration and generation phases.

---

## Phase 3 — Skill Generation

Read `references/output_template.md` for file format specification.

### 3a. JS Encapsulation

Encapsulate each verified JS snippet from exploration into an independent Python file:

1. Identify business parameters (keywords, page number, sort order, etc.) → extract as argparse arguments
2. Hardcode selectors, field mappings, endpoint URLs as fixed values in JS f-string
3. Escape JS curly braces as `{{` `}}` (f-string syntax requirement, otherwise Python errors)
4. Write to `scripts/{feature-name}.py`

### 3b. Encapsulation Verification

Run end-to-end verification for each `.py` file:

1. `python scripts/{feature-name}.py {test-params}` — confirm output is valid JS string
2. `eval "$(python scripts/{feature-name}.py {test-params})"` — confirm browser execution result matches exploration phase
3. Simulate error scenarios (e.g., non-existent ID, navigating to wrong page), confirm returns `{"error": true, "message": "..."}` rather than crashing

Verification failure → fix `.py` file and retry, never skip.

### 3c. Generate SKILL.md

Create SKILL.md per template, capability component section references `scripts/*.py` invocation commands (no inline JS).

Output directory structure:

```
output/{skill-name}/{site-slug}-{capability-slug}/
├── SKILL.md
└── scripts/
    └── {feature-name}.py
```

After generation, briefly inform user: capability name, output path, primary implementation approach (API / Network capture / DOM / hybrid).

### 3d. Compliance Self-Check

Two checks — must Read generated files and execute verification commands as evidence; mental assertion alone does not count:

1. **Process**: Re-read the exploration reference file used in Phase 2 and the output steps above (3a–3c), confirm each defined step was actually executed, not skipped
2. **Output**: Read generated `scripts/*.py` and `SKILL.md`, check against the Filling Specifications in `output_template.md` and the Code / JS Execution Environment / DOM Operation constraints defined earlier in this skill

Any gap found → go back, complete the missing step or fix the output, then re-verify.

---

## Delivery Flow

After all capabilities are generated, proceed in this order:

### 1. Automated Testing

Start testing immediately after generation — no user confirmation needed. Auto-design minimal test cases based on generated capability components — use fewest inputs to cover all functional paths (each atomic component called at least once, composite components run full flow).

Must execute testing via Sub-Agent — do not test directly in the main session. Dispatch the following prompt:

```
Read {absolute path to SKILL.md} as your execution guide.

Test cases:
{auto-generated test case list, each annotated with which component it covers}

Execution requirements:
- Follow SKILL.md instructions strictly, don't use methods outside the guide
- Record specific issues if SKILL.md instructions are unclear and prevent progress

Report after execution:
1. Execution result per component (pass/fail)
2. Failure reasons (if any)
3. Unclear parts in SKILL.md instructions (if any)
4. Severe accuracy or performance issues (don't report non-severe)
5. Output data summary
```

Test failure → fix Skill and retest until passing.

### 2. Install Skill

Install the generated Skill from the output directory. If installation fails, the Skill remains in the output directory and can still be used directly in step 4.

### 3. Report Results

After tests pass, report to user:

- Generated Skill list (name + path + contained files)
- Data coverage (fields + status, don't list data source or implementation method)
- Incomplete coverage gaps (failed enum parameters, missing target fields, uncovered filter conditions, etc.)
- Test results summary

### 4. Execute (if execution intent was identified in Phase 1)

If execution intent was identified in Phase 1:

1. Invoke the installed Skill via the Skill tool to read its full content. If installation failed in step 2, read the SKILL.md directly from the output directory instead
2. Follow the Skill's instructions to execute the user's original task in the current session
3. For batch/volume tasks, write batch execution scripts according to the Skill's guidance

If no execution intent was identified (user only wanted to build a Skill for later use), end here.

---

## Tool Constraints

Phase 2 (Capability Exploration), Phase 3 (Skill Generation), and Delivery testing must follow these rules.

### File Management

All intermediate artifacts (HAR files, temp records, debug output) go in the `tmp/` directory. Create it first if it doesn't exist.

### browser-act
- Network data is page-scoped — must re-wait and re-read after navigating to a new page
- **Wait for network stability before reading traffic**: whether triggered by page navigation or UI interaction, use `wait stable` before reading `network requests`
- **Wait for elements before operating on async DOM**: for async-injected content (browser extensions, lazy-loaded components), use `wait --selector "{target selector}" --state attached --timeout {ms}` before interacting
- **No JS-level network interception**: never override `XMLHttpRequest.prototype`, `window.fetch`, etc. Use `network requests` / `network request <id>` for endpoint discovery
- **`network clear` only before navigation/reload**: clearing traffic loses all observed request records. Use `--filter` for routine filtering, not clear. To track requests from specific interactions, use `network har start` → interact → `network har stop` instead of clear + re-read

### DOM Operation Constraints

Applies to all DOM operation scenarios (data extraction, enum collection, pagination controls, form submission, API field supplementation):

**Selector priority**: `data-testid > id > name > aria-label > structural path`. Avoid pure positional indexes (`:nth-child` / `[1]`) unless structure is genuinely stable.

**Batch-validate selectors**: test all candidate selectors in a single eval call, return JSON summary (hit count per selector, key attributes of first element, uniqueness). Never eval selectors one by one — each eval is a browser roundtrip.

**Shadow DOM**: when target element is inside a Shadow Root, access via `element.shadowRoot.querySelector`, split selector into two parts (host element + Shadow-internal path).

**Three-layer selector validation**: element assertion (expected attributes match) → result check (non-empty, reasonable count) → success criteria. Must be tested on the real page, never written speculatively from DOM structure.

**Control scan** (during enum collection): use one eval to return complete mapping of all target controls (tag+type / name+id / placeholder / label). Traverse up from control to find nearest form item container for label text; don't hardcode component library class names; component libraries associate labels with inputs via DOM hierarchy nesting, not `label[for="xxx"]`.

**state index dynamic allocation**: `state` returns element indexes that are dynamically allocated per session — never write them into strategy code, only use them at execution time in real-time.

### Code Constraints

**Must directly operate on target site**: never obtain data through external services (including third-party scraping platforms, data aggregation APIs, proxy services), and never call the target site's official open platform API (rationale: generated Skills target zero-config deployment without requiring users to register developer API keys or manage credentials). Solutions must access the target site directly through the browser, using its frontend's internal endpoints or DOM data — the same resources already visible to the authenticated user.

**Framework internal state fast-fail**: when attempting to access page data or element info through framework internals (`__vue_app__`, `$data`, React fiber, Angular `ng`, etc.), **give up after one failure** and immediately switch to `state` scan + value-fill-trigger approach. Framework internals are version/implementation dependent, multiple retries won't change the result.

### JS Execution Environment Constraints

Code executed in eval is **browser-side JS**: only browser-native APIs and page-loaded third-party libraries may be used, no require/import of external modules. Code violating this constraint will inevitably error at execution time.

### Conclusion Criteria

Account permission limits ≠ technical solution failure. Paid features, membership tiers, etc. equally affect all approaches; when API is technically viable but data is limited due to account permissions (pagination truncated, filter conditions ineffective), conclusion is "pass" with permission dependency noted in "Known Limitations".

**Partial success counts as success**: core capability verified working (whether API or DOM path) counts as pass — even with: some enum parameters marked `[collection failed]`, non-core fields missing, some filter conditions not covered. After generating the Skill, **must inform user which parts are not fully covered** — never silently omit.

### Efficiency Rules

Core criterion: **every browser roundtrip must yield information gain.** The table below shows common efficient patterns, but they're just examples — if a pattern doesn't actually reduce roundtrips in practice, change approach and find other batch methods rather than repeatedly fine-tuning in the same direction.

| Rule | Description |
|------|-------------|
| **Composite eval** | Merge multiple independent queries into one eval, wrap in async IIFE, return JSON summary. Each eval is a browser roundtrip — merge everything mergeable |
| **Runtime first** | Information retrieval priority: JS runtime state → network data → DOM. Never reverse-engineer runtime data from DOM |
| **Output volume control** | Extract key fields (count, total, sample) from large responses inside the browser before returning; avoid truncation |
| **Async wait cohesion** | Use Promise + setTimeout polling (with timeout cap) for wait conditions, don't poll repeatedly across tools |
| **Fast permission-restricted detection** | When restricted signals appear (upgrade prompts, data identical to unfiltered, controls disabled), batch-mark similar items as restricted, don't verify one by one |
| **Fetch once, analyze many** | Fetch data from same source only once, save then analyze multiple times; format large text with line breaks to avoid truncation |
| **Stop at verification** | Once API endpoint confirmed working (fetch success + data structure matches expectation), move to next phase immediately, don't continue redundant exploration of the same endpoint (e.g., reverse-searching script tags, extracting extra config) |
| **Slider/range controls batch** | Range sliders (e.g., noUiSlider) and numeric range controls — like input/select, set all controls to different values at once → trigger one search → read all numericFilters mapping from request, don't test each control individually |
