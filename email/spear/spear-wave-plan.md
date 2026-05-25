# 40hr Farmer SPEAR — send wave plan

**Status:** Wave 0 sent 2026-05-12 (HubSpot). Wave 1 sent via **Resend** to the full 852-contact engaged-remainder audience (50/50 Body A / Body B) between 2026-05-15 and 2026-05-22, before Resend was dropped. Exact send date + results recap TBD. ESP now locked: **Postmark** (2026-05-25). Future SPEAR waves go through Postmark broadcast streams.
**Source list:** HubSpot list `1722` — "The 40 Hour Farmer SPEAR" (size 4955 as of 2026-05-13).
**SPEAR copy:** [`orisha-list-spear.md`](orisha-list-spear.md).
**Framework:** Dan Martell single-email SPEAR. CTA = link to landing page (anchor varies per body).
**Sending platform:** Postmark (broadcast stream `broadcast`). Compliance footer at [`email/compliance-footer.html`](../compliance-footer.html) with `{{{ pm:unsubscribe }}}` wired.

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
| Audience size | **852** (built via `email/spear/scripts/spear-wave1-build.py`; HubSpot static list `1732` for parity; CSV at `email/spear/spear-wave1-audience.csv`) |
| Variant A | **Subject:** "Cutting farm hours without cutting income". **Body:** Mechanism / How. CTA → `#leverage`, `utm_content=wave1-howto`. |
| Variant B | **Subject:** "Making the farm pay for the life you want". **Body:** Flip / Drew & Allison. CTA → `#story`, `utm_content=wave1-flip`. |
| Both locked in | [`orisha-list-spear.md`](orisha-list-spear.md) |
| Platform | **Sent via Resend** between 2026-05-15 and 2026-05-22 (exact date TBD). |
| Read window | 48h |
| Metrics | Open + click via Resend tracking. Results recap TBD — retrieve from Resend archive before Resend account is closed. |

**Subject design:** A/B run two distinct subject lines paired with two distinct bodies (subject A ↔ body A, subject B ↔ body B), splitting the 852-contact audience 50/50. Wave 2+ subject will be re-decided after Wave 1 results.

**Platform history (2026-05-15 → 2026-05-25):** Originally set up on Loops.so (audience pushed via sync script, tagged `spearWave1 = yield`). Migrated to Sequenzy briefly, then off Sequenzy to Resend on 2026-05-15. **Wave 1 sent on Resend** before Resend itself was dropped 2026-05-22. ESP locked on Postmark 2026-05-25 after eval test send. Loops sync script, Sequenzy drafts, and Resend scripts have all been deleted from the repo.

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
  - SPEAR broadcasts: ESP-specific syntax TBD; re-lock once ESP picked.
- No other personalization in the body.

## Suppression (already handled by list 1722 filters)

- Not in welcome workflow (filtered by "has not submitted 40hr Farmer Waitlist form")
- Marketing-contact status only
- English language only
- Excludes "Others" and "Not a Client Anymore" lifecycle stages

## Send config

- **Wave 0 send time:** Tuesday 6:00 AM ET (sent 2026-05-12).
- **Wave 1 send time:** Sent via Resend between 2026-05-15 and 2026-05-22 (exact timestamp TBD).
- **Sender name:** Guillaume Lambert.
- **Reply-to:** `guillaume@orisha.io`.
- **Engagement filter (Wave 0 + Wave 1 source pool):** Marketing email last open date < 61 days ago. On 2026-05-13 the pool was 999 contacts (150 sent in Wave 0, 852 remain for Wave 1).

Hard-bounce-history exclusion is optional; not currently in list 1722. HubSpot auto-suppresses at send time. ESP auto-suppression behavior to be re-verified once ESP is picked.

## Postmark setup (for Wave 2+ and future SPEAR sends)

**Status (2026-05-25):** Postmark locked. Wave 1 already sent via Resend; this section is the template for Wave 2 onward.

- Postmark account verified for `orisha.io` (DKIM + Return-Path + tracking CNAME on `learn.orisha.io`).
- Server token in `.secrets/postmark.env` (`POSTMARK_SERVER_TOKEN`). Default broadcast stream id: `broadcast`.
- Audience split (per wave): pull from the relevant audience CSV in `email/spear/`, seed-42 split for reproducibility.
- Per-broadcast config:
  - Variant config (subject + body + UTM) sourced from [`orisha-list-spear.md`](orisha-list-spear.md).
  - From: `Guillaume <guillaume@orisha.io>`; reply-to: `guillaume@orisha.io`.
  - Compliance footer: drop in `email/compliance-footer.html` verbatim. Footer's `{{{ pm:unsubscribe }}}` resolves automatically on the broadcast stream.
- First-name token: Postmark Mustache syntax `{{name "there"}}` with `there` fallback (template-driven sends) or render server-side per recipient (API sends).
- Test send to `guillaume@orisha.io`: verify subject, first-name token resolved, Postmark link wrapping, footer rendering, landing page load, downstream HubSpot waitlist-form trigger.
- Cross-system unsubscribe sync: wire `scripts/sync-esp-unsubscribes-to-hubspot.py` against Postmark suppression list (`GET /message-streams/{stream}/suppressions/dump`). Workflow `.github/workflows/sync-unsubscribes.yml` cron still commented out.
