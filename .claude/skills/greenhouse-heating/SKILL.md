---
name: greenhouse-heating
description: Guide a partner farmer from "no heat" to a priced heating plan for their tomato greenhouse — peak heat load, electric vs fuel feasibility, fuel running cost, equipment type, capex range, who to call. Use when a farmer needs to install or size greenhouse heat, compare propane / natural gas / electric / heat pump, or estimate heating cost to work with Orisha.
---

# Greenhouse heating

Worked case: [EXAMPLE.md](EXAMPLE.md). Constants, prices, heater types: [REFERENCE.md](REFERENCE.md).

## 1. Gather inputs
Ask only what's missing:
- Farm + region
- Footprint, structure type, sidewall + peak height, cover
- Airtightness (unknown → 1 air change/h)
- Current heat
- Target night temp (default 21 °C: safety margin, early transplants)
- Season: transplant month → crop-out month
- Electric service: volts, amps, phase, existing load, who pays
- Fuel preference + constraints

## 2. Peak heat load
- Design low = coldest night inside the season, not year round
- Run `python3 scripts/heat_load.py --width … --length … --wall-height … --peak-height … --target … --design-low …`
- Report kW + BTU/h + felt translation (≈ 1.5 kW per plug-in space heater)

## 3. Electric feasibility
- Usable = amps × volts × 0.8 − existing load
- Existing load unknown → utility account peak hourly kWh, or electrician load calc
- Resistance fits? Heat pump (COP ≈ 2 cold) fits?
- Neither → hybrid (heat pump + fuel backup) or service upgrade (ask who'd pay)

## 4. Fuel options
- Check natural gas availability at address (utility portal / map)
- Price both fuels per GJ → season fuel cost
- Gas cheap → heat pumps rarely pay back; propane → heat pumps or condensing heaters pay back

## 5. Equipment
- 2 unit heaters, each ≈ 60% of peak (one can fail)
- Vent type + efficiency: see REFERENCE.md
- Propeller default; blower only with poly-tube distribution
- Portable generator + manual transfer switch, sized for heater fans/igniters (4–5 kW)
- Phone temperature alarm

## 6. Capex table
- Rows: heaters, venting/gas fitter, electrician, generator, transfer switch, permits, fuel supply
- Range low → high; name the swing factors (distance to meter/tank/panel, gas service line, heater type, panel room)
- Flag ballpark → get local quotes

## 7. Contacts
- Fuel supplier or gas utility
- Licensed gas fitter / HVAC contractor, greenhouse experience → hire first
- Electrician (or contractor with both trades)

## 8. Save
- Write case to `partnership/in-progress/heating-<farm>.md`
