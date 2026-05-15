# 40hr Farmer SPEAR — send wave plan

**Status:** Wave 0 sent 2026-05-12. Wave 1 locked 2026-05-14, sending platform switched from Loops.so → Sequenzy → Resend on 2026-05-15.
**Source list:** HubSpot list `1722` — "The 40 Hour Farmer SPEAR" (size 4955 as of 2026-05-13).
**SPEAR copy:** [`promo/orisha-list-spear.md`](orisha-list-spear.md).
**Framework:** Dan Martell single-email SPEAR. CTA = link to landing page (anchor varies per body).
**Sending platform:** Resend. See [Resend broadcast setup](#resend-broadcast-setup-wave-1) below. Compliance footer at [`email/compliance-footer.html`](../email/compliance-footer.html).

## Hero metric

CTR on the landing link → downstream form submit on the 40hr Farmer waitlist.

Open rate is the secondary metric, used only to compare subject-line variants.

## Subject lines (locked, 3-way)

| Variant | Subject | Angle |
|---|---|---|
| A | A path to your dream farm? | Emotional / aspirational |
| B | Cutting farm hours without cutting income | Analytical / promise |
| C | Farming with energy left at the end of the day? | Felt / lifestyle |

Body identical across variants. Sender, reply-to, send time identical across variants.

## Waves

### Wave 0 — canary (150 engaged contacts, 3-way, sent 2026-05-12)

| Field | Value |
|---|---|
| Source | List 1722 + engagement filter: "Marketing email last open date < 61 days ago" |
| Sample | 150 random contacts from engaged sub-segment |
| Split | 50 → A (seed 42), 50 → B (seed 42), 50 → C (seed 43, drawn from pool minus A∪B) |
| Read window | 24h |
| Platform | HubSpot |

**Results (24h window):**

| Variant | Subject | Open | Click |
|---|---|---|---|
| A | A path to your dream farm? | 34% | 0% |
| B | Cutting farm hours without cutting income | 38% | 6% |
| C | Farming with energy left at the end of the day? | 34% | 6% |

**Read:** Subject B leads on opens. B and C tied on click; no clear 1.5× click winner per decision gate. Click rates (0 to 6%) signal the **body** is the bottleneck (it was identical across A/B/C). Subject was off-axis from body (subjects promised hours/income/energy; body opened on energy-for-people only). Decision: lock subject B for Wave 1; ship a new body aligned to the subject's promise.

### Wave 1 — engaged remainder (locked 2026-05-14)

| Field | Value |
|---|---|
| Source | Engaged sub-segment minus Wave 0 contacts |
| Audience size | **852** (built via `scripts/spear-wave1-build.py`; HubSpot static list `1732` for parity; CSV at `promo/spear-wave1-audience.csv`) |
| Variant A | **Subject:** "Cutting farm hours without cutting income". **Body:** Mechanism / How. CTA → `#leverage`, `utm_content=wave1-howto`. |
| Variant B | **Subject:** "Making the farm pay for the life you want". **Body:** Flip / Drew & Allison. CTA → `#story`, `utm_content=wave1-flip`. |
| Both locked in | [`orisha-list-spear.md`](orisha-list-spear.md) |
| Platform | Resend. See [Resend broadcast setup](#resend-broadcast-setup-wave-1) below. |
| Read window | 48h |
| Metrics | Same as Wave 0 (open + click via Resend tracking on `learn.orisha.io`), plus baseline numbers for Wave 2 expectations |

**Subject design:** A/B run two distinct subject lines paired with two distinct bodies (subject A ↔ body A, subject B ↔ body B), splitting the 852-contact audience 50/50. Wave 2+ subject will be re-decided after Wave 1 results.

**Platform-switch audit trail (2026-05-15):** Wave 1 was originally set up on Loops.so (audience pushed via the now-defunct `scripts/spear-wave1-loops-sync.py`, tagged `spearWave1 = yield`). Migrated to Sequenzy briefly, then off Sequenzy to Resend the same day — full reasoning in memory note `project-email-platform-resend`. The Loops sync script is dead; Sequenzy sequences are abandoned drafts in the Sequenzy dashboard.

### Wave 2+ — cold remainder (~3939 contacts)

| Field | Value |
|---|---|
| Source | List 1722 minus everyone sent in Waves 0–1 |
| Chunking | ~500/day, Tue–Thu only |
| Subject | Same winner as Wave 1 |
| Cadence | One chunk per day, ~8 sending days total |

## Kill-switch thresholds (per wave or per chunk)

Pause and recalibrate if any of these trip:

- Hard bounce rate > 2%
- Spam complaint rate > 0.1%
- Unsubscribe rate > 4% (for cold; 2% for engaged)

Between chunks: suppress hard bounces from prior chunks so the bad-address contamination doesn't compound.

## Tracking

Landing link UTM scheme:

| Param | Value |
|---|---|
| `utm_source` | `orisha-email` |
| `utm_medium` | `email` |
| `utm_campaign` | `spear-2026-05` |
| `utm_content` | Wave 0: `subject-a` / `subject-b` / `subject-c`. Wave 1: `wave1-howto` (Body A) / `wave1-flip` (Body B). |

Wave 0 URLs:
- Variant A: `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=subject-a`
- Variant B: `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=subject-b`
- Variant C: `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=subject-c`

Wave 1 URLs:
- Body A (Mechanism / How): `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=wave1-howto#leverage`
- Body B (Flip / Drew & Allison): `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=wave1-flip#story`

Downstream conversion = waitlist form submit (already tracked, triggers the welcome workflow).

## Personalization

- First-name token with `there` fallback.
  - HubSpot (welcome workflow): `{{contact.firstname | default("there")}}`.
  - Resend (SPEAR broadcasts): `{{{FIRST_NAME|there}}}` (triple braces, pipe-fallback).
- No other personalization in the body.

## Suppression (already handled by list 1722 filters)

- Not in welcome workflow (filtered by "has not submitted 40hr Farmer Waitlist form")
- Marketing-contact status only
- English language only
- Excludes "Others" and "Not a Client Anymore" lifecycle stages

## Send config

- **Wave 0 send time:** Tuesday 6:00 AM ET (sent 2026-05-12).
- **Wave 1 send time:** TBD pending second body lock and smoke test.
- **Sender name:** Guillaume Lambert.
- **Reply-to:** `guillaume@orisha.io`.
- **Engagement filter (Wave 0 + Wave 1 source pool):** Marketing email last open date < 61 days ago. On 2026-05-13 the pool was 999 contacts (150 sent in Wave 0, 852 remain for Wave 1).

Hard-bounce-history exclusion is optional; not currently in list 1722. HubSpot auto-suppresses at send time. Resend auto-suppresses unsubscribes (via the `{{{RESEND_UNSUBSCRIBE_URL}}}` token) and bounces.

## Resend broadcast setup (Wave 1)

Domain `orisha.io` is verified in Resend (DKIM + SPF + tracking CNAME on `learn.orisha.io`, all set 2026-05-15). Compliance footer lives at [`email/compliance-footer.html`](../email/compliance-footer.html) and is included verbatim at the bottom of each body.

### Audience prep

Run `python scripts/spear-wave1-resend-import.py --push` (idempotent). It:

1. Reads `promo/spear-wave1-audience.csv` (852 rows: `email,firstname,contactId`).
2. Deterministically shuffles with seed `42` and splits 50/50 (426 / 426).
3. Creates or finds two audiences in Resend: `SPEAR Wave 1 — A (Mechanism)` and `SPEAR Wave 1 — B (Flip)`. Two audiences instead of one with a Segment because Segments are paid-plan-only; pre-split audiences keep the broadcast config simple on any tier.
4. Writes the sync log + audience IDs to `promo/spear-wave1-resend-sync.log.json`.

**Plan-tier note:** Resend free tier caps at 3 audiences total. The "General" default + A + B uses all three; any new audience needs one deleted first.

### Per-broadcast config (do this twice — once for A, once for B)

| Field | Variant A | Variant B |
|---|---|---|
| Name | `SPEAR Wave 1 — Body A (Mechanism)` | `SPEAR Wave 1 — Body B (Flip)` |
| Subject | `Cutting farm hours without cutting income` | `Making the farm pay for the life you want` |
| From | `Guillaume <guillaume@orisha.io>` | same |
| Reply-To | `guillaume@orisha.io` | same |
| Audience | Wave 1 sub-audience A | Wave 1 sub-audience B |
| Body | Locked copy from [`orisha-list-spear.md`](orisha-list-spear.md) Body A | Locked copy Body B |
| Personalization token | `{{{FIRST_NAME\|there}}}` | same |
| CTA URL | Wave 1 URL A above (`#leverage`, `utm_content=wave1-howto`) | Wave 1 URL B above (`#story`, `utm_content=wave1-flip`) |
| Footer | Drop in `email/compliance-footer.html` verbatim | same |

### Required body tokens (gotchas)

- **`{{{RESEND_UNSUBSCRIBE_URL}}}` MUST appear in the body.** Resend's `POST /broadcasts` with `send: true` silently sets `status: failed` and never delivers if it's missing — no error message. The compliance footer includes it.
- HTTP requests to Resend's API (`api.resend.com`) need a `User-Agent` header or Cloudflare returns 403 / error 1010.

### Procedure

1. Create both broadcasts via `POST /broadcasts` with `send: false` (drafts).
2. `POST /broadcasts/{id}/test` to send a preview to `guillaume@orisha.io` for each. Verify in inbox: subject, first-name token resolved, link wrapped through `learn.orisha.io`, footer renders as a single grey line, landing page loads, downstream waitlist form submit triggers the HubSpot welcome workflow.
3. After both tests pass, `POST /broadcasts/{id}` with `{"send": true}` (or click Send in the dashboard) for both, simultaneously.
4. Monitor open/click events via `GET /emails/{id}` or webhooks; aggregate stats appear on the broadcast detail page.

### Cross-system unsubscribe sync

Closed by `scripts/sync-resend-unsubscribes-to-hubspot.py` + the GitHub Action at `.github/workflows/sync-unsubscribes.yml`. The action runs hourly: iterates every Resend audience, finds contacts with `unsubscribed: true`, calls HubSpot's v1 `PUT /email/public/v1/subscriptions/{email}` with `{"unsubscribeFromAll": true}`. Idempotent — re-running is safe.

**One-time setup** (the action won't run until both are set):

1. In the GitHub repo, add two Actions secrets: `RESEND_API_KEY` and `HUBSPOT_API_KEY` (Settings → Secrets and variables → Actions).
2. Confirm the HubSpot private app token has the `marketing-email` (or equivalent) scope for the v1 subscriptions endpoint.

Lag: up to ~1 hour between a Resend unsubscribe and HubSpot reflection. Acceptable for the CASL window because the welcome workflow sends at most a few emails/day. If the lag becomes a real problem, swap the cron for a Resend webhook bridge (Cloudflare Worker, ~30 min).
