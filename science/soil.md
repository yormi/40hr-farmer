# Soil — cation exchange, base saturation, pH drift


## Model


### Cation exchange


- **clay + humus surfaces** carry negative charge → hold **cations** (Ca²⁺, Mg²⁺, K⁺, Na⁺, H⁺)   (the exchange complex; the soil's nutrient reservoir)

- **CEC** (cation exchange capacity, meq/100 g) = total charge available   (sand ~5, silt loam ~10, clay ~15+)

- CEC → buffering   (higher CEC → more amendment per unit pH change, slower drift both ways)

- **base saturation** = share of CEC held by Ca, Mg, K, Na vs H   (the balance among the bases, not the amount)


### Base saturation from Mehlich-3 ppm


- ppm → meq/100 g: divide by the cation's equivalent weight × 10

| Cation | ppm ÷ |
|---|---|
| Ca | 200 |
| Mg | 120 |
| K | 390 |
| Na | 230 |

- `CEC ≈ Ca_meq + Mg_meq + K_meq + Na_meq + H_meq`   (H from buffer pH; ~0 above pH 7)

- `base sat % = cation_meq ÷ CEC × 100`

- Example: Ca 2000, Mg 240, K 195, Na 23 ppm → 10.0 + 2.0 + 0.5 + 0.1 = 12.6 meq → Ca 79 %, Mg 16 %, K 4 %, Na 1 %

- Tomato bands: Ca 65–75 %, Mg 10–15 %, K 3–5 %, Na < 2 %   (Mg:K ≈ 2:1 on ppm)

- Ca, Mg, K compete for the same sites → one high → others' uptake drops even at adequate ppm   (antagonism; why ratios matter more than absolutes)


### pH drift under irrigation


- irrigation water **alkalinity** (HCO₃⁻, as CaCO₃) → lime deposited each irrigation   (~25 kg CaCO₃/ha per inch of 100 ppm water)

- 40 in season × 100 ppm → ~1 t CaCO₃/ha/year → +0.2–0.4 pH on loam

- **elemental S** + O₂ + H₂O → (bacteria) → H₂SO₄ → neutralises carbonate   (biological; 3–6 months, needs warm moist soil)

- S needed per pH unit ∝ CEC   (sand : silt loam : clay ≈ 1 : 2 : 4)

- pH > 6.8 → P, Fe, Mn availability falls   (lockup zone)


### Salts and leaching


- salts accumulate where water evaporates, not where it drains   (bed surface, wetting-front edges)

- leaching removes salt ∝ drainage depth ÷ root-zone depth   (≈ 50 % per equal depth of water through)

- intermittent pulses > continuous ponding per inch of water   (slow flux displaces pore water instead of bypassing through cracks)

- Na on exchange sites disperses clay → structure and drainage degrade   (the slow, hard-to-reverse salt problem)

- **gypsum** (CaSO₄) → Ca displaces Na off exchange → Na leachable   (no pH change)

- leached soil EC floor ≈ 1.5–2 × irrigation water EC   (can't rinse below the water you rinse with)


## Invariants


- An EC reading says how much salt, never which ions. Ions need a lab.

- Reserves (M3) and the soluble pool (SME) are different questions; neither substitutes for the other.


## Boundaries


- Nitrogen budgeting, organic-matter mineralisation → not yet covered.
- Water uptake and root-zone salt symptoms on the plant → [water.md](water.md).


## Vocabulary


- **Mehlich-3 (M3)** — acid extract; reads the exchangeable reserve. Governs amendments.
- **SME** — saturated media extract; reads what's dissolved now. Governs leaching and fertigation.
- **meq/100 g** — milliequivalents per 100 g soil; charge units so cations compare on equal footing.
