# 40hr Farmer / Orisha

Landing page, HubSpot funnel, and email automation for the 40hr Farmer coaching program.

## Read before you write copy, design, or pitch anything

These are the shared brand foundations. Always consult them before producing copy, imagery choices, or funnel changes.

Brand foundations live in the `brand/` submodule. Public site: https://brand.orisha.io/. If the submodule is missing, run `git submodule update --init`.

- [`brand/docs/brand/purpose.md`](brand/docs/brand/purpose.md) — Orisha mission, the Playbook, and the strategic path.
- [`brand/docs/brand/positioning.md`](brand/docs/brand/positioning.md) — Pressure-relief-through-yield thesis and why greenhouse tomatoes are the lever.
- [`brand/docs/brand/products.md`](brand/docs/brand/products.md) — Program pricing, GFM partnership, Helper and Chief Grower details.
- [`brand/docs/brand/ideal-farmer.md`](brand/docs/brand/ideal-farmer.md) — Who the program is for and who it is not for.
- [`brand/docs/brand/voice-and-values.md`](brand/docs/brand/voice-and-values.md) — Voice, style rules, positioning, scarcity, testimonials, red lines.
- [`brand/docs/brand/email-sequences.md`](brand/docs/brand/email-sequences.md) — How we structure multi-email funnels (5-email arc, mechanics, what we do not do).
- [`brand/docs/brand/visual-design.md`](brand/docs/brand/visual-design.md) — Quiet farm journal aesthetic.
- [`brand/docs/internal/story-and-origin.md`](brand/docs/internal/story-and-origin.md) — Canonical 2024/2025 timeline, Drew, Gordon, consulting facts. Not published.
- [`brand/docs/internal/drew-raw-notes.md`](brand/docs/internal/drew-raw-notes.md) — Drew's raw 2025 season field notes (archival source). Not published.
- [`brand/docs/internal/gordon-raw-notes.md`](brand/docs/internal/gordon-raw-notes.md) — Gordon's raw 2025 weekly check-ins from Ten Mothers Farm (archival source). Not published.

## Non-negotiables (inline, because they are easy to forget)

- **The farmer is the hero.** Orisha is the guide. Copy is about the farmer's life, not our product.
- **NO DASHES** in copy output. Use commas, periods, colons, or rewrite.
- **No claims, no promises** on the course. Orisha product guarantees possible but ask Guillaume first.
- **Never** manipulative, flashy, guilt-tripping, preachy, or salesy.
- **Off-limits:** politics, religion, competitor bashing, fear-mongering.
- **Always surface copy drafts for Guillaume's approval** before shipping.

## Project state

See [`docs/project-state.md`](docs/project-state.md) for current phases, key IDs (HubSpot portal, form, workflow, email IDs), and file map.

## Email infrastructure

- **Broadcasts / marketing sends:** Resend (verified domain `orisha.io`). CASL-compliant footer snippet at [`email/compliance-footer.html`](email/compliance-footer.html) — drop into every marketing send verbatim. SPEAR-specific procedure in [`email/spear/spear-wave-plan.md`](email/spear/spear-wave-plan.md).
- **Welcome sequence:** templates in [`email/welcome-sequence/`](email/welcome-sequence/). Sending is being migrated off HubSpot (see [`docs/resend-welcome-migration-plan.md`](docs/resend-welcome-migration-plan.md)).
- **CRM:** HubSpot only. Landing page form submits create contacts via HubSpot Forms API. Resend → HubSpot unsubscribe sync runs hourly via [`.github/workflows/sync-unsubscribes.yml`](.github/workflows/sync-unsubscribes.yml) — needs `RESEND_API_KEY` + `HUBSPOT_API_KEY` repo secrets.
- **API keys:** `.secrets/*.env` files locally (`resend.env`, `hubspot.env`); env vars in CI. Scripts follow this pattern.
- Loops and Sequenzy were tried and dropped 2026-05-15 — do not suggest as ESP options.

## Funnel conversions to optimize

1. Program signup (form submit on landing page).
2. Email open (across the 5-email welcome sequence).
3. Sales call booked with Orisha (Helper or Chief Grower).

## Local dev server

Hot-reload preview for `landing/index.html`:

```bash
./scripts/dev-server.sh
```

Serves `landing/` on `http://localhost:8888` with `/assets` and `/drew-season` mounted from their sibling directories — same path layout as deployed GH Pages. File-watching auto-refresh. Stop with `pkill -f live-server`. Requires Node 22 (managed via `fnm`); the script switches automatically.

**Localhost caveat:** HubSpot Forms Submissions API silently strips field values when the Origin is `localhost`, so contacts created from local-dev submits land with only `email` populated. The form **works fine from the GitHub Pages URLs** (production and staging). Use the staging URL below for full end-to-end browser submit testing.

## Staging preview

Sister repo `yormi/40hr-farmer-staging` deploys to `https://yormi.github.io/40hr-farmer-staging/` via GitHub Pages.

Push the current branch to staging with:

```bash
./scripts/deploy-staging.sh
```

(Force-pushes current HEAD to the staging repo's `main`. Deploys in 30-90s.) Use this to preview any landing-page change in a real GitHub Pages environment before pushing to the production repo.

## Repo layout

- `landing/` — landing page source (deployed at https://the40hourfarmer.orisha.io/; `yormi.github.io/40hr-farmer/` redirects there)
  - `landing/index.html` — landing page
  - `landing/40hr_farmer_pitch_deck.html` — pitch deck
  - `landing/docs/` — landing rework process, outline + locked copy, sources. See `landing/docs/README.md`.
- `email/welcome-sequence/` — 5 welcome email templates + sequence planning docs (`docs/sequence-plan.md`)
- `email/spear/` — SPEAR broadcast project: plan, audience CSVs, samples, scripts (`scripts/`)
- `email/compliance-footer.html` — CASL footer for all Resend marketing sends
- `docs/resend-welcome-migration-plan.md` — plan for moving welcome sequence off HubSpot onto Resend
- `docs/utm-links.md` — UTM scheme + canonical tagged URLs for the waitlist
- `brand/` — brand foundations submodule (read these, see top of file)
- `assets/clients/ferme-decembre/` — farm photography
- `scripts/` — repo-wide utilities (dev server, doc map, staging deploy, Resend↔HubSpot unsubscribe sync)
