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

## Architectural constraint discovered 2026-05-15 (empirical test)

Resend **ignores delay-edits for in-flight contacts**. Confirmed by live
test (`scripts/test-resend-delay-edit.py`, run 20:10 UTC 2026-05-15): shortened
a 3-minute delay to 30 seconds after 90s elapsed; the parked contact still
fired at +182.6s (the original schedule). Edits apply only to new enrollments.

Combined with the documented 30-day max delay, this means the build-as-you-go
pattern Guillaume sketched — *park 1y → splice new email → shorten delay to
2d → 48h+ fires immediately* — **does not work on pure Resend Automations**.

This forces an architecture choice: who owns scheduling?

| | A. HubSpot owns scheduling, Resend owns sending (**recommended**) | B. Resend owns everything, no in-flight extensions |
|---|---|---|
| Drip engine | HubSpot workflow, webhook actions only (no HubSpot email sends) | Resend Automation, multi-step |
| Sending | Resend (via one-step automation per email, triggered by webhook event) | Resend |
| Long delays | ✅ Unlimited | ❌ 30d max per step |
| Build-as-you-go (splice + shorten releases parked contacts) | ✅ Documented in `email/HUBSPOT-PROCEDURE.md` | ❌ Empirically confirmed not supported |
| Real-time bridge | The workflow IS the trigger — webhook fires on contact enrollment in ms | Needs cron/worker, since HubSpot still has the form |
| For future emails after sequence ends | Edit the workflow live (HubSpot supports this on enabled workflows) | Run Broadcasts to past-completers (SPEAR-style manual send) |
| New infrastructure | Zero (if HubSpot webhook supports custom Auth header) — else a 30-line Cloudflare Worker proxy | One bridge script + GitHub Action |

**Recommendation: A.** Guillaume's build-as-you-go pattern is literally how
HubSpot delay edits work (documented in the procedure doc). We still get
every other Resend win we wanted — sending from orisha.io via Resend's
infrastructure, consistency with broadcasts, no HubSpot email-editor pain.
We just delegate scheduling to HubSpot (which is what it's good at anyway).

If picking A, the migration becomes: each email gets a one-step Resend
Automation (trigger event = `welcome_01`, `welcome_02`, ...). HubSpot
workflow keeps its `delay → action → delay → action` shape, but every
action is now a webhook to Resend's `/events/send` endpoint, no HubSpot
email send actions.

## Open question if Option A picked

Does HubSpot's workflow webhook action on Guillaume's plan tier support
custom Authorization headers + custom JSON body templating? If yes: zero
new infrastructure. If no: a 30-line Cloudflare Worker as relay
(`webhook.orisha.io` → forwards to Resend with auth header).

Need to verify in the HubSpot portal before locking the architecture.

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
