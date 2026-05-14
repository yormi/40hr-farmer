# 40hr Farmer SPEAR — send wave plan

**Status:** Wave 0 sent 2026-05-12. Wave 1 locked 2026-05-14 (subject + 2-body A/B), on Loops.so.
**Source list:** HubSpot list `1722` — "The 40 Hour Farmer SPEAR" (size 4955 as of 2026-05-13).
**SPEAR copy:** [`promo/orisha-list-spear.md`](orisha-list-spear.md).
**Framework:** Dan Martell single-email SPEAR. CTA = link to landing page (`#leverage` anchor).

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
| Audience size | **852** (built via `scripts/spear-wave1-build.py`; HubSpot static list `1732` for parity) |
| Subject | Making the farm pay for the life you want |
| Bodies (A/B) | A: Mechanism / How. B: Flip / Drew & Allison. Both locked in [`orisha-list-spear.md`](orisha-list-spear.md). |
| Platform | Loops.so (audience pushed via `scripts/spear-wave1-loops-sync.py`, tagged `spearWave1 = yield`; tag will be re-split into `wave1-howto` / `wave1-flip` before send) |
| Read window | 48h |
| Metrics | Same as Wave 0, plus baseline numbers for Wave 2 expectations |

**Subject change note (2026-05-14):** Wave 0 winner subject ("Cutting farm hours without cutting income") was dropped in favor of "Making the farm pay for the life you want" alongside the body refresh. Wave 2+ subject will be re-decided after Wave 1 results.

Split the 852 audience 50/50 between Body A and Body B; `utm_content` differs per body (`wave1-howto` vs `wave1-flip`).

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
- Body B (Flip / Drew & Allison): `https://the40hourfarmer.orisha.io/?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05&utm_content=wave1-flip#leverage`

Downstream conversion = waitlist form submit (already tracked, triggers the welcome workflow).

## Personalization

- First-name token with `there` fallback (HubSpot: `{{contact.firstname | default("there")}}`).
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

Hard-bounce-history exclusion is optional; not currently in list 1722. HubSpot auto-suppresses at send time. Loops auto-suppresses unsubscribes/bounces on its end.

## Loops.so campaign setup (Wave 1)

Audience is pre-tagged in Loops with custom field `spearWave1 = "yield"` (852 contacts as of 2026-05-13). Before the smoke test, re-split that tag 50/50 into `wave1-howto` and `wave1-flip` so each body has its own audience filter. Then, for each body in the Loops dashboard:

1. **Campaigns → New campaign.** Name: "SPEAR Wave 1 — Mechanism (A)" / "SPEAR Wave 1 — Flip (B)".
2. **Audience filter:** `spearWave1` equals `wave1-howto` (A) or `wave1-flip` (B). Each should resolve to ~426 contacts.
3. **Subject (both):** `Making the farm pay for the life you want`.
4. **From name:** `Guillaume Lambert`. **Reply-to:** `guillaume@orisha.io`.
5. **Body:** paste the matching body from [`orisha-list-spear.md`](orisha-list-spear.md) Wave 1 section. First-name token: `{{firstName | default: "there"}}` (Loops Liquid). CTA href: the matching Wave 1 URL above (Body A → `wave1-howto`, Body B → `wave1-flip`).
6. **Send test** of each campaign to `guillaume@orisha.io` from the campaign editor. Verify: subject, token resolution, link with UTM, landing page loads, downstream form submit triggers the welcome workflow.
7. After both tests pass, send both campaigns simultaneously.
