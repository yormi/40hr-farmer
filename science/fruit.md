# Fruit — set, development, and load


## Model


### Pollination and set


- **flower opens** → viable for 1 to 2 days   (shorter in summer)

- **dry pollen** → releases on vibration ; damp pollen clumps and will not shed

- **trellis wire vibration** → pollen release   (the wire carries the shake to every plant on it; shaking plants individually does not)

- no pollination → no fruit → fruit load is gated here before any other lever

- **flower** 1—1 **fruit** ; **cluster** 1—* **fruit** ; **leader** 1—* **cluster**

- well-pollinated truss → **uniform, fast swelling**: fruitlets at pea size within ~a week of flowering, all siblings within a size step of each other

- one fat fruitlet + stragglers → the truss set over too long a window (pollination trouble); the stragglers stay small


### Pollen and heat — the two-week lag


- pollen develops over the **~2 weeks before** a flower opens

- heat damage accumulates in that development window, not on the day the flower opens

- so an aborted flower today reports the **last fortnight's** weather

| Exposure | Effect on pollen |
|---|---|
| 4 h above 95 °F | not viable |
| 1 h above 105 °F | not viable |
| 5 consecutive nights above 75 °F | seriously degraded |

- **plant health entering the heat** → tolerance of pollen degradation   (a strong plant compensates for partial loss; summer set is decided in May and June)


### Fruit development


- **fruit cell number** ← the first ~14 days after set   (fixed then; nothing later changes it)

- **fruit cell expansion** ← assimilate supply   (the only window in which more leaf means bigger fruit)

- full-size green fruit → no further enlargement   (extra sugar has no destination)

- **breaker** → phloem connection closes   (nothing more arrives from the vine; ripening runs on the fruit's own reserves)

- sinks full → **feedback inhibition** → photosynthesis down-regulates   (surplus assimilate is not banked)


### Ripening as thermal time


- **accumulated degree-days** (base 10 °C) → development stage   (`days = DD_required / (T_avg − 10)`)

- anthesis → red ripe ≈ **600 DD** ; breaker → red ripe ≈ **130 DD**

- °F degree-days: base **50 °F**, 1 °C-day = 1.8 °F-days

| Metric | °C | °F |
|---|---|---|
| Degree-day base | 10 °C | 50 °F |
| Anthesis → red ripe | ~600 DD | ~1,080 DD |
| Anthesis → breaker | ~470 DD | ~845 DD |
| Breaker → red | ~130 DD | ~235 DD |
| Unheated finish line (24 h avg where accumulation ~stalls) | ~12 °C | ~54 °F |
| Unheated house offset vs outside (24 h avg) | 1–3 °C | 2–5 °F |
| Ripening floor with 5–6 trusses on | 17 °C | 63 °F |

| T_avg | Breaker → red |
|---|---|
| 24 °C | 9 days |
| 22 °C | 11 days |
| 20 °C | 13 days |
| 18 °C | 16 days |
| 16 °C | 22 days |
| 14 °C | 33 days |

- the curve steepens sharply toward the 10 °C base

- **fruit load** → ripening speed only indirectly, via the heat headroom it buys and via the expansion window if the plant was source-limited


### Fruit as the dominant sink


- **fruit** → the largest single draw on the energy pool   (larger than leaf, stem, or root)

- fruit count → stem caliper, inversely   (a mature fruit on a stem thinner than a BIC pen is the extreme read)

- **fruit removed early** → sugar recovered ; **fruit removed at full size** → sugar already spent, nothing recovered

- **uniformity of load across clusters** → uniformity of irrigation demand, climate response, and harvest flow   (a bed alternating 1-fruit and 7-fruit clusters cannot be steered as one unit)


### Physical load


- perfect fruit load → over **2,500 lb** on a single wire ; ~**4,600 lb** per bed at once

- wire specification: ~**1/8 in**, about gauge 9

- systems that fail under real peak load: Qlipr-type, wrap-around / roll systems, jute twine, compostable clips and twine


## Invariants


- A fruit at or past breaker gains nothing from remaining on the vine.

- Sugar becomes larger fruit only inside the expansion window. Outside it, more leaf changes nothing.

- Trellis capacity is a precondition for fruit-load targets, not a consequence of them.


## Boundaries


- Covers fruit from flower to ripe, and the physical load it imposes.

- Where the sugar comes from → [`leaf-energy.md`](leaf-energy.md).

- The vegetative / generative split that decides how much reaches fruit → [`vigor.md`](vigor.md).

- Heat thresholds for the plant as a whole → [`climate.md`](climate.md).


## Vocabulary


**breaker** — the first 10 % of colour break on a green fruit, usually a blush at the blossom end; the point the fruit disconnects from the vine. _Avoid_: turning, first blush

**mature green** — full size, still uniformly green, before breaker. Picked at this stage a fruit ripens pale and bland.

**swelling gate** — whether any fruit on the plant is still expanding; open means sugar has a destination, closed means it does not.

**anthesis** — flower opening.

**parthenocarpic** — setting fruit without pollination, so seedless.

**catfacing** — scarred, misshapen blossom end from cold during flower development.
