# Project state

40hr Farmer landing page and HubSpot automation.

## What

Landing page, HubSpot form + automation, and 5-email welcome sequence for the 40hr Farmer coaching program. Funnel drives to Orisha sales calls for Helper or Chief Grower.

## Why

Waitlist and email funnel live before the May/June 2026 cohort launch.

## Current state (as of 2026-04-15)

### Done

- Phase 1: content extraction and copy refinement.
- Phase 2: landing page built (`index.html` deployed).
- Phase 3: GitHub Pages deploy at https://yormi.github.io/40hr-farmer/
- Phase 4: HubSpot form integration.
- Phase 5: 5 welcome emails written and uploaded to HubSpot.
- Phase 6: HubSpot automation workflow built (disabled, enable when ready).
- GA4 analytics: form conversion + CTA click tracking.
- Photo collection: 14 photos from Ferme Décembre shared album + 66 curated photos from personal library (Aug 2025+) in `assets/clients/ferme-decembre/`.

### Pending

- Set `waitlist_signup` as a key event in GA4 and build a simple report.
- Enable HubSpot workflow (ID below) when ready to go live.
- Funnel conversion optimization pass (the current work).

## Strategic priorities (set 2026-04-16)

### Immediate
**Launch with 50 farmers on the waiting list.** The funnel's near-term job is filling that list before the May/June cohort.

### This quarter
1. Run the program on a weekly cadence.
2. Learn from the users.
3. Push as much of the guidance as possible into the Consultant app, so the playbook gets more self-serve over time.

### This year
**Get 5 new Orisha users per month from the program.** The cohort and funnel exist to feed the paid Orisha product (Helper / Chief Grower) pipeline.

### Bottleneck
**Guillaume's time.** Design work that minimizes his input loops. Prefer automation over coordination. Batch decisions. Default to taking initiative where brand alignment is strong; escalate only when genuinely needed.

## Cohort 1 plan (set 2026-04-17)

- **Start:** May or June 2026.
- **Size:** Small on purpose. The frame is **capacity, not scarcity**. Quote: "Starting smaller with coaching sessions to learn to serve as many farmers as possible as much as possible. Going too fast could ruin that." Drop any "first 50" or "first in" FOMO language in copy.
- **Month 1 teaching goal:** Maximize fruit load without exhausting the plant. Anchored in two real cases: Drew still only reached about half of his plants' carrying capacity in 2025, and Gordon had significant flower abortion. The pattern is widespread across the farmers we have talked to. See [`story-and-origin.md`](story-and-origin.md).
- **Posture:** The playbook is **not finished**. Cohort 1 is where we build it together with the farmers. That is a feature, communicate it honestly.

## Landing-page content decisions (locked 2026-04-17)

Log of decisions already made, so we do not re-litigate them. Does not cover pending drafts.

- **FAQ section shipped** in `index.html` between `#pricing` and `#testimonials` (roughly lines 610 to 717). Intro mailto points to `louis-bernard@orisha.io`. Q4 is written generically so it does not rot when the email sequence changes. Q6 wording ("probably a stretch") is intentionally firm; Guillaume may revisit if the tone feels wrong over time.
- **Drew testimonial updated:** pull quote unchanged, "Read his season" link added pointing to `/drew-season/`. **Do not mention the yield number** (4x, 250%, or 2000 lbs) in the testimonial itself. The lifestyle angle (Allison quitting) is the chosen hook.
- **Drew 15-episode season published** at `drew-season/`. Build script: `scripts/build-drew-season.py`. Cached HubSpot responses: `.cache/drew-emails/` (gitignored).
- **HubSpot API credentials** at `.secrets/hubspot.env` as `HUBSPOT_API_KEY`. `.secrets/` is gitignored.
- **Photo diversity pass done:** Jordane visible in 2 of 8 hero-region slots (down from 4). `drive-0241.jpg` and `drive-0672.jpg` added.
- **Reframe drafts in progress** at `docs/reframe-drafts.md`: new Where-we-are section, light hero sub-headline touch, final CTA rewrite to capacity-not-scarcity. Draft phase, not yet shipped to `index.html`. Another agent may be actively writing to that file; treat as off-limits unless coordinating with Guillaume.
- **Upstream promotion plan** shortened from 11 pages to 4. Final version at `docs/upstream-promotion-plan.md`, treat as frozen.
- **Factual corrections resolved in conversation:**
  - Drop "flooding" from Drew's story. He had **wilted** transplants, not flooding.
  - The "too many tomatoes" line is the **"more cherry tomatoes than all of 2023"** quote from his raw notes.
  - The IG URL informally labeled "2000 lbs" (`C6O7kEZOsdY`) actually shows the Orisha automation caption. The yield proof lives on the Dec 31 2024 year-in-review post (`DEQhrJXORKw`).

## Open items (TBD, do not invent)

- **GFM editorial deadline** for the upstream promotion piece. Need from Andrew at GFM.
- **Third named consulting client** beyond Drew and Gordon. Parked. Do not fabricate one.
- **Pending copy approvals from `docs/reframe-drafts.md`:** hero sub-headline final wording, Where-we-are section final wording, final CTA final wording. All awaiting Guillaume's review.
- **HubSpot API token rotation.** Guillaume pasted the token into chat, so treat it as slightly exposed. Low urgency, but worth rotating when convenient.

## Funnel conversions to optimize

1. Program signup (form submit on landing page).
2. Email open (5-email welcome sequence).
3. Sales call booked with Orisha (Helper or Chief Grower).

## Key IDs

- HubSpot Portal: `5156324`
- HubSpot Form: `036c50fb-2650-48ba-a1af-eb12a8f1074e`
- HubSpot Workflow: `1804689064` (disabled)
- Email IDs: `01=210995615298`, `02=210995615301`, `03=210993395305`, `04=210995615304`, `05=210993395308`

## Key files

- `index.html` — landing page (deployed)
- `email/*.html` — 5 welcome email templates
- `email/HUBSPOT-PROCEDURE.md` — HubSpot API setup docs
- `docs/user-experience-flow.md` — email sequence flow diagram
- `docs/brand/` — brand foundations
- `assets/clients/ferme-decembre/` — farm photos
- `scripts/gphotos_picker.py` + `.secrets/gphotos-oauth-client.json` — Google Photos Picker API (OAuth). `.secrets/` is gitignored.
