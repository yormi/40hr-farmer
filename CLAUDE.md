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
