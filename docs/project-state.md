# Project state

40hr Farmer landing page and HubSpot automation.

## What

Landing page, HubSpot form + automation, and 5-email welcome sequence for the 40hr Farmer coaching program. Funnel drives to Orisha sales calls for Helper or Chief Grower.

## Why

Waitlist and email funnel live before the June 2026 cohort launch.

## Current state (as of 2026-04-23)

### Done

- Phase 1: content extraction and copy refinement.
- Phase 2: landing page built (`index.html` deployed).
- Phase 3: GitHub Pages deploy at https://yormi.github.io/40hr-farmer/
- Phase 4: HubSpot form integration.
- Phase 5: 5 welcome emails written and uploaded to HubSpot.
- Phase 6: HubSpot automation workflow built (disabled, enable when ready).
- GA4 analytics: form conversion + CTA click tracking.
- Photo collection: 14 photos from Ferme Décembre shared album + 66 curated photos from personal library (Aug 2025+) in `assets/clients/ferme-decembre/`.
- **Landing page rework under reader-type-first method** — step-1 page intent + step-2 section intents + step-3 decompositions all locked in `docs/landing/outline.md`. Step-4 locked copy now covers: Hero (Gut), Drew arc (Peer Sub 1), What a bed can buy back (Peer Sub 2), Analytical Subs 1–4, Practical Subs 1–3, Team section (Committer Sub 1 including all three bios + framing + closer), and Committer Sub 2 Beat 1 (why today).

### Pending

- Set `waitlist_signup` as a key event in GA4 and build a simple report.
- Enable HubSpot workflow (ID below) when ready to go live.
- **Landing page step-4 remaining:** Committer Sub 2 Beats 2–4 (what-happens-after-signup, form, disclosures), "What it starts to feel like" placement decision, FAQ re-draft under the reader-type-first method.
- **Landing page step-5 + step-6** (scannable structure + HTML render) — the new working approach is section-by-section: walk through steps 5 and 6 for Hero first, then each subsequent section, addressing any remaining step-4 gaps as they come up.

## New working approach (set 2026-04-23)

Instead of locking every section's step-4 prose before moving on, we now advance section-by-section through steps 5 (scannable structure) and 6 (HTML render) in page order (Hero → Drew → ...). If a section still has unlocked prose when we reach it, we finish step 4 for that section in-line, then continue.

The reason: most sections are prose-locked; further waiting for the last few unlocked beats would delay visible progress. Step-5 structure decisions and step-6 render work can also surface weaknesses in the locked prose, which sends us back to step 4 with a sharper question than pure-prose review would.

## Strategic priorities (set 2026-04-16)

### Immediate
**Launch with 50 farmers on the waiting list.** The funnel's near-term job is filling that list before the May cohort.

### This quarter
1. Run the program on a weekly cadence.
2. Learn from the users.
3. Push as much of the guidance as possible into the Consultant app, so the playbook gets more self-serve over time.

### This year
**Get 5 new Orisha users per month from the program.** The cohort and funnel exist to feed the paid Orisha product (Helper / Chief Grower) pipeline.

### Bottleneck
**Guillaume's time.** Design work that minimizes his input loops. Prefer automation over coordination. Batch decisions. Default to taking initiative where brand alignment is strong; escalate only when genuinely needed.

## Cohort 1 plan (set 2026-04-17)

- **Start:** June 2026.
- **Size:** Small on purpose. The frame is **capacity, not scarcity**. Quote: "Starting smaller with coaching sessions to learn to serve as many farmers as possible as much as possible. Going too fast could ruin that." Drop any "first 50" or "first in" FOMO language in copy.
- **Month 1 teaching goal:** Maximize fruit load without exhausting the plant. Anchored in two real cases: Drew still only reached about half of his plants' carrying capacity in 2025, and Gordon had significant flower abortion. The pattern is widespread across the farmers we have talked to. See [`brand/docs/internal/story-and-origin.md`](../brand/docs/internal/story-and-origin.md).
- **Posture:** The playbook is **not finished**. Cohort 1 is where we build it together with the farmers. That is a feature, communicate it honestly.

## Team (updated 2026-04-23)

Three people show up on the live coaching calls:

- **Guillaume** (Orisha founder).
- **Antoine** — 2-acre market gardener, crisis-turnaround veteran, 4x greenhouse tomato yields.
- **Andrew Mefferd** — *Greenhouse and Hoophouse Grower's Handbook* author, GFM editor + podcast host.

**Louis-Bernard (LB)** hosts the community forum between calls — **not on the live calls**. Orisha is the backing company.

Canonical bios, framing, and closer are locked in `docs/landing/outline.md` (Team section). Brand-level story context in [`brand/docs/internal/story-and-origin.md`](../brand/docs/internal/story-and-origin.md).

## Ferme Décembre (Guillaume's farm project)

- Started 2025 with Guillaume's partner.
- Target 2026: $500k revenue with 4 employees.
- Purpose: live test of the 40hr farm playbook. Feeds real-time input to the coaching calls.
- Photos: `assets/clients/ferme-decembre/`.

## Landing-page content decisions (locked 2026-04-17)

Log of decisions already made, so we do not re-litigate them. Does not cover pending drafts.

- **FAQ section shipped** in `index.html` between `#pricing` and `#testimonials` (roughly lines 610 to 717). Intro mailto points to `louis-bernard@orisha.io`. Q4 is written generically so it does not rot when the email sequence changes. Q6 wording ("probably a stretch") is intentionally firm; Guillaume may revisit if the tone feels wrong over time.
- **Drew testimonial updated:** pull quote unchanged, "Read his season" link added pointing to `/drew-season/`. **Do not mention the yield number** (4x, 250%, or 2000 lbs) in the testimonial itself. The lifestyle angle (Allison quitting) is the chosen hook.
- **Drew 15-episode season published** at `drew-season/`. Build script: `scripts/build-drew-season.py`. Cached HubSpot responses: `.cache/drew-emails/` (gitignored).
- **HubSpot API credentials** at `.secrets/hubspot.env` as `HUBSPOT_API_KEY`. `.secrets/` is gitignored.
- **Photo diversity pass done:** Jordane visible in 2 of 8 hero-region slots (down from 4). `drive-0241.jpg` and `drive-0672.jpg` added.
- **Landing rework in progress** in `docs/landing/` (process.md, outline.md, sources/). The older reframe-drafts.md and option1-landing-draft.md have been retired; their best material flowed into the current outline. Working doc for the reader-type-first rework is `docs/landing/outline.md`, which holds both the page structure and all locked copy.
- **Upstream promotion plan** shortened from 11 pages to 4. Final version at `docs/upstream-promotion-plan.md`, treat as frozen.
- **Factual corrections resolved in conversation:**
  - Drop "flooding" from Drew's story. He had **wilted** transplants, not flooding.
  - The "too many tomatoes" line is the **"more cherry tomatoes than all of 2023"** quote from his raw notes.
  - The IG URL informally labeled "2000 lbs" (`C6O7kEZOsdY`) actually shows the Orisha automation caption. The yield proof lives on the Dec 31 2024 year-in-review post (`DEQhrJXORKw`).

## Open items (TBD, do not invent)

- **GFM editorial deadline** for the upstream promotion piece. Need from Andrew at GFM.
- **Pending landing-copy work in `docs/landing/outline.md`:** see the Status markers per section. Remaining: Committer Sub 2 Beats 2–4 (what-happens-after-signup, form, disclosures), "What it starts to feel like" placement decision, FAQ re-draft under the reader-type-first method.
- **HubSpot API token rotation.** Guillaume pasted the token into chat, so treat it as slightly exposed. Low urgency, but worth rotating when convenient.

## Funnel conversions to optimize

1. Program signup (form submit on landing page).
2. Email open (5-email welcome sequence).
3. Sales call booked with Orisha (Helper or Chief Grower).

## Key IDs

- HubSpot Portal: `5156324`
- HubSpot Form: `7f28cb26-8aea-432e-bf7f-c50a1484d0a3` (V3, API-managed, replaces V4 form `036c50fb-…` retired 2026-05-04)
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
