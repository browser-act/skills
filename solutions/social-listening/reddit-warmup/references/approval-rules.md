# Approval Rules -Comments & Brand Content (inviolable)

This file unifies two interdependent approval rulesets: **Comment Approval** (comment publishing follows `approval_policy`. Manual paths require user pick; auto paths let the agent select and publish with audit logging) and **Brand Approval** (brand-bearing content adds a Brand Exposure risk warning + Path B dual-approval on top of Comment Approval).

Both rulesets share the same infrastructure (`pending_approval/<batch>/` + `drafts/<batch>/` directories, `activity_log.jsonl` entries), so they live in one file to avoid drift between them.

---

## Layering -one compact view of how the two layers stack

- **Baseline Comment Approval** applies to every comment, post, and reply. Behavior follows `config.yaml.approval_policy`.
- **Manual paths** write items to `pending_approval/<batch>/`, show one batch approval request per account with all currently displayable items, wait for the user's pick/revision/skip with no time limit, then publish from the stored batch records.
- **Auto paths** skip `pending_approval/`, let the agent select an eligible variant, publish immediately, and write an audit record to `drafts/<batch>/`.
- **Brand Approval** is an additional layer only for brand-bearing content. It adds the Brand Exposure warning, visible `OKbrand` labels, and Path B sub verification/draft approval behavior.

Baseline: every comment/post/reply goes through the same approval-policy router. Manual paths require user approval; auto paths let the agent select and publish with audit logging. Additional: brand-bearing content + Path B promo posts add one more risk layer.

---

# Approval Policy -Master Table

`config.yaml.approval_policy` is the **single source of truth** for all approval behavior. It applies uniformly to comments, posts, brand-bearing content, and all stages. Users set it in Phase 1 Step 7.5 and can request a change by saying "set approval to manual / auto / auto_stage2 for `<username>`".

| approval_policy | Non-brand content | Brand-bearing content (Stage 2) | Brand-bearing content (Stage 3) |
|---|---|---|---|
| `manual` | User picks A/B/C/D/skip (no time limit) | User picks (no time limit) | User picks (no time limit) |
| `auto` | Agent auto-picks and publishes | Agent auto-picks and publishes | Agent auto-picks and publishes |
| `auto_stage2` | Agent auto-picks and publishes | Agent auto-picks and publishes | **User picks** (no time limit) |

**Brand Exposure warning (Rule B2) and sub verification (Rule B3 Step 1) always run regardless of policy** -these are risk-visibility mechanisms, not approval gates. For `auto` and `auto_stage2`-Stage-2 paths, the warning is logged to `activity_log.jsonl` as a `brand_ratio_check` entry but is NOT displayed in chat (user chose uninterrupted automation). For paths that require user picks, the warning displays in chat as usual.

**"Change approval policy" command** (always available, no conditions):
```
set approval to manual for <username>
set approval to auto for <username>
set approval to auto_stage2 for <username>
```

Agent behavior:

1. Read current `approval_policy` from `~/.reddit-warmup/<username>/config.yaml`.
2. If `new_policy == current_policy`, say it is already set; do not rewrite the file.
3. If the policy changes, warn first:

   ```text
   Changing approval policy changes the execution path:
   - auto paths publish immediately and do not create pending approval batches.
   - approval paths pause, store variants, and wait for a user pick.
   Switching between these paths can change the account's behavior pattern and may increase account risk. Please switch only if you understand the risk.

   Reply "confirm switch to <new_policy>" to continue, or "cancel" to keep <current_policy>.
   Natural-language confirmations also work: "confirm switch to <new_policy>",
   "I understand the risk, switch to auto", "continue, change it to manual",
   "cancel, keep the current mode".
   ```

4. If the user cancels or is ambiguous, do not change the policy.
5. If the user explicitly confirms or insists after the warning, write the new value to `config.yaml ->approval_policy`, confirm in chat: "`<username>` approval policy ->`<new_policy>`". Takes effect for the next run.

Never proactively suggest switching to `auto` / `auto_stage2` because approvals were missed, stale, skipped, or repeatedly unpicked. Missed approval is a user-control outcome, not a reason to push auto-publishing.

---

# Approval Display Mode

When `approval_policy` requires a user pick (`manual` or `auto_stage2` + Stage 3 brand), use a runtime-neutral text approval request. Do not depend on runtime-specific question widgets, background agents, sub-agents, or notification events.

The user's reply can be natural language. The Agent must run the Approval Intent Resolver before normal conversation routing while any non-stale `pending_approval/<batch>/meta.json` exists.

## Approval Intent Resolver

Map clear user replies to one of three internal actions:

| User reply examples | Internal action |
|---|---|
| `D`, `reply D`, `pick D`, `use D`, `approve D`, `publish D` | approve variant D |
| `use the second one`, `second option`, `the second one` | approve variant B |
| `approved`, `looks good`, `publish it`, `go ahead` | approve only items with `meta.json.recommended_variant` or `meta.json.default_variant`; otherwise ask which variant for the remaining items |
| `skip`, `pass`, `do not publish`, `don't post it` | skip batch |
| `make it shorter`, `make it sound more natural`, `remove the brand mention`, `rewrite`, `modify`, `revise it` | revise the pending batch; do not publish |
| `all A`, `use B for all`, `publish all C` | apply that variant to every displayed item that has that variant |
| `1 B, 2 skip, 3 revise title` / `use B for item 1 and skip item 2` | apply item-specific actions by displayed item number |

Resolution rules:
1. First parse item-specific references: displayed item number, `batch_id`, or exact account+batch anchor.
2. If the message names a `batch_id`, use that batch.
3. If no `batch_id` is named and the current conversation has exactly one displayed approval item, use that item.
4. If no `batch_id` is named and the current conversation has multiple displayed items:
   - `all A/B/C/D` or bare `A/B/C/D` applies to all displayed items that have that variant.
   - `confirm` / `publish it` applies only to displayed post items with a deterministic default/recommended draft; otherwise ask which item(s).
   - `skip all` skips all displayed items.
   - Revision wording without an item number is ambiguous; ask which item(s) to revise.
5. If no anchor is visible, list matching local files under `~/.reddit-warmup/*/pending_approval/*/meta.json`.
6. If exactly one pending item exists, use it.
7. If one account has multiple pending items, run the Approval Batch Activation helper, display the batch request, and ask the user to reply against the displayed item numbers. Do not apply a bare pick from the same turn unless the user named the exact `batch_id`.
8. If multiple accounts have pending items and the target is unclear, list account-level pending summaries oldest-first. Ask which account the reply applies to.
9. If all selected actions are clear, immediately proceed to Reply Execution Flow. Do not only acknowledge, do not only write a choice file, and do not stop after recording the pick.
10. If any revision request is clear and item-scoped, immediately proceed to Revision Execution Flow for those items. Do not only acknowledge, do not only write a note, and do not wait for a new daily run.
11. If part of the reply is ambiguous, execute only the unambiguous skip/revision actions that are safe, then ask one concise clarification for the remaining unresolved items. Never publish an ambiguous item.

## Approval Batch Request Format

Display format:
```
Approval Batch: reddit-warmup / <username>
platform: reddit  browser: <browser_id>  pending: <N>

[1] kind: <comment|reply|post|brand>  batch: <batch_id>
Target: r/<sub> -"<post title>"
<complete post body>

[If brand-bearing: Brand Exposure warning (Rule B2) first]

**A.** <full text>
**B.** <full text>
**C.** <full text>
**D.** <full text>  OKbrand

[2] kind: <post>  batch: <batch_id>
Post draft -r/<sub>
Title: <title>
Body: <body>

You can reply naturally:
- `all A`
- `1 B, 2 confirm, 3 skip`
- `1 make it shorter, 2 publish`
- `skip all`
Canonical item command: `approve <username> <batch_id> A|B|C|D|confirm`
Revise item command: `revise <username> <batch_id> <instruction>`
Skip item command: `skip <username> <batch_id>`
```

**Multi-account rule:** Batch-display only one account at a time. Never mix multiple Reddit accounts in one approval batch request. If multiple accounts have pending items, show an account-level summary first and ask which account to handle.

## Approval Queue: Batch Display

Draft generation may produce multiple approval items in one daily run, for example several comments plus one post. Persist all items, then expose all currently displayable items for the same account in one approval batch request. This reduces user friction while keeping each item independently addressable.

**Queue fields in `meta.json`:**
```json
{
  "queue_status": "queued | displayed | retired",
  "queue_position": <int>,
  "queue_total": <int>,
  "approval_item_index": <int>,
  "display_group_id": "<account-scoped display batch id>",
  "displayed_at": "<ISO+offset|null>",
  "retired_at": "<ISO+offset|null>"
}
```

**Queue ordering:**
1. Comments and replies first, in creation order.
2. Posts after all pending comments/replies, in creation order.
3. Brand-bearing Path B posts keep the same order but still show the Brand Exposure warning inside their item block.

**Display rule:** at any moment, show one Approval Batch Request per account. Include every non-retired item for that account that is ready for user review, ordered by the queue ordering above. Additional items created after the batch request can be appended to a later batch request; do not mix multiple accounts in one request.

**Batch reply rule:** item-numbered replies are preferred (`1 B, 2 skip`). `all A/B/C/D` applies to every displayed item with that variant. A bare `A/B/C/D` in a visible multi-item batch is interpreted as `all A/B/C/D` only when every displayed item has that variant; otherwise ask one clarification. `confirm` applies to post items only when the target item is numbered or there is exactly one post item.

**Execution rule:** after the user reply is parsed, execute clear approve/skip actions sequentially in queue order. Do not publish items in parallel. Comments/replies execute before posts unless the user explicitly numbers a different safe order. If some items need revision, revise and redisplay only those unresolved items after finished publish/skip actions complete.

**Activation helper:** when generating drafts, resuming a conversation, or retiring handled items, normalize the queue before displaying anything:
1. List matching local files under `~/.reddit-warmup/<username>/pending_approval/*/meta.json` for the same account.
2. Ignore batches with `queue_status: "retired"`.
3. Sort remaining batches by the Queue ordering above, then by `created_at` / batch id.
4. Set every sorted item to `queue_status: "displayed"` when it is included in the current Approval Batch Request.
5. Assign `display_group_id` for the request and set `displayed_at` to now for newly displayed items.
6. Recompute `queue_position`, `queue_total`, and `approval_item_index` for every non-retired batch before displaying the batch request.
7. Legacy `queue_status: "active"` means `displayed`; normalize it to `"displayed"` on the next write.

**Explicit batch override:** if the user names both `<username>` and `<batch_id>`, use that exact batch even if it was not included in the most recent displayed batch. This is the only time a non-displayed batch can be selected directly.

**After the user replies with clear approval, skip, or revision requests** ->Rule C6 handles execution (see Part 1 Rule C6). Clear approve/skip intents execute immediately in sequence; clear revision requests update the targeted items and immediately show a revised Approval Batch Request for unresolved items.

## Detection logic

1. Current `approval_policy` path requires a user pick ->show the runtime-neutral Approval Batch Request.
2. Later user message ->run Approval Intent Resolver before normal routing.

For `auto` and `auto_stage2`-auto paths: no display -agent picks and publishes immediately per Rule C1.

---

## Reply Execution Flow

**Triggered by:** a clear natural-language approval, A / B / C / D, confirm, or skip -from the Approval Batch Request or Rule C6 hot pick.

**Hard rule: approval ->next step is execution. Never stop after acknowledging the pick. Never treat writing `choice`, `selected_variant`, or another local marker as completion.**

### Step 1 -Locate batch

If the user's reply addresses multiple items, expand it into an ordered list of per-item actions first. Each item still maps to exactly one `pending_approval/<batch_id>/meta.json`. Run Steps 1-7 below for each approved/skipped item sequentially in queue order, unless the user gave explicit item numbers that define a different safe order. Never publish multiple items in parallel.

Check in order:
1. `~/.reddit-warmup/<username>/pending_approval/<batch_id>/meta.json`
2. If already moved: `~/.reddit-warmup/<username>/drafts/<batch_id>/meta.json`

Also read: `config.yaml`, `progress.json`. Read `sub_profiles.json` if flair or sub rules are needed.

For approval intents (not skip or revision), before publishing, update `meta.json` with:
```json
{
  "approval_status": "approved",
  "selected_variant": "<A|B|C|D|confirm>",
  "approved_at": "<ISO+offset>",
  "approved_text_hash": "<sha256 of exact text to publish>"
}
```

This state update is only a checkpoint. The Agent must continue into Step 2 immediately.

If the user intent is `skip`, do not open the browser and do not publish. Instead:
1. Update `meta.json` with `approval_status: "skipped"`, `selected_variant: null`, `skipped_at: "<ISO+offset>"`, and `queue_status: "retired"`.
2. Append `type: "skip"` to `activity_log.jsonl` with `batch_id`, `kind`, `subreddit`, and the exact user message.
3. Remove the batch from `pending_approval/` or move it to the skipped audit location used by this skill.
4. Run the Approval Batch Activation helper and display the remaining unresolved items, if any.
5. Report that this batch was skipped. Do not ask for a second confirmation unless the user's skip wording was ambiguous.

### Step 2 -Read metadata + rate-limit check

From `meta.json`, extract: `batch_id`, `subreddit`, target URL (or post title/body), variant text for the picked letter, `username`, `browser_id`, `kind` (comment / reply / post), `path` (A/B for posts), flair requirements.

Rate-limit: read `progress.json.last_publish_at`. If `now - last_publish_at < 90s`, wait the remainder.

### Step 3 -Start fresh browser-act runtime session + verify login

Create a new `<run_session>` for this approval execution. Do not reuse or depend on a previous browser-act session; browser-act may close sessions after each completed flow. The durable binding is `browser_id`, not session. For a multi-item approval reply, the agent may continue using the same `<run_session>` for the next item only if it is still active inside this same execution; if it is missing or closed, open a new fresh `<run_session>` with the same stored `browser_id` before continuing the next item.

```bash
RUN_SESSION="reddit-warmup-<username>-approval-<ts>"
browser-act --session "$RUN_SESSION" browser open --headed <browser_id> https://www.reddit.com/user/me/
browser-act --session "$RUN_SESSION" wait stable --timeout 10000
browser-act --session "$RUN_SESSION" state
```

`wait stable` is a short, non-blocking readiness hint on Reddit's SPA. If it times out, continue to `state`; the `state` current URL is the authority for this step.

Missing active browser-act session is expected and is not a publish failure. Open the same `browser_id` from `meta.json` / `config.yaml` in the fresh `<run_session>`, then continue. Do not create a new browser profile and do not switch accounts.

Read the current URL from the `state` output. It must resolve to `/user/<username>/`. Abort only on `/login` or wrong account after opening and verification: tell user "Login expired for `<username>`. Log in manually, then reply `<pick>` again."

Do **not** run the Avatar Menu Health Check in this approval execution path. Hot Approval is a surgical user-approved publish action, not a new daily preflight. Account-health checks belong to the scheduled daily run (`phase2-preflight.md ->Step 6.1`) before that run starts proactive activity. After the user approves a stored draft, the publish path only verifies login/account identity here and then relies on the target-page/commentability checks in Step 4. Do not inspect or block on `progress.json.account_risk_flagged` in this path; surface only publish-time failures from the target page or submit/verification flow.

Do not add a separate subreddit warmup page hop in the hot-approval path. The publish flow itself handles a short target-page dwell before writing. This avoids turning one approved publish into multiple unrelated page loads while keeping the account check, target-page guard, fill verification, and post-submit visibility verification intact.

Use **normal production mode** for hot approvals: short non-blocking waits, `state` / markdown as the authority, and screenshots only at evidence points. Use a stricter diagnostic mode only after a publish-time failure, UI drift, or user-requested investigation.

### Step 4 -Submit

| Kind | Execute via |
|---|---|
| comment / reply | `references/comment-publishing.md` ->use the verified `<run_session>` from Step 3 |
| post (Path A / B) | `references/image-posting.md` ->Common flow using the verified `<run_session>` from Step 3 |

If subreddit requires flair: select flair **before** submitting.

### Step 5 -Verify

Must obtain verified published evidence. "Submit button clicked" is not success.

For comments/replies:
- Follow `comment-publishing.md ->Step 9` exactly.
- The agent must return to the original post thread after submission and verify the submitted body is visible there, or discover a permalink from the account comment history and verify that permalink resolves to the submitted body.
- A network 200, disappeared composer, or account-history row alone is not enough. Do not write a successful `comment` log entry until the original thread or verified permalink shows the body.

For posts:
- Must obtain `post_id` / permalink and complete the submitted-list + permalink filter checks from `image-posting.md`.
- Record `visible`, `removed_by_filter`, or `failed`; do not collapse filtered posts into success.

### Step 6 -Write back state

- Move `pending_approval/<batch_id>/` ->`drafts/<batch_id>/`
  - Posts: also write `published_at`, `draft_expires_at = now+24h`, and `result` into moved `meta.json`
- Append to `activity_log.jsonl` (`type: "comment"` or `type: "post"`, `"approval": "hot_pick"`)
- Update `progress.json`:
  - All: `last_publish_at = now`
  - Post only: `last_post_url`, `last_post_time`, `posts_this_week += 1`, `promo_posts_this_week += 1` (Path B), `post_watchtower_deadline = now+30min` (visible only), `seen_reply_ids = []`
- Save evidence screenshot to `evidence/`

### Step 7 -Report to user

Include: handled item count, each batch id, variant letter or confirm action, final status (published / removed_by_filter / skipped / failed), permalink or post id.

After each successful publish or skip, set that handled batch's `queue_status` to `"retired"` and `retired_at` to now. After all clear actions from the user's reply have been processed, check `pending_approval/` for the same account:
- If unresolved items remain because they need revision, clarification, or were not addressed, display one refreshed Approval Batch Request for those items.
- If no unresolved items remain, say there are no more pending approvals for the account.

On failure: surface the specific failure reason immediately (e.g. "session expired", "post locked", "fill didn't commit", "Reddit 429"). Never silently swallow errors -the user explicitly approved this content.

---

## Revision Execution Flow

**Triggered by:** a clear natural-language revision request such as `make it shorter`, `rewrite`, `make it more natural`, `remove the brand mention`, `modify`, or `revise it`.

**Hard rule: revision ->next step is rewriting the pending batch and redisplaying approval. Never stop after saying "got it", never wait for the next daily run, and never publish during a revision turn.**

1. **Locate the batch** with the same resolver as Reply Execution Flow Step 1:
   - Use the Approval Batch anchor and item number first when visible.
   - Otherwise list matching local files under `~/.reddit-warmup/*/pending_approval/*/meta.json`.
   - If multiple batches match and the user's revision does not name `username` or `batch_id`, list pending batches oldest-first and ask which one to revise.

2. **Read `meta.json` and current draft files.** Required fields: `platform`, `skill`, `username`, `browser_id`, `batch_id`, `kind`, `subreddit`, target URL or post title/body, and the current `variants` or post draft.

3. **Apply the user's revision instruction immediately.**
   - Comment / reply batch: regenerate or edit the A/B/C/D variants using the original `post_body`, target context, persona, duplicate rules, brand constraints, and the user's exact instruction. Keep the same `batch_id`.
   - Post batch: edit title/body/image note as requested, preserving subreddit, path, brand constraints, and post type. Keep the same `batch_id`.
   - If the instruction is underspecified ("make it better"), make a conservative improvement and redisplay. If the instruction could change risk materially ("add link", "mention brand", "switch sub"), ask one clarification before rewriting.

4. **Write back state before displaying.**
   - Update the draft text files in the existing `pending_approval/<batch_id>/` directory.
   - Update `meta.json`:
     ```json
     {
       "approval_status": "pending",
       "selected_variant": null,
       "approved_at": null,
       "approved_text_hash": null,
       "revision_count": <previous + 1>,
       "last_revision_instruction": "<exact user message>",
       "last_revised_at": "<ISO+offset>",
       "revision_history": ["<optional compact summary of previous title/body or variant hashes>"]
     }
     ```
   - Preserve `platform`, `skill`, `username`, `browser_id`, `batch_id`, `subreddit`, `kind`, and target URL fields exactly. These are the recovery keys for the next approval reply.

5. **Immediately display the revised Approval Batch Request** using the same runtime-neutral anchor:
   ```text
   Approval Batch: reddit-warmup / <username>
   platform: reddit  browser: <browser_id>  pending: <N>
   [<approval_item_index>] kind: <comment|reply|post|brand>  batch: <batch_id>
   ```
   Include the revised variants or revised post draft, plus natural-language approval / revise / skip commands. If multiple items were revised, show all revised items in one batch request.

6. **Do not publish in the same revision turn** unless the user gave a combined unambiguous instruction such as "make it shorter and publish B" and the selected final text is deterministically known. In normal cases, wait for the user's next clear approval.

---

# Part 1 -Comment Approval

All comments and posts go through this flow. Behavior at each step is gated by `approval_policy`.

### Rule C1 -Generate, persist, display, and publish variants

Generate variants ->write to `~/.reddit-warmup/<username>/pending_approval/<batch_id>/` (persisted for audit).

**Then branch on `approval_policy`:**

| approval_policy | Behavior |
|---|---|
| `manual` | Enqueue the batch. Display it as part of the current account's Approval Batch Request. User can pick A/B/C/D/skip per item or for all displayed items ->publish picked items sequentially |
| `auto` | Agent picks uniformly at random among eligible variants ->publish immediately (no window, no chat display) |
| `auto_stage2` | Stage 2 or Stage 3 non-brand ->same as `auto`; Stage 3 brand-bearing ->same as `manual` |

For `auto` and `auto_stage2`-auto paths: skip writing to `pending_approval/` (no window needed); write directly to `drafts/<batch>/` as audit record after publishing. Log `"approval": "auto_policy"`.

For `manual` and `auto_stage2`-manual paths: write to `pending_approval/` (no expiry while unpicked -batch stays until the user picks/skips or 7-day stale cleanup per Rule C4). Set `queue_status` to `"queued"` by default, then display all ready same-account items together per the Approval Queue rule. After a clear pick or skip is handled, the batch must leave `pending_approval/` or become `queue_status: "retired"` so future natural-language replies cannot re-trigger it.

Log the auto-pick in `activity_log.jsonl`:
```json
{"type": "comment", ..., "variant": "<A|B|C|D>", "approval": "auto_policy"}
```

`meta.json` for every batch must include at minimum:

```json
{"kind": "comment",
 "platform": "reddit",
 "skill": "reddit-warmup",
 "batch_id": "<batch_id>",
 "created_at": "<ISO+offset>",
 "post_url": "<url>", "subreddit": "r/<sub>", "post_title": "<title>",
 "post_body": "<complete post body text>",
 "stage": "<comment|promote>",
 "brand_bearing": <bool>,
 "browser_id": "<browser_id from config.yaml>",
 "username": "<reddit account username>",
 "approval_status": "pending",
 "queue_status": "queued | displayed | retired",
 "queue_position": <int>,
 "queue_total": <int>,
 "approval_item_index": <int>,
 "display_group_id": "<account-scoped display batch id>",
 "displayed_at": null,
 "retired_at": null,
 "selected_variant": null,
 "approved_at": null,
 "approved_text_hash": null,
 "variants": {
   "A": "<full rendered text of variant A>",
   "B": "<full rendered text of variant B>",
   "C": "<full rendered text of variant C>",
   "D": "<full rendered text of variant D>"
 }}
```

### Rule C2 -When showing variants, always output batch context

Show one Approval Batch Request per account, containing all displayable pending items for that account. Queued batches are stored until the next batch request is displayed. The display requires:

1. **Batch anchor** (mandatory):
   ```
   Approval Batch: reddit-warmup / <username>
   platform: reddit  browser: <browser_id>  pending: <N>
   ```
   This lets any subsequent conversation turn (including after context compaction) resolve the platform, skill, account, and browser profile without re-running the daily task. It does not require the old browser-act session to exist.

2. **Per-item anchor** (mandatory for every displayed item):
   ```
   [<approval_item_index>] kind: <comment|reply|post|brand>  batch: <batch_id>
   ```

3. **Post context**: target sub, original post title, **complete post body**, (if applicable) the full content of the comment being replied to. Without this the user cannot judge which variant fits.

### Rule C3 -No approval window -reply any time

Once variants are in `pending_approval/<batch>/`, the batch stays there until the user picks or skips. **There is no time limit while it is unpicked.** The pick can happen immediately, hours later, or days later -in the same run, in any subsequent run, or in any new conversation via Hot Approval (Rule C6). After the pick/skip is executed, the batch is no longer pending and must be moved/retired from the hot-approval pool.

User replies A/B/C/D ->stored variant text is used directly ->publish. No regeneration, no re-confirmation.

### Rule C4 -Batch cleanup (7-day stale sweep)

Pre-flight Step 1 runs a single sweep on every run:

- List matching local files under `pending_approval/*/meta.json`.
- For each batch: if `replay_after` is set and `now >= replay_after` ->clear `replay_after`. Do **not** surface batch text in the Daily Report; the Daily Report only shows the count of open pending approvals. If the batch needs renewed attention, emit a standalone Approval Batch Request with the normal batch anchor.
- For each batch: if `created_at` is **older than 7 days** and `replay_after` is null ->delete the directory, append `type: "skip", reason: "batch_stale_7d"` to `activity_log.jsonl`. (Post is almost certainly dead by then -commenting on a week-old post that prompted original variants would be off-context.)

`pending_approval/` is only for unhandled user-pick batches. After a manual-path batch is approved and published, move it to `drafts/<batch>/` with `approval_status`, `selected_variant`, `published_at`, `result`, and evidence fields populated. After a skip, remove it from `pending_approval/` and keep the skip entry in `activity_log.jsonl`. Never leave an already-published or skipped batch in `pending_approval/`.

### Rule C5 -Log the user's pick

After the user picks A/B/C/D/confirm/skip, write the matching `type: "comment"`, `type: "reply"`, `type: "post"`, or `type: "skip"` entry to `activity_log.jsonl`. Record `variant` or `confirm` + the `content_hash` of the picked draft when applicable. Audit depends on this. A successful publish or skip must also retire the batch from `pending_approval/`; leaving it there is a duplicate-publish hazard.

### Rule C6 -Hot Approval (natural-language pick, executes immediately)

When the user sends a clear approval in **any conversation** -`A` / `B` / `C` / `D` / `skip` alone, batch language like `all A`, or item-specific language like `1 B, 2 skip, 3 make it shorter` -the agent treats it as a **hot approval intent**. Clear approve/skip intents execute immediately, no daily task re-run required. This is the primary path when the cron session has already exited and the user replies in a new conversation.

**Trigger patterns (case-insensitive):**
- Variant pick: entire meaningful content is `A` / `B` / `C` / `D`, or prefixed with `pick ` / `approve ` / `select ` / `reply ` / `publish `.
- Ordinal pick: `first` / `first one` ->A, `second` / `second one` ->B, `third` / `third one` ->C, `fourth` / `fourth one` ->D.
- Batch pick: `all A` / `use B for all` / `publish all C` ->apply to all displayed items with that variant.
- Item pick: `1 B`, `item 2 skip`, `3 revise title`, `use A for 1 and B for 2` ->apply to the displayed item number.
- Skip: `skip` / `pass` / `do not publish` / `don't post it`.
- Revise: `make it shorter` / `rewrite` / `make it more natural` / `remove the brand mention` / `modify` / `revise it`; run Revision Execution Flow, regenerate/edit the targeted item(s), and display a new Approval Batch Request. Do not publish.
- Generic approval: `approved` / `looks good` / `publish it` / `go ahead` executes only for displayed items with `meta.json.recommended_variant` or `meta.json.default_variant`. Otherwise ask which variant for the unresolved items.

**Execution flow:**

1. **Resolve batch context** -two sources, in order of priority:
   - **Priority 1 -Approval batch in current conversation:** if the approval notification is visible in the current conversation context, extract `username`, `platform`, `skill`, `browser_id`, each displayed item number, and each `batch_id` from the batch request. Read each targeted `~/.reddit-warmup/<username>/pending_approval/<batch_id>/meta.json` directly.
   - **Priority 2 -local pending-approval file lookup (new conversation / anchor not visible):** list matching local files under `C:/Users/<system_user>/.reddit-warmup/*/pending_approval/*/meta.json` across all configured accounts.
     - **Exactly one pending item across all accounts:** use it directly.
     - **One account with multiple pending items:** run the Approval Batch Activation helper for that account and display a batch request. Do not apply a bare pick from the same turn unless the user named exact `batch_id` values or the message is explicitly batch-scoped (`all A`, `skip all`).
     - **Single legacy batch with no `queue_status`:** treat it as displayed for this reply, then write queue fields back to `meta.json`.
     - **Multiple accounts with pending items:** list them oldest-first by account and item count (format: `Account: <username>  platform: reddit  skill: reddit-warmup  browser: <browser_id>  pending: <N>`) and ask which account this reply applies to before executing. Never apply a bare A/B/C/D across multiple accounts.
   - **No pending batches found:** tell user "No pending approval batches found." Do NOT treat as hot approval.

2. Read `meta.json` for the matched batch. Confirm `platform == "reddit"` and `skill == "reddit-warmup"` when present; if missing in an older batch, infer these values from the directory/skill context and preserve them when writing the next `meta.json`.

3. If the user intent is a revision request, go to **Revision Execution Flow** immediately. Do not resolve a variant, do not publish, and do not only acknowledge.

4. If the user intent is `skip`, run the skip branch in Reply Execution Flow Step 1 immediately. Do not resolve a variant and do not open the browser.

5. Resolve variant text: `meta.json.variants.<pick>` (e.g. `variants.A`).
   - `meta.json.brand_bearing == true`: the variant display already labeled brand variants with `OKbrand`. The user's explicit pick IS the confirmation -**no re-confirm step**. Brand exposure is already logged as `brand_ratio_check` when variants were generated.

6. After resolving variant text for every clear item ->immediately proceed to **Reply Execution Flow Steps 1-7** above for each item sequentially. For comments/replies use the comment path (comment-publishing.md); for posts use the post path (image-posting.md).

**What hot approval does NOT do:** does not re-run Pre-flight, does not browse / upvote / subscribe, does not advance `current_day`, does not update `last_run`, and does not stop at writing `choice` or `selected_variant`. It is a surgical approval-publish flow for the selected item(s), not a full daily task.

**Multiple displayed batches for the same account:** this is valid when they are part of one Approval Batch Request. If stale `active` statuses from older docs are detected, normalize all non-retired same-account items to `queue_status: "displayed"` and recompute item numbers before interpreting the user's reply.

---

# Part 2 -Brand Approval (additional layer)

Part 2 governs every piece of content that mentions the brand or promotes the product. It adds another layer ON TOP of Part 1's baseline -**not a replacement** -the baseline runs as always, with extra hard gates added.

### Definition -what counts as "brand-bearing"

A draft is **brand-bearing** when any of the following holds:

1. **Variant D** is generated (deliberate Problem-Solution intent, regardless of whether the text literally contains the brand name) ->log `brand_mention_intent: "deliberate"`
2. Any `config.yaml ->keywords.brand` token appears in the rendered text (case-insensitive substring match) ->for A/B/C hits, log `brand_mention_intent: "accidental"`
3. **Posts**: the draft is generated via **Path B** (promotional). Path B drafts always count as brand-bearing, even without brand names -the posting intent itself is brand promotion

A/B/C with zero brand tokens **and no D sibling** ->`brand_mention_intent: "none"`; Part 1 alone is enough.

### Rule B1 -Brand-bearing content approval follows `approval_policy`

Brand-bearing content (D variant / `keywords.brand` hit / Path B post) is subject to the same `approval_policy` as all other content. There is no separate "brand override" that supersedes the user's choice.

| approval_policy | Brand-bearing behavior |
|---|---|
| `manual` | Show Brand Exposure warning in chat ->user explicitly picks A/B/C/D/rewrite/skip |
| `auto` | Brand Exposure check logged silently ->agent auto-picks and publishes |
| `auto_stage2` | Stage 2 brand: agent auto-picks and publishes; Stage 3 brand: show warning + user picks |

The user set this policy in Phase 1 Step 7.5. Changing it follows the "Change approval policy" warning flow above. The agent must not silently flip into or out of auto-publish mode; warn first, then switch only after the user confirms.

### Rule B2 -Brand Exposure warning: chat display vs. silent log

Compute the brand exposure ratio regardless of policy (`ratio_before`, `risk_level in {low, moderate, elevated}` -see `stage3-promote.md ->Brand Exposure Target`).

| approval_policy + stage | Warning delivery |
|---|---|
| `manual` (any stage) | Display in chat BEFORE showing variants. User reads risk level first. |
| `auto_stage2` + Stage 3 brand | Display in chat BEFORE showing variants. |
| `auto` (any stage) | Log silently to `activity_log.jsonl` as `type: "brand_ratio_check"`. No chat display. |
| `auto_stage2` + Stage 2 / Stage 3 non-brand | Log silently. No chat display. |

**Show the warning BEFORE variants when displaying** (for manual/auto_stage2-S3 paths) -user reads the risk level before seeing drafts, to avoid impulse-picks.

### Rule B3 -Path B posts: sub verification always runs; draft approval follows policy

In order:

1. **Sub verification** (always, regardless of policy) -the specialized-sub check in `stage3-promote.md ->Path B Step 2` outputs `post | blocked | warm-up-first`. Only `post` continues. This is a risk gate, not an approval gate -the sub either allows self-promotion or it doesn't.
2. **Draft approval** -follows `approval_policy`:
   - `manual`: confirm / modify / revise it / cancel (user picks)
   - `auto`: agent auto-selects and publishes
   - `auto_stage2` + Stage 3: confirm / modify / revise it / cancel (user picks)
   - `auto_stage2` + Stage 2: agent auto-selects and publishes

### Rule B4 -Manual-path batches have no expiry while unpicked

Batches that require user picks (manual / auto_stage2 Stage 3 brand) ->write to `pending_approval/` with no expiry while unpicked. Stay there until picked/skipped or 7-day stale cleanup (Rule C4). After publish/skip, retire them from `pending_approval/` immediately.

Batches on auto paths ->skip `pending_approval/`; publish immediately; write audit record directly to `drafts/<batch>/` with `draft_expires_at = now + 24h`.

### Rule B5 -Tag, don't hide

When displaying brand-bearing variants, label them explicitly:

```
Target: r/<sub> -"<post title>"
<complete post body>

---
A. <full text>
B. <full text>
C. <full text>  OKbrand (detected keyword: "<matched_token>")
D. <full text>  OKbrand (D variant -always brand-bearing)

Pick A / B / C / D / skip
```

The user can see which variants have brand intent. NEVER silently mix brand/non-brand variants without labels.

### Rule B6 -9:1 ratio is advisory, not a block

Warning is shown; user decides. Elevated-risk drafts can still be published via an explicit pick. The hard block is Rule B1 (no auto-publish); 9:1 is only advisory.

### Rule B7 -Log every brand decision

When the Brand Exposure warning fires, append a `brand_ratio_decision` entry to `activity_log.jsonl`:

```json
{"type": "brand_ratio_decision",
 "ratio_before": {"rolling_10_brand_count": 2, "weekly_promo_posts": 1, "weekly_brand_comments": 1},
 "risk_level": "low|moderate|elevated",
 "user_choice": "rewrite|publish_anyway|skip",
 "draft_summary": "<first 80 chars>"}
```

Weekly/monthly reports derive the brand posture from this.

---

## Interaction with other systems

### Weekly Posting Cap

| Stage | Total posts/week | Promotional posts/week |
|-------|------------------|------------------------|
| Lurk | 0 | 0 |
| Comment | 1 (Wednesday practice post only; text-only; no brand) | 0 |
| Promote | 2 | **1 (advisory -user can exceed with explicit ack)** |

**The weekly promotional-post cap is advisory, not a hard block.** When `promo_posts_this_week >= 1` and the user is about to trigger a second Path B post this week:

1. Generate the draft normally
2. In the Brand Exposure warning (Rule B2, Stage 3 Path B Step 2), **prepend an extra line**:
   ```
   Warning: Weekly promo-post cap exceeded
   You've already published <N> promotional post this week (cap: 1).
   Publishing another one this week materially increases:
     -sub AutoMod filter probability (many target subs track "N posts
       per user per week" and hide subsequent ones)
     -"spam poster" profile fingerprint from Reddit's site-wide ML
   Recommended: wait until next week (resets every Monday <account tz>).
   Continue anyway? (yes / no / save-for-next-week)
   ```
3. User picks `yes` ->proceed to normal Path B approval flow (user still has to approve the specific draft)
4. User picks `no` ->`skip("weekly_cap_declined")`, log the fact the user saw the warning
5. User picks `save-for-next-week` ->write to `drafts/<batch>/` with `meta.json.replay_after: <next_monday_iso>`; Pre-flight on that Monday clears `replay_after` and auto-restores the batch into `pending_approval/` (normal Rules C3/C4 apply -no expiry)

This is a **warning**, not a block. The user is operating their own account and knows their own risk tolerance. A "never let user exceed the cap" hard-stop is paternalistic; a "show the risk, log the decision, let them proceed" gate gives full control while keeping accountability.

**Logging**: every time the cap warning fires, append a `weekly_cap_warning` entry to `activity_log.jsonl`:
```json
{"type": "weekly_cap_warning",
 "promo_posts_this_week_before": <N>,
 "user_choice": "yes | no | save-for-next-week",
 "draft_summary": "<first 80 chars of title>"}
```

This lets the weekly report surface "user overrode the cap X times this month" if the pattern becomes habitual.

### Rule-Reading Gate

Brand approval sits **on top of** the Rule-Reading Gate, not in place of it. Brand-bearing drafts still have to pass the sub's `forbids_self_promo` / karma gate / every other gate. A user picking "publish_anyway" in the Brand Exposure warning **does NOT override** `forbids_self_promo` -the skill still skips the sub.

### Approval consistency

- Rules C3/C4 (comment batches) and Rule B4 (brand batches) share the same no-expiry-while-unpicked design: manual-path batches stay in `pending_approval/` only until picked/skipped or 7-day stale cleanup.
- `drafts/` stores auto-pick audit records, published manual-path audit records, and delayed replay records. `pending_approval/` must never contain already-published or skipped batches.
- `REDDIT_WARMUP_UNATTENDED=1` governs non-approval interactive points only -specifically the CAPTCHA Tier 3 fallback (interactive wait vs unattended abort + `daily_skip_reason: "captcha_at_preflight"` / `"captcha_on_relogin"`) and any error-recovery prompts that would otherwise hang a headless run. See `stages.md ->Rate Limit & CAPTCHA Rules`.

