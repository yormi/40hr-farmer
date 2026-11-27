# Heating case: The Sharing Farm (Richmond BC)

Worked case → source for heating-install skill.

## Inputs
- 50x80 ft (4,000 ft²) high tunnel, double poly, no gutter, airtightness unknown
- No heat today
- Target 21 °C night (safety margin, early transplants)
- Season: transplant March → crop out mid-December
- Power: 240 V / 200 A, unknown existing load, electricity free to them
- Fuel preference: electric > electric+propane > propane

## Heat load
- Skin ≈ 6,100 ft², volume ≈ 44,000 ft³
- U double poly 0.7 BTU/h·ft²·°F; infiltration 1 ACH (unknown tightness)
- UA ≈ 2.7 kW/°C
- Design low: −7 °C year round → 76 kW; March–mid-Dec −4 °C → 68 kW, −2 °C → 62 kW

## Electric check
- 200 A × 240 V × 80% continuous ≈ 38 kW usable, minus existing load
- Resistance: no. Heat pump alone (COP ~2 cold): no. Hybrid heat pump + fuel backup: yes
- Spare capacity: BC Hydro account peak hourly kWh, or electrician load calc
- Heat pumps (6–7 cold-climate 3-ton mini-splits): ~$60–90k; pays back only vs propane, not vs natural gas

## Fuel
- Natural gas ≈ $8–10/GJ (FortisBC small commercial, 2026) vs propane ≈ $32–40/GJ
- Season ≈ 300 GJ fuel → gas ≈ $2.7k/yr, propane ≈ $9.5–12k/yr
- Gas availability: FortisBC service request portal (address + pin) → https://servicerequestportal.fortisbc.com/

## Capex (locked scope: no fans, no controller, portable generator + manual transfer switch)
| Item | Propane | Natural gas |
|---|---|---|
| 2 × 150k BTU unit heaters (low: Modine PTP, high: BTP) | $4–10k | $4–10k |
| Venting, mounting, gas fitter | $3–6k | $3–6k |
| Electrician: heater circuits + transfer switch | $1.5–3k | $1.5–3k |
| Portable generator 7–9 kW (tri-fuel for NG) | $1.5–3k | $1.5–3k |
| Manual transfer switch | $0.5–1k | $0.5–1k |
| Permits | $0.5–1.5k | $0.5–1.5k |
| Fuel supply | regulators + line $1.5–3.5k, tank rented | FortisBC service $2–10k |
| **Total** | **$12.5–28k** | **$13–34.5k** |
- PTP150 ≈ $1.5–1.8k USD, BTP150 ≈ $3.6k USD (sale). BTP only worth it with poly tube distribution (not included).
- Bought tank: +$4–8k. Gas main extension: + tens of thousands.

## Contacts
- Propane supplier (tank, first regulator, fuel)
- FortisBC 1-888-224-2710, Construction Services (service + meter)
- Licensed gas fitter / HVAC contractor, greenhouse experience; hire first → sizes tank/meter
- Electrician (or HVAC contractor with both trades)
