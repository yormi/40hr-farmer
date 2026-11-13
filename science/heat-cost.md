# Heat cost: yield lost per extra °F

Theory model for exhaust fan payback. Output: lb/ft² per season per °F.

Status: peak term falsified by farm observation (fruit sets at 105 °F). Chronic mean term is the current best estimate.


## Scope


### Angles

- Pollen viability

- Flower abortion (source/sink)

- Disease from weaker plants


### Crop inputs

| Input | Value |
|---|---|
| Leaders | 0.25 /ft² |
| Clusters | 1 / leader / week |
| Fruits per cluster (summer) | 3 |
| Fruit weight | 0.4 lb |
| Hot days | 40 |
| Clusters exposed per leader | ~6 |
| Summer potential, exposed clusters | 1.8 lb/ft² |


## Mechanisms


### Pollen viability

- Sensitive windows: meiosis 8 to 13 days before anthesis; anthesis ±2 days

- Set drops when 24 h mean > ~77 °F (25 °C)

- Near zero at constant ~90 °F, 12 h/day (Sato 2000) or ~84 °F mean (Peet 1998)

- Driver: 24 h mean + night temperature, not confirmed for short day peaks


### Source/sink: abortion and fruit size

- Maintenance respiration Q10 = 2 → +1.8 °F = ~2 to 3 % net assimilate lost

- Hotter fruit grow faster → ~9 % fewer fruits carried per +1.8 °F, but faster turnover

- Mostly shifts timing; real kg loss = respiration


### Disease from weaker plants

- No mechanistic theory → scenario parameter only

- Spider mites: strongest basis, generation time ~halves 68 → 86 °F

- Not priced


## Model terms


### Chronic mean term (current best)

- Loss = 0.04 to 0.07 lb/ft² per °F of summer mean above 77 °F

- Covers respiration + mild pollen loss

- Source: 25 → 26 °C mean ≈ 3 to 8 % kg


### Peak term (falsified, reference only)

- Daily dose `d = hours above 86 °F × (peak − 86)²`

- Set loss `L = min(1, 0.0055 × d)`

- Compensation `E = L × (0.5 + 0.5 L)`

- Loss = 1.8 × E lb/ft²

- Calibration: Sato, 12 h/day at ~90 °F ≈ full set loss

- Contradiction: farm sets fruit at 105 °F; model predicts full loss → coefficient ≥10× too harsh for short peaks


### Reference table (peak term invalid)

3 h/day at peak, 40 days, summer mean = peak − 13 °F.

| Peak | Mean | Peak loss | Chronic loss | Total lb/ft² | lb/ft² per extra °F |
|---|---|---|---|---|---|
| 86 °F | 73 °F | 0 | 0 | 0 | 0 |
| 88 °F | 75 °F | 0.06 | 0 | 0.06 | 0.03 |
| 90 °F | 77 °F | 0.30 | 0 | 0.30 | 0.12 |
| 92 °F | 79 °F | 0.85 | 0.11 | 0.96 | 0.33 |
| 95 °F | 82 °F | 1.80 | 0.28 | 2.08 | 0.37 |
| 100 °F | 87 °F | 1.80 | 0.55 | 2.35 | 0.05 |


## Conclusions

- Fan value ≈ 0.05 lb/ft² per °F removed from summer mean; peak effect unproven

- Fans cut day peaks, barely touch nights → small mean effect → low payback unless nights cool and days long and hot

- 0.4 lb/ft² per °F is not a fair scale for houses peaking ~100 °F


## Open gaps

| Gap | Bias |
|---|---|
| Fan can't cool below outside air; savings depend on site weather | Overstates savings |
| No warm-night term | Missing main pollen driver |
| Flower temp ≠ air temp; sensor placement | ±3 to 10 °F |
| Humidity / pollen release | Either way |
| Lost summer set partly recovered in fall | Overstates loss |
| Chronic and peak terms overlap | Overstates ~10 to 20 % |
| Color, cracking, blossom-end rot (price, not lb) | Understates $ |
| Disease and mites not priced | Understates |
| Plant damage above 100 °F | Understates |


## Needed to recalibrate

1. Duration at 105 °F + night lows

2. Sensor position

3. Set at those temps (3 of 3?)

4. Variety
