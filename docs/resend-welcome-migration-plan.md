# Welcome sequence: HubSpot → Resend migration plan

Drafted 2026-05-15. Surface for review before any execution.

## Summary

Move the 5-email welcome sequence off HubSpot (where the workflow is still
**disabled** and has never sent live) onto **Resend Automations**, which
shipped a native drip primitive (event-triggered, time-delayed, multi-step,
API-first). HubSpot stays as the CRM: form, contact properties, list,
unsubscribe sync. Resend takes over all sending for the welcome funnel.

This is the cleanest possible migration moment — no in-flight contacts to
care about, no live drip to cut over, just switching tech before launch.

## Starting position (today)

| Piece | Where it lives | State |
|---|---|---|
| Landing page form submit | HubSpot Forms v3 (`7f28cb26-…`) | Live |
| Contact record + custom props | HubSpot CRM | Live |
| 5 email HTMLs | `email/welcome-sequence/0[1-5]-*.html` (repo) + HubSpot Email shells | Authored, shells exist |
| Welcome workflow | HubSpot Workflow `1804689064` | **Disabled, never enabled** |
| Resend Audiences | SPEAR Wave 1 A/B (broadcast use) | Live |
| Resend → HubSpot unsubscribe sync | `.github/workflows/sync-unsubscribes.yml` | Hourly cron, live |

## Target architecture

```
Browser form submit
   │
   ▼
HubSpot Forms API  ───►  HubSpot Contact created
                                │
                                ▼
                  GitHub Action cron (every 5–10 min)
                                │
                                ▼
                  POST resend.com/events/send
                  { event: "welcome_signup",
                    email, payload: { firstname, farm_name, deal flags } }
                                │
                                ▼
                  Resend Automation (welcome_signup trigger)
                                │
                  Send 01 ─► 3d ─► 02 ─► 3d ─► 03 ─► 3d ─► 04 ─► 4d ─► 05
                                │
                                ▼
                  Resend Audience "40hr Farmer — Waitlist"
                                │
                                ▼
                  (existing hourly unsubscribe sync brings unsubs back to HubSpot)
```

## The one open architectural choice — form-submit bridge

How does a HubSpot form submit reach Resend? Three options:

| # | Mechanism | Latency to Email 01 | New infra | Risk |
|---|---|---|---|---|
| A | **GitHub Action cron (every 5–10 min)** poll HubSpot for new contacts → fire Resend event. Mirrors existing unsubscribe-sync pattern. | 5–10 min | None (reuses Actions) | Low |
| B | **HubSpot workflow webhook action** → tiny Cloudflare Worker / Vercel function → Resend `/events/send`. | Seconds | One hosted endpoint | Medium (one more thing to keep alive) |
| C | **Browser dual-fire**: page submits to HubSpot AND directly to Resend `/events/send`. | Seconds | None | High — Resend API key in browser, spam/abuse vector |

**Recommendation: A.** Reuses the pattern Guillaume already validated for
unsubscribe sync. 5-min delay on the first email is invisible to users (and
arguably nicer — they get their thank-you state in the browser, then the email
a few minutes later). No new hosted endpoint to monitor. Idempotency lives on
a single HubSpot contact property (`resend_welcome_fired_at`).

## Phases

### Phase 1 — Build Resend side (no HubSpot changes yet)

1. Create Resend Audience: **"40hr Farmer — Waitlist"** (production) + **"40hr Farmer — Test"** (smoke tests).
2. Port 5 email HTMLs to Resend Templates. Adapt personalization syntax (`{{contact.firstname | default("there")}}` → Resend's Liquid `{{ FIRST_NAME | default: "there" }}`). Confirm compliance footer + auto-injected unsubscribe link both render.
3. Define custom event `welcome_signup` (payload schema: `firstname`, `farm_name`, `forty_hour_farmer_deal`).
4. Build the Automation: trigger `welcome_signup` → send 01 → wait 3d → 02 → wait 3d → 03 → wait 3d → 04 → wait 4d → 05.
5. Fire a manual test event to `guillaume+resend-test@orisha.io`, verify Email 01 lands and Run shows in Resend dashboard. *(Don't wait 13 days — verify the steps fire by editing the delays to 1 min for the test pass, then restoring.)*

### Phase 2 — Build the bridge

6. `scripts/sync-hubspot-signups-to-resend.py`:
   - Queries HubSpot for contacts where `resend_welcome_fired_at` is empty AND created within last N hours.
   - Fires `POST /events/send` to Resend, payload from HubSpot contact properties.
   - Stamps `resend_welcome_fired_at` on the contact (idempotency guard).
7. `.github/workflows/sync-hubspot-signups.yml`: cron `*/10 * * * *`, reuses `RESEND_API_KEY` + `HUBSPOT_API_KEY` repo secrets.
8. Create the `resend_welcome_fired_at` custom contact property in HubSpot (datetime).

### Phase 3 — End-to-end smoke test

9. Write a new smoke-test script `scripts/test-welcome-funnel.sh`: submit through HubSpot Forms API → poll HubSpot for contact creation → wait up to 12 min for the sync cron → query Resend `/automations/runs` for a run on that email → query Resend `/emails` for a `delivered` event on Email 01 → delete the test contact from both systems. (The old HubSpot-only version was deleted 2026-05-15.)
10. Run the smoke test. If green, Phase 4. If red, debug without touching HubSpot side.

### Phase 4 — Retire HubSpot email path (only after smoke test green)

11. Delete HubSpot workflow `1804689064`.
12. Archive the 5 HubSpot email shells (UI archive or API DELETE).
13. Write `email/welcome-sequence/RESEND-PROCEDURE.md` as the new canonical procedure. (The old `email/HUBSPOT-PROCEDURE.md` was deleted 2026-05-15 along with the rest of the HubSpot sending code.)

### Phase 5 — Update knowledge base + skill

15. Update `CLAUDE.md` "Email infrastructure" section: welcome workflow now lives in Resend.
16. Update `docs/project-state.md`: Current state, Key IDs (Resend Automation ID, Audience ID), Key files.
17. Build a new `extend-email-sequence` skill keyed to "add a step to the Resend Automation". (The previous HubSpot-centric version was deleted 2026-05-15.)

### Phase 6 — Groundwork for future sequences

18. Document the reusable pattern in `RESEND-PROCEDURE.md`: a new sequence = new event name + new Automation. Bridge script can fire any event; HubSpot property can gate enrollment (e.g., `re_engagement_fired_at`).
19. Helper utility `scripts/resend-fire-event.py` for ad-hoc event firing.

## What stays the same

- Landing page form submission code (unchanged).
- HubSpot CRM: contacts, properties, list, history.
- Hourly Resend → HubSpot unsubscribe sync (`.github/workflows/sync-unsubscribes.yml`).
- The 5 email source HTMLs in `email/welcome-sequence/` (single source of truth; we keep porting from there).
- All 5-email arc copy and timing (0d / 3d / 6d / 9d / 13d).

## What changes

- Email sending moves from HubSpot → Resend.
- "Workflow ID" reference in project-state.md becomes "Resend Automation ID".
- New canonical procedure: `email/welcome-sequence/RESEND-PROCEDURE.md` (the old HubSpot procedure was deleted 2026-05-15).
- New cron in GitHub Actions (signup sync), new HubSpot contact property (`resend_welcome_fired_at`).
- `extend-email-sequence` skill rebuilt for Resend Automations (old HubSpot version deleted 2026-05-15).

## Rollback

If Resend Automations misbehave at any phase before Phase 4:
- The HubSpot side is untouched. Re-enable workflow `1804689064` in the UI; we're back to the original plan with zero data loss.

After Phase 4 (HubSpot workflow deleted):
- The HubSpot welcome workflow is unrecoverable without recreating it from scratch (the old `email/HUBSPOT-PROCEDURE.md` was deleted on 2026-05-15). If rollback is needed, regenerate the workflow using HubSpot's v4 API + the 5 email shells, ~1 hour of work.

## Open questions before execution

1. **Bridge mechanism** — confirm option A (cron sync) is the pick.
2. **Audience scope** — one audience for everyone, or separate audiences per sequence (welcome, re-engagement, post-call) so the unsubscribe sync stays clean?
3. **Personalization scope** — Email 01 uses `firstname`. Do we want any of the other emails to reference `farm_name` or the deal flags (`orisha` / `gfm`) for branching/personalization in the Automation, or keep them simple linear sends like today?
