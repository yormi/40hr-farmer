# 40hr Farmer / Orisha

Landing page, HubSpot funnel, and email automation for the 40hr Farmer coaching program.

## Read before you write copy, design, or pitch anything

These are the shared brand foundations. Always consult them before producing copy, imagery choices, or funnel changes.

- [`docs/brand/purpose.md`](docs/brand/purpose.md) — Orisha mission, the Playbook, and the strategic path.
- [`docs/brand/positioning.md`](docs/brand/positioning.md) — Pressure-relief-through-yield thesis and why greenhouse tomatoes are the lever.
- [`docs/brand/products.md`](docs/brand/products.md) — Program pricing, GFM partnership, Helper and Chief Grower details.
- [`docs/brand/ideal-farmer.md`](docs/brand/ideal-farmer.md) — Who the program is for and who it is not for.
- [`docs/brand/voice-and-values.md`](docs/brand/voice-and-values.md) — Voice, style rules, positioning, scarcity, testimonials, red lines.
- [`docs/brand/visual-design.md`](docs/brand/visual-design.md) — Quiet farm journal aesthetic.
- [`docs/story-and-origin.md`](docs/story-and-origin.md) — Canonical 2024/2025 timeline, Drew, Gordon, consulting facts.
- [`docs/drew-raw-notes.md`](docs/drew-raw-notes.md) — Drew's raw 2025 season field notes (archival source).
- [`docs/gordon-raw-notes.md`](docs/gordon-raw-notes.md) — Gordon's raw 2025 weekly check-ins from Ten Mothers Farm (archival source).

## Non-negotiables (inline, because they are easy to forget)

- **The farmer is the hero.** Orisha is the guide. Copy is about the farmer's life, not our product.
- **NO DASHES** in copy output. Use commas, periods, colons, or rewrite.
- **No claims, no promises** on the course. Orisha product guarantees possible but ask Guillaume first.
- **Never** manipulative, flashy, guilt-tripping, preachy, or salesy.
- **Off-limits:** politics, religion, competitor bashing, fear-mongering.
- **Always surface copy drafts for Guillaume's approval** before shipping.

## Project state

See [`docs/project-state.md`](docs/project-state.md) for current phases, key IDs (HubSpot portal, form, workflow, email IDs), and file map.

## Funnel conversions to optimize

1. Program signup (form submit on landing page).
2. Email open (across the 5-email welcome sequence).
3. Sales call booked with Orisha (Helper or Chief Grower).

## Local dev server

Hot-reload preview for `index.html`:

```bash
./scripts/dev-server.sh
```

Serves the repo root on `http://localhost:8765` with file-watching auto-refresh. Stop with `pkill -f live-server`. Requires Node 22 (managed via `fnm`); the script switches automatically.

## Repo layout

- `index.html` — landing page (deployed at https://yormi.github.io/40hr-farmer/)
- `email/*.html` — 5 welcome email templates
- `email/HUBSPOT-PROCEDURE.md` — HubSpot API setup docs
- `docs/user-experience-flow.md` — email sequence flow diagram
- `docs/brand/` — brand foundations (read these)
- `assets/clients/ferme-decembre/` — farm photography
- `scripts/` — utilities (Google Photos picker, etc.)
