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

- `30` g CH₂O per mol CO₂ ; mature 18-in leaf area ≈ 0.06 m²


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

- mature 18-in leaf ≈ **2.0 g dry weight** → ~0.040 g CH₂O/day at 25 °C

- daytime temperature alone does NOT set respiration; the 24 h average does


### Construction cost


- **expanding leaf** → construction cost   (`Growth = 1.4 × daily dry-weight gain`)

- construction cost → zero once the leaf reaches full size

- a 2.0 g leaf costs ~2.8 g CH₂O to build, drawn over ~18 days, peaking ~0.16 g/day

- **sucker** → construction cost **plus** its own export, spent on vegetative tissue   (a sucker is net positive on carbon; it competes by *where its output goes*, not by consuming the pool)

- **sucker** → flower cluster if left   (a sink that will not finish, on a topped plant)


### Who imports and who exports


Sign is the wrong lens for most pruning calls — see the allocation note at the foot of this cluster.


| Organ state | Balance |
|---|---|
| Flower cluster, fruit | **importer** — pure sink, no photosynthesis |
| Leaf ~85 %+ damaged, in deep shade | **importer** |
| Any leaf, dark hours | **importer** |
| Leaf in its first ~4 days | ~break-even — tiny area, but top-of-canopy light |
| Sucker with 2-3 small leaves | **exporter**, ~+0.3 g/day in summer light |
| Healthy leaf, any canopy depth to LAI ~5 | **exporter** |

- shade reduces a healthy leaf's *magnitude*, not its *sign*   (a bottom leaf earns ~1/10 of a top leaf, and still exports)

- `Health`, not shade, is what flips a leaf's sign inside a real canopy

- **net balance does not decide pruning; allocation does**   (a sucker exports, and still spends most of its output building tissue that carries no fruit)


### Compensation depth


- **compensation depth** = LAI above at which net carbon reaches zero   (`ln(PAR_top × ε × 30 × Area / Resp) / k`)

| Month | PAR_top (mol/m²/day) | T_avg (°C) | Compensation depth (LAI) |
|---|---|---|---|
| June | 28 | 22 | 6.2 |
| July | 26 | 24 | 5.9 |
| August | 20 | 23 | 5.6 |
| September | 13 | 19 | 5.4 |
| October | 8 | 16 | 5.0 |

- a tomato canopy runs LAI 3 to 4 → compensation depth sits **below** the canopy floor in every month


### Worked balances (g CH₂O per leaf per day)


| Organ | LAI above | Gross | Resp | Growth | Net |
|---|---|---|---|---|---|
| July, top, mature leaf | 0 | 1.64 | 0.037 | 0 | +1.60 |
| July, mid-canopy leaf | 1.5 | 0.82 | 0.037 | 0 | +0.78 |
| July, bottom leaf | 3.5 | 0.20 | 0.037 | 0 | +0.16 |
| July, day-4 leaf (10 % area) | 0.1 | 0.16 | 0.003 | 0.16 | ~0.00 |
| July, sucker, 3 small leaves | 0.5 | 0.74 | 0.019 | 0.42 | **+0.30** |
| Sept, bottom leaf, healthy | 3.5 | 0.10 | 0.026 | 0 | +0.07 |
| Sept, bottom leaf, 60 % blighted | 3.5 | 0.040 | 0.026 | 0 | +0.01 |
| Sept, bottom leaf, 90 % blighted | 3.5 | 0.010 | 0.026 | 0 | −0.02 |


### Whether the sugar has a destination


- exported sugar → **fruit** only while the fruit is expanding   (the **swelling gate**; stages and timings in [`fruit.md`](fruit.md))

- swelling gate shut → surplus assimilate has no sink → **feedback inhibition** down-regulates photosynthesis   (an oversized canopy over a finished fruit load idles; it does not bank)

- **topping** → guarantees the gate will close; it does not close it   (the youngest truss reaching full size does)


### Ideal LAI


- canopy gross photosynthesis ← light **captured**, saturating in LAI   (`PAR_top × (1 − exp(−k·L)) × ε × 30`)

- canopy respiration ← LAI, **linear**, never saturating   (`L × 33 × 0.02 × Q10factor`)

- `L_opt` = `ln(PAR_top × ε × 30 × k / (0.66 × Q10factor)) / k`

- `L_opt` sits ~0.5 LAI **shallower** than compensation depth   (the marginal leaf is shaded by everything above it)

| Month | `L_opt` | Net at `L_opt` | Net at LAI 3 |
|---|---|---|---|
| June | 5.7 | 37.0 | 34.4 |
| July | 5.4 | 34.7 | 32.4 |
| August | 5.1 | 26.5 | 24.8 |
| September | 4.9 | 17.4 | 16.4 |
| October | 4.5 | 10.7 | 10.2 |

- LAI 3 captures 93 to 96 % of the LAI-5 return → the optimum is a **plateau**, not a peak

- above LAI ~3 the binding constraint is disease, fruit light, and labour, not carbon

- `leaves_per_stem` = `LAI / (stems_per_m² × 0.06)`   (mature 18-in leaf ≈ 0.06 m²)

- 18 leaves at 2.5 stems/m² → LAI 2.7


## Invariants


- Removing a healthy leaf removes sugar from the plant. Leaf removal is never a way to add assimilate to fruit.

- A sucker is a net carbon exporter. It is removed for where its output goes, not for what it costs.

- Ripening rate is set by average temperature, not by leaf count.

- Sugar becomes larger fruit only inside the expansion window. Outside it, more leaf changes nothing.



## Boundaries


- Covers one leaf's carbon budget, the canopy optimum, and whether the sugar has a destination.

- Where the exported sugar **goes** — the vegetative / generative split — lives in [`vigor.md`](vigor.md).

- Fruit stages, thermal time, and load → [`fruit.md`](fruit.md).

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

**feedback inhibition** — a leaf reducing its own photosynthesis when sugar backs up because downstream sinks are full.
