---
name: reddit-warmup
description: "Reddit account onboarding and a staged 30-day warm-up workflow through BrowserAct CLI. Use for Reddit warmup, daily browsing and engagement, account handover, reviewing pending comments/posts, and configured brand-promotion workflows. Requires a logged-in Reddit account, a persistent browser profile with a fixed proxy, and an agent that can manage local state and follow approval policies. The skill defines agent workflows; daily scheduling is configured separately."
---

# Reddit Account Warm-up (30-Day Brand Promotion)

Builds authentic-looking Reddit accounts through a 30-day progression, then uses them to promote any brand the user configures. State files are managed as local files under `~/.reddit-warmup/<username>/`.

**Agent compatibility:** this skill is runtime-neutral. It can be used by any agent environment that can load local Markdown references, read/write local JSON/YAML/text files, list local directories, run shell commands for `browser-act`, and continue a conversation after a user approval reply. Do not depend on runtime-specific question widgets, background agents, sub-agents, notification events, or tool names.

**Execution boundary:** every Reddit-facing browser, page, network, publishing, and verification operation must use `browser-act` CLI as the only browser execution tool. No other browser execution path is allowed. Use `browser-act state` / `get markdown` / `get title` / screenshots / network capture for verification. Local state files are the only non-browser exception and may be handled with the host agent's normal local file read/write/list capabilities. If browser-act cannot complete a step, stop, log/notify, or use browser-act `remote-assist`; never fall back to another browser execution tool. Details in `references/browser-act-rules.md`.

**Three stages:**
- **Days 2-14 -Lurk**: browse and upvote only
- **Days 15-29 -Comment**: AI-generated natural comments; up to 1 non-brand practice post per week
- **Days 30+ -Promote**: comments + up to 2 posts/week (1 normal + 1 promotional)

**Core rule: one account = one browser profile = one proxy.** Never swap, never mix.

---

## Requirements and installation

Install this entire directory, including `references/` and `assets/`; installing only `SKILL.md` is incomplete. Also install the [BrowserAct entry skill](https://github.com/browser-act/skills/tree/main/browser-act) and its CLI using the official installation instructions. This package is an agent workflow, not a standalone unattended program.

Before the first browser or proxy command, load the BrowserAct entry skill and its current runtime guide. Onboarding needs both `browser-act get-skills core --skill-version 2.0.2` and `browser-act get-skills advanced`. Missing CLI/authentication, an unavailable fixed proxy, or a Reddit login requirement is a setup prerequisite to resolve, not a successful run. Keep credentials out of chat and state logs.

Resolve `~` using the current operating-system user's home directory for every state lookup and write, including pending approvals. Do not substitute a Windows-only path on other systems.

## Step 0 -Load Reference Files (required before any action)

Instructions live in separate files loaded on demand. Load the files for the current context before taking any action. Prior knowledge does not substitute for loading the current reference files.

| Context | Load these files (in order) |
|---|---|
| `config.yaml` not found (onboarding) | `references/phase1-onboarding.md` only |
| Phase 2, any stage -start of run | `references/browser-act-rules.md` ->`references/phase2-preflight.md` |
| Stage 1 (Days 2-14) execution | `references/stage1-lurk.md` |
| Stage 2 (Days 15-29) execution | `references/stage2-comment.md` ->`references/approval-rules.md` |
| Stage 3 (Day 30+) execution | `references/stage3-promote.md` ->`references/approval-rules.md` |
| Notification / inbox check | `references/notification-check.md` (called from phase2-preflight Step 6) |
| Daily tail recon + feedback | `references/end-of-day-recon.md` ->`references/comment-follow-up.md` |
| Existing-account migration run | `references/migration.md` (after login and account-health checks) |
| Daily report + anomaly check | `references/anomaly-detection.md` |

---

## Language

All process output to the user (plan confirmation, progress updates, process notifications) follows the user's language.

---

## Red Lines (every account, every stage, no exceptions)

| Rule | Why |
|------|-----|
| Never delete any post/comment in first 30 days | Deletion is a stronger bot signal than silence |
| Email verified immediately after registration | Unverified accounts get silently filtered by many subs' AutoMod |
| No DMs, no friend requests in first 30 days | New-account DMs trigger anti-harassment heuristics instantly |
| No unsubscribing in first 30 days | Sub-hopping looks like a burner account |
| Never edit the same comment more than twice | Repeated edits flag the account |
| All `browser open` uses `--headed` | |
| All browser work goes through `browser-act` CLI | No alternate execution path |

---

## State Files

All state lives in `~/.reddit-warmup/<username>/`:

| File | Purpose |
|------|---------|
| `config.yaml` | Browser ID, proxy, subreddits, keywords, timezone |
| `progress.json` | Current day, karma, stage, last_run, pause flags, week counters |
| `sub_profiles.json` | Per-sub risk cache (karma/age gate, rules, flair, filter rate) -14-day TTL |
| `activity_log.jsonl` | Append-only log; every action recorded here |
| `pending_approval/<batch_id>/` | Batches awaiting user pick -no expiry while unpicked, then retired after skip/publish |
| `drafts/<batch_id>/` | Published / auto-pick audit records and delayed replay records |
| `evidence/` | Per-event screenshots |
| `images/` | Downloaded images for Stage 3 image posts |
| `last_run.png` | Most recent run screenshot |

Templates: `assets/config.yaml.template`, `assets/progress.json.template`, `assets/sub_profiles.json.template`, `assets/persona.json.template`.

**How the agent manages these:** use the host environment's normal local-file capabilities to load JSON/YAML/text, rewrite whole state files, and list matching account/batch directories. Append to JSONL by reading existing content and writing it back with a new line. Do not use shell text-processing shortcuts for state mutation.

---

##  Keyword Rotation

The user's `keywords.find` and `keywords.brand` typically have more than one entry. **Daily tasks automatically rotate** one term from the list so activity naturally disperses.

| List | Rotates? | Reason |
|------|--------|------|
| `keywords.find` | Daily rotation | Swap daily so search result subsets naturally shift |
| `keywords.brand` | Rotates per brand post | Alternate between different selling points per post |
| `keywords.content` | NONo rotation | Persona descriptors form a whole; splitting them causes voice drift |

### Rotation state in `progress.json`

```json
"keyword_rotation": {
  "find_index":  <int>,   // index to use next time Stage 2/3 uses keywords.find
  "brand_index": <int>    // index to use next time Path B uses keywords.brand
}
```

Both indices start at 0 and increment by 1 per use. Retrieval: `list[index % len(list)]`.
- List has only 1 item ->always uses that one (no error)
- User adds/removes items mid-stream ->index just modulos to the new length
- List becomes empty ->skip the current use case

### When to increment

| Trigger | Increment |
|----------------|---------|
| Stage 2/3 uses `find` keyword to search candidate posts | +1 `find_index` (at most once per day) |
| Path B post draft generation determines today's brand angle | +1 `brand_index` (per draft generation, regardless of publish) |

Write back to `progress.json` at the end of the run.

### User-facing commands

| User says | Effect |
|-------|------|
| "Reset keyword rotation `<username>`" | `find_index = 0`, `brand_index = 0` |
| "Next keyword `<username>`" | `find_index += 1`, `brand_index += 1` |
| "Which keyword today `<username>`" | Display today's rotated keyword for find and brand |

---

## Core Principles

1. **Strictly stage-gated.** `current_day = (today - start_date).days + 1` decides the stage. Onboarding backdates `start_date` by `initial_day - 1` days for an existing account; `onboarding_date` records the actual setup date. Reddit account age is independent of this workflow calendar. No jumping ahead.
2. **Preview first, execute immediately.** Show today's plan as one short message, then start -don't wait for "go".
3. **Auto-execute safe actions, pause for publishing.** Browse / upvote / subscribe / scrape run non-stop. These pause for explicit user ack: CAPTCHA / bot challenge, email verification, every comment/post publish (per approval_policy), inbox reply, brand exposure warning, Stage 3 entry decision card.
4. **Once per scheduler day.** If `progress.json.last_run_scheduler_date == today_scheduler`, show cached report and exit. Approval publish flows do not update this field and do not count as the daily run.
5. **All time comparisons use `config.yaml ->account.timezone`.** Never machine-local, never UTC. Timestamps = ISO 8601 with offset.

---

## Approval Rules -Policy-Driven Content Publishing

All content publishing (comments, posts, brand or non-brand) is governed by **`config.yaml.approval_policy`** -the single source of truth. Full rules in **`references/approval-rules.md`**.

**Master policy table:**

| approval_policy | Non-brand content | Brand-bearing (Stage 2) | Brand-bearing (Stage 3) |
|---|---|---|---|
| `manual` | User picks (no expiry) | User picks (no expiry) | User picks (no expiry) |
| `auto` | Agent auto-picks & publishes | Agent auto-picks & publishes | Agent auto-picks & publishes |
| `auto_stage2` | Agent auto-picks & publishes | Agent auto-picks & publishes | **User picks** (no expiry) |

**Change approval policy:** "set approval to manual / auto / auto_stage2 for `<username>`" ->agent first warns that changing between auto-publish and approval paths changes the account's behavior pattern and may increase risk. If the user still confirms, write to config.yaml; takes effect next run. Do not auto-suggest switching to auto mode because of missed or stale approvals.

**Brand-bearing determination**: Variant D / any `keywords.brand` token hit / Path B generated post.

**Brand Exposure warning**: always computed. User-picks paths ->displayed in chat before variants. Auto paths ->logged silently.

**Sub verification** (Path B only): always runs regardless of policy -blocked sub = post skipped entirely.

**Approval** (user-picks paths only): no time limit while unpicked -batch stays in `pending_approval/` until user replies. If one run generates several comments/replies plus posts, store all of them and show one same-account Approval Batch Request containing all currently reviewable items. Comments/replies are ordered before posts. The user can approve in bulk (`all A`) or per item (`1 B, 2 skip, 3 revise title`). Each item still carries its own `batch_id`, `browser_id`, `platform`, `skill`, and account metadata, so execution remains deterministic. Clear approve/skip actions publish or retire items sequentially; do not publish in parallel. After publish/skip, remove each handled item from `pending_approval` and keep the audit record outside the hot-approval pool. Batches older than 7 days are cleaned up by Pre-flight (post almost certainly dead).

**Hot Approval (Rule C6):** natural-language approval in any conversation -`D`, `all A`, `1 B, 2 skip`, `publish B`, `skip`, `make item 1 shorter`, etc. ->agent resolves item(s) from the Approval Batch anchor, item number, `batch_id`, or local pending-approval file lookup ->normalizes the message to internal pick / skip / revise actions. Clear picks start a fresh browser-act run session with the stored `browser_id`, open directly to `/user/me/` for a short account check, then publish stored variants sequentially through the optimized production flow. Clear revise requests update targeted pending items and redisplay one anchored Approval Batch Request for unresolved items. `meta.json` carries `platform`, `skill`, `username`, `browser_id`, `batch_id`, and full draft/variant text for self-contained execution; it must not depend on any previous browser-act session surviving.

**Hard execution rule:** user approval is not complete when the agent writes a `choice` file, marker, or local state note. Approval is complete only after the browser publish flow runs, result is verified, `activity_log.jsonl` / progress are updated, and the final permalink/status is reported. If the natural-language approval is ambiguous, ask one clarification; if it is clear, execute immediately and do not only acknowledge.

Full rules ->`references/approval-rules.md`.

---

## One-Day Execution Flow

```
Daily trigger:
  once per scheduler day ->"today's task - reddit warmup <username>"
  1. Load: references/browser-act-rules.md
  2. Load: references/phase2-preflight.md
  3. Run Pre-flight (phase2-preflight.md Steps 0a onward)
  4. Run Avatar Menu Health Check (click top-right avatar menu; server-error toast blocks writes)
  5. Load references/notification-check.md ->run Notification + Inbox Check
  6. Determine effective_stage from current_day
  7. Route by stage:
     - setup (Day 1): report "initialization complete, Stage 1 browsing starts Day 2" ->exit
     - lurk (Days 2-14): load references/stage1-lurk.md ->browse + upvote + subscribe
     - comment (Days 15-29): load references/stage2-comment.md + references/approval-rules.md ->comment loop
       - If today is Wednesday, posts_this_week < 1, persona ok, and no rate_limit: run Wednesday Practice Post
       - Otherwise skip practice post with no retry until next Wednesday
     - promote (Day 30+): load references/stage3-promote.md + references/approval-rules.md ->entry card if needed ->comment loop
       - Wednesday Path B: run only when all Path B conditions pass; otherwise skip with no retry until next Wednesday
       - Friday Path A: run only when all Path A conditions pass; otherwise skip with no retry until next Friday
  8. Cross-stage checks:
     - Watchtower if this run just posted (30-minute reply campout)
     - Load references/anomaly-detection.md ->full-stop check only
     - If any full-stop signal appears: log, mute, exit without daily tail
  9. Daily tail:
     - Load references/end-of-day-recon.md
     - Load references/comment-follow-up.md
     - Run light daily tail: End-of-Day Recon + Comment Feedback Loop
     - Skip tail if rate-limited, logged out, over time budget, or no eligible targets
  10. Load references/anomaly-detection.md ->final Daily Report
```

Risk posture: the account gets **one scheduled automation run per scheduler day**. Do not wire a fixed second cron/task for recon or feedback. User approval replies are separate event-driven publish flows: they publish the already-approved pending batch only, verify it, write logs, and do **not** re-run Phase 2, browse/upvote/subscribe, or advance the daily run.

---

## Phase 1: Account Onboarding

Triggered when `~/.reddit-warmup/<username>/config.yaml` does not exist.

**->Load `references/phase1-onboarding.md` and follow it entirely.** Do not proceed to Phase 2 from this file.

Skeleton steps (detail in `phase1-onboarding.md`):

| Step | Description |
|------|------|
| 1 | Account type (new / existing) + proxy setup -no credentials collected; proxy URL provided by user or auto-retrieved from browser-act |
| 2 | Create unique browser profile `reddit-setup-<ts>` + temporary setup `run_session` (unified for both paths) + bind proxy + verify IP (ipinfo.io) + proxy conflict check |
| 3A / 3B | Registration or login via remote collaboration (`remote-assist`) ->user completes in browser ->`/user/me/` confirms actual username ->account directory + `browser_id` binding finalized; future browser-act sessions are temporary per-flow `run_session` values |
| 4 | Reddit-side status detection (existing accounts only) |
| 5-.7 | Collect `config_pending` values + sub discovery + persona creation + profile customization; do not write final `config.yaml` yet |
| 6 | Initialize progress.json |
| 7 | Detect scheduler timezone into `config_pending` and preview scheduler wiring |
| 7.5 | 30-day plan preview + approval policy selection ->write final `config.yaml` ->initialization complete |

---

## Phase 2: Daily Execution

Load `config.yaml` and `progress.json`. Compute `current_day`. Show a one-line preview, then:

**->Load `references/browser-act-rules.md`**
**->Load `references/phase2-preflight.md`** -contains all pre-flight steps (0a-), stage determination, and milestone checks.

After pre-flight, proceed to the stage-specific reference file per the Phase Router table above.

---

## Stage 2: Comment (Days 15-29)

Full flow in **`references/stage2-comment.md`** (persona gate, recon, finding posts, variants, duplicate check, approval, publish, verification). Load it when effective_stage == "comment".

**Wednesday Practice Post check (explicit -runs AFTER the comment loop):**

```
Check ALL of the following:
  1. current_day in [15, 29]
  2. today == Wednesday  (account.timezone -NOT machine local, NOT UTC)
  3. progress.json.posts_this_week < 1
  4. Persona readiness gate == "ok"
  5. rate_limit_hit_today == false

->All 5 hold: run Wednesday Practice Post (stage2-comment.md ->Wednesday Practice Post)
->Any one fails: skip silently; no retry until next Wednesday
```

---

## Stage 3: Promote (Day 30+)

Full flow in **`references/stage3-promote.md`** (entry card, Path A/B, Watchtower, Shadowban Check). Load it when effective_stage == "promote".

**Stage 3 post triggers (explicit -run AFTER comment loop):**

Wednesday Path B:
```
Check ALL: effective_stage=="promote" AND today==Wednesday AND promo_posts_this_week<1
           AND posts_this_week<2 AND persona+brand_story ok AND rate_limit_hit_today==false
           AND eligible target sub passes Rule-Reading Gate + no self_promo ban
->All 7: run Path B (stage3-promote.md ->Path B)
->Any fails: skip; log reason; no retry until next Wednesday
```

Friday Path A:
```
Check ALL: effective_stage=="promote" AND today==Friday AND posts_this_week<2
           AND (posts_this_week - promo_posts_this_week)<1 AND persona ok
           AND rate_limit_hit_today==false AND eligible sub passes Rule-Reading Gate
->All 7: run Path A (stage3-promote.md ->Path A)
->Any fails: skip; log reason; no retry until next Friday
```

---

## Daily Tail: End-of-Day Recon + Comment Feedback Loop

Runs once at the end of the same daily scheduled run, after the stage flow and cross-stage checks. This is not a second scheduled job.

Load `references/end-of-day-recon.md` ->`references/comment-follow-up.md`.

Preconditions: main flow completed + `rate_limit_hit_today != true` + login state valid. Reuse the current `<run_session>` only if it is still active inside the same flow; otherwise open a fresh `<run_session>` with the configured `browser_id`. Insert a 90-180s pause between the two routines. If the daily run is already near its time budget or the account has no eligible recon/follow-up targets, skip the tail and report the reason.

---

## Multi-Account Management

Each account = its own dir under `~/.reddit-warmup/`. Run accounts **sequentially, never in parallel.**

List the account directories that contain `config.yaml`. For each where `paused != true` and `skip_tomorrow != true`, run Phase 2; reset `skip_tomorrow`.

| Command | Effect |
|---------|--------|
| "Subscribe to one more sub today" | Add one subscribe task to current account |
| "Skip tomorrow `<username>`" | `progress.json.skip_tomorrow = true` |
| "Switch to light day" | Halve today's remaining activity targets |
| "pause warmup `<username>`" | `paused = true`; remind user to disable external scheduler |
| "resume warmup `<username>`" | `paused = false` |
| "delete account `<username>`" | Move dir to `~/.reddit-warmup/.archived/<username>_<YYYYMMDD>/` |
| "camp `<username>`" | Manual watchtower pass (see stage3-promote.md) |
| "stop camping `<username>`" | Clear `post_watchtower_deadline` |
| "enter brand phase `<username>`" | Manual Stage 3 entry -see `stage3-promote.md ->Entry Decision Card` |
| "refresh subreddit pool `<username>`" | Re-run Phase 1 Step 5.5 auto-discovery |
| "set approval to manual/auto/auto_stage2 for `<username>`" | Warn about mode-switch risk first; if user confirms, write `approval_policy` to config.yaml |
| "clear account risk `<username>`" | After user confirms avatar menu opens cleanly, set `account_risk_flagged = false`, clear `account_risk_reason` / `account_risk_flagged_at` |

---

## References

- `references/browser-act-rules.md` -**Always load first** in Phase 2: No Screenshot rule, Browser Profile + Headed Mode, Authoritative Username, Rule-Reading Gate, CLI idx-selection, UI Drift Fallback, When to ask for help
- `references/migration.md` -Existing-account migration restrictions, clean-login counters, and completion
- `references/phase2-preflight.md` -**Always load second** in Phase 2: Prerequisites, Execution Proof, Rate Limit, Pre-flight Steps 0a-, Stage Determination, Milestone Checks
- `references/notification-check.md` -Cross-stage Notification + Inbox Check (called from phase2-preflight Step 6)
- `references/stage1-lurk.md` -Stage 1 lurk flow (Days 2-14)
- `references/stage2-comment.md` -Full Stage 2 operational flow (Days 15-29)
- `references/stage3-promote.md` -Full Stage 3 operational flow (Day 30+)
- `references/anomaly-detection.md` -**Load at end of every run**: Anomaly Detection + Daily Report
- `references/approval-rules.md` -Comment + brand content approval rules (load with Stage 2/3)
- `references/phase1-onboarding.md` -Full Phase 1 onboarding (load only when config.yaml not found)
- `references/stages.md` -Stage 1/2/3 timing parameters, comment schedule, weekly activity pattern
- `references/end-of-day-recon.md` -daily-tail pre-warm of tomorrow's sub profiles
- `references/comment-follow-up.md` -daily-tail revisit of old comments + karma_by_sub flywheel
- `references/comment-rules.md` -A/B/C/D prompt guidelines, AI-smell blacklist, length table
- `references/comment-publishing.md` -Comment/reply publishing: pure browser-act CLI flow
- `references/login-verification.md` -Step 0 authoritative username + four-layer verification
- `references/image-posting.md` -TEXT / LINK / IMAGE post publishing: pure browser-act CLI
- `references/activity-log-schema.md` -Per-event-type JSON schema, field semantics, append rules
- `references/scheduling.md` -Daily single-trigger wiring (cron, Task Scheduler, agent-native schedulers)

## Assets

- `assets/config.yaml.template`
- `assets/progress.json.template`
- `assets/sub_profiles.json.template`
- `assets/persona.json.template`
