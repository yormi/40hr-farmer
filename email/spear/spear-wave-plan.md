# 40hr Farmer SPEAR — send wave plan

**Status:** Wave 0 sent 2026-05-12. Wave 1 locked 2026-05-14 but **send is paused** — ESP not chosen (Loops → Sequenzy → Resend all dropped between 2026-05-15 and 2026-05-22; evaluating Postmark next).
**Source list:** HubSpot list `1722` — "The 40 Hour Farmer SPEAR" (size 4955 as of 2026-05-13).
**SPEAR copy:** [`orisha-list-spear.md`](orisha-list-spear.md).
**Framework:** Dan Martell single-email SPEAR. CTA = link to landing page (anchor varies per body).
**Sending platform:** TBD pending ESP pick. See [ESP broadcast setup](#esp-broadcast-setup-wave-1) below. Compliance footer scaffold at [`email/compliance-footer.html`](../compliance-footer.html).

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
| Platform | TBD pending ESP pick. See [ESP broadcast setup](#esp-broadcast-setup-wave-1) below. |
| Read window | 48h |
| Metrics | Same as Wave 0 (open + click via ESP tracking on `learn.orisha.io`), plus baseline numbers for Wave 2 expectations |

**Subject design:** A/B run two distinct subject lines paired with two distinct bodies (subject A ↔ body A, subject B ↔ body B), splitting the 852-contact audience 50/50. Wave 2+ subject will be re-decided after Wave 1 results.

**Platform-switch audit trail (2026-05-15 → 2026-05-22):** Wave 1 was originally set up on Loops.so (audience pushed via a sync script, tagged `spearWave1 = yield`). Migrated to Sequenzy briefly, then off Sequenzy to Resend on 2026-05-15, then Resend dropped on 2026-05-22. Evaluating Postmark next. Loops sync script, Sequenzy drafts, and Resend scripts have all been deleted from the repo.

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
- **Wave 1 send time:** TBD pending second body lock and smoke test.
- **Sender name:** Guillaume Lambert.
- **Reply-to:** `guillaume@orisha.io`.
- **Engagement filter (Wave 0 + Wave 1 source pool):** Marketing email last open date < 61 days ago. On 2026-05-13 the pool was 999 contacts (150 sent in Wave 0, 852 remain for Wave 1).

Hard-bounce-history exclusion is optional; not currently in list 1722. HubSpot auto-suppresses at send time. ESP auto-suppression behavior to be re-verified once ESP is picked.

## ESP broadcast setup (Wave 1)

**Status (2026-05-22):** ESP not chosen. Loops, Sequenzy, and Resend all dropped. Evaluating Postmark next. This section is a checklist of what must be re-locked before Wave 1 can send:

- ESP picked + `orisha.io` domain verified (DKIM + SPF + tracking CNAME on `learn.orisha.io`).
- Audience split: 426/426 from `email/spear/spear-wave1-audience.csv` (852 rows, seed 42, idempotent).
- Per-broadcast config (twice — once per variant):
  - Variant A: `SPEAR Wave 1 — Body A (Mechanism)`, subject `Cutting farm hours without cutting income`, body from [`orisha-list-spear.md`](orisha-list-spear.md), CTA → `#leverage` + `utm_content=wave1-howto`.
  - Variant B: `SPEAR Wave 1 — Body B (Flip)`, subject `Making the farm pay for the life you want`, body from [`orisha-list-spear.md`](orisha-list-spear.md), CTA → `#story` + `utm_content=wave1-flip`.
  - From: `Guillaume <guillaume@orisha.io>`; reply-to: `guillaume@orisha.io`.
  - Compliance footer: drop in `email/compliance-footer.html` verbatim; re-bind the unsubscribe merge token to the ESP's syntax (currently a generic `{{ unsubscribe_url }}` placeholder).
- First-name token: re-lock the ESP-specific syntax with a `there` fallback.
- Test send to `guillaume@orisha.io`: verify subject, first-name token resolved, link wrapping, footer rendering, landing page load, and downstream HubSpot waitlist-form trigger.
- Cross-system unsubscribe sync: re-point `scripts/sync-esp-unsubscribes-to-hubspot.py` at the new ESP's unsubscribe-list endpoint. Workflow `.github/workflows/sync-unsubscribes.yml` runs hourly and is currently a scaffold awaiting ESP wiring.
