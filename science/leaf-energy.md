# Leaf energy — carbon balance of a single leaf


## Model


### Leaf carbon balance


- **leaf** → net carbon = gross photosynthesis − maintenance respiration − construction cost   (per leaf, per day, in g CH₂O)

- net carbon > 0 → **net exporter**; net carbon < 0 → **net importer**

- **net exporter** → energy pool; **net importer** ← energy pool   (the leaf feeds, or is fed by, the plant's shared pool)

- gross photosynthesis runs in daylight only; maintenance respiration runs 24 h   (the asymmetry that makes warm nights costly)

- **plant** 1—* **leaf** ; **leaf** 1—1 **canopy position**


### Light interception


- **canopy position** → light reaching the leaf   (Beer's law: `PAR_leaf = PAR_top × exp(−k × LAI_above)`)

- **LAI above the leaf** → light reaching the leaf   (attenuates; the dominant driver of a leaf's output)

- **k** (extinction coefficient) ≈ 0.7 for tomato

- light reaching the leaf → gross photosynthesis   (`Gross = PAR_leaf × ε × 30 × Area_leaf × Age × Health`)

- **ε** (light use efficiency) ← light level   (~0.05 mol CO₂/mol PAR in shade; ~0.035 in full sun, where the leaf saturates)

- **CO₂ concentration** → ε   (×1.3 at 800 ppm vs ambient)

- **VPD** above ~1.2 kPa → stomata close → gross photosynthesis drops, respiration unchanged   (the one climate state that pushes a healthy leaf toward net importer)

- `30` g CH₂O per mol CO₂ ; mature 18-in leaf area ≈ 0.04 m²


### Leaf age


- **leaf age** → photosynthetic capacity   (the `Age` factor, 0 to 1)

| Days from unfurl | Age factor | State |
|---|---|---|
| 0 – 12 | 0.3 → 1.0 | expanding |
| 12 – 35 | 1.0 | peak |
| 35 – 55 | 1.0 → 0.6 | declining |
| 55 – 75 | 0.6 → 0.2 | senescing |

- **damage fraction** → photosynthetic capacity   (`Health = 1 − fraction covered`; respiration is unaffected by damage)


### Respiration


- **leaf dry weight** → maintenance respiration   (`Resp = DW × 0.02 × 2^((T_avg − 25)/10)`)

- **24-hour average temperature** → maintenance respiration   (Q10 = 2: doubles per 10 °C)

- mature 18-in leaf ≈ **1.5 g dry weight** → ~0.028 g CH₂O/day at 25 °C

- daytime temperature alone does NOT set respiration; the 24 h average does


### Construction cost


- **expanding leaf** → construction cost   (`Growth = 1.4 × daily dry-weight gain`)

- construction cost → zero once the leaf reaches full size

- a 1.5 g leaf costs ~2.1 g CH₂O to build, drawn over ~18 days, peaking ~0.15 g/day

- **sucker** → construction cost with little offsetting area   (several small leaves, all building, in mid-canopy shade)


### Who imports and who exports


| Leaf state | Balance |
|---|---|
| Leaf under ~10 days old | **importer** — building faster than it earns |
| Sucker (few small leaves, shaded) | **importer** |
| Flower cluster | **importer** — pure sink, no photosynthesis |
| Healthy leaf, any canopy depth to LAI ~4 | **exporter** |
| Leaf ~70 %+ damaged, in deep shade | **importer** |
| Any leaf, dark hours | **importer** |

- shade reduces a healthy leaf's *magnitude*, not its *sign*   (a bottom leaf earns ~1/10 of a top leaf, and still exports)

- `Health`, not shade, is what flips a leaf's sign inside a real canopy


### Compensation depth


- **compensation depth** = LAI above at which net carbon reaches zero   (`ln(PAR_top × ε × 30 × Area / Resp) / k`)

| Month | PAR_top (mol/m²/day) | T_avg (°C) | Compensation depth (LAI) |
|---|---|---|---|
| June | 28 | 22 | 6.0 |
| July | 26 | 24 | 5.7 |
| August | 20 | 23 | 5.5 |
| September | 13 | 19 | 5.2 |
| October | 8 | 16 | 4.9 |

- a tomato canopy runs LAI 3 to 4 → compensation depth sits **below** the canopy floor in every month


### Worked balances (g CH₂O per leaf per day)


| Leaf | LAI above | Gross | Resp | Growth | Net |
|---|---|---|---|---|---|
| July, top, mature | 0 | 1.09 | 0.028 | 0 | +1.06 |
| July, mid canopy | 1.5 | 0.53 | 0.028 | 0 | +0.50 |
| July, bottom | 3.5 | 0.14 | 0.028 | 0 | +0.11 |
| July, day-4 leaf | 0.1 | 0.09 | 0.004 | 0.15 | −0.06 |
| July, sucker (3 leaves) | 0.5 | 0.09 | 0.010 | 0.12 | −0.04 |
| Sept, bottom, healthy | 3.5 | 0.067 | 0.020 | 0 | +0.05 |
| Sept, bottom, 60 % blighted | 3.5 | 0.027 | 0.020 | 0 | +0.01 |
| Sept, bottom, 90 % blighted | 3.5 | 0.007 | 0.020 | 0 | −0.01 |


## Invariants


- Removing a healthy leaf removes sugar from the plant. Leaf removal is never a way to add assimilate to fruit.

- Ripening rate is set by average temperature, not by leaf count.


## Boundaries


- Covers one leaf's carbon budget: what it earns, what it costs, and its sign.

- Where the exported sugar **goes** — the vegetative / generative split — lives in [`vigor.md`](vigor.md).

- Non-carbon reasons to remove a leaf (airflow, disease spread, nitrogen remobilization, access, transpiration load) are protocol matters, not part of this balance.


## Vocabulary


**PAR** — photosynthetically active radiation; the slice of sunlight a leaf can use, counted in mol of photons per m² per day. _Avoid_: light

**LAI** — leaf area index; m² of leaf per m² of floor. "LAI above" is the leaf area stacked between a given leaf and the sky.

**CH₂O** — sugar equivalents; the accounting unit for both what a leaf makes and what it burns.

**maintenance respiration** — sugar a living leaf burns just to stay alive, independent of any growth.

**construction cost** — sugar consumed building new tissue, over and above the tissue's own dry weight.

**Q10** — the factor a rate multiplies by per 10 °C rise. Q10 = 2 means respiration doubles.

**net exporter / net importer** — a leaf whose daily carbon balance is positive (feeds the plant) or negative (is fed by it).

**compensation depth** — the canopy depth, in LAI above, where a leaf's daily production exactly equals its respiration.
