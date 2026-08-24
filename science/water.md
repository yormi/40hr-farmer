# Water — transpiration, air dryness, and root-zone salts


## Model


### Transpiration as a service, not a cost


- **root water uptake** → xylem stream → **transpiration**   (evaporation out of the leaf)

- transpiration → **evaporative cooling**   (a healthy transpiring canopy runs up to ~15 °F below air; ~10× the flux of a stressed one)

- transpiration → **calcium delivery**   (Ca moves in the xylem only; no phloem transport, so a fruit gets Ca only while water is flowing to it)

- transpiration ← min(**stomatal aperture**, **water supply**)   (binding limiter; whichever is scarcer sets the rate)

- stomata closed → transpiration stops → leaf temperature climbs → photosynthesis stops   (the whole chain fails together)

- **bed** 1—* **plant** ; **plant** 1—* **leader** ; leader count → root demand   (two leaders need a larger root system than one)


### Air dryness


- **air temperature** + **relative humidity** → **VPD**   (how hard the air pulls water out of the leaf)

- warmer air holds more water → the same RH is drier when hot

- VPD → transpiration **demand**; water supply → transpiration **capacity**

- demand > capacity → stomata close → growth stops → stem thins   (the air-dryness failure chain)

| VPD | g/m³ | Reads |
|---|---|---|
| < 0.3 kPa | < 2 | too wet; transpiration stalls, Ca delivery fails |
| 0.4 – 0.95 kPa | 3 – 7 | working band |
| 0.95 – 1.2 kPa | 7 – 9 | generative, watch the head |
| > 1.2 kPa | > 9 | stomata closing, photosynthesis dropping |

- `g/m³ = VPD_Pa × 18.015 / (8.314 × T_kelvin)`   (≈ kPa × 7.4 at 20 °C)

- "too dry" thresholds in RH terms: ~55 % at 65 °F, ~75 % at 90 °F

- RH ceiling for the 3 g/m³ deficit floor (aim at this RH or drier), by air temperature:

| °F | RH ceiling | °F | RH ceiling |
|---|---|---|---|
| 55 | 73 % | 85 | 90 % |
| 60 | 77 % | 90 | 91 % |
| 65 | 81 % | 95 | 92 % |
| 70 | 84 % | 100 | 93 % |
| 75 | 86 % | 105 | 94 % |
| 80 | 88 % | 110 | 95 % |

- dropping below the RH ceiling every 90 min is enough; the average between drops does not need to stay below it


### The stress ladder


One response worsening, not five diagnoses.

| Rung | Sign | State |
|---|---|---|
| 1 | leaf no cooler than air to the touch | stomata shut, invisible |
| 2a | leaf margins cup upward, green, undistorted | mild, reversible |
| 2b | leaflets roll lengthwise into tubes | moderate, reversible |
| 3 | turgor gone, canopy droops | severe |
| 4 | dead leaf margins | damage done |

- upper leaves near the head respond first   (cleanest signal)

- house-wide and even → environment; patchy by bed → that bed's water or feed

- distorted, mottled, or bronzed tissue is **not** this ladder   (herbicide, virus, mites, boron)

- hard roll at **dawn** on a fully hydrated leaf after a heavy prune or cold night → carbohydrate buildup, not water


### Water need is a moving target


Drivers, all live at once:

- **daylight length** → demand

- **sun strength** → demand

- **plant maturity** → demand   (a fruiting July plant drinks; a May seedling sips)

- **foliar area** → demand   (6-in leaves need ~90 % less water than 18-in leaves)

- **soil texture**, **system flow rate**, **emitter size and pressure** → supply   (wrong emitter can deliver 4× the intended volume)


### Both irrigation errors are invisible


| Error | Chain | Cost |
|---|---|---|
| too much | roots suffocate → root disease | stunted, pale; weeks lost unseen |
| too little | photosynthesis stops → wilt | hours of growth lost; stem thins within a week |

- irrigation **pattern** → the vegetative / generative split   (many small even shots → leaf; fewer larger with overnight dry-down → fruit)

- a shot under ~2 minutes only fills the drip tape

- bed ends drain better than bed middles → mid-bed plants worse than end plants means over-watering


### Root-zone salts


- **fertilizer input** − **crop uptake** − **leaching** → root-zone **EC**

- EC → **osmotic potential** → the plant's ability to draw water   (high salt is what stops the plant drinking, regardless of how much water is present)

- low EC → vegetative lean ; high EC → generative lean

- **1:1 slurry EC (w/w)** 1—1 **soil texture column**   (a weight-based slurry dilutes sand most and clay least, so the same root-zone state reads differently per texture)

| State | Sand | Loam | Clay |
|---|---|---|---|
| low | < 0.5 | < 1.0 | < 1.3 |
| in band | 0.5 – 1.0 | 1.0 – 2.0 | 1.3 – 2.7 |
| high | 1.0 – 1.25 | 2.0 – 2.5 | 2.7 – 3.3 |
| salt buildup | > 1.25 | > 2.5 | > 3.3 |

EC_slurry in mS/cm, 1:1 by weight.

- source-water EC above ~0.15 mS/cm adds to every reading


## Invariants


- Water management is about performance, not survival. A plant that never wilts can still be badly irrigated.

- Calcium reaches a fruit only while water is flowing to it. No transpiration, no calcium, whatever the soil holds.

- Soil bulk density drifts with moisture, so only a weight-based slurry stays comparable week to week.


## Boundaries


- Covers water movement, air dryness, and root-zone salinity.

- What the plant does with the sugar it makes → [`leaf-energy.md`](leaf-energy.md) and [`vigor.md`](vigor.md).

- Temperature as a rate driver → [`climate.md`](climate.md).


## Vocabulary


**VPD** — vapour-pressure deficit; how much more water the air could hold at its current temperature. A "feels-like" number for the plant. _Avoid_: humidity

**osmotic potential** — the pull that dissolved salts exert on water, working against the root's ability to take it up.

**leaching** — water moving past the root zone and carrying dissolved nutrients with it.

**1:1 slurry (w/w)** — equal weights of soil and water, stirred and read with an EC pen. _Avoid_: 1:1 by volume
