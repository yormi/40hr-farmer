# Seedling → transplant calendar

Back-engineer every propagation date from the first sale week.
Grafted (2 heads) and non-grafted (1 head) transplant the same day.

Why → [`science/fruit.md`](../../science/fruit.md)


## Rule

- Anchor = first sale week → first ripe fruit 1 week earlier.
- Transplant 8 weeks before first ripe, first cluster in flower.
- Heat on + warm beds 1 week before transplant.
- Grafted: seed 9 weeks before transplant.
- Non-grafted: seed 6 weeks before transplant, single head.
- Shift the sale date → every row moves by the same offset.


## Example: first sale week of May 3, 2027

| Week of | ISO wk | Grafted (2 heads) | Non-grafted (1 head) |
|---|---|---|---|
| Nov 16, 2026 | 47 | Order seeds, rootstock, clips, trays, mix, lights, heat mats | same |
| Dec 28 | 53 | Lights on, heat mats on, propagation room to 24 °C | |
| Jan 4, 2027 | 1 | Seed rootstock | |
| Jan 7 | 1 | Seed scion, 3 days after rootstock | |
| Jan 18 | 3 | Graft, stems pencil-lead size, ~14 days | |
| Jan 25 | 4 | Out of healing chamber after 7 days, harden 3 days | Seed non-grafted |
| Feb 1 | 5 | Pot up to 4 in | |
| Feb 8 | 6 | Pinch scion above 2nd true leaf, keep 2 suckers as heads | |
| Feb 15 | 7 | | Pot up to 4 in |
| Feb 22 | 8 | Space pots so leaves don't touch | same |
| Mar 1 | 9 | Heat on, house to 18 °C min, warm beds to 15 °C at root depth | same |
| Mar 8 | 10 | Transplant, first cluster flowering | Transplant, same day |
| Apr 26 | 17 | First ripe fruit | same |
| May 3 | 18 | First sale | same |


## Durations

| Step | Weeks |
|---|---|
| Transplant → first ripe (21 °C avg, ~600 DD base 10 °C) | 8 |
| Grafted seed → transplant | 9 |
| Non-grafted seed → transplant | 6 |
| Rootstock seeded before scion | 3 days |
| Seed → graft | 2 |
| Healing chamber | 1 |
| Graft + 2-head pinch growth cost | ~1 each |


## Light and space by phase

Target 16–18 h/day. W/ft² over occupied tray area. Clearance =
plant height + 4–6 in to tubes. HPS only over the final spaced
bench, never on a rack. LED shop light = generic 4 ft 4000–5000 K
garage fixture, ~1.2–1.5 µmol/J, roughly 2 fixtures per ft of
rack width.

| Phase | Weeks | Target µmol | LED T8 W/ft² | LED shop light W/ft² | Fluo T5/T8 W/ft² | HPS W/ft² | Shelf clearance | Where |
|---|---|---|---|---|---|---|---|---|
| Germination to graft | 0–2 | 250 | 14 | 22 | 25 | - | 12 in | Rack |
| Healing chamber | 3 | ~0 then 50 | 3 | 4 | 5 | - | 12 in, dome | Rack |
| Post-heal to pot-up | 4–5 | 250 | 14 | 22 | 25 | - | 18 in | Rack |
| Potted, 2 heads, to transplant | 6–9 | 250 | 14 | 22 | 25 | 24 | 24 in | Bench in greenhouse |

- Size fixtures for the final spaced bench area; early on run
  only tubes over occupied trays.
- Heat mats only if room air <24 °C in weeks 0–1; skip otherwise.
- Set rack shelves at 18 in from day 1 → no reshelving live trays.
- Week 6 exit is about area, not height: pinch spreads 2 heads,
  pots go to 3–4× spacing.
- After week 7 sun carries most of it; lights top up mornings and
  grey days.
- Air after healing: 20–22 °C day, 17–18 °C night. Heat mats off.


## Fixed rules

- Pinch only once the graft has resumed growth.
- Non-grafted stays 1 head: 2 leaders on own roots = −10–20 % yield.
- March average under 20 °C → push transplant 1 week earlier.


## Caveats

- Standard heated-house durations (Mefferd, Johnny's grafting
  guide), not yet field-reviewed.
