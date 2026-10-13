#!/usr/bin/env python3
"""Average weekly propane cost to heat a greenhouse: 24 °C day, 20 °C night.

Geocodes the address (Nominatim), pulls 10 years of hourly temperature
and solar radiation (Open-Meteo ERA5, worldwide, no API key), averages heat demand
per ISO week, credits solar gain through the covering, converts to
propane volume and cost at 80 % efficiency.

  python3 propane_weekly_cost.py "1535 ch. Ste-Foy, Québec, QC" \
      --length-ft 100 --width-ft 30 --covering double --price-per-litre 0.85
  python3 propane_weekly_cost.py "Burlington, VT" \
      --length-ft 96 --width-ft 30 --covering single --price-per-gallon 3.20
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta

DAY_SETPOINT = 24.0
NIGHT_SETPOINT = 20.0
EFFICIENCY = 0.8
YEARS = 10
U_VALUES = {"single": 6.2, "double": 4.2}  # W/m2·°C
TRANSMITTANCE = {"single": 0.85, "double": 0.75}  # solar gain fraction
PROPANE_KWH_PER_LITRE = 6.9
LITRES_PER_US_GALLON = 3.785
USER_AGENT = "orisha-propane-estimator/1.0"


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def geocode(address):
    query = urllib.parse.urlencode({"q": address, "format": "json", "limit": 1})
    results = fetch_json(f"https://nominatim.openstreetmap.org/search?{query}")
    if not results:
        sys.exit(f"Address not found: {address}")
    return float(results[0]["lat"]), float(results[0]["lon"]), results[0]["display_name"]


def hourly_observations(latitude, longitude):
    end = date.today() - timedelta(days=7)
    start = end.replace(year=end.year - YEARS)
    query = urllib.parse.urlencode({
        "latitude": latitude, "longitude": longitude,
        "start_date": start.isoformat(), "end_date": end.isoformat(),
        "hourly": "temperature_2m,is_day,shortwave_radiation", "timezone": "auto",
    })
    data = fetch_json(f"https://archive-api.open-meteo.com/v1/archive?{query}")
    hourly = data["hourly"]
    return [
        (datetime.fromisoformat(stamp), temperature, bool(is_day), radiation or 0.0)
        for stamp, temperature, is_day, radiation in zip(
            hourly["time"], hourly["temperature_2m"], hourly["is_day"], hourly["shortwave_radiation"])
        if temperature is not None
    ]


def hourly_heat_demand_kw(temperature, is_day, radiation, u_value, envelope, floor, transmittance):
    """Envelope loss minus solar gain, floored at zero."""
    setpoint = DAY_SETPOINT if is_day else NIGHT_SETPOINT
    loss = u_value * envelope * (setpoint - temperature)
    gain = transmittance * floor * radiation
    return max(0.0, loss - gain) / 1000


def weekly_kwh(observations, u_value, envelope, floor, transmittance):
    """Mean heat demand per ISO week across all years, scaled to 168 h."""
    buckets = defaultdict(list)
    for stamp, temperature, is_day, radiation in observations:
        week = min(stamp.isocalendar()[1], 52)
        buckets[week].append(hourly_heat_demand_kw(temperature, is_day, radiation, u_value, envelope, floor, transmittance))
    return {week: 168 * sum(values) / len(values) for week, values in sorted(buckets.items())}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("address")
    parser.add_argument("--covering", choices=U_VALUES, required=True, help="single poly or double inflated poly")
    price = parser.add_mutually_exclusive_group(required=True)
    price.add_argument("--price-per-litre", type=float)
    price.add_argument("--price-per-gallon", type=float, help="US gallon")
    size = parser.add_mutually_exclusive_group(required=True)
    size.add_argument("--envelope-m2", type=float, help="roof + walls area in m2")
    size.add_argument("--length-ft", type=float, help="floor length in ft (pairs with --width-ft)")
    parser.add_argument("--width-ft", type=float)
    arguments = parser.parse_args()

    if arguments.envelope_m2:
        envelope = arguments.envelope_m2
        floor = envelope / 1.5
    else:
        if not arguments.width_ft:
            parser.error("--length-ft requires --width-ft")
        floor = arguments.length_ft * arguments.width_ft * 0.0929
        envelope = 1.5 * floor

    if arguments.price_per_gallon is not None:
        unit, litres_per_unit, price = "gal", LITRES_PER_US_GALLON, arguments.price_per_gallon
    else:
        unit, litres_per_unit, price = "L", 1.0, arguments.price_per_litre

    latitude, longitude, place = geocode(arguments.address)
    u_value = U_VALUES[arguments.covering]
    weeks = weekly_kwh(hourly_observations(latitude, longitude), u_value, envelope, floor, TRANSMITTANCE[arguments.covering])

    print(f"{place}\n{latitude:.4f}, {longitude:.4f} | {YEARS} yr history | "
          f"day {DAY_SETPOINT:.0f} °C / night {NIGHT_SETPOINT:.0f} °C | "
          f"{arguments.covering} poly U={u_value} | envelope {envelope:.0f} m2 | "
          f"${price}/{unit} | eff {EFFICIENCY}\n")
    print(f"{'week':>4} {'kWh':>7} {unit:>7} {'$':>7}")
    total_volume = total_cost = 0.0
    for week, kwh in weeks.items():
        volume = kwh / (PROPANE_KWH_PER_LITRE * EFFICIENCY) / litres_per_unit
        cost = volume * price
        total_volume += volume
        total_cost += cost
        print(f"{week:>4} {kwh:>7.0f} {volume:>7.0f} {cost:>7.0f}")
    print(f"\nyear total: {total_volume:.0f} {unit}, ${total_cost:.0f}")


if __name__ == "__main__":
    main()
