# InstaDM Decision-Tree DSL — Specification v1.0

**Owner:** Guillaume Lambert (Orisha) · **Date:** Nov 20, 2026 · **Updated:** Nov 22, 2026 · **Status:** Draft v1.0
**Files:** `decision-tree.schema.json` (JSON Schema 2020-12) · `profit-funnel.json` (PROFIT funnel) · `interpreter.py` (reference sketch) · `validate.py` (schema + lint + offline demo)

## 1. Purpose

One file describes the agent's whole Instagram DM conversation. It is used by:

1. **The editor app**: displays the tree as a graph (nodes + edges) and edits it.
2. **The server** behind ManyChat: interprets the same file for every inbound DM or quick-reply tap that passes the `profit_active` gate (see the project definition and §7). The server owns all copy, state (its own DB), tags, Claude, reminders, analytics, and handoff (Slack alert to Phil). ManyChat is a thin pipe only.

Design rules: **declarative** (no code in the tree), **JSON** as the canonical format (YAML may be used for hand-authoring and converted 1:1), **stable ids**, and **one waiting point per turn**.

## 2. Model

The tree is a **state machine**. Each contact has a state:

| Field | Meaning |
|---|---|
| `node` | Current node id (the node waiting for the lead's answer) |
| `vars` | Values collected so far (typed, declared in `variables`) |
| `tries` | Failed attempts on the current node (reset on every transition) |
| `human_handoff` | true = a human owns the conversation; the server stays silent |
| `last_inbound_at` | Timestamp of the lead's last message (24-hour window) |
| `tree_version` | Tree version the contact started on |

Nodes are either **waiting** (`ask`, `choice`: they send a prompt and stop until the lead answers), **pass-through** (`message`, `condition`, `set`, `action`: they run and continue immediately), or **terminal** (`end`, `handoff`).

**Edges are implicit.** They are the node-id references in `next`, `on_fail`, `else`, `on_error`, `branches[].next`, `options[].next`, and `no_match.on_fail`. The editor derives edges from these fields and labels them (option caption, branch label, "fail", "else"). There is no separate edge list, so the graph can never disagree with the logic.

## 3. File structure

```jsonc
{
  "dsl_version": "1.0",               // spec version; server accepts any 1.x
  "tree": { "id", "name", "version", "language", "updated_at", "updated_by", "redirects", "ui" },
  "config": { "inbound_url", "ai", "window_hours", "max_messages_per_send", "pacing",
              "on_inbound_after_end", "default_max_tries", "livechat_url_template", "transcript_size" },
  "constants": { "BOOKING_URL": null, "PROFIT_THRESHOLD": 8000, "SLACK_HANDOFF_WEBHOOK_URL": null, "SLACK_PHIL_USER_ID": null },
  "variables": { "season_sales": { "type": "number", "manychat_field": "season_sales" } },
  "triggers": [ { "id": "profit_comment", "type": "comment_keyword", "keyword": "PROFIT", "start": "welcome" } ],
  "global_intents": [ { "id": "human", "keywords": ["talk to guillaume"], "goto": "handoff_request" } ],
  "persistent_quick_replies": [ { "caption": "Talk to Guillaume" } ],
  "start": "welcome",
  "nodes": { "welcome": { "type": "message", ... } }
}
```

- **Ids** (`^[a-z][a-z0-9_]{0,47}$`) are the node keys. The editor generates them once, on creation, and never rewrites them. Renaming is cosmetic (`ui.label`). If a node is deleted or its id must change, add `tree.redirects: {"old_id": "new_id"}` so contacts parked on it continue.
- **`ui`** (any node, plus `tree.ui`) holds editor metadata: `x`, `y`, `label`, `color`, `collapsed`. Optional; the server ignores it. `notes` holds free-form comments.
- **Versioning:** `dsl_version` = spec (major.minor; a new major means a breaking change). `tree.version` = integer, +1 on every publish. The server keeps every published version; a contact mid-conversation continues on the latest version, resolved through `redirects` (if the node no longer exists and has no redirect, the server logs it and restarts at `start`).
- **Constants** (UPPER_SNAKE) are tree-wide settings (URLs, thresholds). `null` = not set yet. The linter blocks publishing a tree that references an unset constant.
- **Variables** (lower_snake) are per-contact, typed (`string|number|integer|boolean|enum|list`), stored in the **server's own database**. Optional `manychat_field` mirrors a value to ManyChat with `setCustomFieldByName` for visibility only.

## 4. Node types

Shared fields: `type`, optional `notes`, optional `ui`. `say` is a list of messages: a string (text template) or `{ "text": ..., "delay_ms"? }` / `{ "image_url": ..., "delay_ms"? }`. Each item is sent as its own `sendContent`, with human-paced delays (§8). `delay_ms` optionally overrides the wait before that message.

| Type | Kind | Required | Optional | Behavior |
|---|---|---|---|---|
| `message` | pass | `say`, `next` | | Queue messages, continue |
| `ask` | wait | `say`, `extract`, `var` or `save`, `next`, `on_fail` | `quick_replies`, `max_tries`, `retry`, `reminder`, `hide_persistent` | Ask, capture + validate the answer (§5) |
| `choice` | wait | `say`, `options[]` | `var`, `ai_match`, `no_match`, `reminder`, `hide_persistent` | Quick-reply buttons and/or free text → branch |
| `condition` | pass | `branches[{when, next, label}]`, `else` | | First true `when` wins |
| `set` | pass | `assign {var: expr}`, `next` | | Compute variables (in order) |
| `action` | pass | `actions[]`, `next` | `on_error` | Side effects (below) |
| `handoff` | terminal | `reason`, `notify` | `say`, `tags` | Send holding `say`, tag, set `human_handoff`, remove `profit_active`, Slack-alert Phil; bot goes silent |
| `end` | terminal | `outcome` | `say`, `tags`, `quick_replies` | Send `say`, tag, record the outcome, remove `profit_active` |

**Quick replies.** `{ "caption": "≤20 chars", "type": "callback", "when" }`. Every button is a ManyChat `dynamic_block_callback` that POSTs `{contact_id, text: caption}` to `config.inbound_url`, so a tap is processed exactly like a typed message. This includes **Talk to Guillaume** (it is not a ManyChat `node` jump). Max 13 per message, including persistent ones; the linter checks this.

**Choice options.** `{ id, caption, next, synonyms[], ai_hint, show, when }`. `show: false` = not a button, matched only from typed text. `var` stores the chosen option id.

**Action types** (in `actions[]`, run in order). There is no `manychat_flow` / `sendFlow`.
- `{ "type": "set_field", "field": "...", "value": "template" | "expr": "..." }`: optional ManyChat field mirror
- `{ "type": "add_tag" | "remove_tag", "tag": "..." }`
- `{ "type": "notify_slack", "webhook_url", "mention_user_id?", "text?", "include_vars?", "last_messages?" }`: Slack incoming-webhook alert (same shape as `handoff.notify`; see below)
- `{ "type": "webhook", "url", "method", "headers", "body", "timeout_ms", "save": { "var": "$.json.path" } }`: string leaves of `body` are templates; `save` maps JSONPath results into variables
- `{ "type": "log", "event": "...", "data": {} }`: analytics/audit event

On error the action node goes to `on_error` if set, otherwise logs and continues to `next`.

**Handoff node.** Required: `reason`, `notify` (a non-empty list). Optional: holding `say`, `tags`. There is no `flow_ns`. On entry the server: queues `say` and flushes it (the lead's holding message); adds `tags`; `removeTagByName("profit_active")`; sets `human_handoff = true` in its DB (optional ManyChat field mirror); then runs each `notify` entry. After that the bot sends nothing more to this contact until an admin reset (§8).

Each `notify` item is `{ "type": "notify_slack", "webhook_url": "{{SLACK_HANDOFF_WEBHOOK_URL}}", "mention_user_id": "{{SLACK_PHIL_USER_ID}}", "text": "headline template", "include_vars": ["crop", "country", "region", "season_sales", "greenhouse_sqft", "profit_opportunity", "qualified"], "last_messages": 6 }`. The server composes the Slack body: mention `<@id>`, the headline, a line stressing to **reply swiftly**, lead name and IG handle, reason, the listed vars, the last N transcript lines, and a conversation link from `config.livechat_url_template` if set (otherwise a note that Phil can reply in the Instagram app).

## 5. Capturing answers: `ask` + `extract`

```json
"extract": { "method": "ai", "prompt": "…rules…", "output": { "type": "number", "min": 1000, "max": 5000000 } }
```

- **Methods:** `ai` (Claude with `prompt`), `number` (deterministic parse: digits, `k`, `m`), `text` (any non-empty text), `regex` (`pattern`).
- **Output types:** `string | number | integer | boolean | enum (values) | object (fields, required)`. For `object`, the node's `save` maps output fields to variables (e.g. `country`, `region`, `is_english` from one location answer).
- **AI contract.** The server builds the system prompt as `config.ai.system_preamble` + the node `prompt` (rendered, so `{{country}}` etc. give context) + a fixed **output contract** generated from `output` and `global_intents`:
  ```
  Reply with JSON only, one of:
  {"status":"ok","value":<value matching the output type>}
  {"status":"retry","followup":"<one short clarifying question for the lead>"}
  {"status":"intent","intent":"<one of: human, …>"}   // only for intents with ai_description
  ```
  This replaces the earlier "digits only" trick (needed only inside ManyChat). Since the server reads JSON, there's no need to parse Claude's text.
- **Server-side validation** always runs after the AI: type, `min`/`max`, `values`, `required`. A value that fails is treated as `retry`. The AI is never the only gate.
- **Retries.** Every `retry` increments `tries`. If `tries < max_tries` (default `config.default_max_tries`), the server sends the AI's `followup` (`retry.mode: "ai_followup"`) or the fixed `retry.say` (`mode: "fixed"`, also the fallback when the AI gives no follow-up) and stays on the node. When `tries` reaches `max_tries`, it goes to `on_fail`.
- **Suggestions.** `ask.quick_replies` are shortcuts: a tap sends its caption as text, so it goes through the same extraction (e.g. "$50k–$150k" → midpoint 100000).
- **Reminder** (optional): if no answer after `after_minutes` (max 1380 = 23h, inside the window), send `reminder.say` once (`max`). It needs a delayed job; it is cancelled by any inbound message.

**Choice matching order:** (1) exact caption, case-insensitive and trimmed; (2) `synonyms`; (3) if `ai_match`, Claude classifies the text into an option id using `caption` + `ai_hint` (`{"status":"ok","value":"<option_id>"}` or `{"status":"none"}`, or `intent`); (4) no match → `no_match.say` (default: re-send `say`), and after `no_match.max_tries` → `no_match.on_fail` (default: stay).

## 6. Templates and expressions

**Templates** (in `say`, prompts, webhook / Slack fields): `{{name}}` or `{{name | filter}}`. Names are variables, constants, or built-ins `contact.id`, `contact.first_name`, `contact.ig_handle`, `sys.tries`, `sys.last_input`. Filters: `money` ($214,000), `number` (214,000), `upper`, `lower`, `default:"text"`. A missing value renders as empty (use `default`). Templates contain **no logic**: anything computed goes in a `set` node.

**Expressions** (in `condition.when`, `set.assign`, `when` on options/quick replies/intents) use a tiny, safe, **Python/JS-like subset**:

```
expr    := or
or      := and ("or" and)*
and     := not ("and" not)*
not     := "not" not | cmp
cmp     := sum (("=="|"!="|"<"|"<="|">"|">="|"in"|"not in") sum)*
sum     := term (("+"|"-") term)*
term    := unary (("*"|"/"|"%") unary)*
unary   := "-" unary | primary
primary := NUMBER | STRING | "true" | "false" | "null" | "[" [expr ("," expr)*] "]"
         | NAME | ("contact"|"sys") "." NAME | FUNC "(" [expr ("," expr)*] ")" | "(" expr ")"
FUNC    := min | max | round | abs | len | lower | is_set | coalesce
```

Examples: `country in ["US", "CA"] and english_speaker == true` · `profit_opportunity > PROFIT_THRESHOLD` · `max(0, round(greenhouse_sqft * BENCHMARK_PER_SQFT - season_sales))` · `"crop"` (string literal assignment).

Semantics: unknown names = `null`; comparisons `< <= > >=` with `null` are false; arithmetic with `null` is an error (the node fails and goes to `on_error`, or logs and stops); no assignment, no attribute access except `contact.*`/`sys.*`, no user functions, no loops. That keeps it side-effect-free and impossible to abuse.

**Why not JSONLogic?** JSONLogic is safe, but `{"and":[{"in":[{"var":"country"},["US","CA"]]},{">":[{"var":"profit_opportunity"},8000]}]}` is unreadable on an edge label and painful to type. The string subset reads like what Guillaume would write, fits on an edge label, and is ~100 lines to implement in TypeScript (Pratt parser) or Python (the reference uses Python's `ast` with a whitelist). If the editor later wants a visual condition builder, it can compile to and from this same string. JSONLogic stays an option as an alternate *storage* form in a future 1.x (`{"jsonlogic": …}`) without changing semantics.

## 7. Triggers and global intents

**ManyChat inbound gating.** ManyChat is a thin pipe with no business logic. Only PROFIT leads reach the server via Default Reply; other DMs are left untouched.

- The **PROFIT comment-trigger flow** adds tag `profit_active` and forwards the first event to `/ig-inbound` with `"trigger": "profit_comment"` (plus `contact_id`, `name`, `text`). It **sends no message**; the server sends the welcome.
- The **Instagram Default Reply** starts with a Condition: if the contact has `profit_active`, it POSTs `{contact_id, name, text, human_handoff}` to `/ig-inbound`; otherwise it does nothing.
- ManyChat **Live Chat is history only**. It does not trigger handoff and is not driven by `sendFlow`.
- When the interpreter reaches an `end` or `handoff` node, the server removes `profit_active` via `removeTagByName`. Handoff also sets `human_handoff` and Slack-alerts Phil (§4). Later typed DMs from that contact are no longer forwarded.

Rejected alternative: a relay flow via `sendFlow` plus a User Input block to catch the next DM. That loses the server's dynamic quick replies.

**Triggers** start (or restart) the tree. `comment_keyword` is matched by the inbound `trigger` field (`"trigger": "profit_comment"` on the first event from the PROFIT comment flow). `dm_keyword` is matched when the whole DM equals `keyword` (case-insensitive). `new_contact` applies to a contact with no state. `reset_variables` (default true) clears `vars`.

**Global intents** are checked on every inbound message, in any node. `keywords` with `match: "exact"` (the whole message) or `"phrase"` (whole word/phrase anywhere), an optional `when` expression, and `goto`. If an intent has `ai_description`, the AI call already being made for the current node may also return `{"status":"intent","intent":"<id>"}`, so semantic detection costs no extra call. **A caption of the current node's options always wins over a global keyword.** Typical intents: `human` → handoff, `stop` → opt-out end.

`persistent_quick_replies` (max 3) are appended to every waiting node's buttons (unless `hide_persistent: true`), e.g. "Talk to Guillaume". They are always `callback`s: the caption is POSTed to `/ig-inbound` and hits the `human` intent, which goes to a `handoff` node. They are not ManyChat `node` jumps.

## 8. Interpreter semantics (server)

`POST /ig-inbound` → validate the body → **return 200 empty immediately** → process the event. v1 handles events **as they arrive**: no dedup and no per-contact queue (the risk, and the later design, are in §12).

1. **Load state** for `contact_id` (create an empty one if new). Load the published tree (latest `tree.version`).
2. **Record** `last_inbound_at = now`, `last_input = text`, name. Cancel pending reminders.
3. **Human handoff check:** if `state.human_handoff` or the inbound `human_handoff` field (sent by Default Reply) is true → log and stop. **Nothing is sent.** This runs before triggers, so even a new PROFIT comment is ignored until the flag is cleared. Reset is manual only: Phil or Guillaume calls a server admin endpoint (e.g. `POST /admin/handoff/clear` with `contact_id`) and/or clears the mirrored ManyChat field. The reset sets `human_handoff = false` in the server DB; re-add `profit_active` if Default Reply should keep forwarding, or let the lead comment PROFIT again after the flag is clear.
4. **Triggers:** inbound `trigger` id or an exact `dm_keyword` → (reset vars) → go to the trigger's `start`.
5. **Global intents** (keywords, unless a current option caption matches) → `goto`.
6. **Current node input:**
   - waiting node (`ask`/`choice`) → resolve the text (§5): success → set variables → transition to `next`/option `next`; retry → queue the follow-up and **stay**; exhausted → `on_fail`.
   - terminal node (`end`) → `config.on_inbound_after_end`: `ignore` (default; only triggers and global intents act), `restart`, or `handoff`.
   - no state → `start`.
7. **Auto-advance loop** from the target node: apply `redirects`; set `node`, reset `tries`; then
   - `message`: queue `say` → `next` · `set`: evaluate assignments in order (sync `manychat_field`s) → `next` · `condition`: first true branch, or `else` · `action`: **flush queued messages first** (order), run actions → `next` (or `on_error`)
   - `ask`/`choice`: queue `say`, **stop** (wait) · `end`: queue `say`, add tags, record `outcome`, `removeTagByName("profit_active")`, stop · `handoff`: queue holding `say`, flush, add tags, `removeTagByName("profit_active")`, set `human_handoff = true`, POST Slack alert(s) in `notify`, stop. No `sendFlow`.
   - Guard: max 100 steps per inbound event (cycle protection; the linter also flags cycles of pass-through nodes).
8. **Paced send:** each queued message goes out as its own `sendContent` (Dynamic Block v2, `type: "instagram"`), **in the background after the 200**, so delays never hit ManyChat's 10-second timeout. Do not batch several texts into one call.
   - Before the first message after the lead speaks: wait `config.pacing.thinking_ms` (default 1500 ms, about 1–2 s).
   - Before each later message: wait `clamp(base_ms + per_char_ms × length of the previous message, min_ms, max_ms)` (defaults: 800 + 40 ms/character, clamped 1200–4000). A say item may set `delay_ms` to override that wait.
   - Quick replies attach only to the **last** message of the turn (options with `show` + `when`, node `quick_replies`, persistent ones; max 13). Every callback carries `payload: {contact_id, text: caption}` and `url: inbound_url`.
   - A typing indicator may be shown between messages if the ManyChat API supports it for Instagram — **verify**, do not assume it works.
   - If the lead writes again mid-sequence, increment `send_gen` and **cancel** any remaining queued messages for that contact (simple approach: each inbound bumps a generation counter; the send loop bails if it no longer matches).
   - `max_messages_per_send` is only a safety cap on how many messages can be queued for one inbound event, not a batch size.
9. **Persist** state (+ `tree_version`) and log the event, AI calls (prompt, raw reply, parsed result), and API calls.

**24-hour window (API sends only).** Before every `sendContent`: if `human_handoff`, don't send; if `now - last_inbound_at > window_hours`, don't send and log `window_closed`. Native replies in the **Instagram app have no 24-hour limit** and are the intended human path. A ManyChat Live Chat reply after 24 hours would need the 7-day Human Agent tag; Live Chat is otherwise just history. Reminders are capped at 23h. After the API window closes, the bot resumes only when the lead writes again (state is kept) or re-triggers PROFIT after any handoff flag is cleared.

**Failures.** Claude timeout/error → retry once, then treat as `retry` with the fixed `retry.say` (no attempt counted on the first failure). ManyChat API error → retry with backoff (3×), then log; state is still saved, so the next inbound message continues correctly.

## 9. Editor contract

- Nodes = `nodes` entries; position from `ui.x/y` (auto-layout if missing); color by `type`.
- Edges = derived from reference fields (§2), labeled by option caption / branch label / `fail` / `else` / `error`. Entry markers: `start`, each trigger, each global intent target.
- Editing an edge = rewriting the reference field. Deleting a node = the editor asks where its incoming edges go, or adds a redirect.
- **Publish** = schema validation + lint (`validate.py --publish`) + `tree.version += 1` + `updated_at/by`. Lint checks: dangling references, undeclared variables, unknown template names, unparseable expressions, unset constants, quick replies > 13, unreachable nodes (warning).

## 10. PROFIT funnel (`profit-funnel.json`) at a glance

```
[comment PROFIT] → welcome → q_crop (choice: Greenhouse tomatoes / No)
   tomatoes → q_location (ask: AI → country, region, is_english) → c_geo
      US/CA + English → q_sales (ask: AI, $1k–$5M, 3 tries, fail → handoff_numbers)
         → q_sqft (ask: AI, acres/m² → sq ft) → compute_opportunity (set)
         → c_qualified (> PROFIT_THRESHOLD = 8000)
            yes → mark_qualified (tag) → set_qualified → offer (choice: Refine my numbers / Learn on my own)
                     → send_booking (end: BOOKING_URL) | send_masterclass (end: MASTERCLASS_URL)
            no  → dq_low → close_unqualified (end: friendly close + MASTERCLASS_URL)
      else → dq_geo → close_unqualified
   other (No) → dq_crop → close_unqualified
Global: "Talk to Guillaume"/human → handoff_request · "stop" → opt_out
```

Run `python validate.py profit-funnel.json --demo` for an offline simulated conversation.

## 11. Open items

| Item | Notes |
|---|---|
| `BENCHMARK_PER_SQFT` + formula | Placeholder: `max(0, sqft × benchmark − season_sales)`. Guillaume to confirm the benchmark and whether "profit opportunity" = sales gap × margin. The sq ft question exists only for this. |
| `SLACK_HANDOFF_WEBHOOK_URL` | Slack incoming webhook for handoff alerts. Null → publishing blocked. |
| `SLACK_PHIL_USER_ID` | Phil's Slack member id (`<@id>` in the alert). Null → publishing blocked. |
| `config.livechat_url_template` | Optional ManyChat Live Chat URL (with `{{contact.id}}`) for the Slack alert. If unset, the alert tells Phil to reply in the Instagram app. |
| API verification | Confirm Instagram support for `quick_replies`/`dynamic_block_callback` in `sendContent`, and whether a typing indicator can be sent between paced messages. |
| CAD rate | `CAD_TO_USD = 0.73` is a constant; update as needed. |
| Model | `claude-haiku-4-5` set in `config.ai.model`; confirm the exact model id at build time. |

## 12. Out of scope / Later

Deferred past v1 (do not also list these under Open items):

- **PDF guide lead magnet.** v1 sends no guide (`GUIDE_URL` is not a v1 constant). Later: add `GUIDE_URL`, mention it in the welcome, and send the PDF to every lead (qualified and not).
- **Message dedup and out-of-order handling.** v1 processes inbound events as they arrive, with no dedup and no per-contact queue. Duplicate or out-of-order External Requests can therefore repeat a step or apply answers in the wrong order. Later: `config.dedupe_seconds` (hash of contact_id + text, or a ManyChat message id if available) and a worker that processes each contact sequentially (per-contact lock or queue partition).
